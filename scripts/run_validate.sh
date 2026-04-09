#!/usr/bin/env bash
# 全量校验：与 make validate、.githooks/pre-commit、CI validate job 共用（避免步骤漂移）。
# 在项目根由 Makefile / 钩子调用；勿在子 shell 中改目录后调用。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! python3 -c "import jsonschema" 2>/dev/null; then
  echo "缺少 jsonschema。请执行: python3 -m pip install -r requirements.txt" >&2
  exit 1
fi

python3 -m compileall -q scripts
python3 scripts/validate-evolution-manifest.py
python3 scripts/validate-evolution-candidates.py
python3 scripts/validate_evolution_hint_decisions.py
python3 scripts/check_manifest_drift.py
python3 scripts/sync_site_nav.py --check
PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_*.py' -q
python3 scripts/analysis_engine.py --check
python3 scripts/validate_analysis_snapshot_schema.py
