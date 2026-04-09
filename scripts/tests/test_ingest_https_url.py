"""ingest：仅允许 https 抓取 URL。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ingest_opinion_law import (  # noqa: E402
    assert_https_ingest_url,
    validate_config_fetch_urls,
)


class TestIngestHttpsUrl(unittest.TestCase):
    def test_rejects_http(self) -> None:
        with self.assertRaises(ValueError):
            assert_https_ingest_url("http://www.example.com/feed.xml", "t")

    def test_accepts_https(self) -> None:
        assert_https_ingest_url("https://www.example.com/feed.xml", "t")

    def test_rejects_missing_host(self) -> None:
        with self.assertRaises(ValueError):
            assert_https_ingest_url("https:///nope", "t")

    def test_validate_config_rejects_http_feed(self) -> None:
        with self.assertRaises(ValueError):
            validate_config_fetch_urls(
                {"rss_feeds": [{"id": "x", "url": "http://evil.example/a"}]}
            )

    def test_validate_config_ok_https(self) -> None:
        validate_config_fetch_urls(
            {
                "rss_feeds": [{"id": "x", "url": "https://good.example/a"}],
                "law_html_pages": [],
            }
        )


if __name__ == "__main__":
    unittest.main()
