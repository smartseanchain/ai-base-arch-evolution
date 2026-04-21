#!/usr/bin/env python3
"""
404.html 的 skip-bar 不经 sync_site_nav 写回，须与 partials/skip-bar.inc.html 的意图对齐。

不含 maintainer-hub 的 #mh-* 扩展（仅注册页由 sync_site_nav 写回；见 scripts/sync_site_nav.py）。

规则（与 docs/PLATFORM、SITE_REVIEW 一致）：
- 须含跳到正文（#main）、index.html#three-questions、index.html#read-guide（模板含读站指路占位时）。
- 第四链：模板为「分区速跳」；404 可用 index.html#hub-catalog **或** synthesis.html#continuation（失页回正常用矩阵）。
- 第五链：模板为「常见下一站」；404 须含 index.html#reader-next（与模板占位对齐）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

PARTIAL = REPO_ROOT / "partials" / "skip-bar.inc.html"
PAGE404 = REPO_ROOT / "404.html"


def _skip_bar_inner(html: str) -> str | None:
    m = re.search(
        r'<div\s+class="skip-bar"[^>]*>(.*?)</div>\s*',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    return m.group(1) if m else None


def main(*, quiet: bool = False) -> int:
    if not PARTIAL.is_file():
        print(f"错误: 缺少 {PARTIAL}", file=sys.stderr)
        return 1
    if not PAGE404.is_file():
        print(f"错误: 缺少 {PAGE404}", file=sys.stderr)
        return 1

    tpl = PARTIAL.read_text(encoding="utf-8")
    body = PAGE404.read_text(encoding="utf-8")
    inner = _skip_bar_inner(body)
    if not inner:
        print("错误: 404.html 中未找到 skip-bar 块", file=sys.stderr)
        return 1

    errs: list[str] = []
    if not re.search(r'href\s*=\s*["\']#main["\']', inner):
        errs.append("404 skip-bar 缺少跳到正文 #main")

    if "__THREEQ_SKIP_HREF__" in tpl and "index.html#three-questions" not in inner:
        errs.append("404 skip-bar 缺少 index.html#three-questions（与模板三问占位对齐）")

    if "__READ_GUIDE_SKIP_HREF__" in tpl and "index.html#read-guide" not in inner:
        errs.append("404 skip-bar 缺少 index.html#read-guide（与模板读站指路占位对齐）")

    if "__HUB_CATALOG_SKIP_HREF__" in tpl:
        if (
            "index.html#hub-catalog" not in inner
            and "synthesis.html#continuation" not in inner
        ):
            errs.append(
                "404 skip-bar 第四链须为 index.html#hub-catalog 或 synthesis.html#continuation"
            )

    if "__READER_NEXT_SKIP_HREF__" in tpl and "index.html#reader-next" not in inner:
        errs.append(
            "404 skip-bar 缺少 index.html#reader-next（与模板常见下一站占位对齐）"
        )

    if errs:
        for e in errs:
            print(f"漂移: {e}", file=sys.stderr)
        print(
            "请同步 404.html 的 skip-bar，或更新本脚本规则（若有意变更）。",
            file=sys.stderr,
        )
        return 1

    if not quiet:
        print("OK: 404.html skip-bar 与 partials/skip-bar.inc.html 对齐")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
