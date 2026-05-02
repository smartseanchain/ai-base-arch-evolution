# 可进化管道脚本

参与贡献、合并前自检：**[CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd)**。**全仓角色入口（四条动线）**：[README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进（五步）**：[ARCHITECTURE_ONE_PAGER · #architect-stewardship](../docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · **[不变量索引](../docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index)** · **[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** · **[PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)** · **[动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)**。**整体内容框架**：**[docs/README · #content-framework](../docs/README.md#content-framework)**。**前后台模块一页表**：[**#front-back-modules**](../docs/README.md#front-back-modules)。**系统组件与功能一条表**（可执行单元 × 主链）：**[docs/README · #system-components-fusion](../docs/README.md#system-components-fusion)**。**全文档整理主线**（维护者按序扫读）：**[docs/README.md · 文档主线](../docs/README.md#docs-spine)** · **[常见改动最短链 · #quick-paths](../docs/README.md#quick-paths)**（**0c**）。**主链联动与验证 · 仓库物理分层**（本目录落在哪一层、与谁联动）：**[勿混粒度 · 五维/六域/七类](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**读者面 / 管理面一页**（与脚本闸门对读）：**[PLATFORM_MASTER_MAP · 节 1a](../docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)**。**脚本 vs 只读 API vs 组件化（替换边界与升级建议）**：[docs/SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md](../docs/SCRIPTS_APIS_AND_COMPONENTS_UPGRADE.md)。合并/发布一页清单：**[MERGE_AND_RELEASE_CHECKLIST.md · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**。**技术栈文档**（简版 **§1—§4** + 详版分层/能力地图）：**[TECH_ARCHITECTURE_AND_UPGRADE_BRIEF](../docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)** · **[附录](../docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)**（[别名](../docs/TECH_ARCHITECTURE_CAPABILITIES.md)）· **[docs/README · #tech-stack-read-merge](../docs/README.md#tech-stack-read-merge)**。**按阶段升级**（编排/Kafka/生产库前对表）：**[docs/PHASED_UPGRADE_EXECUTION_GUIDE.md](../docs/PHASED_UPGRADE_EXECUTION_GUIDE.md)**；根 **`make help`** 文首 echo 同列 **[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** · **[PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)** · **[动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)**（与根 **README** / **Makefile** `help` 一致）。

**读者 MPA 维护枢纽**：[维护导读](../maintainer-hub.html) · [关系视图](../maintainer-hub.html#mh-spine-map)（本页 ↔ **`evolution-registry.json`** ↔ 文档锚点）· [系统边界速查](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)；**管理端观测 UI**（不写 manifest）：[admin-console/README.md](../admin-console/README.md)。

**自动化助手**（与 **`scripts/tests/test_agents_doc_anchors.py`** 枢纽文件表对读）：[AGENTS.md · 契约](../AGENTS.md#agents-contract) · [合并前](../AGENTS.md#agents-pre-merge) · [人审闸门](../AGENTS.md#agents-invariants) · [Cursor 规则](../AGENTS.md#agents-cursor-rules) · **[repo-gates.mdc](../.cursor/rules/repo-gates.mdc)**（判型 · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map) · 文首 **「子规则对读」** 链式点名三份子规则）。

**依赖**：校验链需 **`pip install -r requirements.txt`**（`jsonschema`，用于快照与 Schema 文件对齐）。

**可选**：在 **venv**（或具备用户级安装权限的环境）下，仓库根 **`pip install -e .`**（**`pyproject.toml`** + **`setup.py`**）后，可使用 **`evolution-ingest`** / **`evolution-analyze`** / **`evolution-merge`**（与薄壳脚本参数一致，**无需** **`PYTHONPATH=scripts`**）。CI、pre-commit 与 **`make validate`** 仍以 **`scripts/run_validate.sh`** 内路径为真源。

**轻量闸门**：**`make validate-fast`**（**`scripts/run_validate_fast.sh`**）缩短迭代等待；**省略**对账、顶栏 partial、404 skip-bar、黄金集映射、hint 决策、沉淀 JSON Schema 等；**已含** **`validate_ai_overlay_step_schema`** / **`validate_ai_analysis_overlay_schema`**（与全量同源，无文件则跳过）。**CI** 与 **pre-commit** **不跑** **`validate-fast`**。**合并 PR 前仍须** **`make validate`**。

**架构**：包 **`evolution_pkg`**（`evolution_pkg.io`；`evolution_pkg.pipeline`；**`evolution_pkg.nav_links`**；**`evolution_pkg.spa_nav`**；**`evolution_pkg.sediment_validate`**、**`evolution_pkg.sediment_daily`**（**`--sediment`** 写 ``data/sediment.json`` + SQLite）；**`evolution_pkg.hint_closure`**（`track_closure` 与决策闭环缺口）、**`evolution_pkg.analysis_hints`**（规则提示、diff、候选分解、**`load_hint_rules_from_path`**）、**`evolution_pkg.analysis_core`**（**`run_analysis`** 聚合）、**`evolution_pkg.analysis_validate`**（**`--check`** 内存结构校验）、**`evolution_pkg.analysis_snapshot_build`**（快照顶层 dict）、**`evolution_pkg.analysis_pipeline`**（**`main`**、**`default_analysis_paths`**、**`parse_analysis_cli`**、**`run_analysis_pipeline`** / **`AnalysisPaths`**）；**`analysis_engine.py`** 为薄 CLI 壳（与 **`-m evolution_pkg.analysis_pipeline`** 等价）；**`evolution_pkg.readonly_disk_routes`**（只读 HTTP 磁盘 **GET** 表，**`readonly_api`** 启动注册）；**`evolution_pkg.ops`**（**`http_cache`**：ETag / If-None-Match，**`readonly_api`** 复用）；**`evolution_pkg.domains`**（六域枚举与子模块归属，见 **[INTELLIGENCE_SIX_DOMAINS.md · 代码侧](../docs/INTELLIGENCE_SIX_DOMAINS.md#code-mapping)**））。**兼容**：`evolution_io.py` 仍可作为旧 `from evolution_io import …` 入口。

**新增或变更 JSON 契约（快照 / 沉淀 / 趋势 / 注册表 / SPA 导航等）时建议按序自检**，避免 Schema、校验脚本与消费方漂移：

1. 在 **`docs/schemas/`** 增补或修订 **`.schema.json`**（Draft 2020-12 与现有文件风格一致）；**索引表**维护 **[docs/schemas/README.md](../docs/schemas/README.md)**。  
2. 若有对应 **`scripts/validate_*_schema.py`**，同步字段与必填项；否则新增校验脚本并在下步接入。  
3. 在 **`scripts/run_validate.sh`** 中于合适位置调用该校验（与 **`make validate`**、pre-commit、CI 共用）。**`run_validate.sh`** 与 **`run_update_pipeline.sh`** / **`run_analyze_write.sh`** / **`run_ingest_only.sh`** 等入口 shell 所引用 **`scripts/*.py`** 的路径存在性由 **`scripts/tests/test_run_validate_script_refs.py`** 校验；**`evolution_pkg.pipeline.runner`** 的 **analyze / fast** 步骤表由 **`scripts/tests/test_pipeline_runner_script_refs.py`** 校验；**`docs/DATA_CONTRACTS.md`** / **`docs/ARCHITECTURE.md`** / **`docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md`** / **`docs/EVOLUTION_RUNBOOK.md`** / **`docs/MERGE_AND_RELEASE_CHECKLIST.md`** 对外 HTML 锚点与跨文档深链由 **`scripts/tests/test_data_contracts_doc_anchors.py`**、**`scripts/tests/test_architecture_doc_anchors.py`**、**`scripts/tests/test_intel_playbook_doc_anchors.py`**、**`scripts/tests/test_evolution_runbook_doc_anchors.py`**、**`scripts/tests/test_merge_checklist_doc_anchors.py`** 兜底（另全仓扫描：合并清单文件名 **`MERGE_AND_RELEASE_CHECKLIST.md`** 在 Markdown 链中须带 **`#`** fragment，如 **`#pre-merge`** / **`#doc-index`**；覆盖 **`*.md`** / **`*.mdc`** / **`*.yaml`** / **`*.yml`** / **`*.json`** / **`*.html`**，跳过 **`node_modules`** / **`dist`** 等目录）。**`CONTRIBUTING.md`** 稳定锚点、**`maintainer-hub.html`** 深链，及对「**`CONTRIBUTING`** 清单文件名在 Markdown / HTML 属性中**紧接** **`.md)`**、**`.md"`** 或 **`.md'`** 且无 **`#`**」的全仓扫描（后缀与 MERGE 扫描一致）由 **`scripts/tests/test_contributing_doc_anchors.py`** 兜底。**`docs/README.md`** 在 Markdown 或 **`href`** 中若以 **`.md`** 紧接 **`)`**、**`"`** 或 **`'`** 且无 URL **`#`** fragment，由 **`scripts/tests/test_docs_readme_doc_anchors.py`** 兜底（stem **`docs/README`**，与 **`doc_link_fragment_scan`** 共用）。**仓库根** **`*.html`** 中 **`href="docs/…*.md"`** 须带 **`#`** fragment；**`admin-console/static/index.html`** 中 **`href="docs/…"`** 与 **`href="https://github.com/…/blob/…/docs/…*.md"`** 亦须带 **`#`**，均由 **`scripts/tests/test_root_html_docs_md_hrefs.py`** 兜底（与 **`maintainer-hub.html`** 的 **`test_contributing_doc_anchors`** 子测互补：后者仅扫维护导读）。**`AGENTS.md`** 入口 HTML 锚点与对「**`AGENTS`** 文件名在 Markdown / href 中**紧接** **`.md)`**、**`.md"`** 或 **`.md'`** 且无 **`#`** fragment」的全仓扫描（后缀同上）由 **`scripts/tests/test_agents_doc_anchors.py`** 兜底（**`AGENTS` / `CONTRIBUTING` / `MERGE_AND_RELEASE_CHECKLIST` 无 `#` 链** 的 rglob 判定与 **`scripts/doc_link_fragment_scan.py`** 共用；同模块含 **`MERGE`** §4 闸门表行核心 **`agents-*`** fragment、**`docs/README.md`** 维护者 **`AGENTS` 表行**、以及若干 **枢纽 `docs/**`（含 `docs/README` 与 `MERGE` 清单）、根 `README`/`CONTRIBUTING`、本 `scripts/README`、`spa`/`admin-console` README、PR 模板、**`.github/ISSUE_TEMPLATE`**（如 **`pipeline-triage.md`**）、`maintainer-hub.html`、`.cursor/rules`、`.github/workflows`（如 **`ci.yml`** / **`ingest-pipeline.yml`** / **`pr-candidates.yml`** / **`update-pipeline.yml`**）头部注释中 `AGENTS.md#…`** 断言；`docs/README` 维护者表行片段与 **`test_docs_readme_agents_row_*`** 共用常量）。  
4. 在 **`scripts/README.md`** 本表与相关文档（如 **[DATA_CONTRACTS.md](../docs/DATA_CONTRACTS.md)**）中注明新文件路径与消费者（Hub、总线、`readonly_api` 路由等）；**`docs/schemas/README.md`** 索引表须包含新 **`*.schema.json`**（**`scripts/tests/test_schemas_readme_index.py`** 会校验）。平台级扩展清单见 **[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](../docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist)**。  
5. **大功能拆 PR、提前挂健康/只读骨架**：见 **[INCREMENTAL_BUILD_PLAYBOOK.md](../docs/INCREMENTAL_BUILD_PLAYBOOK.md)**（组件引入顺序 · 调试闭环 · **[PR 切片模板](../docs/templates/incremental-pr-slice.md)**）。

<a id="scripts-by-role"></a>

## 脚本分类（按职责）

顶层 `scripts/` 除目录 **`evolution_pkg/`**（可 import 的库）与 **`tests/`**（单测）外，按下表浏览；**具体参数与是否走外网仍以下方命令表为准**。与 [docs/ARCHITECTURE.md#seven-layers](../docs/ARCHITECTURE.md#seven-layers) 七类模块可对读。

| 职责 | 典型脚本 / Shell |
|------|-------------------|
| **闸门与对账** | **`run_validate.sh`**（**`make validate`** 总入口）、**`run_validate_fast.sh`**（**`make validate-fast`**，非合并真源）、`validate-evolution-manifest.py`、`validate-evolution-candidates.py`、`validate_evolution_hint_decisions.py`、`validate_evolution_registry_schema.py`、`validate_golden_mapping.py`（**`--dir fixtures/ai_mapping_golden`**；Schema + **expect ⊆ registry**）、`validate_analysis_snapshot_schema.py`、`validate_sediment_artifacts_schema.py`、**`validate_pipeline_metrics_schema.py`**（**`fixtures/pipeline_metrics_example.json`** + 可选 **`artifacts/pipeline-metrics-*.json`**）、**`validate_ai_overlay_step_schema.py`**、**`validate_ai_analysis_overlay_schema.py`**、`check_manifest_drift.py`、`check_nav_links_registry.py`、`sync_site_nav.py`（`--check` / 写回）、`check_skip_bar_404.py` |
| **编排（分析写盘）** | `run_update_pipeline.sh`、`run_analyze_write.sh`、`run_pipeline_steps.py` → **`evolution_pkg.pipeline.runner`** |
| **抓取与入池** | `run_ingest_only.sh`、`ingest_opinion_law.py`（配置 **`ingest_config.json`**、**`maps_to_hints.json`**）；运行约束与信源分层见 **[INTEL · §2—2a](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)**；微博/主媒 App 流与开放平台见 **[INTEL · §2b](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)** |
| **人审合并** | **`python3 -m evolution_pkg.candidate_merge`**（**`main()`** 在包内）；根 **`merge_candidates_to_manifest.py`** 为薄壳 |
| **分析与血缘** | `analysis_engine.py`、**`evolution_pkg.analysis_lineage`**（**`lineage_utils.py`** 兼容重导出） |
| **沉淀、SQLite、趋势** | `sqlite_store.py`、`import_sediment_json_to_sqlite.py`、`sediment_trends.py`、`list_analysis_snapshot_history.py`；历史表读写见 **`evolution_pkg.analysis_snapshot_history`** |
| **站点与双轨呈现** | `sync_spa_public.py`、`gen_nav_links_ts.py`、`gen-sitemap.py`、`gen_site_search_index.py`（**`make site-search-index`** → **`assets/site-search-index.json`**） |
| **运维与侧车** | `print_evolution_status.py`、`evolution_intelligence_digest.py`（**`make digest`**）、`diff_analysis_snapshot.py`、`readonly_api.py`（**`requirements-api.txt`**）、`query_evolution_duckdb.py`（**`requirements-analytics.txt`**）、**`analytics/`**（DuckDB 示例 SQL）；容器编排见根目录 **[DOCKER.md](../docs/DOCKER.md)**、**`make docker-up`** / **`make docker-up-api`** |
| **兼容入口** | `evolution_io.py`（`from evolution_io import …` → **`evolution_pkg.io`**） |

### 文件命名（连字符与下划线）

仓库中并存 **`validate-evolution-*.py`**（连字符，较早入口）与 **`validate_*` / `check_*`**（下划线）。**新增脚本建议统一为 `snake_case.py`**，并与 **`run_validate.sh`** 的调用名一致。旧名保留以免破坏文档、CI 与外部引用；**不建议**对大量现网脚本一次性批量重命名。

<a id="pkg-migrate-queue"></a>

### `evolution_pkg` 收束队列（依次推进）

供排期用：**先**在包内补函数与单测、**再**把顶层脚本收成薄 CLI，避免双实现。每步合并前后均 **`make validate`**。与 **[MODULE_INVENTORY · evolution_pkg](../docs/MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#evolution-pkg)** · **[INTELLIGENCE · 代码映射](../docs/INTELLIGENCE_SIX_DOMAINS.md#code-mapping)** 对读。

| 序 | 顶层脚本 / 区域 | 建议落点 | 备注 |
|----|------------------|----------|------|
| 1 | **`diff_analysis_snapshot.py`** | **`evolution_pkg.analysis_diff`**（`build_report` / `snapshot_diff_json*`） | **已完成**：CLI 仅 git/路径；对比逻辑可 `from evolution_pkg.analysis_diff import …` 复用 |
| 2 | **`lineage_utils.py`** | **`evolution_pkg.analysis_lineage`** | **已完成**：**`analysis_pipeline`** 已直引包；**`lineage_utils.py`** 仅重导出 |
| 3 | **`validate-evolution-manifest.py`** / **`validate-evolution-candidates.py`** | **`evolution_pkg.signals_flat_validate`** | **已完成**：脚本仅 IO + **exit**；单测 **`test_signals_flat_validate.py`** |
| 4 | **`list_analysis_snapshot_history.py`** | **`python3 -m evolution_pkg.analysis_snapshot_history`**（**`main()`** 在包内） | **已完成**：根脚本为薄壳；**`test_sqlite_snapshot_history`** 覆盖 **`main --json`** |
| 5 | **`ingest_opinion_law.py`** / **`analysis_engine.py`** / **`merge_candidates_to_manifest.py`** | 维持**官方 CLI 入口**；大块逻辑应在包内（**`ingest_opinion_pool`**、**`ingest_json_http`**、**`ingest_maps`**、**`ingest_https`**、**`ingest_fetch`**、**`ingest_rss`**、**`analysis_pipeline`**、**`evolution_pkg.candidate_merge`** 等） | **merge** 薄壳 + **`-m evolution_pkg.candidate_merge`**；ingest 推荐 **`-m evolution_pkg.ingest_opinion_pool`**；分析推荐 **`-m evolution_pkg.analysis_pipeline`**（根 **`analysis_engine.py`** 薄壳） |

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
| 人审合并 | **`python3 -m evolution_pkg.candidate_merge`**、**`merge_candidates_to_manifest.py`**（薄壳） |
| 分析 + 当日快照 | `analysis_engine.py` |
| 沉淀 + 本地库 | `analysis_engine.py --sediment`、`sqlite_store.py`（含 **`analysis_snapshot_history`**）、`import_sediment_json_to_sqlite.py`、`list_analysis_snapshot_history.py` |
| 跨日汇总 | `sediment_trends.py` |
| 规则闭环 JSON | `validate_evolution_hint_decisions.py` |
| 闸门 / 对账 | `validate-evolution-*.py`、`validate_evolution_registry_schema.py`、`validate_analysis_snapshot_schema.py`、`validate_sediment_artifacts_schema.py`、`validate_pipeline_metrics_schema.py`、**`validate_ai_overlay_step_schema.py`**、**`validate_ai_analysis_overlay_schema.py`**、`check_nav_links_registry.py`、`check_manifest_drift.py`、`sync_site_nav.py`、`check_skip_bar_404.py` |
| 站点辅助 | `gen-sitemap.py`、`gen_site_search_index.py`（**`make site-search-index`**） |

| 命令 | 作用 | 外网 |
|------|------|------|
| `bash scripts/run_ingest_only.sh` | 抓取 → `evolution-candidates.json` → 校验候选（可附加 `ingest_opinion_law.py` 参数） | 是 |
| `WRITE_INGEST_SUMMARY=1 bash scripts/run_ingest_only.sh` | 同上并写入根目录 `ingest-summary.json`（**已 gitignore**；CI 默认开启） | 是 |
| `python3 scripts/ingest_opinion_law.py --full-pool` / `PYTHONPATH=scripts python3 -m evolution_pkg.ingest_opinion_pool --full-pool` / `make ingest-full` | 单次忽略 `require_route_match`，全量进池 | 是 |
| `ingest_config.require_route_match` | `true`：仅保留命中 `routes` 的 RSS/法规线索并清理旧未命中候选 | — |
| `bash scripts/run_update_pipeline.sh` | 由 **`evolution_pkg.pipeline.runner`**（经 `run_pipeline_steps.py analyze`）编排：与 **`run_validate.sh` 相同的前半段**（至单测）+ **`--sediment`** + **`sediment_trends`** + 沉淀/趋势 Schema + 快照 Schema + **`--check`**；结束写 **`artifacts/pipeline-metrics-*.json`**（`SKIP_PIPELINE_TELEMETRY=1` 可关）。**`runner` 步骤表内 `scripts/*.py` 路径**由 **`scripts/tests/test_pipeline_runner_script_refs.py`** 校验存在性 | 否 |
| `bash scripts/run_analyze_write.sh` / **`make evolution-fast`** | **`run_pipeline_steps.py fast`**：同上，步骤较少。**不**重跑 manifest/漂移/单测/顶栏。须先 **`make validate`**，提交前仍须 validate | 否 |
| `python3 scripts/diff_analysis_snapshot.py` | 对比两份 `analysis-snapshot.json`，输出 Markdown 或 `--json`（贴 PR） | 否 |
| `python3 scripts/query_evolution_duckdb.py` | DuckDB 附加 `data/evolution.db` 跑 SQL（需 `pip install -r requirements-analytics.txt`） | 否 |
| `python3 scripts/list_analysis_snapshot_history.py` | 列出 SQLite **`analysis_snapshot_history`** 元数据（`run_id`、时间、`snapshot_json` 字节数）；`--json` | 否 |
| `PYTHONPATH=scripts python3 -m uvicorn readonly_api:app` | 只读 HTTP：`/health`、`/snapshot`、`/trends`、`/manifest`、`/registry`、`/sediment`、`/candidates`（**敏感**·未审候选）、`/hint-decisions`（人审决策·宜受控）、`/hint-rules`（分析规则）、`/maps-to-hints`（ingest 映射）、`/ingest-config`（RSS 源·宜受控）、`/site-meta`、**`/site-search-index`**（**可选**·无文件 **404**）、`/snapshot-history`、`/snapshot-history/{run_id}`（**ETag** + **Cache-Control**；**If-None-Match** 命中返回 **304**；动态历史体 **no-store**；**`/sediment`** 无文件时 **404**；需 `requirements-api.txt`；历史依赖本地 `data/evolution.db`） | 否 |
| `make docker-up` / `make docker-up-api` / `make docker-up-admin` | **Docker Compose**：MPA **8765**；**`api`** → 只读 API **8099**；**`admin`** → 管理端脚手架 **8100**（**[admin-console/README.md](../admin-console/README.md)** · **[ADMIN_CONSOLE · §7](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**）；开发挂载见 **[DOCKER.md](../docs/DOCKER.md)** | 否（构建/拉镜像时可能需网络） |
| `make serve-reader` | 根目录 **Python** 静态服务读者 MPA **http://127.0.0.1:8000/**（默认 **`READER_PORT=8000`**；占用时可 **`READER_PORT=8001`**；无 Docker、与 **8765** 错开；须 **http** 以便 **`fetch`** JSON）；见 **[README.md](../README.md)** | 否 |
| `python3 scripts/validate_evolution_registry_schema.py` | **`evolution-registry.json`** 与 **`docs/schemas/evolution-registry.schema.json`**；已并入 **`make validate`** 与 **`make test`** | 否 |
| `bash scripts/run_validate.sh` | 与 **`make validate`** 相同的全套校验（compileall + JSON + **registry Schema** + 对账 + **navLinks** + 顶栏 + **404 skip-bar** + 单测 + `--check` + 快照/沉淀/趋势 Schema） | 否 |
| `make validate-fast` / `bash scripts/run_validate_fast.sh` | **子集**闸门（compileall + manifest/候选/registry/navLinks + 单测 + **`analysis_engine --check`** + 快照 Schema + **`validate_pipeline_metrics_schema`** + **`validate_ai_overlay_step_schema`** + **`validate_ai_analysis_overlay_schema`**）；**不**含 drift、顶栏写回检查、skip-bar、黄金集、hint 决策、沉淀 JSON Schema 等；**CI / pre-commit 不跑**；**不可**替代合并前 **`make validate`** | 否 |
| `make trends` / `python3 scripts/sediment_trends.py` | 仅根据已有沉淀重算 `assets/sediment-trends.json`（不跑分析引擎） | 否 |
| `make status` / `python3 scripts/print_evolution_status.py` | 先打印 `assets/site-meta.json` 的 **site_version**；若存在则打印 **`artifacts/ai-overlay-step.json`**（可含 **token** 摘要：`otel_hints` 或 **`usage`**）、**`assets/ai-analysis-overlay.json`**、**`artifacts/ai-overlay-llm-dead-letter.txt`** 一行摘要；再打印 `analysis-snapshot.json` 合并计数、hint 决策统计、闭环缺口条数（及 rule_id 列表） | 否 |
| `make digest` / `python3 scripts/evolution_intelligence_digest.py` | 将 **快照 + 可选 sediment-trends + 沉淀** 组装为 **Markdown** 摘要（热力/共现/闭环缺口/趋势表）；无 LLM；与 **`diff_analysis_snapshot.py`**（两版 diff）互补 | 否 |
| `python3 scripts/analysis_engine.py` / `PYTHONPATH=scripts python3 -m evolution_pkg.analysis_pipeline` | 写 **`assets/analysis-snapshot.json`** 时默认向 **`evolution.db`** 表 **`analysis_snapshot_history`** 追加只读历史（**`--no-sqlite-snapshot-history`** 关闭） | 否 |
| `python3 scripts/analysis_engine.py --check` / `PYTHONPATH=scripts python3 -m evolution_pkg.analysis_pipeline --check` | 跑分析逻辑、校验输出结构，**不写** `analysis-snapshot.json`（CI / pre-commit；**不**与上期快照做 diff 提示）；根级含 **`run.run_id` / `run.repo_revision`** 血缘；`sources` 含 `candidate_review_breakdown`、`hint_decisions` | 否 |
| `python3 scripts/validate_analysis_snapshot_schema.py` | 用 **jsonschema** 校验**已提交**的 `assets/analysis-snapshot.json` 与 `docs/schemas/analysis-snapshot.schema.json`（无文件则跳过）；已并入 `make validate` | 否 |
| `python3 scripts/validate_pipeline_metrics_schema.py` | 校验 **`fixtures/pipeline_metrics_example.json`** 及（若存在）**`artifacts/pipeline-metrics-*.json`** 与 **`docs/schemas/pipeline-metrics.schema.json`**；已并入 **`make validate`** | 否 |
| `make clean-pipeline-metrics-dry-run` | 仅 **`echo`** 将删除的 **`artifacts/pipeline-metrics-*.json`** 路径（**不**删除） | 否 |
| `make clean-pipeline-metrics` | 删除 **`artifacts/pipeline-metrics-*.json`**（旧格式遥测会触发 validate 警告；文件已 **gitignore**） | 否 |
| `make clean-overlay-artifacts` | 删除 **`artifacts/ai-overlay-step.json`** 与 **`artifacts/ai-overlay-llm-dead-letter.txt`**（若存在；**gitignore**） | 否 |
| `python3 scripts/validate_sediment_artifacts_schema.py` | 校验 **`data/sediment.json`**、**`assets/sediment-trends.json`** 与 **`docs/schemas/sediment*.schema.json`**（无文件则跳过）；已并入 `make validate` | 否 |
| `python3 scripts/gen_nav_links_ts.py` | 默认：检查 **navLinks.ts** 是否与 **spa/nav.config.json** 一致；**`--write`** 写回 **navLinks.ts**（**`make gen-nav-links`**） | 否 |
| `python3 scripts/check_nav_links_registry.py` | **nav.config.json** 与 registry 页面集一致，且 **navLinks.ts** 为生成结果（**`evolution_pkg.spa_nav`**；无 **spa/package.json** 则跳过）；已并入 `make validate` 与 **`make test`** | 否 |
| `python3 scripts/merge_candidates_to_manifest.py <id>…` / **`PYTHONPATH=scripts python3 -m evolution_pkg.candidate_merge <id>…`** | 人审后合并进 manifest；**须** `review_state=queued_for_manifest`（`--force` 跳过） | 否 |
| `python3 scripts/validate-evolution-manifest.py` | 校验正式库结构 | 否 |
| `python3 scripts/validate-evolution-candidates.py` | 校验候选结构 | 否 |
| `python3 scripts/validate_evolution_hint_decisions.py` | 校验 `assets/evolution-hint-decisions.json`；根级可选 `schema_version: 1`；`rule_id` 若填写须 ∈ `evolution-hint-rules.json` 的 `rules[].id` | 否 |
| `python3 scripts/check_manifest_drift.py` | **对账**：`maps_to.pages` ∈ **`scripts/evolution-registry.json`** 且文件存在；`lab_factors` 与 registry 及 **`lab.js` 因子 id 集合一致**；`ingest_config` / `maps_to_hints` / `gen-sitemap` PRIORITY | 否 |
| `make test` | **`validate_evolution_registry_schema.py`** + unittest（`PYTHONPATH=scripts`）+ **`check_nav_links_registry.py`** + **`validate_sediment_artifacts_schema.py`** | 否 |
| `make test-readonly-api` | 安装 **`requirements.txt` + `requirements-api.txt`** 后跑 **`test_readonly*.py`**（**`test_readonly_api`**：ETag / 304；**`test_readonly_proxy_segment_sync`**：管理端 **`READONLY_PROXY_SEGMENTS`** 与 **`readonly_api`** 单段路径对账；本地未装 fastapi 时 **`make validate`** 中相关用例 **skip**） | 否 |
| `make test-admin-console` | 安装 **`admin-console/requirements.txt`** 后跑 **`admin-console/tests`**（管理端脚手架烟测；单页 UI 真源 **[ADMIN_CONSOLE · §7](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**） | 否（`pip install` 可能需网络） |
| `make merge-ready` | **`make validate`** 成功后执行 **`make test-readonly-api`** 与 **`make test-admin-console`**（合并前推荐；见 **[docs/MERGE_AND_RELEASE_CHECKLIST.md · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**） | 否 |
| `python3 scripts/sync_site_nav.py` / `make sync-nav` | 按 **`partials/skip-bar.inc.html`** + **`partials/site-nav.inc.html`** 写回根目录各页（跳过 **404**、legacy 单页）；**`maintainer-hub.html`** 在五链后再拼 **`#mh-spine-map` / `#mh-boundaries` / `#mh-reader-admin-matrix`**（**`build_skip_bar`** + 源码常量 **`MAINTAINER_HUB_SKIP_EXTRA`**，与页内 **`toc--pilot`** 前三节一致，**勿**在 HTML 手改）；**404.html** 顶栏/skip 手维护；**legacy-all-in-one.html** 五链 skip 手维护；改模板后须与 **`check_skip_bar_404.py`** 及单测 **`test_legacy_skip_bar_parity`**、**`test_spa_skip_bar_parity`**、**`test_sync_site_nav`** 对表（已含 **`make validate`**） | 否 |
| `make check-site-nav` | 顶栏与模板一致（已并入 `make validate`） | 否 |
| `bash scripts/install-git-hooks.sh` | 启用 `.githooks/pre-commit`（**`bash scripts/run_validate.sh`**，等同 **`make validate`**；**不**跑 **`validate-fast`**）；**pre-commit** 注释、装钩成功 **echo** 与 **`scripts/run_validate.sh`** 文首注释同构（均含 **MERGE** / **maintainer-hub** / **make help（CONTRIBUTING.md#contributing-five-minute · #contributing-pr-evidence-triad · #contributing-change-to-command）**） | 否 |
| `SITE_BASE=https://… make sitemap` | 生成根目录 `sitemap.xml` | 否 |
| `make site-search-index` | 由 **`evolution-registry.json` · `pages`** 与各页 **`<title>`** 生成 **`assets/site-search-index.json`**（可选站内搜索；**不入** `make validate`） | 否 |
| `make spa-sync` / `python3 scripts/sync_spa_public.py` | 根目录 HTML/assets/docs → `spa/public`（剥顶栏供 iframe）；**MERGE** / **maintainer-hub** 与判型见 **[开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)** · **[PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)** · **[动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)**（根 **`make help`** 文首三锚对表） | 否 |
| `make spa-build` | `spa-sync` + `npm ci` + Vite 生产构建 → `spa/dist`（CI **`spa-build`** job：变更触及 `spa/`、**`evolution-registry.json`**、sync 输入等时运行，见 `ci.yml`）；判型与 **`make help`** 三锚同上 | 否（`npm ci` 需 registry） |
| `make spa-install` | 仅 `spa` 目录 `npm ci` | 否（需 registry） |

<a id="sync-site-nav-source"></a>

#### `sync_site_nav.py` 真源摘要（与 MERGE §1、AGENTS 双轨一致）

- **五链**：来自 **`partials/skip-bar.inc.html`** 占位符；**顶栏**来自 **`partials/site-nav.inc.html`**。与导航相关的 HTML 注释**仅**放在上述块**内部**；勿在 **`<div class="skip-bar">` / `<header class="site-nav">`** 外再写一份（``sync_site_nav`` 只替换整块，块外注释不参与对账）。
- **`maintainer-hub.html` 仅**：`build_skip_bar()` 追加 **`MAINTAINER_HUB_SKIP_EXTRA`**，并把 **`aria-label`** 改为「快捷跳转与本页锚点」；改 `#mh-*` 或 pill 文案须同步源码常量 + **`make sync-nav`** + **`scripts/tests/test_sync_site_nav.py`**。
- **不写回**：**`404.html`**、**`legacy-all-in-one.html`**（对表 **`check_skip_bar_404.py`** 等）。

在确定性快照之上**可选**叠加 **AI 服务解读**（独立产物与配置、不并入快照必填域）的约定与检查单：**[docs/AI_ASSISTED_ANALYSIS_LAYER.md](../docs/AI_ASSISTED_ANALYSIS_LAYER.md)**；配置形状示例：**[docs/examples/ai_analysis_overlay.example.json](../docs/examples/ai_analysis_overlay.example.json)**。契约校验：**`validate_ai_analysis_overlay_schema.py`**（无文件则跳过；有则与 **`analysis-snapshot.json`** 的 **`run.run_id`** 对账）；侧车 **`artifacts/ai-overlay-step.json`**：**`validate_ai_overlay_step_schema.py`**（无文件则跳过）。写入入口：**`python3 scripts/write_ai_analysis_overlay.py`**（默认跳过；**`--stub`** 或 **`make ai-overlay-stub`** 占位；**`AI_OVERLAY_ENABLE=1`** + API 环境变量可选外呼）；**`write_ai_analysis_overlay_stub.py`** 为兼容别名。**`make analyze`** 在 **`--check`** 之后跑 overlay 写入步骤（未启用则不写盘）。

推荐节奏：ingest 单独排期 → 本地审阅 merge → 再跑 `run_update_pipeline.sh`（与 [analysis-hub · 方法与演进总线](../analysis-hub.html#panorama) 对表）。**双轨**：增删注册页须维护 [spa/nav.config.json](../spa/nav.config.json) 并 **`make gen-nav-links`**（已含于 **`make spa-build`**）；**`check_nav_links_registry.py`** 已含于 **`make validate`**。说明见 [spa/README.md](../spa/README.md)。**舆情 / 制度 / 国情**跟踪与人审节奏见 [docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)（[§2—2a](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers) · [§2b](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)）。

- **`scripts/ingest_config.json`**：`routes` 正则命中后写入 `maps_to`；**`scripts/maps_to_hints.json`** 按 **RSS 链接 host** 与 **标题/摘要关键词** 再合并 `pages` / `lab_factors`（仍须人审）。可选 **`fetch_pacing`**（**`after_rss_fetch`** / **`after_law_html_fetch`** / **`after_json_feed_fetch`**，秒，默认 **0.8 / 1.0 / 0.8**，上限 **120**）控制各源两次 GET 间隔，见 **[INTEL playbook · §2—2a](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**。可选 **`json_feeds`**：每项含 **`id`**、**`url`**（**https**）、**`items_path`**（点分路径，空则根为 JSON 数组）、**`max_items`**、**`default_kind`**，以及可选 **`keys_title` / `keys_link` / `keys_summary`**（字符串键优先序列表）；由 **`ingest_opinion_law.py`** 拉取并与 RSS 同池合并，**`source.type`** 为 **`json_http`**。侧车若输出固定 JSON 形状，可只配映射而不拷贝对方代码。**`admin-console`** 首页数据源目录可勾选并**复制 `rss_feeds` 草案 JSON**（与只读 **`/ingest-config`** 去重时附 **`omitted_already_in_ingest`**），仍须手工合并本文件并经 **PR** + **`make validate`**（见 [admin-console/README.md](../admin-console/README.md) · **[ADMIN_CONSOLE · §7](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)**）。
- **`scripts/evolution-hint-rules.json`**：`analysis_engine` 中条件类 `evolution_hints` 的外置规则；可选 **`track_closure`**：触发且决策 JSON 中尚无同 `rule_id` 的 done/rejected 时，快照含 **`hint_closure_gaps`**（分析页高亮）。与**已有** `assets/analysis-snapshot.json` 对比可生成「相较上期」的 diff 提示（`--check` 模式跳过 diff）。

双周反哺清单：[docs/EVOLUTION_RUNBOOK.md](../docs/EVOLUTION_RUNBOOK.md)。**舆情与制度跟踪**：[docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md](../docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)。架构总览：[docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)。**模块全量梳理与升级矩阵**：[docs/MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](../docs/MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)。首次参与仓库开发见根目录 [CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute)。
