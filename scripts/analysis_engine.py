#!/usr/bin/env python3
"""
分析引擎：读取 manifest / candidates，生成模块与因子热力、共现与进化提示；
可选将日摘要写入 data/sediment.json，并双写到 data/evolution.db（SQLite）；
支持 ``--check`` 或 ``--dry-run``（不写快照/沉淀，仅校验）；
写入快照时默认向 evolution.db 的 analysis_snapshot_history 表追加**只读历史**
（与已提交的 analysis-snapshot.json 闸门分离，可用 --no-sqlite-snapshot-history 关闭）。
对 track_closure 规则比对 evolution-hint-decisions，输出 hint_closure_gaps。

输出: assets/analysis-snapshot.json

**实现**在 **``evolution_pkg.analysis_pipeline``**；推荐 **``PYTHONPATH=scripts python3 -m evolution_pkg.analysis_pipeline``**（参数相同）。
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from evolution_pkg.analysis_core import run_analysis  # noqa: E402
from evolution_pkg.analysis_hints import load_hint_rules_from_path  # noqa: E402
from evolution_pkg.analysis_pipeline import default_analysis_paths, main  # noqa: E402

__all__ = [
    "CANDIDATES",
    "HINT_DECISIONS_PATH",
    "HINT_RULES_PATH",
    "MANIFEST",
    "OUT",
    "SEDIMENT",
    "load_hint_rules",
    "main",
    "run_analysis",
]

_DEFAULT_PATHS = default_analysis_paths()
MANIFEST = _DEFAULT_PATHS.manifest
CANDIDATES = _DEFAULT_PATHS.candidates
OUT = _DEFAULT_PATHS.out_snapshot
SEDIMENT = _DEFAULT_PATHS.sediment
HINT_RULES_PATH = _DEFAULT_PATHS.hint_rules
HINT_DECISIONS_PATH = _DEFAULT_PATHS.hint_decisions


def load_hint_rules() -> dict[str, Any]:
    """仓库内 ``evolution-hint-rules.json``；单测与脚本仍从本入口调用。"""
    return load_hint_rules_from_path(_DEFAULT_PATHS.hint_rules)


if __name__ == "__main__":
    raise SystemExit(main())
