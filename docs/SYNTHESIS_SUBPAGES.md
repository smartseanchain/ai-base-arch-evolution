# 综合推演 · 分子页说明

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

原单文件 `synthesis.html`（约 1300 行）已拆为**三页**，顶栏仍只保留「综合推演」入口（`synthesis.html`），子页从主篇 TOC 与页脚进入。**推演叙事与工程 JSON/脚本落点对照**：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（**0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。**自动化助手（动 `.html` 叙事时）**：[枢纽首屏](../AGENTS.md#agents-hub-lead) · [架构边界](../AGENTS.md#agents-arch-boundary) · [合并前](../AGENTS.md#agents-pre-merge)。**呈现双轨（`spa-sync` / `spa-build`）**：[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map)。

| 文件 | 内容（原章节） | 适用读者 |
|------|----------------|----------|
| [synthesis.html](../synthesis.html) | §1—§5、§10（模块表、判据、毗邻、合成轴、配方 A—H、工作台） | 先建立全站变量与判据 |
| [synthesis-extensions.html](../synthesis-extensions.html) | §6—§9（叠加五域与 I—V、复合表、三簇、五维切片） | 叠乘域、表行、形态分叉 |
| [synthesis-methods.html](../synthesis-methods.html) | §11—§13（持续迭代插槽、跨学科办法、深读透镜） | 迭代纪律与研究套路 |

**站外锚点迁移**（书签与文档链接已批量替换）：

- `synthesis.html#perpetual` → `synthesis-methods.html#perpetual`
- `synthesis.html#methods` → `synthesis-methods.html#methods`
- `synthesis.html#deep-lens` → `synthesis-methods.html#deep-lens`
- `synthesis.html#stack-domains` / `#matrix` / `#forks` / `#dimensions` → `synthesis-extensions.html#…`

主篇仍保留 `#inventory`、`#criteria`、`#graph`、`#axes`、`#recipes`、**`#continuation`（继续推演 · 全站深描矩阵）**、`#workflow`。

**再拆分**：若 `modules-map.html` 或 `legacy-all-in-one.html` 仍觉过长，可按本模式增子页并更新 `scripts/evolution-registry.json` 与 `scripts/gen-sitemap.py` 的 `PRIORITY`。

**重建页面**（从当前三页反推不推荐；仅当需从旧单文件重生时）：仓库内 `scripts/_build_synthesis_subpages.py` 曾用于首次切分，日常维护请直接编辑三个 HTML。
