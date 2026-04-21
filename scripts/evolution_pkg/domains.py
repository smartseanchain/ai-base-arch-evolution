"""
六域协同（智能化）在 ``evolution_pkg`` 内的落点：枚举 + 子模块归属。

人读真源：仓库 ``docs/INTELLIGENCE_SIX_DOMAINS.md``。新增 ``evolution_pkg`` 顶层
子模块时，须在本文件的 ``SUBMODULE_DOMAIN`` 中登记，否则
``scripts/tests/test_evolution_pkg.py`` 会失败。
"""
from __future__ import annotations

from enum import Enum
from pathlib import Path


class IntelligenceDomain(str, Enum):
    """与文档 INTELLIGENCE_SIX_DOMAINS 六域一一对应（值为稳定英文键）。"""

    DATA = "data"
    PIPELINE = "pipeline"
    ANALYSIS = "analysis"
    FRONTEND = "frontend"
    OPS = "ops"
    GOVERNANCE = "governance"


DOMAIN_LABEL_ZH: dict[IntelligenceDomain, str] = {
    IntelligenceDomain.DATA: "数据",
    IntelligenceDomain.PIPELINE: "管道",
    IntelligenceDomain.ANALYSIS: "分析",
    IntelligenceDomain.FRONTEND: "前端",
    IntelligenceDomain.OPS: "运维",
    IntelligenceDomain.GOVERNANCE: "治理",
}


# evolution_pkg 下可 import 的顶层子模块（文件名去 .py，或子包名）→ 主归属域
SUBMODULE_DOMAIN: dict[str, IntelligenceDomain] = {
    "io": IntelligenceDomain.DATA,
    "signals_flat_validate": IntelligenceDomain.DATA,
    "candidate_merge": IntelligenceDomain.GOVERNANCE,
    "ingest_json_http": IntelligenceDomain.DATA,
    "ingest_maps": IntelligenceDomain.DATA,
    "ingest_https": IntelligenceDomain.DATA,
    "ingest_fetch": IntelligenceDomain.DATA,
    "ingest_rss": IntelligenceDomain.DATA,
    "ingest_opinion_pool": IntelligenceDomain.DATA,
    "sediment_validate": IntelligenceDomain.DATA,
    "sediment_daily": IntelligenceDomain.DATA,
    "ai_overlay_validate": IntelligenceDomain.ANALYSIS,
    "ai_overlay_write": IntelligenceDomain.ANALYSIS,
    "ai_overlay_step_validate": IntelligenceDomain.ANALYSIS,
    "analysis_snapshot_history": IntelligenceDomain.ANALYSIS,
    "hint_closure": IntelligenceDomain.ANALYSIS,
    "analysis_hints": IntelligenceDomain.ANALYSIS,
    "analysis_core": IntelligenceDomain.ANALYSIS,
    "analysis_validate": IntelligenceDomain.ANALYSIS,
    "analysis_snapshot_build": IntelligenceDomain.ANALYSIS,
    "analysis_pipeline": IntelligenceDomain.ANALYSIS,
    "analysis_diff": IntelligenceDomain.ANALYSIS,
    "analysis_lineage": IntelligenceDomain.ANALYSIS,
    "nav_links": IntelligenceDomain.FRONTEND,
    "spa_nav": IntelligenceDomain.FRONTEND,
    "ops": IntelligenceDomain.OPS,
    "beijing_time": IntelligenceDomain.OPS,
    "readonly_disk_routes": IntelligenceDomain.OPS,
    "pipeline": IntelligenceDomain.PIPELINE,
}


def evolution_pkg_submodule_names() -> frozenset[str]:
    """``evolution_pkg`` 目录下应登记域的顶层子模块名（不含本模块与包根 __init__）。"""
    pkg = Path(__file__).resolve().parent
    names: set[str] = set()
    for p in pkg.iterdir():
        if p.name in ("__init__.py", "domains.py"):
            continue
        if p.name.startswith("__"):
            continue
        if p.is_dir():
            if (p / "__init__.py").is_file():
                names.add(p.name)
        elif p.suffix == ".py":
            names.add(p.stem)
    return frozenset(names)
