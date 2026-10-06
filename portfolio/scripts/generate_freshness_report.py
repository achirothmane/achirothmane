#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PORTFOLIO = ROOT / "portfolio"
INDEX_PATH = PORTFOLIO / "index.yaml"
POLICY_PATH = PORTFOLIO / "freshness-policy.yaml"
REPORT_MD = PORTFOLIO / "FRESHNESS-REPORT.md"
REPORT_JSON = PORTFOLIO / "freshness-report.json"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected mapping")
    return value


def parse_date(value: object) -> date | None:
    if value in (None, "", "UNKNOWN"):
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def contains_unknown(value: object) -> int:
    if isinstance(value, str):
        return 1 if value.strip().upper() == "UNKNOWN" else 0
    if isinstance(value, list):
        return sum(contains_unknown(item) for item in value)
    if isinstance(value, dict):
        return sum(contains_unknown(item) for item in value.values())
    return 0


def policy_for(status: str, policy: dict) -> tuple[str, dict]:
    for class_name, config in policy.get("classes", {}).items():
        if status in (config.get("statuses") or []):
            return class_name, config
    return "default", policy["default"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--as-of",
        default=datetime.now(timezone.utc).date().isoformat(),
        help="UTC reference date in YYYY-MM-DD format",
    )
    args = parser.parse_args()
    as_of = date.fromisoformat(args.as_of)

    index = load_yaml(INDEX_PATH)["portfolio"]
    policy = load_yaml(POLICY_PATH)["freshness_policy"]

    records = []
    by_id = {}
    for rel in index.get("project_records", []):
        path = PORTFOLIO / rel
        project = load_yaml(path).get("project")
        if not isinstance(project, dict):
            raise ValueError(f"{path}: missing project record")
        project_id = str(project.get("id") or "")
        if not project_id:
            raise ValueError(f"{path}: missing project.id")

        status = str(project.get("status") or "UNKNOWN")
        class_name, thresholds = policy_for(status, policy)
        verified = parse_date(project.get("last_verified"))
        unknown_count = contains_unknown(project)

        if verified is None:
            age_days = None
            freshness = "UNKNOWN"
        else:
            age_days = (as_of - verified).days
            if age_days < 0:
                raise ValueError(f"{project_id}: last_verified is in the future")
            fresh_through = int(thresholds["fresh_through_days"])
            stale_after = int(thresholds["stale_after_days"])
            if age_days <= fresh_through:
                freshness = "FRESH"
            elif age_days <= stale_after:
                freshness = "AGING"
            else:
                freshness = "STALE"

        record = {
            "id": project_id,
            "repository": project.get("repository"),
            "status": status,
            "freshness_class": class_name,
            "freshness": freshness,
            "last_verified": None if verified is None else verified.isoformat(),
            "age_days": age_days,
            "unknown_value_count": unknown_count,
            "completeness": "INCOMPLETE" if unknown_count else "COMPLETE",
            "dependencies": list(project.get("dependencies") or []),
        }
        records.append(record)
        by_id[project_id] = record

    stale_upstream = []
    for record in records:
        for dependency in record["dependencies"]:
            dep = by_id.get(str(dependency))
            if dep and dep["freshness"] in {"STALE", "UNKNOWN"}:
                stale_upstream.append(
                    {
                        "project": record["id"],
                        "dependency": dep["id"],
                        "dependency_freshness": dep["freshness"],
                    }
                )

    counts = {state: 0 for state in policy["states"]}
    for record in records:
        counts[record["freshness"]] += 1

    report = {
        "schema_version": 1,
        "as_of": as_of.isoformat(),
        "policy": "freshness-policy.yaml",
        "project_count": len(records),
        "freshness_counts": counts,
        "incomplete_project_count": sum(1 for r in records if r["completeness"] == "INCOMPLETE"),
        "dependency_freshness_risks": stale_upstream,
        "projects": sorted(records, key=lambda r: (r["freshness"], r["id"])),
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Freshness Report",
        "",
        "> Generated from project `last_verified` values and `portfolio/freshness-policy.yaml`.",
        "> Freshness measures recency, not truth completeness.",
        "",
        f"**As of:** {as_of.isoformat()}  ",
        f"**Projects:** {len(records)}  ",
        f"**FRESH:** {counts['FRESH']}  ",
        f"**AGING:** {counts['AGING']}  ",
        f"**STALE:** {counts['STALE']}  ",
        f"**UNKNOWN freshness:** {counts['UNKNOWN']}  ",
        f"**Incomplete records (contain UNKNOWN values):** {report['incomplete_project_count']}",
        "",
        "## Action semantics",
        "",
        "| Freshness | Meaning | Material action |",
        "|---|---|---|",
        "| FRESH | recently verified for its policy class | normal gates apply |",
        "| AGING | still usable, but current-state-sensitive decisions should reverify | verify when material |",
        "| STALE | verification age exceeded | reverify first |",
        "| UNKNOWN | no usable verification date | reverify first |",
        "",
        "## Projects",
        "",
        "| Project | Status | Class | Freshness | Age | Completeness |",
        "|---|---|---|---|---:|---|",
    ]

    order = {"STALE": 0, "UNKNOWN": 1, "AGING": 2, "FRESH": 3}
    for record in sorted(records, key=lambda r: (order[r["freshness"]], r["id"])):
        age = "—" if record["age_days"] is None else str(record["age_days"])
        lines.append(
            f"| `{record['id']}` | {record['status']} | {record['freshness_class']} | "
            f"**{record['freshness']}** | {age} | {record['completeness']} |"
        )

    lines += ["", "## Dependency freshness risks", ""]
    if stale_upstream:
        for risk in stale_upstream:
            lines.append(
                f"- `{risk['project']}` depends on `{risk['dependency']}`, whose state is "
                f"**{risk['dependency_freshness']}**."
            )
    else:
        lines.append("No registered hard dependency currently points to STALE or UNKNOWN upstream state.")

    lines += [
        "",
        "## Invariant",
        "",
        "> A stale record is not automatically false; it is **inadmissible as current-state evidence** until reverified when a material decision depends on it.",
        "",
        "A FRESH record may still be incomplete. `UNKNOWN` values remain unknown even when the record itself is fresh.",
        "",
    ]

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
