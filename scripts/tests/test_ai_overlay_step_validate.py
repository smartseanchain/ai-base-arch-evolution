"""ai_overlay_step_validate：侧车 JSON Schema。"""
from __future__ import annotations

import json
import unittest

from evolution_pkg.ai_overlay_step_validate import STEP_JSON, overlay_step_schema_violations


class TestAiOverlayStepValidate(unittest.TestCase):
    def test_no_file_returns_empty(self) -> None:
        backup = None
        if STEP_JSON.is_file():
            backup = STEP_JSON.read_text(encoding="utf-8")
            STEP_JSON.unlink()
        try:
            self.assertEqual(overlay_step_schema_violations(), [])
        finally:
            if backup is not None:
                STEP_JSON.parent.mkdir(parents=True, exist_ok=True)
                STEP_JSON.write_text(backup, encoding="utf-8")

    def test_invalid_json(self) -> None:
        backup = STEP_JSON.read_text(encoding="utf-8") if STEP_JSON.is_file() else None
        try:
            STEP_JSON.parent.mkdir(parents=True, exist_ok=True)
            STEP_JSON.write_text("{", encoding="utf-8")
            errs = overlay_step_schema_violations()
            self.assertTrue(any("JSON 无效" in e for e in errs), msg=errs)
        finally:
            if backup is not None:
                STEP_JSON.write_text(backup, encoding="utf-8")
            elif STEP_JSON.is_file():
                STEP_JSON.unlink()

    def test_valid_minimal(self) -> None:
        backup = STEP_JSON.read_text(encoding="utf-8") if STEP_JSON.is_file() else None
        try:
            STEP_JSON.parent.mkdir(parents=True, exist_ok=True)
            STEP_JSON.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "finished_at": "2026-01-01T00:00:00+08:00",
                        "mode": "skip",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            self.assertEqual(overlay_step_schema_violations(), [])
        finally:
            if backup is not None:
                STEP_JSON.write_text(backup, encoding="utf-8")
            elif STEP_JSON.is_file():
                STEP_JSON.unlink()


if __name__ == "__main__":
    unittest.main()
