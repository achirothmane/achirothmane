#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PORTFOLIO = ROOT / "portfolio"

INDEX = PORTFOLIO / "index.yaml"
FRESHNESS = PORTFOLIO / "freshness-report.json"
POLICY = PORTFOLIO / "priority-policy.yaml"
DIRECTIVES = PORTFOLIO / "priority-directives.yaml"
REPORT_JSON = PORTFOLIO / "priority-report.json"
REPORT_MD = PORTFOLIO / "PRIORITY-REPORT.md"

LANE_ORDER = {
    "NOW": 0,
    "NEXT": 1,
    "WATCH": 2,
    "PARKED": 3,
    "REVERIFY": 4,
    "CLOSED": 5,
}


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected mapping")
    return value


def known_gate(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    return bool(text and text.upper() != "UNKNOWN")


def nonempty(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return bool(str(value).strip())


def main() -> None:
    index = load_yaml(INDEX)["portfolio"]
    policy = load_yaml(POLICY)["priority_policy"]
    directives_doc = load_yaml(DIRECTIVES)["priority_directives"]

    freshness_doc = json.loads(FRESHNESS.read_text(encoding="utf-8"))
    freshness_by_id = {row["id"]: row for row in freshness_doc.get("projects", [])}

    directives = {}
    directive_order = {}
    for i, item in enumerate(directives_doc.get("focus", [])):
        project_id = str(item["project"])
        directives[project_id] = item
        directive_order[project_id] = i

    projects = {}
    for rel in index.get("project_records", []):
        record = load_yaml(PORTFOLIO / rel).get("project")
        if not isinstance(record, dict) or not record.get("id"):
            raise ValueError(f"{rel}: missing project.id")
        projects[str(record["id"])] = record

    closed_statuses = set(policy["derived_rules"]["CLOSED"].get("statuses", []))
    parked_statuses = set(policy["derived_rules"]["PARKED"].get("statuses", []))
    next_statuses = set(policy["derived_rules"]["NEXT"].get("statuses", []))
    watch_statuses = set(policy["derived_rules"]["WATCH"].get("statuses", []))
    reverify_states = set(policy["derived_rules"]["REVERIFY"].get("freshness", []))

    rows = []
    for project_id, project in projects.items():
        fresh = freshness_by_id.get(project_id, {})
        freshness = str(fresh.get("freshness") or "UNKNOWN")
        completeness = str(fresh.get("completeness") or "UNKNOWN")
        status = str(project.get("status") or "UNKNOWN")
        directive = directives.get(project_id)

        if status in closed_statuses:
            lane = "CLOSED"
            source = "derived-status"
            reason = "commercial or project direction is explicitly closed"
        elif freshness in reverify_states:
            lane = "REVERIFY"
            source = "freshness-gate"
            reason = f"state freshness is {freshness}; current-state evidence must be reverified"
        elif directive:
            lane = str(directive["lane"])
            source = "human-directive"
            reason = str(directive.get("reason") or "explicit human priority directive")
        elif status in parked_statuses:
            lane = "PARKED"
            source = "derived-status"
            reason = f"status {status} is parked by policy"
        elif status in next_statuses:
            if known_gate(project.get("next_gate")):
                lane = "NEXT"
                source = "derived-status"
                reason = f"status {status} has a concrete next gate"
            else:
                lane = "WATCH"
                source = "derived-status"
                reason = f"status {status} lacks a concrete next gate"
        elif status in watch_statuses:
            lane = "WATCH"
            source = "derived-status"
            reason = "active/reviewable does not imply NOW without explicit promotion or strong economic evidence"
        else:
            lane = "WATCH"
            source = "default"
            reason = "no stronger priority evidence is registered"

        blockers = list(project.get("blockers") or [])
        evidence = list(project.get("evidence") or [])
        economic_evidence = project.get("economic_evidence")
        economic_evidence_state = "PRESENT" if nonempty(economic_evidence) else "UNKNOWN"

        if directive and directive.get("next_action"):
            next_action = str(directive["next_action"])
        else:
            next_action = str(project.get("next_gate") or "UNKNOWN")

        row = {
            "id": project_id,
            "repository": project.get("repository"),
            "status": status,
            "lane": lane,
            "decision_source": source,
            "reason": reason,
            "next_action": next_action,
            "blockers": blockers,
            "freshness": freshness,
            "completeness": completeness,
            "knowledge_gap": completeness != "COMPLETE",
            "economic_role": project.get("economic_role"),
            "economic_evidence_state": economic_evidence_state,
            "evidence": evidence,
            "constraints": list((directive or {}).get("constraints") or []),
            "explicit_directive": bool(directive),
            "directive_order": directive_order.get(project_id),
        }
        rows.append(row)

    counts = {lane: 0 for lane in LANE_ORDER}
    for row in rows:
        counts[row["lane"]] += 1

    now_cap = int(policy["wip"]["now_cap"])
    next_cap = int(policy["wip"]["next_cap"])
    wip = {
        "now_cap": now_cap,
        "now_count": counts["NOW"],
        "now_overflow": max(0, counts["NOW"] - now_cap),
        "next_cap": next_cap,
        "next_count": counts["NEXT"],
        "next_overflow": max(0, counts["NEXT"] - next_cap),
    }

    rows.sort(
        key=lambda r: (
            LANE_ORDER[r["lane"]],
            0 if r["explicit_directive"] else 1,
            r["directive_order"] if r["directive_order"] is not None else 9999,
            r["id"],
        )
    )

    report = {
        "schema_version": 1,
        "as_of": freshness_doc.get("as_of"),
        "policy": "priority-policy.yaml",
        "directives": "priority-directives.yaml",
        "lane_counts": counts,
        "wip": wip,
        "projects": [{k: v for k, v in row.items() if k != "directive_order"} for row in rows],
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Priority / Next-Action Report",
        "",
        "> Priority is gate-based, not a technical-activity score.",
        "> ACTIVE does not mean NOW. Human directives and evidence outrank repository activity.",
        "",
        f"**As of:** {report['as_of']}  ",
        f"**NOW:** {counts['NOW']} / cap {now_cap}  ",
        f"**NEXT:** {counts['NEXT']} / cap {next_cap}  ",
        f"**WATCH:** {counts['WATCH']}  ",
        f"**PARKED:** {counts['PARKED']}  ",
        f"**REVERIFY:** {counts['REVERIFY']}  ",
        f"**CLOSED:** {counts['CLOSED']}",
        "",
        "## Lane semantics",
        "",
        "| Lane | Meaning |",
        "|---|---|",
        "| NOW | explicit current focus; eligible to consume active build time |",
        "| NEXT | concrete next gate, but not current WIP |",
        "| WATCH | observe / validate / wait for evidence; do not create work merely for activity |",
        "| PARKED | intentionally inactive until a named re-entry condition is met |",
        "| REVERIFY | state is too stale or unknown for material decisions |",
        "| CLOSED | direction is closed; preserve evidence only unless separately extracted |",
        "",
    ]

    if wip["now_overflow"] or wip["next_overflow"]:
        lines += [
            "## WIP violation",
            "",
            f"- NOW overflow: {wip['now_overflow']}",
            f"- NEXT overflow: {wip['next_overflow']}",
            "",
        ]

    for lane in ["NOW", "NEXT", "WATCH", "PARKED", "REVERIFY", "CLOSED"]:
        lines += [f"## {lane}", ""]
        lane_rows = [r for r in rows if r["lane"] == lane]
        if not lane_rows:
            lines += ["_None._", ""]
            continue
        lines += [
            "| Project | Why | Next action | Blockers | Knowledge |",
            "|---|---|---|---|---|",
        ]
        for row in lane_rows:
            blockers = "; ".join(str(x) for x in row["blockers"]) or "—"
            knowledge = row["completeness"]
            lines.append(
                f"| `{row['id']}` | {row['reason']} | {row['next_action']} | {blockers} | {knowledge} |"
            )
        lines.append("")

    lines += [
        "## Invariants",
        "",
        "- No project enters NOW because it is technically interesting or recently active.",
        "- STALE or UNKNOWN freshness overrides priority and becomes REVERIFY.",
        "- A blocker remains visible; priority does not erase it.",
        "- Missing economic evidence remains UNKNOWN rather than being inferred from technical evidence.",
        "- Human strategic directives remain authoritative over derived lanes.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
