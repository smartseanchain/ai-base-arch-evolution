"""ai_overlay_write：解析与闸门（不默认外呼）。"""
from __future__ import annotations

import io
import json
import os
import unittest
from unittest.mock import patch

from evolution_pkg.ai_overlay_write import (
    _otel_hints_from_usage,
    _parse_llm_body,
    build_stub_document,
    run_write_overlay_main,
    truncate_context,
)


class TestAiOverlayWrite(unittest.TestCase):
    def test_truncate_context(self) -> None:
        big = {"x": "y" * 50000}
        s = truncate_context(big, 200)
        self.assertLessEqual(len(s), 250)
        self.assertIn("截断", s)

    def test_parse_llm_json_object(self) -> None:
        raw = json.dumps(
            {
                "summary_md": "## 摘要\n\n要点。",
                "sections": [{"title_zh": "A", "body_md": "正文"}],
            },
            ensure_ascii=False,
        )
        sm, secs = _parse_llm_body(raw)
        self.assertIn("摘要", sm)
        self.assertEqual(len(secs), 1)
        self.assertEqual(secs[0]["title_zh"], "A")

    def test_parse_llm_fenced(self) -> None:
        raw = '```json\n{"summary_md":"S","sections":[]}\n```'
        sm, secs = _parse_llm_body(raw)
        self.assertEqual(sm, "S")
        self.assertEqual(secs[0]["title_zh"], "解读")

    def test_build_stub_document_shape(self) -> None:
        d = build_stub_document("r1", "abc")
        self.assertEqual(d["source_run_id"], "r1")
        self.assertEqual(d["provider"]["kind"], "stub")
        self.assertIn("sections", d)

    def test_otel_hints_from_usage_maps_tokens(self) -> None:
        h = _otel_hints_from_usage(
            {"prompt_tokens": 10, "completion_tokens": 3, "total_tokens": 13}
        )
        self.assertIsNotNone(h)
        assert h is not None
        attrs = h.get("attributes") or {}
        self.assertEqual(attrs.get("gen_ai.usage.input_tokens"), 10)
        self.assertEqual(attrs.get("gen_ai.usage.output_tokens"), 3)
        self.assertEqual(attrs.get("gen_ai.usage.total_tokens"), 13)

    def test_otel_hints_from_usage_empty(self) -> None:
        self.assertIsNone(_otel_hints_from_usage({}))
        self.assertIsNone(_otel_hints_from_usage({"foo": "bar"}))

    def test_cli_skip_without_enable(self) -> None:
        from evolution_pkg.ai_overlay_write import TELEMETRY_JSON

        with patch.dict(os.environ, {}, clear=True):
            code = run_write_overlay_main(argv=[])
        self.assertEqual(code, 0)
        self.assertTrue(TELEMETRY_JSON.is_file())
        meta = json.loads(TELEMETRY_JSON.read_text(encoding="utf-8"))
        self.assertEqual(meta.get("mode"), "skip")
        try:
            TELEMETRY_JSON.unlink()
        except OSError:
            pass

    def test_cli_stub_missing_snapshot(self) -> None:
        from evolution_pkg import ai_overlay_write as mod

        with patch.object(mod, "build_context_payload", side_effect=FileNotFoundError("no snapshot")):
            with patch("sys.stderr", new=io.StringIO()):
                code = run_write_overlay_main(argv=["--stub"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
