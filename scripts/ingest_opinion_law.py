#!/usr/bin/env python3
"""
从 ingest_config.json 中的 RSS 与法规/政策 HTML 页抓取条目，汇总为 assets/evolution-candidates.json。

- 仅作「候选线索」：摘要来自提要或标题拼接，非全文法理分析。
- 须人工审阅后再 merge 进 evolution-manifest.json。
- 依赖：Python 3.9+ 标准库（urllib + xml）。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "scripts" / "ingest_config.json"
OUT_PATH = ROOT / "assets" / "evolution-candidates.json"

UA = "Mozilla/5.0 (compatible; EvolutionIngest/1.0; +https://example.local)"
TIMEOUT = 25


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def strip_ns(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def text_or_none(el: ET.Element | None) -> str | None:
    if el is None or el.text is None:
        return None
    t = el.text.strip()
    return t or None


def parse_rss_or_atom(data: bytes) -> list[dict]:
    out: list[dict] = []
    root = ET.fromstring(data)
    tag = strip_ns(root.tag).lower()
    if tag == "rss":
        channel = root.find("channel")
        if channel is None:
            return out
        for item in channel.findall("item"):
            title = text_or_none(item.find("title")) or ""
            link_el = item.find("link")
            link = text_or_none(link_el) or ""
            desc_el = item.find("description")
            summary = text_or_none(desc_el) or ""
            pub = text_or_none(item.find("pubDate")) or ""
            if title or link:
                out.append(
                    {
                        "title": title[:500],
                        "link": link[:2000],
                        "summary": summary[:2000],
                        "pub": pub[:200],
                    }
                )
        return out
    if tag == "feed":
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title_el = entry.find("atom:title", ns)
            title = text_or_none(title_el) or ""
            link = ""
            for le in entry.findall("atom:link", ns):
                if le.get("rel") in (None, "alternate"):
                    link = le.get("href") or ""
                    break
            if not link:
                le = entry.find("atom:link", ns)
                if le is not None:
                    link = le.get("href") or ""
            summ_el = entry.find("atom:summary", ns)
            if summ_el is None:
                summ_el = entry.find("atom:content", ns)
            summary = text_or_none(summ_el) or ""
            pub_el = entry.find("atom:updated", ns)
            if pub_el is None:
                pub_el = entry.find("atom:published", ns)
            pub = text_or_none(pub_el) or ""
            if title or link:
                out.append(
                    {
                        "title": title[:500],
                        "link": link[:2000],
                        "summary": summary[:2000],
                        "pub": pub[:200],
                    }
                )
        return out
    return out


def html_title(data: bytes) -> str:
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


def apply_routes(
    text: str, routes: list[dict]
) -> tuple[list[str], list[str]]:
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


def load_config() -> dict:
    if not CONFIG_PATH.is_file():
        print(f"错误: 缺少 {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def main() -> None:
    cfg = load_config()
    routes = cfg.get("routes") or []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    signals: dict[str, dict] = {}

    if OUT_PATH.is_file():
        try:
            old = json.loads(OUT_PATH.read_text(encoding="utf-8"))
            for s in old.get("signals") or []:
                sid = s.get("id")
                if sid:
                    signals[sid] = s
        except json.JSONDecodeError:
            pass

    for feed in cfg.get("rss_feeds") or []:
        url = feed.get("url")
        if not url:
            continue
        fid = feed.get("id", url)
        default_kind = feed.get("default_kind", "opinion")
        max_items = int(feed.get("max_items") or 15)
        try:
            raw = fetch_bytes(url)
            time.sleep(0.8)
        except (urllib.error.URLError, OSError) as e:
            print(f"[RSS 跳过] {fid}: {e}", file=sys.stderr)
            continue
        items = parse_rss_or_atom(raw)[:max_items]
        for it in items:
            title = it.get("title") or ""
            link = it.get("link") or ""
            summary = it.get("summary") or ""
            blob = f"{title} {summary}"
            kind = default_kind
            if re.search(r"法|条例|立法|草案|修订|征求|意见|公告|规定", blob):
                kind = "law" if kind == "opinion" else kind
            lf, pg = apply_routes(blob, routes)
            sid = stable_id(link or url, title)
            signals[sid] = {
                "id": sid,
                "kind": kind,
                "title": title or "(无标题)",
                "summary": (summary[:800] if summary else f"来源 RSS：{fid}"),
                "weight": "medium",
                "since": now[:10],
                "status": "candidate",
                "source": {
                    "type": "rss",
                    "feed_id": fid,
                    "url": url,
                    "item_link": link,
                    "fetched_at": now,
                },
                "maps_to": {"pages": pg, "lab_factors": lf},
            }

    for page in cfg.get("law_html_pages") or []:
        url = page.get("url")
        if not url:
            continue
        pid = page.get("id", url)
        default_kind = page.get("default_kind", "law")
        try:
            raw = fetch_bytes(url)
            time.sleep(1.0)
        except (urllib.error.URLError, OSError) as e:
            print(f"[页面跳过] {pid}: {e}", file=sys.stderr)
            continue
        title = html_title(raw) or f"页面线索 ({pid})"
        blob = title
        lf, pg = apply_routes(blob, routes)
        sid = stable_id(url, title)
        signals[sid] = {
            "id": sid,
            "kind": default_kind,
            "title": title[:500],
            "summary": f"自法规/政策索引页抓取标题，需人工点开核对正文。页：{pid}",
            "weight": "low",
            "since": now[:10],
            "status": "candidate",
            "source": {
                "type": "law_html",
                "page_id": pid,
                "url": url,
                "fetched_at": now,
            },
            "maps_to": {"pages": pg, "lab_factors": lf},
        }

    out = {
        "schema_version": 1,
        "updated": now[:10],
        "fetched_at": now,
        "notes": "由 scripts/ingest_opinion_law.py 生成；merge 前请人工筛选。",
        "signals": sorted(signals.values(), key=lambda x: x.get("id", "")),
    }
    OUT_PATH.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"已写入 {OUT_PATH}（{len(signals)} 条，含历史去重 id）")


if __name__ == "__main__":
    main()
