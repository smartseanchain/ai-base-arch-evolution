"""evolution_pkg 包与 evolution_io 兼容层。"""
from __future__ import annotations

import unittest

from evolution_io import REPO_ROOT as ROOT_SHIM, load_json as load_shim
from evolution_pkg.io import REPO_ROOT, load_json


class TestEvolutionPkg(unittest.TestCase):
    def test_repo_root_matches_shim(self) -> None:
        self.assertEqual(REPO_ROOT.resolve(), ROOT_SHIM.resolve())

    def test_registry_present(self) -> None:
        reg = REPO_ROOT / "scripts" / "evolution-registry.json"
        self.assertTrue(reg.is_file(), msg="REPO_ROOT 应指向仓库根")

    def test_load_json_missing(self) -> None:
        p = REPO_ROOT / "no-such-file-xyz.json"
        self.assertEqual(load_json(p), {})
        self.assertEqual(load_shim(p), {})


if __name__ == "__main__":
    unittest.main()
