"""
SQLite 存储（标准库 sqlite3）：沉淀日摘要，与 data/sediment.json 双写。
含 hint_closure_gaps_n、hint_decisions_total（与 JSON entries 对齐）；旧库启动时自动 ALTER 补列。
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
  hint_closure_gaps_n INTEGER NOT NULL DEFAULT 0,
  hint_decisions_total INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sediment_date ON sediment_entry(date);
"""


def _migrate_sediment_columns(conn: sqlite3.Connection) -> None:
    """旧库补列（CREATE TABLE 早于 hint_* 字段时）。"""
    cur = conn.execute("PRAGMA table_info(sediment_entry)")
    existing = {row[1] for row in cur.fetchall()}
    if "hint_closure_gaps_n" not in existing:
        conn.execute(
            "ALTER TABLE sediment_entry ADD COLUMN hint_closure_gaps_n "
            "INTEGER NOT NULL DEFAULT 0"
        )
    if "hint_decisions_total" not in existing:
        conn.execute(
            "ALTER TABLE sediment_entry ADD COLUMN hint_decisions_total "
            "INTEGER NOT NULL DEFAULT 0"
        )
    if "run_id" not in existing:
        conn.execute(
            "ALTER TABLE sediment_entry ADD COLUMN run_id TEXT NOT NULL DEFAULT ''"
        )
    if "repo_revision" not in existing:
        conn.execute(
            "ALTER TABLE sediment_entry ADD COLUMN repo_revision TEXT NOT NULL DEFAULT ''"
        )


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(DDL)
        _migrate_sediment_columns(conn)
        conn.commit()


def upsert_sediment(
    *,
    date: str,
    manifest_n: int,
    candidate_n: int,
    top_factors: list[str],
    top_pages: list[str],
    hint_closure_gaps_n: int = 0,
    hint_decisions_total: int = 0,
    run_id: str = "",
    repo_revision: str = "",
) -> None:
    init_db()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO sediment_entry (
              date, manifest_n, candidate_n,
              top_factors_json, top_pages_json,
              hint_closure_gaps_n, hint_decisions_total,
              run_id, repo_revision,
              updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
              manifest_n = excluded.manifest_n,
              candidate_n = excluded.candidate_n,
              top_factors_json = excluded.top_factors_json,
              top_pages_json = excluded.top_pages_json,
              hint_closure_gaps_n = excluded.hint_closure_gaps_n,
              hint_decisions_total = excluded.hint_decisions_total,
              run_id = excluded.run_id,
              repo_revision = excluded.repo_revision,
              updated_at = excluded.updated_at
            """,
            (
                date,
                manifest_n,
                candidate_n,
                json.dumps(top_factors, ensure_ascii=False),
                json.dumps(top_pages, ensure_ascii=False),
                int(hint_closure_gaps_n),
                int(hint_decisions_total),
                str(run_id or ""),
                str(repo_revision or ""),
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
            "SELECT date, manifest_n, candidate_n, top_factors_json, top_pages_json, "
            "hint_closure_gaps_n, hint_decisions_total, run_id, repo_revision "
            "FROM sediment_entry ORDER BY date"
        )
        rows = cur.fetchall()
    out: list[dict[str, Any]] = []
    for r in rows:
        row = {
            "date": r["date"],
            "manifest_n": r["manifest_n"],
            "candidate_n": r["candidate_n"],
            "top_factors": json.loads(r["top_factors_json"] or "[]"),
            "top_pages": json.loads(r["top_pages_json"] or "[]"),
            "hint_closure_gaps_n": int(r["hint_closure_gaps_n"] or 0),
            "hint_decisions_total": int(r["hint_decisions_total"] or 0),
        }
        run_id = str(r["run_id"] or "").strip()
        rev = str(r["repo_revision"] or "").strip()
        if run_id:
            row["run_id"] = run_id
        if rev:
            row["repo_revision"] = rev
        out.append(row)
    return out


def count_sediment_rows() -> int:
    if not DB_PATH.is_file():
        return 0
    with connect() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM sediment_entry")
        return int(cur.fetchone()[0])
