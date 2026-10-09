#!/usr/bin/env python3
"""Export a tightly-scoped real Portfolio snapshot in the Go D2 JSON contract.

Input is the checked-out, date-valid public Portfolio state. This exporter never
creates READY tasks, authorizes effects, calls a model or mutates its sources.
Only evidence-allowlisted public project IDs enter the reasoning projection.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

import yaml
import shadow_management
import shadow_live_gate

PORTFOLIO = Path(__file__).resolve().parents[1]
TARGET_WORK_ITEM = "dots-runtime-evidence-observe-006"
SOURCE_BINDINGS = (
    "portfolio/evidence-baseline.json",
    "portfolio/shadow-reference.json",
    "portfolio/s1-readiness.json",
    "portfolio/execution-queue.yaml",
    "portfolio/priority-report.json",
    "portfolio/freshness-report.json",
    "portfolio/dot-handoff.yaml",
    "portfolio/priority-policy.yaml",
    "portfolio/index.yaml",
    "portfolio/dependency-graph.json",
)


def canonical(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def build_snapshot(root: Path, date: dt.date) -> dict:
    docs, input_digest = shadow_management.load_inputs(root / "portfolio")
    s1 = shadow_live_gate.source_preflight(docs, input_digest, as_of=date)
    if s1["state"] != "READY_FOR_SEPARATE_RUNTIME_ATTESTATION":
        raise ValueError("S1 admission failed: " + s1["state"])
    if s1["runnable_count"] != 1 or s1["provider_calls_performed"] != 0 or s1["actual_dots_trace_count"] != 0:
        raise ValueError("S1 must have exactly one non-paid and unexecuted work item")

    report = json.loads((root / "portfolio/priority-report.json").read_text(encoding="utf-8"))
    freshness = json.loads((root / "portfolio/freshness-report.json").read_text(encoding="utf-8"))
    evidence = json.loads((root / "portfolio/evidence-baseline.json").read_text(encoding="utf-8"))
    handoff = yaml.safe_load((root / "portfolio/dot-handoff.yaml").read_text(encoding="utf-8"))["dot_handoff"]
    queue = yaml.safe_load((root / "portfolio/execution-queue.yaml").read_text(encoding="utf-8"))["execution_queue"]
    policy = yaml.safe_load((root / "portfolio/priority-policy.yaml").read_text(encoding="utf-8"))["priority_policy"]
    index = yaml.safe_load((root / "portfolio/index.yaml").read_text(encoding="utf-8"))["portfolio"]
    graph = json.loads((root / "portfolio/dependency-graph.json").read_text(encoding="utf-8"))
    public = {x["id"] for x in evidence["projects"] if x["visibility"] == "public"}
    by_priority = {x["id"]: x for x in report["projects"]}
    by_freshness = {x["id"]: x for x in freshness["projects"]}
    ready = [x for x in queue["items"] if x.get("state") == "READY"]
    if len(ready) != 1 or ready[0]["id"] != TARGET_WORK_ITEM:
        raise ValueError("S1 ready work item identity changed")
    item = ready[0]
    if (item["project"] not in public or item["authority"] != "OBSERVE" or
            by_priority[item["project"]]["lane"] != "NOW" or
            by_freshness[item["project"]]["freshness"] != "FRESH" or
            item["project"] != "governed-agent-runtime" or
            item.get("provider_cost_approved") is not False or
            item.get("external_effects_approved") is not False):
        raise ValueError("Work item does not have bounded public OBSERVE admission")
    if (handoff["current"]["runnable_items"] != [TARGET_WORK_ITEM] or
            sorted(handoff["current"]["now_projects"]) != sorted(x["id"] for x in report["projects"] if x["lane"] == "NOW")):
        raise ValueError("Handoff and priority disagree")

    final_actions = handoff["human_authority"]["final_on"]
    if not all(x in final_actions for x in ("merge", "paid-spend", "external-messaging", "destructive-change")):
        raise ValueError("Missing human final authority")
    now_ids = sorted(public & set(handoff["current"]["now_projects"]))
    if now_ids != ["governed-agent-runtime"]:
        raise ValueError("Public-only NOW scope has drifted")
    if report["lane_counts"]["NOW"] > policy["wip"]["now_cap"]:
        raise ValueError("Portfolio NOW WIP over cap")

    projected = {
        "structural_review": str(index["last_structural_review"]),
        "now_projects": now_ids,
        "now_project_state": [{
            "id": project_id,
            "freshness": by_freshness[project_id]["freshness"],
            "completeness": by_freshness[project_id]["completeness"],
        } for project_id in now_ids],
        "runnable_items": [{
            "id": item["id"],
            "project": item["project"],
            "authority": "OBSERVE",
            "objective": item["objective"],
            "evidence_required": item["evidence_required"],
            "stop_conditions": item["stop_conditions"],
        }],
        "verified_contracts": [{
            "id": edge["id"], "source": edge["source"], "target": edge["target"],
            "relations": edge["relations"], "hard_dependency": edge["hard_dependency"],
        } for edge in graph["edges"] if edge["source"] in public and edge["target"] in public],
        "human_final_on": final_actions,
        "execution_principle": "priority-does-not-equal-execution-authority",
        "wip": {
            "now_cap": policy["wip"]["now_cap"],
            "now_count": report["lane_counts"]["NOW"],
            "next_cap": policy["wip"]["next_cap"],
            "next_count": report["lane_counts"]["NEXT"],
        },
    }
    bindings = []
    for relpath in SOURCE_BINDINGS:
        source = root / relpath
        bindings.append({
            "path": relpath,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        })
    snapshot = {
        "schema_version": 1,
        "state": "EXECUTABLE",  # Go D2: eligible for a DECISION only, not any tool or effect.
        "reasons": [],
        "source_bindings": bindings,
        "projection": projected,
    }
    snapshot["snapshot_digest"] = hashlib.sha256(canonical(snapshot)).hexdigest()
    return snapshot


def main() -> int:
    arg = argparse.ArgumentParser()
    arg.add_argument("--root", type=Path, default=PORTFOLIO.parent)
    arg.add_argument("--output", type=Path, required=True)
    arg.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    args = arg.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    if root in output.parents:
        raise ValueError("Sealed context must be written OUTSIDE public checkout (never commit it)")
    snapshot = build_snapshot(root, dt.date.fromisoformat(args.as_of))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical(snapshot) + b"\n")
    print(json.dumps({
        "result": "REAL_PUBLIC_CONTEXT_SEALED_FOR_OBSERVATION_ONLY",
        "snapshot_digest": snapshot["snapshot_digest"],
        "work_item_count": len(snapshot["projection"]["runnable_items"]),
        "project_scope": "public-audited-only",
        "reasoner_calls": 0,
        "paid_provider_calls": 0,
        "tool_dispatch_authority": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, ValueError, OSError, TypeError, yaml.YAMLError, json.JSONDecodeError) as error:
        raise SystemExit("REAL_DOTS_CONTEXT_FAIL_CLOSED: " + str(error))
