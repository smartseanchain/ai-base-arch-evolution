"""仓库根路径与 JSON 读取（供 scripts 下各模块共用，减少 ROOT/load_json 复制）。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict[str, Any]:
    """路径不存在时返回 {}；存在则按 UTF-8 解析，非法 JSON 抛 JSONDecodeError。"""
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
