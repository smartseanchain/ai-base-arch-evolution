"""evolution_pkg.ops.http_cache：无 FastAPI 依赖，默认 test 套件必跑。"""
from __future__ import annotations

import json
import unittest

from evolution_pkg.ops.http_cache import (
    CACHE_JSON_DYNAMIC,
    CACHE_JSON_REVALIDATE,
    etag_for_bytes,
    if_none_match_prefers_304,
    prepare_dynamic_json,
    prepare_revalidated_json,
)


class TestHttpCache(unittest.TestCase):
    def test_etag_stable(self) -> None:
        raw = b'{"a":1}'
        self.assertEqual(etag_for_bytes(raw), etag_for_bytes(raw))
        self.assertTrue(etag_for_bytes(raw).startswith('"'))
        self.assertTrue(etag_for_bytes(raw).endswith('"'))

    def test_if_none_match_empty(self) -> None:
        self.assertFalse(if_none_match_prefers_304(None, '"x"'))
        self.assertFalse(if_none_match_prefers_304("", '"x"'))
        self.assertFalse(if_none_match_prefers_304("   ", '"x"'))

    def test_if_none_match_star(self) -> None:
        self.assertTrue(if_none_match_prefers_304("*", '"any"'))

    def test_if_none_match_exact(self) -> None:
        etag = '"abc123"'
        self.assertTrue(if_none_match_prefers_304(etag, etag))

    def test_if_none_match_weak_prefix(self) -> None:
        etag = '"abc123"'
        self.assertTrue(if_none_match_prefers_304("W/" + etag, etag))

    def test_if_none_match_comma_list(self) -> None:
        etag = '"hit"'
        self.assertTrue(
            if_none_match_prefers_304('"miss", "other", ' + etag, etag)
        )

    def test_if_none_match_no_hit(self) -> None:
        self.assertFalse(
            if_none_match_prefers_304('"a", "b"', '"c"'),
        )

    def test_prepare_revalidated_json_200(self) -> None:
        raw = b'{"x":1}'
        prep = prepare_revalidated_json(raw, None)
        self.assertEqual(prep.status_code, 200)
        self.assertEqual(prep.body, raw)
        self.assertEqual(prep.headers["Cache-Control"], CACHE_JSON_REVALIDATE)
        self.assertEqual(prep.headers["ETag"], etag_for_bytes(raw))

    def test_prepare_revalidated_json_304(self) -> None:
        raw = b'{"x":1}'
        etag = etag_for_bytes(raw)
        prep = prepare_revalidated_json(raw, etag)
        self.assertEqual(prep.status_code, 304)
        self.assertIsNone(prep.body)
        self.assertEqual(prep.headers["ETag"], etag)

    def test_prepare_dynamic_json_200_and_304(self) -> None:
        data = {"total": 0, "rows": []}
        prep0 = prepare_dynamic_json(data, None)
        self.assertEqual(prep0.status_code, 200)
        self.assertIsNotNone(prep0.body)
        self.assertEqual(prep0.headers["Cache-Control"], CACHE_JSON_DYNAMIC)
        etag = prep0.headers["ETag"]
        prep1 = prepare_dynamic_json(data, etag)
        self.assertEqual(prep1.status_code, 304)
        self.assertIsNone(prep1.body)

    def test_prepare_dynamic_json_non_200_no_304(self) -> None:
        """非 200 不根据 If-None-Match 返回 304（与 readonly_api 语义一致）。"""
        data = {"error": "x"}
        raw = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
        etag = etag_for_bytes(raw)
        prep = prepare_dynamic_json(data, etag, status_code=404)
        self.assertEqual(prep.status_code, 404)
        self.assertIsNotNone(prep.body)


if __name__ == "__main__":
    unittest.main()
