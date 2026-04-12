"""
SQLite 存储（标准库 sqlite3）：
- 沉淀日摘要，与 data/sediment.json 双写（sediment_entry）。
- 分析快照**追加历史**（analysis_snapshot_history）：每次 analysis_engine 写入
  assets/analysis-snapshot.json 时插入一行（run_id 主键）；**不**替代 Git 内快照闸门。

库文件默认 data/evolution.db；可在 .gitignore 中忽略二进制，仅提交 JSON。
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from evolution_pkg.io import REPO_ROOT

DB_PATH = REPO_ROOT / "data" / "evolution.db"

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

DDL_SNAPSHOT_HISTORY = """
CREATE TABLE IF NOT EXISTS analysis_snapshot_history (
  run_id TEXT PRIMARY KEY,
  repo_revision TEXT NOT NULL,
  generated_at TEXT NOT NULL,
  snapshot_json TEXT NOT NULL,
  stored_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_snap_hist_stored ON analysis_snapshot_history(stored_at);
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
        conn.executescript(DDL_SNAPSHOT_HISTORY)
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


def append_analysis_snapshot_history(snapshot: dict[str, Any]) -> bool:
    """
    追加一整份 analysis-snapshot 结构（与写入 assets/analysis-snapshot.json 的对象一致）。
    run_id 重复时 INSERT OR IGNORE，返回 False。成功插入返回 True。
    """
    run = snapshot.get("run")
    if not isinstance(run, dict):
        return False
    run_id = str(run.get("run_id") or "").strip()
    if not run_id:
        return False
    repo_revision = str(run.get("repo_revision") or "").strip()
    generated_at = str(snapshot.get("generated_at") or "")
    payload = json.dumps(snapshot, ensure_ascii=False)
    stored_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    init_db()
    with connect() as conn:
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO analysis_snapshot_history (
              run_id, repo_revision, generated_at, snapshot_json, stored_at
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (run_id, repo_revision, generated_at, payload, stored_at),
        )
        conn.commit()
        return cur.rowcount == 1


def list_analysis_snapshot_history(
    *,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """仅元数据，不含 snapshot_json；按 stored_at 新到旧。"""
    if not DB_PATH.is_file():
        return []
    init_db()
    lim = max(1, min(int(limit), 500))
    off = max(0, int(offset))
    with connect() as conn:
        cur = conn.execute(
            """
            SELECT run_id, repo_revision, generated_at, stored_at,
                   length(snapshot_json) AS snapshot_bytes
            FROM analysis_snapshot_history
            ORDER BY stored_at DESC
            LIMIT ? OFFSET ?
            """,
            (lim, off),
        )
        rows = cur.fetchall()
    out: list[dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "run_id": r["run_id"],
                "repo_revision": r["repo_revision"],
                "generated_at": r["generated_at"],
                "stored_at": r["stored_at"],
                "snapshot_bytes": int(r["snapshot_bytes"]),
            }
        )
    return out


def get_analysis_snapshot_history(run_id: str) -> dict[str, Any] | None:
    """按 run_id 取回完整快照对象；无则 None。"""
    rid = str(run_id or "").strip()
    if not rid or not DB_PATH.is_file():
        return None
    init_db()
    with connect() as conn:
        cur = conn.execute(
            "SELECT snapshot_json FROM analysis_snapshot_history WHERE run_id = ?",
            (rid,),
        )
        row = cur.fetchone()
    if not row:
        return None
    return json.loads(row["snapshot_json"])


def count_analysis_snapshot_history() -> int:
    if not DB_PATH.is_file():
        return 0
    init_db()
    with connect() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM analysis_snapshot_history")
        return int(cur.fetchone()[0])
