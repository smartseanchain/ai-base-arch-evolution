"""``gen_site_search_index`` 标题解析与 ``build_doc`` 形状（不写盘）。"""
from __future__ import annotations

import unittest


class TestExtractTitle(unittest.TestCase):
    def test_plain_title(self) -> None:
        from gen_site_search_index import extract_title

        html = "<html><head><title>Foo · Bar</title></head></html>"
        self.assertEqual(extract_title(html), "Foo · Bar")

    def test_collapses_whitespace(self) -> None:
        from gen_site_search_index import extract_title

        html = "<title>  A\n\tB  </title>"
        self.assertEqual(extract_title(html), "A B")

    def test_case_insensitive(self) -> None:
        from gen_site_search_index import extract_title

        html = "<TITLE>x</TITLE>"
        self.assertEqual(extract_title(html), "x")

    def test_missing_returns_empty(self) -> None:
        from gen_site_search_index import extract_title

        self.assertEqual(extract_title("<html></html>"), "")


class TestBuildDocShape(unittest.TestCase):
    def test_build_doc_matches_registry(self) -> None:
        from gen_site_search_index import build_doc

        doc = build_doc()
        self.assertEqual(doc.get("schema_version"), 1)
        self.assertIn("generated_at", doc)
        self.assertIn("entries", doc)
        entries = doc["entries"]
        self.assertIsInstance(entries, list)
        self.assertGreaterEqual(len(entries), 1)
        for e in entries:
            self.assertIn("path", e)
            self.assertIn("title", e)
            self.assertIsInstance(e["path"], str)
            self.assertIsInstance(e["title"], str)
            self.assertTrue(e["path"].endswith(".html"), msg=e["path"])


if __name__ == "__main__":
    unittest.main()
