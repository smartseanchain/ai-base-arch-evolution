"""
SQLite 存储（标准库 sqlite3）：沉淀日摘要，与 data/sediment.json 双写。
库文件默认 data/evolution.db；可在 .gitignore 中忽略二进制，仅提交 JSON。
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "evolution.db"

DDL = """
CREATE TABLE IF NOT EXISTS sediment_entry (
  date TEXT PRIMARY KEY,
  manifest_n INTEGER NOT NULL DEFAULT 0,
  candidate_n INTEGER NOT NULL DEFAULT 0,
  top_factors_json TEXT NOT NULL DEFAULT '[]',
  top_pages_json TEXT NOT NULL DEFAULT '[]',
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sediment_date ON sediment_entry(date);
"""


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(DDL)
        conn.commit()


def upsert_sediment(
    *,
    date: str,
    manifest_n: int,
    candidate_n: int,
    top_factors: list[str],
    top_pages: list[str],
) -> None:
    init_db()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO sediment_entry (date, manifest_n, candidate_n, top_factors_json, top_pages_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
              manifest_n = excluded.manifest_n,
              candidate_n = excluded.candidate_n,
              top_factors_json = excluded.top_factors_json,
              top_pages_json = excluded.top_pages_json,
              updated_at = excluded.updated_at
            """,
            (
                date,
                manifest_n,
                candidate_n,
                json.dumps(top_factors, ensure_ascii=False),
                json.dumps(top_pages, ensure_ascii=False),
                now,
            ),
        )
        conn.commit()


def list_sediment_entries() -> list[dict[str, Any]]:
    """返回与 sediment.json entries[] 同构的字典列表（无则 []）。"""
    if not DB_PATH.is_file():
        return []
    init_db()
    with connect() as conn:
        cur = conn.execute(
            "SELECT date, manifest_n, candidate_n, top_factors_json, top_pages_json FROM sediment_entry ORDER BY date"
        )
        rows = cur.fetchall()
    out: list[dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "date": r["date"],
                "manifest_n": r["manifest_n"],
                "candidate_n": r["candidate_n"],
                "top_factors": json.loads(r["top_factors_json"] or "[]"),
                "top_pages": json.loads(r["top_pages_json"] or "[]"),
            }
        )
    return out


def count_sediment_rows() -> int:
    if not DB_PATH.is_file():
        return 0
    with connect() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM sediment_entry")
        return int(cur.fetchone()[0])
