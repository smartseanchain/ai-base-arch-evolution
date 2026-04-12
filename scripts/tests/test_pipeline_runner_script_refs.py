"""evolution_pkg.pipeline.runner 的 steps_analyze / steps_fast 中引用的 scripts/*.py 须存在。"""
from __future__ import annotations

import unittest
from pathlib import Path

from evolution_pkg.pipeline.runner import steps_analyze, steps_fast


def _script_py_paths_in_argv(argv: list, scripts_dir: Path) -> list[Path]:
    out: list[Path] = []
    for a in argv:
        if not isinstance(a, str):
            continue
        p = Path(a)
        if not p.is_absolute():
            continue
        try:
            p.relative_to(scripts_dir)
        except ValueError:
            continue
        if p.suffix == ".py":
            out.append(p)
    return out


class TestPipelineRunnerScriptRefs(unittest.TestCase):
    def test_analyze_and_fast_steps_reference_existing_scripts(self) -> None:
        root = Path(__file__).resolve().parents[2]
        scripts_dir = root / "scripts"
        by_path: dict[Path, str] = {}
        for step_id, argv in list(steps_analyze()) + list(steps_fast()):
            for p in _script_py_paths_in_argv(argv, scripts_dir):
                rp = p.resolve()
                if rp not in by_path:
                    by_path[rp] = step_id
        self.assertTrue(
            by_path,
            msg="runner 应至少引用一条 scripts/*.py（analyze/fast 步骤表）",
        )
        for path, step_id in sorted(by_path.items(), key=lambda x: str(x[0])):
            self.assertTrue(
                path.is_file(),
                msg=f"runner 步骤 {step_id} 引用 {path.relative_to(root)}，但文件不存在",
            )


if __name__ == "__main__":
    unittest.main()
