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

from evolution_pkg.io import REGISTRY_JSON_PATH, REPO_ROOT, load_json

SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "evolution-registry.schema.json"


def main() -> None:
    if not REGISTRY_JSON_PATH.is_file():
        print(f"错误: 缺少 {REGISTRY_JSON_PATH}", file=sys.stderr)
        sys.exit(1)
    if not SCHEMA_PATH.is_file():
        print(f"错误: 缺少 Schema {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(1)
    try:
        doc = load_json(REGISTRY_JSON_PATH)
    except json.JSONDecodeError as e:
        print(f"错误: {REGISTRY_JSON_PATH} JSON 无效 — {e}", file=sys.stderr)
        sys.exit(1)
    if not doc:
        print(f"错误: {REGISTRY_JSON_PATH} 为空或不可解析", file=sys.stderr)
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
