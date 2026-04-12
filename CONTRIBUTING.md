# 参与贡献

欢迎提交 PR。**合并前须本地通过 `make validate`**（与 CI **`validate` job、pre-commit 一致）。推荐再执行 **`make merge-ready`**（= **`validate`** + **`test-readonly-api`** + **`test-admin-console`**）— 动线见 **[docs/MERGE_AND_RELEASE_CHECKLIST.md](docs/MERGE_AND_RELEASE_CHECKLIST.md)**。全文档**整理主线**（维护者按序扫读）：**[docs/README.md · 文档主线](docs/README.md#docs-spine)**。以下为最小必读路径，细节见链接文档。

**Fork 本仓库**：`.github/ISSUE_TEMPLATE/pipeline-triage.md` 文首的 CONTRIBUTING 链接指向**上游默认远程**；若需指向你的 Fork，请把该 URL 改成你的仓库地址（或改为相对路径 `../../CONTRIBUTING.md`）。**`.github/ISSUE_TEMPLATE/config.yml`** 中 **`contact_links`** 的文档 URL 同理，请改为本仓库 **`blob/main/docs/...`**。

**Cursor / 自动化助手**：**[AGENTS.md](AGENTS.md)**；**`.cursor/rules/repo-gates.mdc`**（始终）；改 **`spa/src/**`** 时 **`.cursor/rules/spa-nav-registry.mdc`**。**技术 / 内容 / 推演** 三架构速览：**[ARCHITECTURE_ONE_PAGER · 三架构对照](docs/ARCHITECTURE_ONE_PAGER.md#three-architectures)**。**按阶段升级**（阶段 0→1→2/3、正交 2.5 数据层、验收与迭代模板）：**[PHASED_UPGRADE_EXECUTION_GUIDE](docs/PHASED_UPGRADE_EXECUTION_GUIDE.md)**。**增量开发**（提前接组件、边调试边补、**[PR 切片模板](docs/templates/incremental-pr-slice.md)**）：**[INCREMENTAL_BUILD_PLAYBOOK](docs/INCREMENTAL_BUILD_PLAYBOOK.md)**。

## 环境与命令

- **Python 3.12+**（与 CI 一致）：`python3 -m pip install -r requirements.txt`
- **常用 Make 目标**：`make help`（首行指向本文）
- **合并前**：`make validate`（**`make phase-1`** 与其同源；含 **registry** JSON Schema、JSON 对账、nav.config↔navLinks、顶栏、单测、`analysis_engine --check`、快照与沉淀/趋势 Schema）。仅跑子集可用 **`make test`**（**registry** JSON Schema + 单测 + navLinks + 沉淀/趋势 Schema + 可选 **ai-analysis-overlay** Schema）。
- **合并前推荐**：**`make merge-ready`**（**`make validate`** → **`make test-readonly-api`** → **`make test-admin-console`**）。一页动线见 **[docs/MERGE_AND_RELEASE_CHECKLIST.md](docs/MERGE_AND_RELEASE_CHECKLIST.md)**。
- **只读 API 单测**：CI **`validate`** 已装 **`requirements-api.txt`**，**`test_readonly*.py`**（**`test_readonly_api`**、**`test_readonly_proxy_segment_sync`**）必跑；本地仅 **`requirements.txt`** 时该类会在 **`make validate`** 中 **skip**，需对齐请执行 **`make test-readonly-api`**（已含于 **`make merge-ready`**）。**管理端烟测**：**`make test-admin-console`**（变更 **`admin-console/**`** 时 CI 另跑 **`admin-console-tests`**；**`make merge-ready`** 亦包含）。
- **SPA / Node**：**Node 18+**。**`make merge-ready` 不含 `make spa-build`**；若 PR 将触发 CI **`spa-build`**（路径条件见 **[docs/README 文首](docs/README.md)**），合并前须再 **`make spa-build`**。仅改根 **`index.html`** 读站等、需更新壳内 iframe 时，再 **`make spa-sync`**（**[spa/README.md](spa/README.md)**）。**可选分析栈**：`requirements-analytics.txt`（[DATA_CONTRACTS.md](docs/DATA_CONTRACTS.md)）；API 依赖见上文 **只读 API**。

<a id="contributing-terminology"></a>

## 架构术语与契约纪律（PR 描述建议写清）

避免把不同「版本线」与职责混在一句话里：

| 说法 | 指什么 | 典型字段 / 文件 |
|------|--------|-----------------|
| **分析运行** | 某次 `analysis_engine` / 流水线算快照 | `analysis-snapshot.json` · **`run.run_id`**、**`run.repo_revision`** |
| **站点发布线** | 人为宣告的展示里程碑（与分析跑次无关） | **`assets/site-meta.json`** · **`site_version`** |
| **分析 / 快照** | 热力、共现、提示、闭环缺口等结构化产出 | **`analysis-snapshot.json`**（引擎**不写** HTML） |
| **内容生成** | 读者看到的叙事与版式 | 根目录 **`.html`**、人写为主 |

**契约先行**：若改 **快照**、**沉淀** 或 **趋势** JSON 的语义结构，须**先**更新对应 **`docs/schemas/*.schema.json`** 与校验脚本，再改 **`analysis_engine`** 或消费方（与下表「常见变更自检」一致）。

## CI 与分支保护

- **`ci.yml` · validate**：始终运行，**以根目录 MPA 为默认真源**；安装 **`requirements.txt` + `requirements-api.txt`**，**`test_readonly*.py`**（ETag / 304 + 代理白名单对账）不再跳过。
- **`ci.yml` · spa-build**：仅当变更触及 `spa/`、**`scripts/evolution-registry.json`**、**`docs/schemas/evolution-registry.schema.json`**、**`scripts/validate_evolution_registry_schema.py`**、sync 相关路径等时才运行，否则 **skipped** 属正常。
- 建议分支保护**只必选 `validate`**；双轨说明见 **[docs/README.md 文首](docs/README.md)**。

## 常见变更自检

| 你在改什么 | 至少要做 |
|------------|----------|
| 根目录新分页 / `maps_to.pages` | 更新 **`scripts/evolution-registry.json`**（须符合 [**`docs/schemas/evolution-registry.schema.json`**](docs/schemas/evolution-registry.schema.json)）；顶栏只改 **`partials/`** 后 **`make sync-nav`** |
| 沙盘因子 | registry **`lab_factors`** 与 **`assets/lab.js`** 中 `id` 集合一致 |
| 维护 **SPA** | 编辑 **`spa/nav.config.json`**（顺序/文案）后 **`make gen-nav-links`**；**`spa/src/navLinks.ts` 勿手改**；**`make test`** / **`make validate`** 跑 **`check_nav_links_registry.py`** |
| 改 **`admin-console/`**（管理端脚手架） | **`make validate`**（**`compileall admin-console/app`**）+ **`make test-admin-console`**；Compose 见 **`docs/DOCKER.md#profile-admin`**；CI 在变更触及 **`admin-console/**`** 时跑 **`admin-console-tests`** |
| 新增 **`evolution_pkg`** 顶层子模块（`.py` 或子包） | 在 **`scripts/evolution_pkg/domains.py`** · **`SUBMODULE_DOMAIN`** 登记**主归属域**（六域协同）；**`make test`** 校验目录与映射一致 |
| 改 **沉淀/趋势** 结构 | 同步 **`docs/schemas/sediment*.schema.json`**；**`make test`** / **`make validate`** 含 **`validate_sediment_artifacts_schema.py`**（实现 **`evolution_pkg.sediment_validate`**） |
| 快照结构 | 递增 **`schema_version`**，并改 **`docs/schemas/analysis-snapshot.schema.json`** 与校验脚本 |
| **manifest** | 仅 **`review_state=queued_for_manifest`** 可合并；勿绕过人审闸门 |
| 带 **`nexus-legend`** 的枢纽页 | 三色 **CSS 类可复用**，**中文标签按页定义**（类名≠全站同一套三字文案），见 [ARCHITECTURE.md · 三色标签](docs/ARCHITECTURE.md#nexus-tag-labels) |

完整检查单：[PLATFORM_CAPABILITY_MAP.md §6](docs/PLATFORM_CAPABILITY_MAP.md#enhance-checklist) · 扩展性与进化 [§8](docs/PLATFORM_CAPABILITY_MAP.md#extensibility) · [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) · [MERGE_AND_RELEASE_CHECKLIST.md](docs/MERGE_AND_RELEASE_CHECKLIST.md) · 只读 API 集成 [INTEGRATION_AND_READONLY_API.md](docs/INTEGRATION_AND_READONLY_API.md)。

**读者路径与发布复查（摘要）**：顶栏链与注册表一致，新人可先记 **五枢纽**（总览 → 立体联结或模块图谱 → 综合推演 → 分析引擎 → 沙盘），见 [index.html · 读站指路](index.html#read-guide)。站内 **`docs/*.md`** 在 **GitHub Pages 根部署**下多为原文/下载，与网页渲染不同，见 [PLATFORM · §7](docs/PLATFORM_CAPABILITY_MAP.md#reader-and-release) 与 [SITE_REVIEW · 四角色复查](docs/SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)。**大版本或改顶栏/总线后**建议在 **`make validate`** 之外过一遍该节中的 **发布前轻量清单**。

## 阅读顺序（维护者）

与 **[docs/README.md · 文档主线（表）](docs/README.md#docs-spine)** 同序；**读者面/管理面一页**（与闸门、脚本对读）见 **[PLATFORM_MASTER_MAP · 节 1a](docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)**。若只读最短链，可按下列序号：

1. [MERGE_AND_RELEASE_CHECKLIST.md](docs/MERGE_AND_RELEASE_CHECKLIST.md)（合并/发布一页）· [ARCHITECTURE_ONE_PAGER.md](docs/ARCHITECTURE_ONE_PAGER.md)（**[三架构对照](docs/ARCHITECTURE_ONE_PAGER.md#three-architectures)**）· [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)（技术栈整理 + 升级路径简版）  
2. [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)（插槽、进化轨、**[智能化与自动化边界](docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)**）· [PLATFORM_CAPABILITY_MAP.md §8](docs/PLATFORM_CAPABILITY_MAP.md#extensibility) · [USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](docs/USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)（用户端/管理端 · 数据源 · 审核；**[节 1a · 前端读者 · 后端管理](docs/USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)**）  
3. [ARCHITECTURE.md](docs/ARCHITECTURE.md)（数据流、适应度函数、七类模块）· [DATA_CONTRACTS.md](docs/DATA_CONTRACTS.md) · [schemas/README.md](docs/schemas/README.md)  
4. [PLATFORM_CAPABILITY_MAP.md](docs/PLATFORM_CAPABILITY_MAP.md)（四条支柱、MPA/SPA、**[阅读顺序 §5](docs/PLATFORM_CAPABILITY_MAP.md#reading-order)**）  
5. [scripts/README.md](scripts/README.md)（命令表）· [EVOLUTION_RUNBOOK.md](docs/EVOLUTION_RUNBOOK.md) · [SITE_DATA_UPDATE_FRAMEWORK.md](docs/SITE_DATA_UPDATE_FRAMEWORK.md)  
6. 全站 **页头 `lead` / `read-hint` 分层**：[SITE_REVIEW_THREE_PASSES.md](docs/SITE_REVIEW_THREE_PASSES.md) · §3.5 · **深链与本轮提要** §3.6 · **[四角色复查](docs/SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)**  
7. 分阶段升级：**[PHASED_UPGRADE_EXECUTION_GUIDE.md](docs/PHASED_UPGRADE_EXECUTION_GUIDE.md)**（按阶段执行）· [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](docs/ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) · 可落地全景：[ARCHITECTURE_UPGRADE_ROADMAP.md](docs/ARCHITECTURE_UPGRADE_ROADMAP.md) · 模块对表：[MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](docs/MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md) · 编排/事件流：[ORCHESTRATION_AND_EVENT_STREAMING.md](docs/ORCHESTRATION_AND_EVENT_STREAMING.md)  
8. 只读 API 集成：[INTEGRATION_AND_READONLY_API.md](docs/INTEGRATION_AND_READONLY_API.md) · 内容草稿插槽：[scripts/draft/README.md](scripts/draft/README.md)

**改 SPA 壳**（`spa/src/SpaLayout.tsx`、`spaRouteMeta.ts`、`LegacyFrame.tsx`）时：快捷链顺序须与 **`partials/skip-bar.inc.html`** 一致；总览 **`#read-guide`** / **`#three-questions`** / **`#hub-catalog`** 的 **`document.title`·读屏** 与 **iframe `title`** 须在 **`spaRouteMeta`** 与 **`LegacyFrame`** 中成对更新（见 **AGENTS.md** 双轨条）。

PR 请使用模板 **[`.github/pull_request_template.md`](.github/pull_request_template.md)**。

**校验或 Actions 仍失败**：新建 Issue 可选用 **[流水线 / 校验失败排查](.github/ISSUE_TEMPLATE/pipeline-triage.md)**（模板文首链回本文，便于对照 **validate** / **spa-build**）。
