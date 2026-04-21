"""Regression tests for docs/EVOLUTION_RUNBOOK.md HTML anchors.

Stable ids avoid reliance on GitHub heading slug rules (especially for
non-ASCII titles). Several docs deep-link #accelerate and #sqlite-sidecar.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EVOLUTION = REPO_ROOT / "docs" / "EVOLUTION_RUNBOOK.md"

_REQUIRED_ANCHORS = (
    "github-actions-cadence",
    "pr-evidence-triad",
    "accelerate",
    "sqlite-sidecar",
    "continuous-push",
)

_MUST_LINK_ACCELERATE = (
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "docs" / "DATA_CONTRACTS.md",
    REPO_ROOT / "docs" / "MERGE_AND_RELEASE_CHECKLIST.md",
    REPO_ROOT / "docs" / "PLATFORM_MASTER_MAP_AND_INVOCATION.md",
    REPO_ROOT / "docs" / "schemas" / "README.md",
    REPO_ROOT / "docs" / "SITE_DATA_UPDATE_FRAMEWORK.md",
    REPO_ROOT / "docs" / "DATA_ANALYSIS_SITE_CONTENT_SYNC.md",
    REPO_ROOT / "docs" / "TECH_ARCHITECTURE_CAPABILITIES.md",
)

_MUST_LINK_SQLITE_SIDECAR = (
    REPO_ROOT / "docs" / "DATA_CONTRACTS.md",
    REPO_ROOT / "docs" / "ARCHITECTURE_ONE_PAGER.md",
    REPO_ROOT / "docs" / "DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md",
)

_MUST_LINK_GITHUB_ACTIONS_CADENCE = (
    REPO_ROOT / "docs" / "INTEL_AND_POLICY_TRACKING_PLAYBOOK.md",
)


class TestEvolutionRunbookDocAnchors(unittest.TestCase):
    def test_evolution_runbook_has_stable_html_anchors(self) -> None:
        text = EVOLUTION.read_text(encoding="utf-8")
        for aid in _REQUIRED_ANCHORS:
            needle = f'<a id="{aid}"></a>'
            self.assertIn(
                needle,
                text,
                f"Missing stable anchor {needle!r} in {EVOLUTION.relative_to(REPO_ROOT)}",
            )

    def test_key_docs_link_accelerate_fragment(self) -> None:
        fragment = "#accelerate"
        for path in _MUST_LINK_ACCELERATE:
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                self.assertTrue(path.is_file(), f"Missing file: {path}")
                body = path.read_text(encoding="utf-8")
                self.assertIn(
                    fragment,
                    body,
                    f"{path.relative_to(REPO_ROOT)} should deep-link {fragment!r}",
                )

    def test_key_docs_link_sqlite_sidecar_fragment(self) -> None:
        fragment = "#sqlite-sidecar"
        for path in _MUST_LINK_SQLITE_SIDECAR:
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                self.assertTrue(path.is_file(), f"Missing file: {path}")
                body = path.read_text(encoding="utf-8")
                self.assertIn(
                    fragment,
                    body,
                    f"{path.relative_to(REPO_ROOT)} should deep-link {fragment!r}",
                )

    def test_evolution_runbook_links_merge_partials_sequence(self) -> None:
        body = EVOLUTION.read_text(encoding="utf-8")
        self.assertIn(
            "MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence",
            body,
            "EVOLUTION_RUNBOOK 合并前段落应对读 MERGE partials 手顺",
        )

    def test_intel_playbook_links_github_actions_cadence(self) -> None:
        fragment = "EVOLUTION_RUNBOOK.md#github-actions-cadence"
        intel = _MUST_LINK_GITHUB_ACTIONS_CADENCE[0]
        body = intel.read_text(encoding="utf-8")
        self.assertIn(
            fragment,
            body,
            f"{intel.relative_to(REPO_ROOT)} should link {fragment!r}",
        )


if __name__ == "__main__":
    unittest.main()
