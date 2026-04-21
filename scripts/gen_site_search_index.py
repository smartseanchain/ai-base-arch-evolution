#!/usr/bin/env python3
"""
从 ``scripts/evolution-registry.json`` 的 ``pages[]`` 与各根目录 HTML 的 ``<title>``
生成 ``assets/site-search-index.json``，供读者站自建轻量搜索（**fetch** 单文件即可）。

**不**进入默认 ``make validate``；发版或增删注册页后按需执行 ``make site-search-index``。
详见 **[docs/INTEGRATION_AND_READONLY_API.md · 可选增强](../docs/INTEGRATION_AND_READONLY_API.md#optional-reader-ops-enhancements)**。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from evolution_pkg.beijing_time import now_iso_beijing  # noqa: E402
from evolution_pkg.io import REPO_ROOT, load_json  # noqa: E402

REGISTRY = REPO_ROOT / "scripts" / "evolution-registry.json"
OUT = REPO_ROOT / "assets" / "site-search-index.json"
TITLE_RE = re.compile(r"<title>([^<]{1,800})</title>", re.IGNORECASE | re.DOTALL)


def extract_title(html: str) -> str:
    m = TITLE_RE.search(html)
    if not m:
        return ""
    return " ".join(m.group(1).split())


def build_doc() -> dict:
    reg = load_json(REGISTRY)
    pages: list[str] = list(reg.get("pages") or [])
    entries: list[dict[str, str]] = []
    for page in pages:
        p = REPO_ROOT / page
        title = page
        if p.is_file():
            try:
                raw = p.read_text(encoding="utf-8", errors="replace")
                t = extract_title(raw)
                if t:
                    title = t
            except OSError:
                pass
        entries.append({"path": page, "title": title})
    return {
        "schema_version": 1,
        "generated_at": now_iso_beijing(),
        "source": "evolution-registry.json#pages + root HTML <title>",
        "entries": entries,
    }


def main() -> int:
    doc = build_doc()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(doc['entries'])} 条 · {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
