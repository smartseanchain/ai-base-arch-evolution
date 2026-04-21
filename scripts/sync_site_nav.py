#!/usr/bin/env python3
"""
将根目录各注册页的 skip-bar 与 site-nav 与 partials 真源同步。

真源文件（改后须 ``make sync-nav``，再 ``make validate``）：
  - ``partials/skip-bar.inc.html`` — 五链占位符（``__THREEQ_SKIP_HREF__`` 等）
  - ``partials/site-nav.inc.html`` — 顶栏；当前页 ``<a href="basename">`` 加 ``class="current"``

按当前文件名替换占位符：
  - ``index.html``：三问/读站/分区/常见下一站 用页内 ``#…``；其余页用 ``index.html#…``（与模板一致）。
  - 顶栏「三问」「分区」链同理（``threeq_href`` / ``hub_catalog_href`` 等）。

**maintainer-hub.html（仅此页）**：``build_skip_bar()`` 在五链之后插入
``MAINTAINER_HUB_SKIP_EXTRA``（``#mh-spine-map`` / ``#mh-boundaries`` / ``#mh-reader-admin-matrix``），
并把外层 ``aria-label`` 从「快捷跳转」改为「快捷跳转与本页锚点」。
``MAINTAINER_HUB_SKIP_EXTRA`` 的 href 与文案须与 ``maintainer-hub.html`` 内 ``nav.toc--pilot``
（或同 id 的节标题）一致；改锚时同步本常量并跑单测
``scripts/tests/test_sync_site_nav.py`` · ``test_maintainer_hub_extra_anchors_after_five_chain``（期望 **8** 条 ``skip-link``）。
**勿**在 ``maintainer-hub.html`` 手改上述三段，否则 ``sync_site_nav --check`` 漂移。

跳过写回：``404.html``、``legacy-all-in-one.html``（失页与归档页手维护；404 与 partial 对表见 ``check_skip_bar_404.py``）。

**注释位置**：与顶栏/skip 相关的 ``<!-- … -->`` 只能写在 **``partials/``** 模板里、且须落在 **``<div class="skip-bar">`` / ``<header class="site-nav">`` 内部**；勿在块外再贴一份，否则 ``--check`` 替换范围不含块外注释，易产生重复或与真源漂移。

用法：
  python3 scripts/sync_site_nav.py          # 写回各 HTML
  python3 scripts/sync_site_nav.py --check  # 仅校验（CI）

改根 ``*.html`` 后若仍维护 SPA 壳内 iframe：须 ``make spa-sync``（或 ``make spa-build``）。

对表：``docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge`` · ``#pre-merge-partials-sequence`` · ``scripts/README.md``（``sync_site_nav`` 行）·
``maintainer-hub.html#mh-spine-map`` · ``#mh-boundaries`` · ``#mh-reader-admin-matrix`` · ``make help``
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

# 维护导读页：在五链之后追加与本页 TOC（toc--pilot）一致的页内锚；改 id/文案时同步此处并 make sync-nav。
MAINTAINER_HUB_SKIP_EXTRA = """      <a class="skip-link" href="#mh-spine-map">关系视图</a>
      <a class="skip-link" href="#mh-boundaries">系统边界</a>
      <a class="skip-link" href="#mh-reader-admin-matrix">衔接矩阵</a>"""

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


def reader_next_href(basename: str) -> str:
    return "#reader-next" if basename == "index.html" else "index.html#reader-next"


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
    """从 ``template`` 生成单页 skip-bar HTML。

    ``maintainer-hub.html``：五链后追加 ``MAINTAINER_HUB_SKIP_EXTRA``，并替换 ``aria-label``。
    其余页：仅五链，不含 ``#mh-*``。
    """
    base = (
        template.replace("__THREEQ_SKIP_HREF__", threeq_href(basename))
        .replace("__READ_GUIDE_SKIP_HREF__", read_guide_href(basename))
        .replace("__HUB_CATALOG_SKIP_HREF__", hub_catalog_href(basename))
        .replace("__READER_NEXT_SKIP_HREF__", reader_next_href(basename))
        .rstrip("\n\r")
    )
    if basename != "maintainer-hub.html":
        return base
    base = base.replace(
        'aria-label="快捷跳转"',
        'aria-label="快捷跳转与本页锚点"',
        1,
    )
    idx = base.rfind("</div>")
    if idx == -1:
        print("错误: skip-bar 模板闭合 </div> 缺失", file=sys.stderr)
        sys.exit(1)
    prefix = base[:idx].rstrip()
    return prefix + "\n" + MAINTAINER_HUB_SKIP_EXTRA + "\n    </div>"


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
