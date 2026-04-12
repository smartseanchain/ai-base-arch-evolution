# 文档索引

站内 Markdown 说明与 Schema 入口（与根目录 [README.md](../README.md) 中的运行说明互补）。**新贡献者**：先读根目录 [CONTRIBUTING.md](../CONTRIBUTING.md)，再按下表深入。**Cursor**： [.cursor/rules/repo-gates.mdc](../.cursor/rules/repo-gates.mdc)（始终）；**`spa/nav.config.json`** → [spa-nav-config.mdc](../.cursor/rules/spa-nav-config.mdc)；**`spa/src/**`** → [spa-nav-registry.mdc](../.cursor/rules/spa-nav-registry.mdc)；**`scripts/evolution-registry.json`** → [evolution-registry.mdc](../.cursor/rules/evolution-registry.mdc)（与 [AGENTS.md](../AGENTS.md) 一致）。

<a id="docs-spine"></a>

## 文档主线（整理速览）

维护、改版或对外说明时，建议按下面**顺序扫一遍**（各步链到 canonical 文档；与 [PLATFORM_CAPABILITY_MAP · §5 维护者](./PLATFORM_CAPABILITY_MAP.md#reading-order) 一致并互为补充）：

| 顺序 | 主题 | 主文档 |
|------|------|--------|
| 0 | **合并闸门与 CI 对齐** | **`make validate`**（必）· 推荐 **`make merge-ready`** — [MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md)、[CONTRIBUTING.md](../CONTRIBUTING.md) |
| 0a | **平台总览：内容·架构·组件与合理调用** | [PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)（总表 · [读者面/管理面速查 · 节 1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces) · 三条黄金路径 · 文档入口选择） |
| 0b | **五维整体架构图谱（总索引）** | [PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md)（数据 · 内容 · 演进 · 方法论 · 运行态） |
| 1 | **三架构一页对照** | [ARCHITECTURE_ONE_PAGER.md](./ARCHITECTURE_ONE_PAGER.md#three-architectures) |
| 1a | **技术架构整理 + 升级路径（简版）** | [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)（分层 · 阶段 0—3 · 优先级 backlog） |
| 1b | **模块全量梳理与架构升级矩阵** | [MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)（七类 × 脚本簇 × `evolution_pkg` × 阶段 0—3） |
| 1c | **按阶段升级（执行指南）** | [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)（**[落地执行 · 可复制命令](./PHASED_UPGRADE_EXECUTION_GUIDE.md#execution-now)** · 阶段 0→1→2/3 · 正交 2.5 数据层 · 验收与迭代模板） |
| 2 | **扩展插槽 · 进化轨 · 智能化边界 · 六域协同 · 读者/管理分拆 · 管理 Web 路线图** | [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md) · [USER_ADMIN_SPLIT · 节 1a · 前端/后端](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend) · [ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md) · [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) · [PLATFORM_CAPABILITY_MAP §8](./PLATFORM_CAPABILITY_MAP.md#extensibility) · [分端设计全文](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md) |
| 3 | **数据流与字段主键** | [ARCHITECTURE.md](./ARCHITECTURE.md) · [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) · [schemas/README.md](./schemas/README.md) |
| 3a | **SQLite 侧车列速查 · 不宜主库域 · 服务器库与 CDC 排期** | [DATA_CONTRACTS · §5 速查](./DATA_CONTRACTS.md#sqlite-sidecar-column-inventory) · [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md) |
| 3b | **方法论分析 + 可选 AI 解读层（配置接入）** | [AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md) · [examples/ai_analysis_overlay.example.json](./examples/ai_analysis_overlay.example.json) |
| 3c | **舆情类开源系统：参考引用设计（侧车/管道边界）** | [REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md)（与 **3b**、**8a**、**ARCHITECTURE** 对读） |
| 4 | **命令与管道节奏** | [scripts/README.md](../scripts/README.md) · [EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md) |
| 4a | **增量构建 · 提前接组件 · 调试闭环** | [INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md) · [templates/incremental-pr-slice.md](./templates/incremental-pr-slice.md) |
| 5 | **总线 · 读数消费方** | [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md) |
| 6 | **呈现 · 读者预期 · 发布复查** | [SITE_REVIEW_THREE_PASSES.md](./SITE_REVIEW_THREE_PASSES.md) · [PLATFORM_CAPABILITY_MAP §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release) |
| 7 | **分阶段升级 · 编排/事件流 · 数据层后续** | [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)（**按阶段执行**）· [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) · [ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)（**可落地改造全景**）· [MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)（**模块级对表**）· [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) · [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md) |
| 8 | **只读 API · 对外集成** | [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md) · [DOCKER.md](./DOCKER.md)（Compose、`Dockerfile.readonly-api`） |
| 8a | **脚本 vs 只读 API vs 组件：替换边界与升级建议** | [SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](./SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md) |
| 8b | **管理端管道 UI · 数据源迁移 · 自动拉取与沉淀分析** | [ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)（与 [ADMIN_WEB_CONSOLE_ROADMAP](./ADMIN_WEB_CONSOLE_ROADMAP.md) 对读） |
| 8c | **管理端控制台：框架总览与预期边界** | [ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md)（HTTP/bootstrap/UI/**未实现项** 对表） |
| 9 | **内容草稿插槽（LLM/辅助）** | [scripts/draft/README.md](../scripts/draft/README.md) |

**读者路径**：叙事与 `make validate` 默认真源为根目录 MPA。阅读顺序、时间窗官方深链及「深链后仍看推演扩展 · 本轮提要」惯例见 [PLATFORM_CAPABILITY_MAP · §5](./PLATFORM_CAPABILITY_MAP.md#reading-order) 与 [SITE_REVIEW_THREE_PASSES · §3.6](./SITE_REVIEW_THREE_PASSES.md)。**枢纽记忆、站内 `docs/*.md` 在静态部署下的行为、发布前人工清单**见 [PLATFORM · §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release) 与 [SITE_REVIEW · 四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)。**站内 HTML 概念总览**（与分页叙事互补）：[evolvable-architecture.html](../evolvable-architecture.html)。

**持续集成（双轨）**：与 [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) §1「默认栈」一致。PR/推送时 [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) 的 **`validate`** 始终安装 **`requirements.txt` + `requirements-api.txt`** 并跑 `run_validate.sh`（根目录 MPA 为默认真源；含 **`test_readonly*.py`**）；**`spa-build`** 仅在变更触及 [PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md) 所述路径集合（含 `spa/`、`scripts/evolution-registry.json`、**`docs/schemas/evolution-registry.schema.json`**、**`scripts/validate_evolution_registry_schema.py`**、sync 输入等）时执行 **`make spa-build`**，否则为 skipped。分支保护建议以 **`validate`** 为必选。若评估 Dagster/Prefect 或 Kafka 系，见同目录 **编排与事件流** 文档。

**本地子集**：**`make test`** = registry JSON Schema + 单测 + **`check_nav_links_registry`** + 沉淀/趋势 Schema；**不含** manifest 对账、顶栏、**`analysis_engine --check`** 等。**合并前仍须** **`make validate`**（与 **`run_validate.sh`**、pre-commit、CI **validate** 一致）。合并前推荐 **`make merge-ready`**（另含 **`test-admin-console`**）或分步 **`make test-readonly-api`** / **`make test-admin-console`**（见 [MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md)）。详见 [CONTRIBUTING.md](../CONTRIBUTING.md)、[AGENTS.md](../AGENTS.md)。

| 文档 | 用途 |
|------|------|
| [CONTRIBUTING.md](../CONTRIBUTING.md) | 参与贡献：环境、**`make validate`**（必）、**`make merge-ready`**（与 CI 对齐推荐）、**`make test`**（子集）、CI 双轨、注册表/SPA 自检与阅读顺序 |
| [AGENTS.md](../AGENTS.md) | 自动化助手：合并前闸门、**`merge-ready`**、**`make test`** 快速子集、人审闸门、分析/展示边界、MPA+SPA 双轨 |
| [PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md) | **平台总览**：内容×架构×组件总表、[读者面/管理面速查 · 节 1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)、合并/增能/读站三条黄金路径、`make` 与文档入口怎么选 |
| [PROJECT_ARCHITECTURE_OVERVIEW.md](./PROJECT_ARCHITECTURE_OVERVIEW.md) | **整体架构图谱**：五维索引 + 总图 + 六域对表 + 升级入口 + 命令脊 |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 仓库架构、数据流、内容生成边界、七类模块 |
| [ARCHITECTURE_ONE_PAGER.md](./ARCHITECTURE_ONE_PAGER.md) | 架构一页纸（**[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 主链、闸门、双轨、版本线、侧车 DB、内容与呈现） |
| [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md) | **技术架构整理与升级路径（简版）**：分层一览、阶段 0—3、优先级 backlog、验收命令 |
| [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md) | Dagster/Prefect 与 Kafka/Redpanda：何时引入、与本站 Actions+JSON 栈的关系（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 技术·阶段 2/3） |
| [DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md) | **数据存储后续架构**：OLTP、缓存、读副本、数仓、与 **Kafka Connect/CDC** 及编排状态库的分工；与 Git 真源边界（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 技术·数据层） |
| [spa/README.md](../spa/README.md) | 全站 React SPA（Vite、路由、iframe 承载分页、Pages 部署 base） |
| [PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md) | 平台四条支柱、MPA/SPA 双轨、`site_version` vs `run_id`、阅读顺序与增能检查单 |
| [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md) | **智能化目标架构**：数据 / 管道 / 分析 / 前端 / 运维 / 治理六域协同；与七类模块、插槽、PR 自检对表 |
| [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) | **扩展插槽、四条进化轨、阶段跑道、[智能化与自动化边界](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)、新增能力检查单**（最大可扩展落地） |
| [USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md) | **分端设计**：用户端 vs 管理端、数据源分类、进化/分析方法、审核分层（L0—L5）、规划矩阵；**[节 1a · 前端读者 · 后端管理](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)** |
| [ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md) | **管理端 Web 化**：登录（IdP/会话）、用户与 RBAC、审核与工作流、Git 真源与审计、运维安全、分阶段与反模式 |
| [ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md) | **`admin-console` 实现框架**：组件拓扑、bootstrap 字段、静态 `data/*.json`、UI 区块、阶段对表、**明确未实现** |
| [MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md) | **合并与发布一页清单**（`make merge-ready`、增能/四角色链） |
| [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md) | **只读 HTTP API**：OpenAPI、路由、ETag、网关侧 CORS/鉴权 |
| [SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](./SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md) | **脚本 / API / 组件**：哪些适合只读 HTTP、哪些必须保留 CLI·闸门、包化与阶段升级顺序 |
| [REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md) | **舆情类 GitHub 参考引用**：模式映射本仓落点、侧车 vs 管道步骤、许可证/合规、与 **AI 解读层** 衔接 |
| [DOCKER.md](./DOCKER.md) | **Docker 部署**：MPA / 开发挂载 / profile **`api`** / profile **`admin`**（**[§3a](./DOCKER.md#profile-admin)**）/ SPA 镜像 `Dockerfile.spa`、可选 **`docker-compose.kafka-dev.yml`**（**[§4a](./DOCKER.md#kafka-dev-overlay)**）、Makefile 快捷目标 |
| [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) | 整体适配不变量、分阶段升级建议、后续扩展面与反模式（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**） |
| [ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md) | **可落地升级路线图**：决策全景图、分域改造矩阵、分阶段执行卡、验收门禁（依据 UPGRADE / 六域 / ORCHESTRATION） |
| [MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md) | **模块全量梳理**：七类能力对表、`evolution_pkg`、脚本簇、呈现/管理端、阶段 0—3 **升级矩阵** |
| [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md) | **按阶段升级**：阶段 0—3 与 **2.5 数据层** 目标/准入/落地/验收 + 单迭代模板 |
| [INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md) | **增量构建与调试**：原则、组件引入顺序表、调试闭环、PR 切片；模板见 [templates/incremental-pr-slice.md](./templates/incremental-pr-slice.md) |
| [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) | 各 JSON / SQLite 字段职责、关联键、校验入口与可选分析栈；**[§5 · 侧车列速查](./DATA_CONTRACTS.md#sqlite-sidecar-column-inventory)**（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 技术·数据层） |
| [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md) | 全站读数总线、消费方登记、`SiteDataBus`、推荐流水线（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**） |
| [DATA_ANALYSIS_SITE_CONTENT_SYNC.md](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md) | 数据与分析如何对齐分页模块、叙事 vs 动态块（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**） |
| [SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md](./SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md) | 全站梳理后按纪律重推演与更新落点（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 推演） |
| [TECH_ARCHITECTURE_CAPABILITIES.md](./TECH_ARCHITECTURE_CAPABILITIES.md) | 技术栈分层、已实现能力地图、进化能力含义（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**） |
| [DEDUCTION_STRATEGY.md](./DEDUCTION_STRATEGY.md) | 认识论、单轮流程、偏误清单、与闭环对表（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)** · 推演） |
| [RESEARCH_METHODS_MAP.md](./RESEARCH_METHODS_MAP.md) | 研究/推演方法与站内页、沙盘、JSON 管道匹配（文首链 **[三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**） |
| [EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md) | 双周反哺节奏、`evolution-fast` 等运行说明 |
| [SITE_REVIEW_THREE_PASSES.md](./SITE_REVIEW_THREE_PASSES.md) | 全站标题 · 图例 · TOC · 图形 · **§3.5 页头 lead/read-hint 分层** · **§3.6 深链与本轮提要惯例** |
| [SYNTHESIS_SUBPAGES.md](./SYNTHESIS_SUBPAGES.md) | 综合推演主篇与子页（§1—§13）分工及锚点迁移 |
| [schemas/analysis-snapshot.schema.json](./schemas/analysis-snapshot.schema.json) | `analysis-snapshot.json` JSON Schema |
| [schemas/sediment.schema.json](./schemas/sediment.schema.json) | `data/sediment.json` JSON Schema |
| [schemas/sediment-trends.schema.json](./schemas/sediment-trends.schema.json) | `assets/sediment-trends.json` JSON Schema |
| [schemas/spa-nav-config.schema.json](./schemas/spa-nav-config.schema.json) | `spa/nav.config.json` JSON Schema |
| [schemas/README.md](./schemas/README.md) | **JSON Schema 索引**（契约扩展入口与各校验脚本对表） |
| [schemas/evolution-registry.schema.json](./schemas/evolution-registry.schema.json) | `scripts/evolution-registry.json` JSON Schema |
| [scripts/draft/README.md](../scripts/draft/README.md) | **内容草稿插槽**：机器辅助产出边界（PR 审阅；不写 manifest / 不接 `analysis_engine` 写 HTML） |
