# 内容草稿插槽（`scripts/draft/`）

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../../README.md#pm-four-journeys) · [README · 从这里开始](../../README.md#readme-start-here) · [README · 双轨真源](../../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](../docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship)。

本目录用于**可选的**机器辅助产出（如 LLM 生成的 Markdown/HTML **片段**），供 **PR 人工审阅**后再迁入根目录 **`.html`** 或 `docs/`。**不**接入 `analysis_engine`、**不**自动写入 **`evolution-manifest.json`** 或任何 **`assets/*.json`** 真源（与 [ARCHITECTURE.md · 内容生成](../docs/ARCHITECTURE.md#seven-layers)、[AGENTS.md](../AGENTS.md#agents-invariants) 一致）。**主链联动 · 仓库物理分层**（迁入目标层与验收入口）：**[勿混粒度 · 五维/六域/七类](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**整体内容框架**：**[docs/README · #content-framework](../docs/README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](../docs/README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](../docs/README.md#system-components-fusion)。**按改动判型**（**0c**）：**[docs/README · #quick-paths](../docs/README.md#quick-paths)**。**技术栈文档**（简版 + **[详版附录](../docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)** · [别名](../docs/TECH_ARCHITECTURE_CAPABILITIES.md)）：**[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF](../docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)**。**AI 与「自动进化」全文收束**（本目录在能力链中的位置）：**[docs/README · #ai-assisted-evolution](../docs/README.md#ai-assisted-evolution)**。**呈现双轨（`spa-sync` / `spa-build`）**（迁入根 **`.html`** 后验壳）：[MERGE · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map)。

## 使用约定

- 除本 README 外，**`scripts/draft/`** 下本地文件默认 **不提交**（见仓库根 **`.gitignore`**）；若需**提交样例**，仅限脱敏、可审阅的短片段，并在 PR 中说明用途。  
- 合入正文前须满足：**`make validate`**、叙事与 **registry / 总线** 消费方一致；新分页仍走 **`evolution-registry.json`** 与 [PLATFORM_EXTENSIBILITY · 插槽](../docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#extension-slots)。  
- **可演进**：草稿流水线可逐步脚本化（例如 `scripts/draft/generate_*.py`），但每一步产出仍应可 diff、可拒绝；**智能化**体现在辅助起草与检查，**不**替代闸门。

## 与「自动进化」的关系

平台进化体现在**规则 JSON、契约版本、管道步骤、人审后的 manifest** 的迭代；本目录是**叙事侧**的可选加速器，**不是**第二条数据真源。

---

*若增加自动生成脚本，请在 [scripts/README.md](./README.md)「维护用 / 一次性工具」类中登记，并链回本文。*
