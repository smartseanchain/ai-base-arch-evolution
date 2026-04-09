"""assets/site-meta.json 契约（站点发布版本）。"""
from __future__ import annotations

import json
import unittest

from evolution_pkg.io import REPO_ROOT

SITE_META = REPO_ROOT / "assets" / "site-meta.json"


class TestSiteMeta(unittest.TestCase):
    def test_site_meta_exists_and_shape(self) -> None:
        self.assertTrue(SITE_META.is_file(), msg="缺少 assets/site-meta.json")
        data = json.loads(SITE_META.read_text(encoding="utf-8"))
        self.assertEqual(data.get("schema_version"), 1)
        ver = data.get("site_version")
        self.assertIsInstance(ver, str)
        self.assertTrue(ver.strip(), msg="site_version 非空")


if __name__ == "__main__":
    unittest.main()
