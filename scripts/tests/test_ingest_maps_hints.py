"""ingest maps_to 预填逻辑回归。"""
from __future__ import annotations

import unittest

from evolution_pkg.ingest_maps import merge_maps_to_hints


class TestMergeMapsToHints(unittest.TestCase):
    def test_host_suffix(self) -> None:
        cfg = {
            "host_suffixes": {
                "github.blog": {
                    "pages": ["model.html"],
                    "lab_factors": ["ai"],
                }
            }
        }
        lf, pg = merge_maps_to_hints(
            "https://github.blog/2024/foo",
            "Title",
            "",
            [],
            [],
            cfg,
        )
        self.assertIn("model.html", pg)
        self.assertIn("ai", lf)

    def test_keyword_route(self) -> None:
        cfg = {
            "keyword_routes": [
                {
                    "match": "Kubernetes",
                    "pages": ["architecture.html"],
                    "lab_factors": [],
                }
            ]
        }
        lf, pg = merge_maps_to_hints("", "We use Kubernetes", "", [], [], cfg)
        self.assertIn("architecture.html", pg)


if __name__ == "__main__":
    unittest.main()
