#!/usr/bin/env python3
"""
将根目录各页的 skip-bar 与 site-nav 与 partials 同步：
  - partials/skip-bar.inc.html
  - partials/site-nav.inc.html

按当前文件名：`index.html` 上「三问导读 / 顶栏三问」用 `#three-questions`，其余页用 `index.html#three-questions`；
「读站指路」在总览为 `#read-guide`，其余页为 `index.html#read-guide`；
「分区速跳」在总览为 `#hub-catalog`，其余页为 `index.html#hub-catalog`；
顶栏当前页链接打 class=\"current\"。

跳过：404.html、legacy-all-in-one.html。

用法：
  python3 scripts/sync_site_nav.py          # 写回各 HTML
  python3 scripts/sync_site_nav.py --check  # 仅校验（CI）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

PARTIAL_NAV = REPO_ROOT / "partials" / "site-nav.inc.html"
PARTIAL_SKIP = REPO_ROOT / "partials" / "skip-bar.inc.html"
SKIP = frozenset({"404.html", "legacy-all-in-one.html"})

HEADER_INNER_RE = re.compile(
    r"<header class=\"site-nav\">.*?</header>",
    re.DOTALL,
)
SKIP_BAR_RE = re.compile(
    r'<div class="skip-bar"[^>]*>.*?</div>',
    re.DOTALL,
)


def threeq_href(basename: str) -> str:
    return "#three-questions" if basename == "index.html" else "index.html#three-questions"


def hub_catalog_href(basename: str) -> str:
    return "#hub-catalog" if basename == "index.html" else "index.html#hub-catalog"


def read_guide_href(basename: str) -> str:
    return "#read-guide" if basename == "index.html" else "index.html#read-guide"


def _span_with_leading_indent(text: str, inner_start: int, inner_end: int) -> tuple[int, int]:
    start = inner_start
    while start > 0 and text[start - 1] in " \t":
        start -= 1
    return start, inner_end


def site_nav_span(text: str) -> tuple[int, int] | None:
    m = HEADER_INNER_RE.search(text)
    if not m:
        return None
    return _span_with_leading_indent(text, m.start(), m.end())


def skip_bar_span(text: str) -> tuple[int, int] | None:
    m = SKIP_BAR_RE.search(text)
    if not m:
        return None
    return _span_with_leading_indent(text, m.start(), m.end())


def load_template_nav() -> str:
    if not PARTIAL_NAV.is_file():
        print(f"错误: 缺少导航模板 {PARTIAL_NAV}", file=sys.stderr)
        sys.exit(1)
    return PARTIAL_NAV.read_text(encoding="utf-8")


def load_template_skip() -> str:
    if not PARTIAL_SKIP.is_file():
        print(f"错误: 缺少 skip-bar 模板 {PARTIAL_SKIP}", file=sys.stderr)
        sys.exit(1)
    return PARTIAL_SKIP.read_text(encoding="utf-8")


def build_header(basename: str, template: str) -> str:
    block = (
        template.replace("__THREEQ_NAV_HREF__", threeq_href(basename))
        .replace("__HUB_CATALOG_NAV_HREF__", hub_catalog_href(basename))
    )
    # 允许 <a href="page.html" …>（如 title）；须唯一点到本页分页链，勿用裸 ">" 匹配以免误伤其他 href。
    open_prefix = f'<a href="{basename}"'
    idx = block.find(open_prefix)
    if idx == -1:
        print(f"错误: 导航模板中无链接 {open_prefix}", file=sys.stderr)
        sys.exit(1)
    j = idx + len(open_prefix)
    if block.startswith(" class=", j):
        return block.rstrip("\n\r")
    block = block[:j] + ' class="current"' + block[j:]
    return block.rstrip("\n\r")


def build_skip_bar(basename: str, template: str) -> str:
    return (
        template.replace("__THREEQ_SKIP_HREF__", threeq_href(basename))
        .replace("__READ_GUIDE_SKIP_HREF__", read_guide_href(basename))
        .replace("__HUB_CATALOG_SKIP_HREF__", hub_catalog_href(basename))
        .rstrip("\n\r")
    )


def html_targets() -> list[Path]:
    return [p for p in sorted(REPO_ROOT.glob("*.html")) if p.name not in SKIP]


def main() -> None:
    ap = argparse.ArgumentParser(description="同步全站 skip-bar 与 site-nav")
    ap.add_argument(
        "--check",
        action="store_true",
        help="不写入，若任一页与生成结果不一致则退出 1",
    )
    args = ap.parse_args()
    tpl_nav = load_template_nav()
    tpl_skip = load_template_skip()
    paths = html_targets()
    drift = False
    updated = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        span_sb = skip_bar_span(text)
        if span_sb is None:
            print(f"错误: {path.name} 中未找到 skip-bar", file=sys.stderr)
            drift = True
            continue

        exp_skip = build_skip_bar(path.name, tpl_skip)
        got_skip = text[span_sb[0] : span_sb[1]]
        skip_ok = got_skip == exp_skip

        span_nav = site_nav_span(text)
        if span_nav is None:
            print(f"错误: {path.name} 中未找到 site-nav header", file=sys.stderr)
            drift = True
            continue
        exp_nav = build_header(path.name, tpl_nav)
        got_nav = text[span_nav[0] : span_nav[1]]
        nav_ok = got_nav == exp_nav

        if skip_ok and nav_ok:
            continue
        drift = True
        if args.check:
            if not skip_ok or not nav_ok:
                print(
                    f"漂移: {path.name}（请运行: python3 scripts/sync_site_nav.py）",
                    file=sys.stderr,
                )
        else:
            if not skip_ok:
                text = text[: span_sb[0]] + exp_skip + text[span_sb[1] :]
            span_nav = site_nav_span(text)
            if span_nav is None:
                print(f"错误: {path.name} 替换 skip-bar 后丢失 site-nav", file=sys.stderr)
                drift = True
                continue
            exp_nav = build_header(path.name, tpl_nav)
            got_nav = text[span_nav[0] : span_nav[1]]
            if got_nav != exp_nav:
                text = text[: span_nav[0]] + exp_nav + text[span_nav[1] :]
            path.write_text(text, encoding="utf-8")
            updated += 1
            print(f"已更新 {path.name}")

    if args.check:
        if drift:
            sys.exit(1)
        print(
            f"OK: skip-bar + site-nav 与 partials 一致（{len(paths)} 页）"
        )
    elif updated == 0:
        print(f"OK: 无需变更（{len(paths)} 页）")
    else:
        print(f"OK: 已更新 {updated} 页")


if __name__ == "__main__":
    main()
