"""注册表与 lab.js / gen-sitemap 一致性（轻量自检）。"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest

from evolution_pkg.io import REGISTRY_JSON_PATH, REPO_ROOT

REGISTRY = REGISTRY_JSON_PATH
LAB = REPO_ROOT / "assets" / "lab.js"
GEN_SITEMAP = REPO_ROOT / "scripts" / "gen-sitemap.py"


class TestRegistry(unittest.TestCase):
    def test_lab_js_matches_registry_factors(self) -> None:
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        reg_fac = set(reg["lab_factors"])
        text = LAB.read_text(encoding="utf-8")
        js_fac = set(
            re.findall(r'^\s+id:\s*"([a-z0-9_]+)"', text, re.MULTILINE)
        )
        self.assertEqual(reg_fac, js_fac)

    def test_registry_pages_exist(self) -> None:
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        for p in reg["pages"]:
            self.assertTrue((REPO_ROOT / p).is_file(), msg=p)

    def test_registry_pages_have_round_extension_card(self) -> None:
        """注册内分页须含「推演扩展 · 本轮更新」卡片，防漏插或漂移。"""
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        for p in reg["pages"]:
            text = (REPO_ROOT / p).read_text(encoding="utf-8")
            self.assertIn("site-round-extension", text, msg=p)
            self.assertIn("ext-round-", text, msg=p)

    def test_priority_subset_registry(self) -> None:
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        reg_pages = set(reg["pages"])
        spec = importlib.util.spec_from_file_location("_gsm", GEN_SITEMAP)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k in mod.PRIORITY:
            self.assertIn(k, reg_pages, msg=k)


if __name__ == "__main__":
    unittest.main()
