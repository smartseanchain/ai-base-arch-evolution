"""管理端 ``READONLY_PROXY_SEGMENTS`` 与 ``readonly_api`` 单段路径对账。

``admin-console`` 镜像不挂载 ``scripts/``，故对账放在本目录，经 ``importlib`` 加载
``admin-console/app/settings.py``（仅标准库依赖）。
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

from readonly_test_util import READONLY_API_SKIP_REASON, readonly_api_available

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_admin_readonly_segments() -> frozenset[str]:
    path = _REPO_ROOT / "admin-console" / "app" / "settings.py"
    name = "_admin_settings_readonly_gate"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod.READONLY_PROXY_SEGMENTS


def _readonly_single_path_segments() -> frozenset[str]:
    import readonly_api

    out: set[str] = set()
    for route in readonly_api.app.routes:
        p = getattr(route, "path", None)
        if not p or p == "/":
            continue
        if "{" in p:
            continue
        if p.count("/") != 1:
            continue
        out.add(p[1:])
    return frozenset(out)


# ``readonly_api`` 默认还带 ``/redoc``；管理台 BFF 白名单不转发（减暴露；需要时再并入）。
_ADMIN_PROXY_OMIT: frozenset[str] = frozenset({"redoc"})


@unittest.skipUnless(
    readonly_api_available(),
    READONLY_API_SKIP_REASON,
)
class TestReadonlyProxySegmentSync(unittest.TestCase):
    def test_admin_allowlist_matches_readonly_single_paths(self) -> None:
        computed = _readonly_single_path_segments()
        expected = frozenset(computed - _ADMIN_PROXY_OMIT)
        admin = _load_admin_readonly_segments()
        self.assertEqual(
            admin,
            expected,
            msg=(
                "增删 ``readonly_api`` 单段 GET 或调整 FastAPI 内置文档路由后，请同步 "
                "``admin-console/app/settings.py`` · ``READONLY_PROXY_SEGMENTS``；"
                "若有意不代理某路径，改 ``_ADMIN_PROXY_OMIT`` 并写明原因。"
            ),
        )
