# 舆情、制度与国情 · 跟踪与反哺操作手册

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**本文侧重**：**ingest 信源分层**、外链与自动化边界、把线索**接进闸门与 PR**；判型合一见 [docs/README · #quick-paths](./README.md#quick-paths) 表内「情报 ingest · 管理控制台 · SPA 壳」行。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

**整体内容框架** / **读者面×管理面** / **组件串主链**：[docs/README · #content-framework](./README.md#content-framework) · **[#front-back-modules](./README.md#front-back-modules)** · **[#system-components-fusion](./README.md#system-components-fusion)**。

本文说明：**如何把「外部信息更新」接到本仓库的闸门与叙事里**，并约束**工作与生活**场景下的用法。  
**不是**法律/投资建议；**不**替代对原文、发文字号与时效的核对。

**主链与验收入口**：[PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · [勿混粒度](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)。**节奏与 artifact**：[EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md)。**数据源目录与拉取方式（管理端参考）**：[admin-console/data/data_source_catalog.json](../admin-console/data/data_source_catalog.json)（经 **`GET /api/bootstrap`** 下发）。**管理端边界**：[ADMIN_CONSOLE_FRAMEWORK_OVERVIEW · §1a](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#front-back-simple) · [§10 未实现](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-not-implemented)。**与 ingest / 管理端 UI / SPA 壳合一判型**（先 0c 再下钻）：[docs/README · #quick-paths](./README.md#quick-paths) 表内「情报 ingest · 管理控制台 · SPA 壳」行 · [INTELLIGENCE · §6 PR 自检](./INTELLIGENCE_SIX_DOMAINS.md#pr-checklist)。**呈现双轨（`spa-sync` / `spa-build`）**：[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map) · [系统边界](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)。**MPA 顶栏与失页**：**`partials/`** → **`make sync-nav`**；**`404.html`** 手调（`sync_site_nav` 不写回）— **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

---

<a id="intel-purpose"></a>

## 1. 目的与边界

| 要做 | 本仓库适合的方式 |
|------|------------------|
| 对**固定主题**（如算力、监管、地缘等）做**可审计**的线索池与叙事更新 | **`ingest`** + **`scripts/ingest_config.json`** 的 **`rss_feeds` / `json_feeds`** + **`routes`** 过滤 + **PR** + **`make validate`** |
| 把「读过什么、何时采纳」写进协作习惯 | 本手册的**节奏表** + **元数据模板** + **EVOLUTION_RUNBOOK** 周历 |
| **实时热搜、微博/主媒 App 时间线、需登录或付费墙的全文** | **不在**本仓 **`ingest_opinion_law`** 进程内做「模拟登录 / 爬站内信息流」；可选路径见 **[§2b](#intel-social-platforms)**（公开 RSS·官方开放平台 API·人工策展）。 |

---

<a id="intel-source-tiers"></a>

## 2. 信源分层（建议默认遵守）

1. **L1 制度与权威文本**（法规、征求意见稿、正式 PDF/HTML）  
   - **以人工打开门户 + 保存链接/文号/日期为主**；自动化仅作**提醒**，不当作已核对结论。  
   - 入口可参考管理端数据源目录中 **`regulatory_portal`** 类条目（外链由**浏览器**打开，见 [ADMIN_CONSOLE · 不变量](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#3-不变量对表是否符合仓库预期)）。

2. **L2 可机器低频拉取的公开 feed**（RSS/Atom、稳定 HTTPS JSON 侧车）  
   - 与 **`ingest_opinion_law.py`**、**GitHub Actions** 周历对齐；变更 **`ingest_config.json`** 仍须 **Git diff + PR**。  
   - **拉取方式选型**见 **`data_source_catalog.json`** 顶层 **`fetch_method_catalog`**（管理端「数据源参考」区块展示）。

3. **L3 国际与行业参考**  
   - 明确标注**语境差异**（跨境、版权、适用法域），避免直接等同为「境内制度结论」。

### 2a. 自动化拉取的运行约束（频率 · UA · 失败分类）

与常见 **ingest / RSS 聚合** 实践对齐，建议团队内约定：

| 主题 | 建议 |
|------|------|
| **请求间隔** | 脚本在每条 RSS / JSON / 法规 URL 之间已有 **sleep**（见 **`evolution_pkg.ingest_opinion_pool`**）；**GitHub Actions** 定时任务间隔不宜低于 **15–60 分钟** 量级，避免对源站形成突发并发；同一日历日内多次全量 ingest 通常**无必要**。 |
| **User-Agent** | 使用仓库默认 UA（**`evolution_pkg.ingest_fetch`**）；勿在配置中写入 **含密钥的 Header**；尊重对方 **robots.txt** 与 **ToS**。 |
| **失败分类（排障）** | **`ingest-summary.json`**（**`WRITE_INGEST_SUMMARY=1`**）按源列出 **`ok` / `error`**：**网络/超时**（`URLError`、`OSError`）多为可重试；**JSON 解析**（`JSONDecodeError`）多为侧车契约变更，应修配置或映射；**配置 URL** 未通过 **`validate_config_fetch_urls`** 属**契约错误**，须在合并前修 **`ingest_config.json`**。 |
| **间隔可配置** | 根 **`ingest_config.json`** 可选 **`fetch_pacing`**：**`after_rss_fetch`**、**`after_law_html_fetch`**、**`after_json_feed_fetch`**（秒，**0–120**；默认 **0.8 / 1.0 / 0.8**），由 **`evolution_pkg.ingest_opinion_pool`** 在每次成功 GET 后执行；与上表「请求间隔」一致。 |

<a id="intel-social-platforms"></a>

### 2b. 微博、主媒 App 流与「站内信息流」

与 §1 最后一行、**L2** 分工一致：**本仓库默认可自动化的 ingest** 面向 **RSS/Atom** 与 **`json_feeds` 可描述的稳定 HTTPS JSON**，不是社交平台时间线或热搜接口的通用爬虫。

| 诉求 | 建议 |
|------|------|
| **媒体/机构在官网提供的公开 RSS**，或**稳定、可文档化的 JSON 列表 URL**（与 **`json_feeds`** 映射一致） | **纳入 L2**：写入 **`scripts/ingest_config.json`** 的 **`rss_feeds` / `json_feeds`**，**`routes`** 收敛主题；合并前 **`make validate`**。 |
| **仅 App 内、登录后、或实时热搜级流** | **不纳入**当前 **`evolution_pkg.ingest_opinion_pool`** 的默认路径；避免对主站/移动站做未授权的页面级高频抓取（与 §2a **robots / ToS** 一致）。 |
| **平台官方开放平台 API**（需申请、OAuth、密钥与频控） | **视为独立集成**：密钥与 token **勿**写入仓库；可经侧车服务或人工导出后再接 **`json_feeds`** / 人工 PR；管理端「拉取方式」参考见 **`data_source_catalog.json`** · **`fetch_method_catalog`**（含 **`social_timeline_official`**）。 |
| **仍要把某条博文/报道纳入「进化」叙事或候选** | **人工优先**：按 **[§5](#intel-metadata)** 留标题、来源 URL、日期与是否进 manifest；走 **[§3](#intel-workflow)** 候选 → 人审 → 分析，与 **[AGENTS · 人审闸门](../AGENTS.md#agents-invariants)** 一致。 |

---

<a id="intel-workflow"></a>

## 3. 推荐工作流（接到本仓库）

1. **选源**：在管理端「数据源参考」勾选/浏览 → 导出 **RSS / json_feeds 草案** → 合并进 **`scripts/ingest_config.json`** → **PR**。  
2. **收敛**：用现有 **`routes`** 控制进入候选池的主题，避免池子被泛资讯淹没（与 [ingest 配置说明](../scripts/README.md) 对读）。  
3. **跑 ingest**：本地 **`make ingest`** 或依赖 CI **Ingest candidates** artifact（见 [EVOLUTION_RUNBOOK · 自动化周历](./EVOLUTION_RUNBOOK.md#github-actions-cadence)）。  
4. **人审进 manifest**：候选 → **`merge_candidates_to_manifest`** → **PR**；与 **[AGENTS.md](../AGENTS.md#agents-invariants)** 人审闸门一致；**不**跳过 [MERGE 清单](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) 与 **`review_state`** 语义。  
5. **分析与读者面**：**`make analyze`**；合并前 **`make validate`**（本地迭代可辅以 **`make validate-fast`** 省时间，**不可**替代与 CI、pre-commit 同源的全量 **`validate`**，见 **[ARCHITECTURE · `run_validate.sh` 与 fast 子集](./ARCHITECTURE.md#run-validate-gate)**）。通过后由 **`analysis-snapshot`**、站点总线等呈现；纯叙事 HTML 变更仍遵守 [DATA_ANALYSIS_SITE_CONTENT_SYNC](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md) 与 [INTELLIGENCE · 读者契约](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)。若本轮动全站顶栏 / **skip-bar** 模板：**`make sync-nav`**（**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 生成，勿手改 HTML）；**`404.html`** **不经** **`sync_site_nav`** 写回，须**手调** — **[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**。

---

<a id="intel-cadence"></a>

## 4. 建议节奏（可按团队改字，勿删「负责人」）

| 频率 | 动作 | 建议负责人 |
|------|------|------------|
| **每周** | 扫 L1 重点门户是否有新规/征求意见窗口；记录链接与截止日期 | 指定轮值 |
| **与 Actions 对齐** | 看 ingest artifact / 候选池增量是否符合 **`routes`** 预期 | 维护 ingest 的同学 |
| **双周 / 发版前** | **`make merge-ready`** 或等价闸门；复盘本周纳入的线索是否已进 manifest 或刻意丢弃 | 合并责任人 |
| **临时** | 重大政策或突发事件：加开一轮人工审阅，**不必**为「追热点」提高抓取频率以致违规 |

---

<a id="intel-metadata"></a>

## 5. 纳入叙事或内参时的最小元数据（建议字段）

在 PR 描述或内部笔记中至少保留：

- **标题 / 主题标签**（与 **`routes.match`** 或页面映射可对应）  
- **来源名称 + URL**  
- **抓取或阅读日期**（建议统一标注北京时间或 ISO8601「+08:00」）  
- **原文类型**（正式文件 / 新闻稿 / 评论 / 数据表）  
- **是否已核对文号或等效标识**（制度类）  
- **是否进入 `evolution-manifest` / 仅停留候选**  

AI 辅助归纳时：**事实断言仍以原文为准**；解读见 [AI_ASSISTED_ANALYSIS_LAYER](./AI_ASSISTED_ANALYSIS_LAYER.md) 边界。

---

<a id="intel-personal"></a>

## 6. 工作与生活场景（自律边界）

- **工作**：把本手册当作**协作契约**——谁更新 ingest、谁审候选、谁对对外表述负责。  
- **生活**：把公开资讯当作**决策参考之一**，而非唯一依据；控制订阅数量与推送频率，避免「伪实时」焦虑。  
- **本站与私域**：仓库内文档与页面**不**承担个人健康、投资、法律个案咨询职责。

---

<a id="intel-links"></a>

## 7. 相关文档（按需打开）

| 主题 | 文档 |
|------|------|
| 双周节奏与 Actions | [EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md) |
| 脚本入口与 `ingest_config` 说明 | [scripts/README](../scripts/README.md) · **§2b**（[#intel-social-platforms](#intel-social-platforms)：微博/主媒站内流边界） |
| 管道 UI 与数据源阶段 | [ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md) |
| 管理端能力与 HTTP 速览 | [ADMIN_CONSOLE_FRAMEWORK_OVERVIEW](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md) · [§4 HTTP](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-http-surface) |
| 运行与 env | [admin-console/README](../admin-console/README.md) |
| 数据契约与快照 | [DATA_CONTRACTS](./DATA_CONTRACTS.md)（**[`ingest_config` 表行](./DATA_CONTRACTS.md#ingest-config-contract)** · **`fetch_pacing`**） |
| 数据→读者呈现矩阵 | [DATA_ANALYSIS_SITE_CONTENT_SYNC](./DATA_ANALYSIS_SITE_CONTENT_SYNC.md) |
| 只读 API 与网关 | [INTEGRATION_AND_READONLY_API](./INTEGRATION_AND_READONLY_API.md) |
| 舆情类产品参考与暴露面 | [REFERENCE_DESIGN_OPINION_MONITORING](./REFERENCE_DESIGN_OPINION_MONITORING.md) |
| 读者 / 管理分拆 | [USER_ADMIN_SPLIT](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md) |
| 六域与智能化边界 | [INTELLIGENCE_SIX_DOMAINS](./INTELLIGENCE_SIX_DOMAINS.md)（延伸阅读亦回链本手册） |
| 合并 / 发布自检 | [MERGE_AND_RELEASE_CHECKLIST](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [AGENTS.md · 合并前](../AGENTS.md#agents-pre-merge) |
| 五条红线与 PR 复盘 | [ONE_PAGER · 不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [CONTRIBUTING · PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [CONTRIBUTING · 动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command) · [EVOLUTION · 证据三联](./EVOLUTION_RUNBOOK.md#pr-evidence-triad) |
| 真源分层与判型（0c） | [AGENTS.md · 框架](../AGENTS.md#agents-content-framework) · [docs/README · #content-framework](./README.md#content-framework) · [#front-back-modules](./README.md#front-back-modules) · [#system-components-fusion](./README.md#system-components-fusion) · [#quick-paths](./README.md#quick-paths) |
| 自动化助手 · 人审闸门 | [AGENTS.md](../AGENTS.md#agents-invariants) |
| 枢纽页 `lead` / `read-hint` | [SITE_REVIEW · §3.5](./SITE_REVIEW_THREE_PASSES.md#section-3-5-lead-readhint) · [AGENTS.md · 枢纽首屏](../AGENTS.md#agents-hub-lead) |
| **`make test` / `validate-fast` 子集** | [AGENTS.md · 子集](../AGENTS.md#agents-test-subset) · [ARCHITECTURE · fast 子集](./ARCHITECTURE.md#run-validate-gate) |
| 分析管道 vs 枢纽 HTML | [AGENTS.md · 架构边界](../AGENTS.md#agents-arch-boundary) |
| 读者链路与深链惯例 | [AGENTS.md · 读者惯例](../AGENTS.md#agents-reader-conventions) · [PLATFORM · §7 读者预期](./PLATFORM_CAPABILITY_MAP.md#reader-and-release) |
| 长文档索引（深读） | [AGENTS.md · 深读](../AGENTS.md#agents-deep-read) · [PLATFORM_MASTER_MAP · §1a](./PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces) |
| Cursor 规则映射 | [AGENTS.md · Cursor](../AGENTS.md#agents-cursor-rules) · [repo-gates.mdc](../.cursor/rules/repo-gates.mdc)（文首「子规则对读」）· [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map) · [CONTRIBUTING · Cursor / 子规则](../CONTRIBUTING.md#contributing-env-and-cmd) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) |
| 全量 **`validate`** 与本地 **`validate-fast`** | [ARCHITECTURE · `run_validate.sh` 与 fast 子集](./ARCHITECTURE.md#run-validate-gate) · [docs/README · 持续集成](./README.md) · [CONTRIBUTING](../CONTRIBUTING.md#contributing-env-and-cmd) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) |
| 贡献与常见变更表 | [CONTRIBUTING](../CONTRIBUTING.md#contributing-common-changes-checklist) |

---

*新增信源或改 ingest 频率时，请同步 **`ingest_config.json`**、**`make validate`** 与（如使用）**管理端数据源目录 JSON** 的免责声明表述，避免同事误读为「本站代抓外网」。*
