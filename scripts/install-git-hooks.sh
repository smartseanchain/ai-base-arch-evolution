#!/usr/bin/env bash
# 将本仓库的 .githooks 设为 Git 钩子目录（仅影响当前 clone）。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
git config core.hooksPath .githooks
echo "已设置 core.hooksPath=.githooks（pre-commit：bash scripts/run_validate.sh，与 make validate 一致；不跑 validate-fast；亦不跑 spa-build/spa-sync）"
echo "若改根 *.html 或 docs/ 且维护 SPA：请自行 make spa-sync（见 docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · make help）"
echo "参与贡献：根目录 CONTRIBUTING.md"
