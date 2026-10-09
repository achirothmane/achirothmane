#!/usr/bin/env python3
"""Read-only, independent policy oracle for public-scope Portfolio Dot shadow decisions.

No model calls, network access, repository mutations, or execution authority.
A passing policy comparison is NOT evidence of decision quality or Dots autonomy.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "portfolio"
SOURCES = (
    "evidence-baseline.json",
    "freshness-report.json",
    "priority-report.json",
    "execution-queue.yaml",
    "dot-handoff.yaml",
)
REFERENCE = P / "shadow-reference.json"
DENIED_EFFECTS = frozenset({"EXECUTE", "MERGE", "PUBLISH", "SPEND", "SEND", "DELETE", "CHANGE_SECRETS"})
READ_ONLY_ACTIONS = frozenset({"OBSERVE", "RECOMMEND"})
MAX_SNAPSHOT_AGE = 7


def load_inputs(root: Path = P) -> tuple[dict, str]:
    docs = {}
    hashed = hashlib.sha256()
    for name in SOURCES:
        payload = (root / name).read_bytes()
        hashed.update(name.encode("ascii") + b"\0" + payload + b"\0")
        docs[name] = (yaml.safe_load(payload) if name.endswith(".yaml") else json.loads(payload))
    return docs, hashed.hexdigest()


def verify_sources(docs: dict, *, as_of: dt.date) -> tuple[dict, dict, dict, list[str]]:
    e = docs["evidence-baseline.json"]
    f = docs["freshness-report.json"]
    p = docs["priority-report.json"]
    if e.get("scope") != "public-evidence-only":
        raise ValueError("Public evidence scope is not verified")
    if not e.get("projects") or not p.get("projects") or not f.get("projects"):
        raise ValueError("Missing source projects")
    if p.get("as_of") != f.get("as_of"):
        raise ValueError("Priority and freshness snapshots disagree")
    if (as_of - dt.date.fromisoformat(p["as_of"])).days < 0:
        raise ValueError("Report date lies in the future")
    if (as_of - dt.date.fromisoformat(e["captured_on"])).days < 0:
        raise ValueError("Evidence date lies in the future")
    ids_f = [v["id"] for v in f["projects"]]
    ids_p = [v["id"] for v in p["projects"]]
    if len(ids_p) != len(set(ids_p)) or len(ids_f) != len(set(ids_f)) or set(ids_p) != set(ids_f):
        raise ValueError("Project sets diverge between priority and freshness")
    if p.get("lane_counts") and sum(p["lane_counts"].values()) != len(ids_p):
        raise ValueError("Priority lane counts are inconsistent")
    by_p = {row["id"]: row for row in p["projects"]}
    by_f = {row["id"]: row for row in f["projects"]}
    public = {}
    for entry in e["projects"]:
        repo = entry["repository"]
        if entry.get("visibility") != "public" or repo in public or not repo.startswith("achirothmane/"):
            raise ValueError("Invalid or repeated public evidence entry")
        candidates = [item for item in by_p.values() if item.get("repository") == repo]
        if len(candidates) != 1:
            raise ValueError("Public evidence has no unique portfolio project binding")
        proj = candidates[0]
        freshness = by_f[proj["id"]]
        if proj.get("freshness") != freshness.get("freshness"):
            raise ValueError("Cross-report freshness mismatch")
        public[proj["id"]] = (entry, proj, freshness)
    diagnostics = []
    queue = docs["execution-queue.yaml"]["execution_queue"]
    handoff = docs["dot-handoff.yaml"]["dot_handoff"]
    if queue.get("runnable_count") != sum(x.get("state") == "READY" for x in queue.get("items", [])):
        diagnostics.append("RUNNABLE_COUNT_DRIFT")
    merged = {
        (row.get("project"), row.get("target_pull_request"))
        for row in queue.get("items", [])
        if (row.get("observed_2026_10_09") or {}).get("pr7_merged") is True
    }
    if any((item.get("project"), item.get("pull_request")) in merged for item in
           handoff.get("current", {}).get("waiting_human_approval", [])):
        diagnostics.append("STALE_HANDOFF_MERGE_APPROVAL")
    return public, by_p, by_f, diagnostics


def report(docs: dict, digest: str, as_of: dt.date, candidate: dict | None = None) -> dict:
    public, by_p, by_f, diagnostics = verify_sources(docs, as_of=as_of)
    evidence_date = dt.date.fromisoformat(docs["evidence-baseline.json"]["captured_on"])
    report_date = dt.date.fromisoformat(docs["priority-report.json"]["as_of"])
    stale = (as_of - evidence_date).days > MAX_SNAPSHOT_AGE or (as_of - report_date).days > MAX_SNAPSHOT_AGE
    if stale:
        diagnostics.append("SNAPSHOT_EXPIRED")
    rows = []
    for project_id, (entry, priority, freshness) in sorted(public.items()):
        row_codes = []
        if freshness["freshness"] != "FRESH":
            row_codes.append("FRESHNESS_REVERIFY")
        if priority["lane"] in ("PARKED", "CLOSED", "REVERIFY"):
            row_codes.append("PRIORITY_NOT_ADMITTED")
        if any(entry.get(field) == "UNKNOWN" for field in ("deployed", "external_use", "paid_revenue")):
            row_codes.append("OUTCOME_UNPROVEN")
        rows.append({
            "project_id": project_id,
            "priority_lane": priority["lane"],
            "freshness": freshness["freshness"],
            "reference_authority": "OBSERVE_ONLY",
            "outcome_evidence": "UNKNOWN",
            "reason_codes": sorted(set(row_codes)),
        })

    output = {
        "schema_version": 1,
        "mode": "SHADOW_POLICY_ONLY",
        "as_of": as_of.isoformat(),
        "snapshot_sha256": digest,
        "scope": "PUBLIC_PROJECTS_ONLY",
        "projects_total": len(by_p),
        "public_projects_checked": len(public),
        "snapshot_state": "REVERIFY" if stale else "FRESH_WITH_LIMITS",
        "diagnostic_codes": sorted(set(diagnostics)),
        "reference_decisions": rows,
        "live_dots_candidate_count": 0,
        "model_quality_score": "NOT_MEASURED",
        "manager_autonomy": "NOT_AUTHORIZED",
    }
    if candidate is not None:
        output["candidate_evaluation"] = evaluate(candidate, digest=digest, public=public, stale=stale)
    return output


def evaluate(candidate: dict, *, digest: str, public: dict, stale: bool) -> dict:
    if not isinstance(candidate, dict) or candidate.get("schema_version") != 1:
        raise ValueError("Invalid candidate schema")
    if candidate.get("snapshot_sha256") != digest:
        return {"state": "BLOCKED_SNAPSHOT_BINDING", "evaluated": 0, "accepted": 0,
                "blocked": 0, "unknown": 0, "decisions": []}
    proposals = candidate.get("proposals")
    if not isinstance(proposals, list) or len(proposals) > 100:
        raise ValueError("Candidates must contain at most 100 proposals")
    decisions = []
    counts = {"accepted": 0, "blocked": 0, "unknown": 0}
    for idx, item in enumerate(proposals):
        reasons = []
        if not isinstance(item, dict):
            item = {}
            reasons.append("INVALID_PROPOSAL")
        project_id = item.get("project_id")
        action = item.get("action")
        entry = public.get(project_id)
        if entry is None:
            reasons.append("OUTSIDE_PUBLIC_SCOPE")
        if action not in READ_ONLY_ACTIONS:
            reasons.append("NO_EXECUTION_AUTHORITY" if action in DENIED_EFFECTS else "UNKNOWN_ACTION")
        if item.get("asserted_paid_revenue") not in (None, "UNKNOWN"):
            reasons.append("UNSUPPORTED_REVENUE_CLAIM")
        if item.get("asserted_deployed") not in (None, "UNKNOWN"):
            reasons.append("UNSUPPORTED_DEPLOYMENT_CLAIM")
        if item.get("new_hard_dependency"):
            reasons.append("UNAPPROVED_DEPENDENCY")
        if item.get("claims_ready") is True:
            reasons.append("READINESS_NOT_AUTHORIZED")
        if stale:
            reasons.append("SNAPSHOT_EXPIRED")
        if entry:
            _, priority, freshness = entry
            if freshness["freshness"] != "FRESH":
                reasons.append("FRESHNESS_REVERIFY")
            if priority["lane"] in ("CLOSED", "PARKED", "REVERIFY"):
                reasons.append("PROJECT_NOT_ADMITTED")
        if action == "RECOMMEND" and not item.get("evidence_refs"):
            reasons.append("RECOMMENDATION_LACKS_EVIDENCE")
        # Never echo unverified candidate content or any nonpublic project identifier.
        state = ("BLOCKED" if any(code not in ("RECOMMENDATION_LACKS_EVIDENCE", "FRESHNESS_REVERIFY")
                                    for code in reasons)
                 else "UNKNOWN" if reasons else "POLICY_ADMISSIBLE_ONLY")
        category = "blocked" if state == "BLOCKED" else "unknown" if state == "UNKNOWN" else "accepted"
        counts[category] += 1
        decisions.append({"ordinal": idx + 1,
                          "public_project_id": project_id if entry is not None else None,
                          "state": state, "reason_codes": sorted(set(reasons)),
                          "may_execute": False})
    return {"state": "SCOPED_POLICY_COMPARISON_ONLY", "evaluated": len(proposals),
            **counts, "decisions": decisions,
            "decision_quality": "NOT_MEASURED", "human_review_required": True}


def main() -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument("--candidate", type=Path, help="Untrusted Dot proposal JSON; never executable")
    cli.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    cli.add_argument("--write-reference", action="store_true")
    cli.add_argument("--check-reference", action="store_true")
    args = cli.parse_args()
    if args.write_reference and args.check_reference:
        cli.error("Select write or check, not both")
    docs, digest = load_inputs()
    cand = json.loads(args.candidate.read_text(encoding="utf-8")) if args.candidate else None
    result = report(docs, digest, dt.date.fromisoformat(args.as_of), cand)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_reference:
        if cand is not None:
            cli.error("Cannot persist arbitrary candidate content into public reference")
        REFERENCE.write_text(payload, encoding="utf-8")
    elif args.check_reference:
        if cand is not None or not REFERENCE.is_file() or REFERENCE.read_text(encoding="utf-8") != payload:
            raise ValueError("Shadow reference drift or inadmissible candidate")
    else:
        print(payload)
    if result["snapshot_state"] == "REVERIFY":
        raise ValueError("Stale portfolio snapshot: require re-verification")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError, OSError, yaml.YAMLError, json.JSONDecodeError) as ex:
        raise SystemExit("SHADOW_ORACLE_FAIL_CLOSED: " + str(ex))
