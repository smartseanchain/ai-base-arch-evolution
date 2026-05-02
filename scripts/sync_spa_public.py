#!/usr/bin/env python3
"""
为 SPA 开发/构建准备 spa/public：复制 assets、docs、CONTRIBUTING.md；根目录 HTML 去掉顶栏与 skip-bar 后写入 public
（避免与 React 壳重复导航）。index.html → legacy-index.html。404、legacy-all-in-one 整页拷贝不剥壳。

用法（仓库根）: python3 scripts/sync_spa_public.py

合并与双轨对表: docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · make help（CONTRIBUTING.md#contributing-five-minute · #contributing-pr-evidence-triad · #contributing-change-to-command）
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

SPA_PUBLIC = REPO_ROOT / "spa" / "public"

HEADER_INNER_RE = re.compile(
    r"<header class=\"site-nav\">.*?</header>",
    re.DOTALL,
)
SKIP_BAR_RE = re.compile(
    r'<div class="skip-bar"[^>]*>.*?</div>',
    re.DOTALL,
)

NO_STRIP = frozenset({"404.html", "legacy-all-in-one.html"})


def strip_chrome(html: str) -> str:
    html = SKIP_BAR_RE.sub("", html)
    html = HEADER_INNER_RE.sub("", html)
    return html


def main() -> None:
    if not (REPO_ROOT / "spa" / "package.json").is_file():
        print("错误: 缺少 spa/package.json", file=sys.stderr)
        sys.exit(1)

    SPA_PUBLIC.mkdir(parents=True, exist_ok=True)

    assets_src = REPO_ROOT / "assets"
    assets_dst = SPA_PUBLIC / "assets"
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(assets_src, assets_dst)

    docs_src = REPO_ROOT / "docs"
    docs_dst = SPA_PUBLIC / "docs"
    if docs_dst.exists():
        shutil.rmtree(docs_dst)
    shutil.copytree(docs_src, docs_dst)

    contrib_src = REPO_ROOT / "CONTRIBUTING.md"
    if contrib_src.is_file():
        shutil.copy2(contrib_src, SPA_PUBLIC / "CONTRIBUTING.md")

    for p in sorted(REPO_ROOT.glob("*.html")):
        text = p.read_text(encoding="utf-8")
        if p.name == "404.html":
            # 构建产物会用 SPA 的 index 覆盖 dist/404.html（Pages 路由回退），原 404 改名单独保留
            (SPA_PUBLIC / "standalone-404.html").write_text(text, encoding="utf-8")
            continue
        if p.name in NO_STRIP:
            out = SPA_PUBLIC / p.name
            out.write_text(text, encoding="utf-8")
            continue
        stripped = strip_chrome(text)
        if p.name == "index.html":
            out = SPA_PUBLIC / "legacy-index.html"
        else:
            out = SPA_PUBLIC / p.name
        out.write_text(stripped, encoding="utf-8")

    print(f"OK: 已同步到 {SPA_PUBLIC}（HTML 已去顶栏/skip-bar，除 404 与 legacy-all-in-one）")


if __name__ == "__main__":
    main()
