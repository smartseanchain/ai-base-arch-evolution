# 可进化管道脚本

| 命令 | 作用 | 外网 |
|------|------|------|
| `bash scripts/run_ingest_only.sh` | 抓取 → `evolution-candidates.json` → 校验候选（可附加 `ingest_opinion_law.py` 参数） | 是 |
| `WRITE_INGEST_SUMMARY=1 bash scripts/run_ingest_only.sh` | 同上并写入根目录 `ingest-summary.json`（**已 gitignore**；CI 默认开启） | 是 |
| `python3 scripts/ingest_opinion_law.py --full-pool` / `make ingest-full` | 单次忽略 `require_route_match`，全量进池 | 是 |
| `ingest_config.require_route_match` | `true`：仅保留命中 `routes` 的 RSS/法规线索并清理旧未命中候选 | — |
| `bash scripts/run_update_pipeline.sh` | 校验 manifest/候选 → `analysis_engine --sediment` → `sediment_trends` | 否 |
| `python3 scripts/analysis_engine.py --check` | 跑分析逻辑、校验输出结构，**不写** `analysis-snapshot.json`（CI / pre-commit；**不**与上期快照做 diff 提示） | 否 |
| `python3 scripts/merge_candidates_to_manifest.py <id>…` | 人审后合并进 `evolution-manifest.json` | 否 |
| `python3 scripts/validate-evolution-manifest.py` | 校验正式库结构 | 否 |
| `python3 scripts/validate-evolution-candidates.py` | 校验候选结构 | 否 |
| `python3 scripts/check_manifest_drift.py` | **对账**：`maps_to.pages` ∈ **`scripts/evolution-registry.json`** 且文件存在；`lab_factors` 与 registry 及 **`lab.js` 因子 id 集合一致**；`ingest_config` / `maps_to_hints` / `gen-sitemap` PRIORITY | 否 |
| `make test` | `scripts/tests` · unittest（`PYTHONPATH=scripts`） | 否 |
| `bash scripts/install-git-hooks.sh` | 启用 `.githooks/pre-commit`（validate + `--check`） | 否 |
| `SITE_BASE=https://… make sitemap` | 生成根目录 `sitemap.xml` | 否 |

推荐节奏：ingest 单独排期 → 本地审阅 merge → 再跑 `run_update_pipeline.sh`（与 `analysis-hub` 文档一致）。

- **`scripts/ingest_config.json`**：`routes` 正则命中后写入 `maps_to`；**`scripts/maps_to_hints.json`** 按 **RSS 链接 host** 与 **标题/摘要关键词** 再合并 `pages` / `lab_factors`（仍须人审）。
- **`scripts/evolution-hint-rules.json`**：`analysis_engine` 中条件类 `evolution_hints` 的外置规则；与**已有** `assets/analysis-snapshot.json` 对比可生成「相较上期」的 diff 提示（`--check` 模式跳过 diff）。

双周反哺清单：[docs/EVOLUTION_RUNBOOK.md](../docs/EVOLUTION_RUNBOOK.md)。
