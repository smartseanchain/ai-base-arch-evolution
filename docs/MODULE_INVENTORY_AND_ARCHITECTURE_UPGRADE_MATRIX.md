# 模块全量梳理与架构升级矩阵

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

本文在 **[ARCHITECTURE.md · 七类能力](./ARCHITECTURE.md#seven-layers)**、**[scripts/README.md · 脚本分类](../scripts/README.md#scripts-by-role)**、**`evolution_pkg.domains`**（**[INTELLIGENCE_SIX_DOMAINS · 代码映射](./INTELLIGENCE_SIX_DOMAINS.md#code-mapping)**）之上，做**模块级充分梳理**，并给出与 **[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md)** **阶段 0—3** 对齐的**升级落点**（先做哪、何时不必跳级）。

**调用顺序**（合并 / 增能）：**[PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)**。**按阶段升级打勾与验收**：[PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)。**可执行改造全景与分阶段执行卡**仍以 **[ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)** 为准。

**目录**：[1. 七类能力→模块](#seven-to-modules) · [1a. 七类→包/脚本速查](#seven-class-pkg-quick) · [2. `evolution_pkg`](#evolution-pkg) · [3. `scripts/` 簇](#scripts-cluster) · [4. 呈现与管理端](#front-admin-spa) · [5. 升级矩阵](#upgrade-matrix) · [6. 推荐顺序](#sequence) · [7. 反模式](#anti) · [8. 延伸阅读](#reading)。**可复制命令表**：[PHASED · 落地执行](./PHASED_UPGRADE_EXECUTION_GUIDE.md#execution-now)。**主链联动与验证 · 仓库物理分层**：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（主线 **0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。**SPA / 注册 / 枢纽收束**：[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map) · [系统边界](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)。**自动化助手（人审 · 双轨 · 合并前）**：[AGENTS.md · 人审闸门](../AGENTS.md#agents-invariants) · [MPA+SPA 双轨](../AGENTS.md#agents-dual-track) · [合并前](../AGENTS.md#agents-pre-merge)。

---

<a id="seven-to-modules"></a>

## 1. 七类能力 → 仓库模块（全量对表）

| 七类能力 | 主要载体 | 闸门 / 校验（摘要） | 升级时优先动作（阶段 1） |
|----------|----------|---------------------|---------------------------|
| **数据存储** | `assets/*.json`、`data/sediment.json`、`data/evolution.db` | `validate-*`、**`DATA_CONTRACTS`** | 新字段先 **Schema** + **`run_validate.sh`**；侧车仍**可重建** |
| **沉淀** | `analysis_engine --sediment`、`sqlite_store`、`sediment.json` | **`validate_sediment_artifacts_schema.py`** | 与消费者（趋势、Hub）同步；**`schema_version`** |
| **分析** | `analysis_engine.py`、`evolution-hint-rules.json`、快照 | **`analysis_engine --check`**、**`validate_analysis_snapshot_schema.py`** | 规则外置、块级扩展；**不写 HTML** |
| **内容生成** | 根目录 **`*.html`**、`ingest` → 候选 JSON | 人写叙事；ingest **不写 manifest** | 新线索走 **ingest_config** + 候选校验；模型插槽见 **draft** |
| **进化** | `merge_candidates_to_manifest`、`review_state`、决策 JSON | 人审；**`validate_evolution_hint_decisions.py`** | **禁止**自动 merge；PR 引用 **rule_id** |
| **汇总** | 当日快照、**`sediment_trends.py`**、**`gen-sitemap.py`** | 趋势 Schema；drift 含 sitemap | 与快照生成器**解耦**维护 |
| **展示** | **MPA** `*.html` + **`site-data-bus.js`** 等；**SPA** `spa/` | **`sync_site_nav --check`**、**`check_nav_links_registry`**、**`check_skip_bar_404`** | 新占位登记 **SITE_DATA_UPDATE_FRAMEWORK**；SPA **nav ≡ registry**；**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 生成（勿手改 HTML） |

<a id="seven-class-pkg-quick"></a>

### 1a. 七类能力 → `evolution_pkg` / 脚本入口速查

上表「七类」偏**能力边界**；本表偏**落代码时从哪进包、哪找平铺 CLI**（与 [scripts/README · 按角色](../scripts/README.md#scripts-by-role) · **[§3 脚本簇](#scripts-cluster)** 互补）。**新增子模块**仍以 **[§2](#evolution-pkg)** 登记 **`SUBMODULE_DOMAIN`** 为准。

| 七类能力 | 首选 `evolution_pkg` | 平铺脚本 / 闸门入口（摘要） |
|----------|----------------------|------------------------------|
| **数据存储** | **`io`**、**`signals_flat_validate`**（manifest/候选扁平结构） | **`validate-evolution-*.py`**、**`validate-*`**、**`run_validate.sh`**；契约 **[DATA_CONTRACTS](./DATA_CONTRACTS.md)** |
| **沉淀** | **`sediment_validate`**、**`sediment_daily`** | **`analysis_engine --sediment`**（等价 **``-m evolution_pkg.analysis_pipeline --sediment``**）；沉淀/趋势 Schema 校验（**`make validate`**） |
| **分析** | **`analysis_core`**、**`analysis_validate`**、**`analysis_snapshot_build`**、**`analysis_pipeline`**、**`analysis_diff`**、**`analysis_lineage`**、**`hint_closure`**、**`analysis_hints`**、**`analysis_snapshot_history`**、**`ai_overlay_validate`** | **`analysis_engine.py`** / **``-m evolution_pkg.analysis_pipeline``**；**`diff_analysis_snapshot.py`**；**`lineage_utils.py`**（兼容 → **`analysis_lineage`**）；**`--check`** |
| **内容生成** | **`ingest_opinion_pool`**、**`ingest_json_http`**、**`ingest_*`**（maps / https / fetch / rss）、**`pipeline`**（编排子段） | **`ingest_opinion_law.py`** / **``-m evolution_pkg.ingest_opinion_pool``**；草稿 **[scripts/draft/README](../scripts/draft/README.md)** |
| **进化** | **`io`**（manifest/候选/决策读写面）、**`candidate_merge`**（并入清单条目的纯变换） | **`merge_candidates_to_manifest.py`** / **``-m evolution_pkg.candidate_merge``**；**[EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md)** |
| **汇总** | **`sediment_daily`** 与 **`analysis_*` 产出衔接** | **`sediment_trends.py`**、**`gen-sitemap.py`** |
| **展示** | **`nav_links`**、**`spa_nav`** | **`sync_site_nav.py`**（**`build_skip_bar`**：`maintainer-hub` 三锚）、**`gen_nav_links_ts.py`**；总线 **[SITE_DATA_UPDATE_FRAMEWORK](./SITE_DATA_UPDATE_FRAMEWORK.md)** |

---

<a id="evolution-pkg"></a>

## 2. `evolution_pkg` 子模块（六域登记）

新增顶层子模块须在 **`SUBMODULE_DOMAIN`** 登记，否则 **`test_evolution_pkg`** 失败。当前仓库内登记 **27** 个顶层子模块（**`domains.SUBMODULE_DOMAIN`** 键与包目录内 `*.py`/子包一一对应）。

| 子模块 | 六域归属 | 职责摘要 |
|--------|----------|----------|
| **`io`** | 数据 | 读写进化相关 JSON 的兼容入口（与 **`evolution_io.py`** 对齐） |
| **`signals_flat_validate`** | 数据 | **`validate-evolution-manifest.py`** / **`validate-evolution-candidates.py`** 共用的 manifest/候选 **扁平**结构校验 |
| **`candidate_merge`** | 治理 | **`strip_for_manifest`**、**`merge_candidate_ids`**、**`ReviewStateError`**、**`main()`**；推荐 **``python3 -m evolution_pkg.candidate_merge``**（根 **`merge_candidates_to_manifest.py`** 薄壳） |
| **`ingest_json_http`** | 数据 | JSON Feed 拉取与条目规范化（ingest 侧） |
| **`ingest_maps`** | 数据 | **`apply_routes`**、**`merge_maps_to_hints`**、**`load_maps_to_hints`**、**`stable_id`**、**`html_title`**（**`ingest_opinion_law`** / **`validate_golden_mapping`** 调包） |
| **`ingest_https`** | 数据 | **`assert_https_ingest_url`** / **`validate_config_fetch_urls`**（**`ingest_opinion_law`** 调包） |
| **`ingest_fetch`** | 数据 | **`fetch_bytes`** / 默认 **User-Agent**（**`ingest_opinion_law`** 调包） |
| **`ingest_rss`** | 数据 | **`parse_rss_or_atom`**（RSS 2.0 / Atom；**`ingest_opinion_law`** 调包） |
| **`ingest_opinion_pool`** | 数据 | RSS / 法规页 / **`json_feeds`** → **`evolution-candidates.json`** 编排；**`main()`** 返回码；推荐 **``PYTHONPATH=scripts python3 -m evolution_pkg.ingest_opinion_pool``**（根 **`ingest_opinion_law.py`** 薄壳） |
| **`sediment_validate`** | 数据 | 沉淀 / 趋势产物与 Schema 对齐的校验逻辑 |
| **`sediment_daily`** | 数据 | 日粒度沉淀 JSON + SQLite 写入编排（与 **`--sediment`** 衔接） |
| **`pipeline`** | 管道 | **`runner`**：`run_validate` 至单测后的分析写盘、遥测等编排 |
| **`hint_closure`** | 分析 | 闭环缺口 / **`track_closure`** 与规则消费辅助 |
| **`analysis_hints`** | 分析 | **`maps_to_hints`** 等提示加载与归并 |
| **`analysis_core`** | 分析 | 热力、共现等核心统计与共享工具 |
| **`analysis_diff`** | 分析 | 两份快照的 module/factor heat 与 sources 差分；**`build_report`** / **`snapshot_diff_json`**（**`diff_analysis_snapshot.py`** CLI） |
| **`analysis_lineage`** | 分析 | **`run_id`** / **`repo_revision`**（**`build_run_block`** / **`get_repo_revision_short`**）；根目录 **`lineage_utils.py`** 为兼容重导出 |
| **`analysis_validate`** | 分析 | 快照 **`--check`** 与输出形状校验 |
| **`analysis_snapshot_build`** | 分析 | 快照文档组装与写盘编排 |
| **`analysis_pipeline`** | 分析 | **`parse_analysis_cli`**、**`run_analysis_pipeline`**、**`main()`**（返回 **0**）、**`default_analysis_paths`** / **`AnalysisPaths`**；推荐 **``PYTHONPATH=scripts python3 -m evolution_pkg.analysis_pipeline``**（根 **`analysis_engine.py`** 薄壳） |
| **`analysis_snapshot_history`** | 分析 | SQLite **`analysis_snapshot_history`** 表读写元数据 |
| **`ai_overlay_validate`** | 分析 | **`ai-analysis-overlay`** JSON Schema 校验 |
| **`nav_links`** | 前端 | 顶栏 / 导航链生成与校验辅助 |
| **`spa_nav`** | 前端 | **nav.config**、**navLinks.ts** 与 **registry.pages** 一致性（**`check_nav_links_registry`**） |
| **`ops`** | 运维 | **`http_cache`**：ETag / **If-None-Match**，**`readonly_api`** 复用 |
| **`beijing_time`** | 运维 | 业务时区 **`Asia/Shanghai`**：`now_iso_beijing` / `today_iso_beijing` / `compact_date_beijing`（与 ingest / 分析 / SQLite / 管理端时钟对齐） |
| **`readonly_disk_routes`** | 运维 | 只读 API 磁盘 **GET** 路径表与 OpenAPI 登记 |

上表与 **`scripts/evolution_pkg/domains.py`** · **`SUBMODULE_DOMAIN`** 键集合**一一对应**；**`scripts/tests/test_evolution_pkg.py`** 校验「目录内顶层子模块 ≡ 映射键」。

**升级建议**：新增管道/校验/只读能力时**优先进包**，根目录 **`scripts/*.py`** 保持**薄 CLI**；域不明时先对照 **[INTELLIGENCE · §6](./INTELLIGENCE_SIX_DOMAINS.md#pr-checklist)** 再选归属。

---

<a id="scripts-cluster"></a>

## 3. 顶层 `scripts/` 簇（闸门 / 管道 / 侧车）

与 **[scripts/README.md](../scripts/README.md)** 一致，此处按**簇**归纳，便于排期与拆 PR。

| 簇 | 典型入口 | 说明 |
|----|----------|------|
| **总闸门** | **`run_validate.sh`**、**`run_validate_fast.sh`**（**`make validate-fast`**；**非**合并替代） | **`make validate`** 与 pre-commit、CI **validate** 同源；**fast** 仅本地、**不**进 CI/pre-commit；顺序变更须分别回归 |
| **JSON 契约校验** | **`validate_*.py`**、`validate-evolution-*.py` | 与 **`docs/schemas/`** 一一对应；索引 **[schemas/README.md](./schemas/README.md)** |
| **对账与导航** | **`check_manifest_drift`**、**`sync_site_nav`**、**`check_skip_bar_404`**、**`check_nav_links_registry`**、**`gen_nav_links_ts`** | **单一注册表** + **双轨 SPA**；**`sync_site_nav`** 含 **`maintainer-hub`** 的 **`build_skip_bar`** 段（勿手改 HTML） |
| **管道编排** | **`run_pipeline_steps.py`**、**`run_update_pipeline.sh`**、**`run_analyze_write.sh`** | 遥测 **`artifacts/pipeline-metrics-*.json`**；**`SKIP_PIPELINE_TELEMETRY`**；旧文件 **`make clean-pipeline-metrics-dry-run`** / **`make clean-pipeline-metrics`**（**`Makefile`**） |
| **抓取与人审** | **`ingest_opinion_law.py`**（薄；**`ingest_opinion_pool`**）· **`merge_candidates_to_manifest.py`**（薄；**`candidate_merge`**） | 外网 ingest；merge **仅人审后**；等价 **`-m evolution_pkg.ingest_opinion_pool` / `candidate_merge`** |
| **分析写盘** | **`analysis_engine.py`**（薄；**`analysis_pipeline`**） | **`--check`** 不写盘（等价 **`-m evolution_pkg.analysis_pipeline --check`**）；**`--sediment`** 与 SQLite 双写策略见 **DATA_CONTRACTS** |
| **趋势与历史** | **`sediment_trends.py`**、**`list_analysis_snapshot_history.py`** | 趋势默认写 **`assets/sediment-trends.json`** |
| **只读与状态** | **`readonly_api.py`**、**`evolution_pkg.readonly_disk_routes`**、**`print_evolution_status.py`**、**`diff_analysis_snapshot.py`** | API 变更 → **`test_readonly*.py`**（**`make test-readonly-api`** / **`merge-ready`**） |
| **可选分析** | **`query_evolution_duckdb.py`** | **`requirements-analytics.txt`**；不进默认 CI |
| **维护/一次性** | **`migrate_*`**、**`apply_site_round_extensions.py`** 等 | **不**接入默认 **`run_validate.sh`** |

---

<a id="front-admin-spa"></a>

## 4. 呈现与管理端模块

**读者面 × 管理面按模块一页表**（与下表互补）：**[docs/README · #front-back-modules](./README.md#front-back-modules)** · **[docs/README · #system-components-fusion](./README.md#system-components-fusion)**。

| 模块 | 路径 | 职责边界 | 升级注意 |
|------|------|----------|----------|
| **MPA 静态站** | 根 **`*.html`**、`partials/`、`assets/*.js`（含 **`site-data-bus.js`**） | **CI 与 `make validate` 默认真源** | 总线新消费方 → **SITE_DATA_UPDATE_FRAMEWORK** |
| **全站 SPA** | **`spa/src/`**、**`spa/nav.config.json`**、**`vite.config.ts`** | iframe 承载剥壳 HTML；路由 ≡ **registry** | **`make spa-build`**；CI 按路径触发 |
| **管理端脚手架** | **`admin-console/`** | 占位 FastAPI；**不写 manifest** | **ADMIN_WEB_CONSOLE_ROADMAP** · **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**（**`mod-*`** · **`#mod-api`→`#mod-analysis`**）；**`make test-admin-console`** |
| **只读 API 镜像** | **`Dockerfile`** / **compose profile `api`** | 读磁盘 JSON | **INTEGRATION_AND_READONLY_API**、**DOCKER** |

---

<a id="upgrade-matrix"></a>

## 5. 架构升级矩阵（按模块簇 × 阶段）

**原则**：**先耗尽阶段 1** 再评估阶段 2/3（见 **[UPGRADE_ROADMAP · §3](./ARCHITECTURE_UPGRADE_ROADMAP.md#phased-playbook)**）。**数据层服务器库 / CDC** 见 **[DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)**；**编排 / Kafka** 见 **[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)**。

| 模块簇 | 阶段 0—1（推荐默认） | 阶段 2（编排器） | 阶段 3（事件流） |
|--------|----------------------|------------------|------------------|
| **契约 + `run_validate.sh`** | 持续补 **Schema**、单测、文档；保持单入口 | 编排**调用**现有 shell/python，**不**拆 validate 为二套 | 无直接替代；CI 仍以 **validate** 为准 |
| **`evolution_pkg`** | 新逻辑进包 + **`domains`** 登记；根脚本变薄 | 编排步骤 = 对 **`pipeline.runner`** 或子步骤的封装 | 事件由业务服务发；包内逻辑**不**绑死 broker |
| **ingest / merge** | 候选校验、drift；merge **人工** | 定时 ingest 可迁编排；**merge 仍人审** | 多源写入池可考虑 topic；**Git 仍审计主链** |
| **分析（`analysis_pipeline`）+ 沉淀/趋势** | **`schema_version`**、消费者同步；根 **`analysis_engine.py`** 为薄 CLI | 分区回填、多环境参数 | 一般**不需要** Kafka；除非多服务写分析输入 |
| **只读 API + admin-console** | 新 **GET**、ETag、烟测、文档；**`admin-console`** 单页 IA **[§7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** · **[§7b](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-ui-ia)** | 编排可拉取 API 健康状态 | Webhook/事件通知**可选** |
| **MPA / SPA / 总线** | registry/nav/总线登记三件套 | 与编排**无关**时可并行 | 实时推送非默认；仍 **fetch 已提交 JSON** 为主 |
| **Docker / CI** | **双轨** **validate** + **spa-build**；**merge-ready** | 编排 Agent 与 CI **分工文档化** | **kafka-dev** 仅 PoC，**不进**默认 CI |

---

<a id="sequence"></a>

## 6. 推荐升级顺序（同一架构迭代内）

1. **对齐语言**：维护者共读本文 **§1—§2** + **[ARCHITECTURE_UPGRADE_ROADMAP · §1 全景图](./ARCHITECTURE_UPGRADE_ROADMAP.md#upgrade-panorama)**。  
2. **契约先行**：动到的每个 JSON 面 → **Schema → 校验脚本 → `run_validate.sh`**。  
3. **包化与域**：动到的每个新脚本 → **`evolution_pkg`** + **`domains`** + **`test_evolution_pkg`**。  
4. **双轨与导航**：动 **registry** → 同步 **SPA** + **`make validate`**。  
5. **只读与管理端**：动 **API/admin** → **INTEGRATION** / **DOCKER** / **`merge-ready`**。  
6. **再评估 2/3 与 DATA_STORES**：仅 **[ORCHESTRATION](./ORCHESTRATION_AND_EVENT_STREAMING.md)**、**[DATA_STORES](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)** 与 **ROADMAP §3.3—3.4** 信号齐备时单独立项（**[INCREMENTAL_BUILD_PLAYBOOK](./INCREMENTAL_BUILD_PLAYBOOK.md)** **J/K**）。

---

<a id="anti"></a>

## 7. 反模式（模块升级时）

- 为「上编排/上 Kafka」**新建第二套 validate**，与 **`run_validate.sh`** 漂移。  
- 把 **manifest 写入** 放进 **admin-console** 或 **编排器默认步骤**。  
- **大脚本不拆 PR**，一次改契约 + 十页 HTML + SPA + API。  
- **无信号**同时动 **Playbook J + K**（编排与服务器库/Kafka 齐上）。

---

<a id="reading"></a>

## 8. 延伸阅读

- 七类能力细表：**[ARCHITECTURE.md#seven-layers](./ARCHITECTURE.md#seven-layers)**  
- 分域改造矩阵：**[ARCHITECTURE_UPGRADE_ROADMAP · §2](./ARCHITECTURE_UPGRADE_ROADMAP.md#domain-action-matrix)**  
- 增量组件顺序：**[INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md)**  
- 平台总览与调用：**[PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)**  
- 不变量与阶段定义：**[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md)**
- 按阶段执行指南：**[PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)**

---

*随仓库模块变更更新：新增 **`evolution_pkg`** 子包、默认校验链新步骤、或 CI 新 job 时，请修订 **§2—§3** 与 **§5** 对表。*
