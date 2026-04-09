#!/usr/bin/env bash
# 持续更新：校验 JSON → 分析引擎（含当日沉淀）→ 长期趋势汇总（不跑抓取）。
# 抓取单独：bash scripts/run_ingest_only.sh（见 scripts/README.md）
# 在项目根执行: bash scripts/run_update_pipeline.sh  或  make analyze
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== [1/4] validate evolution-manifest"
python3 scripts/validate-evolution-manifest.py

echo "== [2/4] validate evolution-candidates"
python3 scripts/validate-evolution-candidates.py

echo "== [2a/4] validate evolution-hint-decisions"
python3 scripts/validate_evolution_hint_decisions.py

echo "== [2b/4] check manifest / candidates vs pages + lab.js"
python3 scripts/check_manifest_drift.py

echo "== [3/4] analysis_engine --sediment"
python3 scripts/analysis_engine.py --sediment

echo "== [4/4] sediment_trends"
python3 scripts/sediment_trends.py

echo "OK · 已更新 analysis-snapshot.json、data/sediment.json（当日）、assets/sediment-trends.json"
