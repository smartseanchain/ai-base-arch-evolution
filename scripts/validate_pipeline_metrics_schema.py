#!/usr/bin/env python3
"""
校验流水线遥测 JSON 与 docs/schemas/pipeline-metrics.schema.json 一致。

- 始终校验仓库内 **fixtures/pipeline_metrics_example.json**（契约样例）。
- 若存在 **artifacts/pipeline-metrics-*.json**（本地跑 analyze / evolution-fast 生成），一并校验。
  默认 CI 工作区无该文件则仅校验 fixture。依赖 jsonschema（requirements.txt）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "pipeline-metrics.schema.json"
FIXTURE_PATH = REPO_ROOT / "fixtures" / "pipeline_metrics_example.json"
ARTIFACTS_DIR = REPO_ROOT / "artifacts"


def _validate_one(
    validator: Draft202012Validator, path: Path, label: str
) -> list[str]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    errs = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    if not errs:
        return []
    lines = [f"{label}: {path}"]
    for e in errs[:12]:
        loc = "/".join(str(x) for x in e.path) or "(root)"
        lines.append(f"  · {loc}: {e.message}")
    if len(errs) > 12:
        lines.append(f"  … 另有 {len(errs) - 12} 条")
    return lines


def main() -> int:
    if not SCHEMA_PATH.is_file():
        print(f"错误: 缺少 {SCHEMA_PATH}", file=sys.stderr)
        return 1
    if not FIXTURE_PATH.is_file():
        print(f"跳过: 无 fixture {FIXTURE_PATH}", file=sys.stderr)
        return 0
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    all_errs: list[str] = []
    all_errs.extend(_validate_one(validator, FIXTURE_PATH, "fixture"))
    skipped_legacy: list[str] = []
    if ARTIFACTS_DIR.is_dir():
        for p in sorted(ARTIFACTS_DIR.glob("pipeline-metrics-*.json")):
            doc = json.loads(p.read_text(encoding="utf-8"))
            if "input_artifacts" not in doc or "otel_semantics" not in doc:
                skipped_legacy.append(p.name)
                continue
            all_errs.extend(_validate_one(validator, p, "artifact"))
    if skipped_legacy:
        print(
            "警告: 跳过旧格式遥测（无 input_artifacts/otel_semantics）: "
            + ", ".join(skipped_legacy)
            + " — 可先 make clean-pipeline-metrics-dry-run，再 make clean-pipeline-metrics，"
            "重跑 make analyze（见 docs/EVOLUTION_RUNBOOK.md#accelerate）",
            file=sys.stderr,
        )
    if all_errs:
        print("\n".join(all_errs), file=sys.stderr)
        return 1
    extra = ""
    if ARTIFACTS_DIR.is_dir():
        n = len(list(ARTIFACTS_DIR.glob("pipeline-metrics-*.json")))
        if n:
            extra = f" · artifacts 内 {n} 份遥测"
    print(f"OK: pipeline-metrics · fixture + Schema{extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
