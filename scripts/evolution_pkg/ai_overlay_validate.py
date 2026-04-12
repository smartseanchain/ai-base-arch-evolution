"""assets/ai-analysis-overlay.json 与 JSON Schema 对齐；可选与 analysis-snapshot run_id 对账。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from evolution_pkg.io import REPO_ROOT

OVERLAY = REPO_ROOT / "assets" / "ai-analysis-overlay.json"
SNAPSHOT = REPO_ROOT / "assets" / "analysis-snapshot.json"
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "ai-analysis-overlay.schema.json"


def overlay_schema_violations() -> list[str]:
    """无违规返回 []；缺 overlay 文件不报错；缺 Schema 或 JSON/校验/对账失败则收集说明。"""
    errors: list[str] = []
    if not OVERLAY.is_file():
        return errors
    if not SCHEMA_PATH.is_file():
        return [f"缺少 Schema {SCHEMA_PATH}（校验 ai-analysis-overlay）"]
    try:
        doc = json.loads(OVERLAY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{OVERLAY} JSON 无效 — {e}"]
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{SCHEMA_PATH} Schema JSON 无效 — {e}"]
    validator = Draft202012Validator(schema)
    try:
        validator.validate(doc)
    except ValidationError as e:
        return [f"{OVERLAY} 不符合 Schema — {e.message}"]

    rid = doc.get("source_run_id") if isinstance(doc, dict) else None
    if not SNAPSHOT.is_file():
        return errors
    try:
        snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return errors
    run = snap.get("run") if isinstance(snap, dict) else None
    snap_rid = (run or {}).get("run_id") if isinstance(run, dict) else None
    if snap_rid is not None and rid != snap_rid:
        errors.append(
            f"{OVERLAY.name} 的 source_run_id={rid!r} 与 "
            f"analysis-snapshot.json run.run_id={snap_rid!r} 不一致"
        )
    return errors


def run_ai_overlay_schema_cli() -> None:
    errs = overlay_schema_violations()
    if errs:
        for line in errs:
            print(line, file=sys.stderr)
        sys.exit(1)
    if OVERLAY.is_file():
        tail = (
            " · 已与 analysis-snapshot run_id 对账"
            if SNAPSHOT.is_file()
            else " · 未找到 analysis-snapshot，跳过 run_id 对账"
        )
        print(f"OK: assets/ai-analysis-overlay.json · schema 校验通过{tail}")
    else:
        print(f"跳过: 无 {OVERLAY}（可选；见 docs/AI_ASSISTED_ANALYSIS_LAYER.md）")
