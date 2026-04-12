"""
分析快照在 ``analysis_engine --check`` 下的结构校验（与 jsonschema 闸门互补的轻量断言）。

失败时 ``sys.exit(1)`` 并写 stderr；成功时由调用方打印 OK 行。
"""
from __future__ import annotations

import sys
from typing import Any


def expected_snapshot_keys() -> frozenset[str]:
    return frozenset(
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


def validate_hint_closure_gaps(entries: list[Any]) -> None:
    if not isinstance(entries, list):
        print("错误: hint_closure_gaps 须为数组", file=sys.stderr)
        sys.exit(1)
    for i, g in enumerate(entries):
        if not isinstance(g, dict) or not isinstance(g.get("rule_id"), str):
            print(
                f"错误: hint_closure_gaps[{i}] 须为含 rule_id 字符串的对象",
                file=sys.stderr,
            )
            sys.exit(1)
        if "text" in g and not isinstance(g.get("text"), str):
            print(
                f"错误: hint_closure_gaps[{i}].text 须为字符串",
                file=sys.stderr,
            )
            sys.exit(1)


def validate_evolution_hints(entries: list[Any]) -> None:
    for i, h in enumerate(entries):
        if isinstance(h, str):
            continue
        if isinstance(h, dict) and isinstance(h.get("text"), str):
            continue
        print(
            f"错误: evolution_hints[{i}] 须为字符串或含 text 字段的对象",
            file=sys.stderr,
        )
        sys.exit(1)


def validate_analysis_output_for_check(out: dict[str, Any]) -> dict[str, Any]:
    """校验 ``--check`` 路径上的内存快照对象；成功返回 ``sources`` 供打印统计。"""
    missing = expected_snapshot_keys() - frozenset(out.keys())
    if missing:
        print(f"错误: 分析输出缺字段: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)
    validate_evolution_hints(out.get("evolution_hints") or [])
    validate_hint_closure_gaps(out.get("hint_closure_gaps") or [])
    src = out["sources"]
    if not isinstance(src, dict) or "combined_for_analysis" not in src:
        print("错误: sources 结构异常", file=sys.stderr)
        sys.exit(1)
    br = src.get("candidate_review_breakdown")
    if not isinstance(br, dict) or not all(
        k in br for k in ("pending", "noise", "queued_for_manifest")
    ):
        print("错误: sources.candidate_review_breakdown 结构异常", file=sys.stderr)
        sys.exit(1)
    hd = src.get("hint_decisions")
    if not isinstance(hd, dict) or "total" not in hd:
        print("错误: sources.hint_decisions 结构异常", file=sys.stderr)
        sys.exit(1)
    ba = hd.get("by_action")
    if not isinstance(ba, dict) or not all(
        k in ba for k in ("done", "rejected", "deferred")
    ):
        print("错误: sources.hint_decisions.by_action 结构异常", file=sys.stderr)
        sys.exit(1)
    run = out.get("run")
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
    return src
