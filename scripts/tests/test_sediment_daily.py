"""evolution_pkg.sediment_daily JSON 侧行为；SQLite 在单测中 mock，避免写真实 evolution.db。"""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from evolution_pkg.sediment_daily import append_daily_sediment


class TestAppendDailySedimentJson(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = Path(tempfile.mkdtemp())
        self.path = self._dir / "sediment.json"

    def tearDown(self) -> None:
        shutil.rmtree(self._dir, ignore_errors=True)

    def _meta(self, **kwargs: object) -> dict:
        base = {
            "manifest_n": 0,
            "candidate_n": 0,
            "top_factors": [],
            "top_pages": [],
            "hint_closure_gaps_n": 0,
            "hint_decisions_total": 0,
            "run_id": "r",
            "repo_revision": "rev",
        }
        base.update(kwargs)
        return base

    @mock.patch("builtins.print")
    @mock.patch("sqlite_store.upsert_sediment")
    @mock.patch("sqlite_store.DB_PATH", "/tmp/evolution-test.db")
    def test_creates_schema_and_entry(
        self, _mock_upsert: mock.MagicMock, _print: mock.MagicMock
    ) -> None:
        append_daily_sediment(self.path, self._meta(manifest_n=2))
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("schema_version"), 1)
        self.assertEqual(len(data["entries"]), 1)
        self.assertEqual(data["entries"][0]["manifest_n"], 2)
        self.assertIn("date", data["entries"][0])

    @mock.patch("builtins.print")
    @mock.patch("sqlite_store.upsert_sediment")
    @mock.patch("sqlite_store.DB_PATH", "/tmp/evolution-test.db")
    def test_same_day_updates_last_entry(
        self, _mock_upsert: mock.MagicMock, _print: mock.MagicMock
    ) -> None:
        append_daily_sediment(self.path, self._meta(manifest_n=1))
        append_daily_sediment(self.path, self._meta(manifest_n=9))
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["entries"]), 1)
        self.assertEqual(data["entries"][0]["manifest_n"], 9)


if __name__ == "__main__":
    unittest.main()
