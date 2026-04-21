"""evolution_intelligence_digest：Markdown 组装（无磁盘快照依赖）。"""
from __future__ import annotations

import unittest

from evolution_intelligence_digest import build_digest_markdown


class TestEvolutionIntelligenceDigest(unittest.TestCase):
    def test_build_contains_run_and_heat(self) -> None:
        snap = {
            "schema_version": 1,
            "generated_at": "2026-01-01T00:00:00Z",
            "run": {"run_id": "rid", "repo_revision": "abc"},
            "sources": {
                "combined_for_analysis": 10,
                "manifest_signals": 2,
                "candidate_signals": 8,
                "hint_decisions": {
                    "total": 1,
                    "by_action": {"done": 1, "rejected": 0, "deferred": 0},
                },
            },
            "factor_heat": [{"factor": "ai", "count": 3}],
            "module_heat": [{"page": "lab.html", "count": 2}],
            "cooccurrence": [{"pair": ["ai", "reg"], "count": 2}],
            "evolution_hints": [{"rule_id": "x"}],
            "hint_closure_gaps": [{"rule_id": "gap1", "text": "t"}],
        }
        md = build_digest_markdown(snap, {}, {}, include_trends=False, include_sediment=False)
        self.assertIn("rid", md)
        self.assertIn("gap1", md)
        self.assertIn("`ai`", md)
        self.assertIn("lab.html", md)
        self.assertIn("ai` × `reg", md)
        self.assertNotIn("sediment-trends", md)

    def test_trends_section_when_present(self) -> None:
        snap = {
            "run": {},
            "sources": {},
            "factor_heat": [],
            "module_heat": [],
            "cooccurrence": [],
        }
        trends = {
            "factor_persistence": [
                {"factor": "reg", "days_in_top": 3, "coverage": 1.0},
            ]
        }
        md = build_digest_markdown(snap, trends, None, include_sediment=False)
        self.assertIn("跨日因子持久度", md)
        self.assertIn("`reg`", md)


if __name__ == "__main__":
    unittest.main()
