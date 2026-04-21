"""evolution_pkg 包与 evolution_io 兼容层。"""
from __future__ import annotations

import unittest

from evolution_io import REPO_ROOT as ROOT_SHIM, load_json as load_shim
from evolution_pkg.domains import (
    DOMAIN_LABEL_ZH,
    SUBMODULE_DOMAIN,
    IntelligenceDomain,
    evolution_pkg_submodule_names,
)
from evolution_pkg.io import (
    INGEST_CONFIG_JSON_PATH,
    INGEST_CONFIG_JSON_RELPOS,
    MAPS_TO_HINTS_JSON_PATH,
    MAPS_TO_HINTS_JSON_RELPOS,
    REGISTRY_JSON_PATH,
    REGISTRY_JSON_RELPOS,
    REPO_ROOT,
    load_json,
    load_registry_allowed_sets,
)


class TestEvolutionPkg(unittest.TestCase):
    def test_repo_root_matches_shim(self) -> None:
        self.assertEqual(REPO_ROOT.resolve(), ROOT_SHIM.resolve())

    def test_registry_json_path_matches_relpos(self) -> None:
        self.assertEqual(REGISTRY_JSON_PATH, REPO_ROOT / REGISTRY_JSON_RELPOS)
        self.assertNotIn("\\", REGISTRY_JSON_RELPOS)

    def test_ingest_and_hints_paths_match_relpos(self) -> None:
        self.assertEqual(INGEST_CONFIG_JSON_PATH, REPO_ROOT / INGEST_CONFIG_JSON_RELPOS)
        self.assertEqual(MAPS_TO_HINTS_JSON_PATH, REPO_ROOT / MAPS_TO_HINTS_JSON_RELPOS)
        self.assertTrue(INGEST_CONFIG_JSON_PATH.is_file())
        self.assertTrue(MAPS_TO_HINTS_JSON_PATH.is_file())

    def test_registry_present(self) -> None:
        self.assertTrue(REGISTRY_JSON_PATH.is_file(), msg="REPO_ROOT 应指向仓库根")

    def test_load_json_missing(self) -> None:
        p = REPO_ROOT / "no-such-file-xyz.json"
        self.assertEqual(load_json(p), {})
        self.assertEqual(load_shim(p), {})

    def test_load_registry_allowed_sets(self) -> None:
        pages, factors = load_registry_allowed_sets()
        self.assertGreater(len(pages), 0)
        self.assertGreater(len(factors), 0)
        self.assertIn("index.html", pages)
        self.assertIn("reg", factors)

    def test_analysis_snapshot_history_module_loads(self) -> None:
        from evolution_pkg import analysis_snapshot_history as ash

        n = ash.count_rows()
        self.assertIsInstance(n, int)
        self.assertGreaterEqual(n, 0)
        rows = ash.list_meta(limit=3, offset=0)
        self.assertIsInstance(rows, list)

    def test_evolution_pkg_submodules_have_domain(self) -> None:
        """新增 evolution_pkg 子模块须在 domains.SUBMODULE_DOMAIN 登记。"""
        names = evolution_pkg_submodule_names()
        self.assertEqual(names, frozenset(SUBMODULE_DOMAIN), msg=names ^ frozenset(SUBMODULE_DOMAIN))

    def test_domain_labels_cover_all_domains(self) -> None:
        self.assertEqual(set(DOMAIN_LABEL_ZH), set(IntelligenceDomain))


if __name__ == "__main__":
    unittest.main()
