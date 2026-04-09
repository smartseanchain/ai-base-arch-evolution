"""
只读 HTTP API：从磁盘读取已提交的 JSON（不写库、不改 manifest）。
运行（仓库根目录）:
  PYTHONPATH=scripts python3 -m uvicorn readonly_api:app --reload --port 8099

或先: pip install -r requirements-api.txt
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
except ImportError:
    print(
        "缺少 fastapi/uvicorn。请执行: python3 -m pip install -r requirements-api.txt",
        file=sys.stderr,
    )
    raise

app = FastAPI(title="ai-base-arch-evolution-readonly", version="1")


def _read_json(rel: str) -> dict | JSONResponse:
    p = _ROOT / rel
    if not p.is_file():
        return JSONResponse({"error": "not_found", "path": rel}, status_code=404)
    return json.loads(p.read_text(encoding="utf-8"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/snapshot")
def snapshot() -> dict | JSONResponse:
    return _read_json("assets/analysis-snapshot.json")


@app.get("/trends")
def trends() -> dict | JSONResponse:
    return _read_json("assets/sediment-trends.json")


@app.get("/manifest")
def manifest() -> dict | JSONResponse:
    return _read_json("assets/evolution-manifest.json")
