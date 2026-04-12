"""Registry → React 路径集合（工具）；完整 SPA 导航校验与生成见 evolution_pkg.spa_nav。"""
from __future__ import annotations

import json
import re
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

REGISTRY_PATH = REPO_ROOT / "scripts" / "evolution-registry.json"
NAV_LINKS_PATH = REPO_ROOT / "spa" / "src" / "navLinks.ts"


def paths_from_registry() -> set[str]:
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    pages: list[str] = reg["pages"]
    out: set[str] = set()
    for p in pages:
        if p == "index.html":
            out.add("/")
        else:
            out.add("/" + Path(p).stem)
    return out


def paths_from_nav_links_ts() -> set[str]:
    if not NAV_LINKS_PATH.is_file():
        raise FileNotFoundError(str(NAV_LINKS_PATH))
    text = NAV_LINKS_PATH.read_text(encoding="utf-8")
    return set(re.findall(r'to:\s*"([^"]+)"', text))


from evolution_pkg.spa_nav import nav_links_registry_check  # noqa: E402

__all__ = [
    "NAV_LINKS_PATH",
    "REGISTRY_PATH",
    "nav_links_registry_check",
    "paths_from_nav_links_ts",
    "paths_from_registry",
]
