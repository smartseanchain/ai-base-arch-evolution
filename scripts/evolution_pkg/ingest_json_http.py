"""
从 HTTPS JSON 端点解析条目列表，供 ingest_opinion_law 合并进 evolution-candidates。

设计对齐「侧车 / 公开 API 消费者」模式：配置显式 URL 与字段映射，不内置任何第三方常数 URL。
仅处理 JSON；须遵守对方 ToS 与频率；本模块不做鉴权密钥展开（避免把 secret 写进 ingest_config）。
"""
from __future__ import annotations

import json
from typing import Any


def _walk_path(obj: Any, parts: list[str]) -> Any:
    cur: Any = obj
    for p in parts:
        if not p:
            continue
        if not isinstance(cur, dict):
            raise TypeError(f"路径 {parts!r} 在 {p!r} 处遇到非对象")
        if p not in cur:
            raise KeyError(f"路径缺少键 {p!r}")
        cur = cur[p]
    return cur


def resolve_items_list(root: Any, items_path: str) -> list[Any]:
    """
    items_path 为空：root 须为 list。
    否则为点分键路径，如 \"data\"、\"response.items\"，末端须为 list。
    """
    path = (items_path or "").strip()
    if not path:
        if not isinstance(root, list):
            raise TypeError("items_path 为空时，JSON 根须为数组")
        return root
    parts = [x for x in path.split(".") if x]
    end = _walk_path(root, parts)
    if not isinstance(end, list):
        raise TypeError(f"items_path {items_path!r} 末端须为数组，实际为 {type(end).__name__}")
    return end


def _first_text(d: dict[str, Any], keys: list[str], max_len: int) -> str:
    for k in keys:
        if k not in d:
            continue
        v = d[k]
        if v is None:
            continue
        if isinstance(v, str):
            s = v.strip()
        elif isinstance(v, (int, float, bool)):
            s = str(v).strip()
        else:
            continue
        if s:
            return s[:max_len]
    return ""


def normalize_item(
    raw: Any,
    *,
    keys_title: list[str],
    keys_link: list[str],
    keys_summary: list[str],
) -> dict[str, str] | None:
    """从单条 JSON 对象抽出 title / link / summary；无效则返回 None。"""
    if not isinstance(raw, dict):
        return None
    title = _first_text(raw, keys_title, 500)
    link = _first_text(raw, keys_link, 2000)
    summary = _first_text(raw, keys_summary, 2000)
    if not title and not link:
        return None
    return {"title": title, "link": link, "summary": summary}


def parse_json_feed_body(
    data: bytes,
    *,
    items_path: str,
    keys_title: list[str],
    keys_link: list[str],
    keys_summary: list[str],
    max_items: int,
) -> tuple[list[dict[str, str]], int]:
    """
    解析响应体；返回 (规范化条目, 原始列表长度截断前)。
    """
    root = json.loads(data.decode("utf-8"))
    raw_list = resolve_items_list(root, items_path)
    n_raw = len(raw_list)
    slice_list = raw_list[: max(0, int(max_items))]
    out: list[dict[str, str]] = []
    for raw in slice_list:
        norm = normalize_item(
            raw,
            keys_title=keys_title,
            keys_link=keys_link,
            keys_summary=keys_summary,
        )
        if norm:
            out.append(norm)
    return out, n_raw


def feed_parser_keys(feed: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    """单条 json_feed 配置上的字段键优先序。"""
    default_title = ["title", "name", "headline", "text", "word"]
    default_link = ["link", "url", "href"]
    default_summary = ["summary", "description", "desc", "snippet", "content", "intro"]

    def pick(key: str, fallback: list[str]) -> list[str]:
        v = feed.get(key)
        if isinstance(v, list) and all(isinstance(x, str) for x in v):
            cleaned = [x.strip() for x in v if x and str(x).strip()]
            return cleaned if cleaned else fallback
        return fallback

    return (
        pick("keys_title", default_title),
        pick("keys_link", default_link),
        pick("keys_summary", default_summary),
    )
