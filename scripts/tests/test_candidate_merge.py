"""``evolution_pkg.candidate_merge`` · 候选并入 manifest 的纯变换。"""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
import unittest.mock as mock
from datetime import date
from pathlib import Path

import evolution_pkg.io as ep_io

from evolution_pkg.candidate_merge import ReviewStateError, main, merge_candidate_ids


class TestStripForManifest(unittest.TestCase):
    def test_minimal_signal(self) -> None:
        from evolution_pkg.candidate_merge import strip_for_manifest

        sig = {"id": "ing_test1", "title": "T", "summary": "S"}
        out = strip_for_manifest(sig)
        self.assertEqual(out["id"], "ing_test1")
        self.assertEqual(out["kind"], "opinion")
        self.assertEqual(out["title"], "T")
        self.assertEqual(out["summary"], "S")
        self.assertEqual(out["weight"], "medium")
        self.assertEqual(out["maps_to"], {"pages": [], "lab_factors": []})
        self.assertEqual(out["since"], str(date.today()))

    def test_preserves_maps_to(self) -> None:
        from evolution_pkg.candidate_merge import strip_for_manifest

        sig = {
            "id": "ing_x",
            "maps_to": {"pages": ["lab.html"], "lab_factors": ["x"]},
        }
        out = strip_for_manifest(sig)
        self.assertEqual(out["maps_to"], {"pages": ["lab.html"], "lab_factors": ["x"]})

    def test_item_link_appended_to_summary(self) -> None:
        from evolution_pkg.candidate_merge import strip_for_manifest

        sig = {
            "id": "ing_y",
            "summary": "base",
            "source": {"item_link": "https://example/a"},
        }
        out = strip_for_manifest(sig)
        self.assertIn("链接: https://example/a", out["summary"])
        self.assertTrue(out["summary"].startswith("base"))

    def test_law_html_url_appended(self) -> None:
        from evolution_pkg.candidate_merge import strip_for_manifest

        sig = {
            "id": "ing_z",
            "summary": "",
            "source": {
                "type": "law_html",
                "url": "https://law.example/index",
            },
        }
        out = strip_for_manifest(sig)
        self.assertIn("索引页: https://law.example/index", out["summary"])

    def test_summary_truncation(self) -> None:
        from evolution_pkg.candidate_merge import strip_for_manifest

        long_base = "x" * 2400
        sig = {
            "id": "ing_long",
            "summary": long_base,
            "source": {"item_link": "https://x/y"},
        }
        out = strip_for_manifest(sig)
        self.assertLessEqual(len(out["summary"]), 2500)


class TestMergeCandidateIds(unittest.TestCase):
    def test_merges_queued_and_removes_from_candidates(self) -> None:
        man: dict = {"signals": [], "notes": ""}
        cand: dict = {
            "signals": [
                {
                    "id": "ing_a",
                    "status": "candidate",
                    "review_state": "queued_for_manifest",
                    "title": "A",
                }
            ],
            "fetched_at": "2020-01-01",
        }
        m2, c2, n, warns = merge_candidate_ids(cand, man, {"ing_a"})
        self.assertEqual(n, 1)
        self.assertEqual(warns, [])
        self.assertEqual(len(m2["signals"]), 1)
        self.assertEqual(m2["signals"][0]["id"], "ing_a")
        self.assertIn("合并 1 条", m2.get("notes", ""))
        self.assertEqual(c2["signals"], [])
        self.assertEqual(c2.get("fetched_at"), "2020-01-01")
        self.assertIn("updated", m2)
        self.assertIn("updated", c2)

    def test_review_state_rejects_without_force(self) -> None:
        man: dict = {"signals": []}
        cand: dict = {
            "signals": [
                {
                    "id": "ing_b",
                    "status": "candidate",
                    "review_state": "pending",
                    "title": "B",
                }
            ]
        }
        with self.assertRaises(ReviewStateError) as ctx:
            merge_candidate_ids(cand, man, {"ing_b"}, force=False)
        self.assertEqual(ctx.exception.signal_id, "ing_b")
        self.assertEqual(ctx.exception.review_state, "pending")

    def test_force_allows_pending(self) -> None:
        man: dict = {"signals": []}
        cand: dict = {
            "signals": [
                {
                    "id": "ing_c",
                    "status": "candidate",
                    "review_state": "pending",
                    "title": "C",
                }
            ]
        }
        m2, c2, n, _ = merge_candidate_ids(cand, man, {"ing_c"}, force=True)
        self.assertEqual(n, 1)
        self.assertEqual(len(m2["signals"]), 1)
        self.assertEqual(c2["signals"], [])

    def test_skips_duplicate_in_manifest(self) -> None:
        man: dict = {"signals": [{"id": "ing_d", "title": "old"}]}
        cand: dict = {
            "signals": [
                {
                    "id": "ing_d",
                    "status": "candidate",
                    "review_state": "queued_for_manifest",
                    "title": "new",
                }
            ]
        }
        m2, c2, n, warns = merge_candidate_ids(cand, man, {"ing_d"})
        self.assertEqual(n, 0)
        self.assertTrue(any("manifest 已有" in w for w in warns))
        self.assertEqual(len(m2["signals"]), 1)

    def test_missing_id_warning_only(self) -> None:
        man: dict = {"signals": []}
        cand: dict = {"signals": []}
        m2, c2, n, warns = merge_candidate_ids(cand, man, {"missing"})
        self.assertEqual(n, 0)
        self.assertEqual(len(warns), 1)
        self.assertIn("无 id", warns[0])

    def test_does_not_mutate_inputs(self) -> None:
        man: dict = {"signals": []}
        cand: dict = {
            "signals": [
                {
                    "id": "ing_e",
                    "status": "candidate",
                    "review_state": "queued_for_manifest",
                    "title": "E",
                }
            ]
        }
        man_id = id(man)
        cand_id = id(cand)
        merge_candidate_ids(cand, man, {"ing_e"})
        self.assertEqual(id(man), man_id)
        self.assertEqual(id(cand), cand_id)
        self.assertEqual(man["signals"], [])
        self.assertEqual(len(cand["signals"]), 1)


class TestCandidateMergeMain(unittest.TestCase):
    def test_main_merges_in_temp_repo(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "assets").mkdir(parents=True)
            man = root / "assets" / "evolution-manifest.json"
            cand = root / "assets" / "evolution-candidates.json"
            man.write_text(
                json.dumps({"signals": [], "notes": ""}, ensure_ascii=False),
                encoding="utf-8",
            )
            cand.write_text(
                json.dumps(
                    {
                        "signals": [
                            {
                                "id": "ing_cli",
                                "status": "candidate",
                                "review_state": "queued_for_manifest",
                                "title": "CLI",
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            with mock.patch.object(ep_io, "REPO_ROOT", root):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
                    io.StringIO()
                ):
                    rc = main(["ing_cli"])
            self.assertEqual(rc, 0)
            man_out = json.loads(man.read_text(encoding="utf-8"))
            cand_out = json.loads(cand.read_text(encoding="utf-8"))
            self.assertEqual(len(man_out["signals"]), 1)
            self.assertEqual(man_out["signals"][0]["id"], "ing_cli")
            self.assertEqual(cand_out["signals"], [])

    def test_main_review_state_returns_1(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "assets").mkdir(parents=True)
            man = root / "assets" / "evolution-manifest.json"
            cand = root / "assets" / "evolution-candidates.json"
            man.write_text(json.dumps({"signals": []}), encoding="utf-8")
            cand.write_text(
                json.dumps(
                    {
                        "signals": [
                            {
                                "id": "ing_bad",
                                "status": "candidate",
                                "review_state": "pending",
                                "title": "X",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(ep_io, "REPO_ROOT", root):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
                    io.StringIO()
                ):
                    rc = main(["ing_bad"])
            self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
