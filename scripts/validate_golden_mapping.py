#!/usr/bin/env python3
"""
规则层：黄金集中每条用例的标题+摘要拼接文本，经 ingest_config.routes 与 maps_to_hints 合并后，
应满足 expect.lab_factors_contains / expect.pages_contains（子集约束）。

不调用网络与 LLM；与 **evolution_pkg.ingest_maps**（**`apply_routes`** / **`merge_maps_to_hints`**）行为一致。
expect 中出现的页面与 lab_factors 须为 **scripts/evolution-registry.json** 已登记项，防止夹具与注册表漂移。

用法:
  python3 scripts/validate_golden_mapping.py
  python3 scripts/validate_golden_mapping.py --file fixtures/ai_mapping_golden/example_case.json
  python3 scripts/validate_golden_mapping.py --dir fixtures/ai_mapping_golden
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

from evolution_pkg.io import (
    INGEST_CONFIG_JSON_PATH,
    REPO_ROOT,
    load_registry_allowed_sets,
)
from evolution_pkg.ingest_maps import apply_routes, load_maps_to_hints, merge_maps_to_hints

DEFAULT_GOLDEN = REPO_ROOT / "fixtures" / "ai_mapping_golden" / "example_case.json"
CONFIG_PATH = INGEST_CONFIG_JSON_PATH
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "ai-mapping-golden.schema.json"


def _validate_doc_against_schema(doc: dict, path: Path) -> None:
    if not SCHEMA_PATH.is_file():
        return
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(doc, schema)
    except jsonschema.ValidationError as e:
        print(f"错误: {path} 不符合 Schema（{SCHEMA_PATH.name}）: {e.message}", file=sys.stderr)
        sys.exit(1)


def _load_config_routes() -> list[dict]:
    if not CONFIG_PATH.is_file():
        print(f"错误: 缺少 {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return list(cfg.get("routes") or [])


def _expect_in_registry(
    cid: str,
    exp: dict,
    reg_pages: frozenset[str],
    reg_factors: frozenset[str],
) -> tuple[bool, str]:
    for f in exp.get("lab_factors_contains") or []:
        if f not in reg_factors:
            return (
                False,
                f"{cid}: expect 中 lab_factor {f!r} 不在 evolution-registry.json · lab_factors",
            )
    for p in exp.get("pages_contains") or []:
        if p not in reg_pages:
            return (
                False,
                f"{cid}: expect 中页面 {p!r} 不在 evolution-registry.json · pages",
            )
    return True, ""


def _evaluate_case(
    case: dict,
    routes: list[dict],
    hints_cfg: dict,
    reg_pages: frozenset[str],
    reg_factors: frozenset[str],
) -> tuple[bool, str]:
    cid = case.get("id") or "?"
    inp = case.get("input")
    if not isinstance(inp, dict):
        return False, f"{cid}: 缺少 input 对象"
    title = str(inp.get("title") or "")
    summary = str(inp.get("summary_snippet") or "")
    link = str(inp.get("link") or "").strip()
    if not title.strip():
        return False, f"{cid}: input.title 为空"
    blob = f"{title} {summary}".strip()
    lab, pages = apply_routes(blob, routes)
    lab, pages = merge_maps_to_hints(link, title, summary, lab, pages, hints_cfg)
    exp = case.get("expect")
    if not isinstance(exp, dict):
        return False, f"{cid}: 缺少 expect 对象"
    ok_reg, reg_msg = _expect_in_registry(cid, exp, reg_pages, reg_factors)
    if not ok_reg:
        return False, reg_msg
    for f in exp.get("lab_factors_contains") or []:
        if f not in lab:
            return (
                False,
                f"{cid}: 期望因子 {f!r} 未命中；实际 lab_factors={lab!r}",
            )
    for p in exp.get("pages_contains") or []:
        if p not in pages:
            return (
                False,
                f"{cid}: 期望页面 {p!r} 未命中；实际 pages={pages!r}",
            )
    return True, cid


def _validate_one_json_file(
    path: Path,
    routes: list[dict],
    hints_cfg: dict,
    reg_pages: frozenset[str],
    reg_factors: frozenset[str],
) -> tuple[int, int]:
    """处理单个黄金集文件。返回 (失败条数, 用例条数)。"""
    doc = json.loads(path.read_text(encoding="utf-8"))
    _validate_doc_against_schema(doc, path)
    cases = doc.get("cases")
    if not isinstance(cases, list) or not cases:
        print(f"错误: {path} 缺少非空 cases 数组", file=sys.stderr)
        return 1, 0
    failed = 0
    for case in cases:
        if not isinstance(case, dict):
            failed += 1
            print("错误: cases 中存在非对象项", file=sys.stderr)
            continue
        ok, msg = _evaluate_case(case, routes, hints_cfg, reg_pages, reg_factors)
        if not ok:
            failed += 1
            print(f"错误: {msg}", file=sys.stderr)
    if failed == 0:
        print(f"OK: 黄金集 {len(cases)} 条规则映射 · {path}")
    return failed, len(cases)


def _resolve_dir(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "--file",
        type=Path,
        default=None,
        help="单个黄金集 JSON（与 --dir 二选一；皆省略时默认 example_case.json）",
    )
    ap.add_argument(
        "--dir",
        type=Path,
        default=None,
        help="目录内全部 *.json 逐个校验（与 --file 二选一）",
    )
    args = ap.parse_args()
    if args.file is not None and args.dir is not None:
        print("错误: 不可同时使用 --file 与 --dir", file=sys.stderr)
        return 1
    routes = _load_config_routes()
    hints = load_maps_to_hints()
    try:
        reg_pages, reg_factors = load_registry_allowed_sets()
    except (FileNotFoundError, ValueError) as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

    if args.dir is not None:
        target_dir = _resolve_dir(args.dir)
        if not target_dir.is_dir():
            print(f"错误: 不是目录 {target_dir}", file=sys.stderr)
            return 1
        json_files = sorted(target_dir.glob("*.json"))
        if not json_files:
            print(f"错误: {target_dir} 下无 *.json", file=sys.stderr)
            return 1
        total_failed = 0
        total_cases = 0
        for jf in json_files:
            f, n = _validate_one_json_file(jf, routes, hints, reg_pages, reg_factors)
            total_failed += f
            total_cases += n
        if total_failed:
            return 1
        print(
            f"OK: 黄金集目录 {len(json_files)} 个文件 · 共 {total_cases} 条规则映射 · {target_dir}"
        )
        return 0

    path = args.file if args.file is not None else DEFAULT_GOLDEN
    if not path.is_file():
        print(f"跳过: 未找到 {path}（可选检查）", file=sys.stderr)
        return 0
    failed, _ = _validate_one_json_file(path, routes, hints, reg_pages, reg_factors)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
