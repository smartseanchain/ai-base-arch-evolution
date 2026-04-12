#!/usr/bin/env python3
"""
校验 scripts/evolution-registry.json 与 docs/schemas/evolution-registry.schema.json 一致。
依赖 jsonschema（requirements.txt）。须在对账脚本之前通过结构闸门。
"""
from __future__ import annotations

import json
import sys

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from evolution_pkg.io import REPO_ROOT

REGISTRY = REPO_ROOT / "scripts" / "evolution-registry.json"
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "evolution-registry.schema.json"


def main() -> None:
    if not REGISTRY.is_file():
        print(f"错误: 缺少 {REGISTRY}", file=sys.stderr)
        sys.exit(1)
    if not SCHEMA_PATH.is_file():
        print(f"错误: 缺少 Schema {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(1)
    try:
        doc = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: {REGISTRY} JSON 无效 — {e}", file=sys.stderr)
        sys.exit(1)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    try:
        validator.validate(doc)
    except ValidationError as e:
        print(f"错误: evolution-registry 不符合 Schema — {e.message}", file=sys.stderr)
        sys.exit(1)
    np = len(doc.get("pages") or [])
    nf = len(doc.get("lab_factors") or [])
    print(f"OK: evolution-registry.json · pages={np} · lab_factors={nf}")


if __name__ == "__main__":
    main()
