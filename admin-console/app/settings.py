"""环境变量配置（无 pydantic-settings 依赖，便于小镜像）。"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Settings:
    readonly_api_base_url: str
    cors_origins: tuple[str, ...]
    dev_bypass: bool
    dev_user: dict[str, Any] | None
    #: GitHub/GitLab **blob** 视图的 ``…/blob/<branch>/`` 前缀（无尾斜杠亦可），用于控制台拼文档/JSON 外链。Fork 请改指向本仓。
    repo_web_base: str
    #: 非空时启用 ``/api/admin/accounts``；请求头 ``X-Admin-Accounts-Secret`` 或 ``Authorization: Bearer …``。
    admin_accounts_api_secret: str | None
    #: 相对 ``admin-console/`` 根或绝对路径；默认 ``data/admin_accounts.json``。
    admin_accounts_file: str


def load_settings() -> Settings:
    """每次调用重新读环境，便于单测 ``patch.dict``。"""
    raw = os.environ.get("ADMIN_CORS_ORIGINS", "")
    origins = tuple(x.strip() for x in raw.split(",") if x.strip())
    bypass = os.environ.get("ADMIN_DEV_BYPASS", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )
    dev_json = os.environ.get("ADMIN_DEV_USER_JSON", "").strip()
    dev_user: dict[str, Any] | None = None
    if dev_json:
        try:
            parsed = json.loads(dev_json)
            if isinstance(parsed, dict):
                dev_user = parsed
        except json.JSONDecodeError:
            dev_user = None
    base = os.environ.get("READONLY_API_BASE_URL", "").strip().rstrip("/")
    raw_repo = os.environ.get("ADMIN_REPO_WEB_BASE")
    if raw_repo is None:
        repo_base = (
            "https://github.com/smartseanchain/ai-base-arch-evolution/blob/main"
        )
    else:
        repo_base = raw_repo.strip().rstrip("/")
    acct_secret_raw = os.environ.get("ADMIN_ACCOUNTS_API_SECRET", "").strip()
    acct_secret = acct_secret_raw if acct_secret_raw else None
    acct_file = os.environ.get("ADMIN_ACCOUNTS_FILE", "data/admin_accounts.json").strip()
    if not acct_file:
        acct_file = "data/admin_accounts.json"
    return Settings(
        readonly_api_base_url=base,
        cors_origins=origins,
        dev_bypass=bypass,
        dev_user=dev_user,
        repo_web_base=repo_base,
        admin_accounts_api_secret=acct_secret,
        admin_accounts_file=acct_file,
    )


# 仅允许代理到 ``readonly_api`` 的只读 GET 路径（单段）；禁止任意 URL、禁止带 path 穿越。
# 与 ``readonly_api`` 单段路由对账：``evolution_pkg.readonly_disk_routes`` + ``scripts/tests/test_readonly_proxy_segment_sync.py``（``make validate`` / ``make test-readonly-api``）。
READONLY_PROXY_SEGMENTS: frozenset[str] = frozenset(
    {
        "ai-analysis-overlay",
        "ai-overlay-step",
        "candidates",
        "health",
        "ingest-config",
        "hint-decisions",
        "hint-rules",
        "snapshot",
        "snapshot-history",
        "trends",
        "manifest",
        "maps-to-hints",
        "registry",
        "sediment",
        "site-meta",
        "site-search-index",
        "openapi.json",
        "docs",
    }
)
