"""注册表与 lab.js / gen-sitemap 一致性（轻量自检）。"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "scripts" / "evolution-registry.json"
LAB = ROOT / "assets" / "lab.js"
GEN_SITEMAP = ROOT / "scripts" / "gen-sitemap.py"


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
            self.assertTrue((ROOT / p).is_file(), msg=p)

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
