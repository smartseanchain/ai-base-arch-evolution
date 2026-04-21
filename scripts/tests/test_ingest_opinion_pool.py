"""``evolution_pkg.ingest_opinion_pool`` · 入池编排 CLI 返回值与缺配置行为。"""
from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path

import evolution_pkg.ingest_opinion_pool as pool


class TestFetchPacing(unittest.TestCase):
    def test_validate_rejects_unknown_key(self) -> None:
        cfg = {"fetch_pacing": {"after_rss_fetch": 0.5, "oops": 1}}
        with self.assertRaises(ValueError) as ctx:
            pool._validate_fetch_pacing(cfg)
        self.assertIn("未知键", str(ctx.exception))

    def test_validate_rejects_out_of_range(self) -> None:
        cfg = {"fetch_pacing": {"after_rss_fetch": 200.0}}
        with self.assertRaises(ValueError) as ctx:
            pool._validate_fetch_pacing(cfg)
        self.assertIn("120", str(ctx.exception))


class TestIngestOpinionPoolMain(unittest.TestCase):
    def test_main_returns_1_when_config_missing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bogus = Path(td) / "missing_ingest_config.json"
            with mock.patch.object(pool, "CONFIG_PATH", bogus):
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    rc = pool.main([])
                self.assertEqual(rc, 1)
                self.assertIn("错误", err.getvalue())
                self.assertIn(str(bogus), err.getvalue())
