#!/usr/bin/env python3
"""
校验已提交的 assets/ai-analysis-overlay.json 与 docs/schemas/ai-analysis-overlay.schema.json 一致；
若存在 assets/analysis-snapshot.json，则校验 source_run_id 与其 run.run_id 一致。
无 overlay 文件时退出 0。依赖 jsonschema（requirements.txt）。
实现：evolution_pkg.ai_overlay_validate
"""
from __future__ import annotations

from evolution_pkg.ai_overlay_validate import run_ai_overlay_schema_cli


def main() -> None:
    run_ai_overlay_schema_cli()


if __name__ == "__main__":
    main()
