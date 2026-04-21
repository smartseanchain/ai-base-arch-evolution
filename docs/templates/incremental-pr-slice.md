# PR 切片模板（增量构建）

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../../README.md#pm-four-journeys) · [README · 从这里开始](../../README.md#readme-start-here) · [README · 双轨真源](../../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](../ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](../ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](../../CONTRIBUTING.md#contributing-pr-evidence-triad)。

从 **[INCREMENTAL_BUILD_PLAYBOOK · §5](../INCREMENTAL_BUILD_PLAYBOOK.md#pr-slice-template)** 复制到 PR 描述；与 **[INTELLIGENCE_SIX_DOMAINS · §6 PR 自检](../INTELLIGENCE_SIX_DOMAINS.md#pr-checklist)**、**[PLATFORM_EXTENSIBILITY · 新增能力检查单](../PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist)** 合并使用。**整体内容框架** / **前后台** / **组件×主链**：[docs/README · #content-framework](../README.md#content-framework) · [#front-back-modules](../README.md#front-back-modules) · [#system-components-fusion](../README.md#system-components-fusion)。**判型入口**（主线 **0c**）：**[docs/README · #quick-paths](../README.md#quick-paths)**。**自动化助手**：[AGENTS.md · 合并前](../../AGENTS.md#agents-pre-merge) · [框架判型](../../AGENTS.md#agents-content-framework) · [人审闸门](../../AGENTS.md#agents-invariants)。**呈现双轨（`spa-sync` / `spa-build`）**：[README · 双轨真源](../../README.md#readme-dual-track-map) · [MERGE · §1](../MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](../MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../../maintainer-hub.html#mh-spine-map)。**MPA 顶栏模板（`partials/`）**：**`make sync-nav`**；**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 生成，勿手改 HTML；**`404.html`** 手调（`sync_site_nav` 不写回）— **[scripts/README · `sync_site_nav`](../../scripts/README.md)** · **[真源摘要 · #sync-site-nav-source](../../scripts/README.md#sync-site-nav-source)**。

```markdown
## 抽象粒度（五维 / 六域 / 七类）
- [ ] 已读本 PR 在 **[勿混粒度 · 五维/六域/七类](../PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** 中的定位（与 **[CONTRIBUTING · 术语](../CONTRIBUTING.md#contributing-terminology)** 对读），或注明「纯文案 / 不涉架构粒度」

## 域（INTELLIGENCE §6）
- [ ] 数据  [ ] 管道  [ ] 分析  [ ] 前端  [ ] 运维  [ ] 治理

## 本 PR 骨架（已完成）
- [ ] Schema / validate 入口
- [ ] 单测或 smoke
- [ ] 文档（DATA_CONTRACTS / INTEGRATION / DOCKER 择一）

## 读者面版式 vs 总线（触及 `assets/site.css` 或枢纽 `.html` 骨架时）
- [ ] 已按 **[INTELLIGENCE · §2.2](../INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** 自检；**未**误更 **[SITE_DATA_UPDATE_FRAMEWORK](../SITE_DATA_UPDATE_FRAMEWORK.md)** 消费方表（**无**新 **`[data-site-data-live]`** 时）；**或**注明「不涉及版式 / 已登记总线」

## MPA 全站顶栏与失页（触及 `partials/` 或 `404.html` chrome 时）
- [ ] 已 **`make sync-nav`**；**`maintainer-hub.html`** 五链后页内 skip **未**在 HTML 手改（由 **`build_skip_bar`** 生成）；若动 **`skip-bar`** 或失页顶栏须与模板一致，已**手调** **`404.html`** — [MERGE · §1](../MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](../MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)
- [ ] 或注明「本轮未改 `partials/` / 失页 chrome」

## 跨层与物理分层（触及多目录或新主链依赖时）
- [ ] 已对照 **[PROJECT · §1b](../PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**（必要时 **[§1a](../PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)**），或注明「单目录 / 不涉及」

## 故意延后（后续 PR）
- …

## 验证
- [ ] make validate
- [ ] （推荐合并前）make merge-ready（**`validate`** + **`test-readonly-api`** · **`test_readonly*.py`** + **`test-admin-console`**）
- [ ] 已与 **[AGENTS.md · 合并前](../../AGENTS.md#agents-pre-merge)** 对读（`merge-ready` / **`make test`** 子集 vs **`validate`** / 人审）或注明环境限制
```
