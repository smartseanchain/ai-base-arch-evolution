"""
管理员账户文件存储与 API（需环境变量 ``ADMIN_ACCOUNTS_API_SECRET``）。

密码使用 bcrypt；数据文件默认 ``data/admin_accounts.json``（勿提交仓库，见 ``.gitignore``）。
"""
from __future__ import annotations

import json
import logging
import re
import secrets
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional

import bcrypt
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

from .settings import Settings, load_settings

_ROOT = Path(__file__).resolve().parent.parent
_STORE_LOCK = threading.Lock()
_LOGGER = logging.getLogger("admin_console.admin_accounts")


def _audit(level: int, event: str, **fields: Any) -> None:
    """单行 JSON，便于日志采集；不含密码、不含 API 密钥。"""
    payload: dict[str, Any] = {"event": event, "ts": _utc_now_iso()}
    for k, v in fields.items():
        if v is not None:
            payload[k] = v
    _LOGGER.log(level, "%s", json.dumps(payload, ensure_ascii=False))

_USERNAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$")


def _accounts_file_path(settings: Settings) -> Path:
    raw = (settings.admin_accounts_file or "data/admin_accounts.json").strip()
    p = Path(raw)
    if p.is_absolute():
        return p
    return _ROOT / p


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _empty_store() -> dict[str, Any]:
    return {"schema_version": 1, "users": []}


def _load_raw(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError, UnicodeError):
        return _empty_store()
    if not isinstance(data, dict):
        return _empty_store()
    users = data.get("users")
    if not isinstance(users, list):
        data["users"] = []
    return data


def _save_raw(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def _verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("ascii"))
    except (ValueError, TypeError):
        return False


def _user_to_public(u: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": u.get("id", ""),
        "username": u.get("username", ""),
        "roles": list(u.get("roles") or []),
        "disabled": bool(u.get("disabled", False)),
        "created_at": u.get("created_at", ""),
        "updated_at": u.get("updated_at", ""),
    }


def _normalize_roles(roles: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for r in roles:
        s = str(r).strip()
        if not s or len(s) > 64:
            continue
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def load_store(settings: Settings) -> dict[str, Any]:
    path = _accounts_file_path(settings)
    with _STORE_LOCK:
        return _load_raw(path)


def save_store(settings: Settings, data: dict[str, Any]) -> None:
    path = _accounts_file_path(settings)
    with _STORE_LOCK:
        _save_raw(path, data)


def verify_admin_accounts_secret(request: Request, settings: Settings) -> None:
    if not settings.admin_accounts_api_secret:
        raise HTTPException(
            status_code=503,
            detail="ADMIN_ACCOUNTS_API_SECRET not configured",
        )
    header_secret = (request.headers.get("x-admin-accounts-secret") or "").strip()
    auth = request.headers.get("authorization") or ""
    bearer = ""
    if auth.lower().startswith("bearer "):
        bearer = auth[7:].strip()
    got = header_secret or bearer
    if not got or not secrets.compare_digest(got, settings.admin_accounts_api_secret):
        _audit(
            logging.WARNING,
            "admin_accounts_auth_failed",
            path=request.url.path,
            method=request.method,
            client_host=request.client.host if request.client else None,
        )
        raise HTTPException(status_code=401, detail="invalid or missing admin accounts secret")


router = APIRouter(prefix="/api/admin", tags=["admin-accounts"])


class AdminUserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=8, max_length=256)
    roles: List[str] = Field(default_factory=lambda: ["admin"])


class AdminUserUpdate(BaseModel):
    password: Optional[str] = Field(default=None, min_length=8, max_length=256)
    roles: Optional[List[str]] = None
    disabled: Optional[bool] = None


@router.get("/accounts")
def list_admin_accounts(request: Request) -> dict[str, Any]:
    s = load_settings()
    verify_admin_accounts_secret(request, s)
    data = load_store(s)
    users = [_user_to_public(u) for u in data.get("users", []) if isinstance(u, dict)]
    users.sort(key=lambda x: (x.get("username") or "").lower())
    return {"users": users}


@router.post("/accounts", status_code=201)
def create_admin_account(request: Request, body: AdminUserCreate) -> dict[str, Any]:
    s = load_settings()
    verify_admin_accounts_secret(request, s)
    uname = body.username.strip()
    if not _USERNAME_RE.match(uname):
        raise HTTPException(
            status_code=400,
            detail="username must match [a-zA-Z0-9][a-zA-Z0-9._-]{0,63}",
        )
    roles = _normalize_roles(body.roles)
    if not roles:
        raise HTTPException(status_code=400, detail="roles must be a non-empty list")

    with _STORE_LOCK:
        path = _accounts_file_path(s)
        data = _load_raw(path)
        users = data.setdefault("users", [])
        if not isinstance(users, list):
            users = []
            data["users"] = users
        for u in users:
            if isinstance(u, dict) and u.get("username") == uname:
                raise HTTPException(status_code=409, detail="username already exists")
        now = _utc_now_iso()
        uid = str(uuid.uuid4())
        row = {
            "id": uid,
            "username": uname,
            "password_hash": _hash_password(body.password),
            "roles": roles,
            "disabled": False,
            "created_at": now,
            "updated_at": now,
        }
        users.append(row)
        _save_raw(path, data)
    pub = _user_to_public(row)
    _audit(
        logging.INFO,
        "admin_account_created",
        user_id=pub.get("id"),
        username=pub.get("username"),
        roles=pub.get("roles"),
    )
    return pub


@router.patch("/accounts/{user_id}")
def update_admin_account(
    request: Request, user_id: str, body: AdminUserUpdate
) -> dict[str, Any]:
    s = load_settings()
    verify_admin_accounts_secret(request, s)
    uid = user_id.strip()
    if not uid:
        raise HTTPException(status_code=400, detail="invalid user id")
    if body.password is None and body.roles is None and body.disabled is None:
        raise HTTPException(status_code=400, detail="no fields to update")

    with _STORE_LOCK:
        path = _accounts_file_path(s)
        data = _load_raw(path)
        users = data.get("users")
        if not isinstance(users, list):
            raise HTTPException(status_code=404, detail="user not found")
        found: dict[str, Any] | None = None
        for u in users:
            if isinstance(u, dict) and u.get("id") == uid:
                found = u
                break
        if found is None:
            raise HTTPException(status_code=404, detail="user not found")
        now = _utc_now_iso()
        if body.password is not None:
            found["password_hash"] = _hash_password(body.password)
        if body.roles is not None:
            roles = _normalize_roles(body.roles)
            if not roles:
                raise HTTPException(status_code=400, detail="roles must be non-empty when set")
            found["roles"] = roles
        if body.disabled is not None:
            found["disabled"] = body.disabled
        found["updated_at"] = now
        _save_raw(path, data)
    pub = _user_to_public(found)
    _audit(
        logging.INFO,
        "admin_account_updated",
        user_id=pub.get("id"),
        username=pub.get("username"),
        password_rotated=body.password is not None,
        roles_updated=body.roles is not None,
        disabled_updated=body.disabled is not None,
        disabled=pub.get("disabled"),
    )
    return pub


@router.delete("/accounts/{user_id}")
def delete_admin_account(request: Request, user_id: str) -> Response:
    s = load_settings()
    verify_admin_accounts_secret(request, s)
    uid = user_id.strip()
    if not uid:
        raise HTTPException(status_code=400, detail="invalid user id")

    with _STORE_LOCK:
        path = _accounts_file_path(s)
        data = _load_raw(path)
        users = data.get("users")
        if not isinstance(users, list):
            raise HTTPException(status_code=404, detail="user not found")
        deleted_username: Optional[str] = None
        for u in users:
            if isinstance(u, dict) and u.get("id") == uid:
                deleted_username = str(u.get("username") or "")
                break
        new_users = [u for u in users if not (isinstance(u, dict) and u.get("id") == uid)]
        if len(new_users) == len(users):
            raise HTTPException(status_code=404, detail="user not found")
        data["users"] = new_users
        _save_raw(path, data)
    _audit(
        logging.INFO,
        "admin_account_deleted",
        user_id=uid,
        username=deleted_username or "",
    )
    return Response(status_code=204)


def authenticate_admin_user(
    settings: Settings, username: str, password: str
) -> Optional[dict[str, Any]]:
    """供后续登录/会话使用：校验用户名密码，返回公开字段（不含 hash）。"""
    uname = username.strip()
    if not uname or not password:
        return None
    data = load_store(settings)
    for u in data.get("users", []):
        if not isinstance(u, dict):
            continue
        if u.get("username") != uname or u.get("disabled"):
            continue
        ph = u.get("password_hash")
        if not isinstance(ph, str) or not _verify_password(password, ph):
            continue
        return _user_to_public(u)
    return None
