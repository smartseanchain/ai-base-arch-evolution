"""validate_evolution_hint_decisions 结构校验。"""
from __future__ import annotations

import unittest

from validate_evolution_hint_decisions import validate_decisions

PAGES = {"a.html", "b.html"}
# 与校验逻辑一致：填写 rule_id 时须落在此集合（测试中模拟 hint-rules 的 id 集）
RULE_IDS = {"reg_ai", "water_carbon"}


class TestValidateEvolutionHintDecisions(unittest.TestCase):
    def test_empty_ok(self) -> None:
        e = validate_decisions({"decisions": []}, PAGES, RULE_IDS)
        self.assertEqual(e, [])

    def test_valid_row(self) -> None:
        e = validate_decisions(
            {
                "decisions": [
                    {
                        "id": "h1",
                        "action": "done",
                        "recorded_at": "2026-04-01",
                        "hint_summary": "test",
                        "related_pages": ["a.html"],
                        "rule_id": "reg_ai",
                    }
                ]
            },
            PAGES,
            RULE_IDS,
        )
        self.assertEqual(e, [])

    def test_bad_rule_id(self) -> None:
        e = validate_decisions(
            {
                "decisions": [
                    {
                        "id": "z",
                        "action": "done",
                        "recorded_at": "2026-04-01",
                        "rule_id": "not_in_rules_json",
                    }
                ]
            },
            PAGES,
            RULE_IDS,
        )
        self.assertTrue(any("hint-rules" in x for x in e))

    def test_duplicate_id(self) -> None:
        e = validate_decisions(
            {
                "decisions": [
                    {
                        "id": "x",
                        "action": "done",
                        "recorded_at": "2026-04-01",
                    },
                    {
                        "id": "x",
                        "action": "rejected",
                        "recorded_at": "2026-04-02",
                    },
                ]
            },
            PAGES,
            RULE_IDS,
        )
        self.assertTrue(any("重复" in x for x in e))

    def test_bad_page(self) -> None:
        e = validate_decisions(
            {
                "decisions": [
                    {
                        "id": "x",
                        "action": "deferred",
                        "recorded_at": "2026-04-01",
                        "related_pages": ["nope.html"],
                    }
                ]
            },
            PAGES,
            RULE_IDS,
        )
        self.assertTrue(any("registry" in x for x in e))

    def test_extra_root_key(self) -> None:
        e = validate_decisions({"decisions": [], "meta": {}}, PAGES, RULE_IDS)
        self.assertTrue(any("多余" in x or "仅允许" in x for x in e))


if __name__ == "__main__":
    unittest.main()
