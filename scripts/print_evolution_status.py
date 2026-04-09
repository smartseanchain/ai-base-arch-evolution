#!/usr/bin/env python3
"""
打印 assets/analysis-snapshot.json 中的核心计数（合并样本、决策统计、规则闭环缺口条数）。
便于本地或 CI 日志快速扫一眼；无快照时提示运行 analyze 并以 0 退出。
"""
from __future__ import annotations

import json
import sys

from evolution_io import REPO_ROOT

OUT = REPO_ROOT / "assets" / "analysis-snapshot.json"


def main() -> None:
    if not OUT.is_file():
        print(
            f"未找到 {OUT} — 请先运行: make analyze "
            "或 python3 scripts/analysis_engine.py",
            file=sys.stderr,
        )
        print(
            "提示: 快照生成后，已 validate 前提下可 make evolution-fast 做快速重算。",
            file=sys.stderr,
        )
        sys.exit(0)
    try:
        data = json.loads(OUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败 — {e}", file=sys.stderr)
        sys.exit(1)
    src = data.get("sources") or {}
    gaps = data.get("hint_closure_gaps")
    ng = len(gaps) if isinstance(gaps, list) else 0
    hd = src.get("hint_decisions") or {}
    ba = hd.get("by_action") or {}
    tot = hd.get("total")
    gen = data.get("generated_at") or "—"
    run = data.get("run") if isinstance(data.get("run"), dict) else {}
    rid = run.get("run_id") or "—"
    rev = run.get("repo_revision") or "—"
    print(
        f"status · generated_at={gen} · run_id={rid} · repo_revision={rev} · "
        f"combined={src.get('combined_for_analysis', '—')} · "
        f"manifest={src.get('manifest_signals', '—')} · "
        f"candidate={src.get('candidate_signals', '—')} · "
        f"hint_decisions={tot} "
        f"(done={ba.get('done', '—')} rejected={ba.get('rejected', '—')} "
        f"deferred={ba.get('deferred', '—')}) · "
        f"closure_gaps={ng}"
    )
    if ng and isinstance(gaps, list):
        ids = [g.get("rule_id") for g in gaps if isinstance(g, dict)]
        ids = [x for x in ids if x]
        if ids:
            print("  rule_ids: " + ", ".join(ids))


if __name__ == "__main__":
    main()
