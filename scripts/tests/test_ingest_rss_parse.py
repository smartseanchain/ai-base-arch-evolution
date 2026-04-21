"""``evolution_pkg.ingest_rss`` · RSS / Atom 解析。"""
from __future__ import annotations

import unittest

from evolution_pkg.ingest_rss import parse_rss_or_atom


class TestParseRssOrAtom(unittest.TestCase):
    def test_rss_channel_item(self) -> None:
        xml = b"""<?xml version="1.0"?>
<rss><channel>
  <item><title>Hello</title><link>https://ex/a</link>
  <description>Desc</description><pubDate>Mon, 01 Jan 2024</pubDate></item>
</channel></rss>"""
        rows = parse_rss_or_atom(xml)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Hello")
        self.assertEqual(rows[0]["link"], "https://ex/a")
        self.assertEqual(rows[0]["summary"], "Desc")
        self.assertIn("2024", rows[0]["pub"])

    def test_atom_entry(self) -> None:
        xml = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Atom T</title>
    <link href="https://ex/b" rel="alternate"/>
    <summary>Sum</summary>
    <updated>2024-02-01T00:00:00Z</updated>
  </entry>
</feed>"""
        rows = parse_rss_or_atom(xml)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Atom T")
        self.assertEqual(rows[0]["link"], "https://ex/b")
        self.assertEqual(rows[0]["summary"], "Sum")

    def test_unknown_root_empty(self) -> None:
        self.assertEqual(parse_rss_or_atom(b"<html></html>"), [])


if __name__ == "__main__":
    unittest.main()
