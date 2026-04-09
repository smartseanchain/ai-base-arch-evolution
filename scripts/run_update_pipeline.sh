#!/usr/bin/env bash
# 持续更新：校验 JSON → 分析引擎（含当日沉淀）→ 长期趋势汇总（不跑抓取）。
# 抓取单独：bash scripts/run_ingest_only.sh（见 scripts/README.md）
# 在项目根执行: bash scripts/run_update_pipeline.sh  或  make analyze
# 步骤由 Python 编排，结束时写入 artifacts/pipeline-metrics-*.json（SKIP_PIPELINE_TELEMETRY=1 可关闭）。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec python3 scripts/run_pipeline_steps.py analyze
