"""
两份 ``analysis-snapshot.json`` 的结构化对比与 Markdown 摘要。

CLI 入口仍为 ``scripts/diff_analysis_snapshot.py``（git 取基线等留在脚本层）。
"""
from __future__ import annotations

import json
from typing import Any


def heat_top(rows: list[Any], kind: str, n: int = 8) -> list[tuple[str, float]]:
    """取 module_heat / factor_heat 等行表的前 n 条 (名称, 分数)。"""
    out: list[tuple[str, float]] = []
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        if kind == "module":
            name = row.get("page")
        else:
            name = row.get("factor")
        if name is None:
            continue
        raw = row.get("count", row.get("score", 0))
        try:
            score = float(raw)
        except (TypeError, ValueError):
            score = 0.0
        out.append((str(name), score))
    out.sort(key=lambda x: -x[1])
    return out[:n]


def diff_top(
    base_top: list[tuple[str, float]], head_top: list[tuple[str, float]], label: str
) -> list[str]:
    """对比两组 Top，生成 Markdown 行（最多 12 个键）。"""
    m0 = dict(base_top)
    m1 = dict(head_top)
    keys = sorted(set(m0) | set(m1), key=lambda k: -max(m0.get(k, 0), m1.get(k, 0)))
    lines: list[str] = []
    changed = False
    for k in keys[:12]:
        v0, v1 = m0.get(k), m1.get(k)
        if v0 != v1:
            changed = True
            a = "—" if v0 is None else v0
            b = "—" if v1 is None else v1
            lines.append(f"- **{k}**：{a} → {b}")
    if not changed:
        lines.append(f"- （{label} Top 无变化或仅序位微调）")
    return lines


def build_report(base: dict[str, Any], head: dict[str, Any]) -> str:
    """生成与历史 CLI 一致的 Markdown 差分摘要。"""
    br = base.get("run") or {}
    hr = head.get("run") or {}
    sb = base.get("sources") or {}
    sh = head.get("sources") or {}

    lines: list[str] = [
        "## analysis-snapshot 差分摘要",
        "",
        f"- **base** `run_id`: `{br.get('run_id', '—')}` · `repo_revision`: `{br.get('repo_revision', '—')}`",
        f"- **head** `run_id`: `{hr.get('run_id', '—')}` · `repo_revision`: `{hr.get('repo_revision', '—')}`",
        "",
        "### sources",
        f"- `combined_for_analysis`: {sb.get('combined_for_analysis')} → {sh.get('combined_for_analysis')}",
        f"- `manifest_signals`: {sb.get('manifest_signals')} → {sh.get('manifest_signals')}",
        f"- `candidate_signals`: {sb.get('candidate_signals')} → {sh.get('candidate_signals')}",
        "",
        "### 列表长度",
        f"- `evolution_hints`: {len(base.get('evolution_hints') or [])} → {len(head.get('evolution_hints') or [])}",
        f"- `hint_closure_gaps`: {len(base.get('hint_closure_gaps') or [])} → {len(head.get('hint_closure_gaps') or [])}",
        f"- `cooccurrence`: {len(base.get('cooccurrence') or [])} → {len(head.get('cooccurrence') or [])}",
        "",
        "### module_heat（score 变化摘取）",
        *diff_top(
            heat_top(base.get("module_heat") or [], "module"),
            heat_top(head.get("module_heat") or [], "module"),
            "module_heat",
        ),
        "",
        "### factor_heat（count 变化摘取）",
        *diff_top(
            heat_top(base.get("factor_heat") or [], "factor"),
            heat_top(head.get("factor_heat") or [], "factor"),
            "factor_heat",
        ),
        "",
    ]
    return "\n".join(lines)


def snapshot_diff_json(base: dict[str, Any], head: dict[str, Any]) -> dict[str, Any]:
    """``--json`` 模式输出的精简 dict（便于脚本与单测）。"""
    sb = base.get("sources") or {}
    sh = head.get("sources") or {}
    return {
        "base_run": base.get("run"),
        "head_run": head.get("run"),
        "combined_delta": (sh.get("combined_for_analysis") or 0)
        - (sb.get("combined_for_analysis") or 0),
        "hints_delta": len(head.get("evolution_hints") or [])
        - len(base.get("evolution_hints") or []),
        "gaps_delta": len(head.get("hint_closure_gaps") or [])
        - len(base.get("hint_closure_gaps") or []),
    }


def snapshot_diff_json_text(base: dict[str, Any], head: dict[str, Any]) -> str:
    """与历史 CLI 一致的 JSON 字符串（ensure_ascii=False, indent=2）。"""
    return json.dumps(snapshot_diff_json(base, head), ensure_ascii=False, indent=2)
