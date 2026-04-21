"""仓库根路径与 JSON 读取（供 evolution_pkg 与各脚本共用）。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# scripts/evolution_pkg/io.py → 上级 scripts → 再上级仓库根
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# merge / SPA 双轨文档锚点（仓库根）：docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · make help

# 仓库内相对路径（POSIX）；与 ``readonly_api`` 磁盘路由、文档中的 ``scripts/…`` 表述一致。
REGISTRY_JSON_RELPOS = "scripts/evolution-registry.json"
REGISTRY_JSON_PATH = REPO_ROOT / REGISTRY_JSON_RELPOS

INGEST_CONFIG_JSON_RELPOS = "scripts/ingest_config.json"
MAPS_TO_HINTS_JSON_RELPOS = "scripts/maps_to_hints.json"
INGEST_CONFIG_JSON_PATH = REPO_ROOT / INGEST_CONFIG_JSON_RELPOS
MAPS_TO_HINTS_JSON_PATH = REPO_ROOT / MAPS_TO_HINTS_JSON_RELPOS


def load_json(path: Path) -> dict[str, Any]:
    """路径不存在时返回 {}；存在则按 UTF-8 解析，非法 JSON 抛 JSONDecodeError。"""
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry_allowed_sets() -> tuple[frozenset[str], frozenset[str]]:
    """读取 **evolution-registry.json**，返回 (允许页面, 允许 lab_factors)。

    与 **check_manifest_drift**、**validate_golden_mapping**、**validate_evolution_hint_decisions**、
    **gen-sitemap**、**spa_nav** / **nav_links** 等「pages / lab_factors 白名单」语义一致。
    """
    doc = load_json(REGISTRY_JSON_PATH)
    if not doc:
        raise FileNotFoundError(f"缺少或无法读取注册表: {REGISTRY_JSON_PATH}")
    pages = doc.get("pages")
    facs = doc.get("lab_factors")
    if not isinstance(pages, list) or not isinstance(facs, list):
        raise ValueError(
            f"{REGISTRY_JSON_PATH}: pages 与 lab_factors 须为数组"
        )
    return (
        frozenset(str(p).strip() for p in pages if str(p).strip()),
        frozenset(str(f).strip() for f in facs if str(f).strip()),
    )
