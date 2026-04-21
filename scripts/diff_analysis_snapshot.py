#!/usr/bin/env python3
"""
对比两份 analysis-snapshot.json，输出 Markdown 摘要（便于贴 PR）。
用法:
  python3 scripts/diff_analysis_snapshot.py assets/analysis-snapshot.json /path/to/old.json
  python3 scripts/diff_analysis_snapshot.py --git HEAD~1:assets/analysis-snapshot.json

对比逻辑见 ``evolution_pkg.analysis_diff``；本文件仅保留 CLI（含 git 取基线）。
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from evolution_pkg.analysis_diff import build_report, snapshot_diff_json_text
from evolution_pkg.io import REPO_ROOT, load_json


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
        base_doc = load_json(bp)
    else:
        ap.print_help()
        return 2

    head_doc = load_json(head_path)

    if args.json:
        print(snapshot_diff_json_text(base_doc, head_doc))
    else:
        print(build_report(base_doc, head_doc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
