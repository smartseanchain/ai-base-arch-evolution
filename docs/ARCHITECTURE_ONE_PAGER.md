# 架构一页纸

速查用；**五维总图**见 **[PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md)**。**内容·架构·组件与推荐调用顺序**（合并 / 增能 / 读站）见 **[PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)**。细节以 **[ARCHITECTURE.md](./ARCHITECTURE.md)**、**[DATA_CONTRACTS.md](./DATA_CONTRACTS.md)**、**[PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md)** 为准。

<a id="three-architectures"></a>

## 三架构对照（技术 · 内容 · 推演）

全站可拆成三条**正交**架构，升级时先分清改的是哪一条，再选 **[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md)** 的阶段 0—3。

| 架构 | 一句话 | 深读 |
|------|--------|------|
| **技术架构** | 静态 MPA（+ 可选 SPA 壳）+ Python 管道 + **Git 内 JSON** 契约 + **`make validate`**；SQLite / 只读 API / DuckDB 为侧车或可选工具；**服务器库、缓存、数仓、CDC** 见 **DATA_STORES**。**智能化**按 **六域协同**（数据 / 管道 / 分析 / 前端 / 运维 / 治理）规划，不单点堆脚本。 | [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md) · [TECH_ARCHITECTURE_CAPABILITIES.md · §1](./TECH_ARCHITECTURE_CAPABILITIES.md#stack) · [ARCHITECTURE.md · 七类模块](./ARCHITECTURE.md#seven-layers) · [DATA_CONTRACTS.md](./DATA_CONTRACTS.md)（字段/主键） · [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)（可选持久化与事件流衔接） · [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)（阶段 2/3 选型） |
| **内容架构** | **`.html` 为叙事真源**；**`evolution-registry.json`** 约束导航与对账；动态块只 **fetch** 已提交 JSON，**引擎不写正文**；`docs/*.md` 为仓库文档真源。 | 下文 **「内容与呈现」** · [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md) · [DATA_ANALYSIS_SITE_CONTENT_SYNC.md](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md) · **分端（前端读者 · 后端管理）**：[USER_ADMIN_SPLIT · 节 1a](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend) |
| **推演架构** | **定性脚手架**：认识论与单轮流程见 **DEDUCTION_STRATEGY**；与综合推演 **§2 判据**、沙盘、双周 **EVOLUTION_RUNBOOK** 对表；工程侧对应 **数据进化 / 规则闭环 / 叙事迭代** 三层（见 TECH_ARCHITECTURE §3）；全站一轮对表见 **SITE_WIDE_RERUN**。 | [DEDUCTION_STRATEGY.md](./DEDUCTION_STRATEGY.md) · [RESEARCH_METHODS_MAP.md](./RESEARCH_METHODS_MAP.md) · [TECH_ARCHITECTURE_CAPABILITIES.md · §3](./TECH_ARCHITECTURE_CAPABILITIES.md#evolution) · [EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md) · [SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md](./SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md) |

**升级建议（与升级文档对齐）**：**按阶段执行**见 **[PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)**。**可落地改造全景**（决策图 · 分域矩阵 · 阶段卡 · 验收）见 **[ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)**。**模块全量梳理与阶段升级矩阵**见 **[MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)**。**一页整理（分层 + 阶段 0—3 + backlog）**见 **[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)**。阶段 1 优先 **契约与 Schema**、**`evolution_pkg` 分包**、双轨与 **registry** 对账、**`readonly_api`** 扩只读端点；阶段 2/3 再议编排器与事件流 — 见 [ARCHITECTURE_UPGRADE · §2](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#upgrade-tiers) 与 [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)。**最大扩展性在不变量内的落地步骤**见 **[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**（含 **[智能化与自动化边界](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)**）。**智能化六域协同**（排期/PR 打点）见 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**。**合并 / 发布一页动线**见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md)**。

## 主链（数据）

`ingest` → **候选** `evolution-candidates.json` → **人审** → **manifest** `evolution-manifest.json` → **`analysis_engine`** → **`analysis-snapshot.json`** → 可选 **`--sediment`** → **`sediment.json`** + **`evolution.db`·`sediment_entry`** → **`sediment_trends.py`** → **`sediment-trends.json`**

- **勿自动写 manifest**；**引擎不写 HTML**（见根目录 **AGENTS.md**）。

## 闸门（合并前）

**`evolution-registry.json`**（单一注册表）+ **`check_manifest_drift`** + 各 validate + **`sync_site_nav --check`** + **SPA** **`check_nav_links_registry`** → **`make validate`**（**`run_validate.sh`**）。与 **CI `validate`** 中只读 API 子测对齐时，再执行 **`make test-readonly-api`**，或一次 **`make merge-ready`**（**`validate`** + **`test-readonly-api`** + **`test-admin-console`**）— 见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)**。

## 呈现（双轨）

| 形态 | 角色 |
|------|------|
| **MPA** | 根目录 **`.html`**；**CI 默认真源** |
| **SPA** | **`spa/`** 壳 + **`sync_spa_public`** 剥顶栏 HTML；**`nav.config.json` ↔ registry.pages** |

读数：**`site-data-bus.js`**（多页一条）+ **`analysis-hub`**（全量仪表盘）。

## 内容与呈现（读者层逻辑）

- **叙事真源**：根目录 **`.html`**（MPA）；**`analysis_engine` 不写 HTML**（引擎只产出 JSON 等结构化结果）。
- **首屏信息架构**：枢纽页 **`p.lead`** 尽量只保留一句定位；**三问导读、同读链、边界、数据侧**等放入 **`read-hint.page-head-deck`**，避免首屏单段过长 — 对照 **[SITE_REVIEW_THREE_PASSES.md](./SITE_REVIEW_THREE_PASSES.md)** §3.5。
- **节号 vs 短文案**：综合推演等**正文目录与交叉引用**保留 **§ 节号**；**路径条、分享摘要、总览三问链**等短文案优先用可读中文（与同文档 §3.5 一致）。
- **三色图例**：**`.nexus-tag` / `nexus-legend`** 类名可复用，**中文标签按页** — [ARCHITECTURE.md · 三色标签](./ARCHITECTURE.md#nexus-tag-labels)。
- **SPA**：**`nav.config.json` / `navLinks.ts` ≡ `evolution-registry.json`**；**`sync_spa_public`** 与 MPA 同源；**`make spa-build` 不替代 `make validate`**；改 **`index.html`** 总览后须 **`make spa-sync`**（见 [`spa/README.md`](../spa/README.md)）。
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

**[PLATFORM_CAPABILITY_MAP.md §6](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)** · 读者预期与发布前清单 **[§7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)** · **扩展性与进化落地 [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**（插槽、四轨、阶段跑道、**[新增能力检查单](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist)**）· **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md)**（`merge-ready`、发布轻量清单）

## 引入新组件（何时不必、何时再上）

- **默认足够**：定时/手动流水线用 **GitHub Actions**，事实与审计用 **Git + JSON**，合并前 **`make validate`**。低并发、以 PR 为节奏时，**不必**为「架构听起来先进」而引入编排器或消息队列 — 见 **[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)** 开篇。
- **优先阶段 1（无新基础设施）**：契约/`schema_version`、脚本迁入 **`evolution_pkg`**、MPA+SPA 与 registry 对账、**`readonly_api`** 只读扩端点 — 见 **[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md · 阶段 1](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#upgrade-tiers)**。
- **再评估编排器（Prefect / Dagster）**：出现**多条 DAG、分区回填、多环境参数矩阵、强运行历史 UI** 等多条信号时 — 同上文档 **§2.3** 与 ORCHESTRATION **§2**。
- **再评估事件流（Kafka / Redpanda）**：**多服务实时写、多订阅方、需回放**，且与 Git 主事实源分工明确时 — ORCHESTRATION **§3—§5**。
- **反模式备忘**：用 broker 或编排器**替代** Git PR 作唯一审计、或**自动写** `evolution-manifest.json` — **[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md §4](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#anti-patterns)**。
- **能力表与未实现方向速查**：[TECH_ARCHITECTURE_CAPABILITIES.md · §4](./TECH_ARCHITECTURE_CAPABILITIES.md#extend)。
