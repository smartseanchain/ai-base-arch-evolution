# 架构一页纸

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [总览 MPA · 四条动线卡](../index.html#index-intent-pick) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**读站顺序（含步骤 0）**：[PLATFORM_CAPABILITY_MAP · §5](./PLATFORM_CAPABILITY_MAP.md#reading-order)。**架构师五步表**：[#architect-stewardship](#architect-stewardship)（同页 §）· [#architect-invariants-index](#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

速查用；**五维总图**见 **[PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md)**（**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)**；**[§1a 主链联动与验证](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** · **[§1b 仓库物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**）。**内容·架构·组件与推荐调用顺序**（合并 / 增能 / 读站）见 **[PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)**。细节以 **[ARCHITECTURE.md](./ARCHITECTURE.md)**、**[DATA_CONTRACTS.md](./DATA_CONTRACTS.md)**、**[PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md)** 为准。**五维 / 六域 / 七类**：**五维** = PROJECT 索引维度；**六域** = **[INTELLIGENCE](./INTELLIGENCE_SIX_DOMAINS.md)** 协同与 PR 打点；**七类** = **[ARCHITECTURE · 七类](./ARCHITECTURE.md#seven-layers)** — 不同粒度，**勿**在 PR 描述里混用为同一套词。**整体内容框架**见 **[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**判型最短链**（**0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。

<a id="architect-invariants-index"></a>

## 架构红线（不变量索引）

新人**约五分钟**：下表为合并与扩展时**不可口头绕过**的五条；细则仍以各专篇为准。

| 红线 | 一句话 | 权威落点 |
|------|--------|----------|
| **勿自动写已审 manifest** | 候选须经人审再合并 | [AGENTS · 人审闸门](../AGENTS.md#agents-invariants) · [MERGE · 合并前](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) |
| **引擎不写 HTML** | **`analysis_engine`** / **`analysis_pipeline`** 只产出 JSON 等结构化结果 | [AGENTS · 架构边界](../AGENTS.md#agents-arch-boundary) · [内容与呈现](#content-presentation) |
| **合并闸门仅此一套** | **`run_validate.sh`** = **`make validate`** ≈ CI **validate** / pre-commit | [ARCHITECTURE · validate 分界](./ARCHITECTURE.md#run-validate-gate) · [MERGE](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) |
| **敏感只读路由默认勿对公网裸开** | **`/candidates`** 等待审；**`/ingest-config`** 等或暴露运营侧重点 | [INTEGRATION · 网关建议](./INTEGRATION_AND_READONLY_API.md#gateway-default-deny-sensitive) · [DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes) |
| **ingest 不做登录态/热搜时间线** | 默认可自动化路径为 **RSS / `json_feeds`** 低频 GET | [INTEL · §2a](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers) · [§2b](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms) |

**新管道核心逻辑**：优先进 **`scripts/evolution_pkg/`**，**`scripts/*.py`** 保持薄 CLI — [scripts/README · 收束队列](../scripts/README.md#pkg-migrate-queue) · [PROJECT · 物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)。

---

<a id="architect-stewardship"></a>

## 架构师视角：梳理与持续改进

用**不变量 + 真源分层 + 闸门**收束每次演进，避免专篇越长、口头边界越漂。与 **[PLATFORM_MASTER_MAP](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)**（总表与黄金路径）互补：后者回答「怎么调用」，本节回答「先判哪类架构债、再落到哪份真源」。

| 顺序 | 关注点 | 权威落点 |
|------|--------|----------|
| **1. 定粒度** | PR/设计里**五维 / 六域 / 七类**择一写清，勿混称 | [勿混粒度 · PROJECT](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain) · [CONTRIBUTING · 术语](../CONTRIBUTING.md#contributing-terminology) |
| **2. 定真源** | 改动落在契约 JSON、`evolution_pkg`、MPA、SPA、管理壳哪一层 | [PROJECT · §1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout) · [DATA_CONTRACTS](./DATA_CONTRACTS.md) |
| **3. 过闸门** | 合入依据以全量校验为准；子集不得冒充 CI | **`make validate`** · [ARCHITECTURE · run_validate](./ARCHITECTURE.md#run-validate-gate) · [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) |
| **4. 控演进** | 新能力先进检查单与增量切片，再议编排器/重库 | [PLATFORM_EXTENSIBILITY · 检查单](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist) · [INCREMENTAL_BUILD](./INCREMENTAL_BUILD_PLAYBOOK.md) · [PHASED_UPGRADE](./PHASED_UPGRADE_EXECUTION_GUIDE.md) |
| **5. 对节奏** | 候选 / manifest / 分析 / 沉淀与人审周历 | [EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md) · [AGENTS · 人审闸门](../AGENTS.md#agents-invariants) |

---

<a id="three-architectures"></a>

## 三架构对照（技术 · 内容 · 推演）

全站可拆成三条**正交**架构，升级时先分清改的是哪一条，再选 **[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md)** 的阶段 0—3。

| 架构 | 一句话 | 深读 |
|------|--------|------|
| **技术架构** | 静态 MPA（+ 可选 SPA 壳）+ Python 管道 + **Git 内 JSON** 契约 + **`make validate`**；SQLite / 只读 API / DuckDB 为侧车或可选工具；**服务器库、缓存、数仓、CDC** 见 **DATA_STORES**。**智能化**按 **六域协同**（数据 / 管道 / 分析 / 前端 / 运维 / 治理）规划，不单点堆脚本。 | [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)（**[§2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**）· [TECH_BRIEF · 附录 1](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-stack) · [ARCHITECTURE.md · 七类模块](./ARCHITECTURE.md#seven-layers) · [DATA_CONTRACTS.md](./DATA_CONTRACTS.md)（字段/主键） · [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)（可选持久化与事件流衔接） · [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)（阶段 2/3 选型） |
| **内容架构** | **`.html` 为叙事真源**；**`evolution-registry.json`** 约束导航与对账；动态块只 **fetch** 已提交 JSON，**引擎不写正文**；`docs/*.md` 为仓库文档真源。 | **[「内容与呈现」](#content-presentation)** · [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md) · [DATA_ANALYSIS_SITE_CONTENT_SYNC.md](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md) · **分端（前端读者 · 后端管理）**：[USER_ADMIN_SPLIT · 节 1a](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend) · [docs/README · #front-back-modules](./README.md#front-back-modules) · [docs/README · #system-components-fusion](./README.md#system-components-fusion) |
| **推演架构** | **定性脚手架**：认识论与单轮流程见 **DEDUCTION_STRATEGY**；与综合推演 **§2 判据**、沙盘、双周 **EVOLUTION_RUNBOOK** 对表；工程侧对应 **数据进化 / 规则闭环 / 叙事迭代** 三层（见 **[TECH_BRIEF · 附录 3](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-evolution)**）；全站一轮对表见 **SITE_WIDE_RERUN**。 | [DEDUCTION_STRATEGY.md](./DEDUCTION_STRATEGY.md) · [RESEARCH_METHODS_MAP.md](./RESEARCH_METHODS_MAP.md) · [TECH_BRIEF · 附录 3](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-evolution) · [EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md) · [SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md](./SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md) |

**升级建议（与升级文档对齐）**：**按阶段执行**见 **[PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)**。**可落地改造全景**（决策图 · 分域矩阵 · 阶段卡 · 验收）见 **[ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)**。**模块全量梳理与阶段升级矩阵**见 **[MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)**。**一页整理（分层 + 阶段 0—3 + backlog）**见 **[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)**（简版 **§1—§4**）；**[详版附录 · 分层详表与能力地图](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)**（[旧文件名别名](./TECH_ARCHITECTURE_CAPABILITIES.md)）。阶段 1 优先 **契约与 Schema**、**`evolution_pkg` 分包**、双轨与 **registry** 对账、**`readonly_api`** 扩只读端点；阶段 2/3 再议编排器与事件流 — 见 [ARCHITECTURE_UPGRADE · §2](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#upgrade-tiers) 与 [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)。**最大扩展性在不变量内的落地步骤**见 **[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**（含 **[智能化与自动化边界](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)**）。**智能化六域协同**（排期/PR 打点）见 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**（**[§2.2 读者面版式](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**）。**合并 / 发布一页动线**见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**。

## 主链（数据）

`ingest` → **候选** `evolution-candidates.json` → **人审** → **manifest** `evolution-manifest.json` → **`analysis_engine`** → **`analysis-snapshot.json`** → 可选 **`--sediment`** → **`sediment.json`** + **`evolution.db`·`sediment_entry`** → **`sediment_trends.py`** → **`sediment-trends.json`**

- **勿自动写 manifest**；**引擎不写 HTML**（见根目录 **[AGENTS.md · 人审闸门](../AGENTS.md#agents-invariants)** · **[架构边界](../AGENTS.md#agents-arch-boundary)**）。

## 闸门（合并前）

**`evolution-registry.json`**（单一注册表）+ **`check_manifest_drift`** + 各 validate + **`sync_site_nav --check`**（**`maintainer-hub.html`** 五链后三页内锚由 **`build_skip_bar`** 生成，勿手改 HTML；**`404.html`** 顶栏/skip **不在**写回范围，改 **`partials/`** 后须**手调** — **[scripts/README · `sync_site_nav`](../scripts/README.md)**）+ **SPA** **`check_nav_links_registry`** → **`make validate`**（**`run_validate.sh`**）。**`make validate-fast`** 仅本地子集，**不**进 CI/pre-commit（**[ARCHITECTURE#run-validate-gate](./ARCHITECTURE.md#run-validate-gate)**）。与 **CI `validate`** 中只读 API 子测对齐时，再执行 **`make test-readonly-api`**，或一次 **`make merge-ready`**（**`validate`** + **`test-readonly-api`** + **`test-admin-console`**）— 见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**。动 **`admin-console/`** 时单页 **`mod-*`** 与 **`#mod-api`→`#mod-analysis`** 见 **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**。

## 呈现（双轨）

| 形态 | 角色 |
|------|------|
| **MPA** | 根目录 **`.html`**；**CI 默认真源** |
| **SPA** | **`spa/`** 壳 + **`sync_spa_public`** 剥顶栏 HTML；**`nav.config.json` ↔ registry.pages** |

读数：**`site-data-bus.js`**（多页一条）+ **`analysis-hub`**（全量仪表盘）。

<a id="content-presentation"></a>

## 内容与呈现（读者层逻辑）

- **叙事真源**：根目录 **`.html`**（MPA）；**`analysis_engine` 不写 HTML**（引擎只产出 JSON 等结构化结果）。
- **正文地标**：读者页以 **`<main id="main">`** 包裹 **`</header>` 之后、`<footer>` 之前**的主体内容（与 skip-bar **`#main`**、**`site-data-bus.js`** 回顶注入一致）；**每页仅一个 `<main>`**。
- **首屏信息架构**：枢纽页 **`p.lead`** 尽量只保留一句定位；**三问导读、同读链、边界、数据侧**等放入 **`read-hint.page-head-deck`**，避免首屏单段过长 — 对照 **[SITE_REVIEW_THREE_PASSES.md](./SITE_REVIEW_THREE_PASSES.md)** §3.5 · **[AGENTS.md · 枢纽首屏](../AGENTS.md#agents-hub-lead)**。**流程条 / 推演扩展卡 / 三色图例成组、pill 目录与命令卡栅格** 等 **CSS 复用类**见 **[INTELLIGENCE_SIX_DOMAINS · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**（与 `site-data-bus` 并行）。
- **总览四条动线与五簇锚句**：**`index.html`** 的 **`#index-intent-pick`** 与 **[README · 产品视角](../README.md#pm-four-journeys)** 对表；五簇读者枢纽可在 **`lead`** 与 **`read-hint`** 之间加 **`p.muted.hub-cluster-thread`** 一行簇内承诺 — 仍只按 **[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**，**不**冒充 **`[data-site-data-live]`** 新消费方。
- **节号 vs 短文案**：综合推演等**正文目录与交叉引用**保留 **§ 节号**；**路径条、分享摘要、总览三问链**等短文案优先用可读中文（与同文档 §3.5 一致）。
- **三色图例**：**`.nexus-tag` / `nexus-legend`** 类名可复用，**中文标签按页** — [ARCHITECTURE.md · 三色标签](./ARCHITECTURE.md#nexus-tag-labels)。
- **SPA**：**`nav.config.json` / `navLinks.ts` ≡ `evolution-registry.json`**；**`sync_spa_public`** 与 MPA 同源；**`make spa-build` 不替代 `make validate`**；改根目录任意 **`.html`**（读站指路、多页页脚、**`analysis-hub`** 导读等）后若维护 **SPA**，须 **`make spa-sync`**（见 [`spa/README.md`](../spa/README.md) · [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)）。**维护者收束**：[关系视图](../maintainer-hub.html#mh-spine-map)（枢纽页 ↔ 注册表 ↔ 文档锚点）· [系统边界](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)。
- **读者预期与发布复查**：枢纽记忆、站内 **`docs/*.md`** 在静态根部署下的表现、**`make validate`** 之外的轻量清单 — [PLATFORM_CAPABILITY_MAP · §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)、[SITE_REVIEW · 四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)。

## 两条版本线（勿混）

| 线 | 字段 |
|----|------|
| **分析血缘** | **`run.run_id`** / **`run.repo_revision`**（快照） |
| **发布宣告** | **`site-meta.json` · `site_version`** |

## 侧车 SQLite（`data/evolution.db`）

| 表 | 作用 |
|----|------|
| **`sediment_entry`** | 与 **`sediment.json`** 双写 |
| **`analysis_snapshot_history`** | 按 **`run_id`** 追加快照 JSON；**不**替代 Git 内 HEAD 快照闸门 |

可删库重跑分析重建；见 **[EVOLUTION_RUNBOOK.md · 本地 SQLite](./EVOLUTION_RUNBOOK.md#sqlite-sidecar)**。

## 包与入口

- **`scripts/evolution_pkg/`**：**`io`**、**`pipeline`**、**`nav_links`**、**`spa_nav`**、**`sediment_validate`**、**`analysis_snapshot_history`**（快照历史只读封装 → **`sqlite_store`**）
- **只读 API**：**`readonly_api.py`**（含 **`/snapshot-history`**）

## 增能检查单

**[PLATFORM_CAPABILITY_MAP.md §6](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)** · 读者预期与发布前清单 **[§7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)** · **扩展性与进化落地 [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**（插槽、四轨、阶段跑道、**[新增能力检查单](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist)**）· **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**（`merge-ready`、发布轻量清单）

## 引入新组件（何时不必、何时再上）

- **默认足够**：定时/手动流水线用 **GitHub Actions**，事实与审计用 **Git + JSON**，合并前 **`make validate`**。低并发、以 PR 为节奏时，**不必**为「架构听起来先进」而引入编排器或消息队列 — 见 **[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)** 开篇。
- **优先阶段 1（无新基础设施）**：契约/`schema_version`、脚本迁入 **`evolution_pkg`**、MPA+SPA 与 registry 对账、**`readonly_api`** 只读扩端点 — 见 **[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md · 阶段 1](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#upgrade-tiers)**。
- **再评估编排器（Prefect / Dagster）**：出现**多条 DAG、分区回填、多环境参数矩阵、强运行历史 UI** 等多条信号时 — 同上文档 **§2.3** 与 ORCHESTRATION **§2**。
- **再评估事件流（Kafka / Redpanda）**：**多服务实时写、多订阅方、需回放**，且与 Git 主事实源分工明确时 — ORCHESTRATION **§3—§5**。
- **反模式备忘**：用 broker 或编排器**替代** Git PR 作唯一审计、或**自动写** `evolution-manifest.json` — **[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md §4](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#anti-patterns)**。
- **能力表与未实现方向速查**：[TECH_BRIEF · 附录 4](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-extend)。
