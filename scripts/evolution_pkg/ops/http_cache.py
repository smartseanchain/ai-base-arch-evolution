"""JSON 响应常用 Cache-Control 与 RFC 9110 条件 GET（If-None-Match → 304）。"""
from __future__ import annotations

import hashlib
import json
from typing import NamedTuple, Optional

CACHE_JSON_REVALIDATE = "public, max-age=0, must-revalidate"
CACHE_JSON_DYNAMIC = "private, no-store"


class PreparedJsonCache(NamedTuple):
    """供 **`readonly_api`** 等映射为 HTTP 响应：304 时 **body** 为 ``None``。"""

    status_code: int
    body: bytes | None
    headers: dict[str, str]


def etag_for_bytes(raw: bytes) -> str:
    """SHA-256 前缀强 ETag 外观（双引号包裹），与历史 **`readonly_api`** 行为一致。"""
    return '"' + hashlib.sha256(raw).hexdigest()[:24] + '"'


def if_none_match_prefers_304(if_none_match: Optional[str], etag: str) -> bool:
    """``If-None-Match`` 与当前 ETag 命中时返回 304（含 ``*``、弱标签 ``W/``、多值逗号分隔）。"""
    if not if_none_match or not if_none_match.strip():
        return False
    s = if_none_match.strip()
    if s == "*":
        return True
    for token in s.split(","):
        t = token.strip()
        if t.startswith("W/"):
            t = t[2:].strip()
        if t == etag:
            return True
    return False


def _json_cache_headers(etag: str, cache_control: str) -> dict[str, str]:
    return {"ETag": etag, "Cache-Control": cache_control}


def prepare_revalidated_json(
    raw: bytes, if_none_match: Optional[str]
) -> PreparedJsonCache:
    """
    磁盘已提交 JSON 字节：``must-revalidate`` + 条件 GET。

    调用方负责 404（文件不存在）与 ``media_type``；本函数只处理 **200 / 304**。
    """
    etag = etag_for_bytes(raw)
    cc = CACHE_JSON_REVALIDATE
    if if_none_match_prefers_304(if_none_match, etag):
        return PreparedJsonCache(304, None, _json_cache_headers(etag, cc))
    return PreparedJsonCache(200, raw, _json_cache_headers(etag, cc))


def prepare_dynamic_json(
    data: object,
    if_none_match: Optional[str],
    *,
    status_code: int = 200,
) -> PreparedJsonCache:
    """
    内存构造 JSON（如 SQLite 列表/单条文档）：``private, no-store``。

    与 **`readonly_api`** 一致：仅 **status_code == 200** 时参与 **If-None-Match → 304**。
    """
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
    etag = etag_for_bytes(raw)
    cc = CACHE_JSON_DYNAMIC
    if status_code == 200 and if_none_match_prefers_304(if_none_match, etag):
        return PreparedJsonCache(304, None, _json_cache_headers(etag, cc))
    return PreparedJsonCache(status_code, raw, _json_cache_headers(etag, cc))
