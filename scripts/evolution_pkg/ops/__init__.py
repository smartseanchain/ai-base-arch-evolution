"""
运维域：与 HTTP 缓存再验证相关的纯函数（**无 FastAPI**），供 **`readonly_api`** 等复用。

六域说明见仓库 **`docs/INTELLIGENCE_SIX_DOMAINS.md`**。
"""
from __future__ import annotations

from .http_cache import (
    CACHE_JSON_DYNAMIC,
    CACHE_JSON_REVALIDATE,
    PreparedJsonCache,
    etag_for_bytes,
    if_none_match_prefers_304,
    prepare_dynamic_json,
    prepare_revalidated_json,
)

__all__ = [
    "CACHE_JSON_DYNAMIC",
    "CACHE_JSON_REVALIDATE",
    "PreparedJsonCache",
    "etag_for_bytes",
    "if_none_match_prefers_304",
    "prepare_dynamic_json",
    "prepare_revalidated_json",
]
