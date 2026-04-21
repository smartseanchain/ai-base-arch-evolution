"""artifacts/ai-overlay-step.json 与 JSON Schema 对齐（可选文件）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from evolution_pkg.io import REPO_ROOT

STEP_JSON = REPO_ROOT / "artifacts" / "ai-overlay-step.json"
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "ai-overlay-step.schema.json"


def overlay_step_schema_violations() -> list[str]:
    """无违规返回 []；缺侧车文件不报错。"""
    errors: list[str] = []
    if not STEP_JSON.is_file():
        return errors
    if not SCHEMA_PATH.is_file():
        return [f"缺少 Schema {SCHEMA_PATH}（校验 ai-overlay-step）"]
    try:
        doc = json.loads(STEP_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{STEP_JSON} JSON 无效 — {e}"]
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{SCHEMA_PATH} Schema JSON 无效 — {e}"]
    validator = Draft202012Validator(schema)
    try:
        validator.validate(doc)
    except ValidationError as e:
        return [f"{STEP_JSON} 不符合 Schema — {e.message}"]
    return errors


def run_ai_overlay_step_schema_cli() -> None:
    errs = overlay_step_schema_violations()
    if errs:
        for line in errs:
            print(line, file=sys.stderr)
        sys.exit(1)
    if STEP_JSON.is_file():
        print(f"OK: {STEP_JSON.relative_to(REPO_ROOT)} · schema 校验通过")
    else:
        print(f"跳过: 无 {STEP_JSON}（可选；见 docs/DATA_CONTRACTS.md#pipeline-telemetry）")
