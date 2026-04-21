"""Stable HTML anchors in CONTRIBUTING.md and maintainer-hub deep links."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from doc_link_fragment_scan import collect_doc_link_offenders

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
MAINTAINER_HUB = REPO_ROOT / "maintainer-hub.html"
INDEX_HTML = REPO_ROOT / "index.html"
ANALYSIS_HUB = REPO_ROOT / "analysis-hub.html"

_REQUIRED_CONTRIBUTING_ANCHORS = (
    "contributing-env-and-cmd",
    "contributing-common-changes-checklist",
    "contributing-terminology",
    "contributing-pr-evidence-triad",
    "maintainer-reading-order",
)

class TestContributingDocAnchors(unittest.TestCase):
    def test_contributing_has_stable_html_anchors(self) -> None:
        text = CONTRIBUTING.read_text(encoding="utf-8")
        for aid in _REQUIRED_CONTRIBUTING_ANCHORS:
            needle = f'<a id="{aid}"></a>'
            self.assertIn(
                needle,
                text,
                f"Missing stable anchor {needle!r} in {CONTRIBUTING.relative_to(REPO_ROOT)}",
            )

    def test_maintainer_hub_links_contributing_env_section(self) -> None:
        fragment = "CONTRIBUTING.md#contributing-env-and-cmd"
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        self.assertGreaterEqual(
            body.count(fragment),
            2,
            f"{MAINTAINER_HUB.relative_to(REPO_ROOT)} should link {fragment!r} at least twice",
        )

    def test_maintainer_hub_links_invariants_index_pr_triad_partials_sequence(
        self,
    ) -> None:
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        for frag in (
            "ARCHITECTURE_ONE_PAGER.md#architect-invariants-index",
            "CONTRIBUTING.md#contributing-pr-evidence-triad",
            "MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence",
        ):
            with self.subTest(fragment=frag):
                self.assertIn(
                    frag,
                    body,
                    f"{MAINTAINER_HUB.relative_to(REPO_ROOT)} should link {frag!r}",
                )

    def test_index_html_links_invariants_index_and_pr_triad(self) -> None:
        body = INDEX_HTML.read_text(encoding="utf-8")
        for frag in (
            "docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index",
            "CONTRIBUTING.md#contributing-pr-evidence-triad",
        ):
            with self.subTest(fragment=frag):
                self.assertGreaterEqual(
                    body.count(frag),
                    2,
                    f"{INDEX_HTML.relative_to(REPO_ROOT)} should link {frag!r} "
                    "at least twice (kicker + read-guide / 分区脚)",
                )

    def test_analysis_hub_html_links_invariants_index_and_pr_triad(self) -> None:
        body = ANALYSIS_HUB.read_text(encoding="utf-8")
        for frag in (
            "docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index",
            "CONTRIBUTING.md#contributing-pr-evidence-triad",
        ):
            with self.subTest(fragment=frag):
                self.assertGreaterEqual(
                    body.count(frag),
                    2,
                    f"{ANALYSIS_HUB.relative_to(REPO_ROOT)} should link {frag!r} "
                    "at least twice (note-kicker + 架构与读数总线)",
                )

    def test_maintainer_hub_docs_readme_hrefs_have_url_fragments(self) -> None:
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        for m in re.finditer(r'href="(docs/README\.md[^"]*)"', body):
            url = m.group(1)
            self.assertIn(
                "#",
                url,
                f"{MAINTAINER_HUB.relative_to(REPO_ROOT)}: docs/README link missing "
                f"URL fragment: href={url!r}",
            )

    def test_maintainer_hub_hrefs_to_docs_markdown_have_url_fragments(self) -> None:
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        for m in re.finditer(r'href="(docs/[^"]+\.md[^"]*)"', body):
            url = m.group(1)
            self.assertIn(
                "#",
                url,
                f"{MAINTAINER_HUB.relative_to(REPO_ROOT)}: docs/*.md link missing "
                f"URL fragment: href={url!r}",
            )

    def test_no_contributing_markdown_or_href_without_fragment(self) -> None:
        offenders = collect_doc_link_offenders(REPO_ROOT, "CONTRIBUTING")
        self.assertEqual(
            offenders,
            [],
            "Found CONTRIBUTING.md links missing URL fragment "
            f"(use #contributing-env-and-cmd, #contributing-terminology, etc.): {offenders!r}",
        )


if __name__ == "__main__":
    unittest.main()
