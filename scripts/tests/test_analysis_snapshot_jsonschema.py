"""analysis-snapshot 与 docs/schemas/analysis-snapshot.schema.json 一致（需 jsonschema）。"""
from __future__ import annotations

import json
import unittest

from jsonschema import Draft202012Validator

from evolution_pkg.io import REPO_ROOT

SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "analysis-snapshot.schema.json"


class TestAnalysisSnapshotJsonSchema(unittest.TestCase):
    def test_minimal_instance_validates(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        minimal = {
            "schema_version": 1,
            "generated_at": "2026-01-01T00:00:00Z",
            "run": {"run_id": "20260101-abc", "repo_revision": "deadbeef"},
            "sources": {"combined_for_analysis": 0},
            "module_heat": [],
            "factor_heat": [],
            "kind_distribution": {},
            "cooccurrence": [],
            "evolution_hints": [],
            "hint_closure_gaps": [],
        }
        Draft202012Validator(schema).validate(minimal)

    def test_committed_snapshot_if_present(self) -> None:
        snap = REPO_ROOT / "assets" / "analysis-snapshot.json"
        if not snap.is_file():
            self.skipTest("no committed snapshot")
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        doc = json.loads(snap.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(doc)


if __name__ == "__main__":
    unittest.main()
