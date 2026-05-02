#!/usr/bin/env bash
# 轻量校验：迭代 manifest/候选/分析时减少等待；**不等价**于 ``make validate`` / pre-commit / CI。
# 与全量 validate 同源：`compileall` 含 ``scripts`` 与 ``admin-console/app``（若存在）。
# 省略：hint_decisions、对账 drift、顶栏 partial 对齐、404 skip-bar、黄金集映射、沉淀 Schema 等。
# 已含（与全量 validate 同源）：**`validate_ai_overlay_step_schema`**、**`validate_ai_analysis_overlay_schema`**（无对应文件则跳过）。
# 合并 PR 前仍须：``make validate``（见 CONTRIBUTING.md · docs/README.md#quick-paths）。
# 不含 spa-sync：改根 HTML/docs 维护 SPA 见 docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · make help（CONTRIBUTING.md#contributing-five-minute · #contributing-pr-evidence-triad · #contributing-change-to-command）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! python3 -c "import jsonschema" 2>/dev/null; then
  echo "缺少 jsonschema。请执行: python3 -m pip install -r requirements.txt" >&2
  exit 1
fi

python3 -m compileall -q scripts
if [ -d admin-console/app ]; then
  python3 -m compileall -q admin-console/app
fi
python3 scripts/validate-evolution-manifest.py
python3 scripts/validate-evolution-candidates.py
python3 scripts/validate_evolution_registry_schema.py
python3 scripts/check_nav_links_registry.py
PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_*.py' -q
python3 scripts/analysis_engine.py --check
python3 scripts/validate_analysis_snapshot_schema.py
# 与 run_validate.sh 同源：若 artifacts 含旧格式 pipeline-metrics，stderr 会提示 make clean-pipeline-metrics-dry-run 等（见 validate_pipeline_metrics_schema.py）。
python3 scripts/validate_pipeline_metrics_schema.py
python3 scripts/validate_ai_overlay_step_schema.py
python3 scripts/validate_ai_analysis_overlay_schema.py

echo "OK: validate-fast（非全量闸门；合并前请 make validate）" >&2
