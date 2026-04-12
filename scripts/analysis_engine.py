#!/usr/bin/env python3
"""
分析引擎：读取 manifest / candidates，生成模块与因子热力、共现与进化提示；
可选将日摘要写入 data/sediment.json，并双写到 data/evolution.db（SQLite）；
写入快照时默认向 evolution.db 的 analysis_snapshot_history 表追加**只读历史**
（与已提交的 analysis-snapshot.json 闸门分离，可用 --no-sqlite-snapshot-history 关闭）。
对 track_closure 规则比对 evolution-hint-decisions，输出 hint_closure_gaps。

输出: assets/analysis-snapshot.json
"""
from __future__ import annotations

from typing import Any

from evolution_pkg.analysis_core import run_analysis
from evolution_pkg.analysis_hints import load_hint_rules_from_path
from evolution_pkg.analysis_pipeline import (
    default_analysis_paths,
    parse_analysis_cli,
    run_analysis_pipeline,
)

# 编排真源在 ``analysis_pipeline``；本模块保留路径常量 + ``run_analysis`` / ``load_hint_rules`` 供单测与脚本导入。
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
# 模块级路径：与历史脚本/文档对齐；真源为 ``default_analysis_paths()``。
MANIFEST = _DEFAULT_PATHS.manifest
CANDIDATES = _DEFAULT_PATHS.candidates
OUT = _DEFAULT_PATHS.out_snapshot
SEDIMENT = _DEFAULT_PATHS.sediment
HINT_RULES_PATH = _DEFAULT_PATHS.hint_rules
HINT_DECISIONS_PATH = _DEFAULT_PATHS.hint_decisions


def load_hint_rules() -> dict[str, Any]:
    """仓库内 ``evolution-hint-rules.json``；单测与脚本仍从本入口调用。"""
    return load_hint_rules_from_path(_DEFAULT_PATHS.hint_rules)


def main() -> None:
    flags = parse_analysis_cli()
    run_analysis_pipeline(
        _DEFAULT_PATHS,
        check=flags.check,
        write_sediment=flags.write_sediment,
        no_sqlite_snapshot_history=flags.no_sqlite_snapshot_history,
    )


if __name__ == "__main__":
    main()
