"""只读 API 条件 GET（304）；需 ``pip install -r requirements-api.txt``，否则整类跳过。"""
from __future__ import annotations

import unittest

from readonly_test_util import READONLY_API_SKIP_REASON, readonly_api_available


@unittest.skipUnless(
    readonly_api_available(),
    READONLY_API_SKIP_REASON,
)
class TestReadonlyApiConditionalGet(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from fastapi.testclient import TestClient

        import readonly_api

        cls.client = TestClient(readonly_api.app)

    def test_snapshot_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/snapshot")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get("/snapshot", headers={"If-None-Match": etag})
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_snapshot_history_list_304(self) -> None:
        r1 = self.client.get("/snapshot-history?limit=5&offset=0")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get(
            "/snapshot-history?limit=5&offset=0",
            headers={"If-None-Match": etag},
        )
        self.assertEqual(r2.status_code, 304)

    def test_registry_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/registry")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get("/registry", headers={"If-None-Match": etag})
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_sediment_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/sediment")
        if r1.status_code == 404:
            self.skipTest("data/sediment.json missing (optional in shallow clones)")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get("/sediment", headers={"If-None-Match": etag})
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_candidates_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/candidates")
        if r1.status_code == 404:
            self.skipTest("assets/evolution-candidates.json missing")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get("/candidates", headers={"If-None-Match": etag})
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_hint_decisions_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/hint-decisions")
        if r1.status_code == 404:
            self.skipTest("assets/evolution-hint-decisions.json missing")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get("/hint-decisions", headers={"If-None-Match": etag})
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_hint_rules_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/hint-rules")
        if r1.status_code == 404:
            self.skipTest("scripts/evolution-hint-rules.json missing")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get("/hint-rules", headers={"If-None-Match": etag})
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_maps_to_hints_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/maps-to-hints")
        if r1.status_code == 404:
            self.skipTest("scripts/maps_to_hints.json missing")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get("/maps-to-hints", headers={"If-None-Match": etag})
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_ingest_config_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/ingest-config")
        if r1.status_code == 404:
            self.skipTest("scripts/ingest_config.json missing")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get("/ingest-config", headers={"If-None-Match": etag})
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_ai_analysis_overlay_304_when_if_none_match_matches(self) -> None:
        r1 = self.client.get("/ai-analysis-overlay")
        if r1.status_code == 404:
            self.skipTest("assets/ai-analysis-overlay.json missing (optional)")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get(
            "/ai-analysis-overlay", headers={"If-None-Match": etag}
        )
        self.assertEqual(r2.status_code, 304)
        self.assertEqual(r2.content, b"")
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_snapshot_wrong_etag_returns_200_with_body(self) -> None:
        r1 = self.client.get("/snapshot")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        wrong = '"000000000000000000000000"' if etag != '"000000000000000000000000"' else '"ffffffffffffffffffffffff"'
        r2 = self.client.get("/snapshot", headers={"If-None-Match": wrong})
        self.assertEqual(r2.status_code, 200)
        self.assertGreater(len(r2.content), 10)
        self.assertEqual(r2.headers.get("etag"), etag)

    def test_snapshot_weak_etag_prefix_yields_304(self) -> None:
        r1 = self.client.get("/snapshot")
        etag = r1.headers["etag"]
        r2 = self.client.get(
            "/snapshot",
            headers={"If-None-Match": "W/" + etag},
        )
        self.assertEqual(r2.status_code, 304)

    def test_snapshot_comma_separated_if_none_match_second_matches(self) -> None:
        r1 = self.client.get("/snapshot")
        etag = r1.headers["etag"]
        r2 = self.client.get(
            "/snapshot",
            headers={"If-None-Match": '"nomatch", ' + etag},
        )
        self.assertEqual(r2.status_code, 304)

    def test_snapshot_history_unknown_run_404_no_store(self) -> None:
        r = self.client.get("/snapshot-history/readonly-api-test-missing-run-id")
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.headers.get("cache-control"), "no-store")

    def test_snapshot_history_by_run_304_when_sqlite_has_row(self) -> None:
        r0 = self.client.get("/snapshot")
        self.assertEqual(r0.status_code, 200)
        rid = (r0.json().get("run") or {}).get("run_id")
        if not rid:
            self.skipTest("snapshot lacks run.run_id")
        r1 = self.client.get(f"/snapshot-history/{rid}")
        if r1.status_code == 404:
            self.skipTest("no sqlite row for current run_id (local DB optional)")
        self.assertEqual(r1.status_code, 200)
        etag = r1.headers["etag"]
        r2 = self.client.get(
            f"/snapshot-history/{rid}",
            headers={"If-None-Match": etag},
        )
        self.assertEqual(r2.status_code, 304)
