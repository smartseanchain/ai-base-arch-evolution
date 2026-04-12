"""evolution_pkg.analysis_validate 轻量结构校验。"""
from __future__ import annotations

import sys
import unittest
from io import StringIO
from unittest.mock import patch

from evolution_pkg.analysis_validate import (
    expected_snapshot_keys,
    validate_analysis_output_for_check,
    validate_evolution_hints,
    validate_hint_closure_gaps,
)


class TestExpectedKeys(unittest.TestCase):
    def test_includes_sources_and_hints(self) -> None:
        k = expected_snapshot_keys()
        self.assertIn("sources", k)
        self.assertIn("hint_closure_gaps", k)


class TestValidateHintClosureGaps(unittest.TestCase):
    def test_ok(self) -> None:
        validate_hint_closure_gaps([{"rule_id": "x", "text": "t"}])

    def test_not_list_exits(self) -> None:
        stderr = StringIO()
        with patch.object(sys, "stderr", stderr), self.assertRaises(SystemExit) as ctx:
            validate_hint_closure_gaps({})  # type: ignore[arg-type]
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("须为数组", stderr.getvalue())


class TestValidateEvolutionHints(unittest.TestCase):
    def test_ok_dict(self) -> None:
        validate_evolution_hints([{"text": "x"}])

    def test_bad_exits(self) -> None:
        stderr = StringIO()
        with patch.object(sys, "stderr", stderr), self.assertRaises(SystemExit) as ctx:
            validate_evolution_hints([{}])
        self.assertEqual(ctx.exception.code, 1)


class TestValidateAnalysisOutputForCheck(unittest.TestCase):
    def _minimal_out(self) -> dict:
        return {
            "schema_version": 1,
            "generated_at": "2026-01-01T00:00:00Z",
            "run": {"run_id": "rid", "repo_revision": "abc"},
            "sources": {
                "manifest_signals": 0,
                "candidate_signals": 0,
                "candidates_in_file": 0,
                "candidate_review_breakdown": {
                    "pending": 0,
                    "noise": 0,
                    "queued_for_manifest": 0,
                },
                "hint_decisions": {
                    "total": 0,
                    "by_action": {"done": 0, "rejected": 0, "deferred": 0},
                },
                "combined_for_analysis": 0,
            },
            "module_heat": [],
            "factor_heat": [],
            "kind_distribution": {},
            "cooccurrence": [],
            "evolution_hints": [],
            "hint_closure_gaps": [],
        }

    def test_returns_sources(self) -> None:
        out = self._minimal_out()
        src = validate_analysis_output_for_check(out)
        self.assertEqual(src["combined_for_analysis"], 0)

    def test_missing_key_exits(self) -> None:
        out = self._minimal_out()
        del out["run"]
        stderr = StringIO()
        with patch.object(sys, "stderr", stderr), self.assertRaises(SystemExit) as ctx:
            validate_analysis_output_for_check(out)
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("缺字段", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
