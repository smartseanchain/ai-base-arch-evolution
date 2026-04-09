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


def run_analysis(signals: list[dict]) -> dict[str, Any]:
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

    hints: list[str] = []
    top_f = [x["factor"] for x in factor_heat[:3]]
    if fac_c.get("reg", 0) >= 2 and fac_c.get("ai", 0) >= 1:
        hints.append(
            "多条信号同时指向「监管(reg)」与「AI」——建议在综合推演 §6 检查是否已有监管×AI 配方，若无则按 §11 扩展插槽补一条传导链。"
        )
    if fac_c.get("water_cooling", 0) >= 1 and fac_c.get("esg_compute_carbon", 0) >= 1:
        hints.append(
            "算力—水—碳因子共现：与十年场景·算力能源、职基能同读，关注地方邻避叙事。"
        )
    if len(signals) >= 5:
        hints.append(
            f"当前共 {len(signals)} 条信号（含候选），建议每季度做一次 §7 复合表对行，删除已失效叙事。"
        )
    if top_f:
        hints.append(
            "当前热力靠前的沙盘因子：" + "、".join(top_f) + "——打开沙盘工坊勾选对应项做一轮压测。"
        )
    if not hints:
        hints.append(
            "信号较少：优先跑 ingest 抓取或手工充实 manifest，再重新执行本分析脚本。"
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
    analysis = run_analysis(signals)

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
