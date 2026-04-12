"""evolution_pkg.ai_overlay_validate 对 Schema 与 run_id 对账。"""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from evolution_pkg.ai_overlay_validate import overlay_schema_violations
from evolution_pkg.io import REPO_ROOT

_SCHEMA = REPO_ROOT / "docs" / "schemas" / "ai-analysis-overlay.schema.json"


def _valid_overlay(rid: str) -> dict:
    return {
        "schema_version": 1,
        "generated_at": "2026-01-01T00:00:00Z",
        "source_run_id": rid,
        "source_repo_revision": "abc",
        "provider": {"kind": "stub", "model": "none"},
        "disclaimer_zh": "测试",
        "sections": [{"title_zh": "节", "body_md": "正文"}],
    }


class TestAiOverlayValidate(unittest.TestCase):
    def test_no_overlay_file_returns_empty(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            miss = root / "missing.json"
            with patch("evolution_pkg.ai_overlay_validate.OVERLAY", miss), patch(
                "evolution_pkg.ai_overlay_validate.SCHEMA_PATH", _SCHEMA
            ), patch("evolution_pkg.ai_overlay_validate.SNAPSHOT", root / "snap.json"):
                self.assertEqual(overlay_schema_violations(), [])

    def test_run_id_mismatch(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            ov = root / "ai-analysis-overlay.json"
            ov.write_text(
                json.dumps(_valid_overlay("run-a"), ensure_ascii=False), encoding="utf-8"
            )
            sn = root / "analysis-snapshot.json"
            sn.write_text(
                json.dumps(
                    {"run": {"run_id": "run-b", "repo_revision": "x"}},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            with patch("evolution_pkg.ai_overlay_validate.OVERLAY", ov), patch(
                "evolution_pkg.ai_overlay_validate.SCHEMA_PATH", _SCHEMA
            ), patch("evolution_pkg.ai_overlay_validate.SNAPSHOT", sn):
                errs = overlay_schema_violations()
                self.assertTrue(errs)
                self.assertIn("run_id", errs[0])

    def test_matching_run_id_ok(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            ov = root / "ai-analysis-overlay.json"
            ov.write_text(
                json.dumps(_valid_overlay("run-z"), ensure_ascii=False), encoding="utf-8"
            )
            sn = root / "analysis-snapshot.json"
            sn.write_text(
                json.dumps(
                    {"run": {"run_id": "run-z", "repo_revision": "x"}},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            with patch("evolution_pkg.ai_overlay_validate.OVERLAY", ov), patch(
                "evolution_pkg.ai_overlay_validate.SCHEMA_PATH", _SCHEMA
            ), patch("evolution_pkg.ai_overlay_validate.SNAPSHOT", sn):
                self.assertEqual(overlay_schema_violations(), [])


if __name__ == "__main__":
    unittest.main()
