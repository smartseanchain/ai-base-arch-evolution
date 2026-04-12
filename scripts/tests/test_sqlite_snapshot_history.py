"""sqlite_store · analysis_snapshot_history 追加与查询。"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import sqlite_store  # noqa: E402


class TestAnalysisSnapshotHistory(unittest.TestCase):
    def setUp(self) -> None:
        self._prev_db = sqlite_store.DB_PATH
        self.tdir = Path(tempfile.mkdtemp())
        sqlite_store.DB_PATH = self.tdir / "test_evolution.db"

    def tearDown(self) -> None:
        sqlite_store.DB_PATH = self._prev_db
        shutil.rmtree(self.tdir, ignore_errors=True)

    def test_append_ignore_duplicate_and_get(self) -> None:
        snap: dict = {
            "schema_version": 1,
            "generated_at": "2026-04-01T12:00:00Z",
            "run": {"run_id": "test-run-xyz", "repo_revision": "deadbeef"},
            "sources": {"combined_for_analysis": 3},
            "module_heat": [],
            "factor_heat": [],
        }
        self.assertTrue(sqlite_store.append_analysis_snapshot_history(snap))
        self.assertFalse(sqlite_store.append_analysis_snapshot_history(snap))
        rows = sqlite_store.list_analysis_snapshot_history(limit=10)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], "test-run-xyz")
        self.assertEqual(rows[0]["repo_revision"], "deadbeef")
        self.assertGreater(int(rows[0]["snapshot_bytes"]), 10)
        got = sqlite_store.get_analysis_snapshot_history("test-run-xyz")
        assert got is not None
        self.assertEqual(got["run"]["run_id"], "test-run-xyz")
        self.assertEqual(got["sources"]["combined_for_analysis"], 3)

    def test_skip_without_run_id(self) -> None:
        self.assertFalse(
            sqlite_store.append_analysis_snapshot_history({"schema_version": 1})
        )
        self.assertEqual(sqlite_store.count_analysis_snapshot_history(), 0)

    def test_get_missing(self) -> None:
        sqlite_store.init_db()
        self.assertIsNone(sqlite_store.get_analysis_snapshot_history("nope"))


if __name__ == "__main__":
    unittest.main()
