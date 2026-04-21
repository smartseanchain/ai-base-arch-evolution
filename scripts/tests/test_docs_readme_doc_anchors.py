"""docs/README.md 深链须带 URL fragment（与 docs/README 文首 #content-framework 对齐）。"""

from __future__ import annotations

import unittest
from pathlib import Path

from doc_link_fragment_scan import collect_doc_link_offenders

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestDocsReadmeDocAnchors(unittest.TestCase):
    def test_no_docs_readme_markdown_or_href_without_fragment(self) -> None:
        offenders = collect_doc_link_offenders(REPO_ROOT, "docs/README")
        self.assertEqual(
            offenders,
            [],
            "Found docs/README.md links missing URL fragment "
            f"(use #content-framework, #quick-paths, etc.): {offenders!r}",
        )


if __name__ == "__main__":
    unittest.main()
