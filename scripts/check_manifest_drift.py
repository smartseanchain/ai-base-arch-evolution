#!/usr/bin/env python3
"""
对账：evolution-manifest.json（及候选）中 maps_to.pages 须在 evolution-registry.json 内且文件存在；
maps_to.lab_factors 须与 registry（并与 lab.js 解析结果）一致。
另校验 ingest_config.json、maps_to_hints.json 中的 pages / lab_factors；
gen-sitemap.py 的 PRIORITY 键须 ⊆ registry.pages；
partials/site-nav.inc.html 中 href="*.html" 须 ⊆ registry.pages；
evolution-hint-rules.json 中 rules[].target_pages 须 ⊆ registry.pages；
rules[].id 须非空且唯一；track_closure 若存在须为布尔。
不写文件；供 CI / pre-commit / make validate。
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from evolution_pkg.io import (
    INGEST_CONFIG_JSON_PATH,
    MAPS_TO_HINTS_JSON_PATH,
    REPO_ROOT,
    load_registry_allowed_sets,
)

MANIFEST = REPO_ROOT / "assets" / "evolution-manifest.json"
CANDIDATES = REPO_ROOT / "assets" / "evolution-candidates.json"
LAB = REPO_ROOT / "assets" / "lab.js"
INGEST_CONFIG = INGEST_CONFIG_JSON_PATH
MAPS_HINTS = MAPS_TO_HINTS_JSON_PATH
GEN_SITEMAP = REPO_ROOT / "scripts" / "gen-sitemap.py"
HINT_RULES = REPO_ROOT / "scripts" / "evolution-hint-rules.json"


def hint_rules_structural_errors(doc: dict) -> list[str]:
    """校验 rules 形状：id 必填、唯一；track_closure 仅允许布尔。"""
    errs: list[str] = []
    rules = doc.get("rules")
    if rules is None:
        return ["evolution-hint-rules.json: 缺少 rules"]
    if not isinstance(rules, list):
        return ["evolution-hint-rules.json: rules 须为数组"]
    seen: set[str] = set()
    for i, r in enumerate(rules):
        prefix = f"evolution-hint-rules.json: rules[{i}]"
        if not isinstance(r, dict):
            errs.append(f"{prefix} 须为对象")
            continue
        rid = r.get("id")
        if rid is None:
            errs.append(f"{prefix} 缺少 id")
            continue
        if not isinstance(rid, str) or not rid.strip():
            errs.append(f"{prefix}.id 须为非空字符串")
            continue
        rs = rid.strip()
        if rs in seen:
            errs.append(f"evolution-hint-rules.json: 重复的 rules[].id · {rs!r}")
        seen.add(rs)
        tc = r.get("track_closure")
        if tc is not None and not isinstance(tc, bool):
            errs.append(
                f"{prefix}.track_closure 须为布尔或省略，当前: {type(tc).__name__}"
            )
    return errs


def hint_rules_target_pages(doc: dict) -> set[str]:
    out: set[str] = set()
    for r in doc.get("rules") or []:
        tp = r.get("target_pages")
        if not isinstance(tp, list):
            continue
        for p in tp:
            if isinstance(p, str) and p.strip():
                out.add(p.strip())
    return out


def lab_factor_ids_from_js() -> set[str]:
    text = LAB.read_text(encoding="utf-8")
    return set(re.findall(r'^\s+id:\s*"([a-z0-9_]+)"', text, re.MULTILINE))


def gen_sitemap_priority_keys() -> set[str]:
    spec = importlib.util.spec_from_file_location("_gen_sitemap_mod", GEN_SITEMAP)
    if spec is None or spec.loader is None:
        print("错误: 无法加载 gen-sitemap.py", file=sys.stderr)
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(mod.PRIORITY.keys())


def collect_ingest_maps_refs(cfg: dict) -> tuple[set[str], set[str]]:
    pages: set[str] = set()
    facs: set[str] = set()
    for r in cfg.get("routes") or []:
        for p in r.get("pages") or []:
            if isinstance(p, str) and p.strip():
                pages.add(p.strip())
        for f in r.get("lab_factors") or []:
            if isinstance(f, str) and f.strip():
                facs.add(f.strip())
    return pages, facs


def collect_hints_refs(h: dict) -> tuple[set[str], set[str]]:
    pages: set[str] = set()
    facs: set[str] = set()
    for m in (h.get("host_suffixes") or {}).values():
        for p in m.get("pages") or []:
            if isinstance(p, str) and p.strip():
                pages.add(p.strip())
        for f in m.get("lab_factors") or []:
            if isinstance(f, str) and f.strip():
                facs.add(f.strip())
    for row in h.get("keyword_routes") or []:
        for p in row.get("pages") or []:
            if isinstance(p, str) and p.strip():
                pages.add(p.strip())
        for f in row.get("lab_factors") or []:
            if isinstance(f, str) and f.strip():
                facs.add(f.strip())
    return pages, facs


def check_signals(
    signals: list[dict],
    label: str,
    allowed_pages: frozenset[str],
    lab_ids: frozenset[str],
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
            if rel not in allowed_pages:
                errs.append(
                    f"{label} {sid}: 页面不在 evolution-registry.json · {rel}"
                )
                continue
            fp = REPO_ROOT / rel
            if not fp.is_file():
                errs.append(f"{label} {sid}: 页面文件不存在 · {rel}")
        for fac in mt.get("lab_factors") or []:
            if not isinstance(fac, str) or not fac.strip():
                continue
            f = fac.strip()
            if f not in lab_ids:
                errs.append(
                    f"{label} {sid}: 未知沙盘因子 · {f}（请同步 registry 与 assets/lab.js）"
                )
    return errs


def main() -> None:
    try:
        allowed_pages, reg_fac = load_registry_allowed_sets()
    except (FileNotFoundError, ValueError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    for rel in sorted(allowed_pages):
        fp = REPO_ROOT / rel
        if not fp.is_file():
            print(
                f"错误: registry 列出但仓库无此文件 · {rel}",
                file=sys.stderr,
            )
            sys.exit(1)

    if not LAB.is_file():
        print(f"错误: 未找到 {LAB}", file=sys.stderr)
        sys.exit(1)
    lab_js = lab_factor_ids_from_js()
    if not lab_js:
        print("错误: 未能从 lab.js 解析因子 id", file=sys.stderr)
        sys.exit(1)
    if lab_js != reg_fac:
        only_js = sorted(lab_js - reg_fac)
        only_reg = sorted(reg_fac - lab_js)
        print(
            "错误: lab.js 与 evolution-registry.json 的 lab_factors 不一致",
            file=sys.stderr,
        )
        if only_js:
            print(f"  仅在 lab.js: {only_js}", file=sys.stderr)
        if only_reg:
            print(f"  仅在 registry: {only_reg}", file=sys.stderr)
        sys.exit(1)

    prio = gen_sitemap_priority_keys()
    bad_prio = sorted(prio - allowed_pages)
    if bad_prio:
        print(
            "错误: gen-sitemap.py PRIORITY 含未在 registry 声明的页面 · "
            + ", ".join(bad_prio),
            file=sys.stderr,
        )
        sys.exit(1)

    all_errs: list[str] = []

    SITE_NAV_PARTIAL = REPO_ROOT / "partials" / "site-nav.inc.html"
    if SITE_NAV_PARTIAL.is_file():
        nav_hrefs = set(
            re.findall(
                r'href="([a-zA-Z0-9._-]+\.html)"',
                SITE_NAV_PARTIAL.read_text(encoding="utf-8"),
            )
        )
        for h in sorted(nav_hrefs - allowed_pages):
            all_errs.append(
                f"partials/site-nav.inc.html: 未知页面（须 ∈ registry）· {h}"
            )

    if HINT_RULES.is_file():
        try:
            hr = json.loads(HINT_RULES.read_text(encoding="utf-8"))
            all_errs.extend(hint_rules_structural_errors(hr))
            for p in sorted(hint_rules_target_pages(hr) - allowed_pages):
                all_errs.append(
                    f"evolution-hint-rules.json: target_pages 未知（须 ∈ registry）· {p}"
                )
        except json.JSONDecodeError as e:
            all_errs.append(f"evolution-hint-rules.json: JSON 无效 · {e}")

    if INGEST_CONFIG.is_file():
        ic = json.loads(INGEST_CONFIG.read_text(encoding="utf-8"))
        ip, ifac = collect_ingest_maps_refs(ic)
        for p in sorted(ip - allowed_pages):
            all_errs.append(f"ingest_config routes: 未知页面 · {p}")
        for f in sorted(ifac - reg_fac):
            all_errs.append(f"ingest_config routes: 未知因子 · {f}")

    if MAPS_HINTS.is_file():
        hi = json.loads(MAPS_HINTS.read_text(encoding="utf-8"))
        hp, hf = collect_hints_refs(hi)
        for p in sorted(hp - allowed_pages):
            all_errs.append(f"maps_to_hints: 未知页面 · {p}")
        for f in sorted(hf - reg_fac):
            all_errs.append(f"maps_to_hints: 未知因子 · {f}")

    if MANIFEST.is_file():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        all_errs.extend(
            check_signals(data.get("signals") or [], "manifest", allowed_pages, reg_fac)
        )
    else:
        print(f"警告: 未找到 {MANIFEST}", file=sys.stderr)

    if CANDIDATES.is_file():
        cdata = json.loads(CANDIDATES.read_text(encoding="utf-8"))
        all_errs.extend(
            check_signals(
                cdata.get("signals") or [], "candidate", allowed_pages, reg_fac
            )
        )

    if all_errs:
        print("manifest / 候选 / 配置 对账失败：", file=sys.stderr)
        for e in all_errs:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    n_lab = len(reg_fac)
    print(
        f"OK: 对账通过 · registry 页面 {len(allowed_pages)} · lab_factors {n_lab} · "
        "已检查 manifest"
        + (" + candidates" if CANDIDATES.is_file() else "")
        + " + ingest 配置 + site-nav partial + hint-rules（结构+target_pages）"
    )


if __name__ == "__main__":
    main()
