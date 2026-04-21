环境与合并前底线、CI 双轨说明：**[CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd)** · **四条动线（角色 → 第一站）**：[README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map) · **架构师五步**：[ARCHITECTURE_ONE_PAGER · #architect-stewardship](../docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · **五条红线**：[ONE_PAGER · #architect-invariants-index](../docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · **PR 证据三联**：[CONTRIBUTING · #contributing-pr-evidence-triad](../CONTRIBUTING.md#contributing-pr-evidence-triad) · 维护者**文档主线表**：[docs/README · 文档主线](../docs/README.md#docs-spine) · **真源分层**：[docs/README · #content-framework](../docs/README.md#content-framework) · **前后台按域**：[#front-back-modules](../docs/README.md#front-back-modules) · **组件×主链**：[#system-components-fusion](../docs/README.md#system-components-fusion) · **判型最短链**（**0c**）：[docs/README · #quick-paths](../docs/README.md#quick-paths) · **技术栈多篇怎么读**（简版 vs 详版 + 附录）：[docs/README · #tech-stack-read-merge](../docs/README.md#tech-stack-read-merge) · 架构术语（**`run_id`** vs **`site_version`** 等）：**[CONTRIBUTING.md · 术语与契约](../CONTRIBUTING.md#contributing-terminology)** · 合并/发布一页清单：**[MERGE_AND_RELEASE_CHECKLIST.md](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**。

## 术语（请在描述中区分，避免混谈）

- [ ] 已区分本次变更涉及的是 **分析运行**（`run_id` / 快照）还是 **站点发布线**（`site_version` / `site-meta`），或注明「均不涉及」
- [ ] PR 描述已标明本轮落在 **五维 / 六域 / 七类** 哪一类抽象（或「纯文案、无关架构粒度」），参见 **[勿混粒度 · 五维/六域/七类](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · **[CONTRIBUTING · 术语与契约](../CONTRIBUTING.md#contributing-terminology)**

## 合并前与 CI 对齐（推荐）

- [ ] 已执行 **`make merge-ready`**（**`validate`** + **`test-readonly-api`** · **`test_readonly*.py`** + **`test-admin-console`**），或注明环境限制 / 纯文档-only 且已 **`make validate`**
- [ ] （若触及 **`admin-console/`**）已对表 **[ADMIN_CONSOLE · §7](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**，或注明「未触及」

## 变更类型（删无关项）

- [ ] 仅 HTML/CSS/文案
- [ ] 若改根目录任意 **`*.html`**（读站指路、多页页脚、**`analysis-hub`** 导读等）且本 PR 仍维护 **SPA**：已 **`make spa-sync`**（或 **`make spa-build`**），见 **[MERGE · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[关系视图](../maintainer-hub.html#mh-spine-map)** · **[系统边界](../maintainer-hub.html#mh-boundaries)** · **[衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)**，或注明「未维护 SPA / 仅改 `spa/public` 外路径」
- [ ] 若改**枢纽页首屏**（`page-head`）：已对照 **`p.lead` + `read-hint.page-head-deck` 分层**与路径条可读文案（**[AGENTS.md · 枢纽首屏](../AGENTS.md#agents-hub-lead)** · **[SITE_REVIEW_THREE_PASSES.md §3.5](../docs/SITE_REVIEW_THREE_PASSES.md)** · **[ARCHITECTURE_ONE_PAGER · 内容与呈现](../docs/ARCHITECTURE_ONE_PAGER.md)**），或注明「非枢纽页 / 未触达首屏」
- [ ] 若**仅**改 **`assets/site.css`** 或 **[INTELLIGENCE · §2.2](../docs/INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** 所列枢纽版式类 / DOM 骨架（**无**新增 **`[data-site-data-live]`**、**无**新 JSON 读数路径）：已确认**不必**改 **[SITE_DATA_UPDATE_FRAMEWORK](../docs/SITE_DATA_UPDATE_FRAMEWORK.md)** 消费方表，或注明「本 PR 已登记总线 / 已加 live 占位」
- [ ] 若仅改 **`assets/site-data-bus.js`** 的**读者壳层**（顶缘进度、回顶 FAB、`data-no-reading-progress`）且**无**新 `fetch`：已对照 **[SITE_DATA_UPDATE · §3a](../docs/SITE_DATA_UPDATE_FRAMEWORK.md#reader-chrome)**，或注明「触及 live/JSON」
- [ ] `evolution-manifest.json` / `evolution-candidates.json`
- [ ] 脚本 / CI / Makefile
- [ ] **跨层改动**（`assets` / `scripts` / `evolution_pkg` / `spa` / `admin-console` / 根 MPA 等**多目录**或新依赖链）：已对照 **[PROJECT · §1b 仓库物理分层](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)** 与 **[§1a 主链联动与验证](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)**，或注明「单层 / 纯文案 / 不涉及」
- [ ] 若新增 **`scripts/evolution_pkg/`** 顶层子模块（`.py` 或子包）：已更新 **`evolution_pkg/domains.py`** · **`SUBMODULE_DOMAIN`**（否则 **`make test`** 失败），或注明「未新增子模块」
- [ ] 其他：<!-- 简述 -->

## 若涉及编排器 / 消息队列（Kafka 等）/ 生产级数据库或 CDC

- [ ] 已在 PR 描述中写明**目标阶段**（参见 **[按阶段升级执行指南](../docs/PHASED_UPGRADE_EXECUTION_GUIDE.md)**），并已对照 **[升级决策全景图](../docs/ARCHITECTURE_UPGRADE_ROADMAP.md#upgrade-panorama)**；**未**引入第二套与 **`run_validate.sh`** 脱节的合并闸门，或注明「纯文档 / 仅本地 PoC compose，不改变默认 CI」
- [ ] **不**自动写 **`evolution-manifest.json`**、**不**用 broker/库替代 **Git+PR** 作唯一审计源（见 **[ARCHITECTURE_UPGRADE · 反模式](../docs/ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#anti-patterns)**）

## 若涉及 manifest / 候选入库

- [ ] 入库条目的 `review_state` 已为 **`queued_for_manifest`**（噪点用 **`noise`**；默认 **`pending`**）
- [ ] 已本地执行 `make validate`（含对账与 `analysis_engine --check`）
- [ ] 每条新信号能回答「三问」判据（见站内 `evolution-loop.html` §5 · 人必须做什么）
- [ ] `maps_to.pages` 与 `lab_factors` 已人工核对；对账脚本无报错
- [ ] 若新增根目录 HTML 或沙盘因子：已同步 **`scripts/evolution-registry.json`** 与 **`assets/lab.js`**；若维护 **SPA**，已更新 **`spa/nav.config.json`** 并执行 **`make gen-nav-links`**（或 **`make spa-build`**，CI 在触及 registry/spa 时会跑 **spa-build**）
- [ ] 若改全站顶栏或 skip-bar：已更新 **`partials/site-nav.inc.html`** / **`partials/skip-bar.inc.html`** 并执行 **`make sync-nav`**（再 **`make validate`**）；**`maintainer-hub.html`** 五链后三页内 skip 由 **`build_skip_bar`** 生成，**未**在 HTML 手改；**`404.html`** 不在 **`sync_site_nav`** 写回列表，若失页顶栏/skip 需与模板一致则已**手调** **404**，或注明「未改 partials / 404 无需动」；**`<!-- 真源… -->`** 仅在 **`partials`** 内 **skip-bar / site-nav** 块中、**未**在块外重复（**[scripts/README · #sync-site-nav-source](../scripts/README.md#sync-site-nav-source)**）
- [ ] 若改全站顶栏或 skip-bar**且**改 **SPA 壳**（**`spa/src/SpaLayout.tsx`**、**`spaRouteMeta.ts`**、**`LegacyFrame.tsx`**）：**SPA** 快捷链前 **五** 链与 **skip-bar** 同序（壳内「跳到分页导航」等须在五链之后），且总览 hash（**`#read-guide`** / **`#three-questions`** / **`#hub-catalog`** / **`#index-intent-pick`** / **`#reader-next`**）的 **标题 / 读屏 / iframe `title`** 已对照 **[AGENTS.md · MPA+SPA 双轨](../AGENTS.md#agents-dual-track)**，或注明「未触达壳层」

## 若本周期处理了分析引擎的 evolution_hints

- [ ] 已在 **`assets/evolution-hint-decisions.json`** 追加对应记录（或注明为何本轮无提示可处理）；填写 **`rule_id`** 时须与 **`evolution-hint-rules.json`** 中某条 `id` 一致

## 备注

<!-- 可选：链接相关 issue、说明为何否决某条候选等 -->
