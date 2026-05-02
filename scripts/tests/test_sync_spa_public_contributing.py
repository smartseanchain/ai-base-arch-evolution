"""sync_spa_public 须将根目录 CONTRIBUTING.md 写入 spa/public（壳层 SpaLayout 深链）。"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class TestSyncSpaPublicContributing(unittest.TestCase):
    def test_script_copies_contributing_to_spa_public(self) -> None:
        root = Path(__file__).resolve().parents[2]
        contrib = root / "CONTRIBUTING.md"
        self.assertTrue(contrib.is_file(), msg="仓库根须有 CONTRIBUTING.md")
        r = subprocess.run(
            [sys.executable, str(root / "scripts" / "sync_spa_public.py")],
            cwd=str(root),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, msg=r.stderr or r.stdout)
        out = root / "spa" / "public" / "CONTRIBUTING.md"
        self.assertTrue(out.is_file(), msg="sync 后 spa/public/CONTRIBUTING.md 须存在")
        self.assertGreater(out.stat().st_size, 100, msg="CONTRIBUTING 副本不应为空")
        self.assertEqual(
            out.read_text(encoding="utf-8"),
            contrib.read_text(encoding="utf-8"),
            msg="sync_spa_public 须逐字复制根目录 CONTRIBUTING.md",
        )

    def test_spa_public_contributing_matches_root_when_present(self) -> None:
        """工作区已有副本时须与根一致（改 CONTRIBUTING 后须 spa-sync，见 MERGE / CONTRIBUTING）。"""
        root = Path(__file__).resolve().parents[2]
        src = root / "CONTRIBUTING.md"
        dst = root / "spa" / "public" / "CONTRIBUTING.md"
        if not dst.is_file():
            return
        self.assertEqual(
            dst.read_text(encoding="utf-8"),
            src.read_text(encoding="utf-8"),
            msg="spa/public/CONTRIBUTING.md 与根 CONTRIBUTING.md 不一致；请执行 "
            "`python3 scripts/sync_spa_public.py` 或 `make spa-sync`",
        )


if __name__ == "__main__":
    unittest.main()
