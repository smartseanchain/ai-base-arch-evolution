"""analysis_engine 核心逻辑回归（stdlib unittest）。"""
from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from analysis_engine import (  # noqa: E402
    candidate_review_breakdown,
    compute_diff_hints,
    evaluate_hint_rules,
    load_hint_rules,
    run_analysis,
)


def _hints_text(hints: list) -> str:
    parts: list[str] = []
    for h in hints:
        if isinstance(h, dict):
            parts.append(str(h.get("text") or ""))
        else:
            parts.append(str(h))
    return " ".join(parts)


class TestRunAnalysis(unittest.TestCase):
    def test_empty_signals_fallback(self) -> None:
        rules = load_hint_rules()
        out = run_analysis([], None, rules)
        self.assertIn("evolution_hints", out)
        self.assertIn("信号较少", _hints_text(out["evolution_hints"]))

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
        blob = _hints_text(out["evolution_hints"])
        self.assertIn("监管", blob)
        self.assertIn("AI", blob)


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
        self.assertTrue(any("已入库信号" in x["text"] for x in h))


class TestCandidateReviewBreakdown(unittest.TestCase):
    def test_counts(self) -> None:
        c = {
            "signals": [
                {"status": "candidate", "review_state": "pending"},
                {"status": "candidate", "review_state": "noise"},
                {"status": "candidate", "review_state": "queued_for_manifest"},
            ]
        }
        bd = candidate_review_breakdown(c)
        self.assertEqual(bd["pending"], 1)
        self.assertEqual(bd["noise"], 1)
        self.assertEqual(bd["queued_for_manifest"], 1)


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
        self.assertEqual(out[0]["text"], "hit")
        self.assertEqual(out[0]["rule_id"], "x")


if __name__ == "__main__":
    unittest.main()
