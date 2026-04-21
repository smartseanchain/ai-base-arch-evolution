"""spa/nav.config 与 evolution_pkg.spa_nav 的 JSON Schema 行为。"""
from __future__ import annotations

import unittest

from evolution_pkg.spa_nav import nav_config_schema_violations


class TestSpaNavConfigSchema(unittest.TestCase):
    def test_valid_minimal_passes(self) -> None:
        doc = {
            "schema_version": 1,
            "items": [{"page": "index.html", "label": "总览"}],
        }
        self.assertEqual(nav_config_schema_violations(doc), [])

    def test_missing_items_fails(self) -> None:
        doc = {"schema_version": 1}
        errs = nav_config_schema_violations(doc)
        self.assertTrue(errs, msg="须报 Schema 错误")
        self.assertIn("Schema", errs[0])

    def test_page_must_end_with_html(self) -> None:
        doc = {
            "schema_version": 1,
            "items": [{"page": "index.htm", "label": "x"}],
        }
        errs = nav_config_schema_violations(doc)
        self.assertTrue(errs)

    def test_extra_root_property_fails(self) -> None:
        doc = {
            "schema_version": 1,
            "items": [{"page": "index.html", "label": "总览"}],
            "bogus": 1,
        }
        errs = nav_config_schema_violations(doc)
        self.assertTrue(errs)

    def test_optional_group_on_items_passes(self) -> None:
        doc = {
            "schema_version": 1,
            "items": [
                {"page": "index.html", "label": "总览"},
                {"page": "nexus.html", "label": "立体联结", "group": "联结与模型"},
            ],
        }
        self.assertEqual(nav_config_schema_violations(doc), [])


if __name__ == "__main__":
    unittest.main()
