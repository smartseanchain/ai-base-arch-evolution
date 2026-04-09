#!/usr/bin/env bash
# 持续更新：校验 JSON → 分析引擎（含当日沉淀）→ 长期趋势汇总（不跑抓取）。
# 抓取单独：bash scripts/run_ingest_only.sh（见 scripts/README.md）
# 在项目根执行: bash scripts/run_update_pipeline.sh  或  make analyze
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== [1/7] compileall scripts（与 make validate 对齐）"
python3 -m compileall -q scripts

echo "== [2/7] validate evolution-manifest"
python3 scripts/validate-evolution-manifest.py

echo "== [3/7] validate evolution-candidates"
python3 scripts/validate-evolution-candidates.py

echo "== [3a/7] validate evolution-hint-decisions"
python3 scripts/validate_evolution_hint_decisions.py

echo "== [3b/7] check manifest / candidates vs pages + lab.js"
python3 scripts/check_manifest_drift.py

echo "== [3c/7] site nav vs partial"
python3 scripts/sync_site_nav.py --check

echo "== [3d/7] unit tests (scripts/tests)"
PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_*.py' -q

echo "== [4/7] analysis_engine --sediment"
python3 scripts/analysis_engine.py --sediment

echo "== [5/7] sediment_trends"
python3 scripts/sediment_trends.py

echo "== [6/7] committed analysis-snapshot contract"
python3 scripts/validate_analysis_snapshot_schema.py

echo "== [7/7] analysis_engine --check (与 validate 终态一致)"
python3 scripts/analysis_engine.py --check

echo "OK · 已更新 analysis-snapshot.json、data/sediment.json（当日）、assets/sediment-trends.json；并通过快照契约与 --check"
