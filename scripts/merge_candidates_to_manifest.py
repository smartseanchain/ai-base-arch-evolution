#!/usr/bin/env python3
"""
将 evolution-candidates.json 中选定的候选信号合并进 evolution-manifest.json。

**推荐**：``PYTHONPATH=scripts python3 -m evolution_pkg.candidate_merge``（同参数）。

用法:
  python3 scripts/merge_candidates_to_manifest.py ing_xxxxxxxxxxxx
  python3 scripts/merge_candidates_to_manifest.py ing_aaa ing_bbb

合并后会从候选文件中删除已入库 id（若需保留副本请先备份）。

默认仅允许 review_state=queued_for_manifest 的条目（双周审阅后标记）。
应急可加 --force。噪点请先将 review_state 设为 noise（不参与分析热力）。

合并动线与人审: docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · AGENTS.md#agents-invariants
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from evolution_pkg.candidate_merge import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
