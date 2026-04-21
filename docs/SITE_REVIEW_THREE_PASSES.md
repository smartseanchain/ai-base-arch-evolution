# 全站模块 · 三轮梳理（标题 / 内容 / 版式与图形）

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)。

对根目录内容页（不含 `404`、`legacy-all-in-one`）做**结构对照**，标出**不合理 / 不匹配**与**建议优先级**。结论：**无单点「错误」居多**，主要是**模式不统一**与**少数命名落差**，可按 P0→P2 分批收敛。**主链验收入口 · 仓库物理分层**（`partials/`、`assets/`、`spa/` 等同轮改动）：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（**0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。

---

## 第一轮：信息架构 — 模块标题、顶栏与元数据

### 1.1 顶栏文案 vs 页面 `<h1>`

| 顶栏链接 | 典型 `<h1>` | 判断 |
|----------|-------------|------|
| 历史演进 | 基础设施形态演进 | **有意落差**：导航短、标题具体；`og:title` 用「历史演进」与顶栏一致，分享卡片与进入页后首屏标题不同——**可接受**，若要强一致可把 `og:title` 改为与 h1 同长句（SEO 会变长）。 |
| 分层模型 | 分层与模型 | 一致。 |
| 人与AI演进 | 教育·职业·人与AI：演进与走向 | h1 更完整，**合理**。 |
| 整体改造 | 整体智能化改造 | 「智能化」在 h1 多出，与顶栏「整体改造」略差；**P2** 可选统一为「整体改造」或顶栏改为「整体智能化改造」。 |

### 1.2 是否有「三色图例条」`nexus-legend`

- **有图例**：立体联结、综合推演、职基能、模块图谱、战略舆情、进化闭环、分析引擎、可进化架构、智能进化、整体改造、社会责任、十年之问、人与AI演进等（**管道/方法论枢纽页**为主）。
- **无图例**：**总览 index**（卡片矩阵，**合理**）、**历史演进、廿年视角、地缘与商业、分层模型、十年展望、十年场景、架构拓扑、沙盘工坊**等。

**判断**：无图例页多为**单主题工具页或时间轴页**，不一定硬套「依据/扩展/想象」三语义；若强行统一图例，**反而稀释** nexus 方法论地位。**建议**：维持现状；仅在**新页**设计时按「是否三色叙事」决定是否加 `nexus-legend`。

### 1.3 本页目录 `nav.toc`

- **有 TOC**：可进化架构、分析引擎、进化闭环、战略舆情、模块图谱、智能进化、整体改造、社会责任等**长文枢纽**。
- **无 TOC**：timeline、risk-geo、model、lab、decade、decade-scenes、architecture 等**节数少或线性滚动**页。

**判断**：**匹配内容长度**，无需全员 TOC。

---

## 第二轮：内容语义 — 术语、交叉引用、与工程文档对齐

### 2.1 三色标签**文案**并不全局统一

- **nexus / net-biz / edu-nexus** 等：**依据 / 扩展 / 想象**（方法论原教旨）。
- **分析引擎、进化闭环、可进化架构** 等：**观测 / 编码 / 反哺**或**聚合 / 分析 / 反哺**——与**同一 CSS 类名**（`evidence` / `extend` / `imagine`）绑定，**语义已换场景**。

**判断**：**类名统一、文案按页定制**是合理产品设计；风险是**新编辑误以为**全站同一套中文。  
**建议（P1）**：✅ 已写入 [ARCHITECTURE.md · 三色标签](./ARCHITECTURE.md#nexus-tag-labels) 与 [CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd) 自检表：**`nexus-tag` 三色类可承载不同中文标签，以各页 `nexus-legend` 为准。**

### 2.2 §11 / 三问 / 沙盘 交叉链

- 枢纽页（综合推演、沙盘、进化闭环、分析引擎）**互链较密**，整体**健康**。
- **工程向**读者：index 三问、可进化架构、分析 hub 已链 **`docs/ARCHITECTURE.md#seven-layers`**；**P2** ✅ **`modules-map`** 与 **`smart-overhaul`** 的 `read-hint` 已补 **ARCHITECTURE 全文（文首 Mermaid 简图）** + 七层映射 + 分析引擎全景，与上列入口并列。

### 2.3 `title` / `meta description` / `h1`

- 抽查 **timeline**：title「历史演进」与 h1「基础设施形态演进」——与 1.1 同，**社交分享用短名、正文用专名**，可接受。

---

## 第三轮：排版、图形与展示

### 3.1 主图 SVG 与无障碍

- **多数**大示意图带 `aria-label`（如 work-infra-energy、modules-map、synthesis 部分、decade-scenes、decade-us）。
- **部分**装饰性或小 SVG **无** `aria-label`——若处于信息主链，**建议补**；纯装饰可 `aria-hidden="true"`（**P2** 按页扫）。

### 3.2 图例条无障碍（已优化一版）

- 曾有约 **12** 页 `nexus-legend` **无** `aria-label`，与 nexus / net-biz **不一致**。  
- **已统一**补充 `aria-label="三色标签说明"`（与 `nexus.html` 对齐）；`edu-nexus` 原「标签」改为同一文案。

### 3.3 版式组件

- **`page-head` + `lead` + `card`** 在全站主流页**一致**，**好**。
- **index** 使用 **hub 卡片 + SVG 地图**，**刻意不同**，**合理**。

<a id="section-3-5-lead-readhint"></a>

### 3.5 页头导语分层与正文链接（P1 · 已部分落地）

与 **[AGENTS.md · 枢纽首屏](../AGENTS.md#agents-hub-lead)**（自动化助手收束）及 **[ARCHITECTURE_ONE_PAGER · 内容与呈现](./ARCHITECTURE_ONE_PAGER.md)** 互证。

- **长枢纽页 / 总览与工具页**（含 **index 总览**、立体联结、教育纵轴、综合推演三页、分析引擎、可进化架构、沙盘、战略·舆情、进化闭环、模块图谱、社会责任、人与 AI 演进、整体改造、智能进化、十年之问/展望/场景、网·商·资·工、廿年视角、职基能、历史演进、分层模型、架构拓扑、地缘与商业）：**`p.lead`** 只保留「本页一句定位 + 最短必要机制」；判据/深读/双轨对账、数据侧读数、概念对齐、边界声明、同读页等收入 **`<div class="read-hint page-head-deck" role="note">`** 内分段 `<p><strong>小标题</strong>：…</p>`，避免首屏单段过长。
- **首屏下「图例 / 流程条 / 推演扩展 / pill 目录」**：与上条 **互补**——优先复用 **`modular-intro-stack`**、**`nav.toc.toc--pilot`**、命令向 **`card--action-module` / `workbench-split`** 等（**不**替代 `lead`/`read-hint` 语义），契约与分工见 **[INTELLIGENCE_SIX_DOMAINS · §2.2](./INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**；与 **`site-data-bus`** 总线读数对读 **[SITE_DATA_UPDATE_FRAMEWORK](./SITE_DATA_UPDATE_FRAMEWORK.md)**。
- **正文地标（复查）**：根目录读者页以 **`<main id="main">`** 包住 **`</header>` 之后、`<footer>` 之前**的主体，与 skip-bar **`#main`**、**`site-data-bus.js`** 动态回顶链一致，**每页仅一个 `<main>`**；规范句见 **[ARCHITECTURE_ONE_PAGER · 内容与呈现](./ARCHITECTURE_ONE_PAGER.md#content-presentation)**。
- **样式真源**：`assets/site.css` 中 **`.page-head .read-hint.page-head-deck`** 控制与 `lead` 的间距；正文区链接**不要**在 HTML 上写 `style="color:var(--accent)"`，交给 **`.page-head .lead a`、`.read-hint a`、section 内链接规则**统一呈现（与焦点环、hover 一致）。图例色块、网·商·资·工关键词柱、总览卡片缩略说明等已逐步收拢为 **`.phase-legend-swatch*`、`.icbw-kw-*`、`.hub-card-visual-caption*`** 等类，避免重复内联。**综合推演配方卡**左边条色用 **`.synth-recipe--stripe-*`**；**辅文段/列表**与 **`<pre>` 命令行**用 **`.muted.note-*`、`.muted.list-*`、`.pre-code-inline*`**（`scripts/migrate_muted_inline_styles.py` 可对新页做同类替换；**不**处理 `legacy-all-in-one.html` 的空格差异）。

### 3.6 深链锚点与「推演扩展 · 本轮提要」（惯例）

- **hub 卡 / 读站指路** 可使用 `#锚点` 直达正文关键节（如 `timeline.html#timeline-five-eras`、`past-future.html#past-future-comparison`、`decade.html#decade-six-dim`、`decade.html#decade-phase-bars` 等）。
- 多数内容页的 **「推演扩展 · 本轮更新」** 卡片位于该深链**之上**；**惯例**：深链落地后仍建议**快速扫一眼本轮提要**，再精读下文，避免跳过维护节奏与对表要求。
- **总览** `index.html#read-guide` 已提示上述顺序；**综合推演主篇**各 major § 节首可配 **「读后自问」** 一句，与分区 `hub-band-prompt` 同构。

### 3.4 动态 JSON 展示

- **evolution.js / analysis.js** 依赖 **http(s)**，多页已提示 `file://` 限制；**进化闭环**另加 **closure-summary**，**一致**。

---

## 汇总：优先级建议

| 优先级 | 项 | 动作 |
|--------|----|------|
| **P0** | 图例条 a11y | ✅ 已：补全 `nexus-legend` 的 `aria-label` |
| **P1** | 三色文案多义 | ✅ 已：[ARCHITECTURE.md · 三色标签](ARCHITECTURE.md#nexus-tag-labels)；[CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd) 常见变更自检表增行 |
| **P1** | 枢纽页 `lead` 过长 | ✅ 已部分：**总览 index**、上列页 + **历史演进、分层模型、架构拓扑、地缘与商业、十年展望/场景** 等采用 **短 `lead` + `read-hint page-head-deck`**（`decade-scenes` 附注与 `read-hint` 同构）；**404** 附常用入口 **`read-hint`**（含读站指路）；其 **skip-bar** 手维护，**`sync_site_nav`** 不写回；**legacy-all-in-one** 导语拆分并在页内 CSS 对齐 `read-hint` 外观（不引用 `site.css`）。规范与链接勿手写 accent 见 **§3.5** |
| **P2** | 顶栏「整体改造」 vs h1「整体智能化改造」 | ✅ 已：`smart-overhaul` 的 h1 / `<title>` / `og:title` 与顶栏统一为「整体改造」，导语标明智能化方向 |
| **P2** | timeline 分享标题 vs h1 | ✅ 已：**`<title>` / `og:title` / `twitter:title`** 与顶栏短名一致（「历史演进」）；**`og:description`** 点出正文 **h1「基础设施形态演进」**；进入页后以 h1 为专名 |
| **P2** | 缺 TOC/legend 的页 | **不建议**为统一而统一；新页按内容选型 |
| **—** | 架构文档 · 适应度函数 / 血缘 / PR 追溯 | ✅ 已：`ARCHITECTURE.md` 三节 + `EVOLUTION_RUNBOOK` 增补；`analysis-snapshot.run` + `validate_analysis_snapshot_schema.py` + `docs/schemas/analysis-snapshot.schema.json`；**`scripts/run_validate.sh`** 统一 `make validate` / pre-commit / CI |
| **P2** | 主链 SVG `aria-label` | ✅ 已部分：上列各图 + `modules-map` 七层剖面与四路径串联、`nexus` 尺度影响与反馈环、`edu-nexus` 家校政三角·生命周期·AI 触点链（均外层 `role="img"` + 内层 `svg aria-hidden`）。**例外**：`modules-map` 模块星丛与场景轮含可点击 `<a>`，保留根 `svg` 的 `aria-label`，**不**在外层加 `role="img"`；已为星丛各块与场景轮外环链接补 `aria-label`。另：`index` 总览大图内层 `role="img"` + 栅格卡片缩略 `svg aria-hidden`；`net-biz-capital` 主链图由整段 `aria-hidden` 改为可播报；`past-future` 架构对照·形态图标·雷达·情景缩略图补齐；`edu-nexus` §1 四阶与师生双向流同模式；`synthesis` 毗邻图·三簇·§11 循环；`work-infra-energy` 三示意；`decade-us` 四象；`decade-scenes` 热力矩阵；`past-future` 廿年双轨大图；`evolution-triad` 三轨 SVG 滚动区；**`legacy-all-in-one`** 参考架构节外层原有 `role="img"`，内层 `svg` 已补 `aria-hidden` 与分页站一致 |

---

<a id="four-perspectives-review"></a>

## 四角色复查与读者预期（落地清单）

与 [PLATFORM_CAPABILITY_MAP · §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release) 摘要互链；大改呈现或增页后建议按本节约谈「是否符合预期」。

### 产品经理 · 顶栏与记忆负荷

- **注册表一致性**：顶栏链接数与 **`evolution-registry.json`** 对齐，**27 链并列**是刻意取舍（全站可发现性优先），窄屏由 **`site.css`** 换行承载。
- **枢纽记忆口诀（给读者）**：不必死记全栏——优先记住 **五枢纽**：**总览**（`index.html`）→ **立体联结** 或 **模块图谱** → **综合推演** → **分析引擎** → **沙盘工坊**；其余从分区速跳或检索进。总览 [读站指路](../index.html#read-guide) 已写入口分层。
- **后续可选（需产品定稿）**：顶栏分组、折叠菜单或 SPA 侧分组 **不**在本清单内实施；定稿后再开专门改版。

### 领域专家 · 深链与本轮提要

- 与 **§3.6** 一致：从 hub 卡或读站指路 **深链进正文** 后，仍建议扫一眼该页 **「推演扩展 · 本轮提要」**（若存在），再精读，避免跳过维护节奏与对表要求。

### UI / 设计 · 装饰图与内联

- 主链示意图按 **§3.1 / §3.5**；余页可按需扫：**纯装饰 SVG** 用 **`aria-hidden="true"`**；减少新建页 **`style=`** 内联色链。

### 测试与质量 · 自动化边界

- **结构不漂移**：**`make validate`**（含 registry、nav、skip/404、快照与沉淀 Schema、**`test_readonly*.py`** 于 CI）覆盖脚本与契约；**不替代**全站视觉回归。
- **发布前轻量人工清单**（大版本或改顶栏/总线后建议逐项勾）：  
  - [ ] 抽 **2～3 个分页** 点顶栏，**当前页**高亮与 **`class="current"`** 一致。  
  - [ ] 浏览器 **窄窗**（如宽度 390px）看顶栏 **换行**与 **三问 / 分区** 仍可点。  
  - [ ] 打开 **总线** 页（如 `analysis-hub`），确认 **`data-site-meta-version`** 与 **`site-meta.json`** 意图一致（若本版要升 **`site_version`**）。  
  - [ ] 任点一条站内 **`docs/*.md`**（见下节），在 **实际部署环境**（如 GitHub Pages）下确认 **可接受** 或改链说明。  
  - [ ] 若有 **SPA 发布**：抽一条壳内路由与 **iframe** 内分页标题是否可读。
  - [ ] 若本版改了根目录 **`*.html`**（读站指路、页脚、**`analysis-hub`** 导读等）且仍维护 **SPA**：已 **`make spa-sync`**（或 **`make spa-build`**），确认 **`spa/public/`** 与 **`public/docs`** 与 MPA 一致；动线见 **[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[关系视图](../maintainer-hub.html#mh-spine-map)** · **[系统边界](../maintainer-hub.html#mh-boundaries)** · **[衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)**。

### 站内链到 `docs/*.md` 与 GitHub Pages

- 多页从 HTML 使用相对路径链到 **`docs/*.md`**。在 **GitHub Pages 以仓库根为站点根** 部署时，浏览器请求 **`…/docs/FOO.md`** 通常返回 **原始 Markdown 文本或下载**，**不等同**于 github.com 上的 Markdown 渲染页。
- **读者预期管理**：深度文档可在 **GitHub 仓库网页**阅读，或 **克隆仓库** 本地读 **`docs/`**；站内链仍保留以便「真源路径」与贡献者一致。
- **维护者**：若某部署目标 **必须** 浏览器内友好阅读长文，再评估 **薄 HTML 导读页** 或外链 blob（单独立项，非本清单范围）。

---

## 维护建议

- **改顶栏 / skip-bar 模板**：只动 **`partials/site-nav.inc.html`** / **`partials/skip-bar.inc.html`**，再 **`make sync-nav`** → **`make validate`**（见根 [README](../README.md) · [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)）。**`maintainer-hub.html`** 五链后三页内 skip 由 **`build_skip_bar`** 生成，勿在 HTML 手改。**`404.html`** 不在 `sync_site_nav` 写回范围，失页顶栏/skip 须**手调**。
- **大改某一类版式**：优先改 **`assets/site.css`** 与 **单页试点**，再横向推广。
- **重审本文**：重大增页或改版后做一轮 **diff 对照本清单**即可。
