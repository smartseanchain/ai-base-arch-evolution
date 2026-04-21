"""analyze 流水线步骤与 run_validate.sh 闸门对齐（防漂移）。"""
from __future__ import annotations

import unittest

from evolution_pkg.pipeline.runner import steps_analyze, steps_fast


class TestPipelineRunner(unittest.TestCase):
    def test_analyze_includes_validate_gates(self) -> None:
        ids = [sid for sid, _ in steps_analyze()]
        for required in (
            "validate_evolution_registry_schema",
            "check_nav_links_registry",
            "validate_sediment_artifacts_schema",
            "write_ai_analysis_overlay",
            "validate_ai_overlay_step_schema",
            "validate_ai_analysis_overlay_schema",
        ):
            self.assertIn(required, ids, msg=f"缺少步骤 {required}，应与 run_validate.sh 对齐")

    def test_analyze_gate_order(self) -> None:
        ids = [sid for sid, _ in steps_analyze()]
        self.assertLess(
            ids.index("validate_evolution_registry_schema"),
            ids.index("check_manifest_drift"),
        )
        self.assertLess(
            ids.index("check_manifest_drift"),
            ids.index("check_nav_links_registry"),
        )
        self.assertLess(
            ids.index("sediment_trends"),
            ids.index("validate_sediment_artifacts_schema"),
        )
        self.assertLess(
            ids.index("validate_sediment_artifacts_schema"),
            ids.index("validate_snapshot_schema"),
        )
        self.assertLess(
            ids.index("analysis_engine_check"),
            ids.index("write_ai_analysis_overlay"),
        )
        self.assertLess(
            ids.index("write_ai_analysis_overlay"),
            ids.index("validate_ai_overlay_step_schema"),
        )
        self.assertLess(
            ids.index("validate_ai_overlay_step_schema"),
            ids.index("validate_ai_analysis_overlay_schema"),
        )

    def test_fast_skips_preflight(self) -> None:
        ids = {sid for sid, _ in steps_fast()}
        self.assertNotIn("validate_evolution_registry_schema", ids)
        self.assertNotIn("check_nav_links_registry", ids)
        self.assertIn("write_ai_analysis_overlay", ids)
        self.assertIn("validate_ai_overlay_step_schema", ids)
        self.assertIn("validate_ai_analysis_overlay_schema", ids)


if __name__ == "__main__":
    unittest.main()
