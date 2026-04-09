#!/usr/bin/env python3
"""
分析引擎：读取 manifest / candidates，生成模块与因子热力、共现与进化提示；
可选将日摘要写入 data/sediment.json，并双写到 data/evolution.db（SQLite）。

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

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "evolution-manifest.json"
CANDIDATES = ROOT / "assets" / "evolution-candidates.json"
OUT = ROOT / "assets" / "analysis-snapshot.json"
SEDIMENT = ROOT / "data" / "sediment.json"
HINT_RULES_PATH = ROOT / "scripts" / "evolution-hint-rules.json"


def load_json(p: Path) -> dict[str, Any]:
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def collect_signals(manifest: dict, candidates: dict) -> list[dict]:
    out: list[dict] = []
    for s in manifest.get("signals") or []:
        x = dict(s)
        x["_origin"] = "manifest"
        out.append(x)
    for s in candidates.get("signals") or []:
        if s.get("status") == "candidate" or s.get("status") is None:
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


def evaluate_hint_rules(
    fac_c: Counter,
    signals_count: int,
    rules_doc: dict[str, Any],
) -> list[str]:
    out: list[str] = []
    for rule in rules_doc.get("rules") or []:
        fm = rule.get("factors_min") or {}
        if any(fac_c.get(k, 0) < int(v) for k, v in fm.items()):
            continue
        smin = rule.get("signals_count_min")
        if smin is not None and signals_count < int(smin):
            continue
        tpl = rule.get("hint_template")
        plain = rule.get("hint")
        if tpl:
            out.append(tpl.format(signals_count=signals_count))
        elif plain:
            out.append(str(plain))
    return out


def compute_diff_hints(
    prev: dict[str, Any] | None,
    factor_heat: list[dict],
    cooccurrence: list[dict],
    manifest_n: int,
    candidate_n: int,
) -> list[str]:
    if not prev:
        return []
    hints: list[str] = []
    prev_fac = [x["factor"] for x in (prev.get("factor_heat") or [])[:8]]
    curr_fac = [x["factor"] for x in factor_heat[:8]]
    prev_top_set = set(prev_fac[:8])
    new_in_top = [f for f in curr_fac[:5] if f not in prev_top_set]
    if new_in_top:
        hints.append(
            "相较上期快照，热力因子新进入前列："
            + "、".join(new_in_top)
            + "——建议核对 manifest/候选映射是否反映新焦点。"
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
                f"共现新出现：{' × '.join(p)}（count={c}）——可查复合表是否需补传导说明。"
            )
            co_added += 1
        elif c > old:
            hints.append(
                f"共现增强：{' × '.join(p)}（{old}→{c}）——关注对应页面交叉叙事。"
            )
            co_added += 1
        if co_added >= 2:
            break

    prev_src = prev.get("sources") or {}
    pm = prev_src.get("manifest_signals")
    pc = prev_src.get("candidate_signals")
    if isinstance(pm, int) and manifest_n > pm:
        hints.append(
            f"已入库信号较上期增加 {manifest_n - pm} 条（{pm}→{manifest_n}），"
            "建议跑一轮沙盘与 §7 对行。"
        )
    if isinstance(pc, int) and candidate_n > pc:
        hints.append(
            f"候选较上期增加 {candidate_n - pc} 条——可安排双周审阅或减噪。"
        )

    return hints[:4]


def run_analysis(
    signals: list[dict],
    prev_snapshot: dict[str, Any] | None,
    hint_rules: dict[str, Any],
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

    hints: list[str] = []
    hints.extend(
        compute_diff_hints(
            prev_snapshot, factor_heat, cooccurrence, manifest_n, candidate_n
        )
    )
    hints.extend(evaluate_hint_rules(fac_c, len(signals), hint_rules))

    top_tpl = hint_rules.get("top_factors_template") or ""
    top_f = [x["factor"] for x in factor_heat[:3]]
    if top_f and top_tpl:
        hints.append(top_tpl.format(top_factors="、".join(top_f)))
    if not hints:
        hints.append(
            hint_rules.get("fallback_hint")
            or "信号较少：优先跑 ingest 抓取或手工充实 manifest，再重新执行本分析脚本。"
        )

    return {
        "module_heat": module_heat,
        "factor_heat": factor_heat,
        "kind_distribution": kind_distribution,
        "cooccurrence": cooccurrence,
        "evolution_hints": hints[:8],
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
        )
        print(f"已更新 SQLite {DB_PATH}")
    except Exception as exc:  # noqa: BLE001
        print(f"警告: SQLite 写入失败（JSON 已保留）: {exc}", file=sys.stderr)


def _expected_snapshot_keys() -> frozenset[str]:
    return frozenset(
        {
            "schema_version",
            "generated_at",
            "sources",
            "module_heat",
            "factor_heat",
            "kind_distribution",
            "cooccurrence",
            "evolution_hints",
        }
    )


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
    analysis = run_analysis(signals, prev_snapshot, hint_rules)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {
        "schema_version": 1,
        "generated_at": now,
        "sources": {
            "manifest_signals": len(manifest.get("signals") or []),
            "candidate_signals": len(
                [
                    s
                    for s in candidates.get("signals") or []
                    if s.get("status") in (None, "candidate")
                ]
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
        src = out["sources"]
        if not isinstance(src, dict) or "combined_for_analysis" not in src:
            print("错误: sources 结构异常", file=sys.stderr)
            sys.exit(1)
        print(
            f"OK --check · combined={src['combined_for_analysis']} "
            f"manifest={src['manifest_signals']} candidate={src['candidate_signals']}"
        )
        return

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已写入 {OUT}")

    if args.sediment:
        append_sediment(
            {
                "manifest_n": len(manifest.get("signals") or []),
                "candidate_n": len(candidates.get("signals") or []),
                "top_factors": [x["factor"] for x in analysis["factor_heat"][:5]],
                "top_pages": [x["page"] for x in analysis["module_heat"][:5]],
            }
        )
        print(f"已更新 {SEDIMENT}")


if __name__ == "__main__":
    main()
