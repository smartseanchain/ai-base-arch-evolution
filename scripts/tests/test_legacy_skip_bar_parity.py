"""legacy-all-in-one.html 五链 skip 与 partials/skip-bar.inc.html 意图对齐（不经 sync_site_nav 写回）。"""
from __future__ import annotations

import re
import unittest

from evolution_pkg.io import REPO_ROOT

_LEGACY = REPO_ROOT / "legacy-all-in-one.html"
_PARTIAL = REPO_ROOT / "partials" / "skip-bar.inc.html"


def _skip_bar_inner(html: str) -> str | None:
    m = re.search(
        r'<div\s+class="skip-bar"[^>]*>(.*?)</div>\s*',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    return m.group(1) if m else None


class TestLegacySkipBarParity(unittest.TestCase):
    def test_partial_has_reader_next_placeholder(self) -> None:
        tpl = _PARTIAL.read_text(encoding="utf-8")
        self.assertIn("__READER_NEXT_SKIP_HREF__", tpl)
        self.assertIn("常见下一站", tpl)

    def test_legacy_skip_five_hrefs(self) -> None:
        body = _LEGACY.read_text(encoding="utf-8")
        inner = _skip_bar_inner(body)
        self.assertIsNotNone(inner, "legacy-all-in-one.html 缺少 skip-bar 块")
        assert inner is not None
        self.assertIn('href="#main"', inner, "第一链须跳到本页正文地标 #main")
        for frag, label in (
            ("index.html#three-questions", "三问导读"),
            ("index.html#read-guide", "读站指路"),
            ("index.html#hub-catalog", "分区速跳"),
            ("index.html#reader-next", "常见下一站"),
        ):
            with self.subTest(label=label):
                self.assertIn(frag, inner, f"skip-bar 缺少 {label} 链 {frag!r}")

    def test_legacy_skip_link_texts(self) -> None:
        inner = _skip_bar_inner(_LEGACY.read_text(encoding="utf-8"))
        assert inner is not None
        for text in ("跳到正文", "三问导读", "读站指路", "分区速跳", "常见下一站"):
            with self.subTest(text=text):
                self.assertIn(text, inner)


if __name__ == "__main__":
    unittest.main()
