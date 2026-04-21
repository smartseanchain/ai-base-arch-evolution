"""流水线遥测 ``input_artifacts`` 指纹（与 ``runner._input_artifact_hashes`` 对齐）。"""
from __future__ import annotations

import unittest
from pathlib import Path

from evolution_pkg.io import REPO_ROOT
from evolution_pkg.pipeline.runner import _input_artifact_hashes


class TestInputArtifactHashes(unittest.TestCase):
    def test_manifest_shape(self) -> None:
        h = _input_artifact_hashes(REPO_ROOT)
        self.assertIn("manifest", h)
        m = h["manifest"]
        self.assertEqual(m["relpath"], "assets/evolution-manifest.json")
        p = REPO_ROOT / "assets" / "evolution-manifest.json"
        if p.is_file():
            self.assertIsInstance(m.get("sha256"), str)
            self.assertEqual(len(m["sha256"]), 64)
            self.assertIsInstance(m.get("bytes"), int)
        else:
            self.assertTrue(m.get("missing"))

    def test_each_key_has_relpath(self) -> None:
        h = _input_artifact_hashes(REPO_ROOT)
        for key in (
            "manifest",
            "candidates",
            "hint_rules",
            "hint_decisions",
            "ingest_config",
            "maps_to_hints",
        ):
            self.assertIn(key, h, msg=key)
            self.assertIn("relpath", h[key])


if __name__ == "__main__":
    unittest.main()
