---
name: 流水线 / 校验失败排查
about: 本地或 GitHub Actions 失败时的自检清单（也可用于讨论定时任务告警 Issue）
title: "[triage] "
labels: []
---

开 Issue 前可先看环境与合并前底线、CI 双轨说明：**[CONTRIBUTING.md](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/CONTRIBUTING.md#contributing-env-and-cmd)** · **四条动线**：[README · 产品视角](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/README.md#pm-four-journeys) · [README · 从这里开始](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/README.md#readme-start-here) · [README · 双轨真源](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/README.md#readme-dual-track-map) · **架构师五步**：[ARCHITECTURE_ONE_PAGER · #architect-stewardship](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · **不变量索引**：[ONE_PAGER · #architect-invariants-index](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · **PR 证据三联**：[CONTRIBUTING · #contributing-pr-evidence-triad](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/CONTRIBUTING.md#contributing-pr-evidence-triad)。**docs 主链三锚**：[整体内容框架 · #content-framework](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/README.md#content-framework) · [#front-back-modules](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/README.md#front-back-modules) · [#system-components-fusion](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/README.md#system-components-fusion) · [判型 · #quick-paths](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/README.md#quick-paths)。**自动化助手（合并真源 · 人审闸门）**：[AGENTS.md · 合并前](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/AGENTS.md#agents-pre-merge) · [人审闸门](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/AGENTS.md#agents-invariants)。若在讨论**编排器 / Kafka / 生产库**等改造与 CI 分工，先对表 **[按阶段升级执行指南](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/PHASED_UPGRADE_EXECUTION_GUIDE.md#execution-now)** 与 **[升级决策全景图](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/ARCHITECTURE_UPGRADE_ROADMAP.md#upgrade-panorama)**（Fork 后请将文首链改为本仓库 `blob/main` 路径）。**主链联动与验收入口 · 仓库物理分层**：[勿混粒度 · 五维/六域/七类](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain) · [PROJECT · §1a](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · [§1b](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)。

**多篇都写「技术栈」时先选主链**（简版 vs 详版 + 附录）：**[docs/README · #tech-stack-read-merge](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/README.md#tech-stack-read-merge)** · **[TECH_BRIEF · 详版附录](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)**（[旧文件名别名](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/TECH_ARCHITECTURE_CAPABILITIES.md#tech-capabilities-alias)）。

**壳内页面仍像旧版 MPA**（iframe 页脚/读站未更新）：改根 **`*.html`** 后是否已 **`make spa-sync`** — [MERGE · §1](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/maintainer-hub.html#mh-spine-map) · [系统边界](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/maintainer-hub.html#mh-boundaries) · [衔接矩阵](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/maintainer-hub.html#mh-reader-admin-matrix) · [spa/README](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/spa/README.md)。

**`validate` 报顶栏 / skip-bar 漂移**（`sync_site_nav --check`）：是否已 **`make sync-nav`**；**`maintainer-hub.html`** 五链后三锚须由 **`build_skip_bar`** 生成、**未**在 HTML 手改；**`<!-- 真源… -->` 注释**仅能在 **`partials`** 内 skip/header 块中，勿在块外重复（见 [scripts/README · #sync-site-nav-source](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/scripts/README.md#sync-site-nav-source)）；若刚改 **`partials/`**，**`404.html`** 顶栏/skip 须**手调**（脚本不写回）— [MERGE · §1](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [CONTRIBUTING · 常见变更自检](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/CONTRIBUTING.md#contributing-common-changes-checklist)。

## 失败场景

- [ ] `make validate` / pre-commit
- [ ] **CI · spa-build**（仅当 PR 改了 `spa/`、registry、sync 输入等才运行；未改则 **skipped** 属正常，合并以 **validate** 为准）
- [ ] `make ingest` / **Ingest candidates** workflow
- [ ] `make analyze` / **Update pipeline** workflow
- [ ] 其他：<!-- 简述 -->

## 环境

- 本地 OS：
- Python 版本（`python3 --version`）：

## 已尝试

- [ ] 已看 Actions 对应 Run 的日志与 Job Summary
- [ ] 本地复现：<!-- 命令与末 20 行 stderr -->

## 日志摘要

```
粘贴关键报错
```

## 备注

<!-- 链到失败的 workflow run、相关 PR 等 -->
