"""
单次分析聚合：热力、共现、进化提示与闭环缺口（无文件 IO）。

由 ``analysis_engine`` 调用；提示拼装见 ``analysis_hints``，闭环见 ``hint_closure``。
"""
from __future__ import annotations

from collections import Counter
from typing import Any

from evolution_pkg.analysis_hints import (
    compute_diff_hints,
    evaluate_hint_rules,
    hint_entry,
)
from evolution_pkg.hint_closure import (
    closed_rule_ids_from_decisions,
    compute_hint_closure_gaps,
    track_closure_rule_ids,
)


def run_analysis(
    signals: list[dict],
    prev_snapshot: dict[str, Any] | None,
    hint_rules: dict[str, Any],
    decisions_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    mod_c: Counter[str] = Counter()
    fac_c: Counter[str] = Counter()
    kind_c: Counter[str] = Counter()
    pair_c: Counter[tuple[str, str]] = Counter()

    for sig in signals:
        kind_c[sig.get("kind") or "unknown"] += 1
        mt = sig.get("maps_to") or {}
        for p in mt.get("pages") or []:
            mod_c[p] += 1
        facs = list(mt.get("lab_factors") or [])
        for f in facs:
            fac_c[f] += 1
        for i, a in enumerate(facs):
            for b in facs[i + 1 :]:
                pair = tuple(sorted((a, b)))
                pair_c[pair] += 1

    module_heat = [{"page": k, "count": v} for k, v in mod_c.most_common(24)]
    factor_heat = [{"factor": k, "count": v} for k, v in fac_c.most_common(24)]
    cooccurrence = [
        {"pair": list(p), "count": c} for p, c in pair_c.most_common(16) if c > 0
    ]
    kind_distribution = dict(kind_c)

    manifest_n = sum(1 for s in signals if s.get("_origin") == "manifest")
    candidate_n = sum(1 for s in signals if s.get("_origin") == "candidate")

    json_hints = evaluate_hint_rules(fac_c, len(signals), hint_rules)
    dd = decisions_doc if isinstance(decisions_doc, dict) else {}
    tracked = track_closure_rule_ids(hint_rules)
    closed = closed_rule_ids_from_decisions(dd)
    hint_closure_gaps = compute_hint_closure_gaps(json_hints, tracked, closed)

    hints: list[dict[str, Any]] = []
    hints.extend(
        compute_diff_hints(
            prev_snapshot, factor_heat, cooccurrence, manifest_n, candidate_n
        )
    )
    hints.extend(json_hints)

    top_tpl = hint_rules.get("top_factors_template") or ""
    top_f = [x["factor"] for x in factor_heat[:3]]
    if top_f and top_tpl:
        hints.append(
            hint_entry(
                top_tpl.format(top_factors="、".join(top_f)),
                "top_factors",
                {"target_pages": ["lab.html"]},
            )
        )
    if not hints:
        hints.append(
            hint_entry(
                hint_rules.get("fallback_hint")
                or "信号较少：优先跑 ingest 抓取或手工充实 manifest，再重新执行本分析脚本。",
                "fallback",
                {"target_pages": ["evolution-loop.html"]},
            )
        )

    return {
        "module_heat": module_heat,
        "factor_heat": factor_heat,
        "kind_distribution": kind_distribution,
        "cooccurrence": cooccurrence,
        "evolution_hints": hints[:8],
        "hint_closure_gaps": hint_closure_gaps,
    }
