#!/usr/bin/env bash
# 将本仓库的 .githooks 设为 Git 钩子目录（仅影响当前 clone）。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
git config core.hooksPath .githooks
echo "已设置 core.hooksPath=.githooks（pre-commit：校验 manifest/候选 + analysis_engine --check）"
