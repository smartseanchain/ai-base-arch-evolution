"""admin-console 烟测（需先 ``pip install -r admin-console/requirements.txt``）。"""
from __future__ import annotations

import os
import unittest
from unittest import mock

from fastapi.testclient import TestClient

from app.main import app


class TestAdminConsoleSmoke(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        r = self.client.get("/health")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["service"], "admin-console")
        self.assertIn("readonly_api_base_url", data)
        self.assertIn("repo_web_base", data)
        self.assertIn("admin_accounts_enabled", data)
        self.assertIsInstance(data["admin_accounts_enabled"], bool)

    def test_index_dashboard_html(self) -> None:
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"text/html", r.headers.get("content-type", "").encode())
        body = r.text
        self.assertIn("演进站点", body)
        self.assertIn('name="description"', body)
        self.assertIn('name="theme-color"', body)
        self.assertIn('name="color-scheme"', body)
        self.assertIn('content="dark light"', body)
        self.assertIn("(prefers-color-scheme: dark)", body)
        self.assertIn("(prefers-color-scheme: light)", body)
        self.assertIn("探索器状态行:", body)
        self.assertIn("读者面与管理面对表（只读提示）", body)
        self.assertIn("link-platform-reader-admin-matrix", body)
        self.assertIn("reader-admin-contract-matrix", body)
        self.assertIn("复制摘要", body)
        self.assertIn("长页滚动", body)
        self.assertIn("读屏可听", body)
        self.assertIn('aria-label="只读 API 响应正文"', body)
        self.assertIn('spellcheck="false"', body)
        self.assertIn("探索器正文", body)
        self.assertIn("跳到主内容", body)
        self.assertIn("skip-link", body)
        self.assertIn("wireSkipLinkFocusMain", body)
        self.assertIn('aria-modal="true"', body)
        self.assertIn('id="header-breadcrumb"', body)
        self.assertIn("当前：概览", body)
        self.assertIn('id="announcer"', body)
        self.assertIn('id="btn-copy-page-link"', body)
        self.assertIn('class="toolbar-actions" role="toolbar"', body)
        self.assertIn('aria-label="顶栏：快捷方式、外观主题、复制链接与刷新数据"', body)
        self.assertIn('id="theme-appearance"', body)
        self.assertIn('id="theme-appearance-hint"', body)
        self.assertIn('aria-describedby="theme-appearance-hint"', body)
        self.assertIn("adminConsoleTheme", body)
        self.assertIn("复制链接", body)
        self.assertIn('aria-label="复制当前完整 URL（含模块锚点），便于分享"', body)
        self.assertIn("打开键盘快捷方式说明", body)
        self.assertIn('id="btn-kbd-help"', body)
        self.assertIn("快捷键", body)
        self.assertIn('id="kbd-help-dialog"', body)
        self.assertIn("键盘快捷方式", body)
        self.assertIn('data-default-label="刷新数据"', body)
        self.assertIn("重新拉取 bootstrap", body)
        self.assertIn("ingest 配置（若已配置只读基址）", body)
        self.assertIn('id="explore-status"', body)
        self.assertIn("当前探索器请求的 HTTP 状态、体积与耗时", body)
        self.assertIn("aria-live=polite", body)
        self.assertIn("本页键盘快捷方式一览", body)
        self.assertIn("模块顶栏（中等以下视口）", body)
        self.assertIn("aria-describedby=\"mod-analysis-lead mod-analysis-boundary\"", body)
        self.assertIn("模块边界（读屏）", body)
        self.assertIn("系统配色", body)
        self.assertIn("prefers-reduced-transparency", body)
        self.assertIn("动效与透明度", body)
        self.assertIn("prefersReducedMotionOrTransparency", body)
        self.assertIn('th scope="col">键或区域', body)
        self.assertIn('th scope="col">说明', body)
        self.assertIn("探索器来源标签:", body)
        self.assertIn('parts.push("模块（顶栏）:', body)
        self.assertIn('role="contentinfo"', body)
        self.assertIn('id="btn-footer-kbd-help"', body)
        self.assertIn("site-footer", body)
        self.assertIn('b.title = "GET /api/readonly/" + seg', body)
        self.assertIn("视当前模块", body)
        self.assertIn("lastSpyModuleId", body)
        self.assertIn("urlHashLayoutResyncOnce", body)
        self.assertIn("首屏与首次数据拉取后", body)
        self.assertIn("pathQsHash", body)
        self.assertIn("路径与查询参数", body)
        self.assertIn("观测摘要", body)
        self.assertIn('id="obs-signals" role="status"', body)
        self.assertIn("aria-atomic", body)
        self.assertIn('"页面标题: " +', body)
        self.assertIn('id="seg-grid"', body)
        self.assertIn('role="toolbar"', body)
        self.assertIn('id="obs-auto-hint"', body)
        self.assertIn('class="obs-toolbar" role="toolbar"', body)
        self.assertIn('aria-label="观测摘要：值守与复制"', body)
        self.assertIn('explore-actions-btns" role="toolbar"', body)
        self.assertIn('aria-label="探索器正文操作"', body)
        self.assertIn("页签隐藏时暂停定时器", body)
        self.assertIn('aria-describedby="obs-auto-hint"', body)
        self.assertIn("自动刷新", body)
        self.assertIn("服务端时间（北京时间）", body)
        self.assertIn('id="btn-obs-copy-digest"', body)
        self.assertIn("复制观测摘要", body)
        self.assertIn('id="obs-boot-fetch-ms"', body)
        self.assertIn("GET /api/bootstrap", body)
        self.assertIn("ingest-config 拉取超时", body)
        self.assertIn("bootstrap_error_preview", body)
        self.assertIn("ingestConfigTimeout", body)
        self.assertIn("kbdHelpReturnFocus", body)
        self.assertIn('id="obs-parallel-ms"', body)
        self.assertIn("本机网络", body)
        self.assertIn('id="pill-net"', body)
        self.assertIn("aria-pressed", body)
        self.assertIn("随页面刷新", body)
        self.assertIn("@media print", body)
        self.assertIn("prefers-contrast: more", body)
        self.assertIn("prefers-color-scheme: light", body)
        self.assertIn("forced-colors: active", body)
        self.assertIn("admin-theme-color-override", body)
        self.assertIn("onOsColorSchemeChange", body)
        self.assertIn("kbdDialogSavedTitle", body)
        self.assertIn("另一标签页", body)
        self.assertIn("AbortSignal.any", body)
        self.assertIn("AbortSignal.timeout", body)
        self.assertIn("fetchWithOptionalTimeout", body)
        self.assertIn("PARALLEL_LOAD_FETCH_TIMEOUT_MS", body)
        self.assertIn("并行刷新", body)
        self.assertIn('id="explore-open-tab"', body)
        self.assertIn('id="admin-primary-nav"', body)
        self.assertIn('id="mod-overview"', body)
        self.assertIn('id="mod-quick-setup"', body)
        self.assertIn('id="btn-quick-setup"', body)
        self.assertIn("一键拉取并检查", body)
        self.assertIn("一键上手", body)
        self.assertIn("傻瓜自检", body)
        self.assertIn("make serve-reader", body)
        self.assertIn("127.0.0.1:8000", body)
        self.assertIn('id="mod-data"', body)
        self.assertIn('id="mod-identity"', body)
        self.assertIn("模块导航", body)
        self.assertIn('class="module-title"', body)
        self.assertIn("module-boundary", body)
        self.assertIn("本组不做", body)
        self.assertIn("文档与真源", body)
        self.assertIn("数据源参考", body)
        self.assertIn("管道与闸门", body)
        self.assertIn("观测", body)
        self.assertIn("身份与账户", body)
        self.assertIn("ADMIN_WEB_CONSOLE_ROADMAP", body)
        self.assertIn('id="link-docs-quick-paths"', body)
        self.assertIn("docs/README.md#quick-paths", body)
        self.assertIn('id="link-docs-one-pager-architect"', body)
        self.assertIn("docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship", body)
        self.assertIn("架构师跨 PR 收束", body)
        self.assertIn('id="link-docs-ai-evolution"', body)
        self.assertIn("docs/README.md#ai-assisted-evolution", body)
        self.assertIn('id="link-agents-admin-console"', body)
        self.assertIn("AGENTS.md#agents-admin-console", body)
        self.assertIn('id="link-agents-pre-merge"', body)
        self.assertIn("AGENTS.md#agents-pre-merge", body)
        self.assertIn('id="link-docs-merge-pre-merge-nav"', body)
        self.assertIn("docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge", body)
        self.assertIn('id="link-docs-merge-pre-merge-partials-nav"', body)
        self.assertIn(
            "docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence", body
        )
        self.assertIn('id="link-docs-scripts-readme-sync-nav"', body)
        self.assertIn("scripts/README.md", body)
        self.assertIn('id="admin-main"', body)
        self.assertIn('aria-label="主内容"', body)
        self.assertIn('tabindex="-1"', body)
        self.assertIn('aria-controls="mod-overview"', body)
        self.assertIn('aria-controls="mod-identity"', body)
        self.assertIn('id="seg-filter"', body)
        self.assertIn("只读片段：点选后在下方探索器拉取", body)
        self.assertIn("当前请求路径与快捷操作", body)
        self.assertIn('th scope="col">run_id', body)
        self.assertIn('tbody th[scope="row"]', body)
        self.assertIn("button.btn:focus-visible", body)
        self.assertIn("a:focus-visible", body)
        self.assertIn("button.linkish:focus-visible", body)
        self.assertIn("button.btn-tiny:focus-visible", body)
        self.assertIn("在探索器打开片段", body)
        self.assertIn("在探索器加载快照历史 run", body)
        self.assertIn('id="repo-json-quick" role="toolbar"', body)
        self.assertIn("常用只读 JSON：在下方探索器打开", body)
        self.assertIn('aria-label="数据源目录：筛选与批量勾选"', body)
        self.assertIn("根据当前数据自动推断的观测提示", body)
        self.assertIn("全选 RSS：勾选带订阅 URL", body)
        self.assertIn("清空已勾选的数据源", body)
        self.assertIn("复制探索器正文（截断后的可见文本）", body)
        self.assertIn("用同一 URL 再请求一次探索器", body)
        self.assertIn("增大探索器正文可视高度", body)
        self.assertIn("敏感或宜受控，勿对公网裸暴露", body)
        self.assertIn("input:focus-visible", body)
        self.assertIn("关闭键盘快捷方式说明", body)
        self.assertIn("选择数据源 ", body)
        self.assertIn("复制工作流文件路径 ", body)
        self.assertIn('title="在新标签页打开"', body)
        self.assertIn("将已勾选且含订阅 URL 的数据源导出为 ingest 草案 JSON", body)
        self.assertIn("筛选片段", body)
        self.assertIn('id="btn-back-to-top"', body)
        self.assertIn("只读资源", body)
        self.assertIn('id="btn-explore-copy"', body)
        self.assertIn('id="btn-explore-replay"', body)
        self.assertIn("复制正文", body)
        self.assertIn("再拉一次", body)
        self.assertIn('id="explore-path"', body)
        self.assertIn('id="btn-explore-copy-url"', body)
        self.assertIn('id="btn-explore-toggle-height"', body)
        self.assertIn("复制 URL", body)
        self.assertIn("新标签打开", body)
        self.assertIn("加高正文", body)
        self.assertIn("当前分析快照", body)
        self.assertIn('id="snap-fail-wrap"', body)
        self.assertIn('id="btn-snap-fail-copy"', body)
        self.assertIn('aria-describedby="snap-fail"', body)
        self.assertIn("拉取失败时，错误说明旁有", body)
        self.assertIn('id="btn-hist-meta-copy"', body)
        self.assertIn("快照历史索引说明", body)
        self.assertIn("链接、命令与 Actions", body)
        self.assertIn("常用命令（本机执行）", body)
        self.assertIn("CI / Actions", body)
        self.assertIn("GitHub 工作流清单", body)
        self.assertIn("复制路径", body)
        self.assertIn("数据源参考目录", body)
        self.assertIn("admin-datasources", body)
        self.assertIn('id="ds-filter"', body)
        self.assertIn('id="ds-filter-hint"', body)
        self.assertIn("全选 RSS", body)
        self.assertIn("清空勾选", body)
        self.assertIn("常用 JSON（只读）", body)
        self.assertIn("repo-json-quick", body)
        self.assertIn("复制勾选 RSS 为 ingest 草案片段", body)
        self.assertIn("HTTPS JSON 侧车（json_feeds）", body)
        self.assertIn('id="btn-jf-copy"', body)
        self.assertIn('id="btn-jf-copy-full"', body)
        self.assertIn("mergeFullIngestConfigPreview", body)
        self.assertIn("_preview_comment", body)
        self.assertIn("admin_console_json_feeds_draft_v1", body)
        self.assertIn("ingestJsonFeedsIndex", body)
        self.assertIn("omitted_already_in_ingest", body)
        self.assertIn("ADMIN 阶段对表", body)
        self.assertIn("分析快照历史记录", body)
        self.assertIn("控制面能力路线图对照表", body)
        self.assertIn("GitHub Actions 工作流清单", body)
        self.assertIn('id="card-admin-accounts"', body)
        self.assertIn('id="admin-acct-manage-id"', body)
        self.assertIn('id="btn-admin-acct-patch"', body)
        self.assertIn("/api/admin/accounts", body)
        self.assertIn("syncAdminAccountsCard", body)

    def test_bootstrap_lists_proxy_segments(self) -> None:
        r = self.client.get("/api/bootstrap")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("server_time_beijing", data)
        self.assertRegex(
            str(data["server_time_beijing"]),
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$",
        )
        self.assertIn("admin_accounts_enabled", data)
        self.assertIsInstance(data["admin_accounts_enabled"], bool)
        segs = data["readonly_proxy_segments"]
        self.assertIn("snapshot", segs)
        self.assertIn("candidates", segs)
        self.assertIn("hint-decisions", segs)
        self.assertIn("ingest-config", segs)
        self.assertIn("ai-analysis-overlay", segs)
        self.assertIn("ai-overlay-step", segs)
        self.assertIn("hint-rules", segs)
        self.assertIn("maps-to-hints", segs)
        self.assertIn("registry", segs)
        self.assertIn("sediment", segs)
        self.assertIn("site-meta", segs)
        self.assertIn("site-search-index", segs)
        self.assertIn("snapshot-history", segs)

    def test_bootstrap_pipeline_links(self) -> None:
        r = self.client.get("/api/bootstrap")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("repo_web_base", data)
        links = data.get("pipeline_links")
        self.assertIsInstance(links, list)
        self.assertGreaterEqual(len(links), 10)
        paths = {x.get("path") for x in links if isinstance(x, dict)}
        self.assertIn("docs/ADMIN_WEB_CONSOLE_ROADMAP.md", paths)
        first = links[0]
        self.assertIn("label", first)
        self.assertIn("path", first)
        self.assertIn("href", first)
        hints = data.get("pipeline_cli_hints")
        self.assertIsInstance(hints, list)
        self.assertGreaterEqual(len(hints), 5)
        self.assertIn("github_actions_href", data)
        self.assertIsInstance(data.get("github_actions_href"), str)
        wfs = data.get("pipeline_workflows")
        self.assertIsInstance(wfs, list)
        self.assertEqual(len(wfs), 4)
        wf0 = wfs[0]
        for key in ("label", "trigger", "workflow_path", "blob_href", "actions_workflow_href"):
            self.assertIn(key, wf0)

    def test_bootstrap_data_source_catalog(self) -> None:
        r = self.client.get("/api/bootstrap")
        self.assertEqual(r.status_code, 200)
        cat = r.json().get("data_source_catalog")
        self.assertIsInstance(cat, dict)
        self.assertGreaterEqual(int(cat.get("schema_version", 0)), 1)
        self.assertIn("disclaimer_zh", cat)
        src = cat.get("sources")
        self.assertIsInstance(src, list)
        self.assertGreaterEqual(len(src), 8)
        cats = cat.get("categories")
        self.assertIsInstance(cats, list)
        self.assertGreaterEqual(len(cats), 3)
        fmc = cat.get("fetch_method_catalog")
        self.assertIsInstance(fmc, dict)
        methods = fmc.get("methods")
        self.assertIsInstance(methods, list)
        self.assertGreaterEqual(len(methods), 5)
        self.assertIn("title_zh", methods[0])

    def test_bootstrap_control_plane_roadmap(self) -> None:
        r = self.client.get("/api/bootstrap")
        self.assertEqual(r.status_code, 200)
        rp = r.json().get("control_plane_roadmap")
        self.assertIsInstance(rp, dict)
        self.assertGreaterEqual(int(rp.get("schema_version", 0)), 1)
        pillars = rp.get("pillars")
        self.assertIsInstance(pillars, list)
        self.assertGreaterEqual(len(pillars), 4)
        self.assertIn("label_zh", pillars[0])
        phases = rp.get("admin_phases")
        self.assertIsInstance(phases, list)
        self.assertGreaterEqual(len(phases), 4)

    def test_bootstrap_github_actions_href_from_blob_base(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "ADMIN_REPO_WEB_BASE": "https://github.com/acme/demo-repo/blob/develop",
            },
            clear=False,
        ):
            r = self.client.get("/api/bootstrap")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json().get("github_actions_href"),
            "https://github.com/acme/demo-repo/actions",
        )
        wfs = r.json().get("pipeline_workflows") or []
        ingest = next(x for x in wfs if "ingest-pipeline" in (x.get("workflow_path") or ""))
        self.assertEqual(
            ingest.get("blob_href"),
            "https://github.com/acme/demo-repo/blob/develop/.github/workflows/ingest-pipeline.yml",
        )
        self.assertEqual(
            ingest.get("actions_workflow_href"),
            "https://github.com/acme/demo-repo/actions/workflows/ingest-pipeline.yml",
        )

    def test_bootstrap_github_actions_href_empty_for_non_github(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "ADMIN_REPO_WEB_BASE": "https://gitlab.com/a/b/-/blob/main",
            },
            clear=False,
        ):
            r = self.client.get("/api/bootstrap")
        self.assertEqual(r.json().get("github_actions_href"), "")
        for wf in r.json().get("pipeline_workflows") or []:
            self.assertEqual(wf.get("actions_workflow_href"), "")

    def test_bootstrap_pipeline_links_no_href_when_base_empty(self) -> None:
        with mock.patch.dict(os.environ, {"ADMIN_REPO_WEB_BASE": ""}, clear=False):
            r = self.client.get("/api/bootstrap")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data.get("repo_web_base"), "")
        self.assertEqual(data.get("github_actions_href"), "")
        for item in data.get("pipeline_links") or []:
            self.assertEqual(item.get("href"), "")
        for wf in data.get("pipeline_workflows") or []:
            self.assertEqual(wf.get("blob_href"), "")
            self.assertEqual(wf.get("actions_workflow_href"), "")

    def test_me_anonymous(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"ADMIN_DEV_BYPASS": "", "ADMIN_DEV_USER_JSON": ""},
            clear=False,
        ):
            r = self.client.get("/api/me")
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.json()["authenticated"])

    def test_me_dev_bypass(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "ADMIN_DEV_BYPASS": "1",
                "ADMIN_DEV_USER_JSON": '{"sub":"dev","roles":["curator"]}',
            },
            clear=False,
        ):
            r = self.client.get("/api/me")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["authenticated"])
        self.assertEqual(r.json()["sub"], "dev")
        self.assertIn("curator", r.json()["roles"])

    def test_proxy_404_unknown_segment(self) -> None:
        r = self.client.get("/api/readonly/evil")
        self.assertEqual(r.status_code, 404)

    def test_proxy_503_without_base_url(self) -> None:
        with mock.patch.dict(os.environ, {"READONLY_API_BASE_URL": ""}, clear=False):
            r = self.client.get("/api/readonly/snapshot")
        self.assertEqual(r.status_code, 503)

    @mock.patch("app.main._shared_httpx_client")
    def test_proxy_site_search_index_whitelisted(self, get_client: mock.MagicMock) -> None:
        mock_resp = mock.Mock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"entries":[]}'
        mock_resp.headers = {"content-type": "application/json"}
        inst = mock.Mock()
        inst.get = mock.Mock(return_value=mock_resp)
        get_client.return_value = inst
        with mock.patch.dict(
            os.environ, {"READONLY_API_BASE_URL": "http://example"}, clear=False
        ):
            r = self.client.get("/api/readonly/site-search-index")
        self.assertEqual(r.status_code, 200)
        inst.get.assert_called_once()
        self.assertTrue(inst.get.call_args[0][0].endswith("/site-search-index"))

    @mock.patch("app.main._shared_httpx_client")
    def test_proxy_forwards_get(self, get_client: mock.MagicMock) -> None:
        mock_resp = mock.Mock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"ok":true}'
        mock_resp.headers = {"content-type": "application/json", "etag": '"abc"'}
        inst = mock.Mock()
        inst.get = mock.Mock(return_value=mock_resp)
        get_client.return_value = inst
        with mock.patch.dict(
            os.environ, {"READONLY_API_BASE_URL": "http://example"}, clear=False
        ):
            r = self.client.get("/api/readonly/snapshot")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"ok": True})
        inst.get.assert_called_once()
        call_kw = inst.get.call_args
        self.assertTrue(call_kw[0][0].endswith("/snapshot"))

    @mock.patch("app.main._shared_httpx_client")
    def test_proxy_forwards_if_none_match(self, get_client: mock.MagicMock) -> None:
        mock_resp = mock.Mock()
        mock_resp.status_code = 304
        mock_resp.content = b""
        mock_resp.headers = {"etag": '"t"'}
        inst = mock.Mock()
        inst.get = mock.Mock(return_value=mock_resp)
        get_client.return_value = inst
        with mock.patch.dict(
            os.environ, {"READONLY_API_BASE_URL": "http://example"}, clear=False
        ):
            r = self.client.get(
                "/api/readonly/snapshot", headers={"If-None-Match": '"abc"'}
            )
        self.assertEqual(r.status_code, 304)
        inst.get.assert_called_once()
        self.assertEqual(
            inst.get.call_args.kwargs.get("headers"),
            {"If-None-Match": '"abc"'},
        )

    @mock.patch("app.main._shared_httpx_client")
    def test_proxy_snapshot_history_forwards_query(
        self, get_client: mock.MagicMock
    ) -> None:
        mock_resp = mock.Mock()
        mock_resp.status_code = 200
        mock_resp.content = b"{}"
        mock_resp.headers = {"content-type": "application/json"}
        inst = mock.Mock()
        inst.get = mock.Mock(return_value=mock_resp)
        get_client.return_value = inst
        with mock.patch.dict(
            os.environ, {"READONLY_API_BASE_URL": "http://example"}, clear=False
        ):
            r = self.client.get("/api/readonly/snapshot-history?limit=5&offset=1")
        self.assertEqual(r.status_code, 200)
        inst.get.assert_called_once()
        called_url = inst.get.call_args[0][0]
        self.assertIn("limit=5", called_url)
        self.assertIn("offset=1", called_url)
        self.assertTrue(
            called_url.startswith("http://example/snapshot-history?")
            or "/snapshot-history?" in called_url
        )

    def test_proxy_snapshot_history_run_invalid_id(self) -> None:
        with mock.patch.dict(
            os.environ, {"READONLY_API_BASE_URL": "http://example"}, clear=False
        ):
            r = self.client.get("/api/readonly/snapshot-history/evil%20space")
        self.assertEqual(r.status_code, 404)

    @mock.patch("app.main._shared_httpx_client")
    def test_proxy_snapshot_history_run_ok(self, get_client: mock.MagicMock) -> None:
        mock_resp = mock.Mock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"run_id":"a"}'
        mock_resp.headers = {"content-type": "application/json"}
        inst = mock.Mock()
        inst.get = mock.Mock(return_value=mock_resp)
        get_client.return_value = inst
        with mock.patch.dict(
            os.environ, {"READONLY_API_BASE_URL": "http://example"}, clear=False
        ):
            r = self.client.get("/api/readonly/snapshot-history/run-2024-01")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"run_id": "a"})
        inst.get.assert_called_once_with(
            "http://example/snapshot-history/run-2024-01", headers={}
        )


if __name__ == "__main__":
    unittest.main()
