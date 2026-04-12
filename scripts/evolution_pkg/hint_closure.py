"""
进化提示与决策闭环：track_closure 规则、候选 review_state、缺口列表。

供 ``analysis_engine`` 使用；逻辑与 ``assets/evolution-hint-decisions.json`` 约定一致。
"""
from __future__ import annotations

from typing import Any

ALLOWED_REVIEW_STATE = frozenset({"pending", "noise", "queued_for_manifest"})


def effective_review_state(sig: dict) -> str:
    r = sig.get("review_state") or "pending"
    if r in ALLOWED_REVIEW_STATE:
        return str(r)
    return "pending"


def track_closure_rule_ids(rules_doc: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for rule in rules_doc.get("rules") or []:
        if not rule.get("track_closure"):
            continue
        rid = rule.get("id")
        if rid is not None and str(rid).strip():
            out.add(str(rid).strip())
    return out


def closed_rule_ids_from_decisions(doc: dict[str, Any]) -> set[str]:
    """done / rejected 且带 rule_id 视为已闭环（延期 deferred 不算）。"""
    out: set[str] = set()
    for row in doc.get("decisions") or []:
        if not isinstance(row, dict):
            continue
        if row.get("action") not in ("done", "rejected"):
            continue
        rid = row.get("rule_id")
        if isinstance(rid, str) and rid.strip():
            out.add(rid.strip())
    return out


def compute_hint_closure_gaps(
    json_hints: list[dict[str, Any]],
    tracked: set[str],
    closed: set[str],
) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    seen: set[str] = set()
    for h in json_hints:
        if not isinstance(h, dict):
            continue
        rid = h.get("rule_id")
        if not isinstance(rid, str) or not rid.strip():
            continue
        rid = rid.strip()
        if rid not in tracked or rid in closed or rid in seen:
            continue
        seen.add(rid)
        text = h.get("text")
        t = (text if isinstance(text, str) else "")[:200]
        gaps.append({"rule_id": rid, "text": t})
    return gaps
