"""Regression tests for INTEL_AND_POLICY_TRACKING_PLAYBOOK.md HTML anchors.

Many docs deep-link to #intel-source-tiers (§2 / 2a). Renaming or removing
anchors breaks those links without failing markdown builds.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INTEL = REPO_ROOT / "docs" / "INTEL_AND_POLICY_TRACKING_PLAYBOOK.md"

_REQUIRED_ANCHORS = (
    "intel-purpose",
    "intel-source-tiers",
    "intel-social-platforms",
    "intel-workflow",
    "intel-cadence",
    "intel-metadata",
    "intel-personal",
    "intel-links",
)

_MUST_LINK_INTEL_SOURCE_TIERS = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "CONTRIBUTING.md",
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "docs" / "MERGE_AND_RELEASE_CHECKLIST.md",
    REPO_ROOT / "scripts" / "README.md",
)


class TestIntelPlaybookDocAnchors(unittest.TestCase):
    def test_intel_playbook_has_stable_html_anchors(self) -> None:
        text = INTEL.read_text(encoding="utf-8")
        for aid in _REQUIRED_ANCHORS:
            needle = f'<a id="{aid}"></a>'
            self.assertIn(
                needle,
                text,
                f"Missing stable anchor {needle!r} in {INTEL.relative_to(REPO_ROOT)}",
            )

    def test_key_docs_link_intel_source_tiers_fragment(self) -> None:
        fragment = "#intel-source-tiers"
        for path in _MUST_LINK_INTEL_SOURCE_TIERS:
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                self.assertTrue(path.is_file(), f"Missing file: {path}")
                body = path.read_text(encoding="utf-8")
                self.assertIn(
                    fragment,
                    body,
                    f"{path.relative_to(REPO_ROOT)} should deep-link {fragment!r}",
                )

    def test_key_docs_link_intel_social_platforms_fragment(self) -> None:
        fragment = "#intel-social-platforms"
        for path in _MUST_LINK_INTEL_SOURCE_TIERS:
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                body = path.read_text(encoding="utf-8")
                self.assertIn(
                    fragment,
                    body,
                    f"{path.relative_to(REPO_ROOT)} should deep-link {fragment!r} "
                    "(INTEL §2b 微博/站内流)",
                )

    def test_intel_links_pre_merge_partials_sequence(self) -> None:
        body = INTEL.read_text(encoding="utf-8")
        self.assertIn(
            "MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence",
            body,
            "INTEL 文首 MPA/SPA 与顶栏段落应对读 MERGE partials 手顺锚点",
        )

    def test_intel_playbook_links_agents_invariants_and_pre_merge(self) -> None:
        body = INTEL.read_text(encoding="utf-8")
        self.assertIn(
            "AGENTS.md#agents-content-framework",
            body,
            "INTEL §7 table should deep-link AGENTS content-framework / 0c entry",
        )
        self.assertIn(
            "AGENTS.md#agents-invariants",
            body,
            "INTEL workflow/index should deep-link AGENTS manifest review gate",
        )
        self.assertIn(
            "AGENTS.md#agents-pre-merge",
            body,
            "INTEL §7 table should deep-link AGENTS pre-merge gate",
        )
        self.assertIn(
            "AGENTS.md#agents-hub-lead",
            body,
            "INTEL §7 table should deep-link AGENTS hub lead/read-hint gate",
        )
        self.assertIn(
            "AGENTS.md#agents-test-subset",
            body,
            "INTEL §7 table should deep-link AGENTS make-test subset",
        )
        self.assertIn(
            "AGENTS.md#agents-arch-boundary",
            body,
            "INTEL §7 table should deep-link AGENTS analysis/HTML boundary",
        )
        self.assertIn(
            "AGENTS.md#agents-reader-conventions",
            body,
            "INTEL §7 table should deep-link AGENTS reader/deep-link conventions",
        )
        self.assertIn(
            "AGENTS.md#agents-deep-read",
            body,
            "INTEL §7 table should deep-link AGENTS deep-read index",
        )
        self.assertIn(
            "AGENTS.md#agents-cursor-rules",
            body,
            "INTEL §7 table should deep-link AGENTS Cursor rule mapping",
        )


if __name__ == "__main__":
    unittest.main()
