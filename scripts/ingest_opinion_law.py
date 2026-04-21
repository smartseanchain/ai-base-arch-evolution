#!/usr/bin/env python3
"""
从 ingest_config.json 中的 RSS、法规/政策 HTML 页与可选 HTTPS JSON 源抓取条目，汇总为 assets/evolution-candidates.json。

**实现**在 **``evolution_pkg.ingest_opinion_pool``**；推荐 **``PYTHONPATH=scripts python3 -m evolution_pkg.ingest_opinion_pool``**（参数相同）。
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from evolution_pkg.ingest_opinion_pool import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
