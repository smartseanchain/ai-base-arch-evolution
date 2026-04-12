# 可进化管道脚本

参与贡献、合并前自检：**[CONTRIBUTING.md](../CONTRIBUTING.md)**。**全文档整理主线**（维护者按序扫读）：**[docs/README.md · 文档主线](../docs/README.md#docs-spine)**。**读者面 / 管理面一页**（与脚本闸门对读）：**[PLATFORM_MASTER_MAP · 节 1a](../docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)**。**脚本 vs 只读 API vs 组件化（替换边界与升级建议）**：[docs/SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](../docs/SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md)。合并/发布一页清单：**[MERGE_AND_RELEASE_CHECKLIST.md](../docs/MERGE_AND_RELEASE_CHECKLIST.md)**。**按阶段升级**（编排/Kafka/生产库前对表）：**[docs/PHASED_UPGRADE_EXECUTION_GUIDE.md](../docs/PHASED_UPGRADE_EXECUTION_GUIDE.md)**；**`make help`** 文首亦有提示。

**依赖**：校验链需 **`pip install -r requirements.txt`**（`jsonschema`，用于快照与 Schema 文件对齐）。**架构**：包 **`evolution_pkg`**（`evolution_pkg.io`；`evolution_pkg.pipeline`；**`evolution_pkg.nav_links`**；**`evolution_pkg.spa_nav`**；**`evolution_pkg.sediment_validate`**、**`evolution_pkg.sediment_daily`**（**`--sediment`** 写 ``data/sediment.json`` + SQLite）；**`evolution_pkg.hint_closure`**（`track_closure` 与决策闭环缺口）、**`evolution_pkg.analysis_hints`**（规则提示、diff、候选分解、**`load_hint_rules_from_path`**）、**`evolution_pkg.analysis_core`**（**`run_analysis`** 聚合）、**`evolution_pkg.analysis_validate`**（**`--check`** 内存结构校验）、**`evolution_pkg.analysis_snapshot_build`**（快照顶层 dict）、**`evolution_pkg.analysis_pipeline`**（**`default_analysis_paths`**、**`parse_analysis_cli`**、**`run_analysis_pipeline`** / **`AnalysisPaths`**）；**`analysis_engine`** 为 CLI 入口；**`evolution_pkg.readonly_disk_routes`**（只读 HTTP 磁盘 **GET** 表，**`readonly_api`** 启动注册）；**`evolution_pkg.ops`**（**`http_cache`**：ETag / If-None-Match，**`readonly_api`** 复用）；**`evolution_pkg.domains`**（六域枚举与子模块归属，见 **[INTELLIGENCE_SIX_DOMAINS.md · 代码侧](../docs/INTELLIGENCE_SIX_DOMAINS.md#code-mapping)**））。**兼容**：`evolution_io.py` 仍可作为旧 `from evolution_io import …` 入口。

**新增或变更 JSON 契约（快照 / 沉淀 / 趋势 / 注册表 / SPA 导航等）时建议按序自检**，避免 Schema、校验脚本与消费方漂移：

1. 在 **`docs/schemas/`** 增补或修订 **`.schema.json`**（Draft 2020-12 与现有文件风格一致）；**索引表**维护 **[docs/schemas/README.md](../docs/schemas/README.md)**。  
2. 若有对应 **`scripts/validate_*_schema.py`**，同步字段与必填项；否则新增校验脚本并在下步接入。  
3. 在 **`scripts/run_validate.sh`** 中于合适位置调用该校验（与 **`make validate`**、pre-commit、CI 共用）。**`run_validate.sh`** 与 **`run_update_pipeline.sh`** / **`run_analyze_write.sh`** / **`run_ingest_only.sh`** 等入口 shell 所引用 **`scripts/*.py`** 的路径存在性由 **`scripts/tests/test_run_validate_script_refs.py`** 校验；**`evolution_pkg.pipeline.runner`** 的 **analyze / fast** 步骤表由 **`scripts/tests/test_pipeline_runner_script_refs.py`** 校验。  
4. 在 **`scripts/README.md`** 本表与相关文档（如 **[DATA_CONTRACTS.md](../docs/DATA_CONTRACTS.md)**）中注明新文件路径与消费者（Hub、总线、`readonly_api` 路由等）；**`docs/schemas/README.md`** 索引表须包含新 **`*.schema.json`**（**`scripts/tests/test_schemas_readme_index.py`** 会校验）。平台级扩展清单见 **[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](../docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist)**。  
5. **大功能拆 PR、提前挂健康/只读骨架**：见 **[INCREMENTAL_BUILD_PLAYBOOK.md](../docs/INCREMENTAL_BUILD_PLAYBOOK.md)**（组件引入顺序 · 调试闭环 · **[PR 切片模板](../docs/templates/incremental-pr-slice.md)**）。

<a id="scripts-by-role"></a>

## 脚本分类（按职责）

顶层 `scripts/` 除目录 **`evolution_pkg/`**（可 import 的库）与 **`tests/`**（单测）外，按下表浏览；**具体参数与是否走外网仍以下方命令表为准**。与 [docs/ARCHITECTURE.md#seven-layers](../docs/ARCHITECTURE.md#seven-layers) 七类模块可对读。

| 职责 | 典型脚本 / Shell |
|------|-------------------|
| **闸门与对账** | **`run_validate.sh`**（**`make validate`** 总入口）、`validate-evolution-manifest.py`、`validate-evolution-candidates.py`、`validate_evolution_hint_decisions.py`、`validate_evolution_registry_schema.py`、`validate_analysis_snapshot_schema.py`、`validate_sediment_artifacts_schema.py`、`check_manifest_drift.py`、`check_nav_links_registry.py`、`sync_site_nav.py`（`--check` / 写回）、`check_skip_bar_404.py` |
| **编排（分析写盘）** | `run_update_pipeline.sh`、`run_analyze_write.sh`、`run_pipeline_steps.py` → **`evolution_pkg.pipeline.runner`** |
| **抓取与入池** | `run_ingest_only.sh`、`ingest_opinion_law.py`（配置 **`ingest_config.json`**、**`maps_to_hints.json`**） |
| **人审合并** | `merge_candidates_to_manifest.py` |
| **分析与血缘** | `analysis_engine.py`、`lineage_utils.py`（`run` 块等） |
| **沉淀、SQLite、趋势** | `sqlite_store.py`、`import_sediment_json_to_sqlite.py`、`sediment_trends.py`、`list_analysis_snapshot_history.py`；历史表读写见 **`evolution_pkg.analysis_snapshot_history`** |
| **站点与双轨呈现** | `sync_spa_public.py`、`gen_nav_links_ts.py`、`gen-sitemap.py` |
| **运维与侧车** | `print_evolution_status.py`、`diff_analysis_snapshot.py`、`readonly_api.py`（**`requirements-api.txt`**）、`query_evolution_duckdb.py`（**`requirements-analytics.txt`**）；容器编排见根目录 **[DOCKER.md](../docs/DOCKER.md)**、**`make docker-up`** / **`make docker-up-api`** |
| **兼容入口** | `evolution_io.py`（`from evolution_io import …` → **`evolution_pkg.io`**） |

### 文件命名（连字符与下划线）

仓库中并存 **`validate-evolution-*.py`**（连字符，较早入口）与 **`validate_*` / `check_*`**（下划线）。**新增脚本建议统一为 `snake_case.py`**，并与 **`run_validate.sh`** 的调用名一致。旧名保留以免破坏文档、CI 与外部引用；**不建议**对大量现网脚本一次性批量重命名。

### 维护用 / 一次性工具（不接入默认校验链）

下列脚本用于迁移、批量改版或内容生成，**默认不**由 **`run_validate.sh`** 调用；使用前请读脚本顶部说明或相关文档。

| 脚本 | 用途 |
|------|------|
| `migrate_muted_inline_styles.py` | 内联样式等迁移 |
| `apply_site_round_extensions.py` | 全站轮次扩展等批量改版 |
| `_build_synthesis_subpages.py` | 综合推演子页构建辅助 |

**按能力找脚本**（与 [docs/ARCHITECTURE.md#seven-layers](../docs/ARCHITECTURE.md#seven-layers) 七类模块对齐）：

| 能力 | 相关脚本 |
|------|-----------|
| 抓取 / 线索入库 | `ingest_opinion_law.py`、`run_ingest_only.sh` |
| 人审合并 | `merge_candidates_to_manifest.py` |
| 分析 + 当日快照 | `analysis_engine.py` |
| 沉淀 + 本地库 | `analysis_engine.py --sediment`、`sqlite_store.py`（含 **`analysis_snapshot_history`**）、`import_sediment_json_to_sqlite.py`、`list_analysis_snapshot_history.py` |
| 跨日汇总 | `sediment_trends.py` |
| 规则闭环 JSON | `validate_evolution_hint_decisions.py` |
| 闸门 / 对账 | `validate-evolution-*.py`、`validate_evolution_registry_schema.py`、`validate_analysis_snapshot_schema.py`、`validate_sediment_artifacts_schema.py`、`check_nav_links_registry.py`、`check_manifest_drift.py`、`sync_site_nav.py`、`check_skip_bar_404.py` |
| 站点辅助 | `gen-sitemap.py` |

| 命令 | 作用 | 外网 |
|------|------|------|
| `bash scripts/run_ingest_only.sh` | 抓取 → `evolution-candidates.json` → 校验候选（可附加 `ingest_opinion_law.py` 参数） | 是 |
| `WRITE_INGEST_SUMMARY=1 bash scripts/run_ingest_only.sh` | 同上并写入根目录 `ingest-summary.json`（**已 gitignore**；CI 默认开启） | 是 |
| `python3 scripts/ingest_opinion_law.py --full-pool` / `make ingest-full` | 单次忽略 `require_route_match`，全量进池 | 是 |
| `ingest_config.require_route_match` | `true`：仅保留命中 `routes` 的 RSS/法规线索并清理旧未命中候选 | — |
| `bash scripts/run_update_pipeline.sh` | 由 **`evolution_pkg.pipeline.runner`**（经 `run_pipeline_steps.py analyze`）编排：与 **`run_validate.sh` 相同的前半段**（至单测）+ **`--sediment`** + **`sediment_trends`** + 沉淀/趋势 Schema + 快照 Schema + **`--check`**；结束写 **`artifacts/pipeline-metrics-*.json`**（`SKIP_PIPELINE_TELEMETRY=1` 可关）。**`runner` 步骤表内 `scripts/*.py` 路径**由 **`scripts/tests/test_pipeline_runner_script_refs.py`** 校验存在性 | 否 |
| `bash scripts/run_analyze_write.sh` / **`make evolution-fast`** | **`run_pipeline_steps.py fast`**：同上，步骤较少。**不**重跑 manifest/漂移/单测/顶栏。须先 **`make validate`**，提交前仍须 validate | 否 |
| `python3 scripts/diff_analysis_snapshot.py` | 对比两份 `analysis-snapshot.json`，输出 Markdown 或 `--json`（贴 PR） | 否 |
| `python3 scripts/query_evolution_duckdb.py` | DuckDB 附加 `data/evolution.db` 跑 SQL（需 `pip install -r requirements-analytics.txt`） | 否 |
| `python3 scripts/list_analysis_snapshot_history.py` | 列出 SQLite **`analysis_snapshot_history`** 元数据（`run_id`、时间、`snapshot_json` 字节数）；`--json` | 否 |
| `PYTHONPATH=scripts python3 -m uvicorn readonly_api:app` | 只读 HTTP：`/health`、`/snapshot`、`/trends`、`/manifest`、`/registry`、`/sediment`、`/candidates`（**敏感**·未审候选）、`/hint-decisions`（人审决策·宜受控）、`/hint-rules`（分析规则）、`/maps-to-hints`（ingest 映射）、`/ingest-config`（RSS 源·宜受控）、`/site-meta`、`/snapshot-history`、`/snapshot-history/{run_id}`（**ETag** + **Cache-Control**；**If-None-Match** 命中返回 **304**；动态历史体 **no-store**；**`/sediment`** 无文件时 **404**；需 `requirements-api.txt`；历史依赖本地 `data/evolution.db`） | 否 |
| `make docker-up` / `make docker-up-api` / `make docker-up-admin` | **Docker Compose**：MPA **8765**；**`api`** → 只读 API **8099**；**`admin`** → 管理端脚手架 **8100**（**[admin-console/README.md](../admin-console/README.md)**）；开发挂载见 **[DOCKER.md](../docs/DOCKER.md)** | 否（构建/拉镜像时可能需网络） |
| `python3 scripts/validate_evolution_registry_schema.py` | **`evolution-registry.json`** 与 **`docs/schemas/evolution-registry.schema.json`**；已并入 **`make validate`** 与 **`make test`** | 否 |
| `bash scripts/run_validate.sh` | 与 **`make validate`** 相同的全套校验（compileall + JSON + **registry Schema** + 对账 + **navLinks** + 顶栏 + **404 skip-bar** + 单测 + `--check` + 快照/沉淀/趋势 Schema） | 否 |
| `make trends` / `python3 scripts/sediment_trends.py` | 仅根据已有沉淀重算 `assets/sediment-trends.json`（不跑分析引擎） | 否 |
| `make status` / `python3 scripts/print_evolution_status.py` | 先打印 `assets/site-meta.json` 的 **site_version**；再打印 `analysis-snapshot.json` 合并计数、hint 决策统计、闭环缺口条数（及 rule_id 列表） | 否 |
| `python3 scripts/analysis_engine.py` | 写 **`assets/analysis-snapshot.json`** 时默认向 **`evolution.db`** 表 **`analysis_snapshot_history`** 追加只读历史（**`--no-sqlite-snapshot-history`** 关闭） | 否 |
| `python3 scripts/analysis_engine.py --check` | 跑分析逻辑、校验输出结构，**不写** `analysis-snapshot.json`（CI / pre-commit；**不**与上期快照做 diff 提示）；根级含 **`run.run_id` / `run.repo_revision`** 血缘；`sources` 含 `candidate_review_breakdown`、`hint_decisions` | 否 |

在确定性快照之上**可选**叠加 **AI 服务解读**（独立产物与配置、不并入快照必填域）的约定与检查单：**[docs/AI_ASSISTED_ANALYSIS_LAYER.md](../docs/AI_ASSISTED_ANALYSIS_LAYER.md)**；配置形状示例：**[docs/examples/ai_analysis_overlay.example.json](../docs/examples/ai_analysis_overlay.example.json)**。契约校验：**`validate_ai_analysis_overlay_schema.py`**（无文件则跳过；有则与 **`analysis-snapshot.json`** 的 **`run.run_id`** 对账）。占位写入（无 LLM）：**`python3 scripts/write_ai_analysis_overlay_stub.py`**（须已有快照）。
| `python3 scripts/validate_analysis_snapshot_schema.py` | 用 **jsonschema** 校验**已提交**的 `assets/analysis-snapshot.json` 与 `docs/schemas/analysis-snapshot.schema.json`（无文件则跳过）；已并入 `make validate` | 否 |
| `python3 scripts/validate_sediment_artifacts_schema.py` | 校验 **`data/sediment.json`**、**`assets/sediment-trends.json`** 与 **`docs/schemas/sediment*.schema.json`**（无文件则跳过）；已并入 `make validate` | 否 |
| `python3 scripts/gen_nav_links_ts.py` | 默认：检查 **navLinks.ts** 是否与 **spa/nav.config.json** 一致；**`--write`** 写回 **navLinks.ts**（**`make gen-nav-links`**） | 否 |
| `python3 scripts/check_nav_links_registry.py` | **nav.config.json** 与 registry 页面集一致，且 **navLinks.ts** 为生成结果（**`evolution_pkg.spa_nav`**；无 **spa/package.json** 则跳过）；已并入 `make validate` 与 **`make test`** | 否 |
| `python3 scripts/merge_candidates_to_manifest.py <id>…` | 人审后合并进 manifest；**须** `review_state=queued_for_manifest`（`--force` 跳过） | 否 |
| `python3 scripts/validate-evolution-manifest.py` | 校验正式库结构 | 否 |
| `python3 scripts/validate-evolution-candidates.py` | 校验候选结构 | 否 |
| `python3 scripts/validate_evolution_hint_decisions.py` | 校验 `assets/evolution-hint-decisions.json`；根级可选 `schema_version: 1`；`rule_id` 若填写须 ∈ `evolution-hint-rules.json` 的 `rules[].id` | 否 |
| `python3 scripts/check_manifest_drift.py` | **对账**：`maps_to.pages` ∈ **`scripts/evolution-registry.json`** 且文件存在；`lab_factors` 与 registry 及 **`lab.js` 因子 id 集合一致**；`ingest_config` / `maps_to_hints` / `gen-sitemap` PRIORITY | 否 |
| `make test` | **`validate_evolution_registry_schema.py`** + unittest（`PYTHONPATH=scripts`）+ **`check_nav_links_registry.py`** + **`validate_sediment_artifacts_schema.py`** | 否 |
| `make test-readonly-api` | 安装 **`requirements.txt` + `requirements-api.txt`** 后跑 **`test_readonly*.py`**（**`test_readonly_api`**：ETag / 304；**`test_readonly_proxy_segment_sync`**：管理端 **`READONLY_PROXY_SEGMENTS`** 与 **`readonly_api`** 单段路径对账；本地未装 fastapi 时 **`make validate`** 中相关用例 **skip**） | 否 |
| `make test-admin-console` | 安装 **`admin-console/requirements.txt`** 后跑 **`admin-console/tests`**（管理端脚手架烟测） | 否（`pip install` 可能需网络） |
| `make merge-ready` | **`make validate`** 成功后执行 **`make test-readonly-api`** 与 **`make test-admin-console`**（合并前推荐；见 **[docs/MERGE_AND_RELEASE_CHECKLIST.md](../docs/MERGE_AND_RELEASE_CHECKLIST.md)**） | 否 |
| `python3 scripts/sync_site_nav.py` / `make sync-nav` | 按 **`partials/skip-bar.inc.html`** + **`partials/site-nav.inc.html`** 写回根目录各页（跳过 **404**、legacy 单页）；**404.html** 顶栏/skip 手维护，改模板后须与 partial 对齐（**`check_skip_bar_404.py`** 已含于 **`make validate`**） | 否 |
| `make check-site-nav` | 顶栏与模板一致（已并入 `make validate`） | 否 |
| `bash scripts/install-git-hooks.sh` | 启用 `.githooks/pre-commit`（等同 `make validate`） | 否 |
| `SITE_BASE=https://… make sitemap` | 生成根目录 `sitemap.xml` | 否 |
| `make spa-sync` / `python3 scripts/sync_spa_public.py` | 根目录 HTML/assets/docs → `spa/public`（剥顶栏供 iframe） | 否 |
| `make spa-build` | `spa-sync` + `npm ci` + Vite 生产构建 → `spa/dist`（CI **`spa-build`** job：变更触及 `spa/`、**`evolution-registry.json`**、sync 输入等时运行，见 `ci.yml`） | 否（`npm ci` 需 registry） |
| `make spa-install` | 仅 `spa` 目录 `npm ci` | 否（需 registry） |

推荐节奏：ingest 单独排期 → 本地审阅 merge → 再跑 `run_update_pipeline.sh`（与 [analysis-hub · 方法与演进总线](../analysis-hub.html#panorama) 对表）。**双轨**：增删注册页须维护 [spa/nav.config.json](../spa/nav.config.json) 并 **`make gen-nav-links`**（已含于 **`make spa-build`**）；**`check_nav_links_registry.py`** 已含于 **`make validate`**。说明见 [spa/README.md](../spa/README.md)。

- **`scripts/ingest_config.json`**：`routes` 正则命中后写入 `maps_to`；**`scripts/maps_to_hints.json`** 按 **RSS 链接 host** 与 **标题/摘要关键词** 再合并 `pages` / `lab_factors`（仍须人审）。可选 **`json_feeds`**：每项含 **`id`**、**`url`**（**https**）、**`items_path`**（点分路径，空则根为 JSON 数组）、**`max_items`**、**`default_kind`**，以及可选 **`keys_title` / `keys_link` / `keys_summary`**（字符串键优先序列表）；由 **`ingest_opinion_law.py`** 拉取并与 RSS 同池合并，**`source.type`** 为 **`json_http`**。侧车若输出固定 JSON 形状，可只配映射而不拷贝对方代码。**`admin-console`** 首页数据源目录可勾选并**复制 `rss_feeds` 草案 JSON**（与只读 **`/ingest-config`** 去重时附 **`omitted_already_in_ingest`**），仍须手工合并本文件并经 **PR** + **`make validate`**（见 [admin-console/README.md](../admin-console/README.md)）。
- **`scripts/evolution-hint-rules.json`**：`analysis_engine` 中条件类 `evolution_hints` 的外置规则；可选 **`track_closure`**：触发且决策 JSON 中尚无同 `rule_id` 的 done/rejected 时，快照含 **`hint_closure_gaps`**（分析页高亮）。与**已有** `assets/analysis-snapshot.json` 对比可生成「相较上期」的 diff 提示（`--check` 模式跳过 diff）。

双周反哺清单：[docs/EVOLUTION_RUNBOOK.md](../docs/EVOLUTION_RUNBOOK.md)。架构总览：[docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)。**模块全量梳理与升级矩阵**：[docs/MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](../docs/MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)。首次参与仓库开发见根目录 [CONTRIBUTING.md](../CONTRIBUTING.md)。
