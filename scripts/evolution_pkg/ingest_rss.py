"""RSS 2.0 / Atom **feed** 解析为统一条目 dict（无网络 I/O）。

供 **`ingest_opinion_law`** 与单测复用；每条含 **title / link / summary / pub** 截断规则与历史脚本一致。
"""
from __future__ import annotations

import xml.etree.ElementTree as ET


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
