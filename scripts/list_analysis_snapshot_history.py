#!/usr/bin/env python3
"""
列出 data/evolution.db 中 analysis_snapshot_history 元数据（run_id、时间、JSON 字节数）。

**推荐**：``PYTHONPATH=scripts python3 -m evolution_pkg.analysis_snapshot_history``（同参数）。

完整快照示例（需在仓库根且 ``PYTHONPATH=scripts``）::

  python3 -c "import json; from sqlite_store import get_analysis_snapshot_history; print(json.dumps(get_analysis_snapshot_history('RUN_ID'), ensure_ascii=False, indent=2))"
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from evolution_pkg.analysis_snapshot_history import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
