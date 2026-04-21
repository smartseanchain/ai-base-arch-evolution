"""黄金集 JSON Schema 与 validate_golden_mapping 入口。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema


class TestValidateGoldenMapping(unittest.TestCase):
    def test_example_fixture_matches_schema(self) -> None:
        root = Path(__file__).resolve().parents[2]
        fixture = root / "fixtures" / "ai_mapping_golden" / "example_case.json"
        schema_path = root / "docs" / "schemas" / "ai-mapping-golden.schema.json"
        doc = json.loads(fixture.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.validate(doc, schema)

    def test_each_golden_json_matches_schema(self) -> None:
        root = Path(__file__).resolve().parents[2]
        golden_dir = root / "fixtures" / "ai_mapping_golden"
        schema_path = root / "docs" / "schemas" / "ai-mapping-golden.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        paths = sorted(golden_dir.glob("*.json"))
        self.assertTrue(paths, msg="fixtures/ai_mapping_golden 下应有 *.json")
        for path in paths:
            with self.subTest(path=path.name):
                doc = json.loads(path.read_text(encoding="utf-8"))
                jsonschema.validate(doc, schema)

    def test_cli_exit_zero(self) -> None:
        root = Path(__file__).resolve().parents[2]
        env = {**os.environ, "PYTHONPATH": str(root / "scripts")}
        proc = subprocess.run(
            [sys.executable, str(root / "scripts" / "validate_golden_mapping.py")],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)

    def test_cli_dir_mode_exit_zero(self) -> None:
        root = Path(__file__).resolve().parents[2]
        env = {**os.environ, "PYTHONPATH": str(root / "scripts")}
        proc = subprocess.run(
            [
                sys.executable,
                str(root / "scripts" / "validate_golden_mapping.py"),
                "--dir",
                "fixtures/ai_mapping_golden",
            ],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)

    def test_cli_file_and_dir_mutually_rejected(self) -> None:
        root = Path(__file__).resolve().parents[2]
        env = {**os.environ, "PYTHONPATH": str(root / "scripts")}
        proc = subprocess.run(
            [
                sys.executable,
                str(root / "scripts" / "validate_golden_mapping.py"),
                "--file",
                "fixtures/ai_mapping_golden/example_case.json",
                "--dir",
                "fixtures/ai_mapping_golden",
            ],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 1, msg=proc.stdout)

    def test_expect_unknown_page_rejected(self) -> None:
        root = Path(__file__).resolve().parents[2]
        bad_doc = {
            "schema_version": 1,
            "cases": [
                {
                    "id": "bad-page",
                    "input": {"title": "any"},
                    "expect": {"pages_contains": ["not-a-real-registry-page.html"]},
                }
            ],
        }
        env = {**os.environ, "PYTHONPATH": str(root / "scripts")}
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            json.dump(bad_doc, tmp)
            tmp_path = tmp.name
        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts" / "validate_golden_mapping.py"),
                    "--file",
                    tmp_path,
                ],
                cwd=str(root),
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, msg=proc.stdout + proc.stderr)
            self.assertIn("evolution-registry", proc.stderr)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_expect_unknown_lab_factor_rejected(self) -> None:
        root = Path(__file__).resolve().parents[2]
        bad_doc = {
            "schema_version": 1,
            "cases": [
                {
                    "id": "bad-factor",
                    "input": {"title": "any"},
                    "expect": {"lab_factors_contains": ["not-a-registry-factor"]},
                }
            ],
        }
        env = {**os.environ, "PYTHONPATH": str(root / "scripts")}
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            json.dump(bad_doc, tmp)
            tmp_path = tmp.name
        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts" / "validate_golden_mapping.py"),
                    "--file",
                    tmp_path,
                ],
                cwd=str(root),
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, msg=proc.stdout + proc.stderr)
            self.assertIn("evolution-registry", proc.stderr)
            self.assertIn("lab_factor", proc.stderr)
        finally:
            Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
