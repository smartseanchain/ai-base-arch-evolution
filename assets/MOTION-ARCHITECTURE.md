# 动效与读者路径架构（前端）

全站样式以 `site.css` 为主入口；**人与 AI 演进页**（`body.page-triad-future`）在 `evolution-triad.html` 中**额外**加载 `triad.css`（大门、脊、步进器、五站、廊道叠加与 `motion-corridor` 专用规则）。**滚动揭示**基线（`phase-bar`、`triad-block-in` 等）仍在 `site.css`，供其它使用 triad-rail 的页面共用。

## 1. 分层总览

| 层 | 职责 | 文件 / 入口 |
|----|------|-------------|
| 设计令牌 | 色阶、景深、`--motion-persp*`、`--ease-out-*`、`prefers-reduced-motion` 下的关闭规则 | `site.css` `:root` 起首块 |
| 全站滚动揭示 | `section`、`.wrap` 下直接的 `.scene-journey` 绑定 `IntersectionObserver`，打上 `motion-scroll-target` / `is-revealed` | `motion.js` |
| 廊道模式 | `body.page-triad-future` 时给 `<html>` 加 `motion-corridor`，与默认「景深推入」叠加为斜向廊道感 | `motion.js` + `triad.css` 中 `html.motion-corridor` |
| 演进页专用 | 大门入场、五步站点、光带 `--corridor-fill`、脊上五钉、epoch 氛围、`aria-current` | `journey-stepper.js`（仅 `page-triad-future`） |
| 演进页结构 | `section.triad-station`、`triad-station__deck`、站牌、`triad-gate-strip`、SVG 滚动容器等 | `evolution-triad.html` + `triad.css`（及 `site.css` 中 `.triad-rail` / `.fai-hub` 等基线） |

## 2. `motion.js` 契约

- 退出条件：`prefers-reduced-motion: reduce` 时整段不执行；`change` 时 `teardown` 移除 `motion-scroll`、`motion-corridor` 与目标类。
- 交错延迟：演进页 `34ms × index`，其余页 `26ms × index`（上限 16 段）。
- 与 CSS 配套：查找 `html.motion-scroll`、`.motion-scroll-target`（`site.css`「滚动揭示」）、`html.motion-corridor`（`triad.css`）。

## 3. `journey-stepper.js` 契约

- **前置条件**：`document.body.classList.contains('page-triad-future')`，否则立即返回。
- **站点 ID 顺序**（与步进器 `href`、脊上钉一致）：`evo-edu` → `evo-career` → `fai-merge` → `directions` → `cross`。
- **同步**：`setEpoch`（`body.epoch-corridor | epoch-now | epoch-future`）、`syncStationState`（`.triad-station` 的 `is-station-current` / `is-station-past`）、`corridorFill`、`updateSpineMarks`。
- **大门**：`#corridor-gate` 动画结束后再 `kick()`（时长与 `triad.css` 中 `.corridor-gate--opening` keyframes 对齐）。

## 4. 维护提示

- 增删演进页「站点」时：同时改 **五处** HTML（`section` id、`journey-stepper` 链接、`.corridor-spine-mark` 数量）、`journey-stepper.js` 中 `STATION_IDS` / `epochLabels`、站牌文案。
- 改大门时长时：同时改 **`GATE_MS`**（默认 `1500`，见 `journey-stepper.js`）与 `triad.css` 中 `.corridor-gate--opening` 各子动画（当前最长约门扇 `1.36s` + 延迟、`layer-fade` `1.42s`）；`GATE_MS` 应略大于实际最长结束时间，避免 `kick()` 过早。
- 演进页样式：`triad.css` 已独立；改 `site.css` 设计令牌时注意 `triad.css` 仍依赖 `:root` 变量。

## 6. 与数据闭环（manifest / 分析）的关系

- **读者动效**（本文件 §1–2）与 **观测—manifest—分析** 管道**无代码共享**；运维命令见仓库 `scripts/README.md`（`make ingest` / `make analyze`）。

## 5. 与「可进化架构」数据闭环的关系

- **内容侧**：观测 → manifest → 分析 → 沉淀，见 `evolvable-architecture.html`、`evolution-loop.html`。
- **读者侧**：`evolution-triad.html` 用动效表达「驻足、长廊、时代/行业双门」，**不**与 `evolution-manifest.json` 管道共享运行时，仅产品与叙事上对照。
