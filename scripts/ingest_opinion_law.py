#!/usr/bin/env python3
"""
从 ingest_config.json 中的 RSS、法规/政策 HTML 页与可选 HTTPS JSON 源抓取条目，汇总为 assets/evolution-candidates.json。

- 仅作「候选线索」：摘要来自提要或标题拼接，非全文法理分析。
- 须人工审阅后再 merge 进 evolution-manifest.json。
- 可选配置 require_route_match：为 true 时仅写入至少命中一条 routes 的 RSS/法规/JSON 线索（减噪）。
- 可选 **json_feeds**：侧车或公开 API 的 JSON 数组（或 `items_path` 指向的数组）；字段映射见 **evolution_pkg.ingest_json_http**；须 **https**，遵守 ToS/频率。
- 依赖：Python 3.9+ 标准库（urllib + xml + json）；配置中 URL 须为 **https**。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.parse import urlparse

from evolution_pkg.ingest_json_http import feed_parser_keys, parse_json_feed_body
from evolution_pkg.io import REPO_ROOT

CONFIG_PATH = REPO_ROOT / "scripts" / "ingest_config.json"
MAPS_HINTS_PATH = REPO_ROOT / "scripts" / "maps_to_hints.json"
OUT_PATH = REPO_ROOT / "assets" / "evolution-candidates.json"
SUMMARY_PATH = REPO_ROOT / "ingest-summary.json"

INGEST_PROJECT_URL = "https://smartseanchain.github.io/ai-base-arch-evolution/"
UA = (
    "Mozilla/5.0 (compatible; EvolutionIngest/1.0; +"
    + INGEST_PROJECT_URL
    + ")"
)
TIMEOUT = 25
_KEEP_REVIEW = frozenset({"pending", "noise", "queued_for_manifest"})


def assert_https_ingest_url(url: str, label: str) -> None:
    """仅允许 https，降低误配与内网 SSRF 风险；须在发起请求前调用。"""
    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        raise ValueError(f"{label}: 仅允许 https URL，拒绝 {url!r}")
    if not (parsed.hostname or "").strip():
        raise ValueError(f"{label}: URL 缺少有效主机名: {url!r}")


def validate_config_fetch_urls(cfg: dict) -> None:
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
            assert_https_ingest_url(
                str(u), f"JSON·{jf.get('id', u)}"
            )


def fetch_bytes(url: str) -> bytes:
    assert_https_ingest_url(url, "fetch")
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


def load_maps_to_hints() -> dict:
    if not MAPS_HINTS_PATH.is_file():
        return {}
    try:
        return json.loads(MAPS_HINTS_PATH.read_text(encoding="utf-8"))
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


def load_config() -> dict:
    if not CONFIG_PATH.is_file():
        print(f"错误: 缺少 {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description="抓取 RSS / 法规索引页 / 可选 JSON HTTP → assets/evolution-candidates.json",
    )
    ap.add_argument(
        "--full-pool",
        action="store_true",
        help="本次运行忽略 ingest_config.require_route_match（全量进池，且不清理历史未命中 RSS/法规/JSON 项）",
    )
    ap.add_argument(
        "--write-summary",
        action="store_true",
        help="写入项目根 ingest-summary.json（供 CI 汇总各源成功/失败）",
    )
    args = ap.parse_args(argv)

    cfg = load_config()
    validate_config_fetch_urls(cfg)
    hints_cfg = load_maps_to_hints()
    routes = cfg.get("routes") or []
    require_route_match = bool(cfg.get("require_route_match"))
    if args.full_pool:
        require_route_match = False
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    signals: dict[str, dict] = {}
    feed_reports: list[dict] = []
    law_reports: list[dict] = []
    json_reports: list[dict] = []

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
        rep: dict = {
            "id": fid,
            "url": url,
            "ok": False,
            "items_fetched": 0,
            "error": None,
        }
        try:
            raw = fetch_bytes(url)
            time.sleep(0.8)
        except (urllib.error.URLError, OSError, ValueError) as e:
            rep["error"] = str(e)
            feed_reports.append(rep)
            print(f"[RSS 跳过] {fid}: {e}", file=sys.stderr)
            continue
        items = parse_rss_or_atom(raw)[:max_items]
        rep["ok"] = True
        rep["items_fetched"] = len(items)
        feed_reports.append(rep)
        for it in items:
            title = it.get("title") or ""
            link = it.get("link") or ""
            summary = it.get("summary") or ""
            blob = f"{title} {summary}"
            kind = default_kind
            if re.search(r"法|条例|立法|草案|修订|征求|意见|公告|规定", blob):
                kind = "law" if kind == "opinion" else kind
            lf, pg = apply_routes(blob, routes)
            lf, pg = merge_maps_to_hints(link, title, summary, lf, pg, hints_cfg)
            if require_route_match and not lf and not pg:
                continue
            sid = stable_id(link or url, title)
            prev = signals.get(sid)
            row = {
                "id": sid,
                "kind": kind,
                "title": title or "(无标题)",
                "summary": (summary[:800] if summary else f"来源 RSS：{fid}"),
                "weight": "medium",
                "since": now[:10],
                "status": "candidate",
                "review_state": "pending",
                "source": {
                    "type": "rss",
                    "feed_id": fid,
                    "url": url,
                    "item_link": link,
                    "fetched_at": now,
                },
                "maps_to": {"pages": pg, "lab_factors": lf},
            }
            if prev:
                prs = prev.get("review_state")
                if prs in _KEEP_REVIEW:
                    row["review_state"] = prs
                if prev.get("reviewer_note") is not None:
                    row["reviewer_note"] = prev["reviewer_note"]
            signals[sid] = row

    for page in cfg.get("law_html_pages") or []:
        url = page.get("url")
        if not url:
            continue
        pid = page.get("id", url)
        default_kind = page.get("default_kind", "law")
        lrep: dict = {
            "id": pid,
            "url": url,
            "ok": False,
            "error": None,
        }
        try:
            raw = fetch_bytes(url)
            time.sleep(1.0)
        except (urllib.error.URLError, OSError, ValueError) as e:
            lrep["error"] = str(e)
            law_reports.append(lrep)
            print(f"[页面跳过] {pid}: {e}", file=sys.stderr)
            continue
        title = html_title(raw) or f"页面线索 ({pid})"
        blob = title
        lf, pg = apply_routes(blob, routes)
        lf, pg = merge_maps_to_hints(url, title, "", lf, pg, hints_cfg)
        lrep["ok"] = True
        law_reports.append(lrep)
        if require_route_match and not lf and not pg:
            continue
        sid = stable_id(url, title)
        prev = signals.get(sid)
        row = {
            "id": sid,
            "kind": default_kind,
            "title": title[:500],
            "summary": f"自法规/政策索引页抓取标题，需人工点开核对正文。页：{pid}",
            "weight": "low",
            "since": now[:10],
            "status": "candidate",
            "review_state": "pending",
            "source": {
                "type": "law_html",
                "page_id": pid,
                "url": url,
                "fetched_at": now,
            },
            "maps_to": {"pages": pg, "lab_factors": lf},
        }
        if prev:
            prs = prev.get("review_state")
            if prs in _KEEP_REVIEW:
                row["review_state"] = prs
            if prev.get("reviewer_note") is not None:
                row["reviewer_note"] = prev["reviewer_note"]
        signals[sid] = row

    for jfeed in cfg.get("json_feeds") or []:
        url = jfeed.get("url")
        if not url:
            continue
        fid = jfeed.get("id", url)
        default_kind = jfeed.get("default_kind", "opinion")
        max_items = int(jfeed.get("max_items") or 20)
        items_path = str(jfeed.get("items_path") or "")
        kt, kl, ks = feed_parser_keys(jfeed if isinstance(jfeed, dict) else {})
        jrep: dict = {
            "id": fid,
            "url": url,
            "ok": False,
            "items_fetched": 0,
            "items_raw": 0,
            "error": None,
        }
        try:
            raw = fetch_bytes(url)
            time.sleep(0.8)
        except (urllib.error.URLError, OSError, ValueError) as e:
            jrep["error"] = str(e)
            json_reports.append(jrep)
            print(f"[JSON 跳过] {fid}: {e}", file=sys.stderr)
            continue
        try:
            items, n_raw = parse_json_feed_body(
                raw,
                items_path=items_path,
                keys_title=kt,
                keys_link=kl,
                keys_summary=ks,
                max_items=max_items,
            )
        except (json.JSONDecodeError, TypeError, KeyError, ValueError) as e:
            jrep["error"] = str(e)
            json_reports.append(jrep)
            print(f"[JSON 解析失败] {fid}: {e}", file=sys.stderr)
            continue
        jrep["ok"] = True
        jrep["items_raw"] = n_raw
        jrep["items_fetched"] = len(items)
        json_reports.append(jrep)
        for it in items:
            title = it.get("title") or ""
            link = it.get("link") or ""
            summary = it.get("summary") or ""
            blob = f"{title} {summary}"
            kind = default_kind
            if re.search(r"法|条例|立法|草案|修订|征求|意见|公告|规定", blob):
                kind = "law" if kind == "opinion" else kind
            lf, pg = apply_routes(blob, routes)
            lf, pg = merge_maps_to_hints(link, title, summary, lf, pg, hints_cfg)
            if require_route_match and not lf and not pg:
                continue
            sid = stable_id(link or url, title)
            prev = signals.get(sid)
            row = {
                "id": sid,
                "kind": kind,
                "title": title or "(无标题)",
                "summary": (
                    (summary[:800] if summary else f"来源 JSON·{fid}")
                ),
                "weight": "medium",
                "since": now[:10],
                "status": "candidate",
                "review_state": "pending",
                "source": {
                    "type": "json_http",
                    "feed_id": fid,
                    "url": url,
                    "item_link": link,
                    "fetched_at": now,
                },
                "maps_to": {"pages": pg, "lab_factors": lf},
            }
            if prev:
                prs = prev.get("review_state")
                if prs in _KEEP_REVIEW:
                    row["review_state"] = prs
                if prev.get("reviewer_note") is not None:
                    row["reviewer_note"] = prev["reviewer_note"]
            signals[sid] = row

    if require_route_match:
        for sid in list(signals.keys()):
            s = signals[sid]
            mt = s.get("maps_to") or {}
            if (mt.get("pages") or mt.get("lab_factors")):
                continue
            src = s.get("source") or {}
            if src.get("type") in ("rss", "law_html", "json_http"):
                del signals[sid]

    out = {
        "schema_version": 1,
        "updated": now[:10],
        "fetched_at": now,
        "notes": "由 scripts/ingest_opinion_law.py 生成；merge 前请人工筛选。"
        + (
            " require_route_match=on：未命中 routes 的 RSS/法规/JSON 项已丢弃。"
            if require_route_match
            else ""
        ),
        "signals": sorted(signals.values(), key=lambda x: x.get("id", "")),
    }
    OUT_PATH.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"已写入 {OUT_PATH}（{len(signals)} 条，含历史去重 id）")

    if args.write_summary:
        summary_doc = {
            "schema_version": 1,
            "generated_at": now,
            "require_route_match": require_route_match,
            "full_pool": bool(args.full_pool),
            "feeds": feed_reports,
            "law_pages": law_reports,
            "json_feeds": json_reports,
            "signals_count": len(signals),
        }
        SUMMARY_PATH.write_text(
            json.dumps(summary_doc, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"已写入 {SUMMARY_PATH}")


if __name__ == "__main__":
    main(sys.argv[1:])
