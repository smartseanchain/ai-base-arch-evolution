# 舆情类系统：参考引用设计（本仓落地边界）

本文把 **GitHub 等开源「舆情 / 热点 / 多源情报」类产品** 定位为 **架构与产品模式的参考引用**，**不**作为子模块或拷贝源码并入本仓库。设计与 **[ARCHITECTURE.md](./ARCHITECTURE.md)**（数据流、人审）、**[SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](./SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md)**（脚本/API 边界）、**[AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md)**（AI 解读层）、**[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)**（只读路由）对齐。

---

## 1. 参考引用声明（必须遵守）

| 项 | 约定 |
|----|------|
| **性质** | 下述外部仓库仅作 **模式对照**（聚合、筛选、推送、Agent 报告等）；**不**在本文档中承诺 fork、vendor 或许可证继承。 |
| **许可证** | 常见舆情项目多为 **GPL** 等强著佐权许可；**若将来评估代码复用**，须在独立 PR 中做 **许可证兼容** 审查，**不**默认合并。 |
| **合规** | 多源采集、爬虫、平台 API 须遵守 **robots、ToS、频率与地域法规**；本仓 **ingest** 路径以 **RSS 等显式允许源** 为主，**不**把「全网爬虫」写进主链默认行为。 |
| **真源** | **`evolution-manifest.json`** 仍只经 **人审 + PR**；参考系统常见的「自动写库 / 自动定调」**不**映射为本仓主链。 |
| **确定性** | **`analysis_engine`** 产出仍以 **可重复统计与规则** 为主；舆情类 **LLM/Agent 长文** 仅可作为 **可选叠加**（见 §4）。 |

**示例性外部项目（仅列举，不构成背书或依赖）**：

- 热点聚合、关键词筛选、推送、可选 MCP/LLM：**[sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)**（及同类 fork；实现与协议以对方仓库为准）。
- 多 Agent、报告生成、社媒采集架构：**[666ghj/BettaFish](https://github.com/666ghj/BettaFish)**（GPL；仅作「Agent 分工 / 报告结构」参考）。

维护者可将其他项目按同样规则记入 **团队内部清单**；**无需**在每次架构讨论中更新本文 URL 列表。

---

## 2. 模式映射表（参考 → 本仓落点）

| 舆情系统常见能力 | 本仓推荐落点 | 禁止/慎用的落点 |
|------------------|--------------|-----------------|
| 多源归一、时间序列、热度 | 与 **`analysis-snapshot`**、**`sediment`/`trends`** 的统计维度 **类比**；新增指标走 **Schema + `analysis_engine`** 或独立摘要 JSON | 直接改 **`analysis-snapshot`** 必填域塞入非确定性大段文本 |
| 关键词 / 话题 / 订阅 | **`ingest_config.json`**、**`maps_to_hints.json`**、规则 **`evolution-hint-rules.json`**；抓取仍走 **ingest 脚本族** | 管理端 **POST** 直接改仓库 JSON（违反当前边界；见 **ADMIN_WEB_CONSOLE_ROADMAP**） |
| 情感 / NLP / 聚类 | **可选侧车**：独立脚本或服务，产出 **带 `run_id` 的附加 JSON**；或走 **`ai-analysis-overlay`** 契约（**[AI_ASSISTED_ANALYSIS_LAYER](./AI_ASSISTED_ANALYSIS_LAYER.md)**） | 写入 **`evolution-candidates`** / **manifest** 而不经人审 |
| 告警、推送、看板 | **admin-console** 观测、外部 **ntfy/邮件/IM**（独立部署）；或未来编排（**[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)**） | 在 **`readonly_api`** 上开放匿名触发写盘 |
| 多 Agent 研究报告 | **外部作业**：生成 **Markdown/PDF + 摘要 JSON**；人审后 **手工**或 **PR** 纳入站点/候选 | Agent **自动 merge** manifest 或绕过 **`review_state`** |

---

## 3. 推荐集成形态（按侵入性递增）

下列为 **设计选项**，实施须单独 PR + 契约，**不**视为本文已实现的代码路径。

### 3.1 零侵入：仅文档与配置类比

- 在 **ingest** 或 **数据源目录**（**`admin-console/data/data_source_catalog.json`**）侧，用舆情系统的 **「源清单 + 过滤策略」** 思路优化 **RSS/法规源** 的配置结构说明。  
- **交付物**：文档、示例配置片段；**无**新服务。

**已落地（本仓轻量借鉴）**：**`scripts/ingest_config.json`** 可选数组 **`json_feeds`**（HTTPS GET + JSON，**`items_path`** 指向条目数组，**`keys_*`** 可覆写字段名）；由 **`scripts/ingest_opinion_law.py`** 与 RSS/法规同源合并进 **`evolution-candidates.json`**，仍经 **`routes` / `maps_to_hints`** 与 **人审**；解析纯逻辑在 **`evolution_pkg.ingest_json_http`**。**不**内置任何第三方 API URL；**不**在配置中展开密钥头（避免 secret 入库）。

### 3.2 侧车服务（推荐用于重采集 / GPL 栈）

- 独立进程或仓库：负责 **聚合、推送、可选 LLM**；通过 **只读消费** 本仓已发布 JSON（**`GET /snapshot`** 等）或 **Git 拉取**，**不向本仓主 API 写**。  
- 若需把「线索」送回本仓：仅允许 **生成符合 `evolution-candidates` Schema 的片段**，由人 **粘贴/PR** 或 **未来**经显式人审 UI 提交（仍非自动 merge）。  
- **交付物**：侧车 README、网络边界说明；本仓 **不** vendor 其代码。

### 3.3 本仓内可选管道步骤（轻量 NLP / 摘要）

- 在 **`analysis_engine` 成功写快照且 `--check` 通过之后**，增加 **可选步骤**（与 **AI_ASSISTED_ANALYSIS_LAYER §4.2** 一致）：读快照 → 调用外部 API → 写 **`assets/ai-analysis-overlay.json`**。  
- **失败策略**：默认 **软失败**，不阻断确定性管道。  
- **交付物**：独立脚本 + **`evolution_pkg.pipeline.runner`** 注册一步 + Schema/校验已存在则复用。

---

## 4. 与 AI 解读层、只读 API 的衔接

- **AI 长文/报告**：优先落在 **`ai-analysis-overlay`**（或未来并列 Schema），**[前台呈现约定](./AI_ASSISTED_ANALYSIS_LAYER.md#2-前台如何呈现方法论--ai)**（折叠、标注非审计结论、对齐 **`run_id`**）。  
- **只读暴露**：沿用 **`readonly_api`** 已有 **`GET /ai-analysis-overlay`**；**admin-console** 代理白名单已与 **`READONLY_PROXY_SEGMENTS`** 对表（见 **INTEGRATION**、**admin-console** README）。  
- **敏感段**：与 **`/candidates`、`/hint-decisions`、`/ingest-config`** 同类，**网关侧**控制暴露面，**不**因「舆情」需求默认对公网全开。

---

## 5. 验收与文档维护

- 新增任一「参考舆情能力」的 **代码路径** 时，须在 PR 中说明：  
  - 是否 **侧车** 或 **本仓步骤**；  
  - 是否触碰 **manifest/候选真源**；  
  - **许可证与合规** 结论（若引入第三方代码）。  
- 更新 **`docs/README.md`** 索引（本页路径）；重大行为变更时同步 **AI_ASSISTED** / **SCRIPTS_APIS** / **DATA_CONTRACTS** 交叉链接。

---

## 6. 相关文档

| 文档 | 关系 |
|------|------|
| [AI_ASSISTED_ANALYSIS_LAYER.md](./AI_ASSISTED_ANALYSIS_LAYER.md) | 可选 AI 产物形态与管道挂载点 |
| [SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](./SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md) | 脚本 vs 只读 API vs 不宜 API 化的族 |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 数据流、适应度函数、`analysis_engine` 边界 |
| [ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md) | 管理端管道 UI 与数据源叙事 |
| [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md) | 只读路由扩展方式 |

---

*本文档为 **参考引用设计**：固化「可学什么、接到哪、不能做什么」；外部 GitHub 项目链接可能变更，以对方仓库为准。*
