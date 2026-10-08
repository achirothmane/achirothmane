#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


class SnapshotError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SnapshotError(f"missing required source: {path}") from exc
    if not isinstance(value, dict):
        raise SnapshotError(f"{path}: expected mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SnapshotError(f"missing required source: {path}") from exc
    if not isinstance(value, dict):
        raise SnapshotError(f"{path}: expected object")
    return value


def sha256_file(path: Path) -> str:
    try:
        payload = path.read_bytes()
    except FileNotFoundError as exc:
        raise SnapshotError(f"missing required source: {path}") from exc
    return hashlib.sha256(payload).hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def safe_rel(root: Path, path: Path) -> str:
    resolved_root = root.resolve()
    resolved = path.resolve()
    try:
        return resolved.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise SnapshotError(f"source escapes repository root: {path}") from exc


def build_snapshot(root: Path) -> dict[str, Any]:
    root = root.resolve()
    portfolio = root / "portfolio"

    index_path = portfolio / "index.yaml"
    freshness_path = portfolio / "freshness-report.json"
    priority_path = portfolio / "priority-report.json"
    graph_path = portfolio / "dependency-graph.json"
    queue_path = portfolio / "execution-queue.yaml"
    policy_path = portfolio / "execution-policy.yaml"
    handoff_path = portfolio / "dot-handoff.yaml"
    operating_contract_path = portfolio / "DOT-OPERATING-CONTRACT.md"
    system_map_path = root / "SYSTEM-MAP.md"

    index_doc = load_yaml(index_path)
    index = index_doc.get("portfolio")
    if not isinstance(index, dict):
        raise SnapshotError("portfolio/index.yaml: missing portfolio mapping")

    freshness = load_json(freshness_path)
    priority = load_json(priority_path)
    graph = load_json(graph_path)
    queue_doc = load_yaml(queue_path)
    policy_doc = load_yaml(policy_path)
    handoff_doc = load_yaml(handoff_path)

    queue = queue_doc.get("execution_queue")
    policy = policy_doc.get("execution_policy")
    handoff = handoff_doc.get("dot_handoff")
    if not isinstance(queue, dict) or not isinstance(policy, dict) or not isinstance(handoff, dict):
        raise SnapshotError("execution queue, policy, and handoff must be mappings")

    project_records = list(index.get("project_records") or [])
    contract_records = list(index.get("contract_records") or [])

    source_paths = [
        system_map_path,
        index_path,
        freshness_path,
        priority_path,
        graph_path,
        queue_path,
        policy_path,
        handoff_path,
        operating_contract_path,
    ]
    source_paths += [portfolio / str(rel) for rel in project_records]
    source_paths += [portfolio / str(rel) for rel in contract_records]

    seen: set[str] = set()
    bindings: list[dict[str, str]] = []
    for path in source_paths:
        rel = safe_rel(root, path)
        if rel in seen:
            continue
        seen.add(rel)
        bindings.append({"path": rel, "sha256": sha256_file(path)})
    bindings.sort(key=lambda item: item["path"])

    structural_review = str(index.get("last_structural_review") or "UNKNOWN")
    reasons: list[str] = []

    if structural_review in {"", "UNKNOWN"}:
        reasons.append("STRUCTURAL_REVIEW_UNKNOWN")
    if str(freshness.get("as_of") or "UNKNOWN") != structural_review:
        reasons.append("FRESHNESS_AS_OF_MISMATCH")
    if str(priority.get("as_of") or "UNKNOWN") != structural_review:
        reasons.append("PRIORITY_AS_OF_MISMATCH")
    if str(graph.get("structural_review") or "UNKNOWN") != structural_review:
        reasons.append("DEPENDENCY_GRAPH_REVIEW_MISMATCH")

    wip = priority.get("wip") or {}
    if int(wip.get("now_overflow") or 0) > 0:
        reasons.append("NOW_WIP_OVERFLOW")
    if int(wip.get("next_overflow") or 0) > 0:
        reasons.append("NEXT_WIP_OVERFLOW")

    priority_projects = {
        str(row.get("id")): row
        for row in (priority.get("projects") or [])
        if isinstance(row, dict) and row.get("id")
    }
    freshness_projects = {
        str(row.get("id")): row
        for row in (freshness.get("projects") or [])
        if isinstance(row, dict) and row.get("id")
    }

    now_projects = sorted(
        project_id for project_id, row in priority_projects.items()
        if row.get("lane") == "NOW"
    )
    if "portfolio-dot" not in now_projects:
        reasons.append("PORTFOLIO_DOT_NOT_NOW")

    now_state: list[dict[str, Any]] = []
    for project_id in now_projects:
        fresh = freshness_projects.get(project_id)
        if fresh is None:
            reasons.append(f"NOW_PROJECT_FRESHNESS_MISSING:{project_id}")
            now_state.append({"id": project_id, "freshness": "UNKNOWN", "completeness": "UNKNOWN"})
            continue
        fresh_state = str(fresh.get("freshness") or "UNKNOWN")
        completeness = str(fresh.get("completeness") or "UNKNOWN")
        now_state.append({
            "id": project_id,
            "freshness": fresh_state,
            "completeness": completeness,
        })
        if fresh_state not in {"FRESH", "AGING"}:
            reasons.append(f"NOW_PROJECT_INADMISSIBLE_FRESHNESS:{project_id}:{fresh_state}")

    if freshness.get("dependency_freshness_risks"):
        reasons.append("HARD_DEPENDENCY_FRESHNESS_RISK")

    items = [item for item in (queue.get("items") or []) if isinstance(item, dict)]
    ready_items = [item for item in items if item.get("state") == "READY"]
    declared_runnable = int(queue.get("runnable_count") or 0)
    if declared_runnable != len(ready_items):
        reasons.append("RUNNABLE_COUNT_MISMATCH")

    runnable_projection: list[dict[str, Any]] = []
    for item in sorted(ready_items, key=lambda row: str(row.get("id") or "")):
        item_id = str(item.get("id") or "")
        project_id = str(item.get("project") or "")
        authority = str(item.get("authority") or "")
        objective = str(item.get("objective") or "")
        evidence_required = list(item.get("evidence_required") or [])
        stop_conditions = list(item.get("stop_conditions") or [])
        if not item_id or not project_id or not authority or not objective:
            reasons.append(f"READY_ITEM_INCOMPLETE:{item_id or 'UNKNOWN'}")
        if project_id not in now_projects:
            reasons.append(f"READY_ITEM_PROJECT_NOT_NOW:{item_id}:{project_id}")
        if not evidence_required:
            reasons.append(f"READY_ITEM_NO_EVIDENCE_GATE:{item_id}")
        if not stop_conditions:
            reasons.append(f"READY_ITEM_NO_STOP_CONDITIONS:{item_id}")
        runnable_projection.append({
            "id": item_id,
            "project": project_id,
            "authority": authority,
            "objective": objective,
            "evidence_required": evidence_required,
            "stop_conditions": stop_conditions,
        })

    edges = []
    for edge in graph.get("edges") or []:
        if not isinstance(edge, dict):
            continue
        edges.append({
            "id": edge.get("id"),
            "source": edge.get("source"),
            "target": edge.get("target"),
            "relations": list(edge.get("relations") or []),
            "hard_dependency": bool(edge.get("hard_dependency")),
        })
    edges.sort(key=lambda row: str(row.get("id") or ""))

    human_final_on = list(((handoff.get("human_authority") or {}).get("final_on") or []))
    if not human_final_on:
        reasons.append("HUMAN_AUTHORITY_BOUNDARY_MISSING")

    projection = {
        "structural_review": structural_review,
        "now_projects": now_projects,
        "now_project_state": now_state,
        "runnable_items": runnable_projection,
        "verified_contracts": edges,
        "human_final_on": human_final_on,
        "execution_principle": policy.get("principle"),
        "wip": {
            "now_cap": wip.get("now_cap"),
            "now_count": wip.get("now_count"),
            "next_cap": wip.get("next_cap"),
            "next_count": wip.get("next_count"),
        },
    }

    snapshot: dict[str, Any] = {
        "schema_version": 1,
        "state": "EXECUTABLE" if not reasons else "NON_EXECUTABLE",
        "reasons": sorted(set(reasons)),
        "source_bindings": bindings,
        "projection": projection,
    }
    snapshot["snapshot_digest"] = canonical_digest(snapshot)
    return snapshot


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--require-executable", action="store_true")
    args = parser.parse_args()

    snapshot = build_snapshot(args.root)
    payload = json.dumps(snapshot, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    if args.require_executable and snapshot["state"] != "EXECUTABLE":
        raise SystemExit(
            "Portfolio Context Snapshot is NON_EXECUTABLE: "
            + ", ".join(snapshot["reasons"])
        )


if __name__ == "__main__":
    main()
