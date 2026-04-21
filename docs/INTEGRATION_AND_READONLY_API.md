# 只读 API 与对外集成

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**本文侧重**：**`readonly_api`** 只读路由、运行方式与对外集成；读者侧读数叙事见 [分析引擎](../analysis-hub.html)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)。

[`scripts/readonly_api.py`](../scripts/readonly_api.py) 从**磁盘已提交 JSON**（及可选本地 **`data/evolution.db`** 快照历史）提供 **HTTP 只读**访问：**不写** `evolution-manifest.json`、不改 HTML、不改任意仓库真源文件。与 [ARCHITECTURE · 七类模块](./ARCHITECTURE.md#seven-layers)、[DATA_CONTRACTS · 可选栈](./DATA_CONTRACTS.md)、[PLATFORM_EXTENSIBILITY · 只读出口](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#extension-slots) 一致。**路由 ↔ 路径 ↔ 敏感性**总表见 **[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)**。**ETag / If-None-Match** 纯逻辑在 **`evolution_pkg.ops.http_cache`**（无 FastAPI 依赖；单测 **`scripts/tests/test_http_cache.py`**），与 [INTELLIGENCE_SIX_DOMAINS · 代码侧](./INTELLIGENCE_SIX_DOMAINS.md#code-mapping) 运维域对表。**只读服务在仓库物理分层中的位置**及**主链验收入口**：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout) · **[§1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（**0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。**自动化助手（只读不写真源）**：[AGENTS.md · 人审闸门](../AGENTS.md#agents-invariants) · [架构边界](../AGENTS.md#agents-arch-boundary)。**呈现双轨（`spa-sync` / `spa-build`）**：[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map)。**MPA 顶栏与失页**：**`partials/`** → **`make sync-nav`**；**`404.html`** 手调（`sync_site_nav` 不写回）— **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

## 运行

仓库根目录（须 **`PYTHONPATH=scripts`**）：

```bash
python3 -m pip install -r requirements.txt -r requirements-api.txt
PYTHONPATH=scripts python3 -m uvicorn readonly_api:app --host 127.0.0.1 --port 8099
```

单测：**`make test-readonly-api`**（**`test_readonly*.py`**：**ETag / 304** + 管理端 **`READONLY_PROXY_SEGMENTS`** 对账；已含于 **`make merge-ready`**，见 **[MERGE_AND_RELEASE_CHECKLIST](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**）。

## 路由一览

（与 **[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)** 总表对读。）

| 路径 | 说明 |
|------|------|
| **`GET /health`** | 存活检查 |
| **`GET /snapshot`** | `assets/analysis-snapshot.json` |
| **`GET /ai-analysis-overlay`** | `assets/ai-analysis-overlay.json`（**可选**；无文件 **404**；契约 **`ai-analysis-overlay.schema.json`**） |
| **`GET /ai-overlay-step`** | `artifacts/ai-overlay-step.json`（侧车遥测；未跑管道则无文件 **404**；契约 **`ai-overlay-step.schema.json`**） |
| **`GET /trends`** | `assets/sediment-trends.json` |
| **`GET /manifest`** | `assets/evolution-manifest.json` |
| **`GET /site-meta`** | `assets/site-meta.json` |
| **`GET /site-search-index`** | `assets/site-search-index.json`（**可选**；**`make site-search-index`**；无文件 **404**；与 **`site-data-bus`** 顶栏轻量搜索同源） |
| **`GET /registry`** | `scripts/evolution-registry.json`（与 **SPA nav**、**`check_nav_links_registry`** 真源一致） |
| **`GET /sediment`** | `data/sediment.json`（沉淀；与 **`validate_sediment_artifacts_schema`** 一致；**无文件则 404**） |
| **`GET /candidates`** | `assets/evolution-candidates.json`（**待审候选**；与 **`validate-evolution-candidates`** 一致；**可能含未审线索**） |
| **`GET /hint-decisions`** | `assets/evolution-hint-decisions.json`（**规则闭环人审记录**；与 **`validate_evolution_hint_decisions`** 一致；**`rule_id`** 等） |
| **`GET /hint-rules`** | `scripts/evolution-hint-rules.json`（**分析提示规则**；与 **`check_manifest_drift`** / **`analysis_engine`** 真源一致） |
| **`GET /maps-to-hints`** | `scripts/maps_to_hints.json`（**ingest 用 host/关键词 → maps_to**；与 **`ingest_opinion_law`** / **`check_manifest_drift`** 一致） |
| **`GET /ingest-config`** | `scripts/ingest_config.json`（**RSS 源与 routes 配方**；与 **`ingest_opinion_law`** 一致；**含外网 URL**） |
| **`GET /snapshot-history`** | 快照历史**列表**（元数据 JSON；依赖本地 **`evolution.db`**） |
| **`GET /snapshot-history/{run_id}`** | 单条历史**全文**（**`Cache-Control: private, no-store`**） |

静态文件类响应带 **ETag**（SHA-256 前缀）与 **`Cache-Control: public, max-age=0, must-revalidate`**；请求头 **`If-None-Match`** 与当前 ETag 一致时返回 **304**（无正文）。细节以单测与源码为准。

**敏感路由**：**`GET /candidates`** 正文为**候选池**，可能含**尚未人审合并**的线索。**`GET /hint-decisions`** 含**人审决策**与 **`rule_id`** 等治理字段，**不宜**对匿名公网裸暴露。**`GET /ingest-config`** 列出**外网 RSS 与抓取策略**，或暴露运营侧重点，**宜受控暴露**。应用内**无**登录鉴权；若对公网或多方租户暴露，请在**网关**上做 **ACL / mTLS / 鉴权**，或**不**映射上述路径。与 **[SCRIPTS_APIS_AND_COMPONENTS_UPGRADE](./SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md)** §4 一致。对标**舆情类**集成形态时，**不因**「多源情报」需求默认放宽上述暴露面；侧车、overlay 与网关建议见 **[REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md)**。**舆情 / 制度 / 国情**的跟踪与反哺流程（含 ingest 侧，**非**本文件路由契约）：**[INTEL_AND_POLICY_TRACKING_PLAYBOOK.md](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)**（**[§2—2a · 拉取与暴露面](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b · 微博/站内流](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**）。

<a id="gateway-default-deny-sensitive"></a>

### 网关侧默认建议（公网或多方租户前暴露只读 API 时）

与上表「敏感路由」一致：**推荐默认**仅向匿名客户端映射 **`/health`**、**`/snapshot`**、**`/manifest`**、**`/registry`**、**`/site-meta`**、**`/trends`**、**`/sediment`**（按需）、**`/site-search-index`**（按需）、**`/hint-rules`**（按需）等「与已发布读者面强相关」的路径；**不**默认向公网开放 **`/candidates`**、**`/hint-decisions`**、**`/ingest-config`**、**`/maps-to-hints`**（待审线索、人审决策、外网 RSS 配方与 host 线索）。若业务必须开放，须在**反向代理或 API 网关**上单开 **ACL / mTLS / 鉴权** 与审计，并与 **[REFERENCE_DESIGN_OPINION_MONITORING](./REFERENCE_DESIGN_OPINION_MONITORING.md)** 对标。

<a id="extend-readonly-routes"></a>

## 扩展只读路由（复用 `evolution_pkg.ops.http_cache`）

新增 **GET**、正文为 **JSON**、且希望与现网一致的 **ETag + 304** 时：先在 **`evolution_pkg.readonly_disk_routes`** · **`READONLY_DISK_JSON_ROUTES`** 追加一行（磁盘真源），**`readonly_api`** 会在启动时注册；特判路径（非磁盘文件）仍手写 **`@app.get`**。缓存准备优先复用 **`evolution_pkg.ops.http_cache`**（**无 FastAPI 依赖**），响应封装为 **`Response` / `JSONResponse`**：

| 场景 | 使用的准备函数 | `Cache-Control` 语义 |
|------|----------------|----------------------|
| **磁盘已提交文件**（与 `/snapshot` 同类） | **`prepare_revalidated_json(bytes, if_none_match)`** | `public, max-age=0, must-revalidate` |
| **运行期组装的 dict/list**（与 `/snapshot-history` 同类） | **`prepare_dynamic_json(data, if_none_match, status_code=…)`** | `private, no-store`；仅 **status_code == 200** 时参与 **If-None-Match → 304** |

返回 **`PreparedJsonCache`**：`status_code`、**`body`**（304 时为 **`None`**）、**`headers`**（含 **`ETag`**）。路由内：若 **`body is None`** 则 **`Response(status_code=304, headers=prep.headers)`**；否则带 **`media_type="application/json; charset=utf-8"`** 与正文。

契约与单测：**`scripts/tests/test_http_cache.py`**（纯逻辑）；集成行为沿用 **`test_readonly_api.py`** 模式。**`scripts/tests/test_readonly_disk_routes.py`** 校验 **`evolution_pkg.readonly_disk_routes`** 元数据及 **OpenAPI** 注册。**`scripts/tests/test_readonly_proxy_segment_sync.py`** 将 **`readonly_api`** 的单段路径与 **`admin-console/app/settings.py`** · **`READONLY_PROXY_SEGMENTS`** 对账（**`/snapshot-history/{run_id}`** 仍由管理端**专用**路由代理）。上述 **`test_readonly*.py`** 的 **skip 条件** 与说明字符串共用 **`scripts/tests/readonly_test_util.py`**。合并前推荐 **`make merge-ready`**（或至少 **`make validate`** + **`make test-readonly-api`** + **`make test-admin-console`**）。**`admin-console`** 单页 UI 与 **`mod-*`** 对表见 **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**。

<a id="integration-openapi"></a>

## OpenAPI（机器可读契约）

应用为 **FastAPI**，默认提供：

- **`GET /openapi.json`** — OpenAPI 3 schema（**title / description / tags** 与 **[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)** 对读，便于集成方 onboarding）  
- **`GET /docs`** — Swagger UI（开发时联调）

**典型用法（不写网关即可起步）**：

1. 本地起服务（见上文「运行」）。  
2. 拉 schema：`curl -sS http://127.0.0.1:8099/openapi.json -o openapi-readonly.json`。  
3. 用 [openapi-generator](https://openapi-generator.tech/) 或 **httpx + pydantic** 手写薄客户端，**只**覆盖所需路径（`/snapshot`、`/registry` 等）；敏感路径默认勿对公网开放。

生产若关闭文档路由，请在反向代理或启动参数侧按需限制暴露面。

<a id="optional-reader-ops-enhancements"></a>

## 可选增强（搜索 · DuckDB 视图 · 管理端工程化）

与 **[PLATFORM_CAPABILITY_MAP](./PLATFORM_CAPABILITY_MAP.md)**（流水线遥测一行）及 **[DATA_CONTRACTS · §7](./DATA_CONTRACTS.md)** 对读；均为**可选**，不改变 **Git JSON 真源** 与 **`make validate`** 闸门。

| 方向 | 做法 | 注意 |
|------|------|------|
| **站内搜索** | 构建后对根目录 **`*.html`** 跑 **[Pagefind](https://pagefind.app/)**（`npx pagefind --site .`，排除 `admin-console` / `spa/dist` 等），在总线或页脚注入其静态脚本；或自建 **`assets/site-search-index.json`**（**`make site-search-index`** → **`scripts/gen_site_search_index.py`**），由 **`site-data-bus.js`** 在顶栏 **`[data-site-quick-search]`** 消费（**`make sync-nav`** 与 **`partials/site-nav.inc.html`** 对齐） | GitHub Pages **静态根** 下须保证 **search 资源与 HTML 同源**；勿把索引当契约 JSON。改 **`partials/skip-bar.inc.html`**（或影响失页顶栏）后 **`404.html`** 须**手调** — **[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** |
| **DuckDB 复盘** | 在 `scripts/` 旁维护 **`.sql` 视图文件**（只读查询），与 **`query_evolution_duckdb.py`** 对表；可选 CI job 在装 **`requirements-analytics.txt`** 时跑「结果集列名」断言 | 权威仍在 **Git 内 JSON**；SQL 仅为侧车分析 |
| **管理端拆包** | 单页过大时，用 **Vite + TS 多入口** 或极薄 React 壳承载表格/表单，**仍**经 **`readonly_api` + 现有 merge 闸门** 写操作；路线图见 **[ADMIN_WEB_CONSOLE_ROADMAP](./ADMIN_WEB_CONSOLE_ROADMAP.md)** · **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** | 单独里程碑 + **`make test-admin-console`** 迁移计划 |

## CORS、鉴权与部署

- 应用内**未**配置跨域 **CORS**、**未**内建登录鉴权；对外暴露时请在**网关 / 反向代理**上配置允许来源、TLS、mTLS 或内网 ACL。  
- **智能化集成**建议：下游只缓存 **GET**、尊重 **304**，并把 **`site_version`**（发布线）与 **`run_id`**（分析线）在自家仪表盘分开展示（见 [PLATFORM_CAPABILITY_MAP · 两条版本线](./PLATFORM_CAPABILITY_MAP.md#release-lines)）。

## 与「自动进化」的边界

只读 API **放大可读性与可观测性**，不改变**人审 merge manifest**、**artifact → 人工合并** 节奏；禁止用外部 job 经本 API **回写** 仓库 JSON（本服务亦无写接口）。

## Docker 部署

使用 **`Dockerfile.readonly-api`** 与 **`docker compose --profile api`** 与静态 **MPA** 同仓编排，见 **[DOCKER.md](./DOCKER.md#profile-api)**；生产环境请在网关终止 TLS 并限制暴露面。

**与脚本的边界**（哪些适合只读 HTTP、哪些必须保留 CLI/闸门）：**[SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](./SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md)**。

---

*路由或缓存策略变更时请同步本文、[DATA_CONTRACTS](./DATA_CONTRACTS.md)、**`evolution_pkg/ops/http_cache.py`** 与 **`readonly_api.py`** 模块文档字符串。*
