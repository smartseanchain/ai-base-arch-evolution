"""
正式 manifest 与候选池的**扁平结构**校验（非 jsonschema 全量）。

供 **`validate-evolution-manifest.py`** / **`validate-evolution-candidates.py`** 调用；
字段级契约仍以 **[DATA_CONTRACTS](../../docs/DATA_CONTRACTS.md)** 与 drift 对账为准。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from evolution_pkg.io import REPO_ROOT

MANIFEST_JSON_PATH = REPO_ROOT / "assets" / "evolution-manifest.json"
CANDIDATES_JSON_PATH = REPO_ROOT / "assets" / "evolution-candidates.json"

ALLOWED_SIGNAL_KIND = frozenset({"opinion", "policy", "market", "tech", "law"})
ALLOWED_SIGNAL_WEIGHT = frozenset({"high", "medium", "low"})
ALLOWED_REVIEW_STATE = frozenset({"pending", "noise", "queued_for_manifest"})
REVIEWER_NOTE_MAX = 500


class SignalsFlatValidationError(ValueError):
    """单条人类可读错误（与历史脚本 stderr 文案对齐）。"""


def validate_manifest_signals_structure(data: dict[str, Any]) -> int:
    """
    校验 ``evolution-manifest.json`` 顶层与 ``signals[]`` 形状。

    :returns: ``signals`` 条数
    :raises SignalsFlatValidationError: 结构不合法
    """
    if data.get("schema_version") != 1:
        raise SignalsFlatValidationError("错误: schema_version 须为 1")
    signals = data.get("signals")
    if not isinstance(signals, list) or not signals:
        raise SignalsFlatValidationError("错误: signals 须为非空数组")
    ids: set[str] = set()
    for i, s in enumerate(signals):
        sid = s.get("id")
        if not sid or not isinstance(sid, str):
            raise SignalsFlatValidationError(f"错误: signals[{i}] 缺少 id")
        if sid in ids:
            raise SignalsFlatValidationError(f"错误: 重复 id: {sid}")
        ids.add(sid)
        k = s.get("kind")
        if k not in ALLOWED_SIGNAL_KIND:
            raise SignalsFlatValidationError(f"错误: {sid} kind 非法: {k}")
        w = s.get("weight", "medium")
        if w not in ALLOWED_SIGNAL_WEIGHT:
            raise SignalsFlatValidationError(f"错误: {sid} weight 非法: {w}")
        m = s.get("maps_to") or {}
        if not isinstance(m, dict):
            raise SignalsFlatValidationError(f"错误: {sid} maps_to 须为对象")
        lf = m.get("lab_factors") or []
        if lf and not isinstance(lf, list):
            raise SignalsFlatValidationError(f"错误: {sid} lab_factors 须为数组")
    return len(signals)


def validate_candidates_signals_structure(data: dict[str, Any]) -> int:
    """
    校验 ``evolution-candidates.json`` 内 ``signals[]`` 条形状（文件存在由调用方保证）。

    :returns: ``signals`` 条数（含空列表）
    :raises SignalsFlatValidationError: 结构不合法
    """
    for i, s in enumerate(data.get("signals") or []):
        if s.get("kind") not in ALLOWED_SIGNAL_KIND:
            raise SignalsFlatValidationError(
                f"错误: signals[{i}] kind 非法: {s.get('kind')}"
            )
        w = s.get("weight", "medium")
        if w not in ALLOWED_SIGNAL_WEIGHT:
            raise SignalsFlatValidationError(f"错误: {s.get('id')} weight 非法")
        rs = s.get("review_state") or "pending"
        if rs not in ALLOWED_REVIEW_STATE:
            raise SignalsFlatValidationError(
                f"错误: {s.get('id')} review_state 非法: {rs}（允许 pending|noise|queued_for_manifest）"
            )
        note = s.get("reviewer_note")
        if note is not None and (
            not isinstance(note, str) or len(note) > REVIEWER_NOTE_MAX
        ):
            raise SignalsFlatValidationError(
                f"错误: {s.get('id')} reviewer_note 须为字符串且 ≤{REVIEWER_NOTE_MAX} 字"
            )
    return len(data.get("signals") or [])
