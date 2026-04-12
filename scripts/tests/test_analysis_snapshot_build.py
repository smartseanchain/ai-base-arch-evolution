"""evolution_pkg.analysis_snapshot_build 快照 dict 组装。"""
from __future__ import annotations

import unittest

from evolution_pkg.analysis_snapshot_build import build_analysis_snapshot_document


class TestBuildAnalysisSnapshotDocument(unittest.TestCase):
    def test_shape_and_sources_counts(self) -> None:
        manifest = {"signals": [{"id": "m1"}]}
        candidates = {
            "signals": [
                {"status": "candidate", "review_state": "pending"},
                {"status": "candidate", "review_state": "noise"},
            ]
        }
        signals = [{"_origin": "manifest"}, {"_origin": "candidate"}]
        analysis = {
            "module_heat": [],
            "factor_heat": [],
            "kind_distribution": {},
            "cooccurrence": [],
            "evolution_hints": [],
            "hint_closure_gaps": [],
        }
        run = {"run_id": "rid", "repo_revision": "abc"}
        out = build_analysis_snapshot_document(
            manifest=manifest,
            candidates=candidates,
            signals=signals,
            analysis=analysis,
            run=run,
            generated_at="2026-01-01T00:00:00Z",
            hint_decisions_doc={"decisions": []},
        )
        self.assertEqual(out["schema_version"], 1)
        self.assertEqual(out["generated_at"], "2026-01-01T00:00:00Z")
        self.assertEqual(out["run"], run)
        src = out["sources"]
        self.assertEqual(src["manifest_signals"], 1)
        self.assertEqual(src["candidate_signals"], 1)
        self.assertEqual(src["candidates_in_file"], 2)
        self.assertEqual(src["combined_for_analysis"], 2)
        self.assertIn("candidate_review_breakdown", src)
        self.assertEqual(src["hint_decisions"]["total"], 0)


if __name__ == "__main__":
    unittest.main()
