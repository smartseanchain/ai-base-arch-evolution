# 管理端 Web 控制台

与 **[ADMIN_WEB_CONSOLE_ROADMAP.md](../docs/ADMIN_WEB_CONSOLE_ROADMAP.md)** 配套的 **FastAPI** 服务：**不写 manifest**、不提供写 JSON 接口；**`GET /api/readonly/*`** 经白名单代理到 **`readonly_api`**（进程内 **`httpx.Client`** 连接池，超时 30s）。

**四条动线（读者 / 贡献 / 数据 / 部署）**：[README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理（五步）**：[ARCHITECTURE_ONE_PAGER · #architect-stewardship](../docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship)。

**框架与边界（评审）**：[ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md) · [§11a 文档索引](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-doc-index)。**在仓库里的位置 / 主链验证**：[PROJECT_ARCHITECTURE_OVERVIEW · 粒度](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain) · [§1b 物理布局](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout) · [§1a](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)。**整体内容框架 / 前后台一页表 / 组件×功能一条表**：[docs/README · #content-framework](../docs/README.md#content-framework) · [#front-back-modules](../docs/README.md#front-back-modules) · [#system-components-fusion](../docs/README.md#system-components-fusion)。**改动判型（0c）**：[docs/README · #quick-paths](../docs/README.md#quick-paths)。**读者 MPA 维护枢纽**：[维护导读](../maintainer-hub.html) · [关系视图](../maintainer-hub.html#mh-spine-map)（本页 ↔ 注册表 ↔ 文档锚点）· [系统边界](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)。**读者面 ↔ 管理面衔接矩阵 / 场景对表**：[PLATFORM_MASTER_MAP · 衔接矩阵](../docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-contract-matrix) · [场景×面](../docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-scenarios)。**管道与合并命令真源**仍见 **[scripts/README](../scripts/README.md)**；**[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** · **[PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)** · **[动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)**。**AI 与自动进化**：[docs/README · #ai-assisted-evolution](../docs/README.md#ai-assisted-evolution)。**自动化助手**：[AGENTS · 管理端壳](../AGENTS.md#agents-admin-console) · [人审闸门](../AGENTS.md#agents-invariants) · [框架判型](../AGENTS.md#agents-content-framework)。

**`GET /`**：单页控制台（无前端构建链），模块顺序见 [ADMIN_CONSOLE · §7](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)；**`#mod-api`** 旧锚点滚动到 **观测**。

**页内要点**：

- **读者站顶栏（仓库根 MPA）**：与 **`admin-console`** 分轨；改 **`partials/site-nav.inc.html`** / **`partials/skip-bar.inc.html`** 后 **`make sync-nav`**（**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 生成，勿手改 HTML）；**`404.html`** 顶栏/skip **不在** **`sync_site_nav`** 写回范围，须**手调** — **[MERGE · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[scripts/README](../scripts/README.md)**。
- **数据源目录**：勾选存 **localStorage**；可与 **ingest-config** 对账标「在 ingest」；可复制 **RSS / json_feeds** 草案，手工合并进 **`scripts/ingest_config.json`** 后 **PR**，以 **`make validate`** 为准。与「舆情 / 制度 / 国情」跟踪流程对读：**[INTEL_AND_POLICY_TRACKING_PLAYBOOK.md](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)**（**[§2—2a 拉取约束](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b 微博/站内流](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**）。
- **只读探索器 / 快捷条**：白名单含 **`site-search-index`**（页题轻量索引；仓库根 **`make site-search-index`** 后 **`readonly_api`** 与 **`/api/readonly/site-search-index`** 可 **200**，否则 **404**）。与 **[DATA_CONTRACTS · §8.1](../docs/DATA_CONTRACTS.md#readonly-api-routes)** 对读。
- **控制面路线图**：来自 **`admin-console/data/control_plane_roadmap.json`**，只读叙事，无写接口。

## 能力一览

与 **[ADMIN_CONSOLE_FRAMEWORK_OVERVIEW · §4 HTTP 面](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-http-surface)** 对读（文档为速览，本 README 为日常操作真源）。

| 路径 | 作用 |
|------|------|
| **`GET /`** | 控制台（拉 **`/api/bootstrap`**、**`/api/me`**、**`/api/readonly/*`**） |
| **`GET /health`** | 存活与配置摘要 |
| **`GET /api/me`** | 身份占位；生产接 IdP 前可为匿名 |
| **`GET /api/bootstrap`** | 引导 JSON：只读基址、代理片段、**`pipeline_*`**、**`data_source_catalog`**、**`control_plane_roadmap`**、**`admin_accounts_enabled`** 等（**不**请求外网、**不**写 manifest） |
| **`GET/POST/PATCH/DELETE /api/admin/accounts`** | 管理员账户（JSON + bcrypt）。须 **`ADMIN_ACCOUNTS_API_SECRET`**；头 **`X-Admin-Accounts-Secret`** 或 **`Authorization: Bearer …`**。未配密钥 **503** |
| **`GET /api/readonly/{segment}`** | 受控 GET 代理 → **`READONLY_API_BASE_URL/{segment}`**（白名单与 **`readonly_api`** 一致）；**`snapshot-history`** 转发 **`limit`/`offset`** |
| **`GET /api/readonly/snapshot-history/{run_id}`** | 单条历史；**`run_id`** 仅 `[A-Za-z0-9._-]` |
| **`GET /docs`** · **`/openapi.json`** | OpenAPI |

## 环境变量

| 变量 | 说明 |
|------|------|
| **`READONLY_API_BASE_URL`** | compose 默认常指向 **`http://readonly-api:8099`**；本机 **`uvicorn`** 可设 **`http://127.0.0.1:8099`**；空则代理 **503** |
| **`ADMIN_CORS_ORIGINS`** | 逗号分隔来源；空则不加 CORS |
| **`ADMIN_DEV_BYPASS`** | `1`/`true`/`yes` 启用演示用户（**仅本地/内网**） |
| **`ADMIN_DEV_USER_JSON`** | 与 bypass 联用，合并进 **`/api/me`** |
| **`ADMIN_REPO_WEB_BASE`** | 托管 **blob** 前缀（可无尾斜杠），用于 **`pipeline_links[].href`**。未设时默认上游 **`smartseanchain/ai-base-arch-evolution`** 的 **`main`**。**显式置空**则 **`href`** 为空（无出站外链） |
| **`ADMIN_ACCOUNTS_API_SECRET`** | 非空启用账户 API；勿入库；勿与 bypass 混作生产认证 |
| **`ADMIN_ACCOUNTS_FILE`** | 账户文件路径；默认 **`data/admin_accounts.json`** |

**安全**：生产勿开 **`ADMIN_DEV_BYPASS`**。对外请 **TLS + 网络策略**，并规划 **OIDC**（见路线图）。

**审计**：账户变更写 logger **`admin_console.admin_accounts`** 单行 JSON（无密码/密钥）。

**Docker**：只读 503 且 health 正常时，查 shell 是否空导出覆盖了 compose，见 **[DOCKER.md §9](../docs/DOCKER.md#troubleshoot-admin-readonly)**；可用 **`make docker-up-stack`**。

## 本地运行（不依赖 Docker）

读者站：根目录 **`make serve-reader`** → **http://127.0.0.1:8000/**，或 compose **8765**（**[DOCKER.md](../docs/DOCKER.md)**）。勿用 **`file://`** 打开 HTML。

管理端（本目录）：

```bash
python3 -m venv .venv-admin && . .venv-admin/bin/activate
pip install -r admin-console/requirements.txt
cd admin-console && PYTHONPATH=. uvicorn app.main:app --reload --port 8100
```

可选（同机调试只读 API）：

```bash
export READONLY_API_BASE_URL=http://127.0.0.1:8099
# 另开终端：PYTHONPATH=scripts python3 -m uvicorn readonly_api:app --port 8099
```

浏览器：<http://127.0.0.1:8100/> · <http://127.0.0.1:8100/health> · <http://127.0.0.1:8100/docs>

## 单测

```bash
make test-admin-console
```

烟测与 **`static/index.html`** 对表：[ADMIN_CONSOLE · §7](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)。

## Docker Compose（profile `admin`）

```bash
docker compose --profile admin up -d --build
```

默认 **8100**。与只读 API 同栈：

```bash
export READONLY_API_BASE_URL=http://readonly-api:8099
docker compose --profile api --profile admin up -d --build
```

**`make docker-up-admin`**；说明：[DOCKER.md#profile-admin](../docs/DOCKER.md#profile-admin)。

## 校验

根目录 **`make validate`** 对 **`admin-console/app`** 跑 **`compileall`**（语法闸门）。
