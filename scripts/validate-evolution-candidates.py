#!/usr/bin/env python3
"""校验 assets/evolution-candidates.json（逻辑见 ``evolution_pkg.signals_flat_validate``）。"""
from __future__ import annotations

import sys

from evolution_pkg.io import load_json
from evolution_pkg.signals_flat_validate import (
    CANDIDATES_JSON_PATH,
    SignalsFlatValidationError,
    validate_candidates_signals_structure,
)


def main() -> None:
    if not CANDIDATES_JSON_PATH.is_file():
        print(f"OK: {CANDIDATES_JSON_PATH} 不存在（运行 ingest 后生成）")
        return
    data = load_json(CANDIDATES_JSON_PATH)
    try:
        n = validate_candidates_signals_structure(data)
    except SignalsFlatValidationError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print(f"OK: {n} 条候选 · {CANDIDATES_JSON_PATH}")


if __name__ == "__main__":
    main()
