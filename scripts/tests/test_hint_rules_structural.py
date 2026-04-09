"""check_manifest_drift.hint_rules_structural_errors"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_manifest_drift import hint_rules_structural_errors  # noqa: E402


class TestHintRulesStructural(unittest.TestCase):
    def test_ok(self) -> None:
        e = hint_rules_structural_errors(
            {
                "rules": [
                    {"id": "a", "track_closure": True},
                    {"id": "b"},
                ]
            }
        )
        self.assertEqual(e, [])

    def test_duplicate_id(self) -> None:
        e = hint_rules_structural_errors(
            {"rules": [{"id": "x"}, {"id": "x"}]}
        )
        self.assertTrue(any("重复" in x for x in e))

    def test_missing_id(self) -> None:
        e = hint_rules_structural_errors({"rules": [{"hint": "n"}]})
        self.assertTrue(any("缺少 id" in x for x in e))

    def test_track_closure_type(self) -> None:
        e = hint_rules_structural_errors(
            {"rules": [{"id": "z", "track_closure": 1}]}
        )
        self.assertTrue(any("track_closure" in x for x in e))


if __name__ == "__main__":
    unittest.main()
