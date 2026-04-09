#!/usr/bin/env python3
"""
编排 make analyze / evolution-fast（实现位于 evolution_pkg.pipeline.runner）。
用法:
  python3 scripts/run_pipeline_steps.py analyze
  python3 scripts/run_pipeline_steps.py fast
环境:
  SKIP_PIPELINE_TELEMETRY=1  — 不写 artifacts/pipeline-metrics-*.json
"""
from __future__ import annotations

from evolution_pkg.pipeline.runner import main

if __name__ == "__main__":
    raise SystemExit(main())
