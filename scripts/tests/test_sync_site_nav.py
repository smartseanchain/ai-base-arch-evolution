"""sync_site_nav 生成结果与 span 计算。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sync_site_nav import (  # noqa: E402
    build_header,
    build_skip_bar,
    load_template_nav,
    load_template_skip,
    site_nav_span,
    skip_bar_span,
)


class TestBuildHeader(unittest.TestCase):
    def setUp(self) -> None:
        self.template = load_template_nav()

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


class TestSkipBar(unittest.TestCase):
    def setUp(self) -> None:
        self.tpl = load_template_skip()

    def test_index_anchor(self) -> None:
        s = build_skip_bar("index.html", self.tpl)
        self.assertIn('href="#main"', s)
        self.assertIn('href="#three-questions"', s)

    def test_other_page(self) -> None:
        s = build_skip_bar("lab.html", self.tpl)
        self.assertIn('href="index.html#three-questions"', s)

    def test_span_on_lab(self) -> None:
        text = (ROOT / "lab.html").read_text(encoding="utf-8")
        sp = skip_bar_span(text)
        self.assertIsNotNone(sp)
        a, b = sp
        self.assertIn("skip-bar", text[a:b])


if __name__ == "__main__":
    unittest.main()
