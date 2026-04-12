"""
只读 HTTP API：从磁盘读取已提交的 JSON（不写库、不改 manifest）；
本地 **`data/evolution.db`** 存在时提供快照**历史**元数据与按 run_id 取全文。

**磁盘 JSON** 路由真源：**``evolution_pkg.readonly_disk_routes.READONLY_DISK_JSON_ROUTES``**
（与仓库根 **docs/DATA_CONTRACTS.md** §8.1 总表对读）。
另：**`/health`**（合成 JSON）、**`/snapshot-history`**、**`/snapshot-history/{run_id}`**（SQLite 侧车）。

磁盘 JSON 与动态历史 JSON 均带 **ETag**（SHA-256 前缀）与相应 **Cache-Control**；请求头 **If-None-Match**
与当前 ETag 一致时返回 **304**（无正文），便于缓存再验证。

运行（仓库根目录）:
  PYTHONPATH=scripts python3 -m uvicorn readonly_api:app --reload --port 8099

或先: pip install -r requirements-api.txt

OpenAPI: GET /openapi.json · Swagger UI: GET /docs。部署与 CORS/鉴权见 docs/INTEGRATION_AND_READONLY_API.md。
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, Optional, Union

from evolution_pkg.ops.http_cache import prepare_dynamic_json, prepare_revalidated_json

_ROOT = Path(__file__).resolve().parent.parent

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse, Response
except ImportError:
    print(
        "缺少 fastapi/uvicorn。请执行: python3 -m pip install -r requirements-api.txt",
        file=sys.stderr,
    )
    raise

app = FastAPI(title="ai-base-arch-evolution-readonly", version="1")


def _json_file_response(
    rel: str, if_none_match: Optional[str] = None
) -> Union[Response, JSONResponse]:
    p = _ROOT / rel
    if not p.is_file():
        return JSONResponse(
            {"error": "not_found", "path": rel},
            status_code=404,
            headers={"Cache-Control": "no-store"},
        )
    prep = prepare_revalidated_json(p.read_bytes(), if_none_match)
    if prep.body is None:
        return Response(status_code=304, headers=prep.headers)
    return Response(
        content=prep.body,
        media_type="application/json; charset=utf-8",
        headers=prep.headers,
    )


def _json_body_response(
    data: object,
    status_code: int = 200,
    if_none_match: Optional[str] = None,
) -> Response:
    prep = prepare_dynamic_json(
        data, if_none_match, status_code=status_code
    )
    if prep.body is None:
        return Response(status_code=304, headers=prep.headers)
    return Response(
        content=prep.body,
        status_code=prep.status_code,
        media_type="application/json; charset=utf-8",
        headers=prep.headers,
    )


def _make_disk_json_endpoint(
    rel_path: str, operation_name: str, doc: str
) -> Callable[[Request], Union[Response, JSONResponse]]:
    def _endpoint(request: Request) -> Union[Response, JSONResponse]:
        return _json_file_response(
            rel_path, request.headers.get("if-none-match")
        )

    _endpoint.__name__ = operation_name
    _endpoint.__doc__ = doc
    return _endpoint


def _register_disk_json_routes() -> None:
    from evolution_pkg.readonly_disk_routes import READONLY_DISK_JSON_ROUTES

    for spec in READONLY_DISK_JSON_ROUTES:
        op = "readonly_get_" + spec.path.strip("/").replace("-", "_")
        app.get(spec.path, response_model=None, description=spec.description)(
            _make_disk_json_endpoint(spec.rel_path, op, spec.description)
        )


@app.get("/health", response_model=None)
def health() -> Response:
    body = b'{"status":"ok"}'
    return Response(
        content=body,
        media_type="application/json; charset=utf-8",
        headers={"Cache-Control": "no-cache"},
    )


_register_disk_json_routes()


@app.get("/snapshot-history", response_model=None)
def snapshot_history(
    request: Request, limit: int = 30, offset: int = 0
) -> Response:
    """SQLite ``analysis_snapshot_history`` 元数据；无库或空表则 ``total=0``。"""
    from evolution_pkg.analysis_snapshot_history import count_rows, list_meta

    lim = max(1, min(limit, 500))
    off = max(0, offset)
    total = count_rows()
    rows = list_meta(limit=lim, offset=off)
    payload: dict[str, object] = {
        "total": total,
        "limit": lim,
        "offset": off,
        "rows": rows,
    }
    return _json_body_response(
        payload, if_none_match=request.headers.get("if-none-match")
    )


@app.get("/snapshot-history/{run_id}", response_model=None)
def snapshot_history_by_run(
    run_id: str, request: Request
) -> Union[Response, JSONResponse]:
    from evolution_pkg.analysis_snapshot_history import get_full

    doc = get_full(run_id)
    if doc is None:
        return JSONResponse(
            {"error": "not_found", "run_id": run_id},
            status_code=404,
            headers={"Cache-Control": "no-store"},
        )
    return _json_body_response(
        doc, if_none_match=request.headers.get("if-none-match")
    )
