"""根目录 *.html 与 admin-console 静态壳中，指向 docs/*.md 的 href 须带 URL fragment。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_ADMIN_CONSOLE_INDEX = REPO_ROOT / "admin-console" / "static" / "index.html"


class TestRootHtmlDocsMarkdownHrefs(unittest.TestCase):
    def _check_href_relative_docs_md(self, rel: Path, body: str) -> None:
        for m in re.finditer(r'href="(docs/[^"]+)"', body):
            url = m.group(1)
            if ".md" not in url:
                continue
            with self.subTest(path=str(rel), href=url):
                self.assertFalse(
                    url.endswith(".md"),
                    msg="docs Markdown href missing URL fragment",
                )
                self.assertIn("#", url)

    def _check_href_github_blob_docs_md(self, rel: Path, body: str) -> None:
        for m in re.finditer(r'href="(https://github\.com[^"]+)"', body):
            url = m.group(1)
            if "/docs/" not in url or ".md" not in url:
                continue
            with self.subTest(path=str(rel), href=url):
                self.assertIn(
                    "#",
                    url,
                    msg="GitHub blob 指向 docs/*.md 的 href 缺少 URL fragment",
                )

    def test_root_html_docs_md_hrefs_have_url_fragments(self) -> None:
        for path in sorted(REPO_ROOT.glob("*.html")):
            rel = path.relative_to(REPO_ROOT)
            body = path.read_text(encoding="utf-8")
            self._check_href_relative_docs_md(rel, body)

    def test_admin_console_static_docs_md_hrefs_have_fragments(self) -> None:
        self.assertTrue(
            _ADMIN_CONSOLE_INDEX.is_file(),
            msg="缺少 admin-console/static/index.html",
        )
        rel = _ADMIN_CONSOLE_INDEX.relative_to(REPO_ROOT)
        body = _ADMIN_CONSOLE_INDEX.read_text(encoding="utf-8")
        self._check_href_relative_docs_md(rel, body)
        self._check_href_github_blob_docs_md(rel, body)


if __name__ == "__main__":
    unittest.main()
