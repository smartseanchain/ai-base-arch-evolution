# 科学研究与推演方法：与站内能力匹配表

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)。

本文回答三件事：**当前文档里已经收纳了哪些研究/推演套路**、它们**落在站内哪里**、以及**哪些可以真正「用起来」**（页面、沙盘、JSON 管道、命令）——与 [DEDUCTION_STRATEGY.md](./DEDUCTION_STRATEGY.md)（认识论与单轮流程）、[综合推演 §12](../synthesis-methods.html#methods)（跨学科表）、[§13](../synthesis-methods.html#deep-lens)（深读透镜）互补；**不重复** §12 全文，只做**匹配与可利用性**分级。**推演架构**与工程对表的总入口见 **[ARCHITECTURE_ONE_PAGER · 三架构对照](./ARCHITECTURE_ONE_PAGER.md#three-architectures)**。**主链联动 · 仓库物理分层**：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（**0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。**自动化助手（人审 · `make test` 子集 vs `validate`）**：[AGENTS.md · 人审闸门](../AGENTS.md#agents-invariants) · [子集](../AGENTS.md#agents-test-subset) · [合并前](../AGENTS.md#agents-pre-merge)。**呈现双轨（`spa-sync` / `spa-build`）**：[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map)。**MPA 顶栏与失页**：**`partials/`** → **`make sync-nav`**；**`404.html`** 手调（`sync_site_nav` 不写回）— **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

## 中枢入口：分析引擎页

**整体梳理（方法 + 演进策略 + JSON 字段导游）**以站内 **[分析引擎 · 方法与演进总线](../analysis-hub.html#panorama)** 为默认起点：该页把 OODA、§11 插槽 ⑦—⑨、hint 闭环、适应度函数、多源综合台与 §12 读数方式汇成两张总表，并链接本文与 `DEDUCTION_STRATEGY`。读完后再下钻本仓库各 `docs/*.md` 与 [综合推演](../synthesis.html)。

<a id="tiers"></a>

## 1. 可利用性三级（先读这段）

| 级别 | 含义 | 典型手段 |
|------|------|----------|
| **A · 站内核可用** | 有**可执行路径**：页面交互或仓库脚本/JSON 契约可直接参与你的流程 | 沙盘因子与依赖流、`evolution-manifest` / 候选、`analysis-snapshot`、ingest、validate、`make analyze` |
| **B · 结构可用** | **无专用软件**，但站内**章节与表格**已为该套路预留「落笔位置」；产出应是可指回 §2 的文本/表行 | §5 配方分叉、§7 复合表增行、§8 三簇、§9 五维切片、多源综合台 |
| **C · 需自建** | 学科标准流程（问卷、仿真、计量）**本站不内置**；仅说明**产出应对回**哪一节以免飘在术语层 | 德尔菲问卷、系统动力学仿真、回归/IV 等 |

**纪律**（与 §12 一致）：一轮主动只用 **1–2** 种套路；凡选 B/C，仍须能翻译成 **变量注 → [§2 判据](../synthesis.html#criteria) → 传导句 → 征候句**。

<a id="matrix"></a>

## 2. 方法 ↔ 站内落点 ↔ 可利用什么（总表）

下列与 [综合推演 §12 表](../synthesis-methods.html#methods) **行一一对应**，右两列为本页增补。

| 领域或传统（§12） | 在本站的主要落点 | 可利用性 | 具体能用什么 |
|------------------|------------------|----------|--------------|
| 战略与情景规划 | §8 三簇、§5 甲/乙/丙、[十年场景](../decade-scenes.html) | **B** | 用页面结构写多情景 + 征候；无情景树软件 |
| 技术预见 / 德尔菲类 | §1 变量表；团队自建流程 | **C** | 问卷/会议在站外；结论填 §1 或 §7 行 |
| 系统动力学 / 控制论 | §3 毗邻、各配方传导链、延迟叙述 | **B** | 定性反馈环；**无**存量—流量仿真器 |
| 复杂适应系统（思想） | [立体联结](../nexus.html)、§6 叠加域、多方主体 | **B** | 尺度与主体叙事；涌现须落到 §9 可见切片 |
| 因果推断（DAG、反事实） | §2 判据、改配方**一个前提** | **B** | **逻辑**可证伪与混杂追问；**无** DAG 工具与估计量 |
| 历史与制度分析 | [历史演进](../timeline.html)、[廿年视角](../past-future.html) | **B** | 时间轴与词汇锁定；须写清机制对应哪段链 |
| 工程可靠性（FTA / FMEA） | [沙盘 · 依赖流](../lab.html)、§7「谁先绷紧」 | **A** | **依赖流 SVG**、多因子勾选、与 §7 行对读 |
| 运筹与敏感性分析 | 沙盘多因子、§7 行向量 | **A** | **沙盘**作主观排序与边界情景；前提变则序变 |
| 政策过程 / 倡议联盟 | [十年展望](../decade.html)·治理、[人与AI演进](../evolution-triad.html)、地缘叙事 | **B** | 叙事与联盟结构写在正文/表行；无政策网络数据库 |
| 微观行为与离散选择（思想） | [十年之问](../decade-us.html) 四问、约束与异质性 | **B** | 检查约束是否写漏；**不拟合**离散选择模型 |
| 质性研究 / 民族志 | §9 五维形态、可见切片、配方征候句 | **B** | 厚描变「可复核切片」；不进 CAQDAS |
| 危机管理 / 红队 | 沙盘加压、[地缘](../risk-geo.html) 最坏情景、§11 追问 | **A+B** | **沙盘** + 写作纪律：**红队结论应增 §7 行或配方分叉** |

### 2.1 §13「深读透镜」算哪一类？

[§13](../synthesis-methods.html#deep-lens) 的**四穿透**（技术—组织—市场—治理）与**六凝视者**是**元阅读法**，不是独立学科模型：可利用性为 **B**（强制你从多层补变量，防单页过度自信）。与上表**叠加使用**，不单独占「一轮一种」名额。

### 2.2 多源政策—资本—舆论综合推演

[战略·舆情 · §6 多源综合台](../national-strategy-opinion.html#integrated-deduction) 把法律、规划期、舆情、全球资本、多国政策与 **manifest / 分析枢纽 / 沙盘** 写成一条工作台：其中 **ingest → 人审 → merge**、**analysis_engine**、**lab** 为 **A**；链路与甲/乙/丙形态为 **B**。

<a id="pipeline"></a>

## 3. 工程侧：与「研究方法」对齐时可用的资产

若要把推演**可追溯**到仓库（而不仅是读后感），下列与 [ARCHITECTURE](./ARCHITECTURE.md) 一致：

| 资产 / 命令 | 在研究流程中的用途 |
|-------------|-------------------|
| `scripts/ingest_opinion_law.py` + `evolution-candidates.json` | **观测编码**的入口；法规/RSS 标题级线索进池，**须人审**后 merge |
| `merge_candidates_to_manifest.py` | 升格为正式 `evolution-manifest.json` 信号，绑定 `maps_to` / `lab_factors` |
| `scripts/analysis_engine.py` + `assets/analysis-snapshot.json` | **结构校验**：模块热力、因子共现、规则提示、`hint_closure_gaps`（与 `evolution-hint-rules.json` / `evolution-hint-decisions.json`） |
| `data/sediment.json` + `sediment_trends.py` | **跨日**对比：是否长期偏斜某一模块或因子 |
| `lab.html` + `assets/lab.js` | **思想实验**与 FMEA/敏感性叙述的交互落点 |
| `make validate` / `scripts/run_validate.sh` | **适应度函数**：防止页、**`evolution-registry.json`** 结构（**`validate_evolution_registry_schema.py`**）、语义对账、快照与 **沉淀/趋势** 契约、**nav.config↔navLinks** 漂移 |
| `make test` | 同上之**子集**：registry Schema、单测、**navLinks**、沉淀/趋势 Schema（**无**完整对账、顶栏、**`--check`**）；合并前仍须 **`make validate`** |
| `docs/schemas/evolution-registry.schema.json` + `validate_evolution_registry_schema.py` | **注册表**字段与类型契约（先于 **`check_manifest_drift`**） |
| `docs/schemas/analysis-snapshot.schema.json` + `jsonschema` | 快照与展示端**契约**（见 `requirements.txt`） |

**不是**计量平台：不做回归、不做系统动力学数值积分；**是**「定性研究 + 可版本化证据 + 守门脚本」的组合。

<a id="routing"></a>

## 4. 按问题类型速查（与 §12.1 一致，补可利用性）

| 你的问题 | 优先套路（§12） | 建议先用 |
|----------|----------------|----------|
| 谁先失效、单点在哪 | FTA/FMEA + 运筹敏感 | **A**：lab 依赖流 + 沙盘 |
| 同一国内体验为何分裂 | CAS + 制度 + 四问不同步 | **B**：nexus、decade-us、§8 |
| 是否漏第三变量 / 混杂 | 因果推断思想 + §2 | **B**：改前提口述反事实 |
| 叙事过乐观或过悲观 | 情景规划 + 红队 | **B** + **A**：对立征候 + 沙盘加压 |
| 政策与舆论谁牵引谁 | 政策过程 + 双轨 + 多源台 | **B** + **A**：战略·舆情 §6 + manifest/分析 |

<a id="paradigms"></a>

## 5. 与常见「研究范式」的弱对照（仅供定位）

本站**不按**实证/诠释/批判范式收稿，但若你习惯这样自检：

- **实证主义（假设—检验）的弱对应**：用 **征候句**与**可观察切片**代替 p 值；用 **改前提断链**代替识别假设讨论。
- **诠释/建构**：允许，但 **依据层**仍须可指回公开文本或站内核 JSON，避免纯独白。
- **参与式/行动研究**：站外进行；**C** 级；若产出要进站，仍走候选—人审—manifest。

---

**维护**：新增 §12 行或新管道时，同步更新本表「可利用性」列与 [延伸阅读](./DEDUCTION_STRATEGY.md#site-map)。
