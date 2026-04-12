"""关键入口 shell 中直接调用的 scripts/*.py 须存在（防漏迁、防改名后未改闸门/管道）。

覆盖：run_validate.sh、run_update_pipeline.sh、run_analyze_write.sh、run_ingest_only.sh。
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

# 不含 echo 内提示字符串；仅匹配行首（strip 后）真实调用。
_RE = re.compile(r"^(?:exec\s+)?python3\s+scripts/([^\s#]+\.py)")

_GATE_SHELLS = (
    "scripts/run_validate.sh",
    "scripts/run_update_pipeline.sh",
    "scripts/run_analyze_write.sh",
    "scripts/run_ingest_only.sh",
)


class TestGateShellScriptPyRefs(unittest.TestCase):
    def test_each_invoked_script_exists(self) -> None:
        root = Path(__file__).resolve().parents[2]
        for rel_sh in _GATE_SHELLS:
            with self.subTest(shell=rel_sh):
                script_path = root / rel_sh
                self.assertTrue(script_path.is_file(), msg=f"缺少 {rel_sh}")
                lines = script_path.read_text(encoding="utf-8").splitlines()
                seen: list[str] = []
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    m = _RE.match(line)
                    if not m:
                        continue
                    rel_py = m.group(1)
                    seen.append(rel_py)
                    target = root / "scripts" / rel_py
                    self.assertTrue(
                        target.is_file(),
                        msg=f"{rel_sh} 调用 scripts/{rel_py}，但文件不存在",
                    )
                self.assertTrue(
                    seen,
                    msg=f"{rel_sh} 应至少包含一条 python3 scripts/*.py（或 exec python3 …）调用",
                )


if __name__ == "__main__":
    unittest.main()
