# 数据契约与主键（全站 JSON / 侧车）

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**本文侧重**：全站 **JSON / 侧车** 的职责、主键、校验入口与只读路由对表；**非**枢纽页 HTML/CSS 版式（见 [INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)）。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

本文是 [ARCHITECTURE.md](./ARCHITECTURE.md) 的**字段级索引**：各文件的职责、关联键、校验入口与可选分析栈。大改管道时请同步更新本节。在 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** 中，本节内容主要支撑**技术架构**里的**数据契约与侧车**（与 [ARCHITECTURE · 七类模块](./ARCHITECTURE.md#seven-layers) 之存储/沉淀/分析一致）。**Schema 文件列表与校验脚本对表**见 **[docs/schemas/README.md](./schemas/README.md)**；**扩展插槽与进化跑道**见 **[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**。**合并/发布动线**见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**；**整体内容框架**见 **[docs/README · #content-framework](./README.md#content-framework)**；**读者面 × 管理面按模块一页表**见 **[docs/README · #front-back-modules](./README.md#front-back-modules)**；**组件×功能一条表**见 **[docs/README · #system-components-fusion](./README.md#system-components-fusion)**；**全文档整理主线**见 **[docs/README.md · 文档主线](./README.md#docs-spine)**；**按改动判型最短链**（主线 **0c**）见 **[docs/README · #quick-paths](./README.md#quick-paths)** · **[MODULE · §1a 七类→包/脚本](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#seven-class-pkg-quick)**。**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · **主链联动与验收入口**见 **[PROJECT · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)**；**`assets/` 等 JSON 真源在仓库分层中的位置**见 **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**技术架构整理与分阶段升级（简版）**见 **[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)**。**用户端/管理端、数据源与审核分层（设计）**见 **[USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)**。**管理端管道 UI、ingest/分析编排与数据源自动拉取**见 **[ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)**。**方法论快照之上可选叠加 AI 解读与接入配置**见 **[AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md)**。**呈现双轨（`spa-sync` / `spa-build`）** 与维护者收束见 [README · 双轨真源](../README.md#readme-dual-track-map) · [关系视图](../maintainer-hub.html#mh-spine-map)。

**读者面 MPA 版式（非 JSON 字段）**：枢纽页 HTML/CSS 复用类见 **[INTELLIGENCE_SIX_DOMAINS · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**，不列入本节各文件表。

## 1. 单一注册表

| 文件 | 角色 | 关键字段 | 校验 |
|------|------|----------|------|
| `scripts/evolution-registry.json` | 允许出现在 `maps_to.pages` 的根 HTML；`lab_factors` 全集 | `pages[]`、`lab_factors[]` | 契约 [`docs/schemas/evolution-registry.schema.json`](schemas/evolution-registry.schema.json)、**`validate_evolution_registry_schema.py`**（**`make test`** / **`make validate`**）；语义对账 **`check_manifest_drift.py`**（**`make validate`** 等）；仓库内路径与 **`evolution_pkg.io.REGISTRY_JSON_PATH`** / **`REGISTRY_JSON_RELPOS`**（只读 **`GET /registry`**）一致 |

<a id="signals-candidates"></a>

## 2. 信号与候选

<a id="ingest-config-contract"></a>

| 文件 | 角色 | 关键字段 | 校验 |
|------|------|----------|------|
| `assets/evolution-manifest.json` | 已入库信号 | `signals[].id`、`maps_to.pages`、`maps_to.lab_factors`、`review_state`（正式条目中） | `validate-evolution-manifest.py` |
| `assets/evolution-candidates.json` | 待审候选 | `signals[].id`、`review_state`、`status` | `validate-evolution-candidates.py` |
| `scripts/maps_to_hints.json` | ingest 时按 host/关键词补 `maps_to` | 与 ingest 脚本约定 | `check_manifest_drift.py` |
| `scripts/ingest_config.json` | **ingest 管道**（**`ingest_opinion_law.py`** 薄 CLI → **`evolution_pkg.ingest_opinion_pool`**）配方：`rss_feeds`、`law_html_pages`、`routes`，以及可选 **`json_feeds`**（HTTPS JSON 侧车/API，解析见 **`evolution_pkg.ingest_json_http`**）；可选 **`fetch_pacing`**（**`after_rss_fetch`** / **`after_law_html_fetch`** / **`after_json_feed_fetch`** 秒数，默认 **0.8 / 1.0 / 0.8**，上限 **120**） | `require_route_match` | `check_manifest_drift.py`（`routes` 中 pages / lab_factors）；须 **https** URL；抓取频率与信源分层见 **[INTEL · §2—2a](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b 微博/站内流](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)** |
| `fixtures/ai_mapping_golden/*.json` | **规则层回归夹具**（非生产）：标题/摘要/可选链接经 **`apply_routes` + `merge_maps_to_hints`** 后的期望子集 | `cases[]`、`input`、`expect.*_contains` | [`docs/schemas/ai-mapping-golden.schema.json`](schemas/ai-mapping-golden.schema.json)、**`validate_golden_mapping.py --dir`**（**`run_validate.sh`**）；**expect** 白名单与 **`evolution_pkg.io.load_registry_allowed_sets()`**（即 **registry**）一致 |

**路径真源（防漂移）**：**`evolution_pkg.io`** 暴露 **`REGISTRY_JSON_PATH` / `REGISTRY_JSON_RELPOS`**、**`INGEST_CONFIG_JSON_*`**、**`MAPS_TO_HINTS_JSON_*`**；**`ingest_opinion_pool`**（经薄 **`ingest_opinion_law`**）、**`check_manifest_drift`**、**`validate_golden_mapping`**、**`evolution_pkg.readonly_disk_routes`** 等与之一致。

**关联键**：信号 `id`（字符串）在候选与 manifest 之间唯一标识同一条目；合并脚本以 `id` 为主键更新。

## 3. 规则与决策（闭环）

| 文件 | 角色 | 关键字段 | 校验 |
|------|------|----------|------|
| `scripts/evolution-hint-rules.json` | 分析引擎外置规则 | `rules[].id`、`track_closure` | `check_manifest_drift.py`（target_pages）、**`analysis_engine`** / **`evolution_pkg.analysis_pipeline`** |
| `assets/evolution-hint-decisions.json` | 人对提示的落实记录 | `decisions[].rule_id`、`action`（done/rejected/deferred） | `validate_evolution_hint_decisions.py` |

**关联键**：`rule_id` 必须 ∈ `evolution-hint-rules.json` 中的 `rules[].id`（若填写）。

## 4. 当日分析快照

| 文件 | 角色 | 关键字段 | 校验 |
|------|------|----------|------|
| `assets/analysis-snapshot.json` | 热力、共现、提示、闭环缺口 | `run.run_id`、`run.repo_revision`、`sources.*`、`module_heat`（`page`+`count`）、`factor_heat`（`factor`+`count`） | `validate_analysis_snapshot_schema.py`、**`analysis_engine.py --check`**（等价 **``-m evolution_pkg.analysis_pipeline --check``**） |

**契约**：[`docs/schemas/analysis-snapshot.schema.json`](schemas/analysis-snapshot.schema.json)。

**差分**：`python3 scripts/diff_analysis_snapshot.py <base.json> [head.json]` 或 `--git-base HEAD~1:assets/analysis-snapshot.json`。

### 4.1 可选：AI 辅助解读产物（规划）

在**不改变**上文快照 **Schema 必填域**的前提下，可另增**独立文件**承载「对快照/趋势的自然语言或结构化解读」，由**可配置**的外部模型服务生成；**不**替代 **`evolution_hints`** 与 manifest 人审语义。形状、管道挂载点、密钥与前台呈现约定见 **[AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md)**；配置示例见 **[docs/examples/ai_analysis_overlay.example.json](./examples/ai_analysis_overlay.example.json)**。若对标 **GitHub 等开源「舆情 / 热点 / 多源情报」** 产品而引入侧车或外呼，**仅作参考引用**时的契约落点与 manifest 边界见 **[REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md)**。

| 文件（建议名） | 角色 | 校验（落地时） |
|----------------|------|----------------|
| **`assets/ai-analysis-overlay.json`** | 与 **`run.run_id`** 对齐的 AI 解读；**可选**提交或仅内网发布 | [`docs/schemas/ai-analysis-overlay.schema.json`](schemas/ai-analysis-overlay.schema.json)、**`validate_ai_analysis_overlay_schema.py`**（**`evolution_pkg.ai_overlay_validate`**）；占位生成 **`scripts/write_ai_analysis_overlay_stub.py`** |

## 5. 按日沉淀与跨日趋势

| 文件 | 角色 | 关键字段 | 备注 |
|------|------|----------|------|
| `data/sediment.json` | 多日摘要条目 | `entries[].date`、`top_factors`、`top_pages`、`hint_closure_gaps_n` | 可与 SQLite 双写；见 **`analysis_engine.py --sediment`**（等价 **``-m evolution_pkg.analysis_pipeline --sediment``**）；契约 [`docs/schemas/sediment.schema.json`](schemas/sediment.schema.json)、**`validate_sediment_artifacts_schema.py`** |
| `data/evolution.db` | SQLite 侧车（默认忽略提交） | **`sediment_entry`**（与 `sediment.json` 双写）、**`analysis_snapshot_history`**（按 `run_id` 追加整份快照 JSON） | `.gitignore`；**`sqlite_store.py`**、**`list_analysis_snapshot_history.py`** |
| `assets/sediment-trends.json` | 因子/页面持久度、长期 hints | `factor_persistence`、`page_persistence`、`closure_backlog` | `sediment_trends.py`；契约 [`docs/schemas/sediment-trends.schema.json`](schemas/sediment-trends.schema.json)、**`validate_sediment_artifacts_schema.py`** |

**全站 SPA 顶栏**：**`spa/nav.config.json`**（`schema_version`、`items[].page` / `label`）契约见 [`docs/schemas/spa-nav-config.schema.json`](schemas/spa-nav-config.schema.json)；**`items[].page`** 集合须与 **`scripts/evolution-registry.json`** 的 **`pages`** 一致。校验：**`check_nav_links_registry.py`**（**`evolution_pkg.spa_nav`**，已并入 **`make validate`** 与 **`make test`**）。

### 存储策略：哪些适合写入数据库（与架构预期对齐）

与 **[ARCHITECTURE.md](./ARCHITECTURE.md)**「数据存储 / 沉淀 / 闸门」一致：**可版本化、可校验、需人审或 CI 对账的结构化事实以 Git 内 JSON 为真源**；**SQLite 仅作侧车**（查询加速、本地分析），**不**取代校验与 PR 流程。

| 数据 | 推荐主载体 | 是否写入 `evolution.db`（或他库） | 说明 |
|------|------------|-------------------------------------|------|
| 按日沉淀摘要 | **`data/sediment.json`** | **是（已支持）**：表 **`sediment_entry`** 与 JSON **双写** | 真源仍以**已提交** JSON + Schema 为准；库可 `.gitignore`，见 **`scripts/sqlite_store.py`** |
| 跨日趋势产物 | **`assets/sediment-trends.json`** | **否（默认）** | 体量小、随静态站发布；由 **`sediment_trends.py`** 从 JSON/SQLite **读**、写回 JSON |
| 注册表 / 信号 / 候选 / 规则 / 人审决策 | **`evolution-registry.json`**、**`assets/evolution-manifest.json`**、**`assets/evolution-candidates.json`**、**`scripts/evolution-hint-rules.json`**、**`assets/evolution-hint-decisions.json`** | **否作为主存储** | 需 **Diff、validate、人审闸门**；**勿**以 DB 为唯一真源或自动写 manifest（见根目录 **[AGENTS.md · 人审闸门](../AGENTS.md#agents-invariants)**） |
| 当日分析快照（提交态） | **`assets/analysis-snapshot.json`** | **否（闸门仍以文件为准）** | **`validate_analysis_snapshot_schema.py`**、**`analysis_engine --check`**（等价 **``-m evolution_pkg.analysis_pipeline --check``**） |
| 当日分析快照（本地只读历史） | — | **是（已落地）**：表 **`analysis_snapshot_history`** | **`analysis_engine.py`** / **`analysis_pipeline`** 写快照后默认追加一行；**`--no-sqlite-snapshot-history`** 关闭；`run_id` 重复则忽略；**不**替代 Git 内 HEAD 快照 |
| ingest 原始行、流水线审计 | 可选：追加表 | **可（扩展）** | 宜**可重建**；权威合并结果仍在候选 / manifest JSON 与人审流 |
| 站点发布线、SPA 顶栏文案 | **`assets/site-meta.json`**、**`spa/nav.config.json`** | **否** | 与静态站发布链一致，保持 JSON + 生成物 |
| 叙事正文 | 根目录 **`.html`** | **否** | **分析管道**（**`analysis_engine`** / **`analysis_pipeline`**）不写 HTML；正文不进库作为主形态 |
| 流水线遥测 | **`artifacts/pipeline-metrics-*.json`** | **否** | 见下文 §7，不入业务库 |

**小结（更符合当前预期的取舍）**：SQLite 侧车现为 **`sediment_entry`** + **`analysis_snapshot_history`**（均为**可丢可重建**的加速/历史层，真源仍在 Git JSON）；**信号库、注册表、规则与决策**保持 **JSON 真源**；ingest 原始行等可再 **追加**表，**勿**将 manifest 或闸门状态迁库为主。

<a id="sqlite-sidecar-column-inventory"></a>

#### SQLite 侧车：表与列速查（与 `sqlite_store.py` 一致）

便于评审「已进库字段数量」；**语义真源**仍以前表「推荐主载体」列为准。

| 表 | 列数 | 列名 |
|----|------|------|
| **`sediment_entry`** | **10** | `date`（PK）, `manifest_n`, `candidate_n`, `top_factors_json`, `top_pages_json`, `hint_closure_gaps_n`, `hint_decisions_total`, `run_id`, `repo_revision`, `updated_at` |
| **`analysis_snapshot_history`** | **5** | `run_id`（PK）, `repo_revision`, `generated_at`, `snapshot_json`（整包快照 JSON 文本）, `stored_at` |

**说明**：`snapshot_json` 在契约上视为 **1 列**；其内部字段仍以 **`analysis-snapshot`** Schema 为准，**不**在本文逐列展开。

**时间戳**：新写入的 `generated_at`、`stored_at`、`sediment_entry.updated_at` 等为 ISO8601 **北京时间**（IANA `Asia/Shanghai`，`+08:00`）；历史行或旧 artifact 中可能仍为 UTC「`Z`」。

#### 不宜以数据库为「唯一真源」的契约域（类数）

下列 **8 类**须保持 **Git 内 JSON/HTML 为主载体**（与上表及 **[AGENTS.md · 人审闸门](../AGENTS.md#agents-invariants)**、**[架构边界](../AGENTS.md#agents-arch-boundary)** 一致），**不**建议整体迁入 OLTP 替代 PR/validate 闸门：**`evolution-registry.json`**、**`evolution-manifest.json`**、**`evolution-candidates.json`**、**`evolution-hint-rules.json`**、**`evolution-hint-decisions.json`**、**`analysis-snapshot.json`（HEAD）**、**`sediment-trends.json`**、**`site-meta` / `nav.config` + 根目录 `.html` 叙事**。

#### 后续引入服务器级库时，相对符合预期的记录类型

与 **[DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)** 对读：**ingest 原始行或抓取审计**（可重建、与候选/manifest 人审分离）、**流水线 / Job 元数据**（`run_id`、`git_sha`、状态、artifact 指针）、**幂等游标**、**管理端会话与审计日志**（`actor_sub`、`action`、`correlation_id`、关联 PR/run）、**只读 API 读副本/物化投影**（由已提交 JSON 重算）。**仍勿**将 **manifest** 或 **review_state** 的权威副本只放在库内而无 Git 对账。

**运维**：本地 **`evolution.db`** 可随体积删除后重跑分析以重建；列表见 **`list_analysis_snapshot_history.py`** / **`readonly_api`** · **`/snapshot-history`**。详见 **[EVOLUTION_RUNBOOK.md · 本地 SQLite 与快照历史](./EVOLUTION_RUNBOOK.md#sqlite-sidecar)**。

**服务器级数据库、缓存、数仓与 Kafka CDC** 等后续整体设计与落地顺序，见 **[DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)**（与本文互补：本文管**当前**仓库内契约与侧车；该文管**可选扩展**拓扑）。

## 6. 站点发布版本（静态元数据）

| 文件 | 角色 | 关键字段 |
|------|------|----------|
| `assets/site-meta.json` | **人为维护**的发布线版本（与 `analysis-snapshot.run` 无关） | `schema_version`、`site_version`、`codename`、`summary`、`updated` |

顶栏通过 **`[data-site-meta-version]`** 由 `site-data-bus.js` 拉取并显示为 `v1.x.x`。大功能合并或对外宣告时可递增 `site_version` 并更新 `summary`。

<a id="pipeline-telemetry"></a>

## 7. 流水线遥测（不入库）

| 文件 | 角色 | 关键字段 |
|------|------|----------|
| `artifacts/pipeline-metrics-*.json` | `make analyze` / `evolution-fast` 每步耗时与退出码 | `pipeline`、`telemetry_run_id`、`success`、`failed_step`；**`input_artifacts`**：流水线开始时主输入 JSON（如 **`manifest`** / **`candidates`** / **`hint_rules`** / **`ingest_config`** 等）的 **`relpath`**、**`sha256`**（整文件）、**`bytes`** 或 **`missing`**；**OTel 提示**：`otel_semantics`、`steps[].otel_span_name`（建议 span 名 `evolution.pipeline.<pipeline>.<step_id>`）；**`steps[]`**：`id`、`duration_ms`、`exit_code`、`argv`；**`ai_overlay_step`**（可选）：若本轮 **`write_ai_analysis_overlay`** 写了侧车 **`artifacts/ai-overlay-step.json`**，编排器在落盘遥测时并入（**`mode`** / **`usage`** / **`dead_letter_relpath`** 等） |
| `artifacts/ai-overlay-step.json` | AI 解读层单步元数据（不入业务 manifest） | 形状见 [`docs/schemas/ai-overlay-step.schema.json`](schemas/ai-overlay-step.schema.json)；LLM 失败时可追加 **`artifacts/ai-overlay-llm-dead-letter.txt`**（滚动摘要，**gitignore**） |

契约：[`docs/schemas/pipeline-metrics.schema.json`](schemas/pipeline-metrics.schema.json)；样例：**`fixtures/pipeline_metrics_example.json`**；校验：**`validate_pipeline_metrics_schema.py`**（**`make validate`**；对 **`artifacts/pipeline-metrics-*.json`** 仅当同时含 **`input_artifacts`** 与 **`otel_semantics`** 才按 Schema 校验，缺者视为旧格式并**跳过**）。**`artifacts/ai-overlay-step.json`** 另由 **`validate_ai_overlay_step_schema.py`** 校验（无文件则跳过；形状见 [`ai-overlay-step.schema.json`](schemas/ai-overlay-step.schema.json)）。清理旧遥测：可先 **`make clean-pipeline-metrics-dry-run`** 列路径，再 **`make clean-pipeline-metrics`**（见 **[EVOLUTION_RUNBOOK · 加速](./EVOLUTION_RUNBOOK.md#accelerate)**）；侧车与 dead-letter 亦可 **`make clean-overlay-artifacts`**。生成：`python3 scripts/run_pipeline_steps.py`（由 `run_update_pipeline.sh` / `run_analyze_write.sh` 调用）；每轮流水线**开始**会删除上一轮的 **`ai-overlay-step.json`**，避免误并入。关闭：`SKIP_PIPELINE_TELEMETRY=1`。采集器可将每步映射为子 span，**不必**为此引入编排器。

## 8. 可选分析栈（本地）

不进入默认 `requirements.txt`，避免 CI 与轻量环境膨胀。

| 依赖文件 | 用途 |
|----------|------|
| [`requirements-analytics.txt`](../requirements-analytics.txt) | DuckDB / Polars：对 `evolution.db` 或导出数据做 SQL / DataFrame |
| [`requirements-api.txt`](../requirements-api.txt) | FastAPI：只读暴露 `analysis-snapshot.json` 等（本地或内网） |

- **DuckDB 示例**：`python3 scripts/query_evolution_duckdb.py`（需 `pip install -r requirements-analytics.txt`）。
- **只读 API**：`pip install -r requirements-api.txt`；运行与扩展见 **[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)**。路由与磁盘路径、敏感性总表见下 **§8.1**。

<a id="readonly-api-routes"></a>

### 8.1 只读 HTTP 路由总表（`readonly_api`）

与 **`scripts/readonly_api.py`**、**`evolution_pkg.readonly_disk_routes`**（磁盘 **GET** 真源）及单测 **`test_readonly_api.py`**、**`test_readonly_disk_routes.py`**、**`test_readonly_proxy_segment_sync.py`**（**`readonly_api`** 单段路径 ↔ **`admin-console`** **`READONLY_PROXY_SEGMENTS`**）对齐；**OpenAPI** 见 **`GET /openapi.json`**。磁盘类路由使用 **`prepare_revalidated_json`**（**`public, max-age=0, must-revalidate`** + **ETag** → **304**）；动态历史使用 **`prepare_dynamic_json`**（**`no-store`** 等，见 **[INTEGRATION · 扩展只读路由](./INTEGRATION_AND_READONLY_API.md#extend-readonly-routes)**）。对公网或多方租户暴露时的**网关默认建议**（哪些路径宜映射、哪些宜默认不映射）见 **[INTEGRATION · 网关建议](./INTEGRATION_AND_READONLY_API.md#gateway-default-deny-sensitive)**。

| **`GET` 路径** | **真源**（相对仓库根，除非注明） | **无文件 / 无数据** | **暴露面建议** |
|----------------|----------------------------------|---------------------|----------------|
| **`/health`** | 合成 **`{"status":"ok"}`** | — | 低 |
| **`/snapshot`** | `assets/analysis-snapshot.json` | 404 | 低 |
| **`/ai-analysis-overlay`** | `assets/ai-analysis-overlay.json` | 404 | **中**：可能含模型生成文案；**宜标注非审计结论**；契约见 **§4.1**、**`ai-analysis-overlay.schema.json`** |
| **`/ai-overlay-step`** | `artifacts/ai-overlay-step.json` | 404 | **低**：单步遥测（模式、耗时、可选 ``usage``/``otel_hints``）；未跑管道则无文件 |
| **`/trends`** | `assets/sediment-trends.json` | 404 | 低 |
| **`/manifest`** | `assets/evolution-manifest.json` | 404 | 低（已审信号；仍**只读**） |
| **`/site-meta`** | `assets/site-meta.json` | 404 | 低 |
| **`/site-search-index`** | `assets/site-search-index.json` | 404 | 低；**可选**（**`make site-search-index`**）；**非**分析快照契约 |
| **`/registry`** | `scripts/evolution-registry.json` | 404 | 低 |
| **`/sediment`** | `data/sediment.json` | 404 | 低；容器/部署须挂载 **`data/`** 若需此路由 |
| **`/candidates`** | `assets/evolution-candidates.json` | 404 | **高**：**未审候选**；**须网关 ACL/鉴权或不映射**，见 **[INTEGRATION](./INTEGRATION_AND_READONLY_API.md)** |
| **`/hint-decisions`** | `assets/evolution-hint-decisions.json` | 404 | **中**：人审闭环记录；**宜内网或受控暴露** |
| **`/hint-rules`** | `scripts/evolution-hint-rules.json` | 404 | **低**：规则配置；仍随仓库版本发布 |
| **`/maps-to-hints`** | `scripts/maps_to_hints.json` | 404 | **低**：ingest 映射；或含 host 线索，**大规模公网暴露前**可自查内容 |
| **`/ingest-config`** | `scripts/ingest_config.json` | 404 | **中**：**RSS / 可选 json_feeds URL** 与 ``routes`` 配方；**宜受控暴露** |
| **`/snapshot-history`** | **`data/evolution.db`** 表 **`analysis_snapshot_history`** 元数据组装 | 可 **200** 且 `total=0` | 中；仅内网或受控暴露 |
| **`/snapshot-history/{run_id}`** | 同上表全文 JSON | **404** | 中；**`no-store`** |

**管理端同源代理**：**`GET /api/readonly/{segment}`** 白名单与 **`readonly_api`** 单段路径对齐（含 **`ai-analysis-overlay`**、**`ai-overlay-step`**、**`candidates`**、**`hint-decisions`**、**`hint-rules`**、**`ingest-config`**、**`maps-to-hints`**、**`sediment`**、**`site-search-index`** 等），见 **`admin-console/app/settings.py`**。

## 9. Python 包布局（架构升级）

- **`scripts/evolution_pkg/`**：`io`（仓库根、`load_json`）、`pipeline`（analyze / fast 编排与遥测）、**`ingest_json_http`**（ingest 用 HTTPS JSON 条目解析）。
- **`scripts/evolution_io.py`**：兼容层，等价于 `from evolution_pkg.io import …`。

## 10. 相关文档

- **CI 与契约闸门**：**`make validate`** = **`scripts/run_validate.sh`**（含 **`validate_evolution_registry_schema.py`**、**`check_nav_links_registry.py`**、**`validate_sediment_artifacts_schema.py`** 等）；**`make test`** 含上述三项中的 registry / navLinks / 沉淀·趋势 Schema 与单测，**不**含对账、顶栏、**`analysis_engine --check`**（**`make validate`** 含此项，与 **``-m evolution_pkg.analysis_pipeline --check``** 等价）。**`make validate-fast`** 介于 **`make test`** 与全量之间（**已含** **`validate_ai_overlay_step_schema`** / **`validate_ai_analysis_overlay_schema`** 等，无文件则跳过），**不**入 CI/pre-commit（**[ARCHITECTURE#run-validate-gate](./ARCHITECTURE.md#run-validate-gate)**）。**`ci.yml` · spa-build** 按路径跑 **`make spa-build`**，不替代上述 JSON/MPA 闸门。摘要：[docs/README 文首](./README.md)、[PLATFORM_CAPABILITY_MAP §4](./PLATFORM_CAPABILITY_MAP.md#ops-tooling)。
- 平台能力总览（双轨呈现、阅读顺序、自检清单）：[PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md)
- 数据流总图：[ARCHITECTURE.md](./ARCHITECTURE.md)
- 技术栈与功能地图：[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md · 附录](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)（[别名](./TECH_ARCHITECTURE_CAPABILITIES.md)）
- 全站读数总线：[SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md)
