#!/usr/bin/env python3
"""
校验 spa/src/navLinks.ts 是否由 spa/nav.config.json 生成且与 evolution-registry.json 页面集一致。
实现：evolution_pkg.spa_nav。纳入 run_validate.sh；无 spa/package.json 时跳过。
"""
from __future__ import annotations

import sys

from evolution_pkg.nav_links import nav_links_registry_check


def main() -> None:
    skipped, errs = nav_links_registry_check()
    if skipped:
        print("跳过: 无 spa/package.json（未启用 SPA 工程）")
        return
    if not errs:
        print("OK: nav.config items.page ≡ registry.pages · navLinks.ts 已与生成的内容一致")
        return
    for line in errs:
        print(line, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
