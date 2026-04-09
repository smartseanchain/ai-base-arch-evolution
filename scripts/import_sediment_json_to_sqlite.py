#!/usr/bin/env python3
"""
将 data/sediment.json 中的 entries 导入 data/evolution.db（INSERT OR REPLACE）。
用于首次启用 SQLite 或从 JSON 冷备恢复。

用法:
  python3 scripts/import_sediment_json_to_sqlite.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEDIMENT = ROOT / "data" / "sediment.json"

from sqlite_store import upsert_sediment  # noqa: E402


def main() -> None:
    if not SEDIMENT.is_file():
        print(f"错误: 未找到 {SEDIMENT}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(SEDIMENT.read_text(encoding="utf-8"))
    entries = data.get("entries") or []
    n = 0
    for e in entries:
        if not isinstance(e, dict) or not e.get("date"):
            continue
        upsert_sediment(
            date=e["date"],
            manifest_n=int(e.get("manifest_n") or 0),
            candidate_n=int(e.get("candidate_n") or 0),
            top_factors=list(e.get("top_factors") or []),
            top_pages=list(e.get("top_pages") or []),
        )
        n += 1
    print(f"已导入 {n} 条沉淀到 SQLite（data/evolution.db）")


if __name__ == "__main__":
    main()
