"""
站内 Python 管道包（架构升级：集中 I/O、分析与可复用编排）。

- ``evolution_pkg.io``：仓库根路径、JSON 读取（原 ``evolution_io`` 实现迁入此处）。
- ``evolution_pkg.domains``：六域枚举与各子模块主归属（与 ``docs/INTELLIGENCE_SIX_DOMAINS.md`` 对表）；**新增顶层子模块须在此登记**。
- ``evolution_pkg.pipeline``：``make analyze`` / ``evolution-fast`` 步骤编排与遥测（调用 ``analysis_engine.py`` 等脚本入口）。
- **分析链**（热力 / 提示 / 快照 / 沉淀）：``analysis_core``、``analysis_hints``、``hint_closure``、``analysis_validate``、``analysis_snapshot_build``、``analysis_pipeline``、``analysis_snapshot_history``、``sediment_validate``、``sediment_daily``、``ai_overlay_validate``；CLI 真源仍为根目录 ``scripts/analysis_engine.py``（薄封装）。
- **站点与双轨**：``nav_links``、``spa_nav``；**数据入站**：``ingest_json_http``。
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
