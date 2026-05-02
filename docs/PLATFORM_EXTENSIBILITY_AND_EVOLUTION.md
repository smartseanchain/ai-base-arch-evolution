# 平台扩展性与进化（落地指南）

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

本文与 **[ARCHITECTURE_ONE_PAGER · 三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**、**[ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md)**（不变量与阶段 0—3）、**[TECH_BRIEF · 附录 4](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-extend)**（可扩展方向表）对齐，专门回答两件事：**如何把扩展性做到最大**（在不变量之内），以及**平台向下一阶段进化时默认走哪条路**。定性脚手架、非采购清单。**智能化目标表述**已从「单点脚本」升级为 **「六域协同」**（数据 / 管道 / 分析 / 前端 / 运维 / 治理），见专篇 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**。**五维总图 · 主链联动验证 · 仓库物理分层**：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（主线 **0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。**自动化助手（契约 / 人审 / 分析·HTML / 双轨）**：[AGENTS.md · 总入口](../AGENTS.md#agents-contract) · [人审闸门](../AGENTS.md#agents-invariants) · [架构边界](../AGENTS.md#agents-arch-boundary) · [双轨呈现](../AGENTS.md#agents-dual-track) · [合并前 / merge-ready](../AGENTS.md#agents-pre-merge)。**MPA 顶栏与失页**：**`partials/`** → **`make sync-nav`**；**`404.html`** 手调（`sync_site_nav` 不写回）— **[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

<a id="invariants"></a>

## 1. 不变量（扩展不得突破）

下列约定是「最大扩展性」的边界：新能力应**挂接**在插槽上，而不是绕开它们（与 [ARCHITECTURE_UPGRADE · §1](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#adaptation) 一致）。

| 不变量 | 扩展时的含义 |
|--------|----------------|
| **Git 内 JSON 为真源** | 新结构化事实须可 diff、可 `make validate`；第二真源须在文档中显式命名 |
| **单一注册表** | 新分页、新 `lab_factors` 只经 **`scripts/evolution-registry.json`** 进入对账链（**单一注册表不变量**） |
| **人审闸门** | 任何自动化不得默认覆盖已审 **`evolution-manifest.json`** |
| **分析不写 HTML** | 新分析产出只进 JSON；叙事在 **`.html`** 或独立草稿插槽 |
| **双轨呈现** | MPA 为 validate 默认真源；SPA 与 registry / nav 同步演进 |
| **两条版本线** | 对外 **`site_version`** ≠ 分析 **`run_id`**，扩展文档与 API 字段时勿混 |

<a id="automation-and-evolution"></a>

### 1.1 智能化与可演进的自动化（边界）

本站所说的**智能化**，优先指：**规则与数据可计算**（`evolution-hint-rules.json`、快照与沉淀、**`rule_id`** 决策链）、**管道可重复**（**`evolution_pkg.pipeline`**、遥测 artifact）、**契约可校验**（Schema + **`make validate`**）、**集成可缓存再验证**（**`readonly_api`** 的 ETag/304，见 **[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)**）——机器承担的是**一致性、可追溯、减少手工遗漏**，不是替人下结论。

**目标架构（六域协同）**：不把智能化收敛为「某个脚本」，而按 **数据 · 管道 · 分析 · 前端 · 运维 · 治理** 分工与握手；域定义、协同示意、与七类模块/插槽的对照、PR 自检表见 **[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)**。**文首五段阅读顺序**（进化/优化 → 持续分析优化 → 持续的优化 → 持续的升级 → §2.2）与其脚注锚点一致，避免与 §1.1 下文各条**交叉误读**。

**可演进的自动化**包括：定时 **ingest**、bot 开候选 PR、**artifact 下载后人工合并**、在已通过 **`make validate`** 前提下用 **`make evolution-fast`** 加速重算快照/沉淀/趋势、递增 **`schema_version`** 与注册表扩展。进化体现在**数据、规则与契约**的迭代，以及 **[§3 四条轨道](#evolution-tracks)** 的分轨推进。**读者侧呈现**（首屏导读栈、pill 目录、命令卡栅格等）可持续打磨，契约见 **[INTELLIGENCE · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**——与数据/总线登记**并列验收**，**不**把纯 CSS/HTML 枢纽版式误记为 **`[data-site-data-live]`** 消费方扩展。

**不断优化**：在**不变量与既有契约**之下提升可维护性与读者体验——对照 **[PLATFORM_CAPABILITY_MAP · §6](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)** · **[§7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)** 与 **[SITE_REVIEW_THREE_PASSES](./SITE_REVIEW_THREE_PASSES.md)**；与「扩展新能力」区分见 **[INTELLIGENCE · 进化与优化](./INTELLIGENCE_SIX_DOMAINS.md#evolution-and-optimization)**。**不要**用「抛光文案/CSS」掩盖本需 **Schema、登记或新域声明** 的变更。**持续的优化**（发版后仍复查、文档与模板回链；口语 **持续的进行优化** 同指）见 **[INTELLIGENCE · #sustained-optimization](./INTELLIGENCE_SIX_DOMAINS.md#sustained-optimization)** · **[#ongoing-optimization](./INTELLIGENCE_SIX_DOMAINS.md#ongoing-optimization)**。**持续的升级**（阶段 0—3 与 ROADMAP 节律复盘）见 **[INTELLIGENCE · #sustained-upgrade](./INTELLIGENCE_SIX_DOMAINS.md#sustained-upgrade)**。

**明确非目标（与人审不变量一致）**：默认 **自动 merge** 已审 **`evolution-manifest.json`**、用编排器/消息队列**替代 Git** 作唯一审计源、让 **`analysis_engine`** 写 HTML 正文。若使用 **LLM 或机器草稿**，产出应落在 **`scripts/draft/`**（见该目录 **[README](../scripts/draft/README.md)**），经 **PR 审阅**后再迁入 `.html` 或结构化 JSON。

**与「分析结论 + AI」分流**：面向**页面叙事**的长草稿走 **`scripts/draft/`**；面向**已生成分析快照之上的解读叠加**（可配置接入模型服务、独立 JSON 产物），设计叙述见 **[AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md)**——**不**把非确定性文本并入 **`analysis-snapshot.json` 必填域**，**不**让 LLM 写 manifest。若对标 **GitHub 等开源「舆情 / 热点 / 多源情报」** 产品形态，仅作**参考引用**时的能力映射与侧车边界见 **[REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md)**。**AI 辅助「自动进化」能力链与主线表 3b/3d/3e/9 索引**：[docs/README · #ai-assisted-evolution](./README.md#ai-assisted-evolution)。

**合并前推荐动线**：**`make merge-ready`** = **`make validate`** + **`make test-readonly-api`** + **`make test-admin-console`**，见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**。

<a id="extension-slots"></a>

## 2. 扩展性：优先守住的「插槽」

把「能长新东西」收敛成**少数稳定插槽**：新能力先**声明落在哪一格**，再实现，避免全站耦合。

| 插槽 | 扩展什么 | 已有基础 | 扩展时注意 |
|------|----------|----------|------------|
| **契约层** | 新 JSON 形态、新字段 | **`docs/schemas/*.schema.json`**、对应 **`validate_*_schema.py`**、**`schema_version`**、**`scripts/run_validate.sh`** | 先 **Schema + 校验 + `run_validate.sh`**，再写生产方与消费方（**[scripts/README · 契约检查单](../scripts/README.md)** 文首四步） |
| **注册表** | 新分页、新沙盘因子 | **`scripts/evolution-registry.json`** | **唯一入口**；联动 drift、sitemap、ingest、**SPA** **`spa/nav.config.json`**（与 **`check_nav_links_registry.py`** / **`make gen-nav-links`** 对账） |
| **分析规则** | 新提示、新闭环维度 | **`scripts/evolution-hint-rules.json`**、**`assets/evolution-hint-decisions.json`** | 用 **`rule_id`**、**`track_closure`** 保持可审计；**勿**把规则散落在 HTML |
| **展示消费方** | 新读数条、新总线挂载点 | **`site-data-bus.js`**、**`[data-site-data-live]`**、**[SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md)** 登记习惯 | 新占位符 + **文档登记**；避免「悄悄多一个 **fetch**」 |
| **只读出口** | 集成方、内部看板 | **`scripts/readonly_api.py`** | **只读**、**不写 manifest**；CORS / 鉴权在网关层演进 |
| **管道步骤** | 新数据源、新批处理 | **`scripts/evolution_pkg/`**（含 **`evolution_pkg.pipeline`**）、**`scripts/run_pipeline_steps.py`**、**`scripts/run_update_pipeline.sh`** | 步骤可增，但**闸门顺序**与 **artifact → 人工合并** 节奏不要轻易绕开 |
| **可选 AI 解读层** | 在确定性快照之上生成解读（自然语言/结构化摘要） | **契约已落地**：**`ai-analysis-overlay.schema.json`**、**`validate_ai_analysis_overlay_schema.py`**、**`write_ai_analysis_overlay.py`**（**`--stub`** / **`AI_OVERLAY_ENABLE`**）；配置模板 **[examples/ai_analysis_overlay.example.json](./examples/ai_analysis_overlay.example.json)** | 见 **[AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md)**；密钥仅 env；**不**写 manifest |

**原则**：扩展 = 多一个**契约**或多一个**注册项**或多一个**消费方**，而不是多一条「谁都不知道」的暗线。

**默认约定**：新增 **Python 业务逻辑** 优先写在 **`evolution_pkg`** 子模块，**`scripts/*.py`** 保留参数解析与 `if __name__` 入口，便于日后被编排器或测试直接 import。

<a id="evolution-tracks"></a>

## 3. 平台进化：四条可并行轨道

与 [TECH_BRIEF · 附录 3](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-evolution) **进化三层含义**一致：**进化不必串行**，但每条轨道边界要清；规划时标明本轮主要动哪一条，避免「一条 PR 改全世界」。

| 轨道 | 主链与扩展性落点 |
|------|------------------|
| **数据进化** | **观测 → 候选 → 人审 → manifest → 分析 / 沉淀 / 趋势**。扩展性在于 **ingest 配置**、**`maps_to`**、**新 JSON 块**（配 Schema）；**自动化不得默认写 manifest**。 |
| **规则与闭环进化** | **新规则**、**新缺口类型**、**决策记录**扩展。扩展性在于 **规则 JSON + decisions**，而不是改引擎硬编码一堆 `if`。 |
| **叙事与方法进化** | **新页**、**新配方**、方法篇迭代。扩展性在于 **HTML + 交叉引用**（`id` / **`rule_id`**）；**LLM / 草稿**若上，走**独立目录与闸门**（见 [ARCHITECTURE · 内容生成](./ARCHITECTURE.md#seven-layers)）。 |
| **呈现与路由进化** | **MPA** 新枢纽、**SPA** 新路由、**总线**新块。扩展性在于 **registry + partials + `spa-sync`**（**`spa-build`** 前亦 **`spa-sync`**）；**`make validate` 仍以 MPA 为默认真源**。动线 [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map) · [系统边界](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)。 |

**「平台级」进化**（多团队、多环境、多 DAG）再叠 **[ARCHITECTURE_UPGRADE · 阶段 2/3](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#upgrade-tiers)** 与 **[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)**，避免在**单仓库节奏**下过早上重型基础设施。

<a id="phased-runway"></a>

## 4. 分阶段建议（与现有 0—3 阶段对齐）

与 [ARCHITECTURE_UPGRADE · §2](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#upgrade-tiers) 同读；下面是**扩展性视角**的默认取舍。

- **阶段 0（长期基线）**  
  保持 **Git + PR + `make validate`** 为**审计主轴**；定时 workflow 以 **artifact** 为主，**合并仍显式人控**。这是平台可信度的来源；扩展性再强也不能替代。

- **阶段 1（优先做「可插拔」）**  
  - **契约优先**：任何新资产类型先 **Schema + 版本号**。  
  - **包化**：逻辑进 **`evolution_pkg`**，脚本层变薄，便于以后被编排器或测试复用。  
  - **API**：只读端点按**资源**切分（快照 / 趋势 / manifest / site-meta / 历史等），便于外部平台按需拉取（**`readonly_api.py`**）。  
  - **文档**：新插槽同步 **[DATA_CONTRACTS.md](./DATA_CONTRACTS.md)** + **SITE_DATA_UPDATE_FRAMEWORK**（或消费方表），避免「只有代码知道」。

- **阶段 2（编排器）**  
  仅在 **多 DAG、回填、多环境参数矩阵、运行历史 UI** 等信号齐备时，把**现有 Python 步骤包成任务**，而不是重写业务逻辑。**编排器不写 manifest**（与 [ORCHESTRATION · §2](./ORCHESTRATION_AND_EVENT_STREAMING.md) 一致）。

- **阶段 3（事件流）**  
  仅在 **多服务实时写、多订阅、回放** 且与 **Git 事实源分工明确** 时引入；**禁止**用 broker **替代 Git** 作**唯一审计源**（反模式见下文 §7 与 [ARCHITECTURE_UPGRADE · §4](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#anti-patterns)）。

**默认策略**：在**阶段 1 内把插槽用满**，再评估阶段 2/3。

<a id="platform-habits"></a>

## 5. 面向「平台进化」的产品 / 工程习惯

- **合并前固定仪式**：**`make merge-ready`** 与发布轻量清单收在 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**（**`validate`**、只读 API 与管理端烟测）。  
- **能力地图当 backlog**：用 **[PLATFORM_CAPABILITY_MAP.md](./PLATFORM_CAPABILITY_MAP.md)** §1—§4 与 **[增能检查单 §6](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)**、**[读者与发布 §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)** 做「要不要做、做完验什么」的固定仪式。  
- **版本线写清**：对外里程碑用 **`site_version`**，分析血缘用 **`run_id`**，避免平台对外叙事和工程日志混谈。  
- **深链与提要**：平台页变多时，用 **读站指路**、**本轮提要**、**[四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)** 控制读者动线与发布回归成本。  
- **双轨默认**：**MPA** 保真源、**SPA** 保入口体验；新能力默认先在 **MPA 与契约**上跑通，再挂 SPA。

<a id="new-capability-checklist"></a>

## 6. 新增能力检查单（合并前建议逐项勾）

0. **是否跨阶段基础设施？**（编排器、broker、服务器库/CDC）→ 先 **[PHASED_UPGRADE_EXECUTION_GUIDE](./PHASED_UPGRADE_EXECUTION_GUIDE.md)** 与 **[ARCHITECTURE_UPGRADE_ROADMAP · §1](./ARCHITECTURE_UPGRADE_ROADMAP.md#upgrade-panorama)** 判阶段；**默认先耗尽阶段 1**（契约、分包、双轨、只读面），再单独立项 **2/3/[DATA_STORES](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)**。  
1. **是否改契约？** → **`docs/schemas/`** + 校验脚本 + **`run_validate.sh`**（见 [scripts/README](../scripts/README.md) 文首四步）。  
2. **是否新分页/因子？** → **`evolution-registry.json`** → **`make sync-nav`** →（SPA）**`spa/nav.config.json`** + **`make gen-nav-links`**（**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 生成，勿手改 HTML；若本轮动 **`partials/skip-bar.inc.html`**，**`404.html`** 顶栏/skip 须**手调** — [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)）。  
3. **是否新读数 UI？** → **SITE_DATA_UPDATE_FRAMEWORK** 登记消费方；避免未文档化的裸 **`fetch`**。  
4. **是否新对外接口？** → **`readonly_api`** 只读扩展；或文档说明 CORS/部署边界。  
5. **是否动分析语义？** → **`analysis_engine --check`** + 快照 Schema + 沉淀/趋势消费方同步。  
6. **合并前** → **`make validate`**；大改呈现 → [SITE_REVIEW · 四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)。  
7. **Schema 文件索引** → **[docs/schemas/README.md](./schemas/README.md)**。

<a id="anti-patterns"></a>

## 7. 反模式（扩展时最容易翻车）

- **第二套页面表**、**第二套因子表**、绕过 registry 的「临时白名单」。  
- **引擎或外部 job 直接改 `evolution-manifest.json` 或 HTML 正文**。  
- **未登记**的新 **`fetch`** 路径，导致总线缓存与加载顺序混乱。  
- 为「平台感」**同时**上编排器 + 消息队列，而业务仍是**单仓库、单节奏**（见 [ARCHITECTURE_UPGRADE · §4](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#anti-patterns)）。  
- 编排器或消息队列**替代** Git PR 作**唯一**审计源。

---

## 延伸阅读

- **智能化 · 六域协同（目标架构）**：[INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)  
- **全文档整理主线（表）**：**[docs/README · 文档主线](./README.md#docs-spine)**  
- 三架构对照与升级一句化：**[ARCHITECTURE_ONE_PAGER](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**  
- 字段与主键：**[DATA_CONTRACTS](./DATA_CONTRACTS.md)**  
- 合并与发布一页清单：**[MERGE_AND_RELEASE_CHECKLIST](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**（含 **[§4 文档索引](./MERGE_AND_RELEASE_CHECKLIST.md#doc-index)**）  
- 只读 API 与 OpenAPI：**[INTEGRATION_AND_READONLY_API](./INTEGRATION_AND_READONLY_API.md)**  
- 内容草稿插槽：**[scripts/draft/README.md](../scripts/draft/README.md)**  
- 按阶段升级执行：**[PHASED_UPGRADE_EXECUTION_GUIDE](./PHASED_UPGRADE_EXECUTION_GUIDE.md)** · 可落地全景：**[ARCHITECTURE_UPGRADE_ROADMAP](./ARCHITECTURE_UPGRADE_ROADMAP.md)**  
- 技术架构整理 + 升级路径：**[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)**（简版 **§1—§4**）· **[详版附录](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)**（[别名](./TECH_ARCHITECTURE_CAPABILITIES.md)）  
- **分端设计**（用户端/管理端 · 数据源 · 进化与分析 · 审核分层）：**[USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)**  
- **管理端 Web 化**（登录、用户与角色、审核工作流规划）：**[ADMIN_WEB_CONSOLE_ROADMAP](./ADMIN_WEB_CONSOLE_ROADMAP.md)**  
- 能力表与未实现方向：**[TECH_BRIEF · 附录 4](./TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-extend)**  
- 增能与读者预期：**[PLATFORM_CAPABILITY_MAP](./PLATFORM_CAPABILITY_MAP.md#enhance-checklist)** · **[§7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)** · **产品/工程习惯（本文 §5 · `#platform-habits`）**

*随主分支演进；引入新的全局插槽类（如新总线协议）时请同步更新 §2 表与本节交叉链接。*
