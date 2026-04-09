"""分析流水线血缘：run_id、仓库 revision（供 analysis_engine 与校验脚本共用）。"""
from __future__ import annotations

import secrets
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evolution_io import REPO_ROOT


def get_repo_revision_short(cwd: Path | None = None) -> str:
    """`git rev-parse --short HEAD`，非 git 环境或失败时返回 ``unknown``。"""
    base = cwd or REPO_ROOT
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=base,
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "unknown"


def build_run_block() -> dict[str, Any]:
    """单次 analyze 运行的标识，写入 analysis-snapshot.run 与当日 sediment 条目。"""
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    return {
        "run_id": f"{day}-{secrets.token_hex(4)}",
        "repo_revision": get_repo_revision_short(),
    }
