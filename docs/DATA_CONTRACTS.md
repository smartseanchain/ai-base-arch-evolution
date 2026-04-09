# 数据契约与主键（全站 JSON / 侧车）

本文是 [ARCHITECTURE.md](./ARCHITECTURE.md) 的**字段级索引**：各文件的职责、关联键、校验入口与可选分析栈。大改管道时请同步更新本节。

## 1. 单一注册表

| 文件 | 角色 | 关键字段 | 校验 |
|------|------|----------|------|
| `scripts/evolution-registry.json` | 允许出现在 `maps_to.pages` 的根 HTML；`lab_factors` 全集 | `pages[]`、`lab_factors[]` | `check_manifest_drift.py` |

## 2. 信号与候选

| 文件 | 角色 | 关键字段 | 校验 |
|------|------|----------|------|
| `assets/evolution-manifest.json` | 已入库信号 | `signals[].id`、`maps_to.pages`、`maps_to.lab_factors`、`review_state`（正式条目中） | `validate-evolution-manifest.py` |
| `assets/evolution-candidates.json` | 待审候选 | `signals[].id`、`review_state`、`status` | `validate-evolution-candidates.py` |
| `scripts/maps_to_hints.json` | ingest 时按 host/关键词补 `maps_to` | 与 ingest 脚本约定 | `check_manifest_drift.py` |

**关联键**：信号 `id`（字符串）在候选与 manifest 之间唯一标识同一条目；合并脚本以 `id` 为主键更新。

## 3. 规则与决策（闭环）

| 文件 | 角色 | 关键字段 | 校验 |
|------|------|----------|------|
| `scripts/evolution-hint-rules.json` | 分析引擎外置规则 | `rules[].id`、`track_closure` | `check_manifest_drift.py`（target_pages）、`analysis_engine` |
| `assets/evolution-hint-decisions.json` | 人对提示的落实记录 | `decisions[].rule_id`、`action`（done/rejected/deferred） | `validate_evolution_hint_decisions.py` |

**关联键**：`rule_id` 必须 ∈ `evolution-hint-rules.json` 中的 `rules[].id`（若填写）。

## 4. 当日分析快照

| 文件 | 角色 | 关键字段 | 校验 |
|------|------|----------|------|
| `assets/analysis-snapshot.json` | 热力、共现、提示、闭环缺口 | `run.run_id`、`run.repo_revision`、`sources.*`、`module_heat`（`page`+`count`）、`factor_heat`（`factor`+`count`） | `validate_analysis_snapshot_schema.py`、`analysis_engine.py --check` |

**契约**：[`docs/schemas/analysis-snapshot.schema.json`](schemas/analysis-snapshot.schema.json)。

**差分**：`python3 scripts/diff_analysis_snapshot.py <base.json> [head.json]` 或 `--git-base HEAD~1:assets/analysis-snapshot.json`。

## 5. 按日沉淀与跨日趋势

| 文件 | 角色 | 关键字段 | 备注 |
|------|------|----------|------|
| `data/sediment.json` | 多日摘要条目 | `entries[].date`、`top_factors`、`top_pages`、`hint_closure_gaps_n` | 可与 SQLite 双写；见 `analysis_engine.py --sediment` |
| `data/evolution.db` | SQLite 侧车（默认忽略提交） | 沉淀表 | `.gitignore` |
| `assets/sediment-trends.json` | 因子/页面持久度、长期 hints | `factor_persistence`、`page_persistence`、`closure_backlog` | `sediment_trends.py` |

## 6. 站点发布版本（静态元数据）

| 文件 | 角色 | 关键字段 |
|------|------|----------|
| `assets/site-meta.json` | **人为维护**的发布线版本（与 `analysis-snapshot.run` 无关） | `schema_version`、`site_version`、`codename`、`summary`、`updated` |

顶栏通过 **`[data-site-meta-version]`** 由 `site-data-bus.js` 拉取并显示为 `v1.x.x`。大功能合并或对外宣告时可递增 `site_version` 并更新 `summary`。

## 7. 流水线遥测（不入库）

| 文件 | 角色 | 关键字段 |
|------|------|----------|
| `artifacts/pipeline-metrics-*.json` | `make analyze` / `evolution-fast` 每步耗时与退出码 | `pipeline`、`steps[].id`、`duration_ms`、`exit_code`、`success` |

生成：`python3 scripts/run_pipeline_steps.py`（由 `run_update_pipeline.sh` / `run_analyze_write.sh` 调用）。关闭：`SKIP_PIPELINE_TELEMETRY=1`。

## 8. 可选分析栈（本地）

不进入默认 `requirements.txt`，避免 CI 与轻量环境膨胀。

| 依赖文件 | 用途 |
|----------|------|
| [`requirements-analytics.txt`](../requirements-analytics.txt) | DuckDB / Polars：对 `evolution.db` 或导出数据做 SQL / DataFrame |
| [`requirements-api.txt`](../requirements-api.txt) | FastAPI：只读暴露 `analysis-snapshot.json` 等（本地或内网） |

- **DuckDB 示例**：`python3 scripts/query_evolution_duckdb.py`（需 `pip install -r requirements-analytics.txt`）。
- **只读 API**：`pip install -r requirements-api.txt && uvicorn scripts.readonly_api:app --reload`（从仓库根执行时注意 `PYTHONPATH=scripts` 或将应用拷入包路径；见 `readonly_api.py` 顶部说明）。

## 9. Python 包布局（架构升级）

- **`scripts/evolution_pkg/`**：`io`（仓库根、`load_json`）、`pipeline`（analyze / fast 编排与遥测）。
- **`scripts/evolution_io.py`**：兼容层，等价于 `from evolution_pkg.io import …`。

## 10. 相关文档

- 数据流总图：[ARCHITECTURE.md](./ARCHITECTURE.md)
- 技术栈与功能地图：[TECH_ARCHITECTURE_CAPABILITIES.md](./TECH_ARCHITECTURE_CAPABILITIES.md)
- 全站读数总线：[SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md)
