"""doc_link_fragment_scan 契约：违禁子串拼装与全仓扫描入口。"""

from __future__ import annotations

import unittest
from pathlib import Path

from doc_link_fragment_scan import collect_doc_link_offenders, link_fragments_missing_hash

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestDocLinkFragmentScan(unittest.TestCase):
    def test_link_fragments_suffix_shapes(self) -> None:
        stem = "AGENT" + "S"
        md, dq, sq = link_fragments_missing_hash(stem)
        self.assertEqual(md, stem + ".md)")
        self.assertEqual(dq, stem + '.md"')
        self.assertEqual(sq, stem + ".md'")

    def test_collect_offenders_unknown_stem_empty(self) -> None:
        offenders = collect_doc_link_offenders(
            REPO_ROOT,
            "__NO_SUCH_DOC_STEM_XYZ__",
        )
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
