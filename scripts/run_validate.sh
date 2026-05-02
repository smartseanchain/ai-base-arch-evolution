#!/usr/bin/env bash
# 全量校验：与 make validate、.githooks/pre-commit、CI validate job 共用（避免步骤漂移）。
# make analyze 前置段见 evolution_pkg.pipeline.runner（至单测）；不含本脚本后半的 check_skip_bar_404 等，合并仍以本脚本为准。
# 含：evolution-registry Schema、navLinks↔nav.config、sediment/sediment-trends Schema、可选 ai-overlay-step / ai-analysis-overlay Schema 等。
# make test 仅覆盖其中子集（registry Schema + 单测 + navLinks + 沉淀/趋势 Schema），合并前仍以本脚本为准。
# CI validate job 另装 requirements-api.txt，使 test_readonly*.py 必跑；本地未装 fastapi 时该类 skip，可用 make test-readonly-api 对齐。
# 改编排器 / broker / 生产库时：见 docs/PHASED_UPGRADE_EXECUTION_GUIDE.md；新增检查须并入本脚本（或经评审的显式子步骤），勿另立「第二套合并真源」。
# 本脚本不跑 spa-sync：改根 *.html 或 docs/ 且维护 SPA 时须 make spa-sync（或 make spa-build）；docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · make help（CONTRIBUTING.md#contributing-five-minute · #contributing-pr-evidence-triad · #contributing-change-to-command）
# 在项目根由 Makefile / 钩子调用；勿在子 shell 中改目录后调用。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! python3 -c "import jsonschema" 2>/dev/null; then
  echo "缺少 jsonschema。请执行: python3 -m pip install -r requirements.txt" >&2
  exit 1
fi

python3 -m compileall -q scripts
if [[ -d admin-console/app ]]; then
  python3 -m compileall -q admin-console/app
fi
python3 scripts/validate-evolution-manifest.py
python3 scripts/validate-evolution-candidates.py
python3 scripts/validate_evolution_hint_decisions.py
python3 scripts/validate_evolution_registry_schema.py
python3 scripts/check_manifest_drift.py
python3 scripts/check_nav_links_registry.py
python3 scripts/sync_site_nav.py --check
python3 scripts/check_skip_bar_404.py
PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_*.py' -q
PYTHONPATH=scripts python3 scripts/validate_golden_mapping.py --dir fixtures/ai_mapping_golden
python3 scripts/analysis_engine.py --check
python3 scripts/validate_analysis_snapshot_schema.py
python3 scripts/validate_sediment_artifacts_schema.py
python3 scripts/validate_pipeline_metrics_schema.py
python3 scripts/validate_ai_overlay_step_schema.py
python3 scripts/validate_ai_analysis_overlay_schema.py
