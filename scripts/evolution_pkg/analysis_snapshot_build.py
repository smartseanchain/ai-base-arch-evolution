"""
组装写入 ``analysis-snapshot.json`` 的顶层文档（内存 dict，无 IO）。

由 ``analysis_engine`` 在 ``run_analysis`` 之后调用；结构须与 ``--check`` / jsonschema 闸门一致。
"""
from __future__ import annotations

from typing import Any

from evolution_pkg.analysis_hints import (
    candidate_review_breakdown,
    hint_decisions_stats,
)
from evolution_pkg.hint_closure import effective_review_state


def build_analysis_snapshot_document(
    *,
    manifest: dict[str, Any],
    candidates: dict[str, Any],
    signals: list[dict],
    analysis: dict[str, Any],
    run: dict[str, Any],
    generated_at: str,
    hint_decisions_doc: dict[str, Any],
) -> dict[str, Any]:
    """合并 ``sources`` 与 ``run_analysis`` 产出为完整快照对象。"""
    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "run": run,
        "sources": {
            "manifest_signals": len(manifest.get("signals") or []),
            "candidate_signals": len(
                [
                    s
                    for s in candidates.get("signals") or []
                    if s.get("status") in (None, "candidate")
                    and effective_review_state(s) != "noise"
                ]
            ),
            "candidates_in_file": len(
                [
                    s
                    for s in candidates.get("signals") or []
                    if s.get("status") in (None, "candidate")
                ]
            ),
            "candidate_review_breakdown": candidate_review_breakdown(candidates),
            "hint_decisions": hint_decisions_stats(hint_decisions_doc),
            "combined_for_analysis": len(signals),
        },
        **analysis,
    }
