"""``validate_pipeline_metrics_schema.py`` · fixture 与 Schema 对齐。"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


class TestValidatePipelineMetricsSchema(unittest.TestCase):
    def test_cli_exits_zero_on_fixture(self) -> None:
        r = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "validate_pipeline_metrics_schema.py")],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(r.returncode, 0, msg=r.stderr or r.stdout)

    def test_legacy_artifact_stderr_hints_dry_run_make_target(self) -> None:
        ad = REPO / "artifacts"
        ad.mkdir(parents=True, exist_ok=True)
        legacy = ad / "pipeline-metrics-unittest-legacy-skip.json"
        self.addCleanup(legacy.unlink, missing_ok=True)
        legacy.write_text("{}", encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "validate_pipeline_metrics_schema.py")],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(r.returncode, 0, msg=r.stderr or r.stdout)
        self.assertIn("clean-pipeline-metrics-dry-run", r.stderr)
        self.assertIn("跳过旧格式遥测", r.stderr)


if __name__ == "__main__":
    unittest.main()
