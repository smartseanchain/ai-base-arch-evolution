# 可进化管道脚本

**按能力找脚本**（与 [docs/ARCHITECTURE.md#seven-layers](../docs/ARCHITECTURE.md#seven-layers) 七类模块对齐）：

| 能力 | 相关脚本 |
|------|-----------|
| 抓取 / 线索入库 | `ingest_opinion_law.py`、`run_ingest_only.sh` |
| 人审合并 | `merge_candidates_to_manifest.py` |
| 分析 + 当日快照 | `analysis_engine.py` |
| 沉淀 + 本地库 | `analysis_engine.py --sediment`、`sqlite_store.py`、`import_sediment_json_to_sqlite.py` |
| 跨日汇总 | `sediment_trends.py` |
| 规则闭环 JSON | `validate_evolution_hint_decisions.py` |
| 闸门 / 对账 | `validate-evolution-*.py`、`validate_analysis_snapshot_schema.py`、`check_manifest_drift.py`、`sync_site_nav.py` |
| 站点辅助 | `gen-sitemap.py` |

| 命令 | 作用 | 外网 |
|------|------|------|
| `bash scripts/run_ingest_only.sh` | 抓取 → `evolution-candidates.json` → 校验候选（可附加 `ingest_opinion_law.py` 参数） | 是 |
| `WRITE_INGEST_SUMMARY=1 bash scripts/run_ingest_only.sh` | 同上并写入根目录 `ingest-summary.json`（**已 gitignore**；CI 默认开启） | 是 |
| `python3 scripts/ingest_opinion_law.py --full-pool` / `make ingest-full` | 单次忽略 `require_route_match`，全量进池 | 是 |
| `ingest_config.require_route_match` | `true`：仅保留命中 `routes` 的 RSS/法规线索并清理旧未命中候选 | — |
| `bash scripts/run_update_pipeline.sh` | 校验 manifest/候选 → `analysis_engine --sediment` → `sediment_trends`；沉淀含 `hint_closure_gaps_n` / `hint_decisions_total`，趋势 JSON 含 `closure_backlog` | 否 |
| `make trends` / `python3 scripts/sediment_trends.py` | 仅根据已有沉淀重算 `assets/sediment-trends.json`（不跑分析引擎） | 否 |
| `make status` / `python3 scripts/print_evolution_status.py` | 打印 `analysis-snapshot.json` 合并计数、hint 决策统计、闭环缺口条数（及 rule_id 列表） | 否 |
| `python3 scripts/analysis_engine.py --check` | 跑分析逻辑、校验输出结构，**不写** `analysis-snapshot.json`（CI / pre-commit；**不**与上期快照做 diff 提示）；根级含 **`run.run_id` / `run.repo_revision`** 血缘；`sources` 含 `candidate_review_breakdown`、`hint_decisions` | 否 |
| `python3 scripts/validate_analysis_snapshot_schema.py` | 校验**已提交**的 `assets/analysis-snapshot.json` 顶层字段与 `run`（无文件则跳过）；已并入 `make validate` | 否 |
| `python3 scripts/merge_candidates_to_manifest.py <id>…` | 人审后合并进 manifest；**须** `review_state=queued_for_manifest`（`--force` 跳过） | 否 |
| `python3 scripts/validate-evolution-manifest.py` | 校验正式库结构 | 否 |
| `python3 scripts/validate-evolution-candidates.py` | 校验候选结构 | 否 |
| `python3 scripts/validate_evolution_hint_decisions.py` | 校验 `assets/evolution-hint-decisions.json`；根级可选 `schema_version: 1`；`rule_id` 若填写须 ∈ `evolution-hint-rules.json` 的 `rules[].id` | 否 |
| `python3 scripts/check_manifest_drift.py` | **对账**：`maps_to.pages` ∈ **`scripts/evolution-registry.json`** 且文件存在；`lab_factors` 与 registry 及 **`lab.js` 因子 id 集合一致**；`ingest_config` / `maps_to_hints` / `gen-sitemap` PRIORITY | 否 |
| `make test` | `scripts/tests` · unittest（`PYTHONPATH=scripts`） | 否 |
| `python3 scripts/sync_site_nav.py` / `make sync-nav` | 按 **`partials/skip-bar.inc.html`** + **`partials/site-nav.inc.html`** 写回根目录各页（跳过 404、legacy 单页） | 否 |
| `make check-site-nav` | 顶栏与模板一致（已并入 `make validate`） | 否 |
| `bash scripts/install-git-hooks.sh` | 启用 `.githooks/pre-commit`（validate + `--check`） | 否 |
| `SITE_BASE=https://… make sitemap` | 生成根目录 `sitemap.xml` | 否 |

推荐节奏：ingest 单独排期 → 本地审阅 merge → 再跑 `run_update_pipeline.sh`（与 `analysis-hub` 文档一致）。

- **`scripts/ingest_config.json`**：`routes` 正则命中后写入 `maps_to`；**`scripts/maps_to_hints.json`** 按 **RSS 链接 host** 与 **标题/摘要关键词** 再合并 `pages` / `lab_factors`（仍须人审）。
- **`scripts/evolution-hint-rules.json`**：`analysis_engine` 中条件类 `evolution_hints` 的外置规则；可选 **`track_closure`**：触发且决策 JSON 中尚无同 `rule_id` 的 done/rejected 时，快照含 **`hint_closure_gaps`**（分析页高亮）。与**已有** `assets/analysis-snapshot.json` 对比可生成「相较上期」的 diff 提示（`--check` 模式跳过 diff）。

双周反哺清单：[docs/EVOLUTION_RUNBOOK.md](../docs/EVOLUTION_RUNBOOK.md)。架构总览：[docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)。
