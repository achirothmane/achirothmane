#!/usr/bin/env python3
"""Tests of the actual 2026-10-09 Portfolio projection, not an AI decision."""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "portfolio" / "scripts"))
import export_dots_context as ctx
import shadow_management


class SealedPortfolioContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.day = dt.date.fromisoformat("2026-10-09")
        cls.snapshot = ctx.build_snapshot(ROOT, cls.day)

    def test_snapshot_contains_exactly_one_genuine_obs_item(self):
        snapshot = self.snapshot
        self.assertEqual(snapshot["schema_version"], 1)
        self.assertEqual(snapshot["state"], "EXECUTABLE")
        items = snapshot["projection"]["runnable_items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], "dots-runtime-evidence-observe-006")
        self.assertEqual(items[0]["authority"], "OBSERVE")
        self.assertEqual(items[0]["project"], "governed-agent-runtime")
        self.assertEqual(snapshot["projection"]["wip"]["now_count"], 2)

    def test_hash_matches_cross_language_canonical_json(self):
        raw = copy.deepcopy(self.snapshot)
        digest = raw.pop("snapshot_digest")
        self.assertEqual(digest, hashlib.sha256(ctx.canonical(raw)).hexdigest())
        self.assertEqual(len(digest), 64)

    def test_source_bindings_match_actual_bytes(self):
        for item in self.snapshot["source_bindings"]:
            self.assertEqual(item["sha256"], hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest())

    def test_projection_does_not_export_unverified_or_private_project_records(self):
        baseline = json.loads((ROOT / "portfolio/evidence-baseline.json").read_text())
        allowed = {x["id"] for x in baseline["projects"] if x["visibility"] == "public"}
        p = self.snapshot["projection"]
        self.assertTrue(set(p["now_projects"]) <= allowed)
        self.assertTrue(set(row["project"] for row in p["runnable_items"]) <= allowed)
        self.assertTrue(all(x["source"] in allowed and x["target"] in allowed for x in p["verified_contracts"]))
        self.assertNotIn("data-engine", json.dumps(p))
        self.assertNotIn("ci-retry-gate-engine", json.dumps(p))

    def test_expired_snapshot_is_not_an_execution_ticket(self):
        with self.assertRaisesRegex(ValueError, "admission failed"):
            ctx.build_snapshot(ROOT, self.day + dt.timedelta(days=8))

    def test_deleted_ready_task_cannot_be_faked_in_projection(self):
        docs, digest = shadow_management.load_inputs(ROOT / "portfolio")
        mutated = copy.deepcopy(docs)
        mutated["execution-queue.yaml"]["execution_queue"]["items"] = [
            item for item in mutated["execution-queue.yaml"]["execution_queue"]["items"]
            if item.get("id") != "dots-runtime-evidence-observe-006"
        ]
        mutated["execution-queue.yaml"]["execution_queue"]["runnable_count"] = 0
        with patch.object(shadow_management, "load_inputs", return_value=(mutated, digest)):
            with self.assertRaisesRegex(ValueError, "admission failed"):
                ctx.build_snapshot(ROOT, self.day)

    def test_human_final_actions_remain_and_no_extra_tool_data(self):
        p = self.snapshot["projection"]
        self.assertIn("merge", p["human_final_on"])
        self.assertIn("paid-spend", p["human_final_on"])
        self.assertFalse(any("tools" in item or "execute" in item for item in p["runnable_items"]))
        self.assertIn("priority-does-not-equal-execution-authority", p["execution_principle"])


if __name__ == "__main__":
    unittest.main()
