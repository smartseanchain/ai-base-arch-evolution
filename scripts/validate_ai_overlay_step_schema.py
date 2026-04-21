#!/usr/bin/env python3
"""
校验 artifacts/ai-overlay-step.json 与 docs/schemas/ai-overlay-step.schema.json 一致。
无侧车文件时退出 0。依赖 jsonschema（requirements.txt）。
实现：evolution_pkg.ai_overlay_step_validate
"""
from __future__ import annotations

from evolution_pkg.ai_overlay_step_validate import run_ai_overlay_step_schema_cli


def main() -> None:
    run_ai_overlay_step_schema_cli()


if __name__ == "__main__":
    main()
