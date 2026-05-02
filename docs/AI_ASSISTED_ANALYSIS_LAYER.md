# 方法论分析 + 可配置 AI 解读层

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

本文与 **[ARCHITECTURE.md](./ARCHITECTURE.md)**（数据流、**`analysis_engine` 不写 HTML**）、**[DATA_CONTRACTS.md](./DATA_CONTRACTS.md)**（快照契约）、**[PLATFORM_EXTENSIBILITY](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#invariants)**（不变量）、**[USER_ADMIN_SPLIT · §1c](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#front-three-sources)**（前台三源）对齐，说明：**数据分析结论**如何在**确定性方法论产出**之上，**可选地**叠加 **AI 服务**生成的解读，以及如何通过**配置**接入外部模型，而不削弱闸门与人审语义。**站内「AI + 自动进化」全文收束**（overlay · 黄金集 · 草稿插槽 · 管道节奏；**非**全自动改 manifest）：**[docs/README · #ai-assisted-evolution](./README.md#ai-assisted-evolution)** · **[INTELLIGENCE · §8](./INTELLIGENCE_SIX_DOMAINS.md#ai-era-alignment)**。

**已实现（契约层）**：**`docs/schemas/ai-analysis-overlay.schema.json`**、**`validate_ai_analysis_overlay_schema.py`**（并入 **`make validate` / `make test`**）、**`write_ai_analysis_overlay_stub.py`**（向后兼容入口）、**`write_ai_analysis_overlay.py`**（默认跳过；**`--stub`** 占位；**`AI_OVERLAY_ENABLE=1`** + **`AI_OVERLAY_API_BASE`** / **`AI_OVERLAY_API_KEY`** 时可选调用 OpenAI 兼容 **`/v1/chat/completions`**，见 **`evolution_pkg.ai_overlay_write`**）。**合并前仍须**：密钥仅 env、overlay **不**进快照必填域；外呼失败默认软回退（**`AI_OVERLAY_ON_FAILURE`**，见下文检查单）。**只读 GET** **`/ai-analysis-overlay`** 已随磁盘路由注册。**主链联动 · 仓库物理分层**（`assets/` 叠加层与脚本闸门对读）：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（**0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。**自动化助手（overlay 不替代人审 · 分析边界）**：[AGENTS.md · 人审闸门](../AGENTS.md#agents-invariants) · [架构边界](../AGENTS.md#agents-arch-boundary) · [合并前](../AGENTS.md#agents-pre-merge)。**呈现双轨（`spa-sync` / `spa-build`）**：[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map)。**MPA 顶栏模板（`partials/`）**：**`make sync-nav`**；**`404.html`** 手调（`sync_site_nav` 不写回）— **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

<a id="ai-assisted-overlay"></a>

---

## 1. 为什么要拆成两层

| 层 | 职责 | 典型载体 |
|----|------|----------|
| **方法论层（确定性）** | 可重复、可 diff、可进 **`make validate`** 的统计与规则产物（热力、共现、**`evolution_hints`**、闭环缺口等） | **`assets/analysis-snapshot.json`**（及沉淀/趋势） |
| **AI 解读层（可选、概率性）** | 在自然语言或结构化摘要中**综合**快照与业务语境，辅助人读；**不**替代规则真源与 manifest | 建议**独立 JSON 产物**（见 §3），与快照**并列**消费 |

**原则**：

1. **不把 LLM 输出并入 `analysis-snapshot.json` 的必填域**，避免 CI 对非确定性文本做强闸门时抖动或掩盖确定性指标。  
2. **AI 不直接写 `evolution-manifest.json`、不写候选真源**；与 **[AGENTS.md](../AGENTS.md#agents-invariants)** 人审不变量一致。  
3. **叙事类长文草稿**仍优先走 **`scripts/draft/`**（[README](../scripts/draft/README.md)）；本层侧重**「对当日/近期分析结果的解读与对照」**，与纯页面草稿分流。  
4. **密钥与 endpoint** 只出现在**环境变量或密钥管理器**，**不进**静态管理页、**不进**提交的 JSON（示例见 **`docs/examples/ai_analysis_overlay.example.json`**）。

---

## 2. 前台如何呈现「方法论 + AI」

与 **[USER_ADMIN · §1c.1](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#front-three-sources)** 一致：读者页的**动态部分**仍只 **GET** 已部署 JSON。

推荐呈现约定：

- **默认展示**方法论层：**`analysis-snapshot.json`**（及 hub/总线已有逻辑）。  
- **若存在** AI 产物（§3），以**独立区块**展示（例如「AI 辅助解读」折叠面板），并**显著标注**：模型名、生成时间、**非审计结论**、与 **`run_id` 对齐**。  
- **禁止**把 AI 文案冒充为与 **`evolution_hints`** 或 manifest 条目**同一权威等级**的「系统结论」。

---

## 3. 建议的产物形态（独立文件）

在实现阶段推荐新增（名称可调整，但须**独立 Schema**）：

| 文件（建议） | 角色 |
|--------------|------|
| **`assets/ai-analysis-overlay.json`** | 可选；由**独立管道步骤**在 **`analysis-snapshot.json` 生成之后**写入；内含 **`run_id` 对齐**、**`provider` 元数据**、**`sections[]` 或 `summary_md`** 等 |

**优点**：`validate_analysis_snapshot_schema.py` 与 **`analysis_engine --check`** 保持纯粹；AI 步骤失败**不**阻断确定性快照；可按环境 **省略该文件** 发布。

**只读 API**：已注册 **`GET /ai-analysis-overlay`**（磁盘 **`assets/ai-analysis-overlay.json`**；无文件 **404**）与 **`GET /ai-overlay-step`**（**`artifacts/ai-overlay-step.json`** 侧车遥测；未跑步骤则无文件 **404**），与 [INTEGRATION · 路由一览](./INTEGRATION_AND_READONLY_API.md) 及 **`admin-console`** **`READONLY_PROXY_SEGMENTS`** 对表；**不**混用 **`/snapshot`** 的语义。

---

## 4. 可配置接入：配置放哪、写什么

### 4.1 推荐组合

| 项 | 建议 |
|----|------|
| **开关与非敏感参数** | 仓库内**示例**或**默认关闭**的配置模板（如 **`docs/examples/ai_analysis_overlay.example.json`**）；若团队需要提交「团队默认关闭」的模板，可后续增加 **`scripts/ai_analysis_overlay.config.json`** 并**单独**做 Schema + 校验（**勿**把 API Key 写入）。 |
| **密钥与 endpoint** | **仅** `AI_OVERLAY_*` 等环境变量（或 CI Secrets / K8s Secret）。 |
| **Provider** | `openai_compatible` / `azure_openai` / `anthropic` / `custom` 等枚举由实现选定；配置里只写 **kind** 与 **env 变量名**，不写密钥值。 |

### 4.2 管道挂载点

与 **[EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md)**、**`evolution_pkg.pipeline.runner`** 对表：**`make analyze` / `evolution-fast`** 在 **`analysis_engine --check` 之后**、**`validate_ai_analysis_overlay_schema` 之前**运行 **`scripts/write_ai_analysis_overlay.py`**（步骤 id **`write_ai_analysis_overlay`**）。默认**不写盘、不联网**（未设置 **`AI_OVERLAY_ENABLE=1`** 时退出 0）；启用时读 **`assets/analysis-snapshot.json`** 与可选 **`assets/sediment-trends.json`**，调用外部 API 后写 **`assets/ai-analysis-overlay.json`**。该步骤**不**并入 **`analysis_engine.py`**。

- **失败策略**（环境变量 **`AI_OVERLAY_ON_FAILURE`**）：**`stub`**（默认，回退占位 overlay）、**`skip`**（不写文件）、**`fail`**（非 0 退出，阻断流水线）。

---

## 5. 与扩展性插槽的对表

在 **[PLATFORM_EXTENSIBILITY · §2](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#extension-slots)** 中，本能力落在：

- **契约层**：新 **`ai-analysis-overlay.schema.json`** + **`validate_*`** + **`run_validate.sh`**（若文件存在则校验，或默认跳过）。  
- **管道步骤**：**`evolution_pkg.pipeline`** 增一步；遥测可记 **token 用量**（**不入**业务 manifest）。  
- **展示消费方**：**`analysis-hub`** / 总线登记（[SITE_DATA_UPDATE_FRAMEWORK](./SITE_DATA_UPDATE_FRAMEWORK.md)）。  
- **治理**：若解读对外发布，建议 **PR 审阅 overlay 样例**或 **仅内网展示**，避免未审模型输出直接进入公共叙事。

---

## 6. 落地检查单（维护者）

- [x] **Schema 与校验**：overlay 独立契约；**不**扩展 `analysis-snapshot` 的 `required`（**`validate_ai_analysis_overlay_schema.py`**；存在 overlay 时与快照 **`run_id` 对账**）。  
- [x] **可选外呼**：**`write_ai_analysis_overlay.py`** + env（**无密钥进 Git**）；扫描与 pre-commit 规则与团队策略一致。  
- [x] **血缘**：overlay 内 **`source_run_id`** 与 **`analysis-snapshot.json`** 的 **`run.run_id`** 在校验脚本中对账（快照缺失时仅验 Schema）。  
- [x] **前台文案**：**`analysis-hub`** 经 **`analysis.js`** 独立区块展示，含免责声明与 **`run_id`** 不一致提示。  
- [ ] **成本与合规**：日志保留、不向模型发送 PII/未授权正文；遵守供应商条款。  
- [x] **管理端**：**`admin-console`** **`pipeline_links`** 已链本文；**不**在匿名页填 Key。

---

## 7. 延伸阅读

- [DATA_CONTRACTS.md · §4](./DATA_CONTRACTS.md) · 当日分析快照  
- [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md) · 分析域与前端域分工  
- [REFERENCE_DESIGN_OPINION_MONITORING.md](./REFERENCE_DESIGN_OPINION_MONITORING.md) · 舆情类开源作**参考引用**时的侧车、管道步骤与 manifest 边界（与本层 overlay 衔接）  
- [scripts/draft/README.md](../scripts/draft/README.md) · 叙事草稿插槽（与解读层分流）  
- [ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md) · 管理端边界  

---

*随实现迭代；首次合入 overlay 产物或配置真源路径时，须同步 **DATA_CONTRACTS**、**schemas/README**、**run_validate.sh** 与 **readonly_api** 路由说明。*
