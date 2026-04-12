"""evolution_pkg.analysis_hints 读规则与默认文档。"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evolution_pkg.analysis_hints import load_hint_rules_from_path


class TestLoadHintRulesFromPath(unittest.TestCase):
    def test_missing_file_returns_defaults(self) -> None:
        p = Path(tempfile.gettempdir()) / "evolution-hint-rules-nonexistent-test.json"
        doc = load_hint_rules_from_path(p)
        self.assertEqual(doc.get("rules"), [])
        self.assertIn("top_factors_template", doc)
        self.assertIn("fallback_hint", doc)

    def test_valid_json_roundtrip(self) -> None:
        payload = {"rules": [{"id": "t", "hint": "hi"}], "top_factors_template": "x"}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write(json.dumps(payload, ensure_ascii=False))
            path = Path(f.name)
        try:
            doc = load_hint_rules_from_path(path)
            self.assertEqual(len(doc.get("rules") or []), 1)
            self.assertEqual((doc.get("rules") or [{}])[0].get("id"), "t")
        finally:
            path.unlink(missing_ok=True)

    def test_invalid_json_falls_back(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("{ not json")
            path = Path(f.name)
        try:
            doc = load_hint_rules_from_path(path)
            self.assertEqual(doc.get("rules"), [])
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
