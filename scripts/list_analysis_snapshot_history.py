#!/usr/bin/env python3
"""
列出 data/evolution.db 中 analysis_snapshot_history 元数据（run_id、时间、JSON 字节数）。
完整快照：`python3 -c "import json; from sqlite_store import get_analysis_snapshot_history; print(json.dumps(get_analysis_snapshot_history('RUN_ID'), ensure_ascii=False, indent=2))"`
（需在仓库根且 PYTHONPATH=scripts）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from evolution_pkg.analysis_snapshot_history import (  # noqa: E402
    count_rows as count_analysis_snapshot_history,
    list_meta as list_analysis_snapshot_history,
)
from sqlite_store import DB_PATH  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="列出 SQLite 中的分析快照历史（元数据）")
    ap.add_argument("--limit", type=int, default=30, help="条数上限（默认 30，最大 500）")
    ap.add_argument("--offset", type=int, default=0, help="偏移")
    ap.add_argument("--json", action="store_true", help="输出 JSON 数组")
    args = ap.parse_args()
    if not DB_PATH.is_file():
        print(f"无数据库文件: {DB_PATH}", file=sys.stderr)
        sys.exit(1)
    total = count_analysis_snapshot_history()
    rows = list_analysis_snapshot_history(limit=args.limit, offset=args.offset)
    if args.json:
        print(
            json.dumps(
                {"total": total, "rows": rows},
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    print(f"库: {DB_PATH}")
    print(f"共 {total} 条（展示 {len(rows)} 条）")
    for r in rows:
        print(
            f"  {r['run_id']}  rev={r['repo_revision']}  "
            f"gen={r['generated_at']}  stored={r['stored_at']}  "
            f"{r['snapshot_bytes']} B"
        )


if __name__ == "__main__":
    main()
