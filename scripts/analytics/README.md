# 分析侧车 · 只读 SQL 示例（DuckDB）

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../../README.md#pm-four-journeys) · [README · 从这里开始](../../README.md#readme-start-here) · [README · 双轨真源](../../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](../../docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship)。

与 **`scripts/query_evolution_duckdb.py`**、**`requirements-analytics.txt`** 对读；**权威数据**仍以 Git 内 **`assets/*.json`** / **`data/sediment.json`** 为准，本目录仅为**复盘查询**样板。**整体内容框架** / **前后台** / **组件×主链**：[docs/README · #content-framework](../../docs/README.md#content-framework) · [#front-back-modules](../../docs/README.md#front-back-modules) · [#system-components-fusion](../../docs/README.md#system-components-fusion)。**判型**（**0c**）：[docs/README · #quick-paths](../../docs/README.md#quick-paths)。**呈现双轨（`spa-sync` / `spa-build`）**：[MERGE · §1](../../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](../../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../../maintainer-hub.html#mh-spine-map)。

## 用法

```bash
pip install -r requirements-analytics.txt
python3 scripts/query_evolution_duckdb.py < scripts/analytics/example_snapshot_runs.sql
```

或交互：`python3 scripts/query_evolution_duckdb.py` 后粘贴 SQL。

## 文件

| 文件 | 说明 |
|------|------|
| [example_snapshot_runs.sql](example_snapshot_runs.sql) | 从侧车表 **`analysis_snapshot_history`** 列最近 **`run_id`**（需已有 **`data/evolution.db`**） |
