"""
本地 SQLite 表 ``analysis_snapshot_history`` 的只读封装。

实现与写入仍在同目录上级的 **`sqlite_store.py`**（`analysis_engine` 写快照时追加）。
本模块供 **`readonly_api`** 与 CLI 使用；根目录 **`list_analysis_snapshot_history.py`** 为兼容薄壳。

**推荐调用**：``PYTHONPATH=scripts python3 -m evolution_pkg.analysis_snapshot_history``（参数同原脚本：**``--limit``**、**``--offset``**、**``--json``**）。

运行前提：`PYTHONPATH` 须包含 **`scripts`**（与仓库内单测、`uvicorn readonly_api` 一致）。
"""
from __future__ import annotations

from typing import Any

import sqlite_store


def list_meta(*, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
    """元数据行列表，按 ``stored_at`` 新到旧。"""
    return sqlite_store.list_analysis_snapshot_history(limit=limit, offset=offset)


def count_rows() -> int:
    return sqlite_store.count_analysis_snapshot_history()


def get_full(run_id: str) -> dict[str, Any] | None:
    """按 ``run_id`` 取完整快照对象；无则 ``None``。"""
    return sqlite_store.get_analysis_snapshot_history(run_id)


def main(argv: list[str] | None = None) -> int:
    """CLI：列出 ``analysis_snapshot_history`` 元数据；成功返回 0。"""
    import argparse
    import json
    import sys

    ap = argparse.ArgumentParser(
        description="列出 SQLite 中的 analysis_snapshot_history 元数据（run_id、时间、JSON 字节数）。"
    )
    ap.add_argument("--limit", type=int, default=30, help="条数上限（默认 30，最大 500）")
    ap.add_argument("--offset", type=int, default=0, help="偏移")
    ap.add_argument("--json", action="store_true", help="输出 JSON 数组")
    args = ap.parse_args(argv)

    if not sqlite_store.DB_PATH.is_file():
        print(f"无数据库文件: {sqlite_store.DB_PATH}", file=sys.stderr)
        return 1
    total = count_rows()
    rows = list_meta(limit=args.limit, offset=args.offset)
    if args.json:
        print(json.dumps({"total": total, "rows": rows}, ensure_ascii=False, indent=2))
        return 0
    print(f"库: {sqlite_store.DB_PATH}")
    print(f"共 {total} 条（展示 {len(rows)} 条）")
    for r in rows:
        print(
            f"  {r['run_id']}  rev={r['repo_revision']}  "
            f"gen={r['generated_at']}  stored={r['stored_at']}  "
            f"{r['snapshot_bytes']} B"
        )
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
