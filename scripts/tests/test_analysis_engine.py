"""analysis_engine 核心逻辑回归（stdlib unittest）。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from analysis_engine import (  # noqa: E402
    compute_diff_hints,
    evaluate_hint_rules,
    load_hint_rules,
    run_analysis,
)
from collections import Counter  # noqa: E402


class TestRunAnalysis(unittest.TestCase):
    def test_empty_signals_fallback(self) -> None:
        rules = load_hint_rules()
        out = run_analysis([], None, rules)
        self.assertIn("evolution_hints", out)
        self.assertTrue(any("信号较少" in h for h in out["evolution_hints"]))

    def test_reg_ai_rule_fires(self) -> None:
        rules = load_hint_rules()
        sigs = [
            {
                "_origin": "manifest",
                "maps_to": {
                    "pages": ["decade.html"],
                    "lab_factors": ["reg", "reg", "ai"],
                },
            }
        ]
        out = run_analysis(sigs, None, rules)
        hints = " ".join(out["evolution_hints"])
        self.assertIn("监管", hints)
        self.assertIn("AI", hints)


class TestDiffHints(unittest.TestCase):
    def test_no_prev_empty(self) -> None:
        h = compute_diff_hints(
            None,
            [{"factor": "ai", "count": 1}],
            [],
            1,
            1,
        )
        self.assertEqual(h, [])

    def test_manifest_increase(self) -> None:
        prev = {"sources": {"manifest_signals": 1, "candidate_signals": 0}}
        h = compute_diff_hints(prev, [], [], 3, 0)
        self.assertTrue(any("已入库信号" in x for x in h))


class TestEvaluateHintRules(unittest.TestCase):
    def test_factors_min(self) -> None:
        fac = Counter({"reg": 2, "ai": 1})
        doc = {
            "rules": [
                {
                    "id": "x",
                    "factors_min": {"reg": 2, "ai": 1},
                    "hint": "hit",
                }
            ]
        }
        out = evaluate_hint_rules(fac, 10, doc)
        self.assertEqual(out, ["hit"])


if __name__ == "__main__":
    unittest.main()
