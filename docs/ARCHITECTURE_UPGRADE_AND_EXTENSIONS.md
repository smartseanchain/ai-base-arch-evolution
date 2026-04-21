# 整体适配 · 架构升级建议 · 后续扩展

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)。

本文与 [PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md)（能力边界与检查单）、[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)（编排与消息队列分阶段）对齐，回答三件事：**当前栈如何「整体适配」**、**升级按什么顺序做**、**可预期的扩展面在哪里**。定性路线图，非采购清单。**可落地改造全景**（决策图、分域矩阵、阶段执行卡、验收门禁）：**[ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)**。**技术栈分层 + 升级路径一页收束**（可先读）：**[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)**（简版 **§1—§4**；**[详版附录](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)** · [别名](./TECH_ARCHITECTURE_CAPABILITIES.md)）。**技术 / 内容 / 推演** 分层与升级落点对照：**[ARCHITECTURE_ONE_PAGER · 三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**。**在不变量内最大化扩展性、插槽与进化跑道**的落地专篇：**[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（主线 **0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。**呈现双轨（`spa-sync` / `spa-build`）**：[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map)。**MPA 顶栏与失页**：**`partials/`** → **`make sync-nav`**；**`404.html`** 手调（`sync_site_nav` 不写回）— **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

<a id="adaptation"></a>

## 1. 整体适配原则（不变量）

下列约定是「适配」的锚点：新能力应**挂接**在这些不变量上，而不是绕开它们。

| 不变量 | 含义 | 适配时自检 |
|--------|------|------------|
| **Git JSON 为真源** | `assets/*.json`、规则与注册表可 diff、可 `make validate` | 新数据源若不入库，须明确是「附件/缓存」还是「第二真源」 |
| **单一注册表** | `evolution-registry.json` 约束页面与沙盘因子 | 增删页 → registry →（若用 SPA）`navLinks.ts` → 单测 |
| **人审闸门** | manifest 合并、决策 JSON 可追溯 | 任何自动化不得默认覆盖已审 `evolution-manifest.json` |
| **双轨呈现** | MPA 为 validate 默认；SPA 为可选壳 | CI 仍以根目录为准；SPA 可另 job 或手动发布 |
| **两条版本线** | `site_version`（发布）≠ `run_id`（分析运行） | 对外说明、Issue/PR 引用时写清是哪条线 |
| **分析不写 HTML** | `analysis-snapshot.json` 只读消费 | 叙事与版式仍在 `.html`；模型/草稿走独立插槽（见 [ARCHITECTURE.md](./ARCHITECTURE.md) §七类能力） |

**小结**：适配 = 新组件声明自己落在**数据 / 闸门 / 分析 / 展示**哪一层，并复用已有契约与脚本入口，避免 silent 漂移。更完整的平台分工（含**管道 / 运维 / 治理**与 PR 打点）见 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**。

<a id="upgrade-tiers"></a>

## 2. 架构升级建议（分阶段）

按**收益 / 风险 / 运维负担**排序；不必跳级。**按阶段落地打勾、验收与迭代模板**（执行向）：**[PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)**。

### 2.1 阶段 0 — 维持默认栈（推荐长期基线）

- **调度**：GitHub Actions + `scripts/run_validate.sh` + `evolution_pkg.pipeline`（含可选遥测）。
- **事实与审计**：PR、合并前 `make validate`、artifact 下载后人工合并。
- **适用**：低并发、以仓库为日志、团队无专职数据平台。

### 2.2 阶段 1 — 站内增强（低成本、高收益）

在**不引入新基础设施**前提下可做的升级：

| 方向 | 建议 | 参考 |
|------|------|------|
| **契约与文档** | 快照/沉淀大改时递增 `schema_version`，同步 Schema 与校验脚本 | [DATA_CONTRACTS.md](./DATA_CONTRACTS.md)、`analysis-snapshot.schema.json` |
| **脚本分包** | 将平铺 `scripts/*.py` 按域迁入 `evolution_pkg` 子模块，保持 `evolution_io` 兼容层 | [ARCHITECTURE.md](./ARCHITECTURE.md) 适应度函数表 |
| **双轨一致** | 任何 registry 变更同步 SPA；CI 中 **`spa-build` job** 在触及 `spa/`、**`scripts/evolution-registry.json`**、sync 输入（根 `*.html`、`assets/`、`docs/`、`partials/` 等）时跑 **`make spa-build`**，否则跳过（**validate** 始终运行） | [PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md) §2、§4、§6 |
| **可观测性** | 沿用 `artifacts/pipeline-metrics-*.json`、`make status`；需要时再对接告警 | [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) |
| **只读 API** | 扩展端点时仍只读磁盘 JSON，不写 manifest | `readonly_api.py` |

**已并入 `run_validate.sh` 的落地**（阶段 1 相关）：**`evolution-registry.schema.json`** + **`validate_evolution_registry_schema.py`**；**`spa-nav-config.schema.json`** + **`gen_nav_links_ts.py`** / **`check_nav_links_registry.py`**；**`sediment*.schema.json`** + **`validate_sediment_artifacts_schema.py`**；单测 **`test_spa_nav_schema`** 覆盖 nav.config Schema。大改结构时递增 **`schema_version`** 并改对应 Schema。

### 2.3 阶段 2 — 编排器试点（中成本）

当出现**多条 DAG、回填、多环境参数矩阵、需要运行历史 UI** 等多条信号时，再评估 **Prefect** 或 **Dagster** 封装现有 Python 步骤；**仍不**用编排器直接写 manifest。细节与对照表见 [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) §2、§4 阶段 B。

### 2.4 阶段 3 — 事件流（高门槛）

仅在**多服务实时写入、多订阅方回放、与 Git 审计链明确分工**时考虑 **Kafka / Redpanda**；禁止用 broker 替代 Git 作主事实源。见 [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) §3—§5。

### 2.5 数据库与查询层（可选，与阶段 2/3 正交）

**当前**：**Git JSON** 为契约真源；**`data/evolution.db`**（SQLite）为**可重建侧车**；可选 **DuckDB** 做报表（见 [DATA_CONTRACTS.md · §5](./DATA_CONTRACTS.md#存储策略哪些适合写入数据库与架构预期对齐)）。

**后续**仅在出现例如 **多用户会话与审计**、**只读 API 水平扩展**、**运营工作流状态机**、**OLAP/CDC** 等**明确信号**时，再引入 **PostgreSQL 等 OLTP**、**缓存**、**读副本投影**、**数仓**；并与 **[ORCHESTRATION](./ORCHESTRATION_AND_EVENT_STREAMING.md)** 中的 **Kafka Connect / CDC** 设计对齐。**原则**：库与主题承载**运营态与派生数据**，**不**替代 **manifest/注册表** 的 Git 闸门。

**整体组件表、推荐落地顺序、mermaid 总图与反模式**：[DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)。

<a id="extensions"></a>

## 3. 后续扩展面（按域）

便于排期时对照「改谁、验什么」。

| 域 | 可扩展内容 | 闸门 / 注意 |
|----|------------|-------------|
| **内容与叙事** | 新分页、综合推演子页、synthesis 锚点 | registry、sitemap、`sync_site_nav`（**`404.html`** 顶栏/skip **手维护**）；正文仍人写 |
| **数据与 ingest** | 新源、新 `maps_to` 键、配方扩展 | `validate-evolution-candidates`、drift、merge 闸门 |
| **分析与沉淀** | 新规则、新统计块、趋势新维度 | `analysis_engine --check`、快照 Schema、import 与 trends 消费方 |
| **展示与总线** | 新 `data-site-data-live` 占位、总线新 loader | [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md) 消费方登记 |
| **SPA** | 新路由、壳内体验（非改 iframe 内 HTML 结构） | `navLinks` 与 registry 单测；`sync_spa_public` 剥壳约定 |
| **API 与集成** | 更多只读端点、ETL 下游只读副本 | CORS、缓存策略；仍不写库内 JSON |
| **管理端与集成** | **`admin-console/`** 占位、同源代理只读 API、**`merge-ready`** 含管理端烟测 | **[ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md)**；**不写 manifest**；部署见 **[DOCKER.md](./DOCKER.md#profile-admin)** |
| **分析栈可选** | DuckDB 报表、diff 脚本增强 | `requirements-analytics.txt` 可选安装 |
| **持久化与查询（服务器级）** | OLTP、缓存、读副本、数仓、与 **Kafka CDC** 分工 | **[DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)**；**不**以库为 manifest 唯一真源 |
| **平台与合规** | 密钥、多环境配置、审计导出 | 不与「无人审写 manifest」冲突 |

<a id="anti-patterns"></a>

## 4. 反模式（与编排文档一致）

- 用消息队列或编排器**替代** Git PR 流程作为**唯一**审计源。
- 引擎或外部服务**直接写入** `evolution-manifest.json`（绕过 `review_state`）。
- 为「架构听起来先进」**同时**上编排器 + Kafka，而业务仍单日单管道。

<a id="reading"></a>

## 5. 延伸阅读

- **可落地升级路线图**：[ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)
- **五维整体架构图谱（总索引）**：[PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md)（**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)**；**[§1a 主链联动与验证](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** · **[§1b 仓库物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**）
- **技术栈整理与升级路径**：[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)（简版 **§1—§4**；**[详版附录](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)** · [旧链别名](./TECH_ARCHITECTURE_CAPABILITIES.md)）
- 维护者**文档主线表**：[docs/README · 文档主线](./README.md#docs-spine)
- 新贡献者入门：[CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd) · Agent 速查：[AGENTS.md](../AGENTS.md#agents-contract) · [框架判型](../AGENTS.md#agents-content-framework)
- CI 双轨摘要：[docs/README 文首](./README.md)
- 用户端/管理端分面与审核分层：[USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)
- 能力总览与检查单：[PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md)
- 数据流与适应度函数：[ARCHITECTURE.md](./ARCHITECTURE.md)
- 技术分层与已实现能力：[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md · 附录](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)（[别名](./TECH_ARCHITECTURE_CAPABILITIES.md)）
- 编排与事件流分阶段：[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)
- 数据存储组件与后续架构（库 · 缓存 · 数仓 · CDC）：[DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)
- 模块全量梳理与阶段升级矩阵：[MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)
- 按阶段升级执行指南：[PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)
- 字段与主键：[DATA_CONTRACTS.md](./DATA_CONTRACTS.md)
- 扩展插槽与新增能力检查单：[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)
- 合并与发布一页清单：[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)
- 只读 API 集成：[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)
- Schema 文件索引：[docs/schemas/README.md](./schemas/README.md)

---

*随主分支演进；重大变更默认栈或引入新基础设施时，应同步更新本节阶段描述与交叉链接。*
