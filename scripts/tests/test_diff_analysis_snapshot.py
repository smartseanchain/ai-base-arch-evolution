"""evolution_pkg.analysis_diff 与 diff_analysis_snapshot CLI。"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evolution_pkg.analysis_diff import build_report, snapshot_diff_json


def _minimal_snapshot(
    run_id: str, combined: int, hints_n: int, gaps_n: int
) -> dict:
    return {
        "schema_version": 1,
        "generated_at": "2026-01-01T00:00:00Z",
        "run": {"run_id": run_id, "repo_revision": "abc"},
        "sources": {
            "combined_for_analysis": combined,
            "manifest_signals": 1,
            "candidate_signals": 2,
        },
        "module_heat": [{"page": "a.html", "count": 3}],
        "factor_heat": [{"factor": "geo", "count": 2}],
        "kind_distribution": {},
        "cooccurrence": [],
        "evolution_hints": [{}] * hints_n,
        "hint_closure_gaps": [{}] * gaps_n,
    }


class TestDiffAnalysisSnapshot(unittest.TestCase):
    def test_build_report_contains_deltas(self) -> None:
        base = _minimal_snapshot("r0", 10, 1, 2)
        head = _minimal_snapshot("r1", 12, 3, 1)
        md = build_report(base, head)
        self.assertIn("r0", md)
        self.assertIn("r1", md)
        self.assertIn("10 → 12", md)
        self.assertIn("evolution_hints", md)
        self.assertIn("1 → 3", md)

    def test_snapshot_diff_json(self) -> None:
        base = _minimal_snapshot("r0", 10, 1, 2)
        head = _minimal_snapshot("r1", 12, 3, 1)
        out = snapshot_diff_json(base, head)
        self.assertEqual(out["combined_delta"], 2)
        self.assertEqual(out["hints_delta"], 2)
        self.assertEqual(out["gaps_delta"], -1)

    def test_cli_json_mode(self) -> None:
        import subprocess
        import sys

        root = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as td:
            bp = Path(td) / "base.json"
            hp = Path(td) / "head.json"
            bp.write_text(json.dumps(_minimal_snapshot("a", 5, 0, 0)), encoding="utf-8")
            hp.write_text(json.dumps(_minimal_snapshot("b", 7, 1, 0)), encoding="utf-8")
            r = subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts" / "diff_analysis_snapshot.py"),
                    "--json",
                    str(bp),
                    str(hp),
                ],
                cwd=str(root),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(r.returncode, 0, msg=r.stderr)
            out = json.loads(r.stdout)
            self.assertEqual(out["combined_delta"], 2)
            self.assertEqual(out["hints_delta"], 1)


if __name__ == "__main__":
    unittest.main()
