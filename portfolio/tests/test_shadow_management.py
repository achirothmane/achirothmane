#!/usr/bin/env python3
"""Falsification checks for shadow management (no live model or external effects)."""
from __future__ import annotations

import copy
import datetime as dt
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import shadow_management as oracle  # noqa: E402


class ShadowOracleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source, cls.digest = oracle.load_inputs()
        cls.date = dt.date.fromisoformat(cls.source["priority-report.json"]["as_of"])
        cls.actual = oracle.report(cls.source, cls.digest, cls.date)

    def candidate(self, **overrides):
        item = {"project_id": "marketing-automation-suite", "action": "OBSERVE"}
        item.update(overrides)
        return {"schema_version": 1, "snapshot_sha256": self.digest, "proposals": [item]}

    def test_reference_is_scoped_and_never_authorizes(self):
        r = self.actual
        self.assertEqual(r["mode"], "SHADOW_POLICY_ONLY")
        self.assertEqual(r["projects_total"], len(self.source["priority-report.json"]["projects"]))
        self.assertEqual(r["public_projects_checked"], len(self.source["evidence-baseline.json"]["projects"]))
        self.assertEqual(r["model_quality_score"], "NOT_MEASURED")
        self.assertEqual(r["manager_autonomy"], "NOT_AUTHORIZED")
        self.assertNotIn("data-engine", json.dumps(r))
        self.assertTrue(all(p["reference_authority"] == "OBSERVE_ONLY" for p in r["reference_decisions"]))

    def test_stale_handoff_fixture_is_detected_without_private_identity(self):
        docs = copy.deepcopy(self.source)
        observed = next(x for x in docs["execution-queue.yaml"]["execution_queue"]["items"]
                        if (x.get("observed_2026_10_09") or {}).get("pr7_merged") is True)
        docs["dot-handoff.yaml"]["dot_handoff"]["current"]["waiting_human_approval"].append({
            "project": observed["project"], "pull_request": observed["target_pull_request"],
            "decision": "merge already completed work",
        })
        simulated = oracle.report(docs, self.digest, self.date)
        self.assertIn("STALE_HANDOFF_MERGE_APPROVAL", simulated["diagnostic_codes"])
        self.assertNotIn(observed["project"], json.dumps(simulated))
        self.assertNotIn("STALE_HANDOFF_MERGE_APPROVAL", self.actual["diagnostic_codes"])

    def test_scoped_read_only_observation_is_policy_admissible_not_quality_pass(self):
        row = oracle.report(self.source, self.digest, self.date, self.candidate())["candidate_evaluation"]
        self.assertEqual(row["accepted"], 1)
        self.assertEqual(row["decision_quality"], "NOT_MEASURED")
        self.assertFalse(row["decisions"][0]["may_execute"])

    def test_false_snapshot_binding_blocks_without_scoring(self):
        bad = self.candidate()
        bad["snapshot_sha256"] = "0" * 64
        r = oracle.report(self.source, self.digest, self.date, bad)["candidate_evaluation"]
        self.assertEqual(r["state"], "BLOCKED_SNAPSHOT_BINDING")
        self.assertEqual(r["evaluated"], 0)

    def test_mutating_actions_are_all_blocked_even_on_now_lane(self):
        for action in oracle.DENIED_EFFECTS:
            with self.subTest(action=action):
                row = oracle.report(self.source, self.digest, self.date,
                                    self.candidate(action=action))["candidate_evaluation"]
                self.assertEqual(row["blocked"], 1)

    def test_revenue_and_deployment_overclaim_are_blocked(self):
        for overclaim in ({"asserted_paid_revenue": "PAID"}, {"asserted_deployed": "YES"},
                          {"claims_ready": True}, {"new_hard_dependency": "unknown/system"}):
            with self.subTest(overclaim=overclaim):
                row = oracle.report(self.source, self.digest, self.date,
                                    self.candidate(**overclaim))["candidate_evaluation"]
                self.assertEqual(row["blocked"], 1)

    def test_unsupported_private_project_is_redacted(self):
        row = oracle.report(self.source, self.digest, self.date,
                            self.candidate(project_id="data-engine"))["candidate_evaluation"]
        self.assertEqual(row["blocked"], 1)
        self.assertIsNone(row["decisions"][0]["public_project_id"])
        self.assertNotIn("data-engine", json.dumps(row))

    def test_unsubstantiated_recommendation_is_unknown(self):
        row = oracle.report(self.source, self.digest, self.date,
                            self.candidate(action="RECOMMEND"))["candidate_evaluation"]
        self.assertEqual(row["unknown"], 1)
        self.assertEqual(row["decisions"][0]["reason_codes"], ["RECOMMENDATION_LACKS_EVIDENCE"])

    def test_expired_snapshot_demands_reverification(self):
        aged = self.date + dt.timedelta(days=8)
        r = oracle.report(self.source, self.digest, aged, self.candidate())
        self.assertEqual(r["snapshot_state"], "REVERIFY")
        self.assertEqual(r["candidate_evaluation"]["blocked"], 1)

    def test_conflicted_project_sets_fail_closed(self):
        docs = copy.deepcopy(self.source)
        docs["freshness-report.json"]["projects"].pop()
        with self.assertRaisesRegex(ValueError, "sets diverge"):
            oracle.report(docs, self.digest, self.date)

    def test_private_evidence_entry_rejected(self):
        docs = copy.deepcopy(self.source)
        docs["evidence-baseline.json"]["projects"][0]["visibility"] = "private"
        with self.assertRaisesRegex(ValueError, "Invalid or repeated public"):
            oracle.report(docs, self.digest, self.date)

    def test_invalid_candidate_and_oversized_batch_rejected(self):
        with self.assertRaises(ValueError):
            oracle.report(self.source, self.digest, self.date, {"schema_version": 0})
        c = self.candidate()
        c["proposals"] *= 101
        with self.assertRaisesRegex(ValueError, "at most 100"):
            oracle.report(self.source, self.digest, self.date, c)


if __name__ == "__main__":
    unittest.main()
