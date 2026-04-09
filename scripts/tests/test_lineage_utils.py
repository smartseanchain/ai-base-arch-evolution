"""lineage_utils：run 块结构。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lineage_utils import build_run_block, get_repo_revision_short  # noqa: E402


class TestLineageUtils(unittest.TestCase):
    def test_repo_revision_non_empty(self) -> None:
        r = get_repo_revision_short()
        self.assertIsInstance(r, str)
        self.assertTrue(r.strip())

    def test_build_run_block_keys(self) -> None:
        b = build_run_block()
        self.assertIn("run_id", b)
        self.assertIn("repo_revision", b)
        self.assertIsInstance(b["run_id"], str)
        self.assertGreater(len(b["run_id"]), 8)
        self.assertIsInstance(b["repo_revision"], str)


if __name__ == "__main__":
    unittest.main()
