"""SpaLayout 壳内 skip 前五链与 partials/skip-bar.inc.html 顺序、语义对齐。"""
from __future__ import annotations

import re
import unittest

from evolution_pkg.io import REPO_ROOT

_LAYOUT = REPO_ROOT / "spa" / "src" / "SpaLayout.tsx"


def _spa_skip_block(text: str) -> str:
    m = re.search(
        r'className="spa-skip-bar"[^>]*>[\s\S]*?</div>',
        text,
    )
    if not m:
        raise AssertionError("SpaLayout.tsx 中未找到 spa-skip-bar 块")
    return m.group(0)


class TestSpaSkipBarParity(unittest.TestCase):
    def test_five_chains_before_pagination_skip(self) -> None:
        body = _LAYOUT.read_text(encoding="utf-8")
        block = _spa_skip_block(body)
        p_main = block.find("#spa-main")
        p_three = block.find('hash: "three-questions"')
        p_read = block.find('hash: "read-guide"')
        p_hub = block.find('hash: "hub-catalog"')
        p_reader = block.find('hash: "reader-next"')
        p_nav = block.find("#spa-site-nav")
        for name, pos in (
            ("#spa-main", p_main),
            ("three-questions", p_three),
            ("read-guide", p_read),
            ("hub-catalog", p_hub),
            ("reader-next", p_reader),
            ("#spa-site-nav", p_nav),
        ):
            with self.subTest(marker=name):
                self.assertGreaterEqual(pos, 0, f"缺少 {name!r}")
        self.assertLess(p_main, p_three)
        self.assertLess(p_three, p_read)
        self.assertLess(p_read, p_hub)
        self.assertLess(p_hub, p_reader)
        self.assertLess(p_reader, p_nav)


if __name__ == "__main__":
    unittest.main()
