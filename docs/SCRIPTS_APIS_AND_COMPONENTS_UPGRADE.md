# 脚本、只读 API 与组件化：替换边界与升级建议

**角色判型**（读者 / 贡献 / 数据 / 部署 → 第一站）：根 [README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](./ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](./ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad)。

**本文定位**：回答「**部分脚本能否换成 API 或组件**」——在**不削弱 Git 真源、`make validate` 闸门与人审 manifest** 的前提下，给出**整体分类、可替换边界与推荐升级顺序**。

**不替代**命令表与管道细节：**[scripts/README.md](../scripts/README.md)**、**[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)**、**[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**。**按阶段执行**仍以 **[PHASED_UPGRADE_EXECUTION_GUIDE.md](./PHASED_UPGRADE_EXECUTION_GUIDE.md)** 为准。**五维总图 · 主链联动 · 仓库物理分层**：**[勿混粒度 · 五维/六域/七类](./PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1a](./PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation) · **[§1b](./PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**。**整体内容框架**：**[docs/README · #content-framework](./README.md#content-framework)** · **前后台模块一页表**：[**#front-back-modules**](./README.md#front-back-modules) · **组件×功能一条表**：[**#system-components-fusion**](./README.md#system-components-fusion)。**按改动判型**（**0c**）：**[docs/README · #quick-paths](./README.md#quick-paths)**。**自动化助手（validate 真源 · 人审 manifest）**：[AGENTS.md · 契约速览](../AGENTS.md#agents-contract) · [人审闸门](../AGENTS.md#agents-invariants) · [合并前](../AGENTS.md#agents-pre-merge)。**呈现双轨（`spa-sync` / `spa-build`）**：[MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [关系视图](../maintainer-hub.html#mh-spine-map)。**MPA 顶栏与失页**：**`partials/`** → **`make sync-nav`**；**`404.html`** 手调（`sync_site_nav` 不写回）— **[scripts/README · `sync_site_nav`](../scripts/README.md)**。

---

## 1. 结论摘要（维护者决策用）

| 判断 | 建议 |
|------|------|
| **对外/边缘系统只要「读已发布 JSON」** | **扩展只读 HTTP API**（`GET` + **ETag/304**），逻辑复用 **`evolution_pkg.ops.http_cache`**；**不**为每个 JSON 单独造新服务。 |
| **可复用的校验、对账、解析、写盘算法** | **收进 `evolution_pkg.*`**；根目录 **`scripts/*.py`** 保持**薄 CLI**（`python3 scripts/foo.py` 或 `python -m`）。 |
| **合并闸门、PR 与 CI 必须一致** | **保留** **`run_validate.sh`** 及其中 **`validate_*` / `check_*` / `sync_site_nav --check`** 等**可本地复现**入口；**勿**用「仅远端才有的 HTTP 校验」替代合并真源。 |
| **有副作用的长作业**（分析写盘、ingest、趋势） | **不宜**做成匿名公网 API；应保留为 **CLI + 定时/编排调用**（GitHub Actions、未来 **Prefect/Dagster** 封装**同一 argv**）。 |
| **人审合并 manifest** | **不**改为对外 **POST** 自动写 **`evolution-manifest.json`**；管理端若提供 UI，仍走 **[AGENTS.md](../AGENTS.md#agents-invariants)** / **[CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd)** 所述人审与 PR 节奏（见 **[ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md)**）。 |

**一句话**：**阅读面**优先 **API 化**；**闸门与写盘**优先 **包化 + 脚本/编排调用**，而不是「用公网 CRUD 替代仓库工具链」。

---

## 2. 当前形态（已做的「组件化」）

| 层 | 载体 | 作用 |
|----|------|------|
| **库组件** | **`evolution_pkg`**（`io`、`pipeline.runner`、`spa_nav`、`sediment_validate`、`ops.http_cache` 等） | 供脚本、API、单测 **import**；六域归属见 **[INTELLIGENCE_SIX_DOMAINS.md · 代码映射](./INTELLIGENCE_SIX_DOMAINS.md#code-mapping)**。 |
| **只读 API** | **`scripts/readonly_api.py`**（FastAPI） | **`GET`** 暴露快照、趋势、manifest、site-meta、快照历史等；**不写盘**、**不改 manifest**。 |
| **闸门入口** | **`run_validate.sh`**、`make validate` / **`make phase-1`** | 与 pre-commit、CI **validate** **同源**；含 compileall、JSON 校验、对账、顶栏、单测、`analysis_engine --check`、Schema 等。**子集**：**`run_validate_fast.sh`** / **`make validate-fast`** 仅本地迭代，**不**入 CI/pre-commit（**[ARCHITECTURE#run-validate-gate](./ARCHITECTURE.md#run-validate-gate)**）。 |
| **分析管道** | **`run_pipeline_steps.py`** → **`evolution_pkg.pipeline.runner`** | **analyze** / **fast** 步骤表；与 validate **前半段对齐关系**见 runner 模块说明。 |

---

## 3. 不建议用「公网 API」替换的脚本族

下列能力若改成**匿名可调用 HTTP**，易引入**非确定性、滥用、与 PR 脱节**；应继续以 **CLI + CI/编排** 为主。

| 族 | 典型脚本 | 原因 |
|----|----------|------|
| **闸门与对账** | `validate-evolution-*.py`、`validate_*_schema.py`、`check_manifest_drift.py`、`check_nav_links_registry.py`、`sync_site_nav.py --check`、`check_skip_bar_404.py` | 合并真源须与 **本地/CI 同一命令**；远端-only 校验会形成第二套真相。 |
| **分析写盘** | `analysis_engine.py`（含 `--sediment`）、`sediment_trends.py` | CPU/IO 与**写 JSON** 副作用；公网 POST 难做配额与审计对齐 Git。 |
| **抓取入池** | `ingest_opinion_law.py`、`run_ingest_only.sh`（**`ingest_config.json`** 含可选 **`json_feeds`**：HTTPS JSON 侧车/API） | 外网依赖、频率与合规；适合 **定时 job / 内网 worker**，而非开放 HTTP。频率与 UA 约定见 **[INTEL · §2—2a](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b](./INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**。 |
| **人审合并** | **`python3 -m evolution_pkg.candidate_merge`**（**`main()`** 在包内）· **`merge_candidates_to_manifest.py`**（薄壳） | **人审**与 **PR diff** 是产品边界；API 自动合并违反 **[AGENTS.md](../AGENTS.md#agents-invariants)** 闸门表述。 |
| **站点生成/同步** | `sync_site_nav.py`（写回各页，**跳过 `404.html`**）、`gen_nav_links_ts.py`、`sync_spa_public.py`、`gen-sitemap.py` | 修改**仓库内** HTML/TS/产物；属**开发者工作流**，不是站点读者 API；**404** 顶栏/skip 与 **`check_skip_bar_404`** 见 [MERGE · §1](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](./MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)。 |

**若未来管理端要「点按钮触发」**：可做**内网、鉴权后的「触发器」**（例如仅内网队列 + worker 仍执行同一 CLI），默认仍**不**自动 merge manifest；见 **[ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md)**。

---

## 4. 适合扩展为只读 API 的 JSON（优先 GET）

下列文件**已是 Git 真源的一部分**，与现有 **`/snapshot`、`/trends`、`/manifest`** 同类；缺什么就加 **GET**：**磁盘 JSON** 优先在 **`evolution_pkg.readonly_disk_routes`** · **`READONLY_DISK_JSON_ROUTES`** 增行并由 **`readonly_api`** 注册，并复用 **`prepare_revalidated_json`**（见 **[INTEGRATION · 扩展只读路由](./INTEGRATION_AND_READONLY_API.md#extend-readonly-routes)**）。**路由 ↔ 路径 ↔ 敏感性**总表见 **[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)**。**注册表**已实现 **`GET /registry`**；**沉淀**已实现 **`GET /sediment`**（**`data/sediment.json`**，无文件时 **404**）；**候选池**已实现 **`GET /candidates`**（**敏感**，须网关侧控制暴露面）；**hint 人审决策**已实现 **`GET /hint-decisions`**（**宜内网或受控暴露**）；**hint 规则**已实现 **`GET /hint-rules`**（**`scripts/evolution-hint-rules.json`**）；**ingest 映射**已实现 **`GET /maps-to-hints`**（**`scripts/maps_to_hints.json`**）；**ingest 配方**已实现 **`GET /ingest-config`**（**`scripts/ingest_config.json`**，**含 RSS URL**）。

| 数据 | 路径（仓库内） | 备注 |
|------|----------------|------|
| **注册表** | `scripts/evolution-registry.json` | SPA/运维仪表盘常需；**无敏感默认**。**只读 HTTP**：**`GET /registry`**（与 **`readonly_api`** 其余磁盘 JSON 路由同为 **ETag + 304**）。 |
| **沉淀** | `data/sediment.json` | **只读 HTTP**：**`GET /sediment`**；部署须能读到该路径（未跑过分析则无文件 → **404**）。 |
| **候选池** | `assets/evolution-candidates.json` | **可能含未审线索**。**只读 HTTP**：**`GET /candidates`**（**须在网关限制访问**；见 **[INTEGRATION](./INTEGRATION_AND_READONLY_API.md)**）。 |
| **hint 人审决策** | `assets/evolution-hint-decisions.json` | **只读 HTTP**：**`GET /hint-decisions`**（含 **`rule_id`** 等；**宜内网或受控暴露**；见 **[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)**）。 |
| **hint 规则** | `scripts/evolution-hint-rules.json` | **只读 HTTP**：**`GET /hint-rules`**（分析提示规则；见 **[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)**）。 |
| **ingest 映射** | `scripts/maps_to_hints.json` | **只读 HTTP**：**`GET /maps-to-hints`**（host/关键词 → `maps_to`；见 **[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)**）。 |
| **ingest 配方** | `scripts/ingest_config.json` | **只读 HTTP**：**`GET /ingest-config`**（RSS 与 ``routes``；**宜受控暴露**；见 **[DATA_CONTRACTS · §8.1](./DATA_CONTRACTS.md#readonly-api-routes)**）。 |

每增一路由：**磁盘表** **`evolution_pkg.readonly_disk_routes`**（若适用）+ **OpenAPI** + **`test_readonly*.py`**（**`test_readonly_api`**、**`test_readonly_disk_routes`**、**`test_readonly_proxy_segment_sync`**）+ **`READONLY_PROXY_SEGMENTS`** + **DATA_CONTRACTS / INTEGRATION** 一句说明。

---

## 5. 「替换脚本」的推荐升级路径（工程顺序）

1. **先包化**：把共享逻辑迁入 **`evolution_pkg`**，脚本只解析参数并调用包内函数（与 **[MODULE_INVENTORY · §2](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md#evolution-pkg)** 一致）。  
2. **再只读 API 化**：对**稳定、已提交**的 JSON 增加 **GET**；**不**把 validate 链整体改成「调远程服务才算绿」。  
3. **长作业**：继续 **`make analyze` / `make evolution-fast` / ingest shell**；阶段 2 引入编排器时 **只换调度层**，**不换**步骤语义（见 **[ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)**）。  
4. **第二套 validate**：**禁止**（与 **[repo-gates](../.cursor/rules/repo-gates.mdc)**、**[run_validate.sh](../scripts/run_validate.sh)** 文首注释一致）。  

单测层面：入口 shell 与 **`pipeline.runner` 步骤表** 引用的 **`scripts/*.py`** 已由 **`test_run_validate_script_refs`**、**`test_pipeline_runner_script_refs`** 兜底（见 **[PHASED · 阶段 1](./PHASED_UPGRADE_EXECUTION_GUIDE.md#phase-1)**）。

---

## 6. 与阶段 0—3 / 2.5 的对应关系

| 阶段 | 与「API / 组件」相关的典型动作 |
|------|--------------------------------|
| **0—1** | 扩展 **`evolution_pkg`**；扩展 **只读 GET**；加固 **Schema + validate**；**不**上公网写接口。 |
| **2** | 编排器 **调用现有 Python/ shell**；API 仍**可选**且以只读为主。 |
| **3** | 事件 **通知**订阅方；**Git** 仍为契约与审计主链。 |
| **2.5** | OLTP/缓存/读副本服务化的是**运营态与投影**，**不**替代 registry/manifest 的 Git 闸门（**[DATA_STORES](./DATA_STORES_AND_FUTURE_DB_ARCHITECTURE.md)**）。 |

---

## 7. 延伸阅读

- **平台总表与三条黄金路径**：[PLATFORM_MASTER_MAP_AND_INVOCATION.md](./PLATFORM_MASTER_MAP_AND_INVOCATION.md)  
- **只读 API 契约与扩展方式**：[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)  
- **扩展插槽与新增能力检查单**：[PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)  
- **管理端与审核 UX（不替代 manifest 人审）**：[ADMIN_WEB_CONSOLE_ROADMAP.md](./ADMIN_WEB_CONSOLE_ROADMAP.md) · [ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)（管道 UI / 数据源 / 沉淀链）  
- **模块 × 脚本簇 × 升级矩阵**：[MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](./MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md)  
- **可落地改造全景**：[ARCHITECTURE_UPGRADE_ROADMAP.md](./ARCHITECTURE_UPGRADE_ROADMAP.md)

---

*新增对外只读路由或调整「脚本 vs API」边界时，请同步本文与 **INTEGRATION** / **DATA_CONTRACTS**，并跑通 **`make validate`**（或 **`make merge-ready`**）。*
