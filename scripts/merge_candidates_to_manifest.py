#!/usr/bin/env python3
"""
将 evolution-candidates.json 中选定的候选信号合并进 evolution-manifest.json。

用法:
  python3 scripts/merge_candidates_to_manifest.py ing_xxxxxxxxxxxx
  python3 scripts/merge_candidates_to_manifest.py ing_aaa ing_bbb

合并后会从候选文件中删除已入库 id（若需保留副本请先备份）。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "evolution-manifest.json"
CANDIDATES = ROOT / "assets" / "evolution-candidates.json"


def strip_for_manifest(sig: dict) -> dict:
    out = {
        "id": sig["id"],
        "kind": sig.get("kind", "opinion"),
        "title": sig.get("title", ""),
        "summary": sig.get("summary", ""),
        "weight": sig.get("weight", "medium"),
        "since": sig.get("since") or str(date.today()),
        "maps_to": sig.get("maps_to") or {"pages": [], "lab_factors": []},
    }
    src = sig.get("source")
    if isinstance(src, dict):
        extra = []
        if src.get("item_link"):
            extra.append(f"链接: {src['item_link']}")
        if src.get("url") and src.get("type") == "law_html":
            extra.append(f"索引页: {src['url']}")
        if extra:
            out["summary"] = (out["summary"] + "\n\n" + " · ".join(extra))[:2500]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+", help="候选信号 id，如 ing_xxxxxxxxxxxx")
    args = ap.parse_args()
    want = set(args.ids)

    if not CANDIDATES.is_file():
        print(f"错误: 无 {CANDIDATES}", file=sys.stderr)
        sys.exit(1)
    if not MANIFEST.is_file():
        print(f"错误: 无 {MANIFEST}", file=sys.stderr)
        sys.exit(1)

    cand_data = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    man_data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    cand_signals = {s["id"]: s for s in cand_data.get("signals") or [] if "id" in s}
    existing = {s["id"] for s in man_data.get("signals") or []}

    merged = 0
    for sid in want:
        if sid not in cand_signals:
            print(f"警告: 候选中无 id {sid}", file=sys.stderr)
            continue
        sig = cand_signals[sid]
        if sig.get("status") != "candidate":
            print(f"警告: {sid} 非 candidate 状态，跳过", file=sys.stderr)
            continue
        row = strip_for_manifest(sig)
        if row["id"] in existing:
            print(f"警告: manifest 已有 {row['id']}，跳过", file=sys.stderr)
            continue
        man_data.setdefault("signals", []).append(row)
        existing.add(row["id"])
        merged += 1

    if merged == 0:
        print("未合并任何条目。", file=sys.stderr)
        sys.exit(1)

    man_data["updated"] = str(date.today())
    man_data["notes"] = (
        man_data.get("notes") or ""
    ) + f" 最近一次自候选合并 {merged} 条。"

    new_cand = [
        s for s in cand_data.get("signals") or [] if s.get("id") not in want
    ]
    cand_data["signals"] = new_cand
    cand_data["fetched_at"] = cand_data.get("fetched_at")
    cand_data["updated"] = str(date.today())

    MANIFEST.write_text(
        json.dumps(man_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    CANDIDATES.write_text(
        json.dumps(cand_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"已合并 {merged} 条 → {MANIFEST}；候选已删对应 id。")


if __name__ == "__main__":
    main()
