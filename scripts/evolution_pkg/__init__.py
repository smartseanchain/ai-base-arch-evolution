"""
站内 Python 管道包（架构升级：集中 I/O 与可复用编排）。

- ``evolution_pkg.io``：仓库根路径、JSON 读取（原 ``evolution_io`` 实现迁入此处）。
- ``evolution_pkg.pipeline``：``make analyze`` / ``evolution-fast`` 步骤编排与遥测。

运行脚本时仍将 ``PYTHONPATH=scripts``（或从仓库根执行 ``python3 scripts/foo.py``，解释器会把 ``scripts/`` 加入 ``sys.path``）。
"""
from __future__ import annotations

from .io import REPO_ROOT, load_json

__all__ = ["REPO_ROOT", "load_json"]
