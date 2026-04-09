#!/usr/bin/env bash
# 仅写回分析产出（快照 + 当日沉淀 + 趋势 + 快照契约 + --check）。
# 前提：manifest/候选/漂移/单测等已通过 make validate；否则请用 make analyze。
# 用法: bash scripts/run_analyze_write.sh  或  make evolution-fast
# 遥测：artifacts/pipeline-metrics-*.json（SKIP_PIPELINE_TELEMETRY=1 可关闭）。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec python3 scripts/run_pipeline_steps.py fast
