"""sync_site_nav 生成结果与 span 计算。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sync_site_nav import build_header, load_template, site_nav_span  # noqa: E402


class TestBuildHeader(unittest.TestCase):
    def setUp(self) -> None:
        self.template = load_template()

    def test_index_threeq_href(self) -> None:
        h = build_header("index.html", self.template)
        self.assertIn('href="#three-questions"', h)
        self.assertIn('href="index.html" class="current"', h)
        self.assertIn('class="site-nav-threeq"', h)

    def test_other_page_threeq(self) -> None:
        h = build_header("nexus.html", self.template)
        self.assertIn('href="index.html#three-questions"', h)
        self.assertIn('href="nexus.html" class="current"', h)


class TestSiteNavSpan(unittest.TestCase):
    def test_index_has_span(self) -> None:
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        span = site_nav_span(text)
        self.assertIsNotNone(span)
        start, end = span
        self.assertTrue(text[start:end].strip().startswith("<header"))
        self.assertIn("</header>", text[start:end])


if __name__ == "__main__":
    unittest.main()
