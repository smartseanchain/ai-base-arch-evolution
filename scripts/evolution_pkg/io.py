"""仓库根路径与 JSON 读取（供 evolution_pkg 与各脚本共用）。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# scripts/evolution_pkg/io.py → 上级 scripts → 再上级仓库根
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def load_json(path: Path) -> dict[str, Any]:
    """路径不存在时返回 {}；存在则按 UTF-8 解析，非法 JSON 抛 JSONDecodeError。"""
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
