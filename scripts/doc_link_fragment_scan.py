"""Shared repo scan: Markdown / href 指向 `*.md` 却无 `#fragment` 的违禁子串。

供 test_agents_doc_anchors / test_contributing_doc_anchors / test_merge_checklist_doc_anchors /
test_docs_readme_doc_anchors 共用，避免多份相同的 rglob 与判定逻辑漂移。

`collect_doc_link_offenders(repo_root, "docs/README")` 用于禁止裸链 **`docs/README.md`**（Markdown
闭括号或 `href` 无 URL `#fragment`）；文首/双轨入口统一 **`#content-framework`**（与
`docs/README.md` 文首导读一致）。

位于 `scripts/` 以便 `PYTHONPATH=scripts` 与 `unittest discover -s scripts/tests` 均可
`import doc_link_fragment_scan`。
"""

from __future__ import annotations

from pathlib import Path

SKIP_DIR_NAMES = frozenset(
    {".git", "node_modules", "__pycache__", ".venv", "venv", "dist"},
)
SCAN_SUFFIXES = frozenset({".md", ".mdc", ".yaml", ".yml", ".json", ".html"})

_REASON_MARKDOWN = "markdown-style .md)"
_REASON_HREF_DQ = 'href … .md"'
_REASON_HREF_SQ = "href … .md'"


def link_fragments_missing_hash(stem: str) -> tuple[str, str, str]:
    """返回三类违禁子串：Markdown 闭括号、双引号 href、单引号 href（均无 URL hash）。"""
    return (
        stem + ".md)",
        stem + '.md"',
        stem + ".md'",
    )


def collect_doc_link_offenders(repo_root: Path, stem: str) -> list[str]:
    """全仓扫描：命中任一违禁子串的相对路径 + 原因列表（稳定排序）。"""
    md_bad, href_dq, href_sq = link_fragments_missing_hash(stem)
    offenders: list[str] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if SKIP_DIR_NAMES.intersection(path.parts):
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        reasons: list[str] = []
        if md_bad in body:
            reasons.append(_REASON_MARKDOWN)
        if href_dq in body:
            reasons.append(_REASON_HREF_DQ)
        if href_sq in body:
            reasons.append(_REASON_HREF_SQ)
        if not reasons:
            continue
        rel = path.relative_to(repo_root)
        offenders.append(f"{rel} ({', '.join(reasons)})")
    offenders.sort()
    return offenders
