#!/usr/bin/env python3
"""
校验已提交的 assets/analysis-snapshot.json 顶层契约（与 analysis_engine --check 对齐）。
无文件时退出 0（冷启动仓库）；用于 make validate 防止快照与展示端脱节。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "analysis-snapshot.json"

TOP_KEYS = frozenset(
    {
        "schema_version",
        "generated_at",
        "run",
        "sources",
        "module_heat",
        "factor_heat",
        "kind_distribution",
        "cooccurrence",
        "evolution_hints",
        "hint_closure_gaps",
    }
)


def main() -> None:
    if not OUT.is_file():
        print(f"跳过: 无 {OUT}（可执行 make analyze 生成）")
        return
    try:
        doc = json.loads(OUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: {OUT} JSON 无效 — {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(doc, dict):
        print("错误: 快照根须为对象", file=sys.stderr)
        sys.exit(1)
    if doc.get("schema_version") != 1:
        print("错误: schema_version 须为 1", file=sys.stderr)
        sys.exit(1)
    missing = TOP_KEYS - frozenset(doc.keys())
    if missing:
        print(f"错误: 缺顶层字段 {sorted(missing)}", file=sys.stderr)
        sys.exit(1)
    run = doc.get("run")
    if not isinstance(run, dict):
        print("错误: run 须为对象", file=sys.stderr)
        sys.exit(1)
    rid = run.get("run_id")
    rev = run.get("repo_revision")
    if not isinstance(rid, str) or not rid.strip():
        print("错误: run.run_id 须为非空字符串", file=sys.stderr)
        sys.exit(1)
    if not isinstance(rev, str) or not rev.strip():
        print("错误: run.repo_revision 须为非空字符串", file=sys.stderr)
        sys.exit(1)
    src = doc.get("sources")
    if not isinstance(src, dict) or "combined_for_analysis" not in src:
        print("错误: sources 结构异常", file=sys.stderr)
        sys.exit(1)
    print(f"OK: analysis-snapshot · run_id={rid} · repo_revision={rev}")


if __name__ == "__main__":
    main()
