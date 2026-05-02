# 合并与发布检查单（一页汇总）

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**本文侧重**：**合并前**命令与核对、**`spa-sync` / `spa-build`**、发布习惯；以 **贡献 / 维护者**动线为主。**架构师跨 PR 收束**：[ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

本文把分散在多篇文档里的**合并前工程步骤**与**大版本发布习惯**收成一条动线，避免漏项；与 **[CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd)** · **[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)**、**[PLATFORM_CAPABILITY_MAP · §6—§7](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)**、**[SITE_REVIEW_THREE_PASSES · 四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)** 一致，**不替代**其中细节。

**智能化与可演进自动化**在本仓库的含义：契约校验、管道步骤、规则 JSON、只读 API、定时 ingest/分析 artifact 等——在 **[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md · §1.1](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)** 所述**不变量**内演进；**不**包含默认自动覆盖已审 **`evolution-manifest.json`**。目标架构按 **六域协同**（数据 / 管道 / 分析 / 前端 / 运维 / 治理）打点，见 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**（阅读顺序与文首一致：**[进化与优化](./INTELLIGENCE_SIX_DOMAINS.md#evolution-and-optimization)** · **[持续分析优化](./INTELLIGENCE_SIX_DOMAINS.md#continuous-analysis-optimization)** · **[持续的优化](./INTELLIGENCE_SIX_DOMAINS.md#sustained-optimization)**（**[持续的进行优化](./INTELLIGENCE_SIX_DOMAINS.md#ongoing-optimization)**）· **[持续的升级](./INTELLIGENCE_SIX_DOMAINS.md#sustained-upgrade)** · **[§2.2 读者面版式](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**）：改枢纽 MPA 与总线步骤**分列自检**；合并/阶段与小轮迭代习惯）。

<a id="merge-at-a-glance"></a>

### 合并前速览（五条）

1. **`make validate`** 绿（合并真闸门；**`make test` / `validate-fast` 不可替代**）。  
2. 推荐 **`make merge-ready`**：validate + **`test-readonly-api`** + **`test-admin-console`**。  
3. 改 **`partials/`** → **`make sync-nav`** → **手调 `404.html`**（及 **`legacy-all-in-one.html`** skip 与 partial 一致）。  
4. 改根 **`*.html` / `docs/`** 且维护 SPA → **`make spa-sync`** 或按 CI 路径 **`make spa-build`**。  
5. **`evolution-manifest.json`**：仅经人审闸门合并；**不**设计默认自动写入。

<a id="pre-merge"></a>

## 1. 合并 PR 前（维护者 / 工程）

<a id="pre-merge-partials-sequence"></a>

**改 `partials/site-nav.inc.html` / `partials/skip-bar.inc.html` 时建议固定顺序**：**`make sync-nav`** → **`make validate`**；**`404.html`**（及需与 skip 五链一致的 **`legacy-all-in-one.html`**）**不在** **`sync_site_nav`** 写回范围，改模板后须**手调**与 partial 一致 — 下表对应行 · **[scripts/README · sync_site_nav 真源](../scripts/README.md#sync-site-nav-source)**。**`make help`** 文首 echo 与 **[CONTRIBUTING · 开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** · **[PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)** · **[动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)** 三锚对表；往下亦有 MERGE / **maintainer-hub** 收束行。

| 步骤 | 命令或文档 |
|------|------------|
| **开 PR 前**最短步骤（`pip` → `validate` → `merge-ready`；三锚 + **`make help`**） | **[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** |
| 不确定改了 partials / SPA / registry 时**先执行哪条** | **[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** · **[PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)** · **[动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)**（根 **`make help`** 文首三锚对表） |
| 全闸门（与 pre-commit、CI **`validate`** 一致） | **`make validate`** |
| 仅用 **`make validate-fast`** / **`make test`** 本地迭代 | **不可**作为合并依据；**CI** 与 **pre-commit** **不跑** **`validate-fast`**；仍须本表 **`make validate`**（见 **[docs/README · 持续集成](./README.md)** 与 **[ARCHITECTURE · `run_validate.sh` 与 fast 子集](./ARCHITECTURE.md#run-validate-gate)**） |
| **`validate` stderr 提示跳过旧格式 `pipeline-metrics`**（仅本地 **`artifacts/`**，已 gitignore） | 先 **`make clean-pipeline-metrics-dry-run`** 查看将删文件，再 **`make clean-pipeline-metrics`**，重跑 **`make analyze`** / **`make evolution-fast`**；契约见 **[DATA_CONTRACTS · §7](./DATA_CONTRACTS.md#pipeline-telemetry)** · **[EVOLUTION_RUNBOOK · 加速](./EVOLUTION_RUNBOOK.md#accelerate)** |
| 只读 API + 管理端烟测（本地未单装 **fastapi** 时 **`make validate`** 会 **skip** **`test_readonly*.py`**） | **`make merge-ready`**（= 上一步 + **`make test-readonly-api`**（**`test_readonly*.py`**：HTTP **304** + **`READONLY_PROXY_SEGMENTS`** 对账）+ **`make test-admin-console`**）或分步执行后两者。**不含 `spa-build`**，与 **[PLATFORM_MASTER_MAP · 2.1 步骤 5](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#golden-paths)**、`[AGENTS.md](../AGENTS.md#agents-pre-merge)` 合并前条一致 |
| 改 **`admin-console/`**（**`static/index.html`** 顶栏 / **`mod-*`** / 深链） | **[ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**（与 **[§7b](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-ui-ia)** 对表）；**`#mod-api`→`#mod-analysis`**；**`make test-admin-console`**；链入维护表 **[§11a](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-doc-index)** |
| 改 **`scripts/ingest_config.json`** / **`maps_to_hints.json`** 或 RSS / `json_feeds` 路线 | **`make validate`**；对读 **[INTEL_AND_POLICY_TRACKING_PLAYBOOK](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)**（**[§2—2a](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)** · 人审与信源）· **[REFERENCE_DESIGN_OPINION_MONITORING](./REFERENCE_DESIGN_OPINION_MONITORING.md)**（对标与网关）· **[scripts/README](../scripts/README.md)** · **[DATA_CONTRACTS · `ingest_config` 表行](./DATA_CONTRACTS.md#ingest-config-contract)** |
| 变更触及 **SPA** / **registry** / **sync 输入** 等且 CI 会跑 **spa-build** 时 | **`make spa-build`**（见 **[docs/README 文首](./README.md)** 路径说明）；须在 **`merge-ready`** 绿之后**追加**，非其子命令 |
| 改根目录 **`*.html`**（读站指路、多页页脚、**`analysis-hub`** 导读等）且需 **SPA** 侧 **`spa/public/`** 内 iframe 与 **`public/docs`** 与 MPA 一致 | **`make spa-sync`**（或 **`npm run sync`**，见 **[spa/README](../spa/README.md)**）；维护者收束 **[关系视图](../maintainer-hub.html#mh-spine-map)** · **[系统边界](../maintainer-hub.html#mh-boundaries)** · **[衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)**；**不替代** **`make validate`** |
| 只改 **`partials/site-nav.inc.html`** / **`partials/skip-bar.inc.html`**（全站顶栏、skip-bar **模板**，当前 **五** 链含 **常见下一站**） | **`make sync-nav`**（**`sync_site_nav.py`** 写回各注册页；**`make validate`** 内含 **`sync_site_nav --check`**）。**`maintainer-hub.html`** 在五链后再由 **`build_skip_bar`** 拼 **`#mh-spine-map` / `#mh-boundaries` / `#mh-reader-admin-matrix`**（与本页 **`toc--pilot`** 前三锚一致），**勿**在 HTML 手改这三条。**`404.html`** 不在脚本写回范围，改模板后须**手调** **404** 顶栏/skip 与 partial 一致（**`check_skip_bar_404.py`**）— **[scripts/README · `sync_site_nav` / 真源（#sync-site-nav-source）](../scripts/README.md#sync-site-nav-source)** · 本节 **§2** 抽样 |
| 增删 **`evolution-registry.json` · `pages`** 或批量改根目录页 **`<title>`**（影响顶栏轻量搜索 / 只读 **`/site-search-index`**） | **`make site-search-index`**（可选产物 **`assets/site-search-index.json`**；**不入** **`make validate`**）；若提交该 JSON，与 **[SITE_DATA · §3](./SITE_DATA_UPDATE_FRAMEWORK.md#registry)** 对读 |
| 增能自检 | [PLATFORM_CAPABILITY_MAP · §6](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)、[PLATFORM_EXTENSIBILITY · 新增能力检查单](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist) |
| 架构改造排期 / 分域拆 PR | [ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)（决策图 · 分域矩阵 · 阶段卡 · 验收门禁） |
| PR 描述先定「五维 / 六域 / 七类」粒度 | **[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [CONTRIBUTING · 术语与契约](../CONTRIBUTING.md#contributing-terminology) |
| **按阶段升级**（当前阶段、准入、验收） | [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md) |
| 边开发边补全 / PR 骨架 | [INCREMENTAL_BUILD_PLAYBOOK.md](./INCREMENTAL_BUILD_PLAYBOOK.md) · [templates/incremental-pr-slice.md](./templates/incremental-pr-slice.md) |
| manifest / 候选 / 规则决策 | [CONTRIBUTING · 常见变更自检](../CONTRIBUTING.md#contributing-common-changes-checklist) 与 PR 模板勾选项 |

<a id="release-pass"></a>

## 2. 大版本或改顶栏 / 总线后（发布前轻量人工）

与 [SITE_REVIEW · 测试与质量](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review) 清单一致，建议至少：

- [ ] 抽样点顶栏 **2～3 链**，**`current` / `class="current"`** 与当前页一致  
- [ ] **窄窗**（约 390px）顶栏换行与三问/分区可点  
- [ ] 总线页 **`data-site-meta-version`** 与 **`assets/site-meta.json`** 意图一致（若本版要升 **`site_version`**）  
- [ ] 在**实际部署环境**抽一条 **`docs/*.md`** 链，确认读者可接受（静态根部署下多为原文/下载，见 [PLATFORM · §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)）  
- [ ] **本地读者站**：用 **`make serve-reader`**（默认 **8000**，占用时可 **`READER_PORT=8001`**）或 **Docker / dev compose**（**8765**）打开首页，确认总线非白屏（勿 **`file://`**；见根 [README.md](../README.md)）  
- [ ] 若依赖顶栏 **「搜页面…」**：已 **`make site-search-index`** 且 **`assets/site-search-index.json`** 与当前注册页一致（无则顶栏该格隐藏，属预期）  
- [ ] 若发布 **SPA**：抽一条壳内路由 + **iframe** 内标题可读性  
- [ ] 若本版改 **`admin-console`**：除 **`make test-admin-console`** 外，可抽 **≤60rem** 顶栏横向滚动与 **`#mod-…`** 深链（**[§7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** · **[§7b](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-ui-ia)**）

<a id="integration-hint"></a>

## 3. 对外集成方（只读 API）

部署边界、**OpenAPI**、缓存与「只读不写 manifest」见 **[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)**；字段级索引仍以 **[DATA_CONTRACTS.md](./DATA_CONTRACTS.md)** 为准。**舆情 / 制度类外源与反哺节奏**（非路由契约）：**[INTEL_AND_POLICY_TRACKING_PLAYBOOK.md](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)**（**[§2—2a](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**）。

- **网关**：若将 **`readonly_api`** 暴露到公网或多方租户网络，请在反向代理上**限制或鉴权**敏感路径（如 **`GET /candidates`**、**`GET /hint-decisions`**、**`GET /ingest-config`**）；**`GET /hint-rules`**、**`GET /maps-to-hints`** 等相对低敏，仍随版本发布；**`maps-to-hints`** 或含 host 线索，大规模暴露前建议自查正文。应用内**无**登录鉴权，见 **[INTEGRATION · 敏感路由](./INTEGRATION_AND_READONLY_API.md)**。路由与路径对表：**[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)**。
- **与合并闸门**：对外只读服务**不替代** **`make validate`**；集成方变更契约 JSON 时仍以仓库闸门与 PR 为准。

<a id="doc-index"></a>

## 4. 相关文档与命令索引

| 需求 | 去向 |
|------|------|
| **开 PR 前**最短步骤（与上文「合并前速览（五条）」对读） | **[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** |
| 合并前「改了什么 → 先跑什么」一页表 | **[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** · **[PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)** · **[动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)**（根 **`make help`** 文首三锚对表） |
| 全文档整理主线（维护者按序扫读） | [docs/README.md · 文档主线](./README.md#docs-spine) |
| 整体内容框架（真源分层） | [docs/README · #content-framework](./README.md#content-framework) |
| 前后台模块总览（读者面 × 管理面） | [docs/README · #front-back-modules](./README.md#front-back-modules) |
| 组件×功能一条表（可执行单元 × 主链） | [docs/README · #system-components-fusion](./README.md#system-components-fusion) |
| 按改动类型判型（最短链 · 与主线 **0c** 同锚） | [docs/README · #quick-paths](./README.md#quick-paths) · [MODULE · §1a](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#seven-class-pkg-quick) · [内容驱动链 · #content-driven-chain](./README.md#content-driven-chain) · [AI 与自动进化 · #ai-assisted-evolution](./README.md#ai-assisted-evolution) |
| 五维总图 · 主链联动验证 · 仓库物理分层 · 勿混粒度 | **[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · **[§1a 主链联动与验证](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** · **[§1b 仓库物理分层](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)** |
| 术语 · CI · 常见变更表 | [CONTRIBUTING.md](../CONTRIBUTING.md#contributing-terminology) |
| 五条红线 · PR 复盘 · 改 partials 手顺 | [ONE_PAGER · 不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [CONTRIBUTING · 开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [CONTRIBUTING · PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [CONTRIBUTING · 动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command) · [MERGE · partials 手顺](#pre-merge-partials-sequence) |
| 自动化助手闸门 | [AGENTS.md](../AGENTS.md#agents-contract) · [框架判型](../AGENTS.md#agents-content-framework) · [合并前](../AGENTS.md#agents-pre-merge) · [人审](../AGENTS.md#agents-invariants) · [管理端 IA](../AGENTS.md#agents-admin-console) · [双轨](../AGENTS.md#agents-dual-track) · [枢纽首屏](../AGENTS.md#agents-hub-lead) · [make test 子集](../AGENTS.md#agents-test-subset) · [Cursor 规则](../AGENTS.md#agents-cursor-rules) · [repo-gates.mdc](../.cursor/rules/repo-gates.mdc)（[README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map) · 文首「子规则对读」）· [spa-nav-config](../.cursor/rules/spa-nav-config.mdc) · [spa-nav-registry](../.cursor/rules/spa-nav-registry.mdc) · [evolution-registry](../.cursor/rules/evolution-registry.mdc) |
| 命令与脚本职责 | [scripts/README.md](../scripts/README.md)（**`sync_site_nav` / `make sync-nav`**：顶栏模板 → 各页 · **[#sync-site-nav-source](../scripts/README.md#sync-site-nav-source)**） |
| 技术架构整理 · 分阶段升级 | [PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md) · [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)（[附录 · 详版能力地图](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)；[TECH_ARCHITECTURE_CAPABILITIES 别名](./TECH_ARCHITECTURE_CAPABILITIES.md)） · [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) |
| 多篇都写「技术栈」· 简版 vs 详版 · 防散读法 | [docs/README · #tech-stack-read-merge](./README.md#tech-stack-read-merge) |
| 用户端/管理端 · 数据源 · 审核分层 · 前端/后端分拆 | [USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)（**[节 1a](USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)**） · [PLATFORM_MASTER_MAP · 读者面/管理面](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces) · [INTELLIGENCE · §2.2 枢纽页 CSS](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract) |
| 管理 Web · 登录 · 用户 · 审核工作流（规划） | [ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md) |
| 扩展插槽 · 智能化边界 | [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) |
| 智能化 · 六域协同 | [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)（**[§2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**） |
| 增能 · 读者预期 | [PLATFORM_CAPABILITY_MAP §6—§7](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist) |
| 字段与主键 | [DATA_CONTRACTS.md](./DATA_CONTRACTS.md) |
| 舆情 / 制度 / 国情 · ingest 信源分层与反哺 | [INTEL_AND_POLICY_TRACKING_PLAYBOOK.md](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)（**[§2—2a](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**） |
| OpenAPI · 网关 | [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md) |
| Docker 部署 | [DOCKER.md](./DOCKER.md)（含 profile **`admin`** · **[§3a](./DOCKER.md#profile-admin)**） |
| 本地读者站 MPA（无 Docker） | 根 **`make serve-reader`**（默认 **8000**，**`READER_PORT`** 可改）· 根 [README.md](../README.md) · [DOCKER.md §1](./DOCKER.md#quickstart) |
| 管理端脚手架（`admin-console`） | [admin-console/README.md](../admin-console/README.md) · [ADMIN_WEB_CONSOLE_ROADMAP · §8](./ADMIN_WEB_CONSOLE_ROADMAP.md#scaffold-implementation) · [ADMIN_CONSOLE · §7](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)（**`mod-*`** · **`#mod-api`→`#mod-analysis`**） · [ADMIN_CONSOLE · §11a 索引](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-doc-index) |
| 内容草稿（LLM/辅助） | [scripts/draft/README.md](../scripts/draft/README.md) |

---

*与主分支同步；新增全局闸门或发布仪式时请更新本节并回链 [PLATFORM_EXTENSIBILITY](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) 与 [docs/README 文档主线](./README.md#docs-spine)。*
