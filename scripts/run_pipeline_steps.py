#!/usr/bin/env python3
"""
编排 make analyze / evolution-fast（实现位于 evolution_pkg.pipeline.runner）。
用法:
  python3 scripts/run_pipeline_steps.py analyze
  python3 scripts/run_pipeline_steps.py fast
环境:
  SKIP_PIPELINE_TELEMETRY=1  — 不写 artifacts/pipeline-metrics-*.json

合并闸门仍以 make validate / run_validate.sh 为准；不含 spa-sync。
对表: docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · make help（CONTRIBUTING.md#contributing-five-minute · #contributing-pr-evidence-triad · #contributing-change-to-command）
"""
from __future__ import annotations

from evolution_pkg.pipeline.runner import main

if __name__ == "__main__":
    raise SystemExit(main())
