"""check_skip_bar_404 与仓库 partials/404 一致时须通过。"""
from __future__ import annotations

import sys
import unittest

from evolution_pkg.io import REPO_ROOT

SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_skip_bar_404 import main  # noqa: E402


class TestCheckSkipBar404(unittest.TestCase):
    def test_main_ok_on_repo(self) -> None:
        self.assertEqual(main(quiet=True), 0)


if __name__ == "__main__":
    unittest.main()
