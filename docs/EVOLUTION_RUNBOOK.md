# 可进化闭环 · 双周反哺节奏（运行手册）

目标：让「观测 → 入库 → 分析 → 改站内核/沙盘」**按固定节奏发生**，避免只堆 JSON 不反哺正文。

## 自动化周历（GitHub Actions）

| 触发 | Workflow | 作用 |
|------|----------|------|
| 每周二 08:00 UTC | **Ingest candidates** | 抓取候选 → artifact（默认不回写 `main`） |
| 每周一 16:00 UTC | **Update pipeline** | 全量校验 + 写快照/沉淀/趋势 → artifact |
| 手动 | **PR · refresh candidates** | ingest 后直接开 PR 更新 `evolution-candidates.json`（仍须人审后再 merge manifest） |
| push / PR | **CI** | **validate** job：`run_validate.sh`（**`make validate`** 同款）并安装 **`requirements-api.txt`** 跑 **`test_readonly*.py`**；**spa-build** 为按路径触发的另 job，见 [docs/README 文首](../docs/README.md) |

**合并 PR 前推荐**：**`make merge-ready`**（**`validate`** + **`test-readonly-api`** + **`test-admin-console`**），见 **[MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)**。

合并 artifact 到仓库、推送后，线上 Pages 与 `site-data-bus` / `analysis.js` 读数才会变——见根目录 [README.md](../README.md)「定时流水线」。

**管理端 Web 上编排 ingest / 分析与数据源**：设计矩阵与阶段见 **[ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)**（不改变上表 Actions 为默认真源）。

<a id="accelerate"></a>

## 加速本地迭代（不削弱人审）

- **`make analyze`**：前置校验由 **`evolution_pkg.pipeline.runner`** 的 **analyze** 步骤表执行——与 **`run_validate.sh` 直至单测** 对齐（compileall **scripts**、manifest/候选/hint 校验、registry Schema、对账、navLinks、``sync_site_nav --check``、单测）。**不含** 完整 validate 的 **`check_skip_bar_404.py`**、**不** ``compileall admin-console``；写盘与事后 Schema / ``--check`` 顺序亦与 validate **后半段**不同。**合并前仍须** **`make validate`**（或 **`make merge-ready`**），**勿**以「仅 analyze 绿」代替合并闸门。
- **`make validate` 通过后**，若**同一工作区**内只反复调 manifest/候选并希望**快速**重算热力与趋势，可用 **`make evolution-fast`**：仅执行 `analysis_engine --sediment` → `sediment_trends` → 快照 Schema → `--check`，**跳过** 自 compileall 至单测的整段前置（manifest、registry Schema、对账、navLinks、顶栏、单测等）。改完 JSON 未 validate 就提交会有风险，故**提交前仍须** `make validate`；与 CI **`validate`** 完全对齐时再 **`make merge-ready`**（见文首「本地与 CI」段）。
- **只看读数、不写文件**：`make status`。
- **仅跨日趋势**（沉淀已存在）：`make trends`。

<a id="sqlite-sidecar"></a>

## 本地 SQLite 与快照历史（侧车）

- **`data/evolution.db`** 默认 **gitignore**：含 **`sediment_entry`**（与 `sediment.json` 双写）与 **`analysis_snapshot_history`**（每次本地/流水线 **`analysis_engine.py`** 写 **`assets/analysis-snapshot.json`** 时按 **`run_id`** 追加整份快照 JSON，可用 **`--no-sqlite-snapshot-history`** 关闭）。
- **闸门真源**仍是仓库内**已提交**的 JSON；库仅加速查询与本地历史对比。**可删除 `evolution.db` 后重跑 `analysis_engine` / `make analyze`** 重建（历史行会丢，不影响 CI 与 `make validate`）。
- 浏览历史元数据：`python3 scripts/list_analysis_snapshot_history.py`；只读 HTTP：**`readonly_api`** 的 **`/snapshot-history`**、**`/snapshot-history/{run_id}`**（需 **`PYTHONPATH=scripts`**）。

<a id="continuous-push"></a>

## 加快「观测进仓库」的节奏

1. 定时 ingest 的 artifact 下载后替换 `evolution-candidates.json`，或用 **PR · refresh candidates** 减少手工下载步骤。  
2. 候选审阅与 `merge_candidates_to_manifest` 仍是**闸门**；勿为提速跳过。  
3. 分析侧：本地优先 **`make evolution-fast`**（在已 validate 前提下）缩短双周内多轮看板刷新。

## 建议周期

每 **2 周** 一次，单次耗时约 **30～45 分钟**（不含深度改文）；熟练且 JSON 已绿时，其中 **步骤 5** 可多次用 `make evolution-fast` 代替完整 `make analyze`。

若需**更大范围**把全站模块、综合推演判据与分析读数放在一轮里重推，见 **[SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md](./SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md)**（可与本次双周 checklist 合并或分天进行）。

## Checklist

**环境**：首次或更新依赖后执行 `python3 -m pip install -r requirements.txt`（`make validate` / CI 需 **jsonschema** 校验 `analysis-snapshot` 与 `docs/schemas/`）。

**推演纪律**：结构化思考前先扫 [DEDUCTION_STRATEGY.md](./DEDUCTION_STRATEGY.md)（三色分层、单轮七步、偏误表）；与 [综合推演](../synthesis.html) §2 / §12 / §13 及 [总览 · 三问](../index.html#three-questions) 对齐。

**大版本或改站壳后**（顶栏、`index.html` 读站指路、总线/版本展示等）：在 **`make validate`** 之外，建议再过 [SITE_REVIEW_THREE_PASSES · 四角色复查](./SITE_REVIEW_THREE_PASSES.md#four-perspectives-review) 的**发布前轻量清单**；读者预期与站内 **`docs/*.md`** 在静态部署下的行为见 [PLATFORM_CAPABILITY_MAP · §7](./PLATFORM_CAPABILITY_MAP.md#reader-and-release)。维护 **全站 SPA** 时，改根目录 **`index.html`** 后须 **`make spa-sync`**（见 [`spa/README.md`](../spa/README.md)）。

| 步骤 | 动作 | 产出/记录 |
|------|------|-----------|
| 1 | `make ingest`（或 **Actions → Ingest candidates** 定时/手动跑并下载 artifact） | 刷新 `evolution-candidates.json`；`require_route_match=true` 时仅保留命中 `routes` 的线索；`maps_to` 另合并 `scripts/maps_to_hints.json`（host/关键词）。CI 可在 Run 摘要里查看各源是否抓取成功 |
| 2 | 浏览候选：将噪点标 `review_state: noise`（不参与分析热力）；拟入库标 `queued_for_manifest`；可写 `reviewer_note`（≤500 字） | 本地或 PR 中更新 `evolution-candidates.json` |
| 3 | 对值得入库的 id（须已 `queued_for_manifest`）：`python3 scripts/merge_candidates_to_manifest.py …`（应急 `--force`） | 更新 `evolution-manifest.json` |
| 4 | `make validate` | 通过校验 + `analysis_engine --check` + **对账脚本** |
| 5 | `make analyze`（已 `make validate` 且本步要跑多轮时可用 `make evolution-fast`）或 `make trends` 仅刷新趋势 | 更新 `analysis-snapshot.json`（根级 **`run.run_id`** / **`run.repo_revision`** 标识本次流水线，便于与 Actions 日志或本地日志对齐）、**`data/sediment.json`**（当日条目同步 `run_id` / `repo_revision`；含 `hint_closure_gaps_n` / `hint_decisions_total`）、**`assets/sediment-trends.json`**（含 `closure_backlog` 近 14 日） |
| 6 | 打开 `analysis-hub.html`（或读 `analysis-snapshot.json`） | 看热力与共现；需要核对「哪次跑出来的」时看 `run` 块 |
| 7 | 处理 **≥1 条** `evolution_hints`（`analysis-snapshot.json` 中为对象时可点链到 `target_pages`）：**落实**或 **显式否决**；在 **`assets/evolution-hint-decisions.json`** 追加一条记录（`id`、`action`: `done` / `rejected` / `deferred`、`recorded_at` 等；**若规则在 `evolution-hint-rules.json` 中 `track_closure: true`，请填写 `rule_id`** 与提示一致，以便快照清空 `hint_closure_gaps`） | 闭环有可检索的决策痕迹；分析页与快照 `sources.hint_decisions` 可看到累计统计 |
| 8 | 打开 `lab.html`：按热力勾选因子做一轮沙盘 | 与 manifest 映射一致性感性校验 |
| 9 | `git commit` & `push` | 站点与仓库同步 |

## 抓取失败可见性（ingest）

- **GitHub Actions**：`ingest-pipeline` 的 **Job Summary** 会列出各 RSS / 法规源的 `ok` / `failed` 与错误摘要（依赖 `WRITE_INGEST_SUMMARY=1` 与 `ingest-summary.json`）。定时失败会另开 Issue。
- **本地**：`WRITE_INGEST_SUMMARY=1 bash scripts/run_ingest_only.sh` 写入根目录 `ingest-summary.json`（已 gitignore），便于与 CI 对齐排查。

## PR 与决策追溯

改 HTML 或 manifest 时，建议在 PR 描述中写明：**对应 `evolution-hint-decisions.json` 的 `id` 或 `rule_id`**，或对应 **`evolution-manifest` / 候选 `signals[].id`**。与 [ARCHITECTURE.md § 决策与正文的双向追溯](./ARCHITECTURE.md#decision-traceability) 一致。

## 关于「规则闭环缺口」

分析页若出现 **hint_closure_gaps** 或「规则闭环缺口 N 条」，表示：`evolution-hint-rules.json` 里 **`track_closure: true`** 的规则已触发，但 **`evolution-hint-decisions.json`** 中尚无同 **`rule_id`** 的 **done** / **rejected** 记录——这是**待办清单**，不是 CI 失败。冷启动或双周尚未处理时出现多条缺口属正常；写入决策后缺口会消失。**延期 deferred** 不算闭环。进化闭环页顶部会拉取快照显示摘要（需 http(s)）。

## 与人审闸门一致

- 未经审阅 **不** merge 进 manifest。  
- 改 HTML 大段与改 manifest **可同 PR**，但须在描述里写清「对应哪条信号 / 哪条 hint」。

## 相关命令

见仓库根 [README.md](../README.md) 与 [scripts/README.md](../scripts/README.md)。

在 GitHub 上开 PR 修改 manifest/候选时，仓库已配置 [PR 模板](../.github/pull_request_template.md)，请勾选自检项。

## 对账脚本

`python3 scripts/validate_evolution_registry_schema.py`：对照 [**`docs/schemas/evolution-registry.schema.json`**](schemas/evolution-registry.schema.json) 校验 **`scripts/evolution-registry.json`** 结构（先于语义对账）。已并入 **`make test`**、**`make validate`** 与 CI。

`python3 scripts/check_manifest_drift.py`：检查 `maps_to.pages` 是否列入 **`scripts/evolution-registry.json`** 且文件存在；`lab_factors` 是否与 registry / `lab.js` 一致；并校验 ingest 配置与 `maps_to_hints`、`gen-sitemap` PRIORITY；**`evolution-hint-rules.json`** 的 `rules[].id`（唯一、非空）与 `track_closure` 类型、`target_pages` ⊆ registry。已并入 `make validate` 与 CI。

`python3 scripts/validate_evolution_hint_decisions.py`：校验 **`assets/evolution-hint-decisions.json`** 结构及 `related_pages` ⊆ registry；根级可选 **`schema_version`: 1**；若填写 **`rule_id`** 则须为 **`evolution-hint-rules.json`** 中已有规则的 `id`。
