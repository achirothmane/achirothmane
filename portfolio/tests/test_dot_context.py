#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import yaml

from portfolio.scripts.generate_dot_context import SnapshotError, build_snapshot


class DotContextSnapshotTest(unittest.TestCase):
    def write_yaml(self, root: Path, rel: str, value: dict) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    def write_json(self, root: Path, rel: str, value: dict) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def fixture(self) -> Path:
        root = Path(tempfile.mkdtemp())
        (root / "SYSTEM-MAP.md").write_text("# map\n", encoding="utf-8")
        (root / "portfolio").mkdir()
        (root / "portfolio" / "DOT-OPERATING-CONTRACT.md").write_text("# contract\n", encoding="utf-8")

        self.write_yaml(root, "portfolio/projects/portfolio-dot.yaml", {
            "project": {"id": "portfolio-dot", "status": "ACTIVE_BUILD", "last_verified": "2026-10-08"}
        })
        self.write_yaml(root, "portfolio/projects/data-engine.yaml", {
            "project": {"id": "data-engine", "status": "ACTIVE", "last_verified": "2026-10-08"}
        })
        self.write_yaml(root, "portfolio/contracts/portfolio-dot--data-engine.yaml", {
            "contract": {
                "id": "portfolio-dot--data-engine",
                "source_project": "portfolio-dot",
                "target_project": "data-engine",
                "relations": ["CONSUMES"],
                "hard_dependency": False,
            }
        })
        self.write_yaml(root, "portfolio/index.yaml", {
            "portfolio": {
                "last_structural_review": "2026-10-08",
                "project_records": [
                    "projects/portfolio-dot.yaml",
                    "projects/data-engine.yaml",
                ],
                "contract_records": ["contracts/portfolio-dot--data-engine.yaml"],
            }
        })
        self.write_json(root, "portfolio/freshness-report.json", {
            "as_of": "2026-10-08",
            "dependency_freshness_risks": [],
            "projects": [
                {"id": "portfolio-dot", "freshness": "FRESH", "completeness": "COMPLETE"},
                {"id": "data-engine", "freshness": "FRESH", "completeness": "COMPLETE"},
            ],
        })
        self.write_json(root, "portfolio/priority-report.json", {
            "as_of": "2026-10-08",
            "wip": {"now_cap": 3, "now_count": 2, "now_overflow": 0, "next_cap": 6, "next_count": 0, "next_overflow": 0},
            "projects": [
                {"id": "portfolio-dot", "lane": "NOW"},
                {"id": "data-engine", "lane": "NOW"},
            ],
        })
        self.write_json(root, "portfolio/dependency-graph.json", {
            "structural_review": "2026-10-08",
            "edges": [{
                "id": "portfolio-dot--data-engine",
                "source": "portfolio-dot",
                "target": "data-engine",
                "relations": ["CONSUMES"],
                "hard_dependency": False,
            }],
        })
        self.write_yaml(root, "portfolio/execution-queue.yaml", {
            "execution_queue": {
                "runnable_count": 1,
                "items": [{
                    "id": "dots-context-002",
                    "project": "portfolio-dot",
                    "state": "READY",
                    "authority": "PREPARE",
                    "objective": "build snapshot",
                    "evidence_required": ["deterministic digest"],
                    "stop_conditions": ["missing source"],
                }],
            }
        })
        self.write_yaml(root, "portfolio/execution-policy.yaml", {
            "execution_policy": {"principle": "priority-does-not-equal-execution-authority"}
        })
        self.write_yaml(root, "portfolio/dot-handoff.yaml", {
            "dot_handoff": {"human_authority": {"final_on": ["merge", "publish"]}}
        })
        return root

    def test_same_inputs_same_digest(self) -> None:
        root = self.fixture()
        first = build_snapshot(root)
        second = build_snapshot(root)
        self.assertEqual(first["state"], "EXECUTABLE")
        self.assertEqual(first["snapshot_digest"], second["snapshot_digest"])

    def test_source_change_changes_digest(self) -> None:
        root = self.fixture()
        first = build_snapshot(root)
        path = root / "portfolio" / "projects" / "data-engine.yaml"
        path.write_text(path.read_text(encoding="utf-8") + "# changed\n", encoding="utf-8")
        second = build_snapshot(root)
        self.assertNotEqual(first["snapshot_digest"], second["snapshot_digest"])

    def test_stale_generated_state_fails_closed(self) -> None:
        root = self.fixture()
        priority_path = root / "portfolio" / "priority-report.json"
        priority = json.loads(priority_path.read_text(encoding="utf-8"))
        priority["as_of"] = "2026-10-07"
        priority_path.write_text(json.dumps(priority), encoding="utf-8")
        snapshot = build_snapshot(root)
        self.assertEqual(snapshot["state"], "NON_EXECUTABLE")
        self.assertIn("PRIORITY_AS_OF_MISMATCH", snapshot["reasons"])

    def test_unknown_now_freshness_fails_closed(self) -> None:
        root = self.fixture()
        freshness_path = root / "portfolio" / "freshness-report.json"
        freshness = json.loads(freshness_path.read_text(encoding="utf-8"))
        freshness["projects"][0]["freshness"] = "UNKNOWN"
        freshness_path.write_text(json.dumps(freshness), encoding="utf-8")
        snapshot = build_snapshot(root)
        self.assertEqual(snapshot["state"], "NON_EXECUTABLE")
        self.assertTrue(any(reason.startswith("NOW_PROJECT_INADMISSIBLE_FRESHNESS:portfolio-dot") for reason in snapshot["reasons"]))

    def test_missing_required_source_raises(self) -> None:
        root = self.fixture()
        (root / "portfolio" / "execution-policy.yaml").unlink()
        with self.assertRaises(SnapshotError):
            build_snapshot(root)

    def test_ready_item_outside_now_fails_closed(self) -> None:
        root = self.fixture()
        queue_path = root / "portfolio" / "execution-queue.yaml"
        queue = yaml.safe_load(queue_path.read_text(encoding="utf-8"))
        queue["execution_queue"]["items"][0]["project"] = "data-engine"
        priority_path = root / "portfolio" / "priority-report.json"
        priority = json.loads(priority_path.read_text(encoding="utf-8"))
        priority["projects"][1]["lane"] = "NEXT"
        priority["wip"]["now_count"] = 1
        priority_path.write_text(json.dumps(priority), encoding="utf-8")
        queue_path.write_text(yaml.safe_dump(queue, sort_keys=False), encoding="utf-8")
        snapshot = build_snapshot(root)
        self.assertEqual(snapshot["state"], "NON_EXECUTABLE")
        self.assertIn("READY_ITEM_PROJECT_NOT_NOW:dots-context-002:data-engine", snapshot["reasons"])


if __name__ == "__main__":
    unittest.main()
