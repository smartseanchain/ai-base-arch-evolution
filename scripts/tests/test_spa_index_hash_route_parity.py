"""总览 hash 在 spaRouteMeta 与 LegacyFrame 中的文案须成对存在（防 MPA/SPA 标题与 iframe 漂移）。"""
from __future__ import annotations

import unittest
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

_META = REPO_ROOT / "spa" / "src" / "spaRouteMeta.ts"
_FRAME = REPO_ROOT / "spa" / "src" / "LegacyFrame.tsx"

# 与 index.html 内 toc / 锚点及壳层约定一致；改 MPA 或 SPA 时须同步本表与 spa/README、CONTRIBUTING。
INDEX_HASH_LABELS: tuple[tuple[str, str], ...] = (
    ("#hub-catalog", "分区速跳"),
    ("#index-intent-pick", "四条动线"),
    ("#read-guide", "读站指路"),
    ("#three-questions", "三问导读"),
    ("#reader-next", "常见下一站"),
)


class TestSpaIndexHashRouteParity(unittest.TestCase):
    def test_spa_route_meta_contains_hash_and_labels(self) -> None:
        text = _META.read_text(encoding="utf-8")
        for h, label in INDEX_HASH_LABELS:
            with self.subTest(hash=h, label=label):
                self.assertIn(f'if (hash === "{h}")', text)
                self.assertIn(f"总览 · {label}", text)
                self.assertIn(f'当前：总览 · {label}', text)

    def test_legacy_frame_index_hash_returns(self) -> None:
        text = _FRAME.read_text(encoding="utf-8")
        for h, label in INDEX_HASH_LABELS:
            with self.subTest(hash=h, label=label):
                self.assertIn(
                    f'if (hash === "{h}") return "总览 · {label}";',
                    text,
                )


if __name__ == "__main__":
    unittest.main()
