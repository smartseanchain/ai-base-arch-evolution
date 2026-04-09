#!/usr/bin/env python3
"""
分析引擎：读取 manifest / candidates，生成模块与因子热力、共现与进化提示；
可选将日摘要写入 data/sediment.json，并双写到 data/evolution.db（SQLite）。
对 track_closure 规则比对 evolution-hint-decisions，输出 hint_closure_gaps。

输出: assets/analysis-snapshot.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from lineage_utils import build_run_block

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "evolution-manifest.json"
CANDIDATES = ROOT / "assets" / "evolution-candidates.json"
OUT = ROOT / "assets" / "analysis-snapshot.json"
SEDIMENT = ROOT / "data" / "sediment.json"
HINT_RULES_PATH = ROOT / "scripts" / "evolution-hint-rules.json"
HINT_DECISIONS_PATH = ROOT / "assets" / "evolution-hint-decisions.json"


def load_json(p: Path) -> dict[str, Any]:
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


ALLOWED_REVIEW_STATE = frozenset({"pending", "noise", "queued_for_manifest"})


def effective_review_state(sig: dict) -> str:
    r = sig.get("review_state") or "pending"
    if r in ALLOWED_REVIEW_STATE:
        return str(r)
    return "pending"


def track_closure_rule_ids(rules_doc: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for rule in rules_doc.get("rules") or []:
        if not rule.get("track_closure"):
            continue
        rid = rule.get("id")
        if rid is not None and str(rid).strip():
            out.add(str(rid).strip())
    return out


def closed_rule_ids_from_decisions(doc: dict[str, Any]) -> set[str]:
    """done / rejected 且带 rule_id 视为已闭环（延期 deferred 不算）。"""
    out: set[str] = set()
    for row in doc.get("decisions") or []:
        if not isinstance(row, dict):
            continue
        if row.get("action") not in ("done", "rejected"):
            continue
        rid = row.get("rule_id")
        if isinstance(rid, str) and rid.strip():
            out.add(rid.strip())
    return out


def compute_hint_closure_gaps(
    json_hints: list[dict[str, Any]],
    tracked: set[str],
    closed: set[str],
) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    seen: set[str] = set()
    for h in json_hints:
        if not isinstance(h, dict):
            continue
        rid = h.get("rule_id")
        if not isinstance(rid, str) or not rid.strip():
            continue
        rid = rid.strip()
        if rid not in tracked or rid in closed or rid in seen:
            continue
        seen.add(rid)
        text = h.get("text")
        t = (text if isinstance(text, str) else "")[:200]
        gaps.append({"rule_id": rid, "text": t})
    return gaps


def hint_decisions_stats(doc: dict[str, Any]) -> dict[str, Any]:
    """与 evolution-hint-decisions.json 对齐的汇总，写入 analysis-snapshot.sources。"""
    by_action = {"done": 0, "rejected": 0, "deferred": 0}
    decs = doc.get("decisions")
    if not isinstance(decs, list):
        return {"total": 0, "by_action": dict(by_action)}
    n = 0
    for row in decs:
        if not isinstance(row, dict):
            continue
        n += 1
        a = row.get("action")
        if a in by_action:
            by_action[str(a)] += 1
    return {"total": n, "by_action": dict(by_action)}


def candidate_review_breakdown(candidates: dict) -> dict[str, int]:
    bd = {"pending": 0, "noise": 0, "queued_for_manifest": 0}
    for s in candidates.get("signals") or []:
        if s.get("status") not in (None, "candidate"):
            continue
        rs = effective_review_state(s)
        if rs in bd:
            bd[rs] += 1
        else:
            bd["pending"] += 1
    return bd


def collect_signals(manifest: dict, candidates: dict) -> list[dict]:
    out: list[dict] = []
    for s in manifest.get("signals") or []:
        x = dict(s)
        x["_origin"] = "manifest"
        out.append(x)
    for s in candidates.get("signals") or []:
        if s.get("status") != "candidate" and s.get("status") is not None:
            continue
        if effective_review_state(s) == "noise":
            continue
        x = dict(s)
        x["_origin"] = "candidate"
        out.append(x)
    return out


def load_hint_rules() -> dict[str, Any]:
    if HINT_RULES_PATH.is_file():
        try:
            return json.loads(HINT_RULES_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "rules": [],
        "top_factors_template": (
            "当前热力靠前的沙盘因子：{top_factors}——打开沙盘工坊勾选对应项做一轮压测。"
        ),
        "fallback_hint": (
            "信号较少：优先跑 ingest 抓取或手工充实 manifest，再重新执行本分析脚本。"
        ),
    }


def _hint_obj(
    text: str,
    rule_id: str | None,
    rule: dict[str, Any] | None = None,
) -> dict[str, Any]:
    o: dict[str, Any] = {"text": text, "rule_id": rule_id}
    if rule:
        tp = rule.get("target_pages")
        if isinstance(tp, list) and tp:
            o["target_pages"] = [str(p) for p in tp if p]
        ah = rule.get("anchor_hint")
        if isinstance(ah, str) and ah.strip():
            o["anchor_hint"] = ah.strip()
    return o


def evaluate_hint_rules(
    fac_c: Counter,
    signals_count: int,
    rules_doc: dict[str, Any],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rule in rules_doc.get("rules") or []:
        fm = rule.get("factors_min") or {}
        if any(fac_c.get(k, 0) < int(v) for k, v in fm.items()):
            continue
        smin = rule.get("signals_count_min")
        if smin is not None and signals_count < int(smin):
            continue
        rid = rule.get("id")
        rid_s = str(rid) if rid is not None else None
        tpl = rule.get("hint_template")
        plain = rule.get("hint")
        if tpl:
            out.append(
                _hint_obj(tpl.format(signals_count=signals_count), rid_s, rule)
            )
        elif plain:
            out.append(_hint_obj(str(plain), rid_s, rule))
    return out


def compute_diff_hints(
    prev: dict[str, Any] | None,
    factor_heat: list[dict],
    cooccurrence: list[dict],
    manifest_n: int,
    candidate_n: int,
) -> list[dict[str, Any]]:
    if not prev:
        return []
    hints: list[dict[str, Any]] = []
    prev_fac = [x["factor"] for x in (prev.get("factor_heat") or [])[:8]]
    curr_fac = [x["factor"] for x in factor_heat[:8]]
    prev_top_set = set(prev_fac[:8])
    new_in_top = [f for f in curr_fac[:5] if f not in prev_top_set]
    if new_in_top:
        hints.append(
            _hint_obj(
                "相较上期快照，热力因子新进入前列："
                + "、".join(new_in_top)
                + "——建议核对 manifest/候选映射是否反映新焦点。",
                "diff_factor_top",
            )
        )

    prev_co: dict[tuple[str, str], int] = {}
    for x in prev.get("cooccurrence") or []:
        pr = x.get("pair")
        if isinstance(pr, list) and len(pr) == 2:
            prev_co[tuple(sorted((str(pr[0]), str(pr[1]))))] = int(x.get("count") or 0)

    co_added = 0
    for row in cooccurrence[:10]:
        pr = row.get("pair")
        if not isinstance(pr, list) or len(pr) != 2:
            continue
        p = tuple(sorted((str(pr[0]), str(pr[1]))))
        c = int(row.get("count") or 0)
        old = prev_co.get(p)
        if old is None:
            hints.append(
                _hint_obj(
                    f"共现新出现：{' × '.join(p)}（count={c}）——可查复合表是否需补传导说明。",
                    "diff_cooccurrence",
                    {
                        "target_pages": ["synthesis.html"],
                        "anchor_hint": "复合表 / §7",
                    },
                )
            )
            co_added += 1
        elif c > old:
            hints.append(
                _hint_obj(
                    f"共现增强：{' × '.join(p)}（{old}→{c}）——关注对应页面交叉叙事。",
                    "diff_cooccurrence",
                    {"target_pages": ["synthesis.html"]},
                )
            )
            co_added += 1
        if co_added >= 2:
            break

    prev_src = prev.get("sources") or {}
    pm = prev_src.get("manifest_signals")
    pc = prev_src.get("candidate_signals")
    if isinstance(pm, int) and manifest_n > pm:
        hints.append(
            _hint_obj(
                f"已入库信号较上期增加 {manifest_n - pm} 条（{pm}→{manifest_n}），"
                "建议跑一轮沙盘与 §7 对行。",
                "diff_manifest_count",
                {"target_pages": ["lab.html", "synthesis.html"]},
            )
        )
    if isinstance(pc, int) and candidate_n > pc:
        hints.append(
            _hint_obj(
                f"候选较上期增加 {candidate_n - pc} 条——可安排双周审阅或减噪。",
                "diff_candidate_count",
                {"target_pages": ["evolution-loop.html", "analysis-hub.html"]},
            )
        )

    return hints[:4]


def run_analysis(
    signals: list[dict],
    prev_snapshot: dict[str, Any] | None,
    hint_rules: dict[str, Any],
    decisions_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    mod_c: Counter[str] = Counter()
    fac_c: Counter[str] = Counter()
    kind_c: Counter[str] = Counter()
    pair_c: Counter[tuple[str, str]] = Counter()

    for sig in signals:
        kind_c[sig.get("kind") or "unknown"] += 1
        mt = sig.get("maps_to") or {}
        for p in mt.get("pages") or []:
            mod_c[p] += 1
        facs = list(mt.get("lab_factors") or [])
        for f in facs:
            fac_c[f] += 1
        for i, a in enumerate(facs):
            for b in facs[i + 1 :]:
                pair = tuple(sorted((a, b)))
                pair_c[pair] += 1

    module_heat = [{"page": k, "count": v} for k, v in mod_c.most_common(24)]
    factor_heat = [{"factor": k, "count": v} for k, v in fac_c.most_common(24)]
    cooccurrence = [
        {"pair": list(p), "count": c} for p, c in pair_c.most_common(16) if c > 0
    ]
    kind_distribution = dict(kind_c)

    manifest_n = sum(1 for s in signals if s.get("_origin") == "manifest")
    candidate_n = sum(1 for s in signals if s.get("_origin") == "candidate")

    json_hints = evaluate_hint_rules(fac_c, len(signals), hint_rules)
    dd = decisions_doc if isinstance(decisions_doc, dict) else {}
    tracked = track_closure_rule_ids(hint_rules)
    closed = closed_rule_ids_from_decisions(dd)
    hint_closure_gaps = compute_hint_closure_gaps(
        json_hints, tracked, closed
    )

    hints: list[dict[str, Any]] = []
    hints.extend(
        compute_diff_hints(
            prev_snapshot, factor_heat, cooccurrence, manifest_n, candidate_n
        )
    )
    hints.extend(json_hints)

    top_tpl = hint_rules.get("top_factors_template") or ""
    top_f = [x["factor"] for x in factor_heat[:3]]
    if top_f and top_tpl:
        hints.append(
            _hint_obj(
                top_tpl.format(top_factors="、".join(top_f)),
                "top_factors",
                {"target_pages": ["lab.html"]},
            )
        )
    if not hints:
        hints.append(
            _hint_obj(
                hint_rules.get("fallback_hint")
                or "信号较少：优先跑 ingest 抓取或手工充实 manifest，再重新执行本分析脚本。",
                "fallback",
                {"target_pages": ["evolution-loop.html"]},
            )
        )

    return {
        "module_heat": module_heat,
        "factor_heat": factor_heat,
        "kind_distribution": kind_distribution,
        "cooccurrence": cooccurrence,
        "evolution_hints": hints[:8],
        "hint_closure_gaps": hint_closure_gaps,
    }


def append_sediment(snapshot_meta: dict) -> None:
    SEDIMENT.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    if SEDIMENT.is_file():
        data = json.loads(SEDIMENT.read_text(encoding="utf-8"))
    else:
        data = {"schema_version": 1, "entries": []}
    entries: list = data.setdefault("entries", [])
    if entries and isinstance(entries[-1], dict) and entries[-1].get("date") == today:
        entries[-1].update(snapshot_meta)
    else:
        entries.append({"date": today, **snapshot_meta})
    SEDIMENT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    try:
        from sqlite_store import DB_PATH, upsert_sediment

        upsert_sediment(
            date=today,
            manifest_n=int(snapshot_meta.get("manifest_n") or 0),
            candidate_n=int(snapshot_meta.get("candidate_n") or 0),
            top_factors=list(snapshot_meta.get("top_factors") or []),
            top_pages=list(snapshot_meta.get("top_pages") or []),
            hint_closure_gaps_n=int(
                snapshot_meta.get("hint_closure_gaps_n") or 0
            ),
            hint_decisions_total=int(
                snapshot_meta.get("hint_decisions_total") or 0
            ),
            run_id=str(snapshot_meta.get("run_id") or ""),
            repo_revision=str(snapshot_meta.get("repo_revision") or ""),
        )
        print(f"已更新 SQLite {DB_PATH}")
    except Exception as exc:  # noqa: BLE001
        print(f"警告: SQLite 写入失败（JSON 已保留）: {exc}", file=sys.stderr)


def _expected_snapshot_keys() -> frozenset[str]:
    return frozenset(
        {
            "schema_version",
            "generated_at",
            "run",
            "sources",
            "module_heat",
            "factor_heat",
            "kind_distribution",
            "cooccurrence",
            "evolution_hints",
            "hint_closure_gaps",
        }
    )


def validate_hint_closure_gaps(entries: list[Any]) -> None:
    if not isinstance(entries, list):
        print("错误: hint_closure_gaps 须为数组", file=sys.stderr)
        sys.exit(1)
    for i, g in enumerate(entries):
        if not isinstance(g, dict) or not isinstance(g.get("rule_id"), str):
            print(
                f"错误: hint_closure_gaps[{i}] 须为含 rule_id 字符串的对象",
                file=sys.stderr,
            )
            sys.exit(1)
        if "text" in g and not isinstance(g.get("text"), str):
            print(
                f"错误: hint_closure_gaps[{i}].text 须为字符串",
                file=sys.stderr,
            )
            sys.exit(1)


def validate_evolution_hints(entries: list[Any]) -> None:
    for i, h in enumerate(entries):
        if isinstance(h, str):
            continue
        if isinstance(h, dict) and isinstance(h.get("text"), str):
            continue
        print(
            f"错误: evolution_hints[{i}] 须为字符串或含 text 字段的对象",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--sediment",
        action="store_true",
        help="将当日摘要追加/更新到 data/sediment.json 并双写 data/evolution.db",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="仅校验：跑完整分析逻辑并检查输出结构，不写 analysis-snapshot.json / 沉淀（供 CI）",
    )
    args = ap.parse_args()

    manifest = load_json(MANIFEST)
    candidates = load_json(CANDIDATES)
    signals = collect_signals(manifest, candidates)
    prev_snapshot: dict[str, Any] | None = None
    if not args.check and OUT.is_file():
        prev_snapshot = load_json(OUT)
    hint_rules = load_hint_rules()
    decisions_doc = load_json(HINT_DECISIONS_PATH)
    analysis = run_analysis(signals, prev_snapshot, hint_rules, decisions_doc)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run = build_run_block()
    out = {
        "schema_version": 1,
        "generated_at": now,
        "run": run,
        "sources": {
            "manifest_signals": len(manifest.get("signals") or []),
            "candidate_signals": len(
                [
                    s
                    for s in candidates.get("signals") or []
                    if s.get("status") in (None, "candidate")
                    and effective_review_state(s) != "noise"
                ]
            ),
            "candidates_in_file": len(
                [
                    s
                    for s in candidates.get("signals") or []
                    if s.get("status") in (None, "candidate")
                ]
            ),
            "candidate_review_breakdown": candidate_review_breakdown(
                candidates
            ),
            "hint_decisions": hint_decisions_stats(
                load_json(HINT_DECISIONS_PATH)
            ),
            "combined_for_analysis": len(signals),
        },
        **analysis,
    }

    if args.check:
        missing = _expected_snapshot_keys() - frozenset(out.keys())
        if missing:
            print(f"错误: 分析输出缺字段: {sorted(missing)}", file=sys.stderr)
            sys.exit(1)
        validate_evolution_hints(out.get("evolution_hints") or [])
        validate_hint_closure_gaps(out.get("hint_closure_gaps") or [])
        src = out["sources"]
        if not isinstance(src, dict) or "combined_for_analysis" not in src:
            print("错误: sources 结构异常", file=sys.stderr)
            sys.exit(1)
        br = src.get("candidate_review_breakdown")
        if not isinstance(br, dict) or not all(
            k in br for k in ("pending", "noise", "queued_for_manifest")
        ):
            print("错误: sources.candidate_review_breakdown 结构异常", file=sys.stderr)
            sys.exit(1)
        hd = src.get("hint_decisions")
        if not isinstance(hd, dict) or "total" not in hd:
            print("错误: sources.hint_decisions 结构异常", file=sys.stderr)
            sys.exit(1)
        ba = hd.get("by_action")
        if not isinstance(ba, dict) or not all(
            k in ba for k in ("done", "rejected", "deferred")
        ):
            print("错误: sources.hint_decisions.by_action 结构异常", file=sys.stderr)
            sys.exit(1)
        run = out.get("run")
        if not isinstance(run, dict):
            print("错误: run 须为对象", file=sys.stderr)
            sys.exit(1)
        rid = run.get("run_id")
        rev = run.get("repo_revision")
        if not isinstance(rid, str) or not rid.strip():
            print("错误: run.run_id 须为非空字符串", file=sys.stderr)
            sys.exit(1)
        if not isinstance(rev, str) or not rev.strip():
            print("错误: run.repo_revision 须为非空字符串", file=sys.stderr)
            sys.exit(1)
        gaps_n = len(out.get("hint_closure_gaps") or [])
        print(
            f"OK --check · combined={src['combined_for_analysis']} "
            f"manifest={src['manifest_signals']} candidate={src['candidate_signals']} "
            f"closure_gaps={gaps_n}"
        )
        return

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已写入 {OUT}")

    if args.sediment:
        hd_tot = int(
            (out["sources"].get("hint_decisions") or {}).get("total") or 0
        )
        append_sediment(
            {
                "manifest_n": len(manifest.get("signals") or []),
                "candidate_n": len(candidates.get("signals") or []),
                "top_factors": [x["factor"] for x in analysis["factor_heat"][:5]],
                "top_pages": [x["page"] for x in analysis["module_heat"][:5]],
                "hint_closure_gaps_n": len(analysis.get("hint_closure_gaps") or []),
                "hint_decisions_total": hd_tot,
                "run_id": run["run_id"],
                "repo_revision": run["repo_revision"],
            }
        )
        print(f"已更新 {SEDIMENT}")


if __name__ == "__main__":
    main()
