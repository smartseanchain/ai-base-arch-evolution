"""evolution_pkg.spa_nav · build_nav_groups（顶栏分组）。"""
from __future__ import annotations

import unittest

from evolution_pkg.spa_nav import build_nav_groups


class TestBuildNavGroups(unittest.TestCase):
    def test_standalone_then_group(self) -> None:
        rows = [
            {"page": "index.html", "label": "总览", "group": None},
            {"page": "nexus.html", "label": "立体联结", "group": "联结与模型"},
            {"page": "model.html", "label": "分层模型", "group": "联结与模型"},
        ]
        g = build_nav_groups(rows)
        self.assertEqual(
            g,
            [
                (None, [("index.html", "总览")]),
                ("联结与模型", [("nexus.html", "立体联结"), ("model.html", "分层模型")]),
            ],
        )

    def test_two_standalone(self) -> None:
        rows = [
            {"page": "index.html", "label": "总览", "group": None},
            {"page": "maintainer-hub.html", "label": "维护导读", "group": None},
        ]
        g = build_nav_groups(rows)
        self.assertEqual(
            g,
            [
                (None, [("index.html", "总览")]),
                (None, [("maintainer-hub.html", "维护导读")]),
            ],
        )


if __name__ == "__main__":
    unittest.main()
