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

    def test_same_group_name_non_contiguous_splits(self) -> None:
        """同名 group 被无 group 条目隔开时须拆成两组（与顶栏连续 details 语义一致）。"""
        rows = [
            {"page": "a.html", "label": "A", "group": "分区"},
            {"page": "solo.html", "label": "独链", "group": None},
            {"page": "b.html", "label": "B", "group": "分区"},
            {"page": "c.html", "label": "C", "group": "分区"},
        ]
        g = build_nav_groups(rows)
        self.assertEqual(
            g,
            [
                ("分区", [("a.html", "A")]),
                (None, [("solo.html", "独链")]),
                ("分区", [("b.html", "B"), ("c.html", "C")]),
            ],
        )


if __name__ == "__main__":
    unittest.main()
