#!/usr/bin/env python3
"""
由 spa/nav.config.json 生成 spa/src/navLinks.ts（路由与 evolution-registry.json 对齐）。
用法：python3 scripts/gen_nav_links_ts.py --write
无参数：比对 navLinks.ts 与配置是否一致（同 check_nav_links_registry）

对表: docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · spa/README.md
"""
from __future__ import annotations

import argparse
import sys

from evolution_pkg.spa_nav import (
    NAV_LINKS_TS_PATH,
    expected_nav_links_ts_content,
    nav_config_registry_errors,
)


def main() -> None:
    p = argparse.ArgumentParser(
        description="从 spa/nav.config.json 生成或检查 spa/src/navLinks.ts"
    )
    p.add_argument(
        "--write",
        action="store_true",
        help="写入 navLinks.ts；默认仅 --check",
    )
    args = p.parse_args()

    errs = nav_config_registry_errors()
    if errs:
        for line in errs:
            print(line, file=sys.stderr)
        sys.exit(1)

    errors, content = expected_nav_links_ts_content()
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        sys.exit(1)

    if args.write:
        NAV_LINKS_TS_PATH.write_text(content, encoding="utf-8")
        print(f"OK: 已写入 {NAV_LINKS_TS_PATH}")
        return

    # --check 或默认
    actual = (
        NAV_LINKS_TS_PATH.read_text(encoding="utf-8")
        if NAV_LINKS_TS_PATH.is_file()
        else ""
    )
    if actual != content:
        print(
            f"{NAV_LINKS_TS_PATH} 与 nav.config 生成结果不一致。执行 --write 更新。",
            file=sys.stderr,
        )
        sys.exit(1)
    print("OK: navLinks.ts 与 spa/nav.config.json 一致")


if __name__ == "__main__":
    main()
