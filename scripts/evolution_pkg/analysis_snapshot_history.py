"""
本地 SQLite 表 ``analysis_snapshot_history`` 的只读封装。

实现与写入仍在同目录上级的 **`sqlite_store.py`**（`analysis_engine` 写快照时追加）。
本模块供 **`list_analysis_snapshot_history.py`**、**`readonly_api`** 统一入口。

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
