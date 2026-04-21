"""ingest 侧 **routes / maps_to_hints** 归并与 **候选 id** 纯逻辑（无网络）。

与 **`ingest_opinion_law`**、**`validate_golden_mapping`** 共用；**`load_maps_to_hints`** 默认读仓库 **`maps_to_hints.json`**（**`MAPS_TO_HINTS_JSON_PATH`**）。
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from evolution_pkg.io import MAPS_TO_HINTS_JSON_PATH


def html_title(data: bytes) -> str:
    """从 HTML 字节串抽取标题（og:title 优先，否则 ``<title>``）。"""
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        return ""
    m = re.search(
        r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']',
        text,
        re.I,
    )
    if m:
        return m.group(1).strip()[:500]
    m = re.search(r"<title[^>]*>([^<]+)</title>", text, re.I)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()[:500]
    return ""


def stable_id(link: str, title: str) -> str:
    h = hashlib.sha256(f"{link}\n{title}".encode("utf-8")).hexdigest()[:12]
    return f"ing_{h}"


def apply_routes(text: str, routes: list[dict]) -> tuple[list[str], list[str]]:
    factors: set[str] = set()
    pages: set[str] = set()
    for r in routes:
        pat = r.get("match", "")
        if not pat:
            continue
        try:
            if not re.search(pat, text, re.I):
                continue
        except re.error:
            continue
        for x in r.get("lab_factors") or []:
            factors.add(x)
        for x in r.get("pages") or []:
            pages.add(x)
    return sorted(factors), sorted(pages)


def load_maps_to_hints(*, hints_path: Path | None = None) -> dict:
    """读取 **maps_to_hints** JSON；缺文件或非法 JSON 时返回 ``{}``。"""
    p = hints_path or MAPS_TO_HINTS_JSON_PATH
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def merge_maps_to_hints(
    link: str,
    title: str,
    summary: str,
    lab_factors: list[str],
    pages: list[str],
    hints_cfg: dict,
) -> tuple[list[str], list[str]]:
    fs = set(lab_factors)
    ps = set(pages)
    blob = f"{title} {summary}"
    host = ""
    if link:
        try:
            host = (urlparse(link).hostname or "").lower()
        except Exception:
            host = ""
    for suffix, m in (hints_cfg.get("host_suffixes") or {}).items():
        suf = suffix.lower().lstrip(".")
        if host == suf or host.endswith("." + suf):
            ps.update(m.get("pages") or [])
            fs.update(m.get("lab_factors") or [])
    for row in hints_cfg.get("keyword_routes") or []:
        pat = row.get("match", "")
        if not pat:
            continue
        try:
            if re.search(pat, blob, re.I):
                ps.update(row.get("pages") or [])
                fs.update(row.get("lab_factors") or [])
        except re.error:
            continue
    return sorted(fs), sorted(ps)
