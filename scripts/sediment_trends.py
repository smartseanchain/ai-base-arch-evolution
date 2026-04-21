#!/usr/bin/env python3
"""
长期沉淀分析：读取 data/sediment.json 多日条目，汇总因子/页面在 Top 列表中的出现天数与覆盖率，
写入 assets/sediment-trends.json，供 analysis-hub 与 BI 使用。

条目数极大时可在本地用 Polars/DuckDB 做等价聚合（见 requirements-analytics.txt、docs/DATA_CONTRACTS.md）。

用法:
  python3 scripts/sediment_trends.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from evolution_pkg.beijing_time import now_iso_beijing
from evolution_pkg.io import REPO_ROOT

SEDIMENT = REPO_ROOT / "data" / "sediment.json"
OUT = REPO_ROOT / "assets" / "sediment-trends.json"


def load_sediment_entries() -> tuple[list[dict[str, Any]], str]:
    """优先使用 SQLite（行数不少于 JSON 时）；否则用 sediment.json。返回 (条目, 来源说明)。"""
    json_entries: list[dict[str, Any]] = []
    if SEDIMENT.is_file():
        raw = json.loads(SEDIMENT.read_text(encoding="utf-8"))
        json_entries = [e for e in (raw.get("entries") or []) if isinstance(e, dict)]

    try:
        from sqlite_store import list_sediment_entries

        sql_entries = list_sediment_entries()
    except Exception:
        sql_entries = []

    if len(sql_entries) >= len(json_entries):
        return sql_entries, "data/evolution.db (SQLite)"
    return json_entries, "data/sediment.json"


def main() -> None:
    entries, src_label = load_sediment_entries()
    if not entries and not SEDIMENT.is_file():
        print(f"提示: 未找到 {SEDIMENT} 且无 SQLite 沉淀，请先运行 analysis_engine.py --sediment。")
        out = _empty_output()
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"已写入空占位 {OUT}")
        return

    if not entries:
        out = _empty_output()
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"已写入空占位 {OUT}")
        return

    # 按日期排序（ISO 字符串可比较）
    sorted_e = sorted(
        [e for e in entries if e.get("date")],
        key=lambda x: x["date"],
    )
    dates = [e["date"] for e in sorted_e]
    total_days = len(dates)
    first, last = dates[0], dates[-1]

    factor_days: dict[str, set[str]] = defaultdict(set)
    page_days: dict[str, set[str]] = defaultdict(set)

    for e in sorted_e:
        d = e["date"]
        for f in e.get("top_factors") or []:
            if isinstance(f, str) and f:
                factor_days[f].add(d)
        for p in e.get("top_pages") or []:
            if isinstance(p, str) and p:
                page_days[p].add(d)

    def persist(m: dict[str, set[str]], key_name: str) -> list[dict[str, Any]]:
        rows = []
        for name, day_set in m.items():
            n = len(day_set)
            rows.append(
                {
                    key_name: name,
                    "days_in_top": n,
                    "coverage": round(n / total_days, 4) if total_days else 0.0,
                    "first_seen": min(day_set) if day_set else None,
                    "last_seen": max(day_set) if day_set else None,
                }
            )
        rows.sort(key=lambda x: (-x["days_in_top"], x[key_name]))
        return rows

    factor_persistence = persist(factor_days, "factor")
    page_persistence = persist(page_days, "page")

    hints: list[str] = []
    if total_days >= 3:
        sticky = [x for x in factor_persistence if x["days_in_top"] >= total_days - 1]
        if sticky:
            hints.append(
                "以下因子在多日 Top 中反复出现："
                + "、".join(s["factor"] for s in sticky[:8])
                + "——适合与 §7 复合表对行、沙盘加压对照。"
            )
    if total_days >= 7 and page_persistence:
        top_p = page_persistence[0]
        if top_p["days_in_top"] >= 5:
            hints.append(
                f"页面「{top_p['page']}」长期居 Top——可专项审阅该页叙事是否需更新或删陈旧句。"
            )

    closure_backlog: list[dict[str, Any]] = []
    for e in sorted_e:
        closure_backlog.append(
            {
                "date": e["date"],
                "hint_closure_gaps_n": int(e.get("hint_closure_gaps_n") or 0),
                "hint_decisions_total": int(e.get("hint_decisions_total") or 0),
            }
        )
    if total_days >= 3 and len(closure_backlog) >= 3:
        tail = closure_backlog[-3:]
        if all(x["hint_closure_gaps_n"] >= 2 for x in tail):
            hints.append(
                "近 3 日「规则闭环缺口」均 ≥2：建议在双周节奏中优先补写 "
                "evolution-hint-decisions（rule_id + done/rejected）。"
            )

    if not hints:
        hints.append(
            "沉淀条目仍较少：坚持每日 --sediment，或合并历史备份后再跑本脚本以观察趋势。"
        )

    now = now_iso_beijing()
    out = {
        "schema_version": 1,
        "generated_at": now,
        "source": src_label,
        "summary": {
            "entry_count": total_days,
            "date_range": {"first": first, "last": last},
        },
        "factor_persistence": factor_persistence[:32],
        "page_persistence": page_persistence[:32],
        "closure_backlog": closure_backlog[-14:],
        "longterm_hints": hints[:6],
    }

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已写入 {OUT}（{total_days} 日 · 来源 {src_label}）")


def _empty_output() -> dict[str, Any]:
    now = now_iso_beijing()
    return {
        "schema_version": 1,
        "generated_at": now,
        "source": "data/sediment.json",
        "summary": {"entry_count": 0, "date_range": None},
        "factor_persistence": [],
        "page_persistence": [],
        "closure_backlog": [],
        "longterm_hints": [
            "暂无沉淀条目：运行 analysis_engine.py --sediment 数日后再执行本脚本。"
        ],
    }


if __name__ == "__main__":
    main()
