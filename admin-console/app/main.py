"""
管理端：静态仪表盘 + /api/bootstrap + 只读 API 同源代理；不写 manifest、不代理写操作。
只读 API 见 ``scripts/readonly_api.py``；规划见 ``docs/ADMIN_WEB_CONSOLE_ROADMAP.md``。
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo
import threading
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response

from .admin_accounts import router as admin_accounts_router

from .settings import READONLY_PROXY_SEGMENTS, load_settings

_ROOT = Path(__file__).resolve().parent.parent
_DATA_SOURCE_CATALOG_PATH = _ROOT / "data" / "data_source_catalog.json"
_CONTROL_PLANE_ROADMAP_PATH = _ROOT / "data" / "control_plane_roadmap.json"


def _load_data_source_catalog() -> dict[str, Any]:
    """只读参考：市面常见公开数据源入口；**不**由管理端代为请求外网。"""
    empty: dict[str, Any] = {
        "schema_version": 0,
        "title_zh": "数据源参考目录",
        "disclaimer_zh": "未找到 admin-console/data/data_source_catalog.json 或解析失败。",
        "categories": [],
        "sources": [],
    }
    try:
        raw = _DATA_SOURCE_CATALOG_PATH.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError, UnicodeError):
        return empty
    if not isinstance(data, dict):
        return empty
    if not isinstance(data.get("categories"), list):
        data["categories"] = []
    if not isinstance(data.get("sources"), list):
        data["sources"] = []
    return data


def _load_control_plane_roadmap() -> dict[str, Any]:
    """对标市面分析 / 治理后台的分阶段路线图（只读 JSON）；与 ADMIN_WEB_CONSOLE_ROADMAP 对表。"""
    empty: dict[str, Any] = {
        "schema_version": 0,
        "title_zh": "控制面能力路线图",
        "subtitle_zh": "",
        "hard_boundaries_zh": "未找到 admin-console/data/control_plane_roadmap.json 或解析失败。",
        "pillars": [],
        "admin_phases": [],
    }
    try:
        raw = _CONTROL_PLANE_ROADMAP_PATH.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError, UnicodeError):
        return empty
    if not isinstance(data, dict):
        return empty
    if not isinstance(data.get("pillars"), list):
        data["pillars"] = []
    if not isinstance(data.get("admin_phases"), list):
        data["admin_phases"] = []
    return data


# ``/api/bootstrap`` 内 ``pipeline_links``：供控制台拼 Git 托管文档/真源外链（路径相对仓库根）。
_PIPELINE_LINK_ITEMS: tuple[tuple[str, str], ...] = (
    ("管道与数据源 UI", "docs/ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md"),
    ("管理端框架总览", "docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md"),
    ("管理端路线图", "docs/ADMIN_WEB_CONSOLE_ROADMAP.md"),
    ("读者/管理与审核分层", "docs/USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md"),
    ("运行手册：ingest / analyze", "docs/EVOLUTION_RUNBOOK.md"),
    ("舆情与制度跟踪", "docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md"),
    ("舆情类产品对标（参考）", "docs/REFERENCE_DESIGN_OPINION_MONITORING.md"),
    ("数据契约", "docs/DATA_CONTRACTS.md"),
    ("AI 辅助分析层", "docs/AI_ASSISTED_ANALYSIS_LAYER.md"),
    ("数据存储与后续架构", "docs/DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md"),
    ("只读 API 集成", "docs/INTEGRATION_AND_READONLY_API.md"),
    ("编排与事件流", "docs/ORCHESTRATION_AND_EVENT_STREAMING.md"),
    ("合并与发布清单", "docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge"),
    ("MERGE · partials 手顺", "docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence"),
    ("ingest 配置", "scripts/ingest_config.json"),
    ("ingest 映射提示", "scripts/maps_to_hints.json"),
)

# 与 ``EVOLUTION_RUNBOOK`` 对齐的只读「命令链」占位（控制台展示，不代为执行）。
_PIPELINE_CLI_HINTS: tuple[tuple[str, str], ...] = (
    ("抓取候选入池", "make ingest"),
    ("合并前完整校验", "make validate"),
    ("PR 前推荐一键", "make merge-ready"),
    ("分析 + 沉淀 + 趋势", "make analyze"),
    ("校验通过后快算趋势", "make evolution-fast"),
)

_GITHUB_BLOB_BASE = re.compile(
    r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/blob/(?P<branch>[^/]+)/?$",
    re.IGNORECASE,
)


def _github_actions_href(repo_web_base: str) -> str:
    """由 ``…/github.com/owner/repo/blob/ref`` 推导 ``…/owner/repo/actions``；非 GitHub 或无法解析则空串。"""
    m = _GITHUB_BLOB_BASE.match((repo_web_base or "").strip().rstrip("/"))
    if not m:
        return ""
    return "https://github.com/{}/{}".format(
        m.group("owner"),
        m.group("repo"),
    ) + "/actions"


def _github_workflow_ui_href(repo_web_base: str, workflow_filename: str) -> str:
    """``…/actions/workflows/<file>.yml``；非 GitHub blob 基址则空串。"""
    m = _GITHUB_BLOB_BASE.match((repo_web_base or "").strip().rstrip("/"))
    if not m:
        return ""
    return "https://github.com/{}/{}/actions/workflows/{}".format(
        m.group("owner"),
        m.group("repo"),
        workflow_filename,
    )


# 与 ``docs/EVOLUTION_RUNBOOK.md`` ·「自动化周历（GitHub Actions）」对表；文件名须与 ``.github/workflows/`` 一致。
_PIPELINE_WORKFLOWS: tuple[tuple[str, str, str], ...] = (
    (
        "Ingest candidates",
        "每周二 16:00 北京时间（GitHub cron 08:00 UTC）",
        "ingest-pipeline.yml",
    ),
    (
        "Update pipeline",
        "每周二 00:00 北京时间（GitHub cron 周一 16:00 UTC）",
        "update-pipeline.yml",
    ),
    ("PR · refresh candidates", "手动", "pr-candidates.yml"),
    ("CI", "push / PR", "ci.yml"),
)


def _pipeline_workflows_for_bootstrap(repo_web_base: str) -> list[dict[str, str]]:
    base = (repo_web_base or "").strip().rstrip("/")
    out: list[dict[str, str]] = []
    for title, trigger, filename in _PIPELINE_WORKFLOWS:
        rel = f".github/workflows/{filename}"
        blob_href = f"{base}/{rel}" if base else ""
        actions_wf = _github_workflow_ui_href(repo_web_base, filename)
        out.append(
            {
                "label": title,
                "trigger": trigger,
                "workflow_path": rel,
                "blob_href": blob_href,
                "actions_workflow_href": actions_wf,
            }
        )
    return out


def _pipeline_cli_hints_for_bootstrap() -> list[dict[str, str]]:
    return [{"label": a, "command": b} for a, b in _PIPELINE_CLI_HINTS]


def _pipeline_links_for_bootstrap(repo_web_base: str) -> list[dict[str, str]]:
    base = (repo_web_base or "").strip().rstrip("/")
    out: list[dict[str, str]] = []
    for label, rel in _PIPELINE_LINK_ITEMS:
        href = f"{base}/{rel.lstrip('/')}" if base else ""
        out.append({"label": label, "path": rel, "href": href})
    return out


_STATIC = _ROOT / "static"

# 与 ``readonly_api`` 的 ``run_id`` 主键一致：禁止 ``/``、``..`` 等穿越。
_RUN_ID_SAFE = re.compile(r"^[A-Za-z0-9._-]{1,256}$")

# 进程内复用连接池；``httpx.Client`` 对并发 ``get`` 线程安全（见 httpx 文档）。单测可 patch ``_shared_httpx_client``。
_readonly_proxy_http_client: httpx.Client | None = None
_readonly_proxy_http_client_lock = threading.Lock()


def _shared_httpx_client() -> httpx.Client:
    global _readonly_proxy_http_client
    if _readonly_proxy_http_client is not None:
        return _readonly_proxy_http_client
    with _readonly_proxy_http_client_lock:
        if _readonly_proxy_http_client is None:
            _readonly_proxy_http_client = httpx.Client(timeout=30.0)
        return _readonly_proxy_http_client


app = FastAPI(
    title="ai-arch-evolution-admin-console",
    version="0",
    description="演进站点管理端：只读仪表盘与代理；认证与写路径见 ADMIN_WEB_CONSOLE_ROADMAP.md",
)

_cfg = load_settings()
if _cfg.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(_cfg.cors_origins),
        allow_methods=[
            "GET",
            "HEAD",
            "OPTIONS",
            "POST",
            "PATCH",
            "DELETE",
        ],
        allow_headers=[
            "*",
            "If-None-Match",
            "Accept",
            "Authorization",
            "Content-Type",
            "X-Admin-Accounts-Secret",
        ],
        allow_credentials=False,
    )

app.include_router(admin_accounts_router)


@app.get("/health", response_model=None)
def health() -> JSONResponse:
    s = load_settings()
    return JSONResponse(
        {
            "status": "ok",
            "service": "admin-console",
            "readonly_api_base_url": s.readonly_api_base_url,
            "cors_origins_configured": len(s.cors_origins) > 0,
            "dev_bypass": s.dev_bypass,
            "repo_web_base": s.repo_web_base,
            "admin_accounts_enabled": bool(s.admin_accounts_api_secret),
        }
    )


@app.get("/api/me", response_model=None)
def me() -> JSONResponse:
    """占位：后续接 OIDC。本地演示可设 ``ADMIN_DEV_BYPASS=1`` + ``ADMIN_DEV_USER_JSON``。"""
    s = load_settings()
    if s.dev_bypass and s.dev_user is not None:
        body = {"authenticated": True, **s.dev_user}
        return JSONResponse(body)
    return JSONResponse(
        {
            "authenticated": False,
            "sub": None,
            "roles": [],
            "hint": "生产请接 IdP；本地演示见 ADMIN_DEV_BYPASS 与 ADMIN_DEV_USER_JSON（admin-console/README）",
        }
    )


@app.get("/api/bootstrap", response_model=None)
def bootstrap() -> JSONResponse:
    s = load_settings()
    tz_cn = ZoneInfo("Asia/Shanghai")
    server_now = datetime.now(tz_cn).replace(microsecond=0)
    server_time_beijing = server_now.isoformat()
    return JSONResponse(
        {
            "service": "admin-console",
            "server_time_beijing": server_time_beijing,
            "readonly_api_base_url": s.readonly_api_base_url,
            "readonly_proxy_segments": sorted(READONLY_PROXY_SEGMENTS),
            "docs_roadmap": "docs/ADMIN_WEB_CONSOLE_ROADMAP.md",
            "cors_origins_configured": len(s.cors_origins) > 0,
            "repo_web_base": s.repo_web_base,
            "pipeline_links": _pipeline_links_for_bootstrap(s.repo_web_base),
            "pipeline_cli_hints": _pipeline_cli_hints_for_bootstrap(),
            "github_actions_href": _github_actions_href(s.repo_web_base),
            "pipeline_workflows": _pipeline_workflows_for_bootstrap(s.repo_web_base),
            "data_source_catalog": _load_data_source_catalog(),
            "control_plane_roadmap": _load_control_plane_roadmap(),
            "admin_accounts_enabled": bool(s.admin_accounts_api_secret),
        }
    )


def _proxy_readonly_get(
    rel_path: str, request: Request, *, forward_query: bool
) -> Response:
    """``rel_path`` 无前导斜杠，如 ``snapshot`` 或 ``snapshot-history/rid``。"""
    s = load_settings()
    if not s.readonly_api_base_url:
        raise HTTPException(
            status_code=503,
            detail="READONLY_API_BASE_URL not configured",
        )
    url = f"{s.readonly_api_base_url}/{rel_path}"
    if forward_query and request.url.query:
        url = f"{url}?{request.url.query}"
    fwd_headers: dict[str, str] = {}
    if match := request.headers.get("if-none-match"):
        fwd_headers["If-None-Match"] = match
    try:
        r = _shared_httpx_client().get(url, headers=fwd_headers)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    out_headers: dict[str, str] = {}
    for key in ("etag", "cache-control", "content-type"):
        if key in r.headers:
            out_headers[key] = r.headers[key]
    return Response(
        content=r.content,
        status_code=r.status_code,
        headers=out_headers,
    )


@app.get("/api/readonly/snapshot-history/{run_id}", response_model=None)
def proxy_readonly_snapshot_history_run(run_id: str, request: Request) -> Response:
    """代理 ``GET /snapshot-history/{run_id}``（``run_id`` 经字符白名单）。"""
    if not _RUN_ID_SAFE.match(run_id):
        raise HTTPException(status_code=404, detail="invalid run_id")
    return _proxy_readonly_get(
        f"snapshot-history/{run_id}", request, forward_query=False
    )


@app.get("/api/readonly/{segment}", response_model=None)
def proxy_readonly(segment: str, request: Request) -> Response:
    """
    受控 **GET** 代理到 ``readonly_api``（单段路径白名单）；便于管理页同源拉快照而无需浏览器直跨域。

    默认不转发查询串；**``snapshot-history``** 列表需 ``limit``/``offset``，故仅此段转发查询参数。
    """
    if segment not in READONLY_PROXY_SEGMENTS:
        raise HTTPException(status_code=404, detail="segment not allowlisted")
    forward_query = segment == "snapshot-history"
    return _proxy_readonly_get(segment, request, forward_query=forward_query)


@app.get("/", response_model=None)
def index() -> FileResponse:
    index_path = _STATIC / "index.html"
    if not index_path.is_file():
        raise RuntimeError(f"missing static index: {index_path}")
    return FileResponse(index_path, media_type="text/html; charset=utf-8")
