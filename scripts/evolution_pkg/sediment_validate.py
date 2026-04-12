"""data/sediment.json、assets/sediment-trends.json 与 JSON Schema 对齐（供 validate_sediment_artifacts_schema.py 与单测复用）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from evolution_pkg.io import REPO_ROOT

SEDIMENT = REPO_ROOT / "data" / "sediment.json"
TRENDS = REPO_ROOT / "assets" / "sediment-trends.json"
SCHEMA_SEDIMENT = REPO_ROOT / "docs" / "schemas" / "sediment.schema.json"
SCHEMA_TRENDS = REPO_ROOT / "docs" / "schemas" / "sediment-trends.schema.json"

_PAIR: tuple[Path, Path, str] = (
    (SEDIMENT, SCHEMA_SEDIMENT, "data/sediment.json"),
    (TRENDS, SCHEMA_TRENDS, "assets/sediment-trends.json"),
)


def sediment_schema_violations() -> list[str]:
    """无违规返回 []；缺实例文件不报错；缺 Schema 或 JSON/校验失败则收集错误说明。"""
    errors: list[str] = []
    for path, schema_path, label in _PAIR:
        if not path.is_file():
            continue
        if not schema_path.is_file():
            errors.append(f"缺少 Schema {schema_path}（校验 {label}）")
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{path} JSON 无效 — {e}")
            continue
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{schema_path} Schema JSON 无效 — {e}")
            continue
        validator = Draft202012Validator(schema)
        try:
            validator.validate(doc)
        except ValidationError as e:
            errors.append(f"{path} 不符合 Schema — {e.message}")
    return errors


def run_sediment_schema_cli() -> None:
    """打印跳过/OK/错误并设置退出码（与原 validate_sediment_artifacts_schema 行为一致）。"""
    errs = sediment_schema_violations()
    if errs:
        for line in errs:
            print(line, file=sys.stderr)
        sys.exit(1)
    for path, _schema, label in _PAIR:
        if path.is_file():
            print(f"OK: {label} · schema 校验通过")
        else:
            print(f"跳过: 无 {path}（{label}）")

