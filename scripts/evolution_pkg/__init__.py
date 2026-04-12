"""
站内 Python 管道包（架构升级：集中 I/O 与可复用编排）。

- ``evolution_pkg.io``：仓库根路径、JSON 读取（原 ``evolution_io`` 实现迁入此处）。
- ``evolution_pkg.pipeline``：``make analyze`` / ``evolution-fast`` 步骤编排与遥测。
- ``evolution_pkg.domains``：六域协同枚举与各子模块主归属（与 ``docs/INTELLIGENCE_SIX_DOMAINS.md`` 对表）。
- ``evolution_pkg.ops``：运维向纯函数（如 **HTTP ETag / If-None-Match**），无 Web 框架依赖；**``readonly_api``** 复用。
- ``evolution_pkg.readonly_disk_routes``：只读 HTTP **磁盘 JSON** **GET** 路径表（无 FastAPI）；**``readonly_api``** 启动时注册。

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
