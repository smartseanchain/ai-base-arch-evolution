"""Regression tests for docs/MERGE_AND_RELEASE_CHECKLIST.md HTML anchors.

#pre-merge is the primary merge-ready entry; many hub docs deep-link it.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from doc_link_fragment_scan import collect_doc_link_offenders

REPO_ROOT = Path(__file__).resolve().parents[2]
MERGE = REPO_ROOT / "docs" / "MERGE_AND_RELEASE_CHECKLIST.md"

_REQUIRED_ANCHORS = (
    "pre-merge",
    "pre-merge-partials-sequence",
    "release-pass",
    "integration-hint",
    "doc-index",
)

_MUST_LINK_PRE_MERGE = (
    REPO_ROOT / "maintainer-hub.html",
    REPO_ROOT / "README.md",
    REPO_ROOT / "CONTRIBUTING.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "docs" / "ARCHITECTURE_ONE_PAGER.md",
    REPO_ROOT / "docs" / "EVOLUTION_RUNBOOK.md",
    REPO_ROOT / "docs" / "INTEGRATION_AND_READONLY_API.md",
    REPO_ROOT / "docs" / "PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md",
    REPO_ROOT / "docs" / "INTELLIGENCE_SIX_DOMAINS.md",
    REPO_ROOT / "docs" / "ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md",
    REPO_ROOT / "docs" / "PLATFORM_CAPABILITY_MAP.md",
    REPO_ROOT / "docs" / "DATA_CONTRACTS.md",
    REPO_ROOT / "docs" / "PLATFORM_MASTER_MAP_AND_INVOCATION.md",
    REPO_ROOT / "docs" / "PROJECT_ARCHITECTURE_OVERVIEW.md",
    REPO_ROOT / "scripts" / "README.md",
    REPO_ROOT / "spa" / "README.md",
    REPO_ROOT / ".cursor" / "rules" / "repo-gates.mdc",
)

_MUST_LINK_DOC_INDEX = (REPO_ROOT / "docs" / "PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md",)

# PR 模板与 Cursor 子规则须显式链 MERGE「partials / 404 / spa-sync」手顺，避免只记 #pre-merge 而漏失页与壳同步。
_MUST_ANCHOR_MERGE_PARTIALS_SEQUENCE = (
    REPO_ROOT / ".github" / "pull_request_template.md",
    REPO_ROOT / ".cursor" / "rules" / "repo-gates.mdc",
    REPO_ROOT / ".cursor" / "rules" / "spa-nav-config.mdc",
    REPO_ROOT / ".cursor" / "rules" / "spa-nav-registry.mdc",
    REPO_ROOT / ".cursor" / "rules" / "evolution-registry.mdc",
    REPO_ROOT / "maintainer-hub.html",
    REPO_ROOT / "404.html",
    REPO_ROOT / "admin-console" / "static" / "index.html",
    REPO_ROOT / "admin-console" / "app" / "main.py",
    REPO_ROOT / "Makefile",
    REPO_ROOT / "scripts" / "run_validate.sh",
    REPO_ROOT / "scripts" / "run_validate_fast.sh",
    REPO_ROOT / "scripts" / "check_nav_links_registry.py",
    REPO_ROOT / "scripts" / "gen_nav_links_ts.py",
    REPO_ROOT / "scripts" / "merge_candidates_to_manifest.py",
    REPO_ROOT / "scripts" / "readonly_api.py",
    REPO_ROOT / "scripts" / "run_pipeline_steps.py",
    REPO_ROOT / "scripts" / "evolution_pkg" / "candidate_merge.py",
    REPO_ROOT / "scripts" / "evolution_pkg" / "io.py",
    REPO_ROOT / "scripts" / "evolution_pkg" / "nav_links.py",
    REPO_ROOT / "scripts" / "sync_site_nav.py",
    REPO_ROOT / "scripts" / "evolution_pkg" / "spa_nav.py",
    REPO_ROOT / "docker-compose.yml",
    REPO_ROOT / "docker-compose.dev.yml",
    REPO_ROOT / ".github" / "workflows" / "ci.yml",
    REPO_ROOT / ".github" / "workflows" / "ingest-pipeline.yml",
    REPO_ROOT / ".github" / "workflows" / "pr-candidates.yml",
    REPO_ROOT / ".github" / "workflows" / "update-pipeline.yml",
    REPO_ROOT / ".githooks" / "pre-commit",
    REPO_ROOT / "scripts" / "install-git-hooks.sh",
    REPO_ROOT / "docs" / "ORCHESTRATION_AND_EVENT_STREAMING.md",
    REPO_ROOT / "docs" / "DOCKER.md",
    REPO_ROOT / "docs" / "INCREMENTAL_BUILD_PLAYBOOK.md",
    REPO_ROOT / "docs" / "ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md",
    REPO_ROOT / "docs" / "templates" / "incremental-pr-slice.md",
    REPO_ROOT / "assets" / "MOTION-ARCHITECTURE.md",
    REPO_ROOT / "spa" / "package.json",
    REPO_ROOT / "admin-console" / "data" / "control_plane_roadmap.json",
)

# Markdown / YAML 等里「…CHECKLIST.md + 闭括号」且中间无 # 表示链接无 fragment（GitHub 无法跳到 §1）。
# 源码勿写 contiguous 违禁串，否则本文件会被全仓扫描命中。
_MERGE_LINK_MISSING_FRAGMENT = "MERGE_AND_RELEASE_CHECKLIST" + ".md)"
# HTML / 部分 JSON：`href="…CHECKLIST.md"` 无 #fragment。
_MERGE_HREF_MISSING_FRAGMENT = "MERGE_AND_RELEASE_CHECKLIST" + '.md"'
_MERGE_HREF_MISSING_SINGLE_FRAGMENT = "MERGE_AND_RELEASE_CHECKLIST" + ".md'"
_SKIP_DIR_NAMES = frozenset(
    {".git", "node_modules", "__pycache__", ".venv", "venv", "dist"},
)
_SCAN_SUFFIXES = frozenset({".md", ".mdc", ".yaml", ".yml", ".json", ".html"})


class TestMergeChecklistDocAnchors(unittest.TestCase):
    def test_merge_checklist_has_stable_html_anchors(self) -> None:
        text = MERGE.read_text(encoding="utf-8")
        for aid in _REQUIRED_ANCHORS:
            needle = f'<a id="{aid}"></a>'
            self.assertIn(
                needle,
                text,
                f"Missing stable anchor {needle!r} in {MERGE.relative_to(REPO_ROOT)}",
            )

    def test_key_docs_link_pre_merge_fragment(self) -> None:
        fragment = "#pre-merge"
        for path in _MUST_LINK_PRE_MERGE:
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                self.assertTrue(path.is_file(), f"Missing file: {path}")
                body = path.read_text(encoding="utf-8")
                self.assertIn(
                    fragment,
                    body,
                    f"{path.relative_to(REPO_ROOT)} should deep-link {fragment!r}",
                )

    def test_pr_template_and_cursor_rules_anchor_merge_partials_sequence(self) -> None:
        needle = "pre-merge-partials-sequence"
        for path in _MUST_ANCHOR_MERGE_PARTIALS_SEQUENCE:
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                self.assertTrue(path.is_file(), f"Missing file: {path}")
                body = path.read_text(encoding="utf-8")
                self.assertIn(
                    needle,
                    body,
                    f"{path.relative_to(REPO_ROOT)} should reference MERGE {needle!r}",
                )

    def test_platform_extensibility_links_doc_index(self) -> None:
        fragment = "MERGE_AND_RELEASE_CHECKLIST.md#doc-index"
        path = _MUST_LINK_DOC_INDEX[0]
        body = path.read_text(encoding="utf-8")
        self.assertIn(
            fragment,
            body,
            f"{path.relative_to(REPO_ROOT)} should link {fragment!r}",
        )

    def test_role_opener_docs_link_invariants_and_contributing_triad(self) -> None:
        inv = "#architect-invariants-index"
        five = "#contributing-five-minute"
        pr_triad = "#contributing-pr-evidence-triad"
        cmd = "#contributing-change-to-command"
        for relpath in (
            "CONTRIBUTING.md",
            "docs/README.md",
            "docs/DATA_CONTRACTS.md",
            "docs/EVOLUTION_RUNBOOK.md",
            "docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md",
            "docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md",
            "docs/MERGE_AND_RELEASE_CHECKLIST.md",
            "docs/PROJECT_ARCHITECTURE_OVERVIEW.md",
            "docs/ARCHITECTURE.md",
            "docs/ARCHITECTURE_ONE_PAGER.md",
            "docs/INTEGRATION_AND_READONLY_API.md",
            "docs/INCREMENTAL_BUILD_PLAYBOOK.md",
            "docs/templates/incremental-pr-slice.md",
            "spa/README.md",
        ):
            with self.subTest(doc=relpath):
                body = (REPO_ROOT / relpath).read_text(encoding="utf-8")
                self.assertIn(
                    inv,
                    body,
                    f"{relpath} 文首判型链应含 ONE_PAGER{inv}",
                )
                self.assertIn(
                    pr_triad,
                    body,
                    f"{relpath} 文首判型链应含 CONTRIBUTING{pr_triad}",
                )
                self.assertIn(
                    five,
                    body,
                    f"{relpath} 文首判型链应含 CONTRIBUTING{five}",
                )
                self.assertIn(
                    cmd,
                    body,
                    f"{relpath} 文首判型链应含 CONTRIBUTING{cmd}",
                )

    def test_no_merge_checklist_markdown_link_without_fragment(self) -> None:
        offenders = collect_doc_link_offenders(
            REPO_ROOT,
            "MERGE_AND_RELEASE_CHECKLIST",
        )
        self.assertEqual(
            offenders,
            [],
            "Found MERGE_AND_RELEASE_CHECKLIST.md links missing URL fragment "
            f"(use #pre-merge or #doc-index): {offenders!r}",
        )


if __name__ == "__main__":
    unittest.main()
