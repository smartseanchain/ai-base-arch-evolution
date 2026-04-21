"""ingest 配置中对外抓取 URL 的 **https-only** 校验（无网络 I/O）。

供 **`ingest_opinion_law.py`** 在发起请求前调用，与 **`evolution_pkg.ingest_json_http`** 的 JSON 侧车解析分工。
"""
from __future__ import annotations

from urllib.parse import urlparse


def assert_https_ingest_url(url: str, label: str) -> None:
    """仅允许 https，降低误配与内网 SSRF 风险；须在发起请求前调用。"""
    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        raise ValueError(f"{label}: 仅允许 https URL，拒绝 {url!r}")
    if not (parsed.hostname or "").strip():
        raise ValueError(f"{label}: URL 缺少有效主机名: {url!r}")


def validate_config_fetch_urls(cfg: dict) -> None:
    """校验 ``ingest_config`` 内所有 RSS / 法规页 / json_feeds 的 ``url``。"""
    for feed in cfg.get("rss_feeds") or []:
        u = feed.get("url")
        if u:
            assert_https_ingest_url(str(u), f"RSS·{feed.get('id', u)}")
    for page in cfg.get("law_html_pages") or []:
        u = page.get("url")
        if u:
            assert_https_ingest_url(str(u), f"法规页·{page.get('id', u)}")
    for jf in cfg.get("json_feeds") or []:
        u = jf.get("url")
        if u:
            assert_https_ingest_url(str(u), f"JSON·{jf.get('id', u)}")
