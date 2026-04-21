# 动效与读者路径架构（前端）

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](../docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship)。

全站样式以 `site.css` 为主入口；**人与 AI 演进页**（`body.page-triad-future`）在 `evolution-triad.html` 中**额外**加载 `triad.css`（脊、步进器、五站、epoch 氛围；**大门入场默认跳过**，动效与全站其他页同档简化，见 `triad.css` 文末覆盖块）。**滚动揭示**基线（`phase-bar`、`triad-block-in` 等）仍在 `site.css`。**`assets/` 与根 MPA 在仓库物理分层中的位置 · 主链验收入口**：**[勿混粒度 · 五维/六域/七类](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1b](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout) · **[§1a](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)**（改 CSS/JS 后仍须 **`make validate`**）。**整体内容框架** / **前后台** / **组件×主链**：[docs/README · #content-framework](../docs/README.md#content-framework) · [#front-back-modules](../docs/README.md#front-back-modules) · [#system-components-fusion](../docs/README.md#system-components-fusion)。**按改动判型**（**0c**）：[docs/README · #quick-paths](../docs/README.md#quick-paths)。**呈现双轨（`spa-sync` / `spa-build`）**（动根 **`.html`** 且维护 SPA 壳时）：[MERGE · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map)。**MPA 顶栏与失页**：**`partials/`** → **`make sync-nav`**；**`404.html`** 手调（`sync_site_nav` 不写回）— **[MERGE · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

## 1. 分层总览

| 层 | 职责 | 文件 / 入口 |
|----|------|-------------|
| 设计令牌 | 色阶、景深、`--motion-persp*`、`--ease-out-*`、`prefers-reduced-motion` 下的关闭规则 | `site.css` `:root` 起首块 |
| 全站滚动揭示 | `section`、`.wrap` 下直接的 `.scene-journey` 绑定 `IntersectionObserver`，打上 `motion-scroll-target` / `is-revealed` | `motion.js` |
| 廊道标记 | `body.page-triad-future` 时给 `<html>` 加 `motion-corridor`（仍用于类名）；**滚动揭示形态已与默认 `site.css` 对齐**，不再叠斜向廊道 transform | `motion.js` + `triad.css` 文末覆盖 |
| 演进页专用 | 五步站点、光带 `--corridor-fill`、脊上五钉、epoch 氛围、`aria-current`；`#corridor-gate` 仅保留 DOM，**默认 `corridor-gate--skip` 不播入场** | `journey-stepper.js`（仅 `page-triad-future`） |
| 演进页结构 | `section.triad-station`、`triad-station__deck`、站牌、`triad-gate-strip`、SVG 滚动容器等 | `evolution-triad.html` + `triad.css`（及 `site.css` 中 `.triad-rail` / `.fai-hub` 等基线） |

## 2. `motion.js` 契约

- 退出条件：`prefers-reduced-motion: reduce` 时整段不执行；`change` 时 `teardown` 移除 `motion-scroll`、`motion-corridor` 与目标类。
- 交错延迟：演进页 `34ms × index`，其余页 `26ms × index`（上限 16 段）。
- 与 CSS 配套：查找 `html.motion-scroll`、`.motion-scroll-target`（`site.css`「滚动揭示」）、`html.motion-corridor`（`triad.css`）。

## 3. `journey-stepper.js` 契约

- **前置条件**：`document.body.classList.contains('page-triad-future')`，否则立即返回。
- **站点 ID 顺序**（与步进器 `href`、脊上钉一致）：`evo-edu` → `evo-career` → `fai-merge` → `directions` → `cross`。
- **同步**：`setEpoch`（`body.epoch-corridor | epoch-now | epoch-future`）、`syncStationState`（`.triad-station` 的 `is-station-current` / `is-station-past`）、`corridorFill`、`updateSpineMarks`。
- **大门**：`#corridor-gate` 始终加 `corridor-gate--skip`，**立即** `kick()`（与全站模块页一致，无等待门扇动画）。

## 4. 维护提示

- **全站顶栏与 skip-bar**：维护 **`partials/site-nav.inc.html`** 与 **`partials/skip-bar.inc.html`**，再运行 **`make sync-nav`**（见仓库根 README）；勿在单页手改以免漂移。**`404.html`** 顶栏/skip **不在** `sync_site_nav` 写回列表，改模板后须**手调** **404** — [MERGE · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)。
- 增删演进页「站点」时：同时改 **五处** HTML（`section` id、`journey-stepper` 链接、`.corridor-spine-mark` 数量）、`journey-stepper.js` 中 `STATION_IDS` / `epochLabels`、站牌文案。
- 若需**恢复**大门入场：去掉 `journey-stepper.js` 里对 `corridor-gate--skip` 的强制、恢复延时 `kick()`，并核对 `triad.css` 中 `.corridor-gate--opening` 时长。
- 演进页样式：`triad.css` 已独立；改 `site.css` 设计令牌时注意 `triad.css` 仍依赖 `:root` 变量。

## 6. 与数据闭环（manifest / 分析）的关系

- **读者动效**（本文件 §1–2）与 **观测—manifest—分析** 管道**无代码共享**；运维命令见仓库 `scripts/README.md`（`make ingest` / `make analyze`）。

## 5. 与「可进化架构」数据闭环的关系

- **内容侧**：观测 → manifest → 分析 → 沉淀，见 `evolvable-architecture.html`、`evolution-loop.html`。
- **读者侧**：`evolution-triad.html` 用步进与脊轨表达「驻足、五站」；**读数条**由 `site-data-bus.js` 拉取 `analysis-snapshot` / 趋势，与全站数据管道一致；叙事动效**不**绑定 manifest 运行时。
