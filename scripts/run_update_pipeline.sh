#!/usr/bin/env bash
# 持续更新：校验 JSON → 分析引擎（含当日沉淀）→ 长期趋势汇总（不跑抓取）。
# 抓取单独：bash scripts/run_ingest_only.sh（见 scripts/README.md）
# 在项目根执行: bash scripts/run_update_pipeline.sh  或  make analyze
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== [1/6] validate evolution-manifest"
python3 scripts/validate-evolution-manifest.py

echo "== [2/6] validate evolution-candidates"
python3 scripts/validate-evolution-candidates.py

echo "== [2a/6] validate evolution-hint-decisions"
python3 scripts/validate_evolution_hint_decisions.py

echo "== [2b/6] check manifest / candidates vs pages + lab.js"
python3 scripts/check_manifest_drift.py

echo "== [2c/6] site nav vs partial"
python3 scripts/sync_site_nav.py --check

echo "== [2d/6] unit tests (scripts/tests)"
PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_*.py' -q

echo "== [3/6] analysis_engine --sediment"
python3 scripts/analysis_engine.py --sediment

echo "== [4/6] sediment_trends"
python3 scripts/sediment_trends.py

echo "== [5/6] committed analysis-snapshot contract"
python3 scripts/validate_analysis_snapshot_schema.py

echo "== [6/6] analysis_engine --check (与 validate 终态一致)"
python3 scripts/analysis_engine.py --check

echo "OK · 已更新 analysis-snapshot.json、data/sediment.json（当日）、assets/sediment-trends.json；并通过快照契约与 --check"
