#!/usr/bin/env bash
# 将本仓库的 .githooks 设为 Git 钩子目录（仅影响当前 clone）。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
git config core.hooksPath .githooks
echo "已设置 core.hooksPath=.githooks（pre-commit：bash scripts/run_validate.sh，与 make validate 一致；参与贡献见根目录 CONTRIBUTING.md）"
