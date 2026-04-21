#!/usr/bin/env python3
"""校验 assets/evolution-manifest.json 结构（逻辑见 ``evolution_pkg.signals_flat_validate``）。"""
from __future__ import annotations

import sys

from evolution_pkg.io import load_json
from evolution_pkg.signals_flat_validate import (
    MANIFEST_JSON_PATH,
    SignalsFlatValidationError,
    validate_manifest_signals_structure,
)


def main() -> None:
    if not MANIFEST_JSON_PATH.is_file():
        print(f"错误: 未找到 {MANIFEST_JSON_PATH}", file=sys.stderr)
        sys.exit(1)
    data = load_json(MANIFEST_JSON_PATH)
    try:
        n = validate_manifest_signals_structure(data)
    except SignalsFlatValidationError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print(f"OK: {n} 条信号 · {MANIFEST_JSON_PATH}")


if __name__ == "__main__":
    main()
