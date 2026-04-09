# 可进化管道脚本

| 命令 | 作用 | 外网 |
|------|------|------|
| `bash scripts/run_ingest_only.sh` | 抓取 → `evolution-candidates.json` → 校验候选 | 是 |
| `bash scripts/run_update_pipeline.sh` | 校验 manifest/候选 → `analysis_engine --sediment` → `sediment_trends` | 否 |
| `python3 scripts/analysis_engine.py --check` | 跑分析逻辑、校验输出结构，**不写** `analysis-snapshot.json`（CI / pre-commit） | 否 |
| `python3 scripts/merge_candidates_to_manifest.py <id>…` | 人审后合并进 `evolution-manifest.json` | 否 |
| `python3 scripts/validate-evolution-manifest.py` | 校验正式库结构 | 否 |
| `python3 scripts/validate-evolution-candidates.py` | 校验候选结构 | 否 |
| `python3 scripts/check_manifest_drift.py` | **对账**：`maps_to.pages` 文件存在；`lab_factors` ∈ `lab.js` | 否 |
| `bash scripts/install-git-hooks.sh` | 启用 `.githooks/pre-commit`（validate + `--check`） | 否 |
| `SITE_BASE=https://… make sitemap` | 生成根目录 `sitemap.xml` | 否 |

推荐节奏：ingest 单独排期 → 本地审阅 merge → 再跑 `run_update_pipeline.sh`（与 `analysis-hub` 文档一致）。

双周反哺清单：[docs/EVOLUTION_RUNBOOK.md](../docs/EVOLUTION_RUNBOOK.md)。
