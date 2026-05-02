"""SPA 导航：nav.config.json（顺序/文案）与 evolution-registry.json（允许页面）→ 生成 navLinks.ts。

改根 *.html 后维护壳内 iframe：make spa-sync。对表: docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · make help（CONTRIBUTING.md#contributing-five-minute · #contributing-pr-evidence-triad · #contributing-change-to-command）
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from evolution_pkg.io import REPO_ROOT, REGISTRY_JSON_PATH, load_registry_allowed_sets

REGISTRY_PATH = REGISTRY_JSON_PATH
NAV_CONFIG_PATH = REPO_ROOT / "spa" / "nav.config.json"
NAV_CONFIG_SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "spa-nav-config.schema.json"
NAV_LINKS_TS_PATH = REPO_ROOT / "spa" / "src" / "navLinks.ts"

TS_HEADER = """/** 由 spa/nav.config.json + scripts/gen_nav_links_ts.py 生成；请勿手改。
 * 顺序与文案：编辑 spa/nav.config.json 后执行 python3 scripts/gen_nav_links_ts.py --write
 * 与 partials/site-nav.inc.html 对齐；path 为 React Router（无 .html）
 * 改根 *.html 后维护 SPA iframe：make spa-sync；见 ../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · ../maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix · make help（CONTRIBUTING.md#contributing-five-minute · #contributing-pr-evidence-triad · #contributing-change-to-command）
 */
"""


def page_to_route(page: str) -> str:
    if page == "index.html":
        return "/"
    return "/" + Path(page).stem


def load_registry_pages_set() -> set[str]:
    pages_f, _ = load_registry_allowed_sets()
    return set(pages_f)


def nav_config_schema_violations(doc: dict[str, Any]) -> list[str]:
    """JSON Schema（Draft 2020-12）校验 nav.config 根对象。"""
    if not NAV_CONFIG_SCHEMA_PATH.is_file():
        return [f"缺少 {NAV_CONFIG_SCHEMA_PATH}"]
    try:
        schema = json.loads(NAV_CONFIG_SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{NAV_CONFIG_SCHEMA_PATH} 非合法 JSON: {e}"]
    validator = Draft202012Validator(schema)
    try:
        validator.validate(doc)
    except ValidationError as e:
        return [f"nav.config.json 不符合 Schema — {e.message}"]
    return []


def parse_nav_config_items(raw: dict[str, Any]) -> list[dict[str, Any]]:
    items = raw.get("items")
    if not isinstance(items, list):
        raise ValueError("nav.config.json 须含 items 数组")
    out: list[dict[str, Any]] = []
    for i, row in enumerate(items):
        if not isinstance(row, dict):
            raise ValueError(f"items[{i}] 须为对象")
        page = row.get("page")
        label = row.get("label")
        if not isinstance(page, str) or not isinstance(label, str):
            raise ValueError(f"items[{i}] 须含字符串 page、label")
        group = row.get("group")
        if isinstance(group, str) and group.strip():
            g = group.strip()
        else:
            g = None
        out.append({"page": page, "label": label, "group": g})
    return out


def load_nav_config_items() -> list[dict[str, Any]]:
    raw = json.loads(NAV_CONFIG_PATH.read_text(encoding="utf-8"))
    return parse_nav_config_items(raw)


def build_nav_groups(rows: list[dict[str, Any]]) -> list[tuple[str | None, list[tuple[str, str]]]]:
    """同一 group 的连续条目合并为一组；无 group 的条目各自独占一组。"""
    groups: list[tuple[str | None, list[tuple[str, str]]]] = []
    i = 0
    while i < len(rows):
        page = rows[i]["page"]
        label = rows[i]["label"]
        g = rows[i].get("group")
        if g is None:
            groups.append((None, [(page, label)]))
            i += 1
        else:
            title = g
            chunk: list[tuple[str, str]] = []
            while i < len(rows) and rows[i].get("group") == title:
                chunk.append((rows[i]["page"], rows[i]["label"]))
                i += 1
            groups.append((title, chunk))
    return groups


def nav_config_registry_errors() -> list[str]:
    """nav.config.json 与 registry 一致性（不含 navLinks.ts 文件比对）。"""
    if not REGISTRY_PATH.is_file():
        return [f"缺少 {REGISTRY_PATH}"]
    if not NAV_CONFIG_PATH.is_file():
        return [f"缺少 {NAV_CONFIG_PATH}（SPA 导航配置）"]
    try:
        reg_pages = load_registry_pages_set()
    except (json.JSONDecodeError, KeyError, ValueError, FileNotFoundError) as e:
        return [f"evolution-registry.json 无法解析或缺 pages: {e}"]
    try:
        raw_text = NAV_CONFIG_PATH.read_text(encoding="utf-8")
        doc = json.loads(raw_text)
    except json.JSONDecodeError as e:
        return [f"nav.config.json JSON 无效: {e}"]
    if not isinstance(doc, dict):
        return ["nav.config.json 根须为对象"]
    sch_errs = nav_config_schema_violations(doc)
    if sch_errs:
        return sch_errs
    try:
        items = parse_nav_config_items(doc)
    except ValueError as e:
        return [str(e)]
    cfg_pages = [p["page"] for p in items]
    cfg_set = set(cfg_pages)
    if len(cfg_pages) != len(cfg_set):
        return ["nav.config.json 中 page 重复"]
    missing = sorted(reg_pages - cfg_set)
    extra = sorted(cfg_set - reg_pages)
    errs: list[str] = []
    if missing:
        errs.append(f"nav.config 缺少 registry 页面: {missing}")
    if extra:
        errs.append(f"nav.config 含非 registry 页面: {extra}")
    return errs


def render_nav_links_ts(rows: list[dict[str, Any]]) -> str:
    groups = build_nav_groups(rows)
    flat: list[tuple[str, str]] = []
    for _t, chunk in groups:
        flat.extend(chunk)
    lines = []
    lines.append(TS_HEADER.rstrip())
    lines.append("export const NAV_LINKS: { to: string; label: string }[] = [")
    for page, label in flat:
        to = page_to_route(page)
        lines.append(
            f"  {{ to: {json.dumps(to)}, label: {json.dumps(label, ensure_ascii=False)} }},"
        )
    lines.append("];")
    lines.append("")
    lines.append(
        "export type NavGroup = { title: string | null; items: { to: string; label: string }[] };"
    )
    lines.append("export const NAV_GROUPS: NavGroup[] = [")
    for title, chunk in groups:
        if title is None:
            for page, label in chunk:
                to = page_to_route(page)
                lines.append(
                    "  { "
                    f"title: null, items: [{{ to: {json.dumps(to)}, label: {json.dumps(label, ensure_ascii=False)} }}] "
                    "},"
                )
        else:
            inner = ", ".join(
                f"{{ to: {json.dumps(page_to_route(p))}, label: {json.dumps(lb, ensure_ascii=False)} }}"
                for p, lb in chunk
            )
            lines.append(
                f"  {{ title: {json.dumps(title, ensure_ascii=False)}, items: [{inner}] }},"
            )
    lines.append("];")
    return "\n".join(lines) + "\n"


def expected_nav_links_ts_content() -> tuple[list[str], str]:
    """(errors, content). errors 非空时不应使用 content。"""
    errs = nav_config_registry_errors()
    if errs:
        return errs, ""
    try:
        items = load_nav_config_items()
    except (json.JSONDecodeError, ValueError) as e:
        return [str(e)], ""
    return [], render_nav_links_ts(items)


def nav_links_generated_matches_disk() -> list[str]:
    """navLinks.ts 与由 nav.config + registry 生成的内容一致则返回 []。"""
    errs = nav_config_registry_errors()
    if errs:
        return errs
    _, expected = expected_nav_links_ts_content()
    if not expected:
        return ["内部错误: 无法生成期望 navLinks.ts"]
    if not NAV_LINKS_TS_PATH.is_file():
        return [f"缺少 {NAV_LINKS_TS_PATH}"]
    actual = NAV_LINKS_TS_PATH.read_text(encoding="utf-8")
    if actual == expected:
        return []
    return [
        "spa/src/navLinks.ts 与 spa/nav.config.json 生成结果不一致。",
        "  执行: python3 scripts/gen_nav_links_ts.py --write",
    ]


def nav_links_registry_check() -> tuple[bool, list[str]]:
    """(skipped, errors)。无 spa/package.json 时跳过（未启用 SPA 工程）。"""
    if not REGISTRY_PATH.is_file():
        return False, [f"缺少 {REGISTRY_PATH}"]
    if not (REPO_ROOT / "spa" / "package.json").is_file():
        return True, []
    if not NAV_CONFIG_PATH.is_file():
        return False, [
            f"缺少 {NAV_CONFIG_PATH}（存在 spa/package.json 时必填）。"
            " 新建页面后编辑 items 并执行: python3 scripts/gen_nav_links_ts.py --write",
        ]
    if not NAV_LINKS_TS_PATH.is_file():
        return False, [
            f"缺少 {NAV_LINKS_TS_PATH}。执行: python3 scripts/gen_nav_links_ts.py --write",
        ]
    return False, nav_links_generated_matches_disk()
