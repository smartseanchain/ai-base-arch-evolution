# JSON Schema 索引（契约扩展入口）

<a id="schemas-readme-index"></a>

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../../README.md#pm-four-journeys) · [README · 从这里开始](../../README.md#readme-start-here) · [README · 双轨真源](../../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](../ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](../ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../../CONTRIBUTING.md#contributing-change-to-command)。

新增或变更结构化 JSON 时，**先改 Schema 与校验脚本**，再改生产方与消费方（与 [scripts/README · 契约检查单](../scripts/README.md) 文首、[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](../PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#extension-slots) §2 一致）。**整体架构五维索引**见 **[PROJECT_ARCHITECTURE_OVERVIEW.md](../PROJECT_ARCHITECTURE_OVERVIEW.md)**（**[勿混粒度 · 五维/六域/七类](../PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)**；**[§1a 主链联动与验证](../PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** · **[§1b 仓库物理分层](../PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**）。**整体内容框架**见 **[docs/README · #content-framework](../README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](../README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](../README.md#system-components-fusion)。**判型最短链**（主线 **0c**）：**[docs/README · #quick-paths](../README.md#quick-paths)**。**自动化助手**：[AGENTS.md · 框架判型](../../AGENTS.md#agents-content-framework) · [合并前](../../AGENTS.md#agents-pre-merge) · [人审闸门](../../AGENTS.md#agents-invariants)。合并 PR 前推荐 **`make merge-ready`**（**`validate`** + **`test-readonly-api`** + **`test-admin-console`**），见 **[MERGE_AND_RELEASE_CHECKLIST.md](../MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](../MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[关系视图](../../maintainer-hub.html#mh-spine-map)**（**`spa-sync` / `spa-build`** 对表）。**MPA 顶栏与失页**：改 **`partials/`** → **`make sync-nav`**；**`404.html`** 须**手调**（`sync_site_nav` 不写回）— **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

| Schema 文件 | 典型数据文件 | 校验脚本（节选） |
|-------------|--------------|------------------|
| [evolution-registry.schema.json](./evolution-registry.schema.json) | `scripts/evolution-registry.json` | `validate_evolution_registry_schema.py` |
| [analysis-snapshot.schema.json](./analysis-snapshot.schema.json) | `assets/analysis-snapshot.json` | `validate_analysis_snapshot_schema.py` |
| [sediment.schema.json](./sediment.schema.json) | `data/sediment.json` | `validate_sediment_artifacts_schema.py` |
| [sediment-trends.schema.json](./sediment-trends.schema.json) | `assets/sediment-trends.json` | 同上 |
| [spa-nav-config.schema.json](./spa-nav-config.schema.json) | `spa/nav.config.json` | `check_nav_links_registry.py`（**`evolution_pkg.spa_nav`**） |
| [ai-analysis-overlay.schema.json](./ai-analysis-overlay.schema.json) | `assets/ai-analysis-overlay.json`（可选） | `validate_ai_analysis_overlay_schema.py`（**`evolution_pkg.ai_overlay_validate`**） |
| [ai-overlay-step.schema.json](./ai-overlay-step.schema.json) | `artifacts/ai-overlay-step.json`（可选；**`write_ai_analysis_overlay`** 侧车；并入 **`pipeline-metrics`**） | **`validate_ai_overlay_step_schema.py`**（**`evolution_pkg.ai_overlay_step_validate`**）；与 **`pipeline-metrics`** 中 **`ai_overlay_step`** 对读 |
| [ai-mapping-golden.schema.json](./ai-mapping-golden.schema.json) | `fixtures/ai_mapping_golden/*.json`（多文件） | `validate_golden_mapping.py`（`--dir`；expect 与 **`evolution-registry.json`** 对账） |
| [pipeline-metrics.schema.json](./pipeline-metrics.schema.json) | `artifacts/pipeline-metrics-*.json`（可选·本地）；**`fixtures/pipeline_metrics_example.json`**（样例） | `validate_pipeline_metrics_schema.py` |

**pipeline-metrics 补充**：`artifacts/` 内缺 **`input_artifacts`** 或 **`otel_semantics`** 的遥测按旧格式**跳过** Schema 校验（exit 仍 0）；**stderr** 会提示 **`make clean-pipeline-metrics-dry-run`** / **`make clean-pipeline-metrics`**（与 **`make validate`**、**`make validate-fast`** 同源脚本）。契约与清理动线见 **[DATA_CONTRACTS · §7](../DATA_CONTRACTS.md#pipeline-telemetry)** · **[EVOLUTION_RUNBOOK · 加速](../EVOLUTION_RUNBOOK.md#accelerate)**。

**索引完整性**：单测 **`scripts/tests/test_schemas_readme_index.py`** 要求上表覆盖目录内**全部** `*.schema.json`（新增 Schema 文件时须同步本 README，否则 **`make test`** / **`make validate`** 失败）。

**未入此目录的 JSON**（如 `evolution-manifest.json`、候选、hint 决策）仍由 **`validate-evolution-*.py`** 等脚本校验；字段级说明见 **[DATA_CONTRACTS.md](../DATA_CONTRACTS.md)**。

JSON Schema **Draft 2020-12**（与仓库现有 `.schema.json` 一致）。
