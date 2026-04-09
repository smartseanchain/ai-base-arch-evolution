#!/usr/bin/env python3
"""
校验已提交的 assets/analysis-snapshot.json 与 docs/schemas/analysis-snapshot.schema.json 一致。
无快照文件时退出 0；依赖 jsonschema（见 requirements.txt）。
"""
from __future__ import annotations

import json
import sys

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from evolution_io import REPO_ROOT

OUT = REPO_ROOT / "assets" / "analysis-snapshot.json"
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "analysis-snapshot.schema.json"


def main() -> None:
    if not OUT.is_file():
        print(f"跳过: 无 {OUT}（可执行 make analyze 生成）")
        return
    if not SCHEMA_PATH.is_file():
        print(f"错误: 缺少 Schema {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(1)
    try:
        doc = json.loads(OUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: {OUT} JSON 无效 — {e}", file=sys.stderr)
        sys.exit(1)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    try:
        validator.validate(doc)
    except ValidationError as e:
        print(f"错误: 快照不符合 Schema — {e.message}", file=sys.stderr)
        sys.exit(1)
    run = doc.get("run") if isinstance(doc, dict) else None
    rid = (run or {}).get("run_id")
    rev = (run or {}).get("repo_revision")
    print(f"OK: analysis-snapshot · run_id={rid} · repo_revision={rev}")


if __name__ == "__main__":
    main()
