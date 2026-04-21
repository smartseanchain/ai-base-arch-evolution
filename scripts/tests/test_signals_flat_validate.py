"""evolution_pkg.signals_flat_validate。"""
from __future__ import annotations

import unittest

from evolution_pkg.signals_flat_validate import (
    SignalsFlatValidationError,
    validate_candidates_signals_structure,
    validate_manifest_signals_structure,
)


def _good_manifest() -> dict:
    return {
        "schema_version": 1,
        "signals": [
            {
                "id": "s1",
                "kind": "tech",
                "weight": "high",
                "maps_to": {"pages": ["a.html"], "lab_factors": []},
            }
        ],
    }


class TestSignalsFlatValidate(unittest.TestCase):
    def test_manifest_ok(self) -> None:
        n = validate_manifest_signals_structure(_good_manifest())
        self.assertEqual(n, 1)

    def test_manifest_schema_version(self) -> None:
        d = _good_manifest()
        d["schema_version"] = 2
        with self.assertRaises(SignalsFlatValidationError):
            validate_manifest_signals_structure(d)

    def test_manifest_duplicate_id(self) -> None:
        d = _good_manifest()
        d["signals"].append(
            {
                "id": "s1",
                "kind": "law",
                "maps_to": {},
            }
        )
        with self.assertRaises(SignalsFlatValidationError) as ctx:
            validate_manifest_signals_structure(d)
        self.assertIn("重复", str(ctx.exception))

    def test_candidates_ok(self) -> None:
        data = {
            "signals": [
                {
                    "id": "c1",
                    "kind": "policy",
                    "review_state": "pending",
                }
            ]
        }
        self.assertEqual(validate_candidates_signals_structure(data), 1)

    def test_candidates_bad_review_state(self) -> None:
        data = {
            "signals": [
                {
                    "id": "c1",
                    "kind": "policy",
                    "review_state": "bogus",
                }
            ]
        }
        with self.assertRaises(SignalsFlatValidationError):
            validate_candidates_signals_structure(data)


if __name__ == "__main__":
    unittest.main()
