"""
分析引擎中的提示与汇总：候选 review 分解、信号聚合、规则评估、与上期快照 diff。

由 ``analysis_engine`` 调用；规则 JSON 可通过 ``load_hint_rules_from_path`` 读取。
闭环缺口见 ``evolution_pkg.hint_closure``。
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from evolution_pkg.hint_closure import effective_review_state


def _default_hint_rules_doc() -> dict[str, Any]:
    return {
        "rules": [],
        "top_factors_template": (
            "当前热力靠前的沙盘因子：{top_factors}——打开沙盘工坊勾选对应项做一轮压测。"
        ),
        "fallback_hint": (
            "信号较少：优先跑 ingest 抓取或手工充实 manifest，再重新执行本分析脚本。"
        ),
    }


def load_hint_rules_from_path(path: Path) -> dict[str, Any]:
    """读取 ``evolution-hint-rules`` 形状 JSON；缺文件或坏 JSON 时返回内置默认文档。"""
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return _default_hint_rules_doc()


def hint_decisions_stats(doc: dict[str, Any]) -> dict[str, Any]:
    """与 evolution-hint-decisions.json 对齐的汇总，写入 analysis-snapshot.sources。"""
    by_action = {"done": 0, "rejected": 0, "deferred": 0}
    decs = doc.get("decisions")
    if not isinstance(decs, list):
        return {"total": 0, "by_action": dict(by_action)}
    n = 0
    for row in decs:
        if not isinstance(row, dict):
            continue
        n += 1
        a = row.get("action")
        if a in by_action:
            by_action[str(a)] += 1
    return {"total": n, "by_action": dict(by_action)}


def candidate_review_breakdown(candidates: dict) -> dict[str, int]:
    bd = {"pending": 0, "noise": 0, "queued_for_manifest": 0}
    for s in candidates.get("signals") or []:
        if s.get("status") not in (None, "candidate"):
            continue
        rs = effective_review_state(s)
        if rs in bd:
            bd[rs] += 1
        else:
            bd["pending"] += 1
    return bd


def collect_signals(manifest: dict, candidates: dict) -> list[dict]:
    out: list[dict] = []
    for s in manifest.get("signals") or []:
        x = dict(s)
        x["_origin"] = "manifest"
        out.append(x)
    for s in candidates.get("signals") or []:
        if s.get("status") != "candidate" and s.get("status") is not None:
            continue
        if effective_review_state(s) == "noise":
            continue
        x = dict(s)
        x["_origin"] = "candidate"
        out.append(x)
    return out


def hint_entry(
    text: str,
    rule_id: str | None,
    rule: dict[str, Any] | None = None,
) -> dict[str, Any]:
    o: dict[str, Any] = {"text": text, "rule_id": rule_id}
    if rule:
        tp = rule.get("target_pages")
        if isinstance(tp, list) and tp:
            o["target_pages"] = [str(p) for p in tp if p]
        ah = rule.get("anchor_hint")
        if isinstance(ah, str) and ah.strip():
            o["anchor_hint"] = ah.strip()
    return o


def evaluate_hint_rules(
    fac_c: Counter[str],
    signals_count: int,
    rules_doc: dict[str, Any],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rule in rules_doc.get("rules") or []:
        fm = rule.get("factors_min") or {}
        if any(fac_c.get(k, 0) < int(v) for k, v in fm.items()):
            continue
        smin = rule.get("signals_count_min")
        if smin is not None and signals_count < int(smin):
            continue
        rid = rule.get("id")
        rid_s = str(rid) if rid is not None else None
        tpl = rule.get("hint_template")
        plain = rule.get("hint")
        if tpl:
            out.append(
                hint_entry(tpl.format(signals_count=signals_count), rid_s, rule)
            )
        elif plain:
            out.append(hint_entry(str(plain), rid_s, rule))
    return out


def compute_diff_hints(
    prev: dict[str, Any] | None,
    factor_heat: list[dict],
    cooccurrence: list[dict],
    manifest_n: int,
    candidate_n: int,
) -> list[dict[str, Any]]:
    if not prev:
        return []
    hints: list[dict[str, Any]] = []
    prev_fac = [x["factor"] for x in (prev.get("factor_heat") or [])[:8]]
    curr_fac = [x["factor"] for x in factor_heat[:8]]
    prev_top_set = set(prev_fac[:8])
    new_in_top = [f for f in curr_fac[:5] if f not in prev_top_set]
    if new_in_top:
        hints.append(
            hint_entry(
                "相较上期快照，热力因子新进入前列："
                + "、".join(new_in_top)
                + "——建议核对 manifest/候选映射是否反映新焦点。",
                "diff_factor_top",
            )
        )

    prev_co: dict[tuple[str, str], int] = {}
    for x in prev.get("cooccurrence") or []:
        pr = x.get("pair")
        if isinstance(pr, list) and len(pr) == 2:
            prev_co[tuple(sorted((str(pr[0]), str(pr[1]))))] = int(x.get("count") or 0)

    co_added = 0
    for row in cooccurrence[:10]:
        pr = row.get("pair")
        if not isinstance(pr, list) or len(pr) != 2:
            continue
        p = tuple(sorted((str(pr[0]), str(pr[1]))))
        c = int(row.get("count") or 0)
        old = prev_co.get(p)
        if old is None:
            hints.append(
                hint_entry(
                    f"共现新出现：{' × '.join(p)}（count={c}）——可查复合表是否需补传导说明。",
                    "diff_cooccurrence",
                    {
                        "target_pages": ["synthesis.html"],
                        "anchor_hint": "复合表 / §7",
                    },
                )
            )
            co_added += 1
        elif c > old:
            hints.append(
                hint_entry(
                    f"共现增强：{' × '.join(p)}（{old}→{c}）——关注对应页面交叉叙事。",
                    "diff_cooccurrence",
                    {"target_pages": ["synthesis.html"]},
                )
            )
            co_added += 1
        if co_added >= 2:
            break

    prev_src = prev.get("sources") or {}
    pm = prev_src.get("manifest_signals")
    pc = prev_src.get("candidate_signals")
    if isinstance(pm, int) and manifest_n > pm:
        hints.append(
            hint_entry(
                f"已入库信号较上期增加 {manifest_n - pm} 条（{pm}→{manifest_n}），"
                "建议跑一轮沙盘与 §7 对行。",
                "diff_manifest_count",
                {"target_pages": ["lab.html", "synthesis.html"]},
            )
        )
    if isinstance(pc, int) and candidate_n > pc:
        hints.append(
            hint_entry(
                f"候选较上期增加 {candidate_n - pc} 条——可安排双周审阅或减噪。",
                "diff_candidate_count",
                {"target_pages": ["evolution-loop.html", "analysis-hub.html"]},
            )
        )

    return hints[:4]
