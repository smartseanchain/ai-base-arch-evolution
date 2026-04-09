#!/usr/bin/env python3
"""校验 assets/evolution-manifest.json 结构。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

MANIFEST = REPO_ROOT / "assets" / "evolution-manifest.json"

ALLOWED_KIND = frozenset({"opinion", "policy", "market", "tech", "law"})
ALLOWED_WEIGHT = frozenset({"high", "medium", "low"})


def main() -> None:
    if not MANIFEST.is_file():
        print(f"错误: 未找到 {MANIFEST}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        print("错误: schema_version 须为 1", file=sys.stderr)
        sys.exit(1)
    signals = data.get("signals")
    if not isinstance(signals, list) or not signals:
        print("错误: signals 须为非空数组", file=sys.stderr)
        sys.exit(1)
    ids: set[str] = set()
    for i, s in enumerate(signals):
        sid = s.get("id")
        if not sid or not isinstance(sid, str):
            print(f"错误: signals[{i}] 缺少 id", file=sys.stderr)
            sys.exit(1)
        if sid in ids:
            print(f"错误: 重复 id: {sid}", file=sys.stderr)
            sys.exit(1)
        ids.add(sid)
        k = s.get("kind")
        if k not in ALLOWED_KIND:
            print(f"错误: {sid} kind 非法: {k}", file=sys.stderr)
            sys.exit(1)
        w = s.get("weight", "medium")
        if w not in ALLOWED_WEIGHT:
            print(f"错误: {sid} weight 非法: {w}", file=sys.stderr)
            sys.exit(1)
        m = s.get("maps_to") or {}
        if not isinstance(m, dict):
            print(f"错误: {sid} maps_to 须为对象", file=sys.stderr)
            sys.exit(1)
        lf = m.get("lab_factors") or []
        if lf and not isinstance(lf, list):
            print(f"错误: {sid} lab_factors 须为数组", file=sys.stderr)
            sys.exit(1)
    print(f"OK: {len(signals)} 条信号 · {MANIFEST}")


if __name__ == "__main__":
    main()
