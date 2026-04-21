"""pipeline 遥测合并 ai_overlay_step。"""
from __future__ import annotations

import io
import json
import os
import unittest
from unittest.mock import patch

from evolution_pkg.pipeline.runner import (
    AI_OVERLAY_STEP_JSON,
    ARTIFACTS,
    StepRecord,
    _write_telemetry,
)


class TestPipelineOverlayTelemetry(unittest.TestCase):
    def test_write_telemetry_embeds_ai_overlay_step(self) -> None:
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        prev_skip = os.environ.get("SKIP_PIPELINE_TELEMETRY")
        if prev_skip is not None:
            del os.environ["SKIP_PIPELINE_TELEMETRY"]
        backup = None
        if AI_OVERLAY_STEP_JSON.is_file():
            backup = AI_OVERLAY_STEP_JSON.read_text(encoding="utf-8")
        out_path = None
        try:
            AI_OVERLAY_STEP_JSON.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "finished_at": "2026-01-01T00:00:00Z",
                        "mode": "skip",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            with patch("sys.stderr", new=io.StringIO()):
                out_path = _write_telemetry(
                    "fast",
                    "t0",
                    [
                        StepRecord(
                            id="x",
                            argv=["python3"],
                            duration_ms=1.0,
                            exit_code=0,
                            stderr_tail="",
                        )
                    ],
                    True,
                    None,
                    input_artifacts={},
                )
            self.assertIsNotNone(out_path)
            doc = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(doc["ai_overlay_step"]["mode"], "skip")
        finally:
            if backup is not None:
                AI_OVERLAY_STEP_JSON.write_text(backup, encoding="utf-8")
            elif AI_OVERLAY_STEP_JSON.is_file():
                AI_OVERLAY_STEP_JSON.unlink()
            if out_path is not None and out_path.is_file():
                out_path.unlink()
            if prev_skip is not None:
                os.environ["SKIP_PIPELINE_TELEMETRY"] = prev_skip


if __name__ == "__main__":
    unittest.main()
