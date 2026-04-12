# JSON Schema 索引（契约扩展入口）

新增或变更结构化 JSON 时，**先改 Schema 与校验脚本**，再改生产方与消费方（与 [scripts/README · 契约检查单](../scripts/README.md) 文首、[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](../PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#extension-slots) §2 一致）。**整体架构五维索引**见 **[PROJECT_ARCHITECTURE_OVERVIEW.md](../PROJECT_ARCHITECTURE_OVERVIEW.md)**。合并 PR 前推荐 **`make merge-ready`**（**`validate`** + **`test-readonly-api`** + **`test-admin-console`**），见 **[MERGE_AND_RELEASE_CHECKLIST.md](../MERGE_AND_RELEASE_CHECKLIST.md)**。

| Schema 文件 | 典型数据文件 | 校验脚本（节选） |
|-------------|--------------|------------------|
| [evolution-registry.schema.json](./evolution-registry.schema.json) | `scripts/evolution-registry.json` | `validate_evolution_registry_schema.py` |
| [analysis-snapshot.schema.json](./analysis-snapshot.schema.json) | `assets/analysis-snapshot.json` | `validate_analysis_snapshot_schema.py` |
| [sediment.schema.json](./sediment.schema.json) | `data/sediment.json` | `validate_sediment_artifacts_schema.py` |
| [sediment-trends.schema.json](./sediment-trends.schema.json) | `assets/sediment-trends.json` | 同上 |
| [spa-nav-config.schema.json](./spa-nav-config.schema.json) | `spa/nav.config.json` | `check_nav_links_registry.py`（**`evolution_pkg.spa_nav`**） |
| [ai-analysis-overlay.schema.json](./ai-analysis-overlay.schema.json) | `assets/ai-analysis-overlay.json`（可选） | `validate_ai_analysis_overlay_schema.py`（**`evolution_pkg.ai_overlay_validate`**） |

**索引完整性**：单测 **`scripts/tests/test_schemas_readme_index.py`** 要求上表覆盖目录内**全部** `*.schema.json`（新增 Schema 文件时须同步本 README，否则 **`make test`** / **`make validate`** 失败）。

**未入此目录的 JSON**（如 `evolution-manifest.json`、候选、hint 决策）仍由 **`validate-evolution-*.py`** 等脚本校验；字段级说明见 **[DATA_CONTRACTS.md](../DATA_CONTRACTS.md)**。

JSON Schema **Draft 2020-12**（与仓库现有 `.schema.json` 一致）。
