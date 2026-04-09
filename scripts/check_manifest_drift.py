#!/usr/bin/env python3
"""
对账：evolution-manifest.json（及可选 candidates）中 maps_to.pages 须在仓库根存在对应 HTML；
maps_to.lab_factors 须在 assets/lab.js 的因子 id 集合内。
不写文件；供 CI / pre-commit / make validate。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "evolution-manifest.json"
CANDIDATES = ROOT / "assets" / "evolution-candidates.json"
LAB = ROOT / "assets" / "lab.js"


def lab_factor_ids() -> set[str]:
    text = LAB.read_text(encoding="utf-8")
    return set(re.findall(r'^\s+id:\s*"([a-z0-9_]+)"', text, re.MULTILINE))


def check_signals(
    signals: list[dict], label: str, lab_ids: set[str]
) -> list[str]:
    errs: list[str] = []
    for s in signals:
        sid = s.get("id") or "?"
        mt = s.get("maps_to") or {}
        if not isinstance(mt, dict):
            errs.append(f"{label} {sid}: maps_to 须为对象")
            continue
        for p in mt.get("pages") or []:
            if not isinstance(p, str) or not p.strip():
                continue
            rel = p.strip()
            fp = ROOT / rel
            if not fp.is_file():
                errs.append(f"{label} {sid}: 页面文件不存在 · {rel}")
        for fac in mt.get("lab_factors") or []:
            if not isinstance(fac, str) or not fac.strip():
                continue
            f = fac.strip()
            if f not in lab_ids:
                errs.append(
                    f"{label} {sid}: 未知沙盘因子 · {f}（请同步 assets/lab.js）"
                )
    return errs


def main() -> None:
    if not LAB.is_file():
        print(f"错误: 未找到 {LAB}", file=sys.stderr)
        sys.exit(1)
    lab_ids = lab_factor_ids()
    if not lab_ids:
        print("错误: 未能从 lab.js 解析因子 id", file=sys.stderr)
        sys.exit(1)

    all_errs: list[str] = []
    if MANIFEST.is_file():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        all_errs.extend(
            check_signals(data.get("signals") or [], "manifest", lab_ids)
        )
    else:
        print(f"警告: 未找到 {MANIFEST}", file=sys.stderr)

    if CANDIDATES.is_file():
        cdata = json.loads(CANDIDATES.read_text(encoding="utf-8"))
        all_errs.extend(
            check_signals(cdata.get("signals") or [], "candidate", lab_ids)
        )

    if all_errs:
        print("manifest / 候选 对账失败：", file=sys.stderr)
        for e in all_errs:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    n_lab = len(lab_ids)
    print(f"OK: 对账通过 · lab.js 因子 {n_lab} 个 · 已检查 manifest" +
          (" + candidates" if CANDIDATES.is_file() else ""))


if __name__ == "__main__":
    main()
