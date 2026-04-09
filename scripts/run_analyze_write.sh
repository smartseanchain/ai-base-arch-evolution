#!/usr/bin/env bash
# 仅写回分析产出（快照 + 当日沉淀 + 趋势 + 快照契约 + --check）。
# 前提：manifest/候选/漂移/单测等已通过 make validate；否则请用 make analyze。
# 用法: bash scripts/run_analyze_write.sh  或  make evolution-fast
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== [1/4] analysis_engine --sediment"
python3 scripts/analysis_engine.py --sediment

echo "== [2/4] sediment_trends"
python3 scripts/sediment_trends.py

echo "== [3/4] committed analysis-snapshot contract"
python3 scripts/validate_analysis_snapshot_schema.py

echo "== [4/4] analysis_engine --check"
python3 scripts/analysis_engine.py --check

echo "OK · 已更新 analysis-snapshot.json、data/sediment.json、assets/sediment-trends.json（未重跑 manifest/单测校验）"
