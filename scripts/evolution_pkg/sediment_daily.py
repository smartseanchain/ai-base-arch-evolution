"""
按日更新 ``sediment.json`` 并尽力双写 SQLite ``sediment_entry``（与 ``sqlite_store`` 对齐）。

由 ``analysis_engine --sediment`` 调用；路径由调用方注入以便单测使用临时文件。
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


def append_daily_sediment(sediment_path: Path, snapshot_meta: dict[str, Any]) -> None:
    """当日条目存在则 ``update``，否则 ``append``；SQLite 失败时 stderr 警告，JSON 已落盘。"""
    sediment_path.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    if sediment_path.is_file():
        data = json.loads(sediment_path.read_text(encoding="utf-8"))
    else:
        data = {"schema_version": 1, "entries": []}
    entries: list = data.setdefault("entries", [])
    if entries and isinstance(entries[-1], dict) and entries[-1].get("date") == today:
        entries[-1].update(snapshot_meta)
    else:
        entries.append({"date": today, **snapshot_meta})
    sediment_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    try:
        from sqlite_store import DB_PATH, upsert_sediment

        upsert_sediment(
            date=today,
            manifest_n=int(snapshot_meta.get("manifest_n") or 0),
            candidate_n=int(snapshot_meta.get("candidate_n") or 0),
            top_factors=list(snapshot_meta.get("top_factors") or []),
            top_pages=list(snapshot_meta.get("top_pages") or []),
            hint_closure_gaps_n=int(
                snapshot_meta.get("hint_closure_gaps_n") or 0
            ),
            hint_decisions_total=int(
                snapshot_meta.get("hint_decisions_total") or 0
            ),
            run_id=str(snapshot_meta.get("run_id") or ""),
            repo_revision=str(snapshot_meta.get("repo_revision") or ""),
        )
        print(f"已更新 SQLite {DB_PATH}")
    except Exception as exc:  # noqa: BLE001
        print(f"警告: SQLite 写入失败（JSON 已保留）: {exc}", file=sys.stderr)
