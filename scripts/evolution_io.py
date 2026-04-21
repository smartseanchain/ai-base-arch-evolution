"""兼容层：旧代码 ``from evolution_io import …`` 仍可用；新代码请用 ``evolution_pkg.io``。"""
from __future__ import annotations

from evolution_pkg.io import (
    INGEST_CONFIG_JSON_PATH,
    INGEST_CONFIG_JSON_RELPOS,
    MAPS_TO_HINTS_JSON_PATH,
    MAPS_TO_HINTS_JSON_RELPOS,
    REGISTRY_JSON_PATH,
    REGISTRY_JSON_RELPOS,
    REPO_ROOT,
    load_json,
    load_registry_allowed_sets,
)

__all__ = [
    "INGEST_CONFIG_JSON_PATH",
    "INGEST_CONFIG_JSON_RELPOS",
    "MAPS_TO_HINTS_JSON_PATH",
    "MAPS_TO_HINTS_JSON_RELPOS",
    "REGISTRY_JSON_PATH",
    "REGISTRY_JSON_RELPOS",
    "REPO_ROOT",
    "load_json",
    "load_registry_allowed_sets",
]
