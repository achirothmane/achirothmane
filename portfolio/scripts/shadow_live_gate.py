#!/usr/bin/env python3
"""S1 source-bound READ-ONLY ingress for *actual* Dots decision evidence.

This is a preflight/ingress gate, not a model runner or provenance authority.
No network/model/payment/tool invocation. No Dots readiness is manufactured.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

import shadow_management as shadow

PORTFOLIO = Path(__file__).resolve().parents[1]
REFERENCE = PORTFOLIO / "shadow-reference.json"
ATTEST = PORTFOLIO / "s1-readiness.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TRACE_KEYS = {
    "schema_version", "origin", "portfolio_source_digest", "runtime_snapshot_digest",
    "provider_kind", "decision", "provider_receipt",
}
DECISION_KEYS = {
    "kind", "snapshot_digest", "work_item_id", "requested_authority",
    "requested_action", "rationale",
}
RECEIPT_KEYS = {
    "transport", "provider", "response_id", "run_url", "source_commit",
    "paid_call", "observed_at",
}


def source_preflight(docs: dict, digest: str, *, as_of: dt.date) -> dict:
    existing = json.loads(REFERENCE.read_text(encoding="utf-8"))
    if existing.get("snapshot_sha256") != digest:
        raise ValueError("S0 reference is not bound to current source bytes")
    if existing.get("manager_autonomy") != "NOT_AUTHORIZED" or existing.get("scope") != "PUBLIC_PROJECTS_ONLY":
        raise ValueError("S0 reference has unexpected authority or privacy scope")
    current = shadow.report(docs, digest, as_of=as_of)
    if existing.get("as_of") != docs["priority-report.json"].get("as_of"):
        raise ValueError("S0 reference age differs from priority report")
    if (current["snapshot_state"] != "FRESH_WITH_LIMITS" or
            current["public_projects_checked"] != existing.get("public_projects_checked")):
        return {
            "schema_version": 1, "mode": "S1_PREFLIGHT",
            "state": "BLOCKED_STALE_OR_SCOPE_DRIFT",
            "as_of": as_of.isoformat(), "source_sha256": digest,
            "runnable_count": 0, "actual_dots_trace_count": 0,
            "provider_calls_performed": 0, "decision_quality": "NOT_MEASURED",
            "runtime_validated": False, "live_model_authorized": False,
            "effect_authority": "NONE",
        }

    queue = docs["execution-queue.yaml"]["execution_queue"]
    priority = {x["id"]: x for x in docs["priority-report.json"]["projects"]}
    readiness = [x for x in queue.get("items", []) if x.get("state") == "READY"]
    handoff = docs["dot-handoff.yaml"]["dot_handoff"]
    declared = handoff.get("current", {}).get("runnable_items", [])
    if queue.get("runnable_count") != len(readiness):
        state = "BLOCKED_QUEUE_COUNT_CONFLICT"
    elif not isinstance(declared, list) or len(declared) != len(readiness):
        state = "BLOCKED_HANDOFF_COUNT_CONFLICT"
    elif not readiness:
        state = "BLOCKED_NO_READY_WORK"
    else:
        public_ids = set(x["project_id"] for x in current["reference_decisions"])
        if any(x.get("project") not in public_ids for x in readiness):
            state = "BLOCKED_OUTSIDE_PUBLIC_SCOPE"
        elif any(priority.get(x.get("project"), {}).get("lane") != "NOW" or
                 priority.get(x.get("project"), {}).get("freshness") != "FRESH" or
                 not x.get("evidence_required") or not x.get("stop_conditions") or
                 x.get("authority") != "OBSERVE" for x in readiness):
            state = "BLOCKED_EXECUTION_ADMISSION"
        else:
            state = "READY_FOR_SEPARATE_RUNTIME_ATTESTATION"
    return {
        "schema_version": 1, "mode": "S1_PREFLIGHT",
        "state": state, "as_of": as_of.isoformat(), "source_sha256": digest,
        "runnable_count": len(readiness), "actual_dots_trace_count": 0,
        "provider_calls_performed": 0, "decision_quality": "NOT_MEASURED",
        "runtime_validated": False, "live_model_authorized": False,
        "effect_authority": "NONE",
    }


def review_trace(trace: dict, gate: dict, docs: dict) -> dict:
    """Adversarial ingestion: source-controlled trace files are NOT trusted attestations.

    A formatted trace can only be marked PENDING_ORIGIN_ATTESTATION after structural
    checks; NEVER mark VERIFIED or increment a 'live decision' metric from JSON alone.
    """
    result = {"state": "BLOCKED", "reason_codes": [], "counted_as_live_dots_decision": False,
              "effect_authority": "NONE", "decision_quality": "NOT_MEASURED"}
    reasons = []
    if gate["state"] != "READY_FOR_SEPARATE_RUNTIME_ATTESTATION":
        reasons.append("S1_PREFLIGHT_NOT_ADMITTED")
    if not isinstance(trace, dict) or set(trace) != TRACE_KEYS or trace.get("schema_version") != 1:
        reasons.append("INVALID_TRACE_SCHEMA")
        trace = {}
    if trace.get("origin") != "governed-agent-runtime":
        reasons.append("UNTRUSTED_ORIGIN")
    if trace.get("portfolio_source_digest") != gate["source_sha256"]:
        reasons.append("PORTFOLIO_BINDING_MISMATCH")
    runtime_digest = trace.get("runtime_snapshot_digest")
    if not isinstance(runtime_digest, str) or not HEX64.fullmatch(runtime_digest):
        reasons.append("MISSING_RUNTIME_SNAPSHOT_DIGEST")
    decision = trace.get("decision")
    if not isinstance(decision, dict) or set(decision) != DECISION_KEYS:
        reasons.append("INVALID_D3_DECISION")
        decision = {}
    if decision.get("snapshot_digest") != runtime_digest:
        reasons.append("RUNTIME_DECISION_BINDING_MISMATCH")
    if decision.get("kind") not in ("PROPOSE_NEXT_GATE", "ASK_HUMAN", "REFUSE"):
        reasons.append("INVALID_D3_KIND")
    if decision.get("requested_authority") != "OBSERVE":
        reasons.append("AUTHORITY_ESCALATION")
    if decision.get("requested_action") not in ("", None):
        reasons.append("EFFECT_REQUEST_NOT_ADMITTED")
    if not isinstance(decision.get("rationale"), str) or not decision["rationale"].strip():
        reasons.append("MISSING_RATIONALE")
    admitted_ids = {x["id"] for x in docs["execution-queue.yaml"]["execution_queue"]["items"]
                    if x.get("state") == "READY"}
    if decision.get("work_item_id") not in admitted_ids:
        reasons.append("WORK_ITEM_NOT_READY")
    if trace.get("provider_kind") not in ("openai-responses",):
        reasons.append("NO_VERIFIED_LIVE_PROVIDER_KIND")
    receipt = trace.get("provider_receipt")
    if not isinstance(receipt, dict) or set(receipt) != RECEIPT_KEYS:
        reasons.append("INVALID_PROVIDER_RECEIPT")
    else:
        if (receipt.get("transport") != "responses" or
                receipt.get("provider") != "openai-responses" or
                receipt.get("paid_call") is not True or
                not isinstance(receipt.get("response_id"), str) or not receipt["response_id"] or
                not isinstance(receipt.get("source_commit"), str) or
                not HEX64.fullmatch(receipt["source_commit"])):
            reasons.append("INSUFFICIENT_PROVIDER_RECEIPT")
    if reasons:
        result["reason_codes"] = sorted(set(reasons))
    else:
        result["state"] = "PENDING_INDEPENDENT_ORIGIN_ATTESTATION"
        result["reason_codes"] = ["SELF_REPORTED_TRACE_IS_NOT_PROOF"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, help="Untrusted JSON evidence path (not uploaded to GitHub)")
    parser.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    parser.add_argument("--write-reference", action="store_true")
    parser.add_argument("--check-reference", action="store_true")
    args = parser.parse_args()
    if args.write_reference and args.check_reference:
        parser.error("Cannot write and check reference in the same run")
    docs, digest = shadow.load_inputs()
    as_of = dt.date.fromisoformat(args.as_of)
    gate = source_preflight(docs, digest, as_of=as_of)
    if args.trace:
        if args.trace.stat().st_size > 128 * 1024:
            raise ValueError("Trace exceeds 128 KiB")
        trace = json.loads(args.trace.read_text(encoding="utf-8"))
        gate["trace_review"] = review_trace(trace, gate, docs)
    rendered = json.dumps(gate, sort_keys=True, indent=2) + "\n"
    if args.write_reference:
        if args.trace:
            raise ValueError("Candidate evidence cannot be persisted in a public reference")
        ATTEST.write_text(rendered, encoding="utf-8")
    elif args.check_reference:
        if args.trace or not ATTEST.is_file() or rendered != ATTEST.read_text(encoding="utf-8"):
            raise ValueError("S1 readiness reference drift")
    else:
        print(rendered)
    if gate["state"] not in ("BLOCKED_NO_READY_WORK", "READY_FOR_SEPARATE_RUNTIME_ATTESTATION"):
        raise ValueError("S1 unexpected unsafe state: " + gate["state"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, ValueError, OSError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit("S1_FAIL_CLOSED: " + str(exc))
