#!/usr/bin/env python3
"""
写入 assets/ai-analysis-overlay.json：默认跳过（不写盘）；--stub 写占位；
AI_OVERLAY_ENABLE=1 且配置 API 时可选调用 OpenAI 兼容接口（见 docs/AI_ASSISTED_ANALYSIS_LAYER.md）。
"""
from __future__ import annotations

import sys

from evolution_pkg.ai_overlay_write import run_write_overlay_main


if __name__ == "__main__":
    raise SystemExit(run_write_overlay_main())
