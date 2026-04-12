# 合并与发布检查单（一页汇总）

本文把分散在多篇文档里的**合并前工程步骤**与**大版本发布习惯**收成一条动线，避免漏项；与 **[CONTRIBUTING.md](../CONTRIBUTING.md)**、**[PLATFORM_CAPABILITY_MAP · §6—§7](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)**、**[SITE_REVIEW_THREE_PASSES · 四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)** 一致，**不替代**其中细节。

**智能化与可演进自动化**在本仓库的含义：契约校验、管道步骤、规则 JSON、只读 API、定时 ingest/分析 artifact 等——在 **[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md · §1.1](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)** 所述**不变量**内演进；**不**包含默认自动覆盖已审 **`evolution-manifest.json`**。目标架构按 **六域协同**（数据 / 管道 / 分析 / 前端 / 运维 / 治理）打点，见 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**。

<a id="pre-merge"></a>

## 1. 合并 PR 前（维护者 / 工程）

| 步骤 | 命令或文档 |
|------|------------|
| 全闸门（与 pre-commit、CI **`validate`** 一致） | **`make validate`** |
| 只读 API + 管理端烟测（本地未单装 **fastapi** 时 **`make validate`** 会 **skip** **`test_readonly*.py`**） | **`make merge-ready`**（= 上一步 + **`make test-readonly-api`**（**`test_readonly*.py`**：HTTP **304** + **`READONLY_PROXY_SEGMENTS`** 对账）+ **`make test-admin-console`**）或分步执行后两者 |
| 变更触及 **SPA** / **registry** / **sync 输入** 等且 CI 会跑 **spa-build** 时 | **`make spa-build`**（见 **[docs/README 文首](./README.md)** 路径说明） |
| 增能自检 | [PLATFORM_CAPABILITY_MAP · §6](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)、[PLATFORM_EXTENSIBILITY · 新增能力检查单](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist) |
| 架构改造排期 / 分域拆 PR | [ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)（决策图 · 分域矩阵 · 阶段卡 · 验收门禁） |
| **按阶段升级**（当前阶段、准入、验收） | [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md) |
| 边开发边补全 / PR 骨架 | [INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md) · [templates/incremental-pr-slice.md](./templates/incremental-pr-slice.md) |
| manifest / 候选 / 规则决策 | [CONTRIBUTING · 常见变更自检](../CONTRIBUTING.md#常见变更自检) 与 PR 模板勾选项 |

<a id="release-pass"></a>

## 2. 大版本或改顶栏 / 总线后（发布前轻量人工）

与 [SITE_REVIEW · 测试与质量](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review) 清单一致，建议至少：

- [ ] 抽样点顶栏 **2～3 链**，**`current` / `class="current"`** 与当前页一致  
- [ ] **窄窗**（约 390px）顶栏换行与三问/分区可点  
- [ ] 总线页 **`data-site-meta-version`** 与 **`assets/site-meta.json`** 意图一致（若本版要升 **`site_version`**）  
- [ ] 在**实际部署环境**抽一条 **`docs/*.md`** 链，确认读者可接受（静态根部署下多为原文/下载，见 [PLATFORM · §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)）  
- [ ] 若发布 **SPA**：抽一条壳内路由 + **iframe** 内标题可读性  

<a id="integration-hint"></a>

## 3. 对外集成方（只读 API）

部署边界、**OpenAPI**、缓存与「只读不写 manifest」见 **[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)**；字段级索引仍以 **[DATA_CONTRACTS.md](./DATA_CONTRACTS.md)** 为准。

- **网关**：若将 **`readonly_api`** 暴露到公网或多方租户网络，请在反向代理上**限制或鉴权**敏感路径（如 **`GET /candidates`**、**`GET /hint-decisions`**、**`GET /ingest-config`**）；**`GET /hint-rules`**、**`GET /maps-to-hints`** 等相对低敏，仍随版本发布；**`maps-to-hints`** 或含 host 线索，大规模暴露前建议自查正文。应用内**无**登录鉴权，见 **[INTEGRATION · 敏感路由](./INTEGRATION_AND_READONLY_API.md)**。路由与路径对表：**[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)**。
- **与合并闸门**：对外只读服务**不替代** **`make validate`**；集成方变更契约 JSON 时仍以仓库闸门与 PR 为准。

<a id="doc-index"></a>

## 4. 相关文档与命令索引

| 需求 | 去向 |
|------|------|
| 全文档整理主线（维护者按序扫读） | [docs/README.md · 文档主线](./README.md#docs-spine) |
| 术语 · CI · 常见变更表 | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| 自动化助手闸门 | [AGENTS.md](../AGENTS.md) · [repo-gates.mdc](../.cursor/rules/repo-gates.mdc) |
| 命令与脚本职责 | [scripts/README.md](../scripts/README.md) |
| 技术架构整理 · 分阶段升级 | [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md) · [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md) · [TECH_ARCHITECTURE_CAPABILITIES.md](./TECH_ARCHITECTURE_CAPABILITIES.md) · [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) |
| 用户端/管理端 · 数据源 · 审核分层 · 前端/后端分拆 | [USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)（**[节 1a](USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)**） · [PLATFORM_MASTER_MAP · 读者面/管理面](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces) |
| 管理 Web · 登录 · 用户 · 审核工作流（规划） | [ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md) |
| 扩展插槽 · 智能化边界 | [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) |
| 智能化 · 六域协同 | [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md) |
| 增能 · 读者预期 | [PLATFORM_CAPABILITY_MAP §6—§7](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist) |
| 字段与主键 | [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) |
| OpenAPI · 网关 | [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md) |
| Docker 部署 | [DOCKER.md](./DOCKER.md)（含 profile **`admin`** · **[§3a](./DOCKER.md#profile-admin)**） |
| 管理端脚手架（`admin-console`） | [admin-console/README.md](../admin-console/README.md) · [ADMIN_WEB_CONSOLE_ROADMAP · §8](./ADMIN_WEB_CONSOLE_ROADMAP.md#scaffold-implementation) |
| 内容草稿（LLM/辅助） | [scripts/draft/README.md](../scripts/draft/README.md) |

---

*与主分支同步；新增全局闸门或发布仪式时请更新本节并回链 [PLATFORM_EXTENSIBILITY](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) 与 [docs/README 文档主线](./README.md#docs-spine)。*
