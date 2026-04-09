#!/usr/bin/env python3
"""
校验 assets/evolution-hint-decisions.json：结构化记录对 evolution_hints 的落实 / 否决 / 延期。
可选 rule_id 与快照中 evolution_hints[].rule_id 对齐。
related_pages 若存在须 ⊆ evolution-registry.json 的 pages。
不写文件；供 make validate / CI / pre-commit。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISIONS_PATH = ROOT / "assets" / "evolution-hint-decisions.json"
REGISTRY_PATH = ROOT / "scripts" / "evolution-registry.json"

ALLOWED_ACTIONS = frozenset({"done", "rejected", "deferred"})
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MAX_NOTE = 4000
MAX_SUMMARY = 500
MAX_RULE_ID = 120


def load_registry_pages() -> set[str]:
    if not REGISTRY_PATH.is_file():
        print(f"错误: 缺少注册表 {REGISTRY_PATH}", file=sys.stderr)
        sys.exit(1)
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    pages = reg.get("pages")
    if not isinstance(pages, list):
        print("错误: evolution-registry.json 缺少 pages 数组", file=sys.stderr)
        sys.exit(1)
    return {p.strip() for p in pages if isinstance(p, str) and p.strip()}


def validate_decisions(doc: object, allowed_pages: set[str]) -> list[str]:
    errs: list[str] = []
    if not isinstance(doc, dict):
        return ["根须为 JSON 对象"]
    extra_root = set(doc.keys()) - {"decisions"}
    if extra_root:
        errs.append(
            f"根对象仅允许 decisions 字段，多余: {sorted(extra_root)!r}"
        )
    decs = doc.get("decisions")
    if decs is None:
        return ["缺少 decisions 字段"]
    if not isinstance(decs, list):
        return ["decisions 须为数组"]

    seen_ids: set[str] = set()
    for i, row in enumerate(decs):
        prefix = f"decisions[{i}]"
        if not isinstance(row, dict):
            errs.append(f"{prefix} 须为对象")
            continue
        rid = row.get("id")
        if not isinstance(rid, str) or not rid.strip():
            errs.append(f"{prefix}.id 须为非空字符串")
        else:
            rs = rid.strip()
            if rs in seen_ids:
                errs.append(f"重复的 id: {rs!r}")
            seen_ids.add(rs)
        action = row.get("action")
        if action not in ALLOWED_ACTIONS:
            errs.append(
                f"{prefix}.action 须为 done | rejected | deferred，当前: {action!r}"
            )
        ra = row.get("recorded_at")
        if not isinstance(ra, str) or not DATE_RE.match(ra.strip()):
            errs.append(
                f"{prefix}.recorded_at 须为 YYYY-MM-DD，当前: {ra!r}"
            )
        hs = row.get("hint_summary")
        if hs is not None and (not isinstance(hs, str) or len(hs) > MAX_SUMMARY):
            errs.append(
                f"{prefix}.hint_summary 须为字符串且长度 ≤ {MAX_SUMMARY}"
            )
        note = row.get("note")
        if note is not None and (not isinstance(note, str) or len(note) > MAX_NOTE):
            errs.append(f"{prefix}.note 须为字符串且长度 ≤ {MAX_NOTE}")
        pr = row.get("pr_url")
        if pr is not None:
            if not isinstance(pr, str) or not (
                pr.startswith("http://") or pr.startswith("https://")
            ):
                errs.append(f"{prefix}.pr_url 须为 http(s) URL 或省略")
        rule_id = row.get("rule_id")
        if rule_id is not None:
            if not isinstance(rule_id, str) or not rule_id.strip():
                errs.append(f"{prefix}.rule_id 须为非空字符串或省略")
            elif len(rule_id) > MAX_RULE_ID:
                errs.append(
                    f"{prefix}.rule_id 长度须 ≤ {MAX_RULE_ID}"
                )
        rps = row.get("related_pages")
        if rps is not None:
            if not isinstance(rps, list):
                errs.append(f"{prefix}.related_pages 须为字符串数组或省略")
            else:
                for j, p in enumerate(rps):
                    if not isinstance(p, str) or not p.strip():
                        errs.append(f"{prefix}.related_pages[{j}] 须为非空字符串")
                    elif p.strip() not in allowed_pages:
                        errs.append(
                            f"{prefix}.related_pages[{j}] {p.strip()!r} 不在 registry.pages"
                        )
        for k in row.keys():
            if k not in {
                "id",
                "action",
                "recorded_at",
                "hint_summary",
                "note",
                "pr_url",
                "related_pages",
                "rule_id",
            }:
                errs.append(f"{prefix} 未知字段: {k!r}")
    return errs


def main() -> None:
    if not DECISIONS_PATH.is_file():
        print(f"错误: 缺少 {DECISIONS_PATH}", file=sys.stderr)
        sys.exit(1)
    try:
        doc = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败 — {e}", file=sys.stderr)
        sys.exit(1)
    allowed = load_registry_pages()
    errs = validate_decisions(doc, allowed)
    if errs:
        for e in errs:
            print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    n = len(doc.get("decisions") or [])
    print(f"OK: evolution-hint-decisions · {n} 条记录 · {DECISIONS_PATH}")


if __name__ == "__main__":
    main()
