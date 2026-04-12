#!/usr/bin/env python3
"""
使用 DuckDB 附加 SQLite evolution.db，运行示例 SQL（可选依赖）。
安装: python3 -m pip install -r requirements-analytics.txt
用法:
  python3 scripts/query_evolution_duckdb.py
  python3 scripts/query_evolution_duckdb.py -c "SELECT COUNT(*) FROM ev.sediment_entry"
"""
from __future__ import annotations

import argparse
import sys

from evolution_pkg.io import REPO_ROOT


def main() -> int:
    try:
        import duckdb
    except ImportError:
        print(
            "缺少 duckdb。请执行: python3 -m pip install -r requirements-analytics.txt",
            file=sys.stderr,
        )
        return 1

    db = REPO_ROOT / "data" / "evolution.db"
    ap = argparse.ArgumentParser(description="DuckDB + 附加 evolution.db (SQLite)")
    ap.add_argument(
        "-c",
        "--command",
        default="",
        help="单条 SQL；省略则运行内置示例",
    )
    args = ap.parse_args()

    if not db.is_file():
        print(
            f"未找到 {db}，请先本地运行 analysis_engine.py（写快照会建库）或 analysis_engine.py --sediment。",
            file=sys.stderr,
        )
        return 1

    con = duckdb.connect(database=":memory:")
    # Windows 路径含反斜杠时 DuckDB 需正斜杠或转义
    path = db.resolve().as_posix()
    con.execute(f"ATTACH '{path}' AS ev (TYPE sqlite)")

    def _print_result(cur2) -> None:
        rows2 = cur2.fetchall()
        desc2 = cur2.description
        if desc2:
            print("\t".join(d[0] for d in desc2))
        for row in rows2:
            print("\t".join(str(x) for x in row))

    sql = args.command.strip()
    if not sql:
        print("# ev.sediment_entry (recent)")
        _print_result(
            con.execute(
                """
                SELECT date, run_id, hint_closure_gaps_n, hint_decisions_total
                FROM ev.sediment_entry
                ORDER BY date DESC
                LIMIT 8
                """
            )
        )
        print()
        print("# ev.analysis_snapshot_history (recent)")
        try:
            _print_result(
                con.execute(
                    """
                    SELECT run_id, repo_revision, generated_at, stored_at,
                           length(snapshot_json) AS bytes
                    FROM ev.analysis_snapshot_history
                    ORDER BY stored_at DESC
                    LIMIT 8
                    """
                )
            )
        except Exception as exc:  # noqa: BLE001
            print(f"(跳过: 表不存在或为空 — {exc})")
        return 0
    cur = con.execute(sql)
    _print_result(cur)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
