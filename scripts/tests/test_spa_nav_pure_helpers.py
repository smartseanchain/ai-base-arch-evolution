"""evolution_pkg.spa_nav · page_to_route / parse_nav_config_items（无磁盘 I/O）。"""
from __future__ import annotations

import unittest

from evolution_pkg.spa_nav import page_to_route, parse_nav_config_items


class TestPageToRoute(unittest.TestCase):
    def test_cases(self) -> None:
        cases = [
            ("index.html", "/"),
            ("nexus.html", "/nexus"),
            ("analysis-hub.html", "/analysis-hub"),
            ("decade-scenes.html", "/decade-scenes"),
        ]
        for page, want in cases:
            with self.subTest(page=page):
                self.assertEqual(page_to_route(page), want)


class TestParseNavConfigItems(unittest.TestCase):
    def test_valid_and_group_trim(self) -> None:
        raw = {
            "schema_version": 1,
            "items": [
                {"page": "index.html", "label": "总览"},
                {
                    "page": "nexus.html",
                    "label": "立体联结",
                    "group": "  联结与模型  ",
                },
            ],
        }
        rows = parse_nav_config_items(raw)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["group"], None)
        self.assertEqual(rows[1]["group"], "联结与模型")

    def test_empty_group_string_becomes_none(self) -> None:
        raw = {
            "schema_version": 1,
            "items": [
                {"page": "index.html", "label": "总览", "group": ""},
                {"page": "nexus.html", "label": "x", "group": "   "},
            ],
        }
        rows = parse_nav_config_items(raw)
        self.assertIsNone(rows[0]["group"])
        self.assertIsNone(rows[1]["group"])

    def test_missing_items_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_nav_config_items({"schema_version": 1})

    def test_items_not_list_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_nav_config_items({"schema_version": 1, "items": {}})

    def test_row_not_object_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_nav_config_items({"schema_version": 1, "items": ["x"]})

    def test_missing_page_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_nav_config_items(
                {"schema_version": 1, "items": [{"label": "only"}]}
            )


if __name__ == "__main__":
    unittest.main()
