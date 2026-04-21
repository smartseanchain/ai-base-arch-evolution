"""RSS / 法规页 / **json_feeds** → **`assets/evolution-candidates.json`** 抓取编排。

**推荐**：``PYTHONPATH=scripts python3 -m evolution_pkg.ingest_opinion_pool``（参数同根目录 **`ingest_opinion_law.py`**）；根脚本为兼容薄壳。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
from evolution_pkg.beijing_time import now_iso_beijing
from evolution_pkg.ingest_fetch import (
    DEFAULT_PROJECT_PAGE_URL,
    INGEST_FETCH_TIMEOUT,
    fetch_bytes as _fetch_bytes_impl,
    user_agent_for_evolution_ingest,
)
from evolution_pkg.ingest_https import validate_config_fetch_urls
from evolution_pkg.ingest_json_http import feed_parser_keys, parse_json_feed_body
from evolution_pkg.ingest_maps import (
    apply_routes,
    html_title,
    load_maps_to_hints,
    merge_maps_to_hints,
    stable_id,
)
from evolution_pkg.ingest_rss import parse_rss_or_atom
from evolution_pkg.io import INGEST_CONFIG_JSON_PATH, REPO_ROOT

CONFIG_PATH = INGEST_CONFIG_JSON_PATH
OUT_PATH = REPO_ROOT / "assets" / "evolution-candidates.json"
SUMMARY_PATH = REPO_ROOT / "ingest-summary.json"

INGEST_PROJECT_URL = DEFAULT_PROJECT_PAGE_URL
UA = user_agent_for_evolution_ingest(INGEST_PROJECT_URL)
TIMEOUT = int(INGEST_FETCH_TIMEOUT)
_KEEP_REVIEW = frozenset({"pending", "noise", "queued_for_manifest"})
_FETCH_PACING_KEYS = frozenset(
    {"after_rss_fetch", "after_law_html_fetch", "after_json_feed_fetch"}
)
_DEFAULT_FETCH_PACING: dict[str, float] = {
    "after_rss_fetch": 0.8,
    "after_law_html_fetch": 1.0,
    "after_json_feed_fetch": 0.8,
}


def fetch_bytes(url: str) -> bytes:
    """同源 **GET**；UA/超时与模块级 **``UA``** / **``TIMEOUT``** 对齐。"""
    return _fetch_bytes_impl(url, user_agent=UA, timeout=float(TIMEOUT))


def load_config() -> dict | None:
    if not CONFIG_PATH.is_file():
        print(f"错误: 缺少 {CONFIG_PATH}", file=sys.stderr)
        return None
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _validate_fetch_pacing(cfg: dict) -> None:
    """可选 **``fetch_pacing``**：控制各源两次 GET 之间的间隔（秒），见 **INTEL** 手册 §2a。"""
    raw = cfg.get("fetch_pacing")
    if raw is None:
        return
    if not isinstance(raw, dict):
        raise ValueError("ingest_config.fetch_pacing 须为对象")
    for k, v in raw.items():
        if k not in _FETCH_PACING_KEYS:
            raise ValueError(
                f"ingest_config.fetch_pacing: 未知键 {k!r}；允许: {sorted(_FETCH_PACING_KEYS)}"
            )
        try:
            n = float(v)
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"ingest_config.fetch_pacing.{k} 须为非负数字，拒绝 {v!r}"
            ) from e
        if n < 0 or n > 120.0:
            raise ValueError(
                f"ingest_config.fetch_pacing.{k} 须在 [0, 120] 秒内，拒绝 {n}"
            )


def _pause_after_fetch(cfg: dict, key: str) -> None:
    """在成功 **GET** 之后休眠；**key** 为 **``after_rss_fetch``** / **``after_law_html_fetch``** / **``after_json_feed_fetch``**。"""
    pacing = cfg.get("fetch_pacing")
    if not isinstance(pacing, dict):
        pacing = {}
    default = _DEFAULT_FETCH_PACING[key]
    try:
        sec = float(pacing.get(key, default))
    except (TypeError, ValueError):
        sec = default
    if sec > 0:
        time.sleep(sec)


def main(argv: list[str] | None = None) -> int:
    """抓取并入池；成功返回 **0**。"""
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
    if cfg is None:
        return 1
    validate_config_fetch_urls(cfg)
    _validate_fetch_pacing(cfg)
    hints_cfg = load_maps_to_hints()
    routes = cfg.get("routes") or []
    require_route_match = bool(cfg.get("require_route_match"))
    if args.full_pool:
        require_route_match = False
    now = now_iso_beijing()
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
            _pause_after_fetch(cfg, "after_rss_fetch")
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
            _pause_after_fetch(cfg, "after_law_html_fetch")
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
            _pause_after_fetch(cfg, "after_json_feed_fetch")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
