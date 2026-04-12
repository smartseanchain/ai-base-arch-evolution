"""evolution_pkg.ingest_json_http 单元测试（无网络）。"""
from __future__ import annotations

import json
import unittest

from evolution_pkg.ingest_json_http import (
    feed_parser_keys,
    normalize_item,
    parse_json_feed_body,
    resolve_items_list,
)


class TestResolveItemsList(unittest.TestCase):
    def test_root_array(self) -> None:
        self.assertEqual(
            resolve_items_list([{"title": "a"}], ""),
            [{"title": "a"}],
        )

    def test_root_must_be_list_when_empty_path(self) -> None:
        with self.assertRaises(TypeError):
            resolve_items_list({"x": 1}, "")

    def test_nested_path(self) -> None:
        root = {"data": {"items": [{"t": 1}]}}
        self.assertEqual(resolve_items_list(root, "data.items"), [{"t": 1}])


class TestNormalizeItem(unittest.TestCase):
    def test_url_as_link(self) -> None:
        d = normalize_item(
            {"title": "Hi", "url": "https://a.example/x"},
            keys_title=["title"],
            keys_link=["url"],
            keys_summary=["summary"],
        )
        assert d is not None
        self.assertEqual(d["link"], "https://a.example/x")

    def test_skip_non_object(self) -> None:
        self.assertIsNone(
            normalize_item(
                "nope",
                keys_title=["title"],
                keys_link=["url"],
                keys_summary=[],
            )
        )


class TestParseJsonFeedBody(unittest.TestCase):
    def test_orz_style_wrapper(self) -> None:
        payload = {
            "data": [
                {"title": "One", "url": "https://ex/1"},
                {"title": "Two", "href": "https://ex/2"},
            ]
        }
        raw = json.dumps(payload).encode()
        items, n_raw = parse_json_feed_body(
            raw,
            items_path="data",
            keys_title=["title"],
            keys_link=["url", "href"],
            keys_summary=["summary"],
            max_items=10,
        )
        self.assertEqual(n_raw, 2)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "One")


class TestFeedParserKeys(unittest.TestCase):
    def test_defaults(self) -> None:
        kt, kl, ks = feed_parser_keys({})
        self.assertIn("title", kt)
        self.assertIn("url", kl)

    def test_custom_lists(self) -> None:
        kt, kl, ks = feed_parser_keys(
            {
                "keys_title": ["headline"],
                "keys_link": ["permalink"],
                "keys_summary": ["blurb"],
            }
        )
        self.assertEqual(kt, ["headline"])
        self.assertEqual(kl, ["permalink"])
        self.assertEqual(ks, ["blurb"])


if __name__ == "__main__":
    unittest.main()
