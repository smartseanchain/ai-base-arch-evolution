"""合并真源入口防漂移：ci.yml · validate job 与 .githooks/pre-commit 须调用 run_validate.sh；非注释行不得执行 run_validate_fast.sh。"""
from __future__ import annotations

import unittest
from pathlib import Path


def _non_comment_text(text: str) -> str:
    """整行以 # 开头视为注释；其余行拼接后用于检测是否误接 fast 闸门脚本。"""
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(line)
    return "\n".join(lines)


class TestCiValidateWorkflow(unittest.TestCase):
    def test_all_github_workflows_avoid_fast_gate_shell(self) -> None:
        root = Path(__file__).resolve().parents[2]
        wf_dir = root / ".github" / "workflows"
        self.assertTrue(wf_dir.is_dir(), msg="缺少 .github/workflows")
        for path in sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml")):
            with self.subTest(workflow=path.name):
                body = _non_comment_text(path.read_text(encoding="utf-8"))
                self.assertNotIn(
                    "run_validate_fast.sh",
                    body,
                    msg=f"{path.relative_to(root)} 非注释行不应调用 run_validate_fast.sh",
                )

    def test_validate_job_runs_full_gate_shell(self) -> None:
        root = Path(__file__).resolve().parents[2]
        ci = root / ".github" / "workflows" / "ci.yml"
        self.assertTrue(ci.is_file(), msg="缺少 .github/workflows/ci.yml")
        text = ci.read_text(encoding="utf-8")
        self.assertIn(
            "bash scripts/run_validate.sh",
            text,
            msg="ci.yml validate job 应执行 bash scripts/run_validate.sh",
        )
        # run_validate_fast：已由 test_all_github_workflows_avoid_fast_gate_shell 覆盖 ci.yml

    def test_pre_commit_invokes_full_gate_shell_only(self) -> None:
        root = Path(__file__).resolve().parents[2]
        hook = root / ".githooks" / "pre-commit"
        self.assertTrue(hook.is_file(), msg="缺少 .githooks/pre-commit")
        text = hook.read_text(encoding="utf-8")
        self.assertIn(
            "bash scripts/run_validate.sh",
            text,
            msg="pre-commit 应调用 bash scripts/run_validate.sh",
        )
        self.assertNotIn(
            "run_validate_fast.sh",
            _non_comment_text(text),
            msg="pre-commit 非注释行不应调用 run_validate_fast.sh",
        )


if __name__ == "__main__":
    unittest.main()
