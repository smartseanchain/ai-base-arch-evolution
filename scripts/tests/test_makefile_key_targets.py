"""Makefile 关键目标名防漂移（与文档 / CONTRIBUTING 对表）。"""
from __future__ import annotations

import unittest
from pathlib import Path

_TRIPLET_IDS = (
    "contributing-five-minute",
    "contributing-pr-evidence-triad",
    "contributing-change-to-command",
)

# 枢纽文档：任一行若同时出现三 CONTRIBUTING fragment，须与根 Makefile `help` 同序。
_MAKE_HELP_TRIPLET_NEEDLE = (
    "make help（CONTRIBUTING.md#contributing-five-minute · "
    "#contributing-pr-evidence-triad · #contributing-change-to-command）"
)

_TRIPLET_ORDER_DOC_PATHS = (
    "CONTRIBUTING.md",
    "README.md",
    "docs/README.md",
    "docs/MERGE_AND_RELEASE_CHECKLIST.md",
    "AGENTS.md",
    "scripts/README.md",
    ".cursor/rules/repo-gates.mdc",
    ".github/pull_request_template.md",
    ".cursor/rules/spa-nav-config.mdc",
    ".cursor/rules/spa-nav-registry.mdc",
    ".cursor/rules/evolution-registry.mdc",
    "spa/README.md",
    "admin-console/README.md",
    "partials/site-nav.inc.html",
)


def _triplet_order_scan_paths(root: Path) -> list[Path]:
    """显式列表 + 根目录 MPA `*.html` + `spa/public` 下 `CONTRIBUTING.md` 与 `*.html` + 管理端静态壳 + compose + workflows + `scripts/*.sh` + Issue 模板（去重）。"""
    seen: set[str] = set()
    out: list[Path] = []
    for rel in _TRIPLET_ORDER_DOC_PATHS:
        p = root / rel
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            out.append(p)
    for p in sorted(root.glob("*.html")):
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            out.append(p)
    admin_index = root / "admin-console" / "static" / "index.html"
    if admin_index.is_file():
        key = str(admin_index.resolve())
        if key not in seen:
            out.append(admin_index)
    for rel in ("docker-compose.yml", "docker-compose.dev.yml"):
        p = root / rel
        if p.is_file():
            key = str(p.resolve())
            if key not in seen:
                seen.add(key)
                out.append(p)
    wf_dir = root / ".github" / "workflows"
    if wf_dir.is_dir():
        for p in sorted(wf_dir.glob("*.yml")):
            key = str(p.resolve())
            if key not in seen:
                seen.add(key)
                out.append(p)
    scripts_dir = root / "scripts"
    if scripts_dir.is_dir():
        for p in sorted(scripts_dir.glob("*.sh")):
            key = str(p.resolve())
            if key not in seen:
                seen.add(key)
                out.append(p)
    issue_tmpl = root / ".github" / "ISSUE_TEMPLATE"
    if issue_tmpl.is_dir():
        for p in sorted(issue_tmpl.glob("*.md")):
            key = str(p.resolve())
            if key not in seen:
                seen.add(key)
                out.append(p)
    spa_public = root / "spa" / "public"
    if spa_public.is_dir():
        spa_contrib = spa_public / "CONTRIBUTING.md"
        if spa_contrib.is_file():
            key = str(spa_contrib.resolve())
            if key not in seen:
                seen.add(key)
                out.append(spa_contrib)
        for p in sorted(spa_public.glob("*.html")):
            key = str(p.resolve())
            if key not in seen:
                seen.add(key)
                out.append(p)
    return out


class TestMakefileKeyTargets(unittest.TestCase):
    def test_documented_targets_present(self) -> None:
        root = Path(__file__).resolve().parents[2]
        mf = root / "Makefile"
        self.assertTrue(mf.is_file(), msg="缺少根 Makefile")
        text = mf.read_text(encoding="utf-8")
        for needle in (
            "validate-fast:",
            "clean-pipeline-metrics-dry-run:",
            "clean-pipeline-metrics:",
            "clean-overlay-artifacts:",
            "validate:",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text, msg=f"Makefile 须保留目标 {needle!r}")

    def test_help_first_echo_pairs_contributing_anchors(self) -> None:
        root = Path(__file__).resolve().parents[2]
        text = (root / "Makefile").read_text(encoding="utf-8")
        self.assertIn(
            "开 PR 前速览：CONTRIBUTING.md#contributing-five-minute · PR 证据三联：CONTRIBUTING.md#contributing-pr-evidence-triad · 动手→命令速查：CONTRIBUTING.md#contributing-change-to-command",
            text,
            msg="Makefile help 首行应将开 PR 前速览、PR 证据三联与动手→命令速查并列（与 README / CONTRIBUTING 对表）",
        )

    def test_run_validate_scripts_comment_make_help_pairs_contributing_anchors(
        self,
    ) -> None:
        root = Path(__file__).resolve().parents[2]
        needle = _MAKE_HELP_TRIPLET_NEEDLE
        for rel in (
            "scripts/run_validate.sh",
            "scripts/run_validate_fast.sh",
            ".githooks/pre-commit",
            "scripts/install-git-hooks.sh",
        ):
            with self.subTest(script=rel):
                path = root / rel
                self.assertTrue(path.is_file(), msg=f"缺少 {rel}")
                body = path.read_text(encoding="utf-8")
                self.assertIn(
                    needle,
                    body,
                    msg=f"{rel} 应与 pre-commit / compose 收束注释同构 {needle!r}",
                )

    def test_makefile_help_echo_contributing_anchor_token_order(self) -> None:
        """`make help` 首行 echo 中三 CONTRIBUTING 锚须与 CONTRIBUTING 文首句同序（速览→三联→速查）。"""
        root = Path(__file__).resolve().parents[2]
        mf = (root / "Makefile").read_text(encoding="utf-8")
        echo_line = None
        after_help = False
        for line in mf.splitlines():
            if line.rstrip() == "help:":
                after_help = True
                continue
            if after_help and line.lstrip().startswith("@echo"):
                echo_line = line
                break
        self.assertIsNotNone(echo_line, msg="Makefile 应有 help: 后的首条 @echo")
        t5 = echo_line.index("contributing-five-minute")
        tt = echo_line.index("contributing-pr-evidence-triad")
        tc = echo_line.index("contributing-change-to-command")
        self.assertLess(t5, tt, msg="make help：开 PR 前速览须在 PR 证据三联之前")
        self.assertLess(tt, tc, msg="make help：PR 证据三联须在动手→命令速查之前")

    def test_hub_docs_any_line_three_contributing_ids_follow_make_help_order(
        self,
    ) -> None:
        """枢纽 md/mdc、PR 模板、partial、根与 `spa/public` 的 `*.html`、壳内 CONTRIBUTING、admin 壳、compose、workflows、`scripts/*.sh`、Issue 模板：同行三 id 须 five→triad→cmd。"""
        root = Path(__file__).resolve().parents[2]
        f5, ft, fc = _TRIPLET_IDS
        for path in _triplet_order_scan_paths(root):
            rel = path.relative_to(root).as_posix()
            with self.subTest(doc=rel):
                self.assertTrue(path.is_file(), msg=f"缺少 {rel}")
                body = path.read_text(encoding="utf-8")
                for lineno, line in enumerate(body.splitlines(), start=1):
                    if f5 not in line or ft not in line or fc not in line:
                        continue
                    with self.subTest(doc=rel, line=lineno):
                        self.assertLess(
                            line.index(f5),
                            line.index(ft),
                            msg=f"{rel}:{lineno} 三锚顺序应为 开 PR 前速览 → PR 证据三联 → 动手→命令速查",
                        )
                        self.assertLess(
                            line.index(ft),
                            line.index(fc),
                            msg=f"{rel}:{lineno} 三锚顺序应为 PR 证据三联 → 动手→命令速查",
                        )

    def test_gate_python_module_docstrings_include_make_help_triplet(self) -> None:
        """evolution_pkg / 闸门脚本顶注与 run_validate.sh 同构（make help 三锚收束串）。"""
        root = Path(__file__).resolve().parents[2]
        for rel in (
            "scripts/evolution_pkg/io.py",
            "scripts/evolution_pkg/spa_nav.py",
            "scripts/run_pipeline_steps.py",
            "scripts/sync_site_nav.py",
            "scripts/gen_nav_links_ts.py",
            "scripts/sync_spa_public.py",
        ):
            with self.subTest(module=rel):
                path = root / rel
                self.assertTrue(path.is_file(), msg=f"缺少 {rel}")
                body = path.read_text(encoding="utf-8")
                self.assertIn(
                    _MAKE_HELP_TRIPLET_NEEDLE,
                    body,
                    msg=f"{rel} 顶注/注释须含 {_MAKE_HELP_TRIPLET_NEEDLE!r}",
                )


if __name__ == "__main__":
    unittest.main()
