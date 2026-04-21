# 文档索引

站内 Markdown 说明与 Schema 入口（与根目录 [README.md](../README.md) 中的运行说明互补；**读者 / 贡献者入口与 15 分钟自检**：[README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)）。**角色判型**（读者 / 贡献者 / 数据管道 / 部署四条动线）：根 [README · 产品视角](../README.md#pm-four-journeys)（**从这里开始** / **双轨真源**见上句）。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)。**新贡献者**：先读根目录 [CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd)；**真源分层总览**见下方 **[#content-framework](#content-framework)**；**读者面 × 管理面按模块对表**见 **[#front-back-modules](#front-back-modules)**；**可执行单元 × 主链（组件—功能）**见 **[#system-components-fusion](#system-components-fusion)**，再按下表深入。**MPA 维护枢纽**：[维护导读](../maintainer-hub.html) · [关系视图](../maintainer-hub.html#mh-spine-map)（枢纽页 ↔ 注册表 ↔ 文档锚点）· [系统边界速查](../maintainer-hub.html#mh-boundaries)（真源 / 生成物 / 侧车 / 闸门 / 手调例外） · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)。**Cursor**： [.cursor/rules/repo-gates.mdc](../.cursor/rules/repo-gates.mdc)（始终；判型含 [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)）；**`spa/nav.config.json`** → [spa-nav-config.mdc](../.cursor/rules/spa-nav-config.mdc)；**`spa/src/**`** → [spa-nav-registry.mdc](../.cursor/rules/spa-nav-registry.mdc)；**`scripts/evolution-registry.json`** → [evolution-registry.mdc](../.cursor/rules/evolution-registry.mdc)（子规则文首判型链与 **repo-gates** 同构；与 [AGENTS.md](../AGENTS.md#agents-contract) · [#agents-cursor-rules](../AGENTS.md#agents-cursor-rules) 对读；**registry / SPA / hub** 判型亦见 **[#agents-content-framework](../AGENTS.md#agents-content-framework)**）。

<a id="docs-spine"></a>

## 文档主线（整理速览）

维护、改版或对外说明时，建议按下面**顺序扫一遍**（各步链到 canonical 文档；与 [PLATFORM_CAPABILITY_MAP · §5 维护者](./PLATFORM_CAPABILITY_MAP.md#reading-order) 一致并互为补充）。

<a id="tech-stack-read-merge"></a>

### 技术栈文档怎么读（合并入口，防散）

多篇都写「技术栈」，**不必合成一篇超长稿**；按目的选**一条主链**，其余当附录即可：

| 你的目的 | 建议以这一篇为主 | 需要时再打开 |
|----------|------------------|--------------|
| **栈分层 + 主数据链 + 闸门 + 升级阶段（一页收束）** | **[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)**（简版 **§1—§4** + **[附录 · 详版能力地图等](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)**） | 别名入口仍可用 **[TECH_ARCHITECTURE_CAPABILITIES](./TECH_ARCHITECTURE_CAPABILITIES.md)**（重定向表）；数据流与七类模块 **[ARCHITECTURE](./ARCHITECTURE.md)** |
| **内容 × 架构 × 组件 + `make` / 文档入口怎么选** | **[PLATFORM_MASTER_MAP](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)** | 五维总索引 **[PROJECT](./PROJECT_ARCHITECTURE_OVERVIEW.md)**；判型 **[#quick-paths](#quick-paths)** |
| **技术 / 内容 / 推演 三架构对照（一句话）** | **[ARCHITECTURE_ONE_PAGER · 三架构](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** | 各专篇见 ONE_PAGER 内链 |

**分工约定**：**[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)** 内 **§1—§4** 为简表收束，**[#appendix-tech-capabilities](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)** 为原独立篇详版正文（分层详表、Mermaid、能力地图）；旧文件名 **[TECH_ARCHITECTURE_CAPABILITIES](./TECH_ARCHITECTURE_CAPABILITIES.md)** 仅作**重定向与深链别名**。**ARCHITECTURE** 以**数据契约与七类模块**为轴，不是「组件栈清单」；**PLATFORM_MASTER** 以**谁调谁、命令与页面入口**为轴。枢纽页 **[关系视图](../maintainer-hub.html#mh-spine-map)** · **[系统边界](../maintainer-hub.html#mh-boundaries)** · **[衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)** 再把注册表与上述锚点收在一屏。

**维护约定**：新增或调整「栈分层 / 能力地图 / 进化含义」时改 **BRIEF 附录**（或与之对读的 **ARCHITECTURE** 数据轴段落），**不建议**把 **ARCHITECTURE** 或 **PLATFORM_MASTER** 并入技术栈简篇（会混「数据真源」与「调用总表」，检索变差）。**MPA / SPA 双轨**仍按 [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [README · 双轨真源](../README.md#readme-dual-track-map) · [关系视图](../maintainer-hub.html#mh-spine-map) · [系统边界](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)。

<a id="content-framework"></a>

### 整体内容框架（真源分层与预期）

先对表本表，再进 **[#quick-paths](#quick-paths)** 判型；**五维 / 六域 / 七类** 勿混见 **[勿混粒度](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · **[§1b 仓库物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**读者面 / 管理面按模块对读**见本节 **[#front-back-modules](#front-back-modules)**；**组件—功能一条表**见 **[#system-components-fusion](#system-components-fusion)**。

**薄壳 CLI 与包内真源（三条主链）**：CI 与 **`run_validate.sh`** 仍调用 **`scripts/`** 下稳定文件名（**`ingest_opinion_law.py`**、**`merge_candidates_to_manifest.py`**、**`analysis_engine.py`**）；**实现**分别在 **`evolution_pkg.ingest_opinion_pool`**、**`evolution_pkg.candidate_merge`**、**`evolution_pkg.analysis_pipeline`**。本地或编排器可改用 **`PYTHONPATH=scripts python3 -m evolution_pkg.<模块>`**（参数相同），见 **[scripts/README · `evolution_pkg` 收束队列](../scripts/README.md#pkg-migrate-queue)**。

| 层次 | 真源在哪 | 维护时预期 |
|------|----------|------------|
| **读者叙事与枢纽版式** | 根目录 **`*.html`**、**`assets/site.css`**、**`partials/`**（**`make sync-nav`**） | 不冒充 JSON 契约变更；**`maintainer-hub.html`** 在五链 skip 后再由 **`sync_site_nav.py` · `build_skip_bar`** 拼 **`#mh-spine-map` / `#mh-boundaries` / `#mh-reader-admin-matrix`**，勿手改 HTML。**`404.html`** 顶栏/skip **不在** **`sync_site_nav`** 写回范围，改 **`partials/`** 时须**手调** **404** 与 partial 一致（**`make validate`** 含 **`check_skip_bar_404`**）。纯版式/枢纽叙事对照 **[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** 与 **[#content-driven-chain](#content-driven-chain)** 中「纯 CSS/HTML」边界；顶栏模板动线见 **[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[scripts/README · #sync-site-nav-source](../scripts/README.md#sync-site-nav-source)** |
| **结构化数据与注册边界** | **`assets/*.json`**、**`data/*.json`**、**`scripts/evolution-registry.json`**、**`docs/schemas/*.json`** | **Schema** + **`make validate`** + **[DATA_CONTRACTS](./DATA_CONTRACTS.md)**；**分析管道不写 HTML**（**`analysis_engine.py`** 为薄 CLI，真源 **`evolution_pkg.analysis_pipeline`**；见 **[scripts/README · 收束队列](../scripts/README.md#pkg-migrate-queue)**） |
| **站内 Markdown 说明** | **`docs/*.md`** | 静态根部署下点击多为**原文/下载**；与网页渲染差异见 **[PLATFORM · §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)** |
| **闸门与可执行发布** | **`scripts/`**、**`.github/workflows/`**、**`Makefile`** | 合并依据以 **`make validate`** 为准；合并前推荐 **`make merge-ready`**；对齐 **[AGENTS.md](../AGENTS.md#agents-pre-merge)** · **[MERGE 清单](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** |
| **双轨呈现** | **MPA**（根分页；**`validate` / CI 默认真源**）· **`spa/`**（可选；**`nav.config` ≡ `registry.pages`**） | 触达 SPA 路径时见根 **[README.md](../README.md)** · **[spa/README](../spa/README.md)** |
| **管理面脚手架** | **`admin-console/`** | **不写 manifest**；与只读 API 见 **[admin-console/README](../admin-console/README.md)** · **[DOCKER · §3a](./DOCKER.md#profile-admin)**；单页 UI 分区与锚点 **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**（**`mod-*`** · **`#mod-api`→`#mod-analysis`**） |

<a id="front-back-modules"></a>

#### 前后台模块总览（读者面 × 管理面）

**用语**与 **[USER_ADMIN_SPLIT · §1a](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)**、**[PLATFORM_MASTER_MAP · §1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)** 一致：**前台** = 读者在浏览器中的**呈现与只读交互**；**后台** = **Git / 脚本 / CI / 只读 HTTP / 管理脚手架**上的维护动作（**不**替代 **manifest** 人审）。**读者面 ↔ 管理面衔接矩阵 / 场景对表**：[PLATFORM_MASTER_MAP · 衔接矩阵](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-contract-matrix) · [场景×面](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-scenarios)。**七类能力 → 仓库模块**另见 **[MODULE · §1—§1a](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#seven-to-modules)**；**内容 × 架构 × 组件**总表见 **[PLATFORM_MASTER_MAP · §1](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#three-layers-map)**。

| 模块域 | 前台（读者常见触达） | 后台（维护常见触达） | 契约 / 索引 |
|--------|----------------------|----------------------|-------------|
| **枢纽与分页** | 根 **`*.html`**、**`partials/`** 生成的顶栏与 skip-bar（**`404.html`** 顶栏/skip **手维护**；**`maintainer-hub.html`** 五链后三页内锚由 **`build_skip_bar`** 生成） | **`make sync-nav`**、**`sync_site_nav.py --check`**、**`check_skip_bar_404.py`** | **[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** · **[SITE_REVIEW](./SITE_REVIEW_THREE_PASSES.md)** · **[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[scripts/README · #sync-site-nav-source](../scripts/README.md#sync-site-nav-source)** |
| **注册与双轨导航** | 站内分页链、可选 **`spa/`** 壳内 iframe | **`scripts/evolution-registry.json`**、**`spa/nav.config.json`**、**`make gen-nav-links` / `spa-build`** | **[DATA_CONTRACTS](./DATA_CONTRACTS.md)** · **[spa/README](../spa/README.md)** |
| **总线读数** | **`site-data-bus.js`**、页内 **`[data-site-data-live]`** | **[SITE_DATA](./SITE_DATA_UPDATE_FRAMEWORK.md)** 登记消费方；**`assets/*.json`** 真源 | **[SITE_DATA](./SITE_DATA_UPDATE_FRAMEWORK.md)** |
| **分析仪表盘** | **`analysis-hub.html`** 等动态块 | **`analysis_engine.py`**（薄 CLI）/ **``-m evolution_pkg.analysis_pipeline``** · **`assets/analysis-snapshot.json`** 与 Schema | **[DATA_CONTRACTS](./DATA_CONTRACTS.md)** · **[scripts/README](../scripts/README.md)** |
| **沙盘** | **`lab.html`**、**`assets/lab.js`** | **`evolution-registry.json`** 的 **`lab_factors`** | **[MODULE · 七类](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#seven-to-modules)** |
| **信号 / 候选 / manifest** | **`evolution.js`** 等只读呈现；同源只读代理 | **`ingest_opinion_law.py`** / **``-m evolution_pkg.ingest_opinion_pool``** · **`merge_candidates_to_manifest.py`** / **``-m evolution_pkg.candidate_merge``** · PR 与 **`review_state`** | **[DATA_ANALYSIS_SITE_CONTENT_SYNC](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md)** |
| **只读 HTTP API** | 部署后由前端或外链消费 **`/snapshot`** 等 | **`readonly_api.py`**、**`make test-readonly-api`** | **[INTEGRATION](./INTEGRATION_AND_READONLY_API.md)** |
| **管理控制台** | 非叙事真源；观测与脚手架 UI | **`admin-console/`**、**`make test-admin-console`**、Compose profile **`admin`** | **[ADMIN_CONSOLE_FRAMEWORK](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md)** · **[§7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** · **[DOCKER · §3a](./DOCKER.md#profile-admin)** |
| **运行与发布** | GitHub Pages、**`make serve-reader`**、Docker **8765** | **`.github/workflows/`**、**`Makefile`**、**`make validate` / `merge-ready`** | **[README](../README.md)** · **[DOCKER](./DOCKER.md)** · **[MERGE](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** |

<a id="system-components-fusion"></a>

#### 系统组件与功能融合总览（一条表串主链）

与上表 **[#front-back-modules](#front-back-modules)** 互补：上表按**业务域**拆「读者 / 维护 / 契约」；本表按**可部署或可执行单元**收束「**组件 → 角色 → 功能 → 入口**」，便于和 **[ADMIN_CONSOLE · §2 拓扑](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-topology)**、**[INTEGRATION · 只读 API](./INTEGRATION_AND_READONLY_API.md)** 对读。**推演与对表用 Git 真源**在管理端数据源目录 **[「全站推演与对表」类目](../admin-console/data/data_source_catalog.json)**（经 **`GET /api/bootstrap`** · **`data_source_catalog`** 下发），与 **[DEDUCTION_STRATEGY](./DEDUCTION_STRATEGY.md)**、**[SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK](./SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md)** 对表。

| 组件 | 角色 | 主要功能 | 典型入口 |
|------|------|----------|----------|
| **根目录 MPA**（`*.html`、`assets/site.css`、`partials/`） | 读者呈现真源 | 叙事、枢纽、站内链；总线挂载点 | 静态托管 / **`make serve-reader`** / Docker **8765** |
| **`site-data-bus.js`** | 读者壳层 | 并行缓存 **`analysis-snapshot`** / **trends** / **site-meta**；轻量搜索索引可选 | **[SITE_DATA](./SITE_DATA_UPDATE_FRAMEWORK.md)** |
| **`analysis.js` + `analysis-hub.html`** | 读者壳层 | 热力、共现、闭环缺口、可选 AI overlay | **`assets/analysis-snapshot.json`** |
| **`readonly_api.py`** | 只读 HTTP 面 | 白名单 **GET**；磁盘 JSON / SQLite 历史；**不**写 manifest | **`INTEGRATION`** · **`make test-readonly-api`** · 默认 **8099** |
| **`admin-console/`**（FastAPI + `static/index.html`） | 管理薄控制面 | **`/api/bootstrap`**、只读同源代理、账户、**数据源参考**（含推演类目）、观测摘要 | **[ADMIN_CONSOLE](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md)** · Docker profile **admin** · **8100** |
| **`evolution_pkg` + 根 `scripts/*.py` 薄壳** | 闸门与管道真源 | ingest / merge / analyze / Schema 校验 / 导航同步子集 | **[scripts/README](../scripts/README.md)** · **`make validate`** |
| **`.github/workflows` + `Makefile`** | 编排与本地命令 | CI **`validate`**、定时 ingest / analyze **artifact**、**`merge-ready`** | **[EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md)** |
| **`scripts/evolution-registry.json`** | 站点边界登记 | 允许出现的根 **`pages[]`** 与 **`lab_factors`** | **`make validate`** · **`check_nav_links_registry`** |
| **`data_source_catalog.json`**（管理端 `data/`） | 规划参考（非爬虫） | 外网 RSS/门户条目 + **仓库内推演真源**勾选 | **`GET /api/bootstrap`** · **[ADMIN_PIPELINE](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)** |

**数据主链（与上表同一主链，压缩成一句）**：外网/制度线索 → **ingest** → **`evolution-candidates`** → 人审 → **`evolution-manifest`** → **`analysis_engine`** → **`analysis-snapshot`**（+ 可选沉淀 / 趋势）→ **总线 / hub** 呈现；**管理端**只观测与对账，**不**替代 **`make validate`** 与 **PR 人审**。

<a id="quick-paths"></a>

### 常见改动 → 最短链（先判型再深读）

| 本轮主要改… | 先打开的文档 / 命令 |
|---------------|---------------------|
| **`evolution-registry.json` 的 `pages[]` / `lab_factors`（未删 HTML）** | [CONTRIBUTING · 常见变更自检](../CONTRIBUTING.md#contributing-common-changes-checklist) 表「registry 三件套」→ **`make sync-nav`** → **`spa/nav.config.json`** 与 **`pages`** 对齐 → **`make gen-nav-links`** 或 **`make spa-build`** → **`make validate`**；对表 [PROJECT · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)。**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 生成，勿手改 HTML。若本轮含 **`partials/skip-bar.inc.html`**，**`404.html`** 须**手调**（`sync_site_nav` 不写回）— [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · **[scripts/README · #sync-site-nav-source](../scripts/README.md#sync-site-nav-source)** |
| **根目录 HTML 叙事 / 枢纽 CSS（无新 `[data-site-data-live]`）** | [INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract) · [SITE_REVIEW](./SITE_REVIEW_THREE_PASSES.md) |
| **`assets/site-data-bus.js`（总线逻辑 / 读者壳层；无新 `fetch` 路径）** | [SITE_DATA_UPDATE · §3a](./SITE_DATA_UPDATE_FRAMEWORK.md#reader-chrome) · [INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract) · **`make validate`** |
| **快照 / 沉淀 / 趋势 / 规则 JSON 语义** | [DATA_CONTRACTS](./DATA_CONTRACTS.md) → 先 **Schema** → **`analysis_engine --check`**（等价 **``PYTHONPATH=scripts python3 -m evolution_pkg.analysis_pipeline --check``**）；迭代可用 **`make validate-fast`**（**CI / pre-commit 不跑**）；**合并前** **`make validate`** |
| **流水线遥测旧格式 / `validate`  stderr 提示跳过** | [EVOLUTION_RUNBOOK · 加速](./EVOLUTION_RUNBOOK.md#accelerate) · [DATA_CONTRACTS · §7](./DATA_CONTRACTS.md#pipeline-telemetry) · **`make clean-pipeline-metrics-dry-run`** → **`make clean-pipeline-metrics`** → 再 **`make analyze`** 或 **`make evolution-fast`** |
| **AI 解读层 / overlay / 外呼 LLM 规划 · ingest 规则黄金集** | **[AI 与自动进化 · 本节](#ai-assisted-evolution)** · [AI_ASSISTED](./AI_ASSISTED_ANALYSIS_LAYER.md) · [INTELLIGENCE · §8](./INTELLIGENCE_SIX_DOMAINS.md#ai-era-alignment) · **3d** **`fixtures/ai_mapping_golden/`** |
| **新增或迁入 `evolution_pkg` 顶层子模块** | [MODULE · §2](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#evolution-pkg) · **`domains.SUBMODULE_DOMAIN`** → **`make test`** |
| **只读 API / Docker / CI 双轨** | [INTEGRATION_AND_READONLY_API](./INTEGRATION_AND_READONLY_API.md)（**OpenAPI** · **[可选增强：搜索 / DuckDB / 管理端拆包](./INTEGRATION_AND_READONLY_API.md#optional-reader-ops-enhancements)**）· [DOCKER](./DOCKER.md) · [ORCHESTRATION](./ORCHESTRATION_AND_EVENT_STREAMING.md)（§1 默认栈） |
| **舆情 / 制度 / 国情 → ingest 与反哺节奏** | [INTEL_AND_POLICY_TRACKING_PLAYBOOK](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)（**[§2 信源分层 · 2a 拉取约束](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b 微博/站内流](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**）· [EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md) · [ADMIN_PIPELINE](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md) |
| **舆情类开源产品对标与暴露面（参考非依赖）** | [REFERENCE_DESIGN_OPINION_MONITORING](./REFERENCE_DESIGN_OPINION_MONITORING.md) · 与上条手册分工：对标读 REFERENCE，日常流程读 INTEL |
| **`admin-console/`**（**`static/index.html`**、顶栏、**`mod-*`**、深链） | **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** · **[§7b](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-ui-ia)** · **`make test-admin-console`** · [admin-console/README](../admin-console/README.md) · [MERGE 清单 · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) |
| **情报 ingest · 管理控制台 · SPA 壳（常一起判型）** | **[INTEL · §2—2a](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)**（信源/频率）· **[§2b](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**（微博/主媒 App 流）· **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** · [admin-console/README](../admin-console/README.md) · **[spa/README](../spa/README.md)**（`nav.config` ≡ `registry.pages`）；分页/顶栏登记仍走上行 **registry 三件套**；默认真源 **根目录 MPA + `make validate`** |
| **读者面 / 管理面按模块对表（防混读）** | [本节「前后台模块总览」](#front-back-modules) · [本节「组件×功能一条表」](#system-components-fusion) · [USER_ADMIN_SPLIT · §1a](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend) · [PLATFORM_MASTER_MAP · §1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces) |

更细的「该打开哪篇架构文档」见 [PLATFORM_MASTER_MAP · §3](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#architecture-entry)。**七类能力 → 包与脚本入口**速查：[MODULE · §1a](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#seven-class-pkg-quick)。

<a id="content-driven-chain"></a>

**内容驱动（与上表同一判读习惯）**：真源为 **Git 内 JSON** 与已定稿 HTML；**「哪些随数据/分析自动变、哪些必须人改」**以 **[DATA_ANALYSIS_SITE_CONTENT_SYNC](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md)** 为总索引；**总线 `fetch` 与 `[data-site-data-live]` 消费方**见 **[SITE_DATA_UPDATE_FRAMEWORK](./SITE_DATA_UPDATE_FRAMEWORK.md)**。**纯 CSS/HTML 枢纽版式**（无新 live 属性）只按 **[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** 与 **[进化与优化](./INTELLIGENCE_SIX_DOMAINS.md#evolution-and-optimization)** 自检，**不**把此类改动登记进 SITE_DATA 消费方表。字段/语义变更仍先 **[DATA_CONTRACTS](./DATA_CONTRACTS.md)** + Schema；PR 文案里 **进化 vs 优化**、**五维/六域/七类** 与 **[CONTRIBUTING · 术语](../CONTRIBUTING.md#contributing-terminology)** 对齐。

<a id="ai-assisted-evolution"></a>

**AI 与「自动进化」在本站**：**不**表示模型或 Agent **默认**改写 **`evolution-manifest.json`**、候选真源或根目录 **`.html` 叙事真源`**；而在 **[不变量](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#invariants)** 与 **[智能化边界 · §1.1](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)** 内，把算力接到 **可 diff 产物 + Schema + `make validate` + PR 人审**。能力链（与六域对位见 **[INTELLIGENCE · §8](./INTELLIGENCE_SIX_DOMAINS.md#ai-era-alignment)**）：

1. **可选解读叠加（分析域 → 读者域）**：**[AI_ASSISTED_ANALYSIS_LAYER](./AI_ASSISTED_ANALYSIS_LAYER.md)** · **`assets/ai-analysis-overlay.json`** 契约与只读 **`GET /ai-analysis-overlay`**；**不**把 LLM 输出并入 **`analysis-snapshot.json` 必填域**。  
2. **规则层可验收「进化」（数据/管道域）**：**`fixtures/ai_mapping_golden/`** · **`validate_golden_mapping.py`**（主线 **3d**；ingest routes / hints 与 registry 对账）。  
3. **叙事长草稿（内容生成域）**：**[scripts/draft/README.md](../scripts/draft/README.md)** — PR 审阅后再迁入 **`.html`** 或契约 JSON。  
4. **节奏与 artifact（管道/运维域）**：**[EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md)** · Actions / **`make evolution-fast`** — 自动化停在 **artifact 与候选**；合并 manifest 仍人审。

| 顺序 | 主题 | 主文档 |
|------|------|--------|
| 整框 | **整体内容框架**（真源分层；先于判型扫读） | [本节「整体内容框架」](#content-framework) · 再 [「常见改动 → 最短链」](#quick-paths) |
| 前后 | **前后台模块总览**（读者面 × 管理面） | [本节「前后台模块总览」](#front-back-modules) · [本节「融合总览」](#system-components-fusion) · [USER_ADMIN_SPLIT · §1a](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend) · [PLATFORM_MASTER_MAP · §1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces) |
| 融合 | **系统组件与功能一条表**（可执行单元 × 主链） | [本节「融合总览」](#system-components-fusion) · [ADMIN_CONSOLE · §2 拓扑](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-topology) |
| 0 | **合并闸门与 CI 对齐** | **`make validate`**（必）· 推荐 **`make merge-ready`** — [MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)、[CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd) |
| 0a | **平台总览：内容·架构·组件与合理调用** | [PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)（总表 · [读者面/管理面速查 · 节 1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces) · 三条黄金路径 · 文档入口选择） |
| 0b | **五维整体架构图谱（总索引）** | [PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md)（数据 · 内容 · 演进 · 方法论 · 运行态；**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)**；**[§1a 主链联动与验证](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** · **[§1b 仓库物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**） |
| 0c | **常见改动最短链（先判型再深读）** | [本节「常见改动 → 最短链」](#quick-paths) · [MODULE · §1a 七类→包/脚本](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#seven-class-pkg-quick) · [PLATFORM_MASTER_MAP · §3 架构入口](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#architecture-entry) |
| 0b | **五条架构红线（不变量索引）** | [ARCHITECTURE_ONE_PAGER · architect-invariants-index](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [CONTRIBUTING · PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) |
| 1 | **三架构一页对照** | [ARCHITECTURE_ONE_PAGER.md](./ARCHITECTURE_ONE_PAGER.md#three-architectures) |
| 1a | **技术架构整理 + 升级路径** | [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)（简版 **§1—§4**：分层 · 阶段 0—3 · 优先级 backlog）· **[附录 · 详版能力地图等](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)** · [别名 stub](./TECH_ARCHITECTURE_CAPABILITIES.md) |
| 1b | **模块全量梳理与架构升级矩阵** | [MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)（七类 × 脚本簇 × `evolution_pkg` × 阶段 0—3） |
| 1c | **按阶段升级（执行指南）** | [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)（**[落地执行 · 可复制命令](./PHASED_UPGRADE_EXECUTION_GUIDE.md#execution-now)** · 阶段 0→1→2/3 · 正交 2.5 数据层 · 验收与迭代模板） |
| 2 | **扩展插槽 · 进化轨 · 智能化边界 · 六域协同 · 读者/管理分拆 · 管理 Web 路线图** | [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)（**[进化与优化](./INTELLIGENCE_SIX_DOMAINS.md#evolution-and-optimization)** · 枢纽 MPA **CSS/HTML** **[§2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**）· [USER_ADMIN_SPLIT · 节 1a · 前端/后端](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend) · [ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md) · [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) · [PLATFORM_CAPABILITY_MAP §8](./PLATFORM_CAPABILITY_MAP.md#extensibility) · [分端设计全文](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md) |
| 3 | **数据流与字段主键** | [ARCHITECTURE.md](./ARCHITECTURE.md) · [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) · [schemas/README.md](./schemas/README.md) |
| 3d | **ingest 规则层黄金集（routes + hints ↔ registry）** | **`fixtures/ai_mapping_golden/`** · **`scripts/validate_golden_mapping.py`** · [schemas/ai-mapping-golden.schema.json](./schemas/ai-mapping-golden.schema.json) · [DATA_CONTRACTS · §2](./DATA_CONTRACTS.md#signals-candidates) |
| 3a | **SQLite 侧车列速查 · 不宜主库域 · 服务器库与 CDC 排期** | [DATA_CONTRACTS · §5 速查](./DATA_CONTRACTS.md#sqlite-sidecar-column-inventory) · [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md) |
| 3b | **方法论分析 + 可选 AI 解读层（配置接入）** | [AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md) · [examples/ai_analysis_overlay.example.json](./examples/ai_analysis_overlay.example.json) · **[#ai-assisted-evolution](#ai-assisted-evolution)**（与 **3e** 对读） |
| 3c | **舆情类开源系统：参考引用设计（侧车/管道边界）** | [REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md)（与 **3b**、**8a**、**ARCHITECTURE** 对读） |
| 3e | **AI 辅助的「自动进化」总收束（契约内 · 非全自动改站）** | **[本节 · AI 与自动进化](#ai-assisted-evolution)** · [INTELLIGENCE · §8](./INTELLIGENCE_SIX_DOMAINS.md#ai-era-alignment) · [PLATFORM · §1.1](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution) · 与 **3b** / **3d** / **9** 对读 |
| 4 | **命令与管道节奏** | [scripts/README.md](../scripts/README.md) · [EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md) |
| 4a | **增量构建 · 提前接组件 · 调试闭环** | [INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md) · [templates/incremental-pr-slice.md](./templates/incremental-pr-slice.md) |
| 5 | **数据→呈现边界 · 总线 · 读数消费方** | [DATA_ANALYSIS_SITE_CONTENT_SYNC.md](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md) · [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md)（**纯版式**不登记：与 **[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** · **[进化与优化](./INTELLIGENCE_SIX_DOMAINS.md#evolution-and-optimization)** 分列；日常闭环 **[#continuous-analysis-optimization](./INTELLIGENCE_SIX_DOMAINS.md#continuous-analysis-optimization)**）· **[内容驱动链](#content-driven-chain)** |
| 6 | **呈现 · 读者预期 · 发布复查** | [SITE_REVIEW_THREE_PASSES.md](./SITE_REVIEW_THREE_PASSES.md) · [PLATFORM_CAPABILITY_MAP §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release) |
| 7 | **分阶段升级 · 编排/事件流 · 数据层后续** | [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)（**按阶段执行**）· [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) · [ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)（**可落地改造全景**）· [MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)（**模块级对表**）· [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) · [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md) |
| 8 | **只读 API · 对外集成** | [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md) · [DOCKER.md](./DOCKER.md)（Compose、`Dockerfile.readonly-api`） |
| 8a | **脚本 vs 只读 API vs 组件：替换边界与升级建议** | [SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](./SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md) |
| 8b | **管理端管道 UI · 数据源迁移 · 自动拉取与沉淀分析** | [ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)（与 [ADMIN_WEB_CONSOLE_ROADMAP](./ADMIN_WEB_CONSOLE_ROADMAP.md) 对读） |
| 8c | **管理端控制台：框架总览与预期边界** | [ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md)（HTTP/bootstrap/UI/**未实现项** 对表；**[§7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** 七 **`mod-*`** 与顶栏一致 · **`#mod-api`→`#mod-analysis`**） |
| 9 | **内容草稿插槽（LLM/辅助）** | [scripts/draft/README.md](../scripts/draft/README.md) |

**读者路径**：叙事与 `make validate` 默认真源为根目录 MPA。**本地打开读者站**：根目录 **`make serve-reader`**（**http://127.0.0.1:8000/**）或 **`docker compose up`**（**8765**）；须 **http(s)**，勿 **`file://`** — 与根 **[README · 从这里开始](../README.md#readme-start-here)** · **[README.md](../README.md)** 文首及 **[DOCKER.md](./DOCKER.md)** §1 一致。阅读顺序、时间窗官方深链及「深链后仍看推演扩展 · 本轮提要」惯例见 [PLATFORM_CAPABILITY_MAP · §5](./PLATFORM_CAPABILITY_MAP.md#reading-order) 与 [SITE_REVIEW_THREE_PASSES · §3.6](./SITE_REVIEW_THREE_PASSES.md)。**枢纽记忆、站内 `docs/*.md` 在静态部署下的行为、发布前人工清单**见 [PLATFORM · §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release) 与 [SITE_REVIEW · 四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)。**站内 HTML 概念总览**（与分页叙事互补）：[evolvable-architecture.html](../evolvable-architecture.html)。

**持续集成（双轨）**：与 [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) §1「默认栈」一致。PR/推送时 [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) 的 **`validate`** 始终安装 **`requirements.txt` + `requirements-api.txt`** 并跑 **`run_validate.sh`**（根目录 MPA 为默认真源；含 **`test_readonly*.py`**）；**不**调用 **`run_validate_fast.sh`** / **`make validate-fast`**。**`spa-build`** 仅在变更触及 [PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md) 所述路径集合（含 `spa/`、`scripts/evolution-registry.json`、**`docs/schemas/evolution-registry.schema.json`**、**`scripts/validate_evolution_registry_schema.py`**、sync 输入等）时执行 **`make spa-build`**（会先 **`gen-nav-links`** + **`spa-sync`**），否则为 skipped。改根 **`*.html`** 若仅须 **`spa/public/`** 与 MPA 一致、未触发上列路径时，可本地单独 **`make spa-sync`**（见 [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map) · [系统边界](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)）。分支保护建议以 **`validate`** 为必选。若评估 Dagster/Prefect 或 Kafka 系，见同目录 **编排与事件流** 文档。

**本地子集**：**`make test`** = registry JSON Schema + 单测 + **`check_nav_links_registry`** + 沉淀/趋势 Schema；**不含** manifest 对账、顶栏、**`analysis_engine --check`** 等。**`make validate-fast`**（**`run_validate_fast.sh`**）介于 **`make test`** 与全量之间，**仍非** **`run_validate.sh`**；**仅**本地迭代，**CI 与 `.githooks/pre-commit` 不跑**。**合并前仍须** **`make validate`**（与 **`run_validate.sh`**、pre-commit、CI **validate** 一致）。合并前推荐 **`make merge-ready`**（**不含 `spa-build`**；另含 **`test-admin-console`**）或分步 **`make test-readonly-api`** / **`make test-admin-console`**（**`merge-ready`/`spa-build`/`spa-sync` 分工**见 [MERGE_AND_RELEASE_CHECKLIST · 第 1 节](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) 表 · [partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)）。详见 [CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd)、[AGENTS.md](../AGENTS.md#agents-pre-merge)。

**主链联动与验收入口 · 仓库物理分层**（下表各专篇文首多已互链）：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。

| 文档 | 用途 |
|------|------|
| [CONTRIBUTING.md](../CONTRIBUTING.md#maintainer-reading-order) | 参与贡献：环境、**`make validate`**（必）、**`make merge-ready`**（与 CI 对齐推荐）、**`make test`**（子集）、CI 双轨、注册表/SPA 自检与阅读顺序 |
| [AGENTS.md](../AGENTS.md#agents-contract) · [框架判型](../AGENTS.md#agents-content-framework) · [合并前](../AGENTS.md#agents-pre-merge) · [人审](../AGENTS.md#agents-invariants) · [管理端 IA](../AGENTS.md#agents-admin-console) · [双轨](../AGENTS.md#agents-dual-track) · [枢纽首屏](../AGENTS.md#agents-hub-lead) · [子集](../AGENTS.md#agents-test-subset) · [分析/HTML 边界](../AGENTS.md#agents-arch-boundary) · [读者惯例](../AGENTS.md#agents-reader-conventions) · [深读索引](../AGENTS.md#agents-deep-read) · [Cursor 规则](../AGENTS.md#agents-cursor-rules) | 自动化助手：合并前闸门、**`merge-ready`**、**`make test`** 快速子集、人审闸门、分析/展示边界、MPA+SPA 双轨 |
| [PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md) | **平台总览**：内容×架构×组件总表、[读者面/管理面速查 · 节 1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)、合并/增能/读站三条黄金路径、`make` 与文档入口怎么选 |
| [#front-back-modules · 前后台模块总览](#front-back-modules) | **读者面 × 管理面**按模块域一页表（与 USER_ADMIN §1a、PLATFORM §1a、MODULE §4 互补；防混读） |
| [#system-components-fusion · 组件与功能融合](#system-components-fusion) | **MPA / 总线 / hub / `readonly_api` / `admin-console` / `evolution_pkg` / CI** 一条表串主链；与 [ADMIN_CONSOLE · §2 拓扑](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-topology) 对读 |
| [PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md) | **整体架构图谱**：五维索引 + 总图 + 六域对表 + 升级入口 + 命令脊；**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)**；**[§1a 主链联动与验证](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** · **[§1b 仓库物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)** |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 仓库架构、数据流、内容生成边界、七类模块 |
| [ARCHITECTURE_ONE_PAGER.md](./ARCHITECTURE_ONE_PAGER.md) | 架构一页纸（**[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · **[不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index)** · 主链、闸门、双轨、版本线、侧车 DB、内容与呈现） |
| [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md) | **技术架构整理与升级路径**：简版 **§1—§4**（分层一览、阶段 0—3、优先级 backlog、验收命令）；**[详版附录](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)**（[别名 stub](./TECH_ARCHITECTURE_CAPABILITIES.md)） |
| [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) | Dagster/Prefect 与 Kafka/Redpanda：何时引入、与本站 Actions+JSON 栈的关系（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 技术·阶段 2/3） |
| [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md) | **数据存储后续架构**：OLTP、缓存、读副本、数仓、与 **Kafka Connect/CDC** 及编排状态库的分工；与 Git 真源边界（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 技术·数据层） |
| [spa/README.md](../spa/README.md) | 全站 React SPA（Vite、路由、iframe 承载分页、Pages 部署 base） |
| [PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md) | 平台四条支柱、MPA/SPA 双轨、`site_version` vs `run_id`、阅读顺序与增能检查单 |
| [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md) | **智能化目标架构**：六域协同；**导言「文首阅读顺序」**为 **进化/优化** → **持续分析优化** → **持续的优化** → **持续的升级** → **§2.2**；深链 **[进化与优化](./INTELLIGENCE_SIX_DOMAINS.md#evolution-and-optimization)** · **[持续分析优化](./INTELLIGENCE_SIX_DOMAINS.md#continuous-analysis-optimization)** · **[持续的优化](./INTELLIGENCE_SIX_DOMAINS.md#sustained-optimization)** · **[持续的升级](./INTELLIGENCE_SIX_DOMAINS.md#sustained-upgrade)** · **[§2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** |
| [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) | **扩展插槽、四条进化轨、阶段跑道、[智能化与自动化边界](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)、新增能力检查单**（最大可扩展落地） |
| [USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md) | **分端设计**：用户端 vs 管理端、数据源分类、进化/分析方法、审核分层（L0—L5）、规划矩阵；**[节 1a · 前端读者 · 后端管理](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)** |
| [ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md) | **管理端 Web 化**：登录（IdP/会话）、用户与 RBAC、审核与工作流、Git 真源与审计、运维安全、分阶段与反模式 |
| [ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md) | **`admin-console` 实现框架**：组件拓扑、bootstrap 字段、静态 `data/*.json`、UI 区块、阶段对表、**明确未实现**；单页分区与锚点 **[§7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**（**`#mod-api`→`#mod-analysis`**）；链入 §7/§7b 的入口表 **[§11a](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-doc-index)** |
| [MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) | **合并与发布一页清单**（`make merge-ready`、增能/四角色链；顶栏/`404` 手顺） |
| [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md) | **只读 HTTP API**：OpenAPI、路由、ETag、网关侧 CORS/鉴权 |
| [SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](./SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md) | **脚本 / API / 组件**：哪些适合只读 HTTP、哪些必须保留 CLI·闸门、包化与阶段升级顺序 |
| [REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md) | **舆情类 GitHub 参考引用**：模式映射本仓落点、侧车 vs 管道步骤、许可证/合规、与 **AI 解读层** 衔接；日常 ingest / 信源节奏见 **[INTEL](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)** |
| [DOCKER.md](./DOCKER.md) | **Docker 部署**：MPA / 开发挂载 / profile **`api`** / profile **`admin`**（**[§3a](./DOCKER.md#profile-admin)**）/ SPA 镜像 `Dockerfile.spa`、可选 **`docker-compose.kafka-dev.yml`**（**[§4a](./DOCKER.md#kafka-dev-overlay)**）、Makefile 快捷目标 |
| [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) | 整体适配不变量、分阶段升级建议、后续扩展面与反模式（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**） |
| [ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md) | **可落地升级路线图**：决策全景图、分域改造矩阵、分阶段执行卡、验收门禁（依据 UPGRADE / 六域 / ORCHESTRATION） |
| [MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md) | **模块全量梳理**：七类能力对表、`evolution_pkg`、脚本簇、呈现/管理端、阶段 0—3 **升级矩阵** |
| [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md) | **按阶段升级**：阶段 0—3 与 **2.5 数据层** 目标/准入/落地/验收 + 单迭代模板 |
| [INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md) | **增量构建与调试**：原则、组件引入顺序表、调试闭环、PR 切片；模板见 [templates/incremental-pr-slice.md](./templates/incremental-pr-slice.md) |
| [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) | 各 JSON / SQLite 字段职责、关联键、校验入口与可选分析栈；**[§5 · 侧车列速查](./DATA_CONTRACTS.md#sqlite-sidecar-column-inventory)**（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 技术·数据层） |
| [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md) | 全站读数总线、消费方登记、`SiteDataBus`、推荐流水线（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**）；**纯 CSS/HTML 枢纽版式**见 **[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**（不登记消费方）；与 **[内容驱动链](#content-driven-chain)**、**[DATA_ANALYSIS](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md)** 对读 |
| [DATA_ANALYSIS_SITE_CONTENT_SYNC.md](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md) | 数据与分析如何对齐分页模块、叙事 vs 动态块（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**）；**[内容驱动链](#content-driven-chain)** 总索引 |
| [SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md](./SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md) | 全站梳理后按纪律重推演与更新落点（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 推演） |
| [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)（[附录 · 详版能力地图](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities) · [别名 stub](./TECH_ARCHITECTURE_CAPABILITIES.md)） | 技术栈分层、已实现能力地图、进化能力含义（**正文在 BRIEF 附录**；旧文件名仅重定向）（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**） |
| [DEDUCTION_STRATEGY.md](./DEDUCTION_STRATEGY.md) | 认识论、单轮流程、偏误清单、与闭环对表（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 推演） |
| [RESEARCH_METHODS_MAP.md](./RESEARCH_METHODS_MAP.md) | 研究/推演方法与站内页、沙盘、JSON 管道匹配（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**） |
| [EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md) | 双周反哺节奏、`evolution-fast` 等运行说明 |
| [INTEL_AND_POLICY_TRACKING_PLAYBOOK.md](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md) | **舆情 / 制度 / 国情**：ingest 与 PR 闸门、信源分层、**[§2a 拉取约束](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)**（频率 · UA · 失败分类 · **`fetch_pacing`**）· **[§2b 微博/站内流](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**；与 [REFERENCE_DESIGN](./REFERENCE_DESIGN_OPINION_MONITORING.md) 分工（对标 vs 日常） |
| [AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md) | 可选 **AI 解读层**（`ai-analysis-overlay` 契约 · 只读 GET）；与 **[#ai-assisted-evolution](#ai-assisted-evolution)** · **[INTELLIGENCE · §8](./INTELLIGENCE_SIX_DOMAINS.md#ai-era-alignment)** · **主线 3b** 对读 |
| [SITE_REVIEW_THREE_PASSES.md](./SITE_REVIEW_THREE_PASSES.md) | 全站标题 · 图例 · TOC · 图形 · **§3.5 页头 lead/read-hint 分层**（与 [AGENTS · 枢纽首屏](../AGENTS.md#agents-hub-lead) 对读）· **§3.6 深链与本轮提要惯例** |
| [SYNTHESIS_SUBPAGES.md](./SYNTHESIS_SUBPAGES.md) | 综合推演主篇与子页（§1—§13）分工及锚点迁移 |
| [schemas/analysis-snapshot.schema.json](./schemas/analysis-snapshot.schema.json) | `analysis-snapshot.json` JSON Schema |
| [schemas/sediment.schema.json](./schemas/sediment.schema.json) | `data/sediment.json` JSON Schema |
| [schemas/sediment-trends.schema.json](./schemas/sediment-trends.schema.json) | `assets/sediment-trends.json` JSON Schema |
| [schemas/spa-nav-config.schema.json](./schemas/spa-nav-config.schema.json) | `spa/nav.config.json` JSON Schema |
| [schemas/README.md](./schemas/README.md) | **JSON Schema 索引**（契约扩展入口与各校验脚本对表） |
| [schemas/evolution-registry.schema.json](./schemas/evolution-registry.schema.json) | `scripts/evolution-registry.json` JSON Schema |
| [scripts/draft/README.md](../scripts/draft/README.md) | **内容草稿插槽**：机器辅助产出边界（PR 审阅；不写 manifest / 不接 `analysis_engine` 写 HTML） |
