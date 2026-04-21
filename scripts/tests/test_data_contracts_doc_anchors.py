"""DATA_CONTRACTS.md 中对外深链依赖的 HTML 锚点防漂移。"""
from __future__ import annotations

import unittest
from pathlib import Path

# 与 MERGE / PLATFORM / INTEGRATION / schemas README 等文档中的 #fragment 对齐
_REQUIRED_ANCHOR_IDS: tuple[str, ...] = (
    "signals-candidates",
    "ingest-config-contract",
    "sqlite-sidecar-column-inventory",
    "pipeline-telemetry",
    "readonly-api-routes",
)


class TestDataContractsDocAnchors(unittest.TestCase):
    def test_required_html_anchor_ids_present(self) -> None:
        root = Path(__file__).resolve().parents[2]
        path = root / "docs" / "DATA_CONTRACTS.md"
        self.assertTrue(path.is_file(), msg="缺少 docs/DATA_CONTRACTS.md")
        text = path.read_text(encoding="utf-8")
        for aid in _REQUIRED_ANCHOR_IDS:
            with self.subTest(anchor_id=aid):
                needle = f'<a id="{aid}"></a>'
                self.assertIn(
                    needle,
                    text,
                    msg=f"勿删 DATA_CONTRACTS 锚点 {needle}（多处文档深链依赖）",
                )

    def test_ingest_config_row_still_in_section2_table(self) -> None:
        root = Path(__file__).resolve().parents[2]
        text = (root / "docs" / "DATA_CONTRACTS.md").read_text(encoding="utf-8")
        self.assertIn(
            "`scripts/ingest_config.json`",
            text,
            msg="ingest_config 表行应保留在 §2 信号与候选",
        )

    def test_merge_and_contributing_still_link_ingest_anchor(self) -> None:
        root = Path(__file__).resolve().parents[2]
        fragment = "#ingest-config-contract"
        for rel in (
            "docs/MERGE_AND_RELEASE_CHECKLIST.md",
            "CONTRIBUTING.md",
        ):
            with self.subTest(file=rel):
                body = (root / rel).read_text(encoding="utf-8")
                self.assertIn(
                    fragment,
                    body,
                    msg=f"{rel} 应保留对 DATA_CONTRACTS{fragment} 的深链",
                )

    def test_readonly_section_links_integration_gateway_default_deny(self) -> None:
        root = Path(__file__).resolve().parents[2]
        text = (root / "docs" / "DATA_CONTRACTS.md").read_text(encoding="utf-8")
        self.assertIn(
            "./INTEGRATION_AND_READONLY_API.md#gateway-default-deny-sensitive",
            text,
            msg="§8.1 应对读 INTEGRATION 网关默认建议锚点",
        )

    def test_integration_doc_links_merge_partials_sequence(self) -> None:
        root = Path(__file__).resolve().parents[2]
        text = (root / "docs" / "INTEGRATION_AND_READONLY_API.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence",
            text,
            msg="INTEGRATION 应对读 MERGE partials 手顺（顶栏/失页/merge-ready 段落）",
        )


if __name__ == "__main__":
    unittest.main()
