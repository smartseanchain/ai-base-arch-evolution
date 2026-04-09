# 数据与分析 · 驱动全站内容与模块更新（总览）

本文说明：**结构化数据**与**分析引擎产出**如何作用于站内「**模块**」（分页、沙盘因子、注册表页）与「**内容**」（读者可见的叙事与动态块），以及**哪些会随 JSON 自动变、哪些必须人改**。与 [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md)（偏 fetch/总线）、[TECH_ARCHITECTURE_CAPABILITIES.md](./TECH_ARCHITECTURE_CAPABILITIES.md)（偏技术栈与能力地图）互补。

<a id="terms"></a>

## 1. 用语

| 词 | 本站含义 |
|----|-----------|
| **模块** | 以**独立 HTML 页**为主的站内单元（与 [模块图谱](../modules-map.html) 五系七层、 [综合推演 §1](../synthesis.html#inventory) 模块表一致）；另含 **`lab.js` 沙盘因子**（`lab_factors`）。 |
| **内容** | **静态**：各页正文、表、图、TOC——存于 `.html`；**动态**：由 JS `fetch` JSON 写入的区块（信号栏、仪表盘、读数条、闭环摘要等）。 |
| **数据** | 以 Git 内 JSON 为真源：`evolution-manifest.json`、`evolution-candidates.json`、`evolution-hint-decisions.json`、`analysis-snapshot.json`、`sediment-trends.json` 等。 |
| **分析** | `analysis_engine.py`（当日结构）+ `sediment_trends.py`（跨日）；**不**生成 HTML 段落。 |

<a id="matrix"></a>

## 2. 更新方式总矩阵（数据 / 分析 → 内容与模块）

| 读者可见形态 | 是否随数据/分析**自动**变 | 依赖的数据或脚本 | 说明 |
|--------------|---------------------------|------------------|------|
| **各页叙事正文、§ 配方表行、静态 callout** | 否 | — | 人编辑 HTML；可与 `rule_id` / 信号 `id` 在 PR 里对账 |
| **进化信号栏（manifest + 候选）** | 是（刷新后） | `evolution-manifest.json`、`evolution-candidates.json` | `evolution.js`：闭环页、战略·舆情、沙盘页等 |
| **沙盘因子高亮** | 是 | 同上 + `maps_to.lab_factors` | `evolution.js` + `lab.js`；噪声候选不参与 |
| **分析枢纽全页仪表盘** | 是 | `analysis-snapshot.json`、`sediment-trends.json` | `analysis.js`：热力、共现、趋势、聚合解读等 |
| **全站读数条（一行摘要）** | 是 | 同上 + 可选仅快照 | `site-data-bus.js`，registry 内根目录页均已挂载（含 `legacy-all-in-one.html` 单页归档）；`analysis-hub.html` 为 `snapshot-only`，`analysis.js` 复用 `SiteDataBus` 快照缓存 |
| **进化闭环页 · 闭环摘要卡片** | 是 | 快照 + 决策等 | `closure-summary.js` |
| **站点顶栏 / skip-bar** | 否（除非跑 `sync-nav`） | `partials/*.inc.html` | 与数据管道**解耦**；增页须改 registry + partial |
| **sitemap 优先级** | 否（须跑脚本） | `gen-sitemap.py` + registry | 与 manifest `pages` 对账见 `check_manifest_drift` |

**结论**：**自动更新**主要指 **JSON 提交 + 读者刷新** 后，**动态区块**与**统计读数**对齐新数据；**模块体量与叙事深度**仍靠 **人**维护 HTML 与综合推演结构。

<a id="module-map"></a>

## 3. 模块（分页）如何被数据「挂接」

信号条目中的 **`maps_to.pages`** 将线索挂到**允许范围内的**根目录 HTML（见 **`scripts/evolution-registry.json`**）。效果包括：

1. **热力**：`analysis_engine` 按页聚合 `module_heat`，出现在 `analysis-snapshot.json` 与仪表盘。  
2. **读者动线**：分析页上的提示对象可带 `target_pages`（与规则/hint 配置一致时）。  
3. **沙盘**：`maps_to.lab_factors` 须在 registry 的 **`lab_factors`** 与 **`assets/lab.js`** 中均有定义，高亮才一致。

**新增一页「可被信号指向」的模块**时至少：

- 将页面路径加入 **`evolution-registry.json` → `pages`**，文件真实存在；  
- 需要进顶栏时改 **`partials/site-nav.inc.html`**（及 skip-bar 如需）并 `make sync-nav`；  
- 跑 **`make validate`**（对账脚本会查 registry / ingest / sitemap 等）。

详见 [ARCHITECTURE.md · 单一注册表](./ARCHITECTURE.md#fitness-functions)。

<a id="pipeline"></a>

## 4. 推荐传播链（从数据到全站感知）

```mermaid
flowchart LR
  IG[ingest] --> C[candidates]
  H[人审] --> M[manifest]
  M --> AE[analysis_engine]
  C --> AE
  D[hint-decisions] --> AE
  AE --> SN[snapshot]
  AE --> SD[sediment]
  SD --> TR[trends]
  SN --> UI1[analysis.js / site-data-bus]
  TR --> UI1
  M --> UI2[evolution.js]
  C --> UI2
  SN --> UI3[closure-summary]
```

1. **ingest** → 更新候选（或 Actions artifact / PR）。  
2. **人审** → `review_state`、`merge_candidates_to_manifest`（仅闸门内 id）。  
3. **analyze** → `make analyze` 或 **`make evolution-fast`**（须先 validate，见 [EVOLUTION_RUNBOOK](./EVOLUTION_RUNBOOK.md#accelerate)）。  
4. **validate** → **`make validate`** → **git commit & push**。  
5. 读者打开任意挂载页 → **动态内容与模块读数**与最新 JSON 一致。

<a id="checklist"></a>

## 5. 维护者速查（改数据后全站是否「对齐」）

| 若你刚做了… | 建议再检查 |
|-------------|------------|
| 新增/改了 `maps_to.pages` | `evolution-registry.json`、页面是否存在、`make validate` |
| 新增/改了 `lab_factors` | 与 `lab.js` id **集合一致**、registry `lab_factors` |
| 合并了 manifest 或大批候选 | `make analyze`（或 `evolution-fast`）+ 打开 **analysis-hub**、**lab** 看热力与高亮 |
| 写了 `evolution-hint-decisions` | 闭环页、`analysis-snapshot.sources.hint_decisions`、缺口条数 |
| 只改静态正文 | 无需跑分析；若回应某条 hint，PR 中引用 `rule_id` / 决策 `id` |

<a id="boundary"></a>

## 6. 边界（避免误解）

- **分析不会**根据热力**自动修改**综合推演 §6/§7 表或十年场景正文；是否升格为「站内核叙事」由 **§11 迭代 + 人**决定。  
- **热力偏高**仅表示「当前库内映射计数」，**不等于**政策优先级或民意强度；判据见 [DEDUCTION_STRATEGY.md](./DEDUCTION_STRATEGY.md)、[synthesis §2](../synthesis.html#criteria)。  
- **定时 CI** 默认只产 artifact；线上站点与 Git 对齐仍依赖 **合并 JSON 后 push**（根目录 README）。

<a id="read-more"></a>

## 7. 延伸阅读

| 主题 | 文档 / 页面 |
|------|-------------|
| fetch 总线与占位扩展 | [SITE_DATA_UPDATE_FRAMEWORK.md](./SITE_DATA_UPDATE_FRAMEWORK.md) |
| 技术栈与能力清单 | [TECH_ARCHITECTURE_CAPABILITIES.md](./TECH_ARCHITECTURE_CAPABILITIES.md) |
| 数据流与七类模块 | [ARCHITECTURE.md](./ARCHITECTURE.md) |
| 双周节奏与命令 | [EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md) |
| 五系七层与分页导航 | [modules-map.html](../modules-map.html)、[synthesis §1](../synthesis.html#inventory) |
| 方法与字段总线 | [analysis-hub.html#panorama](../analysis-hub.html#panorama) |
| 全站梳理后如何重新推演并决定更新落点 | [SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md](./SITE_WIDE_RERUN_DEDUCTION_PLAYBOOK.md) |
