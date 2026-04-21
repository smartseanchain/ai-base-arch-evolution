#!/usr/bin/env python3
"""
写入 assets/ai-analysis-overlay.json 占位文件（provider.kind=stub），便于联调 Schema 与前台。
不调用外部 LLM。须已有 assets/analysis-snapshot.json。

用法: python3 scripts/write_ai_analysis_overlay_stub.py
（实现已并入 evolution_pkg.ai_overlay_write；本入口保持向后兼容。）
"""
from __future__ import annotations

from evolution_pkg.ai_overlay_write import write_stub_overlay


def main() -> int:
    return write_stub_overlay()


if __name__ == "__main__":
    raise SystemExit(main())
