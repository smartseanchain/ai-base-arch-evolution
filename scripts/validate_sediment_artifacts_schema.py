#!/usr/bin/env python3
"""
校验已提交的 data/sediment.json、assets/sediment-trends.json 与 docs/schemas/ 下 Schema 一致。
任一文件不存在时跳过该文件（退出 0）；依赖 jsonschema（requirements.txt）。
实现：evolution_pkg.sediment_validate
"""
from __future__ import annotations

from evolution_pkg.sediment_validate import run_sediment_schema_cli


def main() -> None:
    run_sediment_schema_cli()


if __name__ == "__main__":
    main()
