# 内容草稿插槽（`scripts/draft/`）

本目录用于**可选的**机器辅助产出（如 LLM 生成的 Markdown/HTML **片段**），供 **PR 人工审阅**后再迁入根目录 **`.html`** 或 `docs/`。**不**接入 `analysis_engine`、**不**自动写入 **`evolution-manifest.json`** 或任何 **`assets/*.json`** 真源（与 [ARCHITECTURE.md · 内容生成](../docs/ARCHITECTURE.md#seven-layers)、[AGENTS.md](../AGENTS.md) 一致）。

## 使用约定

- 除本 README 外，**`scripts/draft/`** 下本地文件默认 **不提交**（见仓库根 **`.gitignore`**）；若需**提交样例**，仅限脱敏、可审阅的短片段，并在 PR 中说明用途。  
- 合入正文前须满足：**`make validate`**、叙事与 **registry / 总线** 消费方一致；新分页仍走 **`evolution-registry.json`** 与 [PLATFORM_EXTENSIBILITY · 插槽](../docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#extension-slots)。  
- **可演进**：草稿流水线可逐步脚本化（例如 `scripts/draft/generate_*.py`），但每一步产出仍应可 diff、可拒绝；**智能化**体现在辅助起草与检查，**不**替代闸门。

## 与「自动进化」的关系

平台进化体现在**规则 JSON、契约版本、管道步骤、人审后的 manifest** 的迭代；本目录是**叙事侧**的可选加速器，**不是**第二条数据真源。

---

*若增加自动生成脚本，请在 [scripts/README.md](./README.md)「维护用 / 一次性工具」类中登记，并链回本文。*
