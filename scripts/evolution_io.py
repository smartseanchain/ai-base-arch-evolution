"""兼容层：旧代码 ``from evolution_io import …`` 仍可用；新代码请用 ``evolution_pkg.io``。"""
from __future__ import annotations

from evolution_pkg.io import REPO_ROOT, load_json

__all__ = ["REPO_ROOT", "load_json"]
