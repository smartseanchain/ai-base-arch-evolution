"""print_evolution_status · overlay_status_lines。"""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from print_evolution_status import overlay_status_lines


class TestOverlayStatusLines(unittest.TestCase):
    def test_empty_repo(self) -> None:
        d = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(d, ignore_errors=True))
        self.assertEqual(overlay_status_lines(d), [])

    def test_step_and_dead_letter(self) -> None:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        (root / "artifacts").mkdir(parents=True)
        (root / "artifacts" / "ai-overlay-step.json").write_text(
            json.dumps({"mode": "skip", "source_run_id": None}, ensure_ascii=False),
            encoding="utf-8",
        )
        (root / "artifacts" / "ai-overlay-llm-dead-letter.txt").write_text(
            "x" * 100, encoding="utf-8"
        )
        lines = overlay_status_lines(root)
        self.assertTrue(any("mode=skip" in x for x in lines))
        self.assertTrue(any("dead-letter" in x and "bytes=100" in x for x in lines))

    def test_step_otel_hints_tokens(self) -> None:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        (root / "artifacts").mkdir(parents=True)
        (root / "artifacts" / "ai-overlay-step.json").write_text(
            json.dumps(
                {
                    "mode": "llm",
                    "source_run_id": "r1",
                    "otel_hints": {
                        "attributes": {
                            "gen_ai.usage.input_tokens": 100,
                            "gen_ai.usage.output_tokens": 20,
                            "gen_ai.usage.total_tokens": 120,
                        }
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        lines = overlay_status_lines(root)
        self.assertTrue(any("in=100" in x and "tot=120" in x for x in lines))

    def test_step_raw_usage_tokens(self) -> None:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        (root / "artifacts").mkdir(parents=True)
        (root / "artifacts" / "ai-overlay-step.json").write_text(
            json.dumps(
                {
                    "mode": "llm",
                    "source_run_id": "r2",
                    "usage": {
                        "prompt_tokens": 5,
                        "completion_tokens": 2,
                        "total_tokens": 7,
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        lines = overlay_status_lines(root)
        self.assertTrue(any("tot=7" in x and "in=5" in x for x in lines))

    def test_overlay_asset(self) -> None:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        (root / "assets").mkdir(parents=True)
        (root / "assets" / "ai-analysis-overlay.json").write_text(
            json.dumps(
                {
                    "source_run_id": "r1",
                    "provider": {"kind": "stub", "model": "none"},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        lines = overlay_status_lines(root)
        self.assertTrue(any("provider=stub" in x and "source_run_id=r1" in x for x in lines))


if __name__ == "__main__":
    unittest.main()
