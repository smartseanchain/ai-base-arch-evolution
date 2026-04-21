"""``evolution_pkg.ingest_fetch`` · HTTPS GET（mock 网络）。"""
from __future__ import annotations

import unittest
import unittest.mock as mock

from evolution_pkg.ingest_fetch import fetch_bytes


class TestFetchBytes(unittest.TestCase):
    def test_https_ok(self) -> None:
        with mock.patch("urllib.request.urlopen") as mu:
            resp = mock.Mock()
            resp.read.return_value = b"ok-body"
            mu.return_value.__enter__.return_value = resp
            mu.return_value.__exit__.return_value = None
            out = fetch_bytes("https://example.test/path")
        self.assertEqual(out, b"ok-body")

    def test_rejects_http(self) -> None:
        with self.assertRaises(ValueError):
            fetch_bytes("http://example.test/x")


if __name__ == "__main__":
    unittest.main()
