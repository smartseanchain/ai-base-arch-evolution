"""管理员账户 API（需 ``ADMIN_ACCOUNTS_API_SECRET`` + 临时文件路径）。"""
from __future__ import annotations

import os
import tempfile
import unittest
from unittest import mock

from fastapi.testclient import TestClient

from app.main import app


class TestAdminAccountsAPI(unittest.TestCase):
    def test_list_without_secret_config_returns_503(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "a.json")
            with mock.patch.dict(
                os.environ,
                {
                    "ADMIN_ACCOUNTS_FILE": path,
                    "ADMIN_ACCOUNTS_API_SECRET": "",
                },
                clear=False,
            ):
                r = TestClient(app).get("/api/admin/accounts")
        self.assertEqual(r.status_code, 503)

    def test_crud_with_secret(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "acct.json")
            env = {
                "ADMIN_ACCOUNTS_API_SECRET": "test-secret-hex",
                "ADMIN_ACCOUNTS_FILE": path,
            }
            with mock.patch.dict(os.environ, env, clear=False):
                c = TestClient(app)
                r = c.get("/api/admin/accounts")
                self.assertEqual(r.status_code, 401)
                h = {"X-Admin-Accounts-Secret": "wrong"}
                r = c.get("/api/admin/accounts", headers=h)
                self.assertEqual(r.status_code, 401)
                h_ok = {"X-Admin-Accounts-Secret": "test-secret-hex"}
                r = c.get("/api/admin/accounts", headers=h_ok)
                self.assertEqual(r.status_code, 200)
                self.assertEqual(r.json(), {"users": []})

                r = c.post(
                    "/api/admin/accounts",
                    headers=h_ok,
                    json={
                        "username": "alice",
                        "password": "password12",
                        "roles": ["admin", "ops"],
                    },
                )
                self.assertEqual(r.status_code, 201)
                body = r.json()
                self.assertEqual(body["username"], "alice")
                self.assertEqual(body["roles"], ["admin", "ops"])
                self.assertFalse(body["disabled"])
                self.assertIn("id", body)
                uid = body["id"]

                r = c.post(
                    "/api/admin/accounts",
                    headers=h_ok,
                    json={"username": "alice", "password": "otherpass1"},
                )
                self.assertEqual(r.status_code, 409)

                r = c.get("/api/admin/accounts", headers=h_ok)
                self.assertEqual(len(r.json().get("users", [])), 1)

                r = c.patch(
                    f"/api/admin/accounts/{uid}",
                    headers=h_ok,
                    json={"disabled": True},
                )
                self.assertEqual(r.status_code, 200)
                self.assertTrue(r.json()["disabled"])

                r = c.delete(f"/api/admin/accounts/{uid}", headers=h_ok)
                self.assertEqual(r.status_code, 204)
                self.assertEqual(r.content, b"")

                r = c.get("/api/admin/accounts", headers=h_ok)
                self.assertEqual(r.json(), {"users": []})

    def test_bearer_auth(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "b.json")
            with mock.patch.dict(
                os.environ,
                {
                    "ADMIN_ACCOUNTS_API_SECRET": "tok",
                    "ADMIN_ACCOUNTS_FILE": path,
                },
                clear=False,
            ):
                c = TestClient(app)
                r = c.get(
                    "/api/admin/accounts",
                    headers={"Authorization": "Bearer tok"},
                )
                self.assertEqual(r.status_code, 200)

    def test_health_and_bootstrap_flag(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "c.json")
            with mock.patch.dict(
                os.environ,
                {
                    "ADMIN_ACCOUNTS_API_SECRET": "x",
                    "ADMIN_ACCOUNTS_FILE": path,
                },
                clear=False,
            ):
                c = TestClient(app)
                self.assertTrue(c.get("/health").json().get("admin_accounts_enabled"))
                self.assertTrue(c.get("/api/bootstrap").json().get("admin_accounts_enabled"))

    def test_auth_failure_emits_warning_audit(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "w.json")
            with mock.patch.dict(
                os.environ,
                {
                    "ADMIN_ACCOUNTS_API_SECRET": "good-secret",
                    "ADMIN_ACCOUNTS_FILE": path,
                },
                clear=False,
            ):
                c = TestClient(app)
                with self.assertLogs("admin_console.admin_accounts", level="WARNING") as cm:
                    r = c.get(
                        "/api/admin/accounts",
                        headers={"X-Admin-Accounts-Secret": "wrong"},
                    )
                self.assertEqual(r.status_code, 401)
        blob = " ".join(cm.output)
        self.assertIn("admin_accounts_auth_failed", blob)

    def test_create_emits_info_audit(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "i.json")
            with mock.patch.dict(
                os.environ,
                {
                    "ADMIN_ACCOUNTS_API_SECRET": "s",
                    "ADMIN_ACCOUNTS_FILE": path,
                },
                clear=False,
            ):
                c = TestClient(app)
                h = {
                    "X-Admin-Accounts-Secret": "s",
                    "Content-Type": "application/json",
                }
                with self.assertLogs("admin_console.admin_accounts", level="INFO") as cm:
                    r = c.post(
                        "/api/admin/accounts",
                        headers=h,
                        json={"username": "u1", "password": "password12"},
                    )
                self.assertEqual(r.status_code, 201)
        blob = " ".join(cm.output)
        self.assertIn("admin_account_created", blob)
