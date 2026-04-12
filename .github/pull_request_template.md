环境与合并前底线、CI 双轨说明：**[CONTRIBUTING.md](../CONTRIBUTING.md)** · 维护者**文档主线表**：[docs/README · 文档主线](../docs/README.md#docs-spine) · 架构术语（**`run_id`** vs **`site_version`** 等）：**[CONTRIBUTING.md · 术语与契约](../CONTRIBUTING.md#contributing-terminology)** · 合并/发布一页清单：**[MERGE_AND_RELEASE_CHECKLIST.md](../docs/MERGE_AND_RELEASE_CHECKLIST.md)**。

## 术语（请在描述中区分，避免混谈）

- [ ] 已区分本次变更涉及的是 **分析运行**（`run_id` / 快照）还是 **站点发布线**（`site_version` / `site-meta`），或注明「均不涉及」

## 合并前与 CI 对齐（推荐）

- [ ] 已执行 **`make merge-ready`**（**`validate`** + **`test-readonly-api`** · **`test_readonly*.py`** + **`test-admin-console`**），或注明环境限制 / 纯文档-only 且已 **`make validate`**

## 变更类型（删无关项）

- [ ] 仅 HTML/CSS/文案
- [ ] 若改**枢纽页首屏**（`page-head`）：已对照 **`p.lead` + `read-hint.page-head-deck` 分层**与路径条可读文案（**[SITE_REVIEW_THREE_PASSES.md §3.5](../docs/SITE_REVIEW_THREE_PASSES.md)** · **[ARCHITECTURE_ONE_PAGER · 内容与呈现](../docs/ARCHITECTURE_ONE_PAGER.md)**），或注明「非枢纽页 / 未触达首屏」
- [ ] `evolution-manifest.json` / `evolution-candidates.json`
- [ ] 脚本 / CI / Makefile
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
- [ ] 若改全站顶栏或 skip-bar：已更新 **`partials/site-nav.inc.html`** / **`partials/skip-bar.inc.html`** 并执行 **`make sync-nav`**；若同时改 **SPA 壳**（**`spa/src/SpaLayout.tsx`**、**`spaRouteMeta.ts`**、**`LegacyFrame.tsx`**）：快捷链与 **skip-bar** 同序，且总览 hash（含 **`#read-guide`**）的 **标题 / 读屏 / iframe `title`** 已对照 **AGENTS.md** 双轨条，或注明「未触达壳层」

## 若本周期处理了分析引擎的 evolution_hints

- [ ] 已在 **`assets/evolution-hint-decisions.json`** 追加对应记录（或注明为何本轮无提示可处理）；填写 **`rule_id`** 时须与 **`evolution-hint-rules.json`** 中某条 `id` 一致

## 备注

<!-- 可选：链接相关 issue、说明为何否决某条候选等 -->
