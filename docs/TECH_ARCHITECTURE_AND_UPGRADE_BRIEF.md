# 技术架构整理与升级路径（简版）

**一页收束**：当前**技术栈如何分层**、**主数据链**、**闸门**是什么；**按阶段可怎么升级**、**何时不必跳级**。若优先需要**内容×组件×命令**总表与**合并/增能/读站**三条路径，先读 **[PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)**。**可落地改造全景**（决策图、分域矩阵、阶段卡、验收）：**[ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)**。**增量构建与调试**（组件引入序、闭环、PR 切片）：**[INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md)**。**五维整体索引**（数据 · 内容 · 演进 · 方法论 · 运行态）：**[PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md)**。细节与完整表仍以 **[TECH_ARCHITECTURE_CAPABILITIES.md](./TECH_ARCHITECTURE_CAPABILITIES.md)**（分层 · 能力地图 · 可扩展方向）、**[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md)**（不变量 · 阶段 0—3 · 扩展矩阵 · 反模式）、**[ARCHITECTURE.md](./ARCHITECTURE.md)**（数据流 · 七类模块）为准。三架构并列速览：**[ARCHITECTURE_ONE_PAGER · 三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**。**智能化目标架构（六域协同）**见 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**。

<a id="layers-summary"></a>

## 1. 技术架构整理（分层一览）

| 层 | 要点 |
|----|------|
| **呈现** | **MPA**：根目录 `.html` + `partials/`（`sync_site_nav`）；**CI / `make validate` 默认真源**。**SPA**：`spa/` + `sync_spa_public` 剥壳 iframe；**`nav.config` ≡ registry.pages**。 |
| **客户端** | 原生 JS：`fetch` 已提交 JSON；总线 **`site-data-bus.js`**；分析/闭环/沙盘脚本分工见 [SITE_DATA_UPDATE_FRAMEWORK](./SITE_DATA_UPDATE_FRAMEWORK.md)。 |
| **数据契约** | **Git 内 JSON** 可 diff、可 Schema 校验；**单一注册表** **`scripts/evolution-registry.json`** 约束页面与 `lab_factors`。 |
| **侧车** | **`data/evolution.db`**（可选本地）：沉淀加速、快照历史；**不**替代 Git 内 HEAD 闸门。 |
| **管道** | **Python**：`scripts/*.py` + **`evolution_pkg`**（`io`、`pipeline`、`spa_nav`、`sediment_validate` 等）；抓取 → 人审 merge → 分析 → 沉淀 → 趋势。 |
| **校验与 CI** | **`run_validate.sh`** / **`make validate`**；**`make merge-ready`** 另含 **`test-readonly-api`** 与 **`test-admin-console`**（见 [MERGE_AND_RELEASE_CHECKLIST](./MERGE_AND_RELEASE_CHECKLIST.md)）。**`ci.yml`**：**validate** 必跑；**admin-console-tests** / **spa-build** 按路径过滤。 |

**主链（技术视角）**：`ingest` → **候选** → **人审** → **manifest** → **`analysis_engine`** → **快照** →（可选）**沉淀** → **趋势** → 前端 **fetch**。**分析引擎不写 HTML**；**manifest 不默认自动 merge**。

**关系示意**（与 [TECH_ARCHITECTURE · mermaid](./TECH_ARCHITECTURE_CAPABILITIES.md#stack) 一致）：浏览器 ← JSON ← 仓库；Actions 跑校验与 artifact，**默认不**替代人工合并主分支。

<a id="upgrade-ladder"></a>

## 2. 可升级建议（分阶段决策）

按 **收益 / 风险 / 运维负担** 排序；**不必跳级**。完整论证与反模式见 [ARCHITECTURE_UPGRADE](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#upgrade-tiers)。**按阶段落地打勾**见 **[PHASED_UPGRADE_EXECUTION_GUIDE](./PHASED_UPGRADE_EXECUTION_GUIDE.md)**。

| 阶段 | 定位 | 建议动作（摘要） | 何时维持不动 |
|------|------|------------------|----------------|
| **0** | **长期基线** | GitHub Actions + **`make validate`** + artifact **人工合并**；`evolution_pkg.pipeline` 遥测可选 | 单仓库节奏、无专职数据平台、低并发 |
| **1** | **站内增强（优先）** | **契约**：`schema_version` + `docs/schemas/` + `run_validate.sh`；**分包**：平铺脚本迁入 **`evolution_pkg`**；**双轨**：registry ↔ SPA ↔ 单测；**只读 API** 扩端点（仍不写 manifest）；**可观测**：`pipeline-metrics`、`make status` | 在引入任何编排器 **之前** 尽量先做完本阶段 |
| **2** | **编排器** | 仅当多条 **DAG**、**分区回填**、**多环境参数矩阵**、**运行历史 UI** 等**多条信号**齐备时，用 **Prefect / Dagster** **封装已有** Python 步骤；**编排器不写 manifest** | 仍是一条 Actions 管道、团队能靠 PR + artifact 协作 → **不必上** |
| **3** | **事件流** | 仅 **多服务实时写**、**多订阅**、**回放** 且与 **Git 审计链分工明确** 时考虑 **Kafka / Redpanda**；**禁止** broker **替代 Git** 作唯一事实源 | 单体会 + 静态 JSON 足够 → **不上** |

**数据层（与上表正交）**：当前 **Git JSON + SQLite 侧车 + 可选 DuckDB** 见 [DATA_CONTRACTS · §5](./DATA_CONTRACTS.md#存储策略哪些适合写入数据库与架构预期对齐)。**服务器级 OLTP、缓存、读副本、数仓及与 Connect/CDC 的衔接**见 **[DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)**——可与阶段 **2/3** 并行规划，**落地顺序**按该文「推荐落地顺序」与 **[INCREMENTAL_BUILD_PLAYBOOK](./INCREMENTAL_BUILD_PLAYBOOK.md)** 分解。

<a id="priority-backlog"></a>

## 3. 升级优先级 backlog（与「可扩展方向」对表）

摘自 [TECH_ARCHITECTURE_CAPABILITIES · §4](./TECH_ARCHITECTURE_CAPABILITIES.md#extend)，按**默认推荐顺序**重排（非采购清单）：

1. **阶段 1 内**：**脚本分包**（余下 `scripts/*.py` → `evolution_pkg`）；**契约与 Schema** 随功能递增 **`schema_version`**。  
2. **低成本增强**：**实时告警**（ingest 失败 Webhook）；**只读 API** / **DuckDB** 报表（可选依赖，见 [DATA_CONTRACTS](./DATA_CONTRACTS.md)）。  
3. **产品与合规向**：**多环境 `ingest_config`**（文档与矩阵同步）；**草稿插槽**（**[scripts/draft/README.md](../scripts/draft/README.md)**），**不**自动写 manifest。  
4. **默认避免**：**全自动 artifact push main**（削弱人审）；**无信号上编排器 + 消息队列**（反模式见 [ARCHITECTURE_UPGRADE · §4](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#anti-patterns)）。  
5. **阶段 2/3**：严格按 §2 表「信号齐备」再评估；细节 **[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)**。

**扩展性落地**（插槽、四轨、检查单）：**[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**。**六域协同打点**（PR/排期）：**[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md#pr-checklist)**。

<a id="verify-after-upgrade"></a>

## 4. 升级后如何验收（不变）

| 动作 | 命令或文档 |
|------|------------|
| 全闸门 | **`make validate`** |
| 合并前本地推荐 | **`make merge-ready`**（见 [MERGE_AND_RELEASE_CHECKLIST](./MERGE_AND_RELEASE_CHECKLIST.md)） |
| 触 SPA / registry / sync | **`make spa-build`**（若 CI 会跑该 job） |
| 增能回归 | [PLATFORM_CAPABILITY_MAP §6](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist) · [PLATFORM_EXTENSIBILITY 检查单](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist) |

---

## 延伸阅读

- **文档主线表**：[docs/README · #docs-spine](./README.md#docs-spine)  
- **平台四条支柱与运维工具**：[PLATFORM_CAPABILITY_MAP §1—§4](./PLATFORM_CAPABILITY_MAP.md#pillars)  
- **编排与 Kafka 对照**：[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)
- **数据库与后续数据架构**：[DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)
- **模块全量梳理与升级矩阵**：[MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)
- **按阶段升级执行指南**：[PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)

*与主分支同步；默认栈或阶段定义变更时，请同步更新本文与 [ARCHITECTURE_UPGRADE](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md)。*
