#!/usr/bin/env python3
"""
对比两份 analysis-snapshot.json，输出 Markdown 摘要（便于贴 PR）。
用法:
  python3 scripts/diff_analysis_snapshot.py assets/analysis-snapshot.json /path/to/old.json
  python3 scripts/diff_analysis_snapshot.py --git HEAD~1:assets/analysis-snapshot.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from evolution_pkg.io import REPO_ROOT, load_json


def _load_path(p: Path) -> dict[str, Any]:
    return load_json(p)


def _load_git_spec(spec: str) -> dict[str, Any]:
    """例如 HEAD~1:assets/analysis-snapshot.json"""
    r = subprocess.run(
        ["git", "show", spec],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        raise SystemExit(f"git show 失败: {spec}\n{r.stderr}")
    return json.loads(r.stdout)


def _heat_top(rows: list[Any], kind: str, n: int = 8) -> list[tuple[str, float]]:
    out: list[tuple[str, float]] = []
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        if kind == "module":
            name = row.get("page")
        else:
            name = row.get("factor")
        if name is None:
            continue
        raw = row.get("count", row.get("score", 0))
        try:
            score = float(raw)
        except (TypeError, ValueError):
            score = 0.0
        out.append((str(name), score))
    out.sort(key=lambda x: -x[1])
    return out[:n]


def _diff_top(
    base_top: list[tuple[str, float]], head_top: list[tuple[str, float]], label: str
) -> list[str]:
    m0 = dict(base_top)
    m1 = dict(head_top)
    keys = sorted(set(m0) | set(m1), key=lambda k: -max(m0.get(k, 0), m1.get(k, 0)))
    lines: list[str] = []
    changed = False
    for k in keys[:12]:
        v0, v1 = m0.get(k), m1.get(k)
        if v0 != v1:
            changed = True
            a = "—" if v0 is None else v0
            b = "—" if v1 is None else v1
            lines.append(f"- **{k}**：{a} → {b}")
    if not changed:
        lines.append(f"- （{label} Top 无变化或仅序位微调）")
    return lines


def build_report(base: dict[str, Any], head: dict[str, Any]) -> str:
    br = base.get("run") or {}
    hr = head.get("run") or {}
    sb = base.get("sources") or {}
    sh = head.get("sources") or {}

    lines: list[str] = [
        "## analysis-snapshot 差分摘要",
        "",
        f"- **base** `run_id`: `{br.get('run_id', '—')}` · `repo_revision`: `{br.get('repo_revision', '—')}`",
        f"- **head** `run_id`: `{hr.get('run_id', '—')}` · `repo_revision`: `{hr.get('repo_revision', '—')}`",
        "",
        "### sources",
        f"- `combined_for_analysis`: {sb.get('combined_for_analysis')} → {sh.get('combined_for_analysis')}",
        f"- `manifest_signals`: {sb.get('manifest_signals')} → {sh.get('manifest_signals')}",
        f"- `candidate_signals`: {sb.get('candidate_signals')} → {sh.get('candidate_signals')}",
        "",
        "### 列表长度",
        f"- `evolution_hints`: {len(base.get('evolution_hints') or [])} → {len(head.get('evolution_hints') or [])}",
        f"- `hint_closure_gaps`: {len(base.get('hint_closure_gaps') or [])} → {len(head.get('hint_closure_gaps') or [])}",
        f"- `cooccurrence`: {len(base.get('cooccurrence') or [])} → {len(head.get('cooccurrence') or [])}",
        "",
        "### module_heat（score 变化摘取）",
        *_diff_top(
            _heat_top(base.get("module_heat") or [], "module"),
            _heat_top(head.get("module_heat") or [], "module"),
            "module_heat",
        ),
        "",
        "### factor_heat（count 变化摘取）",
        *_diff_top(
            _heat_top(base.get("factor_heat") or [], "factor"),
            _heat_top(head.get("factor_heat") or [], "factor"),
            "factor_heat",
        ),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="对比两份 analysis-snapshot.json")
    ap.add_argument("base", nargs="?", help="基准文件路径，或配合 --git-base")
    ap.add_argument("head", nargs="?", help="新文件路径（默认可省略则为当前 assets/analysis-snapshot.json）")
    ap.add_argument("--git-base", metavar="SPEC", help="用 git 取基准，如 HEAD~1:assets/analysis-snapshot.json")
    ap.add_argument("--json", action="store_true", help="输出精简 JSON 而非 Markdown")
    args = ap.parse_args()

    head_path = REPO_ROOT / "assets" / "analysis-snapshot.json"
    if args.head:
        head_path = Path(args.head).expanduser()
        if not head_path.is_absolute():
            head_path = (REPO_ROOT / head_path).resolve()

    if args.git_base:
        base_doc = _load_git_spec(args.git_base)
    elif args.base:
        bp = Path(args.base).expanduser()
        if not bp.is_absolute():
            bp = (REPO_ROOT / bp).resolve()
        base_doc = _load_path(bp)
    else:
        ap.print_help()
        return 2

    head_doc = _load_path(head_path)

    if args.json:
        sb = base_doc.get("sources") or {}
        sh = head_doc.get("sources") or {}
        out = {
            "base_run": base_doc.get("run"),
            "head_run": head_doc.get("run"),
            "combined_delta": (sh.get("combined_for_analysis") or 0)
            - (sb.get("combined_for_analysis") or 0),
            "hints_delta": len(head_doc.get("evolution_hints") or [])
            - len(base_doc.get("evolution_hints") or []),
            "gaps_delta": len(head_doc.get("hint_closure_gaps") or [])
            - len(base_doc.get("hint_closure_gaps") or []),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(build_report(base_doc, head_doc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
