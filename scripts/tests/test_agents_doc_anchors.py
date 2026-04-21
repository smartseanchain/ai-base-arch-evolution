"""Stable HTML anchor in AGENTS.md and repo-wide deep-link hygiene."""

from __future__ import annotations

import unittest
from pathlib import Path

from doc_link_fragment_scan import collect_doc_link_offenders

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS = REPO_ROOT / "AGENTS.md"
DOCS_README = REPO_ROOT / "docs" / "README.md"

_DOCS_README_AGENTS_TABLE_FRAGMENTS = (
    "AGENTS.md#agents-content-framework",
    "AGENTS.md#agents-arch-boundary",
    "AGENTS.md#agents-reader-conventions",
    "AGENTS.md#agents-deep-read",
    "AGENTS.md#agents-cursor-rules",
)

_REQUIRED_AGENTS_ANCHORS = (
    "agents-contract",
    "agents-content-framework",
    "agents-pre-merge",
    "agents-admin-console",
    "agents-test-subset",
    "agents-invariants",
    "agents-arch-boundary",
    "agents-dual-track",
    "agents-reader-conventions",
    "agents-hub-lead",
    "agents-deep-read",
    "agents-cursor-rules",
)

# MERGE §4「自动化助手闸门」表行须覆盖的核心深链（不必穷举 AGENTS 全小节）。
_MERGE_AGENTS_GATE_ROW_FRAGMENTS = (
    "agents-contract",
    "agents-content-framework",
    "agents-pre-merge",
    "agents-invariants",
    "agents-admin-console",
    "agents-dual-track",
    "agents-hub-lead",
    "agents-test-subset",
)

_REPO_GATES_MDC_FRAGMENTS = tuple(
    f"AGENTS.md#{aid}" for aid in _MERGE_AGENTS_GATE_ROW_FRAGMENTS
)

_MERGE = REPO_ROOT / "docs" / "MERGE_AND_RELEASE_CHECKLIST.md"

# 枢纽 / 工具链：须含下列 `AGENTS.md#…` 子串（`../AGENTS.md#…` / `../../AGENTS.md#…` / `blob/.../AGENTS.md#…` 同理命中）。
_HUB_DOCS_AGENTS_FRAGMENTS: tuple[tuple[Path, tuple[str, ...]], ...] = (
    (
        REPO_ROOT / "docs" / "PROJECT_ARCHITECTURE_OVERVIEW.md",
        (
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "schemas" / "README.md",
        (
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "templates" / "incremental-pr-slice.md",
        (
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "PHASED_UPGRADE_EXECUTION_GUIDE.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "ARCHITECTURE_UPGRADE_ROADMAP.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "ORCHESTRATION_AND_EVENT_STREAMING.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "DEDUCTION_STRATEGY.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-arch-boundary",
        ),
    ),
    (
        REPO_ROOT / "docs" / "INCREMENTAL_BUILD_PLAYBOOK.md",
        (
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-content-framework",
        ),
    ),
    (
        REPO_ROOT / "docs" / "REFERENCE_DESIGN_OPINION_MONITORING.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "SYNTHESIS_SUBPAGES.md",
        (
            "AGENTS.md#agents-hub-lead",
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md",
        (
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "TECH_ARCHITECTURE_CAPABILITIES.md",
        (
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-deep-read",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-dual-track",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-dual-track",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "AI_ASSISTED_ANALYSIS_LAYER.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "RESEARCH_METHODS_MAP.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-test-subset",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "docs" / "SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md",
        (
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-arch-boundary",
        ),
    ),
    (
        REPO_ROOT / "docs" / "EVOLUTION_RUNBOOK.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-test-subset",
        ),
    ),
    (
        REPO_ROOT / "docs" / "DATA_ANALYSIS_SITE_CONTENT_SYNC.md",
        (
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "SITE_DATA_UPDATE_FRAMEWORK.md",
        (
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-reader-conventions",
        ),
    ),
    (
        REPO_ROOT / "docs" / "INTELLIGENCE_SIX_DOMAINS.md",
        (
            "AGENTS.md#agents-reader-conventions",
            "AGENTS.md#agents-hub-lead",
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "docs" / "PLATFORM_MASTER_MAP_AND_INVOCATION.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-test-subset",
            "AGENTS.md#agents-deep-read",
        ),
    ),
    (
        REPO_ROOT / "docs" / "ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-content-framework",
        ),
    ),
    (
        REPO_ROOT / "docs" / "INTEGRATION_AND_READONLY_API.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-arch-boundary",
        ),
    ),
    (
        REPO_ROOT / "docs" / "ARCHITECTURE.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-content-framework",
        ),
    ),
    (
        REPO_ROOT / "docs" / "DATA_CONTRACTS.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-arch-boundary",
        ),
    ),
    (
        REPO_ROOT / "docs" / "DOCKER.md",
        ("AGENTS.md#agents-contract",),
    ),
    (
        REPO_ROOT / "docs" / "PLATFORM_CAPABILITY_MAP.md",
        (
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-hub-lead",
            "AGENTS.md#agents-dual-track",
        ),
    ),
    (
        REPO_ROOT / "docs" / "ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md",
        ("AGENTS.md#agents-admin-console",),
    ),
    (
        REPO_ROOT / "docs" / "SITE_REVIEW_THREE_PASSES.md",
        ("AGENTS.md#agents-hub-lead",),
    ),
    (
        REPO_ROOT / "docs" / "ARCHITECTURE_ONE_PAGER.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-hub-lead",
        ),
    ),
    (
        REPO_ROOT / "docs" / "USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-dual-track",
        ),
    ),
    (
        REPO_ROOT / "docs" / "ADMIN_WEB_CONSOLE_ROADMAP.md",
        ("AGENTS.md#agents-invariants",),
    ),
    (
        REPO_ROOT / "docs" / "ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md",
        ("AGENTS.md#agents-invariants",),
    ),
    (
        REPO_ROOT / "docs" / "INTEL_AND_POLICY_TRACKING_PLAYBOOK.md",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-hub-lead",
            "AGENTS.md#agents-test-subset",
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-reader-conventions",
            "AGENTS.md#agents-deep-read",
            "AGENTS.md#agents-cursor-rules",
        ),
    ),
    (
        REPO_ROOT / "CONTRIBUTING.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-deep-read",
            "AGENTS.md#agents-cursor-rules",
            "AGENTS.md#agents-hub-lead",
            "AGENTS.md#agents-dual-track",
        ),
    ),
    (
        REPO_ROOT / "README.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-deep-read",
            "AGENTS.md#agents-cursor-rules",
        ),
    ),
    (
        REPO_ROOT / "spa" / "README.md",
        (
            "AGENTS.md#agents-dual-track",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-cursor-rules",
        ),
    ),
    (
        REPO_ROOT / "admin-console" / "README.md",
        (
            "AGENTS.md#agents-admin-console",
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-content-framework",
        ),
    ),
    (
        REPO_ROOT / "scripts" / "draft" / "README.md",
        ("AGENTS.md#agents-invariants",),
    ),
    (
        REPO_ROOT / "scripts" / "README.md",
        (
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / "maintainer-hub.html",
        (
            "AGENTS.md#agents-invariants",
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-contract",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / "admin-console" / "static" / "index.html",
        (
            "AGENTS.md#agents-admin-console",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / ".github" / "pull_request_template.md",
        (
            "AGENTS.md#agents-hub-lead",
            "AGENTS.md#agents-dual-track",
        ),
    ),
    (
        REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "pipeline-triage.md",
        (
            "AGENTS.md#agents-pre-merge",
            "AGENTS.md#agents-invariants",
        ),
    ),
    (
        REPO_ROOT / ".github" / "workflows" / "ci.yml",
        ("AGENTS.md#agents-pre-merge",),
    ),
    (
        REPO_ROOT / ".github" / "workflows" / "ingest-pipeline.yml",
        ("AGENTS.md#agents-invariants",),
    ),
    (
        REPO_ROOT / ".github" / "workflows" / "pr-candidates.yml",
        ("AGENTS.md#agents-invariants",),
    ),
    (
        REPO_ROOT / ".github" / "workflows" / "update-pipeline.yml",
        (
            "AGENTS.md#agents-arch-boundary",
            "AGENTS.md#agents-pre-merge",
        ),
    ),
    (
        REPO_ROOT / ".cursor" / "rules" / "repo-gates.mdc",
        _REPO_GATES_MDC_FRAGMENTS,
    ),
    (
        REPO_ROOT / ".cursor" / "rules" / "spa-nav-config.mdc",
        (
            "AGENTS.md#agents-dual-track",
            "AGENTS.md#agents-cursor-rules",
        ),
    ),
    (
        REPO_ROOT / ".cursor" / "rules" / "spa-nav-registry.mdc",
        (
            "AGENTS.md#agents-dual-track",
            "AGENTS.md#agents-cursor-rules",
        ),
    ),
    (
        REPO_ROOT / ".cursor" / "rules" / "evolution-registry.mdc",
        (
            "AGENTS.md#agents-content-framework",
            "AGENTS.md#agents-dual-track",
        ),
    ),
    (
        DOCS_README,
        _DOCS_README_AGENTS_TABLE_FRAGMENTS,
    ),
    (
        _MERGE,
        _REPO_GATES_MDC_FRAGMENTS,
    ),
)


class TestAgentsDocAnchors(unittest.TestCase):
    def test_agents_has_stable_html_anchors(self) -> None:
        text = AGENTS.read_text(encoding="utf-8")
        for aid in _REQUIRED_AGENTS_ANCHORS:
            needle = f'<a id="{aid}"></a>'
            self.assertIn(
                needle,
                text,
                f"Missing stable anchor {needle!r} in {AGENTS.relative_to(REPO_ROOT)}",
            )

    def test_merge_checklist_links_agents_pre_merge_for_merge_ready_row(self) -> None:
        body = _MERGE.read_text(encoding="utf-8")
        self.assertIn(
            "AGENTS.md#agents-pre-merge",
            body,
            f"{_MERGE.relative_to(REPO_ROOT)} merge-ready row should deep-link "
            "#agents-pre-merge",
        )

    def test_merge_doc_index_agents_gate_row_links_core_fragments(self) -> None:
        body = _MERGE.read_text(encoding="utf-8")
        for aid in _MERGE_AGENTS_GATE_ROW_FRAGMENTS:
            frag = f"AGENTS.md#{aid}"
            with self.subTest(fragment=frag):
                self.assertIn(
                    frag,
                    body,
                    f"{_MERGE.relative_to(REPO_ROOT)} §4 自动化助手闸门行应含 {frag!r}",
                )

    def test_hub_docs_intros_contain_agents_deep_links(self) -> None:
        for path, frags in _HUB_DOCS_AGENTS_FRAGMENTS:
            body = path.read_text(encoding="utf-8")
            for frag in frags:
                with self.subTest(path=str(path.relative_to(REPO_ROOT)), fragment=frag):
                    self.assertIn(
                        frag,
                        body,
                        f"{path.relative_to(REPO_ROOT)} 应含 AGENTS 深链 {frag!r}",
                    )

    def test_docs_readme_agents_row_links_arch_boundary_and_reader_conventions(
        self,
    ) -> None:
        body = DOCS_README.read_text(encoding="utf-8")
        for frag in _DOCS_README_AGENTS_TABLE_FRAGMENTS:
            with self.subTest(fragment=frag):
                self.assertIn(
                    frag,
                    body,
                    f"{DOCS_README.relative_to(REPO_ROOT)} 维护者表 AGENTS 行应含 {frag!r}",
                )

    def test_no_agents_markdown_or_href_without_fragment(self) -> None:
        offenders = collect_doc_link_offenders(REPO_ROOT, "AGENTS")
        self.assertEqual(
            offenders,
            [],
            "Found AGENTS.md links missing URL fragment "
            f"(use #agents-contract): {offenders!r}",
        )


if __name__ == "__main__":
    unittest.main()
