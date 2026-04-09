#!/usr/bin/env bash
# 仅观测：RSS/法规页抓取 → evolution-candidates.json → 校验候选结构。
# 与 run_update_pipeline.sh 解耦：抓取依赖外网，分析仅依赖本地 JSON。
# 用法：bash scripts/run_ingest_only.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== [1/2] ingest_opinion_law（写入 assets/evolution-candidates.json）"
SUMMARY_ARGS=()
if [ "${WRITE_INGEST_SUMMARY:-}" = "1" ]; then
  SUMMARY_ARGS=(--write-summary)
fi
python3 scripts/ingest_opinion_law.py "${SUMMARY_ARGS[@]}" "$@"

echo "== [2/2] validate evolution-candidates"
python3 scripts/validate-evolution-candidates.py

echo "OK · 候选已更新；入库请人工审阅后: python3 scripts/merge_candidates_to_manifest.py <id>…"
