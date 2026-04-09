#!/usr/bin/env python3
"""
将根目录各页的 <header class="site-nav">…</header> 与 partials/site-nav.inc.html 同步，
并按当前文件名打上 class=\"current\"。

跳过：404.html（极简顶栏）、legacy-all-in-one.html（单页归档无站导航）。

用法：
  python3 scripts/sync_site_nav.py          # 写回各 HTML
  python3 scripts/sync_site_nav.py --check  # 仅校验（CI）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTIAL = ROOT / "partials" / "site-nav.inc.html"
SKIP = frozenset({"404.html", "legacy-all-in-one.html"})
HEADER_INNER_RE = re.compile(
    r"<header class=\"site-nav\">.*?</header>",
    re.DOTALL,
)


def site_nav_span(text: str) -> tuple[int, int] | None:
    """返回待替换区间 [start, end)，含 <header 前的行内缩进（避免重复缩进）。"""
    m = HEADER_INNER_RE.search(text)
    if not m:
        return None
    start = m.start()
    while start > 0 and text[start - 1] in " \t":
        start -= 1
    return start, m.end()


def load_template() -> str:
    if not PARTIAL.is_file():
        print(f"错误: 缺少导航模板 {PARTIAL}", file=sys.stderr)
        sys.exit(1)
    return PARTIAL.read_text(encoding="utf-8")


def build_header(basename: str, template: str) -> str:
    threeq = "#three-questions" if basename == "index.html" else "index.html#three-questions"
    block = template.replace("__THREEQ_NAV_HREF__", threeq)
    needle = f'<a href="{basename}">'
    repl = f'<a href="{basename}" class="current">'
    if needle not in block:
        print(f"错误: 模板中无链接 {needle}", file=sys.stderr)
        sys.exit(1)
    return block.replace(needle, repl, 1).rstrip("\n\r")


def html_targets() -> list[Path]:
    return [p for p in sorted(ROOT.glob("*.html")) if p.name not in SKIP]


def main() -> None:
    ap = argparse.ArgumentParser(description="同步全站 site-nav 顶栏")
    ap.add_argument(
        "--check",
        action="store_true",
        help="不写入，若任一页与生成结果不一致则退出 1",
    )
    args = ap.parse_args()
    template = load_template()
    paths = html_targets()
    drift = False
    updated = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        span = site_nav_span(text)
        if span is None:
            print(f"错误: {path.name} 中未找到 site-nav header", file=sys.stderr)
            drift = True
            continue
        start, end = span
        got = text[start:end]
        expected = build_header(path.name, template)
        if got == expected:
            continue
        drift = True
        if args.check:
            print(
                f"漂移: {path.name}（请运行: python3 scripts/sync_site_nav.py）",
                file=sys.stderr,
            )
        else:
            path.write_text(text[:start] + expected + text[end:], encoding="utf-8")
            updated += 1
            print(f"已更新 {path.name}")

    if args.check:
        if drift:
            sys.exit(1)
        print(f"OK: site-nav 与 {PARTIAL.relative_to(ROOT)} 一致（{len(paths)} 页）")
    elif updated == 0:
        print(f"OK: 无需变更（{len(paths)} 页）")
    else:
        print(f"OK: 已更新 {updated} 页")


if __name__ == "__main__":
    main()
