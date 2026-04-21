"""
站内 Python 管道包（架构升级：集中 I/O、分析与可复用编排）。

- ``evolution_pkg.io``：仓库根路径、JSON 读取（原 ``evolution_io`` 实现迁入此处）。
- ``evolution_pkg.signals_flat_validate``：正式 manifest / 候选池 **扁平**结构校验（**``validate-evolution-*.py``** 调包）。
- ``evolution_pkg.domains``：六域枚举与各子模块主归属（与 ``docs/INTELLIGENCE_SIX_DOMAINS.md`` 对表）；**新增顶层子模块须在此登记**。
- ``evolution_pkg.pipeline``：``make analyze`` / ``evolution-fast`` 步骤编排与遥测（调用 ``analysis_engine.py`` 等脚本入口）。
- **分析链**（热力 / 提示 / 快照 / 沉淀 / 两版 diff / 血缘）：``analysis_core``、``analysis_hints``、``hint_closure``、``analysis_validate``、``analysis_snapshot_build``、``analysis_pipeline``（含 **``main()``** CLI；推荐 **``python3 -m evolution_pkg.analysis_pipeline``**）、``analysis_diff``、``analysis_lineage``、``analysis_snapshot_history``、``sediment_validate``、``sediment_daily``、``ai_overlay_validate``、``ai_overlay_write``（可选 overlay 占位或 OpenAI 兼容外呼）、``ai_overlay_step_validate``（**``artifacts/ai-overlay-step.json``** Schema）；根目录 ``scripts/analysis_engine.py`` 为薄壳并导出路径常量与 **``load_hint_rules``**；快照 diff 为 ``scripts/diff_analysis_snapshot.py``；**``run``** 块见 ``analysis_lineage``（``lineage_utils`` 兼容入口）。
- **站点与双轨**：``nav_links``、``spa_nav``；**数据入站**：``ingest_json_http``、**``ingest_maps``**（**routes** / **maps_to_hints** / **``html_title``** / **``stable_id``**）、**``ingest_https``**、**``ingest_fetch``**、**``ingest_rss``**（**``ingest_opinion_law``** 调包）；**候选→清单**：``candidate_merge``（**``merge_candidate_ids``** / **``main()``**；根 **``merge_candidates_to_manifest.py``** 为薄壳，推荐 **``python3 -m evolution_pkg.candidate_merge``**）。
- ``evolution_pkg.ops``：运维向纯函数（如 **HTTP ETag / If-None-Match**）；**``readonly_api``** 复用。
- ``evolution_pkg.readonly_disk_routes``：只读 HTTP **磁盘 JSON** **GET** 路径表；**``readonly_api``** 启动时注册。

运行脚本时仍将 ``PYTHONPATH=scripts``（或从仓库根执行 ``python3 scripts/foo.py``，解释器会把 ``scripts/`` 加入 ``sys.path``）。
"""
from __future__ import annotations

from .domains import DOMAIN_LABEL_ZH, IntelligenceDomain, SUBMODULE_DOMAIN
from .io import REPO_ROOT, load_json

__all__ = [
    "DOMAIN_LABEL_ZH",
    "IntelligenceDomain",
    "REPO_ROOT",
    "SUBMODULE_DOMAIN",
    "load_json",
]
