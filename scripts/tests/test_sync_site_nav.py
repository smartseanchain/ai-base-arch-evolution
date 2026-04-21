"""sync_site_nav 生成结果与 span 计算。

maintainer-hub：五链 + 三页内锚（共 8 条 skip-link）见 TestSkipBar.test_maintainer_hub_extra_anchors_after_five_chain。
"""
from __future__ import annotations

import sys
import unittest

from evolution_pkg.io import REPO_ROOT

SCRIPTS = REPO_ROOT / "scripts"
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
        self.assertIn('href="#hub-catalog"', h)
        self.assertIn('href="index.html" class="current"', h)
        self.assertIn('class="site-nav-threeq"', h)

    def test_other_page_threeq(self) -> None:
        h = build_header("nexus.html", self.template)
        self.assertIn('href="index.html#three-questions"', h)
        self.assertIn('href="index.html#hub-catalog"', h)
        self.assertIn('href="nexus.html" class="current"', h)

    def test_maintainer_link_may_have_title_before_current(self) -> None:
        h = build_header("maintainer-hub.html", self.template)
        self.assertIn('href="maintainer-hub.html" class="current"', h)
        self.assertIn("reader-admin-surfaces", h)


class TestSiteNavSpan(unittest.TestCase):
    def test_index_has_span(self) -> None:
        text = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
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
        self.assertIn('href="#read-guide"', s)
        self.assertIn('href="#hub-catalog"', s)
        self.assertIn('href="#reader-next"', s)

    def test_other_page(self) -> None:
        s = build_skip_bar("lab.html", self.tpl)
        self.assertIn('href="index.html#three-questions"', s)
        self.assertIn('href="index.html#read-guide"', s)
        self.assertIn('href="index.html#hub-catalog"', s)
        self.assertIn('href="index.html#reader-next"', s)
        self.assertNotIn("#mh-spine-map", s)
        self.assertIn('aria-label="快捷跳转"', s)

    def test_maintainer_hub_extra_anchors_after_five_chain(self) -> None:
        s = build_skip_bar("maintainer-hub.html", self.tpl)
        self.assertIn('aria-label="快捷跳转与本页锚点"', s)
        self.assertIn('href="#mh-spine-map"', s)
        self.assertIn('href="#mh-boundaries"', s)
        self.assertIn('href="#mh-reader-admin-matrix"', s)
        self.assertEqual(s.count("skip-link"), 8)

    def test_span_on_lab(self) -> None:
        text = (REPO_ROOT / "lab.html").read_text(encoding="utf-8")
        sp = skip_bar_span(text)
        self.assertIsNotNone(sp)
        a, b = sp
        self.assertIn("skip-bar", text[a:b])


class TestReaderRootHtmlMainLandmark(unittest.TestCase):
    """根目录读者页与 skip-bar「#main」对读：单页仅一个 <main id=\"main\"> 包裹正文。"""

    _SKIP = frozenset({"legacy-all-in-one.html"})

    def test_root_html_with_skip_to_main_has_single_main_landmark(self) -> None:
        for path in sorted(REPO_ROOT.glob("*.html")):
            if path.name in self._SKIP:
                continue
            text = path.read_text(encoding="utf-8")
            if 'href="#main"' not in text:
                continue
            with self.subTest(path=path.name):
                self.assertNotIn(
                    '<div id="main"',
                    text,
                    msg="应使用 <main id=\"main\">，勿回退 div#main",
                )
                self.assertIn('<main id="main"', text)
                self.assertEqual(
                    text.count("<main"),
                    1,
                    msg="每页至多一个 <main> 地标",
                )
                self.assertIn("</main>", text)
                self.assertLess(text.find("<main"), text.find("</main>"))

    def test_synthesis_subpage_builder_templates_use_main_not_div_main(self) -> None:
        p = REPO_ROOT / "scripts" / "_build_synthesis_subpages.py"
        body = p.read_text(encoding="utf-8")
        self.assertNotIn("<div id=\"main\"", body)
        self.assertGreaterEqual(body.count("<main id=\"main\""), 3)
        self.assertGreaterEqual(body.count("</main>"), 3)


if __name__ == "__main__":
    unittest.main()
