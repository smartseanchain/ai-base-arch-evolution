"""evolution_pkg.analysis_pipeline 与仓库默认真文件集成（--check，不写快照）。"""
from __future__ import annotations

import unittest
from unittest import mock

from evolution_pkg.analysis_pipeline import (
    AnalysisPaths,
    default_analysis_paths,
    parse_analysis_cli,
    run_analysis_pipeline,
)
from evolution_pkg.io import REPO_ROOT


class TestParseAnalysisCli(unittest.TestCase):
    def test_defaults(self) -> None:
        f = parse_analysis_cli([])
        self.assertFalse(f.check)
        self.assertFalse(f.write_sediment)
        self.assertFalse(f.no_sqlite_snapshot_history)

    def test_flags(self) -> None:
        f = parse_analysis_cli(
            ["--check", "--sediment", "--no-sqlite-snapshot-history"]
        )
        self.assertTrue(f.check)
        self.assertTrue(f.write_sediment)
        self.assertTrue(f.no_sqlite_snapshot_history)


class TestDefaultAnalysisPaths(unittest.TestCase):
    def test_matches_explicit_repo_layout(self) -> None:
        d = default_analysis_paths()
        self.assertEqual(
            d,
            AnalysisPaths(
                manifest=REPO_ROOT / "assets" / "evolution-manifest.json",
                candidates=REPO_ROOT / "assets" / "evolution-candidates.json",
                out_snapshot=REPO_ROOT / "assets" / "analysis-snapshot.json",
                hint_rules=REPO_ROOT / "scripts" / "evolution-hint-rules.json",
                hint_decisions=REPO_ROOT / "assets" / "evolution-hint-decisions.json",
                sediment=REPO_ROOT / "data" / "sediment.json",
            ),
        )


class TestRunAnalysisPipelineCheck(unittest.TestCase):
    @mock.patch("builtins.print")
    def test_check_returns_snapshot_dict(self, _print: mock.MagicMock) -> None:
        out = run_analysis_pipeline(default_analysis_paths(), check=True)
        self.assertIn("run", out)
        self.assertIn("sources", out)
        self.assertIn("hint_closure_gaps", out)
        self.assertIsInstance(out["sources"].get("combined_for_analysis"), int)


if __name__ == "__main__":
    unittest.main()
