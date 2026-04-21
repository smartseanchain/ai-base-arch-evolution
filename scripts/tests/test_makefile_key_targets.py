"""Makefile 关键目标名防漂移（与文档 / CONTRIBUTING 对表）。"""
from __future__ import annotations

import unittest
from pathlib import Path


class TestMakefileKeyTargets(unittest.TestCase):
    def test_documented_targets_present(self) -> None:
        root = Path(__file__).resolve().parents[2]
        mf = root / "Makefile"
        self.assertTrue(mf.is_file(), msg="缺少根 Makefile")
        text = mf.read_text(encoding="utf-8")
        for needle in (
            "validate-fast:",
            "clean-pipeline-metrics-dry-run:",
            "clean-pipeline-metrics:",
            "clean-overlay-artifacts:",
            "validate:",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text, msg=f"Makefile 须保留目标 {needle!r}")


if __name__ == "__main__":
    unittest.main()
