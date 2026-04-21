"""ingest 侧 **HTTPS GET** 拉取正文（字节），供 **`ingest_opinion_law`** 等脚本复用。

与 **`evolution_pkg.ingest_https`** 分工：本模块在请求前再次 **assert https**；默认 User-Agent 含项目页链。
"""
from __future__ import annotations

import urllib.request

from evolution_pkg.ingest_https import assert_https_ingest_url

# 与历史 ``ingest_opinion_law.INGEST_PROJECT_URL`` 对齐；fork 可改脚本层再传入 UA。
DEFAULT_PROJECT_PAGE_URL = "https://smartseanchain.github.io/ai-base-arch-evolution/"
INGEST_FETCH_TIMEOUT = 25.0


def user_agent_for_evolution_ingest(project_page_url: str = DEFAULT_PROJECT_PAGE_URL) -> str:
    return (
        "Mozilla/5.0 (compatible; EvolutionIngest/1.0; +"
        + project_page_url
        + ")"
    )


def fetch_bytes(
    url: str,
    *,
    user_agent: str | None = None,
    timeout: float = INGEST_FETCH_TIMEOUT,
) -> bytes:
    assert_https_ingest_url(url, "fetch")
    ua = user_agent if user_agent is not None else user_agent_for_evolution_ingest()
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()
