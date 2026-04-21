# 平台能力总览 · 阅读顺序 · 双轨呈现

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)。

本文把仓库当作**可演进推演平台**来梳理：**数据与闸门**、**分析与读数**、**叙事与路由**、**发布与运维**四条线各指哪里、如何增强。与 [ARCHITECTURE.md](./ARCHITECTURE.md)、[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md · 附录](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)（[别名](./TECH_ARCHITECTURE_CAPABILITIES.md)）互补——偏「一张图看清能力边界与入口」。

<a id="pillars"></a>

## 1. 四条能力支柱

| 支柱 | 你要的能力 | 主要入口 | 默认闸门 / 契约 |
|------|------------|----------|-----------------|
| **数据与真源** | 信号、候选、决策、规则可版本化、可对账 | `assets/evolution-manifest.json` 等 · [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) | `make validate`；**`evolution-registry.json`** + [`evolution-registry.schema.json`](./schemas/evolution-registry.schema.json) |
| **分析与时间** | 当日热力/提示/闭环缺口 + 跨日趋势 + 运行血缘 | `analysis_engine.py` · `analysis-hub.html` | `analysis-snapshot.schema.json`、`run.run_id` |
| **叙事与交互** | 多页推演、沙盘、综合推演矩阵、三问导读 | 根目录 `*.html` · `synthesis.html#continuation` | 人写正文；引擎不写 HTML |
| **呈现与路由** | 读者怎么进、维护者怎么发版 | **MPA**：`sync_site_nav.py`（**`maintainer-hub.html`** 在五链后再由 **`build_skip_bar`** 拼 **`#mh-spine-map` / `#mh-boundaries` / `#mh-reader-admin-matrix`**，勿手改；**`404.html`** 顶栏/skip **不在**写回列表，改 **`partials/`** 后须**手调**）；**SPA**：`spa/` + `sync_spa_public.py` | `site-meta.json`（发布线）；`make spa-build`（可选部署）；**`make sync-nav`** / **404** 见 [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) |

<a id="dual-surface"></a>

## 2. 呈现双轨（MPA + SPA）

| 形态 | 定位 | 构建 / 预览 | 与校验关系 |
|------|------|-------------|------------|
| **多页静态（MPA）** | 仓库根目录 HTML，**CI 与 `make validate` 的默认真源** | 任意静态服或 `python -m http.server` | `sync_site_nav --check`、registry 对账 |
| **全站 SPA** | React 壳 + iframe 加载**已剥顶栏**的同名 HTML，路由与 `evolution-registry.json` 对齐 | `cd spa && npm run dev` / `make spa-build` | **不替代** validate；增删注册页须同步 `spa/src/navLinks.ts`（见单测） |

部署上可二选一或分环境：**根目录**适合与现有 Pages 一致；**`spa/dist/`** 适合以 SPA 为唯一入口时整包上传。

<a id="release-lines"></a>

## 3. 两条「版本」线（勿混用）

| 概念 | 文件 / 字段 | 含义 |
|------|-------------|------|
| **站点发布线** | `assets/site-meta.json` · `site_version` | 人为宣告的产品/架构里程碑；顶栏 `v*` 来自总线拉取 |
| **分析运行线** | `analysis-snapshot.json` · `run.run_id` / `repo_revision` | 某次 `make analyze` 的计算血缘 |

PR/Issue 里写清引用的是 **site_version** 还是 **run_id**，避免对账混淆。

<a id="ops-tooling"></a>

## 4. 运维与增强工具（已实现）

| 能力 | 入口 |
|------|------|
| 流水线遥测 | `artifacts/pipeline-metrics-*.json`（`SKIP_PIPELINE_TELEMETRY=1` 可关） |
| 快照 PR 差分 | `python3 scripts/diff_analysis_snapshot.py` |
| 状态一行扫 | `make status`（含 site-meta + 快照摘要） |
| 可选 DuckDB | `query_evolution_duckdb.py` + `requirements-analytics.txt` |
| 可选只读 API | `readonly_api.py`：`/snapshot`、`/trends`、`/manifest`、**/registry**、**/sediment**、**/candidates**（敏感）、**/hint-decisions**（宜受控）、**/hint-rules**、**/maps-to-hints**、**/ingest-config**（RSS 源·宜受控）、**/site-meta**、**/site-search-index**（可选索引·无文件 **404**）（**ETag** + **revalidate**；**If-None-Match** → **304**；历史 JSON **no-store**；**`/sediment`** 无文件时 **404**）；集成说明见 **[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)** |
| 合并前本地推荐 | **`make merge-ready`**（**`make validate`** + **`make test-readonly-api`** + **`make test-admin-console`**）；动线见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**；改 **`admin-console/`** 时对表 **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** |
| CI 双轨 | `ci.yml`：**validate**（MPA 默认真源）+ **spa-build**（按路径过滤跑 `make spa-build`，含 **`scripts/evolution-registry.json`**、**`docs/schemas/evolution-registry.schema.json`**、**`validate_evolution_registry_schema.py`**；无关提交跳过） |
| 编排/消息队列选型 | [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) |
| 数据层后续（服务器库 · 缓存 · 数仓 · CDC） | [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md) |
| 舆情类开源（仅参考；GPL/爬虫自负） | [REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md)（侧车或可选管道步骤；与 **[AI_ASSISTED_ANALYSIS_LAYER](./AI_ASSISTED_ANALYSIS_LAYER.md)** 衔接） |

<a id="reading-order"></a>

## 5. 推荐阅读顺序

若要把**内容、架构分层、主要组件**与推荐 **`make` / 文档入口**收在**一页总表**里，先读 **[PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)**（三条黄金路径 + 低收益调用清单），再回到本节按角色下钻。

**整体内容框架（真源分层）**与判型入口合一见 **[docs/README · #content-framework](./README.md#content-framework)**（再进 **#quick-paths**）；**读者面 × 管理面按模块一页表**见 **[#front-back-modules](./README.md#front-back-modules)**；**系统组件与功能一条表**见 **[#system-components-fusion](./README.md#system-components-fusion)**。

**新读者（读站）**  
1. [index.html#read-guide](../index.html#read-guide) 读站指路（三条并行入口）与 [三问导读](../index.html#three-questions) → [nexus.html](../nexus.html) 或 [modules-map.html](../modules-map.html)  
2. [synthesis.html#criteria](../synthesis.html#criteria) 判据 → [synthesis.html#continuation](../synthesis.html#continuation) 继续推演矩阵  
3. 按需下钻分页；**时间窗**可先 [历史 · 五代横轴](../timeline.html#timeline-five-eras)、[廿年 · 对照总表](../past-future.html#past-future-comparison)、[十年 · 六维总表](../decade.html#decade-six-dim) / [阶段条](../decade.html#decade-phase-bars)（深链落节后仍建议扫一眼该页「推演扩展 · 本轮提要」）。分析向 [analysis-hub.html#panorama](../analysis-hub.html#panorama)

**维护者（改站 / 管道）**  
- **零步（可选）**：[PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)（总表 · 合并 / 增能 / 读站调用顺序）  
- **整框（推荐先扫）**：[docs/README · 整体内容框架](./README.md#content-framework)（叙事 / JSON / `docs` / 闸门 / 双轨 / 管理面边界）· **[前后台模块总览](./README.md#front-back-modules)** · **[组件与功能融合](./README.md#system-components-fusion)**  
0. **[docs/README.md · 文档主线表](./README.md#docs-spine)**（整理速览；与下列条目一致）  
0c. **[docs/README · 常见改动最短链](./README.md#quick-paths)**（判型后再下钻；与主线表 **0c** 同锚；registry 三件套 · [MODULE · §1a](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#seven-class-pkg-quick)）  
0d. **[docs/README · AI 与自动进化](./README.md#ai-assisted-evolution)**（overlay · 黄金集 · 草稿插槽 · 管道节奏；**非**自动写 manifest）· [INTELLIGENCE · §8](./INTELLIGENCE_SIX_DOMAINS.md#ai-era-alignment)  
0.1. [CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd) 环境与合并前底线（**`make validate`**（必）、**`make merge-ready`**（与 CI 对齐推荐）、CI 双轨、常见自检表）· [MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)  
0.2. [PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md) **五维整体架构图谱**（数据 · 内容 · 演进 · 方法论 · 运行态；**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)**；**[§1a 主链联动与验证](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** · **[§1b 仓库物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**；总索引后再下钻专篇）  
0.3. [INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md) **增量构建与调试**（提前接组件、**[PR 切片模板](./templates/incremental-pr-slice.md)**）· [ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md) 可落地升级全景  
0.5. [ARCHITECTURE_ONE_PAGER.md](./ARCHITECTURE_ONE_PAGER.md) 架构一页纸（**[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 主链 / 闸门 / 双轨 / 侧车 / 内容与呈现）；**扩展性与进化落地** [§8](./PLATFORM_CAPABILITY_MAP.md#extensibility) · [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)  
1. [ARCHITECTURE.md](./ARCHITECTURE.md) 数据流 + 适应度函数  
2. [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) 字段与主键 · [schemas/README.md](./schemas/README.md)  
3. [DATA_ANALYSIS_SITE_CONTENT_SYNC.md](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md)（数据/分析 → 模块 / 叙事 / 动态块边界）· [EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md) 双周节奏 · [INTEL · §2—2a](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)（ingest 信源/频率）· [§2b](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)（微博/站内流）· [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md) 总线（**纯 CSS/HTML 枢纽版式**与 **[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** 分列，非消费方表）；收束叙述见 **[docs/README · 内容驱动链](./README.md#content-driven-chain)**  
4. [scripts/README.md](../scripts/README.md) 命令表 · `make validate` 为合并前底线  
5. CI 双轨（**validate** / **spa-build**）：根目录 [README.md](../README.md)（**持续集成** 一节）· [docs/README 文首](./README.md) · 只读 API 集成 [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)

**架构升级 / 对外说明**  
0. [ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)（**可落地升级路线图**：决策全景 · 分域矩阵 · 阶段执行卡 · 验收门禁）  
0.1. [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)（**简版 §1—§4**：技术架构整理 + 阶段 0—3 + 优先级 backlog）· **[附录 · 详版能力地图等](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)**（[别名](./TECH_ARCHITECTURE_CAPABILITIES.md)）  
1. [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md)（适配原则 · 分阶段升级 · 扩展矩阵）  
2. 本文 §1—§4 · [DEDUCTION_STRATEGY.md](./DEDUCTION_STRATEGY.md) 认识论边界

<a id="enhance-checklist"></a>

## 6. 能力提升检查单（自助）

增能力时建议逐项自问，避免 silent 漂移：

- [ ] **架构 / 基础设施向改造**（编排器、Kafka、生产级数据库等）：是否在 **[PHASED_UPGRADE_EXECUTION_GUIDE](./PHASED_UPGRADE_EXECUTION_GUIDE.md)** 中标明**当前阶段**与**准入**，并优先走完 **[ROADMAP · §1 决策图](./ARCHITECTURE_UPGRADE_ROADMAP.md#upgrade-panorama)**？**阶段 1 未吃透前**避免并行立项 **2/3** 与 **[DATA_STORES](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)** 重投入。  
- [ ] 新分页是否写入 **`evolution-registry.json`**（结构符合 **Schema**；**`make test`** / **`make validate`** 均含 **`validate_evolution_registry_schema.py`**）且通过 **`check_manifest_drift`**（仅 **`make validate`** / pre-commit）？  
- [ ] 顶栏是否只改 **`partials/site-nav.inc.html`** 后 **`make sync-nav`**？  
- [ ] **`maintainer-hub.html`** 五链后的三条页内 skip 是否**仅**由 **`build_skip_bar`**（**`sync_site_nav.py`**）生成、**未**在 HTML 手改？（见 **[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**）  
- [ ] 若影响 SPA：是否更新 **`spa/nav.config.json`** 并已 **`make gen-nav-links`**（或 **`spa-build`**），且 **`check_nav_links_registry.py`** 通过（已含于 **`make validate`** / **`make test`**）？（若 PR 触发了 CI **`spa-build`**，该 job 须绿）
- [ ] **仅改 `evolution-registry.json` 的 `pages`/`lab_factors`（未删 HTML）**：是否已按 **sync-nav → nav.config 与 `pages` 对齐 → gen-nav-links 或 spa-build → validate** 三件套收束（与 **[CONTRIBUTING · 常见变更自检](../CONTRIBUTING.md#contributing-common-changes-checklist)** 表及 **[PROJECT · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** 对读）？  
- [ ] 若改 **`partials/skip-bar.inc.html`** 或 **SPA 壳**（**`SpaLayout` / `spaRouteMeta` / `LegacyFrame`**）：快捷链前五链顺序一致（含 **`#reader-next`** 常见下一站）；总览 **`#read-guide`** 等 hash 的 **标题 / 读屏 / iframe `title`** 成对更新？**`404.html`** 不在 **`sync_site_nav`** 范围内，其 skip-bar / 导读是否已手调对齐（**`make validate`** 含 **`check_skip_bar_404.py`**）？  
- [ ] 若改快照结构：是否递增 **`schema_version`** 并同步 **Schema + 校验脚本**？  
- [ ] 对外里程碑：是否递增 **`site-meta.json`** 的 **`site_version`** 与 **`summary`**？  
- [ ] **仅**改 **`assets/site.css`** 或根 **`.html` 版式骨架**（**[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** 所列模块）：是否按该节约束组合，**未**误增总线消费方或虚构 **`[data-site-data-live]`** 登记？  
- [ ] **持续分析优化**：是否已对照 **[DATA_ANALYSIS_SITE_CONTENT_SYNC](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md)**、**[DATA_CONTRACTS](./DATA_CONTRACTS.md)** 与 **[INTELLIGENCE · 闭环](./INTELLIGENCE_SIX_DOMAINS.md#continuous-analysis-optimization)** 判明本轮是契约/分析侧还是版式/文档侧（必要时拆 PR）？  
- [ ] **跨层改动**：是否已对照 **[PROJECT · §1b 仓库物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)** 确认本轮触及的目录层（MPA / `assets` / `scripts` / `evolution_pkg` / `spa` / `admin-console` / `docs`），避免单层 PR 夹带多层的隐式依赖？若含 **`admin-console`**，UI 分区见 **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**。

<a id="reader-and-release"></a>

## 7. 读者预期与发布前复查（摘要）

**若迷路**：新读者先 [index.html · 读站指路](../index.html#read-guide) 或 [判型入口 · 我是来…](../index.html#index-intent-pick)；整理文档结构或判型改哪一篇 → [docs/README · 文档主线表](../docs/README.md#docs-spine) · [常见改动最短链 0c](../docs/README.md#quick-paths)；维护者闸门与分端入口 → [maintainer-hub.html](../maintainer-hub.html)（[关系视图 · 本页 ↔ 注册表 ↔ 锚点](../maintainer-hub.html#mh-spine-map) · [系统边界速查](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)）。

**部署一页检**：线上 404 / 空白 → 核对 GitHub **Settings → Pages** 源分支与发布目录；**全站 SPA（项目子路径）** → [spa/README · GitHub Pages](../spa/README.md#spa-github-pages) 内 **`VITE_BASE`** 与 `npm run build` 示例须与仓库名一致；**本地** → 根目录 **`make serve-reader`** / Docker，勿 **`file://`**（与下条「本地读者站」对读）。

- **顶栏分组 vs 站内搜索**：**分组顶栏 `<details>`** 负责「按主题找分页」；**顶栏检索**（`data-site-quick-search` + **`assets/site-search-index.json`** 存在时）负责「按关键词定位页面/片段」。二者互补，不必记全分组；深链仍以各页 **`#anchor`** 为准（见 [SITE_REVIEW · hub 卡](../SITE_REVIEW_THREE_PASSES.md) 与根 `index` 枢纽）。
- **枢纽页首屏模块顺序**（默认）：**`h1`** → **`lead`** → **`read-hint`** → 路径条 → **`toc--pilot`** → 读数条；**例外**见 [AGENTS · 枢纽首屏](../AGENTS.md#agents-hub-lead)。
- **枢纽记忆**（不必死记顶栏全链）：**总览** → **立体联结** 或 **模块图谱** → **综合推演** → **分析引擎** → **沙盘工坊**；细节与三条并行入口见 [index.html · 读站指路](../index.html#read-guide)。  
- **枢纽页 CSS 模块**（导读栈、pill 目录、命令卡分栏等，**非** JSON 总线）：[INTELLIGENCE_SIX_DOMAINS · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)。  
- **正文地标**：根目录读者页以 **`<main id="main">`** 包住 **`</header>` 之后、`<footer>` 之前**的主体（与 skip **`#main`**、**`site-data-bus.js`** 回顶链一致，**每页仅一个 `<main>`**）— [ARCHITECTURE_ONE_PAGER · 内容与呈现](./ARCHITECTURE_ONE_PAGER.md#content-presentation) · [SITE_REVIEW · §3.5](./SITE_REVIEW_THREE_PASSES.md#section-3-5-lead-readhint)。  
- **`docs/*.md` 在静态站**：根目录部署下点击 **`docs/… .md`** 多为浏览器打开**源码/下载**，与 GitHub 网页渲染不同；详见 [SITE_REVIEW_THREE_PASSES · 四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)。  
- **本地读者站 MPA（须 http(s)，勿 `file://`）**：根目录 **`make serve-reader`** → **http://127.0.0.1:8000/**；或 **`docker compose`** / **`docker-compose.dev.yml`** 映射 **8765**（见根 **[README.md](../README.md)** · **[DOCKER.md](./DOCKER.md)** §1）。  
- **合并或大版本发布**：除 **`make validate`** 外，建议过一遍 [SITE_REVIEW_THREE_PASSES · 发布前轻量清单](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)（顶栏抽样、窄屏、总线版本、`.md` 链、可选 SPA）。  
- **自动化助手收束**（与上条对读）：[AGENTS.md · 合并前](../AGENTS.md#agents-pre-merge) · [枢纽首屏](../AGENTS.md#agents-hub-lead) · [MPA+SPA 双轨](../AGENTS.md#agents-dual-track)。  
- **顶栏分组 / 文档 HTML 化**：属产品定稿后的结构改版，**当前仓库不强制**；定稿前仍以注册表全链 + 分区速跳为准。

<a id="extensibility"></a>

## 8. 扩展性与平台进化（最大可扩展落地）

**插槽、四条进化轨、阶段 0—3 跑道、[产品/工程习惯](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#platform-habits)、[智能化与自动化边界](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)、新增能力合并前检查单、反模式**见专篇 **[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**。**智能化从单点脚本到六域协同**（数据 / 管道 / 分析 / 前端 / 运维 / 治理）见 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**（**[§2.2 读者面版式](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**）。**用户端/管理端分面、数据源与审核分层**见 **[USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)**（**[节 1a · 前端读者 · 后端管理](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)**）；**与总表对读**：[PLATFORM_MASTER_MAP · 读者面/管理面 · 节 1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)；**按模块域一页表**：[docs/README · #front-back-modules](./README.md#front-back-modules) · **[#system-components-fusion](./README.md#system-components-fusion)**。若规划**带登录的管理 Web**（认证、用户、审核流），见 **[ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md)**。**合并/发布动线**见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**；**JSON Schema 索引**见 **[docs/schemas/README.md](./schemas/README.md)**。与 [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) 阶段描述同读。

---

*与仓库主分支同步；大改呈现双轨或注册表时请更新本节。*
