#!/usr/bin/env python3
"""校验 assets/evolution-candidates.json。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "assets" / "evolution-candidates.json"

ALLOWED_KIND = frozenset({"opinion", "policy", "market", "tech", "law"})
ALLOWED_WEIGHT = frozenset({"high", "medium", "low"})
ALLOWED_REVIEW_STATE = frozenset({"pending", "noise", "queued_for_manifest"})
REVIEWER_NOTE_MAX = 500


def main() -> None:
    if not PATH.is_file():
        print(f"OK: {PATH} 不存在（运行 ingest 后生成）")
        return
    data = json.loads(PATH.read_text(encoding="utf-8"))
    for i, s in enumerate(data.get("signals") or []):
        if s.get("kind") not in ALLOWED_KIND:
            print(f"错误: signals[{i}] kind 非法: {s.get('kind')}", file=sys.stderr)
            sys.exit(1)
        w = s.get("weight", "medium")
        if w not in ALLOWED_WEIGHT:
            print(f"错误: {s.get('id')} weight 非法", file=sys.stderr)
            sys.exit(1)
        rs = s.get("review_state") or "pending"
        if rs not in ALLOWED_REVIEW_STATE:
            print(
                f"错误: {s.get('id')} review_state 非法: {rs}（允许 pending|noise|queued_for_manifest）",
                file=sys.stderr,
            )
            sys.exit(1)
        note = s.get("reviewer_note")
        if note is not None and (
            not isinstance(note, str) or len(note) > REVIEWER_NOTE_MAX
        ):
            print(
                f"错误: {s.get('id')} reviewer_note 须为字符串且 ≤{REVIEWER_NOTE_MAX} 字",
                file=sys.stderr,
            )
            sys.exit(1)
    print(f"OK: {len(data.get('signals') or [])} 条候选 · {PATH}")


if __name__ == "__main__":
    main()
