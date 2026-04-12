"""``evolution_pkg.readonly_disk_routes`` 与 ``readonly_api`` 注册一致性。"""
from __future__ import annotations

import unittest
from pathlib import Path

from readonly_test_util import READONLY_API_SKIP_REASON, readonly_api_available


class TestReadonlyDiskRoutesMeta(unittest.TestCase):
    def test_paths_unique_single_segment(self) -> None:
        from evolution_pkg.readonly_disk_routes import READONLY_DISK_JSON_ROUTES

        paths = [r.path for r in READONLY_DISK_JSON_ROUTES]
        self.assertEqual(len(paths), len(set(paths)))
        for r in READONLY_DISK_JSON_ROUTES:
            self.assertTrue(r.path.startswith("/"), r.path)
            self.assertEqual(r.path.count("/"), 1, r.path)
            self.assertNotIn("..", Path(r.rel_path).parts, r.rel_path)
            self.assertFalse(Path(r.rel_path).is_absolute(), r.rel_path)
            self.assertTrue(r.rel_path.endswith(".json"), r.rel_path)


@unittest.skipUnless(
    readonly_api_available(),
    READONLY_API_SKIP_REASON,
)
class TestReadonlyDiskRoutesOpenAPI(unittest.TestCase):
    def test_disk_paths_in_openapi(self) -> None:
        from evolution_pkg.readonly_disk_routes import READONLY_DISK_JSON_ROUTES

        import readonly_api

        spec = readonly_api.app.openapi()
        openapi_paths = spec.get("paths") or {}
        for route in READONLY_DISK_JSON_ROUTES:
            self.assertIn(
                route.path,
                openapi_paths,
                msg=f"missing OpenAPI path for {route.path!r}",
            )
