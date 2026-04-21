"""ARCHITECTURE.md 中 validate / validate-fast 分界锚点与跨文档深链防漂移。"""
from __future__ import annotations

import unittest
from pathlib import Path

_RUN_VALIDATE_GATE = "#run-validate-gate"
# 多处使用 ./ARCHITECTURE.md# 或 docs/ARCHITECTURE.md#，统一断言 fragment
_LINKED_DOCS: tuple[str, ...] = (
    "docs/MERGE_AND_RELEASE_CHECKLIST.md",
    "docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md",
    "docs/DATA_CONTRACTS.md",
    "docs/ARCHITECTURE_ONE_PAGER.md",
    "docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md",
    "docs/TECH_ARCHITECTURE_CAPABILITIES.md",
    "docs/SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md",
)


class TestArchitectureDocAnchors(unittest.TestCase):
    def test_run_validate_gate_anchor_present(self) -> None:
        root = Path(__file__).resolve().parents[2]
        path = root / "docs" / "ARCHITECTURE.md"
        self.assertTrue(path.is_file(), msg="缺少 docs/ARCHITECTURE.md")
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            '<a id="run-validate-gate"></a>',
            text,
            msg="勿删 ARCHITECTURE 中 run_validate 与 validate-fast 分界锚点",
        )
        self.assertIn(
            '<a id="architecture-dataflow"></a>',
            text,
            msg="勿删 ARCHITECTURE 中文首数据流 Mermaid 深链锚点",
        )

    def test_linked_docs_keep_run_validate_gate_fragment(self) -> None:
        root = Path(__file__).resolve().parents[2]
        for rel in _LINKED_DOCS:
            with self.subTest(doc=rel):
                body = (root / rel).read_text(encoding="utf-8")
                self.assertIn(
                    _RUN_VALIDATE_GATE,
                    body,
                    msg=f"{rel} 应保留对 ARCHITECTURE{_RUN_VALIDATE_GATE} 的深链",
                )


if __name__ == "__main__":
    unittest.main()
