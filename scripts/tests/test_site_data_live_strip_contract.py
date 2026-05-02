"""读数条 `data-site-data-live` 与 `snapshot-only` 约定（对表 SITE_DATA_UPDATE_FRAMEWORK）。"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from evolution_pkg.io import REPO_ROOT, REGISTRY_JSON_PATH


_STRIP_LINE_MARKER = '<aside class="card site-data-live-strip-host"'
# 条带内请求 sediment-trends.json 的例外页（闭环 / 沙盘）
_FULL_TRENDS_PAGES = frozenset({"evolution-loop.html", "lab.html"})
_ANALYSIS_HUB = "analysis-hub.html"


def _registry_pages() -> list[str]:
    doc = json.loads(REGISTRY_JSON_PATH.read_text(encoding="utf-8"))
    pages = doc.get("pages")
    assert isinstance(pages, list)
    return sorted(str(p).strip() for p in pages if str(p).strip())


class TestSiteDataLiveStripContract(unittest.TestCase):
    def test_registry_pages_have_exactly_one_live_strip_aside(self) -> None:
        for page in _registry_pages():
            path = REPO_ROOT / page
            self.assertTrue(path.is_file(), msg=f"registry 列出但缺少文件: {page}")
            text = path.read_text(encoding="utf-8")
            lines = [ln for ln in text.splitlines() if _STRIP_LINE_MARKER in ln]
            self.assertEqual(
                len(lines),
                1,
                msg=f"{page} 须有且仅有一条读数条 <aside（维护站点数据更新框架 §3a）",
            )

    def test_snapshot_only_policy(self) -> None:
        for page in _registry_pages():
            path = REPO_ROOT / page
            text = path.read_text(encoding="utf-8")
            line = next(ln for ln in text.splitlines() if _STRIP_LINE_MARKER in ln)
            if page in _FULL_TRENDS_PAGES:
                self.assertNotIn(
                    "snapshot-only",
                    line,
                    msg=f"{page} 为全量条带页，勿加 snapshot-only",
                )
                self.assertIn("data-site-data-live", line)
            else:
                self.assertIn(
                    'data-site-data-live="snapshot-only"',
                    line,
                    msg=f"{page} 须为 snapshot-only（见 SITE_DATA_UPDATE_FRAMEWORK）",
                )
            if page == _ANALYSIS_HUB:
                self.assertIn(
                    'data-site-data-hub="#dashboard"',
                    line,
                    msg="analysis-hub 条带须指向本页仪表盘锚点",
                )


if __name__ == "__main__":
    unittest.main()
