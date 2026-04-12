#!/usr/bin/env python3
"""
写入 assets/ai-analysis-overlay.json 占位文件（provider.kind=stub），便于联调 Schema 与前台。
不调用外部 LLM。须已有 assets/analysis-snapshot.json。

用法: python3 scripts/write_ai_analysis_overlay_stub.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

SNAPSHOT = REPO_ROOT / "assets" / "analysis-snapshot.json"
OUT = REPO_ROOT / "assets" / "ai-analysis-overlay.json"


def main() -> int:
    if not SNAPSHOT.is_file():
        print(f"错误: 缺少 {SNAPSHOT}（请先 make analyze 或生成快照）", file=sys.stderr)
        return 1
    try:
        snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: 快照 JSON 无效 — {e}", file=sys.stderr)
        return 1
    run = snap.get("run") if isinstance(snap, dict) else None
    if not isinstance(run, dict):
        print("错误: 快照缺少 run 对象", file=sys.stderr)
        return 1
    rid = run.get("run_id")
    rev = run.get("repo_revision")
    if not rid:
        print("错误: 快照 run.run_id 为空", file=sys.stderr)
        return 1
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    doc = {
        "schema_version": 1,
        "generated_at": now,
        "source_run_id": str(rid),
        "source_repo_revision": str(rev) if rev is not None else "",
        "provider": {"kind": "stub", "model": "none"},
        "disclaimer_zh": "本块为占位 stub，非模型生成；接入真实 AI 服务见 docs/AI_ASSISTED_ANALYSIS_LAYER.md。",
        "summary_md": "（stub）尚未调用外部模型；可替换为对当日快照的解读摘要。",
        "sections": [
            {
                "id": "stub",
                "title_zh": "占位节",
                "body_md": "运行 `write_ai_analysis_overlay_stub.py` 生成；合并前可删除本文件或改为真实解读产物。",
            }
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: 已写入 {OUT.relative_to(REPO_ROOT)} · source_run_id={rid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
