#!/usr/bin/env python3
"""
将 **analysis-snapshot**、可选 **sediment-trends** 与 **sediment** 最新条目
汇总为一段 **Markdown**，便于维护者扫读、贴 PR 或存档（无 LLM、不访问外网）。

与 **diff_analysis_snapshot.py**（两份快照 diff）互补：本脚本侧重「当前截面 + 趋势上下文」。

用法（仓库根）:
  python3 scripts/evolution_intelligence_digest.py
  make digest
"""
from __future__ import annotations

import argparse
import sys
from typing import Any

from evolution_pkg.io import REPO_ROOT, load_json

SNAPSHOT_PATH = REPO_ROOT / "assets" / "analysis-snapshot.json"
TRENDS_PATH = REPO_ROOT / "assets" / "sediment-trends.json"
SEDIMENT_PATH = REPO_ROOT / "data" / "sediment.json"


def _heat_lines(rows: list[Any], key: str, label: str, n: int = 6) -> list[str]:
    out: list[str] = []
    for row in (rows or [])[:n]:
        if not isinstance(row, dict):
            continue
        name = row.get(key)
        if name is None:
            continue
        cnt = row.get("count", row.get("score", "—"))
        out.append(f"| `{name}` | {cnt} |")
    if not out:
        return [f"_（无 {label} 数据）_", ""]
    head = [f"### {label}", "", "| 项 | 计数 |", "| --- | --- |"]
    return head + out + [""]


def _cooc_lines(cooc: list[Any], n: int = 5) -> list[str]:
    lines: list[str] = []
    for row in (cooc or [])[:n]:
        if not isinstance(row, dict):
            continue
        pair = row.get("pair")
        if not isinstance(pair, list) or len(pair) < 2:
            continue
        c = row.get("count", "—")
        lines.append(f"- `{pair[0]}` × `{pair[1]}` → **{c}**")
    if not lines:
        return ["_（无共现数据）_", ""]
    return ["### 因子共现（Top）", ""] + lines + [""]


def _trends_factor_lines(trends: dict[str, Any], n: int = 8) -> list[str]:
    fp = trends.get("factor_persistence")
    if not isinstance(fp, list) or not fp:
        return ["_（无 `factor_persistence`；可先 `make trends`）_", ""]
    rows = sorted(
        (r for r in fp if isinstance(r, dict) and r.get("factor")),
        key=lambda r: (-int(r.get("days_in_top") or 0), str(r.get("factor"))),
    )[:n]
    head = ["### 跨日因子持久度（sediment-trends）", "", "| factor | days_in_top | coverage |", "| --- | ---: | --- |"]
    body = []
    for r in rows:
        body.append(
            f"| `{r.get('factor')}` | {r.get('days_in_top', '—')} | {r.get('coverage', '—')} |"
        )
    return head + body + [""]


def _sediment_tail(sediment: dict[str, Any]) -> list[str]:
    ent = sediment.get("entries")
    if not isinstance(ent, list) or not ent:
        return ["_（无 `data/sediment.json` 条目）_", ""]
    last = ent[-1]
    if not isinstance(last, dict):
        return ["_（沉淀末条格式异常）_", ""]
    lines = [
        "### 沉淀最新一日",
        "",
        f"- **date**: `{last.get('date', '—')}`",
        f"- **manifest_n** / **candidate_n**: {last.get('manifest_n', '—')} / {last.get('candidate_n', '—')}",
        f"- **hint_closure_gaps_n**: {last.get('hint_closure_gaps_n', '—')}",
        f"- **run_id**: `{last.get('run_id', '—')}`",
    ]
    tf = last.get("top_factors")
    if isinstance(tf, list) and tf:
        lines.append(f"- **top_factors**: {', '.join(f'`{x}`' for x in tf[:8])}")
    return lines + [""]


def build_digest_markdown(
    snapshot: dict[str, Any],
    trends: dict[str, Any] | None,
    sediment: dict[str, Any] | None,
    *,
    include_trends: bool = True,
    include_sediment: bool = True,
) -> str:
    run = snapshot.get("run") if isinstance(snapshot.get("run"), dict) else {}
    rid = run.get("run_id", "—")
    rev = run.get("repo_revision", "—")
    gen = snapshot.get("generated_at", "—")
    src = snapshot.get("sources") or {}
    hd = (src.get("hint_decisions") or {}) if isinstance(src.get("hint_decisions"), dict) else {}
    ba = hd.get("by_action") or {}
    gaps = snapshot.get("hint_closure_gaps")
    ng = len(gaps) if isinstance(gaps, list) else 0
    hints_n = len(snapshot.get("evolution_hints") or []) if isinstance(
        snapshot.get("evolution_hints"), list
    ) else 0

    blocks: list[str] = [
        "## 进化智能摘要（规则层截面）",
        "",
        f"- **generated_at**: `{gen}`",
        f"- **run_id** / **repo_revision**: `{rid}` / `{rev}`",
        f"- **combined_for_analysis**: {src.get('combined_for_analysis', '—')}（manifest {src.get('manifest_signals', '—')} · candidate {src.get('candidate_signals', '—')}）",
        f"- **hint_decisions.total**: {hd.get('total', '—')}（done {ba.get('done', '—')} · rejected {ba.get('rejected', '—')} · deferred {ba.get('deferred', '—')}）",
        f"- **hint_closure_gaps**: {ng} 条 · **evolution_hints**: {hints_n} 条",
        "",
    ]
    if ng and isinstance(gaps, list):
        ids = [g.get("rule_id") for g in gaps if isinstance(g, dict) and g.get("rule_id")]
        if ids:
            blocks.append("**待闭环 rule_id**（节选）: " + " · ".join(f"`{x}`" for x in ids[:12]))
            blocks.append("")

    blocks += _heat_lines(snapshot.get("factor_heat") or [], "factor", "沙盘因子热力")
    blocks += _heat_lines(snapshot.get("module_heat") or [], "page", "页面热力")
    blocks += _cooc_lines(snapshot.get("cooccurrence") or [])

    if include_trends:
        if trends:
            blocks += _trends_factor_lines(trends)
        else:
            blocks += ["### 跨日趋势", "", "_（未找到 `assets/sediment-trends.json`）_", ""]

    if include_sediment:
        if sediment:
            blocks += _sediment_tail(sediment)
        else:
            blocks += ["### 沉淀", "", "_（未找到 `data/sediment.json`）_", ""]

    blocks += [
        "---",
        "",
        "**下一步（人工）**",
        "",
        "- 快照与上一版 diff：`python3 scripts/diff_analysis_snapshot.py --git HEAD~1:assets/analysis-snapshot.json`",
        "- 一行计数：`make status`",
        "- 路由规则回归：`PYTHONPATH=scripts python3 scripts/validate_golden_mapping.py --dir fixtures/ai_mapping_golden`",
        "",
    ]
    return "\n".join(blocks).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "--no-trends",
        action="store_true",
        help="不读取 sediment-trends.json",
    )
    ap.add_argument(
        "--no-sediment",
        action="store_true",
        help="不读取 data/sediment.json",
    )
    args = ap.parse_args()

    snap = load_json(SNAPSHOT_PATH)
    if not snap:
        print(
            f"未找到或未解析 {SNAPSHOT_PATH} — 请先 `make analyze` 或 `python3 scripts/analysis_engine.py`。",
            file=sys.stderr,
        )
        return 0

    trends = load_json(TRENDS_PATH) if not args.no_trends else None
    sediment = load_json(SEDIMENT_PATH) if not args.no_sediment else None

    text = build_digest_markdown(
        snap,
        trends,
        sediment,
        include_trends=not args.no_trends,
        include_sediment=not args.no_sediment,
    )
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
