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
    compute_hint_closure_gaps,
    evaluate_hint_rules,
    hint_decisions_stats,
    load_hint_rules,
    run_analysis,
    track_closure_rule_ids,
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
        self.assertEqual(out.get("hint_closure_gaps"), [])
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
        out = run_analysis(sigs, None, rules, {})
        blob = _hints_text(out["evolution_hints"])
        self.assertIn("监管", blob)
        self.assertIn("AI", blob)
        gap_ids = {g["rule_id"] for g in out.get("hint_closure_gaps") or []}
        self.assertIn("reg_ai", gap_ids)

    def test_reg_ai_closed_by_decision(self) -> None:
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
        dec = {
            "decisions": [
                {"rule_id": "reg_ai", "action": "done"},
            ]
        }
        out = run_analysis(sigs, None, rules, dec)
        gap_ids = {g["rule_id"] for g in out.get("hint_closure_gaps") or []}
        self.assertNotIn("reg_ai", gap_ids)

    def test_reg_ai_deferred_not_closed(self) -> None:
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
        dec = {"decisions": [{"rule_id": "reg_ai", "action": "deferred"}]}
        out = run_analysis(sigs, None, rules, dec)
        gap_ids = {g["rule_id"] for g in out.get("hint_closure_gaps") or []}
        self.assertIn("reg_ai", gap_ids)


class TestHintClosureGaps(unittest.TestCase):
    def test_compute_basic(self) -> None:
        hints = [{"rule_id": "a", "text": "t"}]
        g = compute_hint_closure_gaps(hints, {"a"}, set())
        self.assertEqual(len(g), 1)
        self.assertEqual(g[0]["rule_id"], "a")

    def test_untracked_ignored(self) -> None:
        rules = {
            "rules": [
                {
                    "id": "only",
                    "factors_min": {"a": 1},
                    "hint": "hi",
                }
            ]
        }
        self.assertEqual(track_closure_rule_ids(rules), set())
        sigs = [
            {"_origin": "manifest", "maps_to": {"lab_factors": ["a"]}},
        ]
        out = run_analysis(sigs, None, rules, {})
        self.assertEqual(out["hint_closure_gaps"], [])


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


class TestHintDecisionsStats(unittest.TestCase):
    def test_empty(self) -> None:
        s = hint_decisions_stats({})
        self.assertEqual(s["total"], 0)
        self.assertEqual(s["by_action"]["done"], 0)

    def test_counts(self) -> None:
        s = hint_decisions_stats(
            {
                "decisions": [
                    {"action": "done"},
                    {"action": "done"},
                    {"action": "rejected"},
                ]
            }
        )
        self.assertEqual(s["total"], 3)
        self.assertEqual(s["by_action"]["done"], 2)
        self.assertEqual(s["by_action"]["rejected"], 1)
        self.assertEqual(s["by_action"]["deferred"], 0)


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
