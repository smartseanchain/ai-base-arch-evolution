# 可进化闭环 · 双周反哺节奏（运行手册）

目标：让「观测 → 入库 → 分析 → 改站内核/沙盘」**按固定节奏发生**，避免只堆 JSON 不反哺正文。

## 建议周期

每 **2 周** 一次，单次耗时约 **30～45 分钟**（不含深度改文）。

## Checklist

| 步骤 | 动作 | 产出/记录 |
|------|------|-----------|
| 1 | `make ingest`（或 **Actions → Ingest candidates** 定时/手动跑并下载 artifact） | 刷新 `evolution-candidates.json`；`require_route_match=true` 时仅保留命中 `routes` 的线索；`maps_to` 另合并 `scripts/maps_to_hints.json`（host/关键词）。CI 可在 Run 摘要里查看各源是否抓取成功 |
| 2 | 浏览候选：将噪点标 `review_state: noise`（不参与分析热力）；拟入库标 `queued_for_manifest`；可写 `reviewer_note`（≤500 字） | 本地或 PR 中更新 `evolution-candidates.json` |
| 3 | 对值得入库的 id（须已 `queued_for_manifest`）：`python3 scripts/merge_candidates_to_manifest.py …`（应急 `--force`） | 更新 `evolution-manifest.json` |
| 4 | `make validate` | 通过校验 + `analysis_engine --check` + **对账脚本** |
| 5 | `make analyze`（或 `make trends` 仅刷新趋势） | 更新 `analysis-snapshot.json`、**`data/sediment.json`**（含 `hint_closure_gaps_n` / `hint_decisions_total`）、**`assets/sediment-trends.json`**（含 `closure_backlog` 近 14 日） |
| 6 | 打开 `analysis-hub.html`（或读 `analysis-snapshot.json`） | 看热力与共现 |
| 7 | 处理 **≥1 条** `evolution_hints`（`analysis-snapshot.json` 中为对象时可点链到 `target_pages`）：**落实**或 **显式否决**；在 **`assets/evolution-hint-decisions.json`** 追加一条记录（`id`、`action`: `done` / `rejected` / `deferred`、`recorded_at` 等；**若规则在 `evolution-hint-rules.json` 中 `track_closure: true`，请填写 `rule_id`** 与提示一致，以便快照清空 `hint_closure_gaps`） | 闭环有可检索的决策痕迹；分析页与快照 `sources.hint_decisions` 可看到累计统计 |
| 8 | 打开 `lab.html`：按热力勾选因子做一轮沙盘 | 与 manifest 映射一致性感性校验 |
| 9 | `git commit` & `push` | 站点与仓库同步 |

## 与人审闸门一致

- 未经审阅 **不** merge 进 manifest。  
- 改 HTML 大段与改 manifest **可同 PR**，但须在描述里写清「对应哪条信号 / 哪条 hint」。

## 相关命令

见仓库根 [README.md](../README.md) 与 [scripts/README.md](../scripts/README.md)。

在 GitHub 上开 PR 修改 manifest/候选时，仓库已配置 [PR 模板](../.github/pull_request_template.md)，请勾选自检项。

## 对账脚本

`python3 scripts/check_manifest_drift.py`：检查 `maps_to.pages` 是否列入 **`scripts/evolution-registry.json`** 且文件存在；`lab_factors` 是否与 registry / `lab.js` 一致；并校验 ingest 配置与 `maps_to_hints`、`gen-sitemap` PRIORITY；**`evolution-hint-rules.json`** 的 `rules[].id`（唯一、非空）与 `track_closure` 类型、`target_pages` ⊆ registry。已并入 `make validate` 与 CI。

`python3 scripts/validate_evolution_hint_decisions.py`：校验 **`assets/evolution-hint-decisions.json`** 结构及 `related_pages` ⊆ registry；若填写 **`rule_id`** 则须为 **`evolution-hint-rules.json`** 中已有规则的 `id`。
