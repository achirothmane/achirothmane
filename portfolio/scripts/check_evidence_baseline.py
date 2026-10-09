#!/usr/bin/env python3
"""Check the public-only portfolio evidence snapshot and render its System Map view.

No network access, credentials, private repo inspection, or autonomous GitHub mutations.
Default: validate + compare the committed System Map table.
Use --write to update only the marked table, after reviewing the source JSON.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "portfolio" / "evidence-baseline.json"
MAP = ROOT / "SYSTEM-MAP.md"
BEGIN = "<!-- PORTFOLIO-EVIDENCE:BEGIN -->"
END = "<!-- PORTFOLIO-EVIDENCE:END -->"
PUBLIC_REPOS = {
    "achirothmane/agent-deal-exchange",
    "achirothmane/github-test-reporter",
    "achirothmane/governed-agent-runtime",
    "achirothmane/marketing-os",
    "achirothmane/releaseguard-n8n",
}
MAIN = {"MAIN_IMPLEMENTED", "BOOTSTRAP_ONLY", "INHERITED_PLUS_ADAPTER"}
TEST = {"EVIDENCE_LINKED_SCOPED", "BRANCH_ONLY_EVIDENCE", "UNKNOWN"}
MAX_AGE_DAYS = 7


def validate(data: dict) -> int:
    if data.get("schema_version") != 1 or data.get("scope") != "public-evidence-only":
        raise ValueError("Unsupported schema or privacy scope")
    date = dt.date.fromisoformat(data["captured_on"])
    age = (dt.datetime.now(dt.timezone.utc).date() - date).days
    if age < 0:
        raise ValueError("Snapshot date is in the future")
    if not isinstance(data.get("projects"), list) or not data["projects"]:
        raise ValueError("Missing projects")
    seen = set()
    for p in data["projects"]:
        repo = p["repository"]
        if (p["id"] in seen or repo not in PUBLIC_REPOS
                or p.get("visibility") != "public"):
            raise ValueError("Duplicate, unapproved, or nonpublic project: " + repo)
        seen.add(p["id"])
        if p["id"] != repo.split("/")[-1]:
            raise ValueError("Project ID differs from repository: " + repo)
        if p["main_status"] not in MAIN or p["test_status"] not in TEST:
            raise ValueError("Unknown technical state: " + repo)
        for state in ("deployed", "external_use", "paid_revenue"):
            if p.get(state) != "UNKNOWN":
                raise ValueError("Unsupported economic/production claim without independent proof: " + repo)
        for field in ("main_evidence", "test_evidence", "outstanding"):
            links = p.get(field)
            if not isinstance(links, list):
                raise ValueError("Missing evidence list " + field + ": " + repo)
            for url in links:
                parsed = urlparse(url)
                if (parsed.scheme != "https" or parsed.netloc != "github.com"
                        or not parsed.path.startswith("/" + repo + "/")
                        or parsed.username or parsed.password or parsed.query
                        or parsed.fragment):
                    raise ValueError("Unapproved evidence link for " + repo)
        if p["test_status"] != "UNKNOWN" and not p["test_evidence"]:
            raise ValueError("Test claim lacks a test link: " + repo)
        if not p["main_evidence"]:
            raise ValueError("Main claim lacks source reference: " + repo)
        if not isinstance(p.get("boundary"), str) or not p["boundary"].strip():
            raise ValueError("Boundary missing: " + repo)
        if "|" in p["boundary"] or "\n" in p["boundary"]:
            raise ValueError("Unsafe markdown field for " + repo)
    return age


def render(data: dict) -> str:
    rows = [
        "## Evidence baseline (public repositories only)",
        "",
        "Source: [portfolio/evidence-baseline.json](portfolio/evidence-baseline.json).",
        "Snapshot: **" + data["captured_on"] + "**. This is not live status or an all-repository inventory.",
        "",
        "| Public project | On default branch | Test evidence | Deployed | External use | Paid revenue |",
        "|---|---|---|---|---|---|",
    ]
    for p in sorted(data["projects"], key=lambda v: v["id"]):
        link = "[`" + p["id"] + "`](https://github.com/" + p["repository"] + ")"
        vals = [link, p["main_status"], p["test_status"],
                p["deployed"], p["external_use"], p["paid_revenue"]]
        rows.append("| " + " | ".join(vals) + " |")
    rows += [
        "",
        "**Interpretation:** Tests on open PR branches do not establish main readiness. "
        "Linked CI evidence is scoped; this audit did not rerun it. UNKNOWN is not zero.",
        "All newly recorded repository-level evidence is public-only; private repository "
        "details require a separate private evidence store and explicit publication review.",
        "Before operational decisions, recheck links, PR state, commit SHA, and runtime evidence.",
    ]
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Regenerate marked System Map section")
    parser.add_argument("--fail-on-stale", action="store_true", help="Fail if older than 7 UTC days")
    args = parser.parse_args()

    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    age = validate(data)
    body = MAP.read_text(encoding="utf-8")
    if body.count(BEGIN) != 1 or body.count(END) != 1:
        raise ValueError("System Map missing unique evidence markers")
    replacement = BEGIN + "\n" + render(data) + "\n" + END
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), flags=re.S)
    expected = pattern.sub(lambda _: replacement, body)
    if args.write:
        if expected != body:
            MAP.write_text(expected, encoding="utf-8")
            print("Updated public evidence section in SYSTEM-MAP.md")
    elif expected != body:
        print("ERROR: System Map evidence section differs from JSON; use --write", file=sys.stderr)
        return 2
    status = "FRESH" if age <= MAX_AGE_DAYS else "AGING"
    print("Evidence baseline valid: " + str(len(data["projects"])) +
          " public projects; age=" + str(age) + " days; " + status)
    if args.fail_on_stale and age > MAX_AGE_DAYS:
        print("ERROR: public snapshot must be reverified", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
