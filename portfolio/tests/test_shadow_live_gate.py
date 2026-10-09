#!/usr/bin/env python3
"""S1 read-only live provenance preflight falsification, not live model tests."""
from __future__ import annotations

import copy
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import shadow_management as s0
import shadow_live_gate as s1


class LiveGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs, cls.digest = s0.load_inputs()
        cls.date = dt.date.fromisoformat(cls.docs["priority-report.json"]["as_of"])
        cls.gate = s1.source_preflight(cls.docs, cls.digest, as_of=cls.date)

    def fake_trace(self):
        return {
            "schema_version": 1, "origin": "governed-agent-runtime",
            "portfolio_source_digest": self.digest,
            "runtime_snapshot_digest": "a" * 64,
            "provider_kind": "openai-responses",
            "decision": {
                "kind": "PROPOSE_NEXT_GATE",
                "snapshot_digest": "a" * 64,
                "work_item_id": "fake-ready",
                "requested_authority": "OBSERVE",
                "requested_action": "",
                "rationale": "Evidence-based hypothetical",
            },
            "provider_receipt": {
                "transport": "responses", "provider": "openai-responses",
                "response_id": "fake-not-an-attestation", "run_url": "https://example.org/run",
                "source_commit": "b" * 64, "paid_call": True,
                "observed_at": "2026-10-09T07:00:00Z",
            },
        }

    def test_actual_portfolio_no_ready_and_no_live_measurement(self):
        self.assertEqual(self.gate["state"], "BLOCKED_NO_READY_WORK")
        self.assertEqual(self.gate["runnable_count"], 0)
        self.assertEqual(self.gate["actual_dots_trace_count"], 0)
        self.assertEqual(self.gate["provider_calls_performed"], 0)
        self.assertFalse(self.gate["live_model_authorized"])
        self.assertFalse(self.gate["runtime_validated"])
        self.assertEqual(self.gate["decision_quality"], "NOT_MEASURED")

    def test_fabricated_real_provider_claim_is_not_counted(self):
        reviewed = s1.review_trace(self.fake_trace(), self.gate, self.docs)
        self.assertEqual(reviewed["state"], "BLOCKED")
        self.assertIn("S1_PREFLIGHT_NOT_ADMITTED", reviewed["reason_codes"])
        self.assertFalse(reviewed["counted_as_live_dots_decision"])

    def test_stale_source_never_promotes_ready(self):
        aged = s1.source_preflight(self.docs, self.digest, as_of=self.date + dt.timedelta(days=8))
        self.assertEqual(aged["state"], "BLOCKED_STALE_OR_SCOPE_DRIFT")

    def test_forged_current_reference_digest_rejected(self):
        with self.assertRaisesRegex(ValueError, "not bound"):
            s1.source_preflight(self.docs, "f" * 64, as_of=self.date)

    def test_false_queue_runnable_count_is_denied(self):
        docs = copy.deepcopy(self.docs)
        docs["execution-queue.yaml"]["execution_queue"]["runnable_count"] = 1
        gate = s1.source_preflight(docs, self.digest, as_of=self.date)
        self.assertEqual(gate["state"], "BLOCKED_QUEUE_COUNT_CONFLICT")

    def test_fake_ready_work_without_handoff_detected(self):
        docs = copy.deepcopy(self.docs)
        queue = docs["execution-queue.yaml"]["execution_queue"]
        queue["items"].append({"id": "fake-ready", "project": "marketing-automation-suite",
                               "state": "READY", "authority": "OBSERVE", "evidence_required": ["x"],
                               "stop_conditions": ["stop"]})
        queue["runnable_count"] = 1
        gate = s1.source_preflight(docs, self.digest, as_of=self.date)
        self.assertEqual(gate["state"], "BLOCKED_HANDOFF_COUNT_CONFLICT")

    def test_fake_handoff_ready_work_is_not_automatic_permission(self):
        docs = copy.deepcopy(self.docs)
        queue = docs["execution-queue.yaml"]["execution_queue"]
        queue["items"].append({"id": "fake-ready", "project": "marketing-automation-suite",
                               "state": "READY", "authority": "OBSERVE", "evidence_required": ["x"],
                               "stop_conditions": ["stop"]})
        queue["runnable_count"] = 1
        docs["dot-handoff.yaml"]["dot_handoff"]["current"]["runnable_items"] = ["fake-ready"]
        gate = s1.source_preflight(docs, self.digest, as_of=self.date)
        self.assertEqual(gate["state"], "BLOCKED_EXECUTION_ADMISSION")  # NEXT is not NOW

    def test_even_well_formed_provider_file_is_not_independent_proof(self):
        docs = copy.deepcopy(self.docs)
        queue = docs["execution-queue.yaml"]["execution_queue"]
        queue["items"].append({"id": "fake-ready", "project": "agent-deal-exchange",
                               "state": "READY", "authority": "OBSERVE", "evidence_required": ["x"],
                               "stop_conditions": ["stop"]})
        queue["runnable_count"] = 1
        docs["dot-handoff.yaml"]["dot_handoff"]["current"]["runnable_items"] = ["fake-ready"]
        # Synthetic priority swap tests only; never written to canonical source.
        project = next(x for x in docs["priority-report.json"]["projects"] if x["id"] == "agent-deal-exchange")
        project["lane"] = "NOW"
        gate = s1.source_preflight(docs, self.digest, as_of=self.date)
        self.assertEqual(gate["state"], "READY_FOR_SEPARATE_RUNTIME_ATTESTATION")
        reviewed = s1.review_trace(self.fake_trace(), gate, docs)
        self.assertEqual(reviewed["state"], "PENDING_INDEPENDENT_ORIGIN_ATTESTATION")
        self.assertFalse(reviewed["counted_as_live_dots_decision"])

    def test_wrong_runtime_digest_or_extended_action_blocked(self):
        trace = self.fake_trace()
        trace["decision"]["snapshot_digest"] = "f" * 64
        trace["decision"]["requested_action"] = "MERGE"
        row = s1.review_trace(trace, self.gate, self.docs)
        self.assertIn("RUNTIME_DECISION_BINDING_MISMATCH", row["reason_codes"])
        self.assertIn("EFFECT_REQUEST_NOT_ADMITTED", row["reason_codes"])
        self.assertFalse(row["counted_as_live_dots_decision"])

    def test_unrecognized_trace_fields_denied(self):
        trace = self.fake_trace()
        trace["auto_execute"] = True
        row = s1.review_trace(trace, self.gate, self.docs)
        self.assertIn("INVALID_TRACE_SCHEMA", row["reason_codes"])

    def test_no_private_rationale_reflection(self):
        trace = self.fake_trace()
        trace["decision"]["rationale"] = "private analysis must stay private"
        row = s1.review_trace(trace, self.gate, self.docs)
        self.assertNotIn("private analysis", str(row))


if __name__ == "__main__":
    unittest.main()
