# 参与贡献

**产品与角色动线**：读者 / 贡献者 / 数据管道 / 部署四条入口与「第一站」见根目录 **[README · 产品视角](README.md#pm-four-journeys)** · **[README · 从这里开始](README.md#readme-start-here)**（约 15 分钟自检）· **[README · 双轨真源](README.md#readme-dual-track-map)**。**架构师梳理与持续改进**：[ARCHITECTURE_ONE_PAGER · 五步表](docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [PR 证据三联](CONTRIBUTING.md#contributing-pr-evidence-triad)。本文以下聚焦 **贡献者** 开 PR 时的闸门、命令与自检。

欢迎提交 PR。**合并前须本地通过 `make validate`**（与 CI **`validate` job、pre-commit 一致）。推荐再执行 **`make merge-ready`**（= **`validate`** + **`test-readonly-api`** + **`test-admin-console`**）— 动线见 **[docs/MERGE_AND_RELEASE_CHECKLIST.md · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**。**整体内容框架**（叙事 / JSON / `docs` / 闸门 / 双轨 / 管理面）：**[docs/README · #content-framework](docs/README.md#content-framework)**。全文档**整理主线**（维护者按序扫读）：**[docs/README.md · 文档主线](docs/README.md#docs-spine)**。**读者面 × 管理面按模块对表**：[docs/README · #front-back-modules](docs/README.md#front-back-modules) · **可执行单元 × 主链（组件—功能）**：[docs/README · #system-components-fusion](docs/README.md#system-components-fusion)。**按改动判型**：**[docs/README · 常见改动最短链](docs/README.md#quick-paths)**（主线表 **0c**；**ingest · 管理端 · SPA** 合一判型见该表「情报 ingest · 管理控制台 · SPA 壳」行）。**技术栈多篇怎么读**（简版 vs 详版 + 附录）：**[docs/README · #tech-stack-read-merge](docs/README.md#tech-stack-read-merge)**。**维护者 MPA 枢纽**：[维护导读](maintainer-hub.html) · [关系视图](maintainer-hub.html#mh-spine-map)（本页 ↔ 注册表 ↔ 文档锚点）· [系统边界速查](maintainer-hub.html#mh-boundaries)（真源 / 生成物 / 侧车 / 闸门 / 手调例外） · [衔接矩阵](maintainer-hub.html#mh-reader-admin-matrix)。**全站顶栏与失页**：改 **`partials/site-nav.inc.html`** / **`partials/skip-bar.inc.html`** → **`make sync-nav`**；**`404.html`** 顶栏/skip **不在** **`sync_site_nav`** 写回范围，须**手调** — **[MERGE · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[scripts/README · #sync-site-nav-source](scripts/README.md#sync-site-nav-source)**（`sync_site_nav` / **`make sync-nav`**）。以下为最小必读路径，细节见链接文档。

**Fork 本仓库**：`.github/ISSUE_TEMPLATE/pipeline-triage.md` 文首的 CONTRIBUTING 链接指向**上游默认远程**；若需指向你的 Fork，请把该 URL 改成你的仓库地址（或改为相对路径 `../../CONTRIBUTING.md`）。**`.github/ISSUE_TEMPLATE/config.yml`** 中 **`contact_links`** 的文档 URL 同理，请改为本仓库 **`blob/main/docs/...`**。

**Cursor / 自动化助手**：**[AGENTS.md](AGENTS.md#agents-contract)**（[框架判型](AGENTS.md#agents-content-framework) · [架构师梳理](AGENTS.md#agents-architect-stewardship) · [深读索引](AGENTS.md#agents-deep-read) · [Cursor 规则](AGENTS.md#agents-cursor-rules)）；**`.cursor/rules/repo-gates.mdc`**（始终；判型含 **[README · 从这里开始](README.md#readme-start-here)** · **[README · 双轨真源](README.md#readme-dual-track-map)**）；改 **`spa/nav.config.json`** 时 **`.cursor/rules/spa-nav-config.mdc`**；改 **`spa/src/**`** 时 **`.cursor/rules/spa-nav-registry.mdc`**；改 **`scripts/evolution-registry.json`** 时 **`.cursor/rules/evolution-registry.mdc`**（子规则文首判型链与 **repo-gates** 同构）。**技术 / 内容 / 推演** 三架构速览：**[ARCHITECTURE_ONE_PAGER · 三架构对照](docs/ARCHITECTURE_ONE_PAGER.md#three-architectures)**。**按阶段升级**（阶段 0→1→2/3、正交 2.5 数据层、验收与迭代模板）：**[PHASED_UPGRADE_EXECUTION_GUIDE](docs/PHASED_UPGRADE_EXECUTION_GUIDE.md)**。**增量开发**（提前接组件、边调试边补、**[PR 切片模板](docs/templates/incremental-pr-slice.md)**）：**[INCREMENTAL_BUILD_PLAYBOOK](docs/INCREMENTAL_BUILD_PLAYBOOK.md)**。

**整体架构三对照**（同一仓库、不同粒度，详见 **[勿混粒度 · 五维/六域/七类](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)**）：**[五维总图 · PROJECT](docs/PROJECT_ARCHITECTURE_OVERVIEW.md)**（**[§1a](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)** · **[§1b](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**）→ **六域** [INTELLIGENCE](docs/INTELLIGENCE_SIX_DOMAINS.md) → **七类** [ARCHITECTURE](docs/ARCHITECTURE.md#seven-layers)。

**内容驱动**（数据/分析 → 模块与叙事边界 → 总线登记 vs 纯版式）：与 **[docs/README · #content-driven-chain](docs/README.md#content-driven-chain)** 同序；专篇 **[DATA_ANALYSIS_SITE_CONTENT_SYNC](docs/DATA_ANALYSIS_SITE_CONTENT_SYNC.md)** · **[SITE_DATA_UPDATE_FRAMEWORK](docs/SITE_DATA_UPDATE_FRAMEWORK.md)** · **[INTELLIGENCE · §2.2](docs/INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**。

**AI 与「自动进化」**（契约内：解读层、ingest 黄金集、草稿插槽、管道 artifact；**非**自动写 manifest）：**[docs/README · #ai-assisted-evolution](docs/README.md#ai-assisted-evolution)** · **[INTELLIGENCE · §8](docs/INTELLIGENCE_SIX_DOMAINS.md#ai-era-alignment)**。

<a id="contributing-env-and-cmd"></a>

## 环境与命令

- **Python 3.12+**（与 CI 一致）：`python3 -m pip install -r requirements.txt`
- **常用 Make 目标**：**`make help`**（含 **维护导读** `maintainer-hub.html`、**关系视图** `#mh-spine-map`、**系统边界** `#mh-boundaries`、**衔接矩阵** `#mh-reader-admin-matrix`、**MERGE §1** `docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge`、**partials 手顺** `docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence` 等收束行；首段亦指向本文）
- **合并前**：`make validate`（**`make phase-1`** 与其同源；含 **registry** JSON Schema、JSON 对账、nav.config↔navLinks、顶栏、单测、**`analysis_engine --check`**（等价 **`PYTHONPATH=scripts python3 -m evolution_pkg.analysis_pipeline --check`**）、快照与沉淀/趋势 Schema）。仅跑子集可用 **`make test`**（**registry** JSON Schema + 单测 + navLinks + 沉淀/趋势 Schema + 可选 **ai-analysis-overlay** / **ai-overlay-step** Schema）。
- **本地迭代（非合并替代）**：**`make validate-fast`**（**`scripts/run_validate_fast.sh`**）跳过部分闸门以省时间（**已含** **`validate_ai_overlay_step_schema`** / **`validate_ai_analysis_overlay_schema`**，与全量同源）；**GitHub Actions** 与 **`.githooks/pre-commit`** 只跑 **`run_validate.sh`** / **`make validate`**，**不跑** **`validate-fast`**。**合并 PR 前仍须** **`make validate`**。若 **`make validate`** 提示跳过旧格式 **`pipeline-metrics`**，可先 **`make clean-pipeline-metrics-dry-run`** 再 **`make clean-pipeline-metrics`** 后重跑 **`make analyze`**；overlay 侧车产物可 **`make clean-overlay-artifacts`**。
- **Git 钩子（可选）**：仓库根 **`bash scripts/install-git-hooks.sh`** → **`git config core.hooksPath .githooks`**（钩子读仓库内 **`.githooks/`**，随 **`git pull`** 更新）；**`pre-commit`** 等同 **`make validate`**，**不跑** **`spa-build` / `spa-sync`**。改根 **`*.html`** 或 **`docs/`** 且维护 **SPA** 时须另行执行（见下 **SPA / Node** 条 · **[MERGE · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[关系视图](maintainer-hub.html#mh-spine-map)** · **[系统边界](maintainer-hub.html#mh-boundaries)** · **[衔接矩阵](maintainer-hub.html#mh-reader-admin-matrix)**）。
- **可选**：在 **venv** 或 **`pip install --user`** 可用环境下，仓库根 **`pip install -e .`** 安装 **`evolution-site-pipeline`** 后，可用 **`evolution-ingest` / `evolution-analyze` / `evolution-merge`**（见 **`pyproject.toml`** + **`setup.py`**），与 **`PYTHONPATH=scripts python3 -m evolution_pkg.…`** 等价；系统 Python 无写权限时请用虚拟环境。
- **合并前推荐**：**`make merge-ready`**（**`make validate`** → **`make test-readonly-api`** → **`make test-admin-console`**）。一页动线见 **[docs/MERGE_AND_RELEASE_CHECKLIST.md · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**。
- **只读 API 单测**：CI **`validate`** 已装 **`requirements-api.txt`**，**`test_readonly*.py`**（**`test_readonly_api`**、**`test_readonly_proxy_segment_sync`**）必跑；本地仅 **`requirements.txt`** 时该类会在 **`make validate`** 中 **skip**，需对齐请执行 **`make test-readonly-api`**（已含于 **`make merge-ready`**）。**管理端烟测**：**`make test-admin-console`**（变更 **`admin-console/**`** 时 CI 另跑 **`admin-console-tests`**；**`make merge-ready`** 亦包含）。
- **SPA / Node**：**Node 18+**。**`make merge-ready` 不含 `make spa-build`**；若 PR 将触发 CI **`spa-build`**（路径条件见 **[docs/README · 文首（#content-framework）](docs/README.md#content-framework)**），合并前须再 **`make spa-build`**。改根目录任意 **`.html`**（读站指路、多页页脚、**`analysis-hub`** 导读等）且需 **`spa/public/`** 内 iframe 与 **`public/docs`** 与 MPA 一致时，**`make spa-sync`**（**[spa/README.md](spa/README.md)** · **[MERGE · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)** · **[维护导读](maintainer-hub.html)** · **[关系视图](maintainer-hub.html#mh-spine-map)** · **[系统边界](maintainer-hub.html#mh-boundaries)** · **[衔接矩阵](maintainer-hub.html#mh-reader-admin-matrix)**）。**可选分析栈**：`requirements-analytics.txt`（[DATA_CONTRACTS.md](docs/DATA_CONTRACTS.md)）；API 依赖见上文 **只读 API**。

<a id="contributing-validate-faq"></a>

### validate 常见失败速查

| 现象或报错 | 优先检查 |
|------------|----------|
| **registry / navLinks / `nav.config` 对账失败** | **`scripts/evolution-registry.json`** 的 **`pages[]`** 与 **`spa/nav.config.json`** 的 **`items[].page`** 一致；**`make gen-nav-links`**；对表 [PROJECT · §1a](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)。 |
| **`sync_site_nav --check` / 顶栏不一致** | 改过 **`partials/site-nav.inc.html`** 或 **`partials/skip-bar.inc.html`** 后执行 **`make sync-nav`** 再 **`make validate`**。**`maintainer-hub.html`** 在五链后另有三条页内 skip（**`#mh-spine-map` / `#mh-boundaries` / `#mh-reader-admin-matrix`**），由 **`scripts/sync_site_nav.py` · `build_skip_bar`** 生成；**勿**在 HTML 里手改这三条。注释**仅**能写在 **`partials`** 内 **`<div class="skip-bar">` / `<header class="site-nav">`** 中，勿在块外重复（见 **[scripts/README · #sync-site-nav-source](scripts/README.md#sync-site-nav-source)**）。 |
| **`404.html` / `legacy-all-in-one.html` / skip-bar 单测失败** | 二者均**不在** **`sync_site_nav`** 写回范围；改 **`partials/skip-bar.inc.html`** 后须**手调** **`404.html`** 与 **`legacy-all-in-one.html`** 五链 skip；**`make validate`** 含 **`check_skip_bar_404.py`** 与 skip 对表单测 — [MERGE · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [scripts/README · #sync-site-nav-source](scripts/README.md#sync-site-nav-source)。 |
| **根目录 HTML 指向 `docs/*.md` 无 fragment** | 站内相对链须为 **`docs/foo.md#anchor`** 形式 — 见单测 **`test_root_html_docs_md_hrefs`**。 |
| **`evolution-registry.json` Schema / 语义对账失败** | 对照 **`docs/schemas/evolution-registry.schema.json`**；**`pages[]`**、**`lab_factors`** 与 **`assets/lab.js`**、**`check_manifest_drift`** 引用一致；可先 **`make test`**（含 registry Schema）。 |
| **`manifest` / 候选 / hint 决策 JSON 结构或交叉引用失败** | 读 **`run_validate.sh`** 输出中的文件路径；对表 [DATA_CONTRACTS](docs/DATA_CONTRACTS.md) 与 registry / ingest 配置。 |
| **`analysis-snapshot` / 沉淀 / 趋势 JSON 与 Schema 不一致** | 与 **`docs/schemas/`** 对表；勿在未递增 **`schema_version`** 时改已提交快照字段语义；完整链路见 **`analysis_engine.py --check`**（已含于 **`make validate`**）。 |
| **Python `compileall` 或 `scripts/tests` 单测红** | 从日志中**第一个**失败用例入手；单独复现：**`PYTHONPATH=scripts python3 -m pytest scripts/tests/… -q`**。 |
| **只读 API 单测未跑 / 与 CI 不一致** | 本地安装 **`requirements-api.txt`** 后 **`make test-readonly-api`**（**`make merge-ready`** 已含）。 |
| **本地 `PermissionError`（`.pyc` / 缓存目录）** | 使用 **venv**、或对仓库根 **`make validate`** 在可写环境下执行（与 CI 一致即可）。 |
| **PR 将触发 CI `spa-build` 但未本地构建** | 合并前补 **`make spa-build`**（**`merge-ready` 不含**）；路径条件见 [docs/README 文首](docs/README.md#content-framework) 与 [MERGE · pre-merge](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)。 |

仍失败可用 **[流水线 / 校验失败排查](.github/ISSUE_TEMPLATE/pipeline-triage.md)** 开 Issue（附完整日志与分支）。根目录 [README · 从这里开始](README.md#readme-start-here) 与 [README · 双轨真源](README.md#readme-dual-track-map) 可与本表对读。

<a id="contributing-terminology"></a>

## 架构术语与契约纪律（PR 描述建议写清）

避免把不同「版本线」与职责混在一句话里：

| 说法 | 指什么 | 典型字段 / 文件 |
|------|--------|-----------------|
| **分析运行** | 某次 `analysis_engine` / 流水线算快照 | `analysis-snapshot.json` · **`run.run_id`**、**`run.repo_revision`** |
| **站点发布线** | 人为宣告的展示里程碑（与分析跑次无关） | **`assets/site-meta.json`** · **`site_version`** |
| **分析 / 快照** | 热力、共现、提示、闭环缺口等结构化产出 | **`analysis-snapshot.json`**（引擎**不写** HTML） |
| **内容生成** | 读者看到的叙事与版式 | 根目录 **`.html`**、人写为主 |
| **不断进化 / 不断优化** | 本站内分工：**进化** = 不变量内扩展契约、管道或消费方；**优化** = 域与真源语义基本不变时的清单化抛光与互链 | **[INTELLIGENCE · #evolution-and-optimization](docs/INTELLIGENCE_SIX_DOMAINS.md#evolution-and-optimization)**（**优化**不替代 Schema / 总线登记） |
| **持续分析优化** | 日常小轮：先读 **DATA_ANALYSIS** / **DATA_CONTRACTS** 判影响面，再按 **进化 vs 优化** 定性，**`make validate`** + **§6 PR 自检** 收束（文首紧接「不断优化」） | **[INTELLIGENCE · #continuous-analysis-optimization](docs/INTELLIGENCE_SIX_DOMAINS.md#continuous-analysis-optimization)** |
| **持续的优化** / **持续的进行优化** | **不断优化** 的节律化 + **反复执行**；与 **持续分析优化** 接力（先判型，再跑发版后清单） | **[INTELLIGENCE · #sustained-optimization](docs/INTELLIGENCE_SIX_DOMAINS.md#sustained-optimization)** · **[#ongoing-optimization](docs/INTELLIGENCE_SIX_DOMAINS.md#ongoing-optimization)** |
| **持续的升级** | **工程**阶段 0—3 与 **PHASED / ROADMAP / 模块矩阵** 节律；与 **不断进化** 分工：进化写域契约，**本行**写门禁与反模式；与 §1「升级表述」**同词不同指** | **[INTELLIGENCE · #sustained-upgrade](docs/INTELLIGENCE_SIX_DOMAINS.md#sustained-upgrade)** |
| **五维 · 六域 · 七类** | **不同抽象层次**：**五维** = PROJECT 总索引（数据·内容·演进·方法论·运行态）；**六域** = INTELLIGENCE 智能化分工与 PR 自检；**七类** = ARCHITECTURE 工程模块表 — **勿**在一句里混成可互换词 | **[勿混粒度 · 五维/六域/七类](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · **[§1 五维表](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#five-lenses)** · **[INTELLIGENCE · §2 六域](docs/INTELLIGENCE_SIX_DOMAINS.md#six-domains)** · **[ARCHITECTURE · 七类](docs/ARCHITECTURE.md#seven-layers)** |

**契约先行**：若改 **快照**、**沉淀** 或 **趋势** JSON 的语义结构，须**先**更新对应 **`docs/schemas/*.schema.json`** 与校验脚本，再改 **`evolution_pkg.analysis_pipeline`**（及薄 **`analysis_engine.py`**）或消费方（与下表「常见变更自检」一致）。

<a id="contributing-pr-evidence-triad"></a>

### PR 证据三联（建议 reviewer 一眼能扫）

1. **闸门**：本 PR 已跑 **`make validate`**（及按需 **`make merge-ready`** / **`make spa-build`**）的结论或**关键日志一行**（失败则勿标可合并）。  
2. **契约范围**：触及哪些 **JSON / Schema / `evolution_pkg`**；若动快照语义是否已 bump **`schema_version`** — [DATA_CONTRACTS](docs/DATA_CONTRACTS.md)。  
3. **外源与叙事**：改 **ingest** 时是否符合 **INTEL** 分层（含 [§2b 微博/站内流](docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)）；改 **HTML** 时粒度（五维/六域/七类择一）与 [DATA_ANALYSIS_SITE_CONTENT_SYNC](docs/DATA_ANALYSIS_SITE_CONTENT_SYNC.md) 是否对读。与 [EVOLUTION_RUNBOOK · 证据三联](docs/EVOLUTION_RUNBOOK.md#pr-evidence-triad) 对表。

## CI 与分支保护

- **`ci.yml` · validate**：始终运行，**以根目录 MPA 为默认真源**；安装 **`requirements.txt` + `requirements-api.txt`**，**`test_readonly*.py`**（ETag / 304 + 代理白名单对账）不再跳过。
- **`ci.yml` · spa-build**：仅当变更触及 `spa/`、**`scripts/evolution-registry.json`**、**`docs/schemas/evolution-registry.schema.json`**、**`scripts/validate_evolution_registry_schema.py`**、sync 相关路径等时才运行，否则 **skipped** 属正常。
- 建议分支保护**只必选 `validate`**；双轨说明见 **[docs/README.md · #content-framework](docs/README.md#content-framework)**。

<a id="contributing-common-changes-checklist"></a>

## 常见变更自检

| 你在改什么 | 至少要做 |
|------------|----------|
| 根目录新分页 / `maps_to.pages` | 更新 **`scripts/evolution-registry.json`**（须符合 [**`docs/schemas/evolution-registry.schema.json`**](docs/schemas/evolution-registry.schema.json)）；顶栏只改 **`partials/`** 后 **`make sync-nav`**（**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 写回，勿手改 HTML）；若本轮动 **`partials/skip-bar.inc.html`**（或失页顶栏须与模板一致），**`404.html`** 须**手调**（`sync_site_nav` 不写回）— [MERGE · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [scripts/README · #sync-site-nav-source](scripts/README.md#sync-site-nav-source)。**骨架**：**`<main id="main" tabindex="-1" aria-label="正文">`** 包住 **`</header>`—`</footer>`** 间主体（**每页一处 `<main>`**），与 skip **`#main`**、**`site-data-bus.js`** 回顶一致 — [ARCHITECTURE_ONE_PAGER · 内容与呈现](docs/ARCHITECTURE_ONE_PAGER.md#content-presentation) · [SITE_REVIEW · §3.5](docs/SITE_REVIEW_THREE_PASSES.md#section-3-5-lead-readhint) |
| 只改 **`partials/site-nav.inc.html`** / **`partials/skip-bar.inc.html`**（全站顶栏、skip-bar **模板**） | **`make sync-nav`** → **`make validate`**（含 **`sync_site_nav --check`**）；**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 写回，**勿**在 HTML 手改；**`404.html`** 不在 **`sync_site_nav`** 写回列表，失页顶栏/skip 须**手调**与 partial 一致 — [MERGE · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [scripts/README · #sync-site-nav-source](scripts/README.md#sync-site-nav-source) |
| 仅改 **`evolution-registry.json`** 的 **`pages[]`/`lab_factors`**（页面清单或因子集） | **三件套**：**`make sync-nav`**（顶栏/skip-bar；**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 写回，勿手改 HTML）→ **`spa/nav.config.json`** 中 **`items[].page`** 与 **`pages`** 对齐 → **`make gen-nav-links`**（或 CI 触达时 **`make spa-build`**）→ **`make test`** / **`make validate`**（**`check_nav_links_registry`**）；对表 [PROJECT · §1a](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)。若同 PR 动 **`partials/skip-bar.inc.html`**，**`404.html`** 须**手调** — [MERGE · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [scripts/README · #sync-site-nav-source](scripts/README.md#sync-site-nav-source) |
| 沙盘因子 | registry **`lab_factors`** 与 **`assets/lab.js`** 中 `id` 集合一致 |
| 维护 **SPA** | 编辑 **`spa/nav.config.json`**（顺序/文案）后 **`make gen-nav-links`**；**`spa/src/navLinks.ts` 勿手改**；**`make test`** / **`make validate`** 跑 **`check_nav_links_registry.py`** |
| 改 **`admin-console/`**（管理端脚手架） | **`make validate`**（**`compileall admin-console/app`**）+ **`make test-admin-console`**；Compose 见 **`docs/DOCKER.md#profile-admin`**；CI 在变更触及 **`admin-console/**`** 时跑 **`admin-console-tests`**；单页 **`static/index.html`** 的**七模块**顶栏与 **`mod-*`**、**`#mod-api`**→**`#mod-analysis`** 见 **[ADMIN_CONSOLE · §7](docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-module-plan)** · **[§11a 链入索引](docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md#admin-console-doc-index)** |
| 改 **`scripts/ingest_config.json`** / **`maps_to_hints.json`** 或 RSS / **`json_feeds`** 路线 | **`make validate`**；入口与命令 **[scripts/README](scripts/README.md)**；信源与人审节奏 **[INTEL_AND_POLICY_TRACKING_PLAYBOOK](docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md)**（**[§2—2a 拉取约束](docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-source-tiers)** · **[§2b 微博/站内流](docs/INTEL_AND_POLICY_TRACKING_PLAYBOOK.md#intel-social-platforms)**）；字段与校验 **[DATA_CONTRACTS · `ingest_config` 表行](docs/DATA_CONTRACTS.md#ingest-config-contract)**；开源对标与暴露面 **[REFERENCE_DESIGN_OPINION_MONITORING](docs/REFERENCE_DESIGN_OPINION_MONITORING.md)** |
| 改 **`assets/site-data-bus.js`**（`SiteDataBus`、live strip、**读者壳层**：顶缘进度 / 回顶 FAB） | **`make validate`**；**无新 JSON `fetch` 时**不必改 §3 消费方表，对读 **[SITE_DATA_UPDATE · §3a](docs/SITE_DATA_UPDATE_FRAMEWORK.md#reader-chrome)** · **[INTELLIGENCE · §2.2](docs/INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)** |
| 新增 **`evolution_pkg`** 顶层子模块（`.py` 或子包） | 在 **`scripts/evolution_pkg/domains.py`** · **`SUBMODULE_DOMAIN`** 登记**主归属域**（六域协同）；**`make test`** 校验目录与映射一致 |
| 新增 ingest / 分析 / 导航等**管道核心逻辑**（非薄壳） | 实现落在 **`scripts/evolution_pkg/`**，**`scripts/*.py`** 保持薄 CLI；见 [scripts/README · 收束队列](scripts/README.md#pkg-migrate-queue) · [ONE_PAGER · 不变量索引](docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) |
| 改 **沉淀/趋势** 结构 | 同步 **`docs/schemas/sediment*.schema.json`**；**`make test`** / **`make validate`** 含 **`validate_sediment_artifacts_schema.py`**（实现 **`evolution_pkg.sediment_validate`**） |
| 快照结构 | 递增 **`schema_version`**，并改 **`docs/schemas/analysis-snapshot.schema.json`** 与校验脚本 |
| **manifest** | 仅 **`review_state=queued_for_manifest`** 可合并；勿绕过人审闸门 |
| 带 **`nexus-legend`** 的枢纽页 | 三色 **CSS 类可复用**，**中文标签按页定义**（类名≠全站同一套三字文案），见 [ARCHITECTURE.md · 三色标签](docs/ARCHITECTURE.md#nexus-tag-labels) |

完整检查单：[PLATFORM_CAPABILITY_MAP.md §6](docs/PLATFORM_CAPABILITY_MAP.md#enhance-checklist) · 扩展性与进化 [§8](docs/PLATFORM_CAPABILITY_MAP.md#extensibility) · [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md) · [MERGE_AND_RELEASE_CHECKLIST.md · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · 只读 API 集成 [INTEGRATION_AND_READONLY_API.md](docs/INTEGRATION_AND_READONLY_API.md)。

**读者路径与发布复查（摘要）**：顶栏链与注册表一致，新人可先记 **五枢纽**（总览 → 立体联结或模块图谱 → 综合推演 → 分析引擎 → 沙盘），见 [index.html · 读站指路](index.html#read-guide)。**本地起读者站**：根目录 **`make serve-reader`**（**8000**）或 Docker **8765**，勿 **`file://`** 双击 `index.html`（总线 **`fetch`** 常失败）— 见根 [README.md](README.md) 与 [docs/DOCKER.md](docs/DOCKER.md) §1。站内 **`docs/*.md`** 在 **GitHub Pages 根部署**下多为原文/下载，与网页渲染不同，见 [PLATFORM · §7](docs/PLATFORM_CAPABILITY_MAP.md#reader-and-release) 与 [SITE_REVIEW · 四角色复查](docs/SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)。**大版本或改顶栏/总线后**建议在 **`make validate`** 之外过一遍该节中的 **发布前轻量清单**。

<a id="maintainer-reading-order"></a>

## 阅读顺序（维护者）

与 **[docs/README.md · 文档主线（表）](docs/README.md#docs-spine)** 同序；**读者面/管理面一页**（与闸门、脚本对读）见 **[PLATFORM_MASTER_MAP · 节 1a](docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)**；**可执行单元 × 主链（组件—功能）**见 **[docs/README · #system-components-fusion](docs/README.md#system-components-fusion)**（与 **#front-back-modules** 互补）。**先按本轮改动判型**见 **[docs/README · 常见改动最短链](docs/README.md#quick-paths)**（与主线表 **0c** 同锚）。若仍要按序号通扫，可从下列序号开始：

1. [MERGE_AND_RELEASE_CHECKLIST.md · §1](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)（合并/发布一页）· [ARCHITECTURE_ONE_PAGER.md](docs/ARCHITECTURE_ONE_PAGER.md)（**[三架构对照](docs/ARCHITECTURE_ONE_PAGER.md#three-architectures)**）· [TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md](docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md)（简版 **§1—§4**；**[详版附录](docs/TECH_ARCHITECTURE_AND_UPGRADE_BRIEF.md#appendix-tech-capabilities)** · [旧链别名](docs/TECH_ARCHITECTURE_CAPABILITIES.md)）  
2. [PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md](docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)（插槽、进化轨、**[智能化与自动化边界](docs/PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)**）· [PLATFORM_CAPABILITY_MAP.md §8](docs/PLATFORM_CAPABILITY_MAP.md#extensibility) · [USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](docs/USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)（用户端/管理端 · 数据源 · 审核；**[节 1a · 前端读者 · 后端管理](docs/USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)**）  
3. [ARCHITECTURE.md](docs/ARCHITECTURE.md)（数据流、适应度函数、七类模块）· [DATA_CONTRACTS.md](docs/DATA_CONTRACTS.md) · [schemas/README.md](docs/schemas/README.md) · **[勿混粒度 · 五维/六域/七类](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [§1a/§1b](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)（主链联动验证 · **[§1b 仓库物理分层](docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout)**）  
4. [PLATFORM_CAPABILITY_MAP.md](docs/PLATFORM_CAPABILITY_MAP.md)（四条支柱、MPA/SPA、**[阅读顺序 §5](docs/PLATFORM_CAPABILITY_MAP.md#reading-order)**）  
5. [scripts/README.md](scripts/README.md)（命令表）· [EVOLUTION_RUNBOOK.md](docs/EVOLUTION_RUNBOOK.md) · [SITE_DATA_UPDATE_FRAMEWORK.md](docs/SITE_DATA_UPDATE_FRAMEWORK.md)（**`[data-site-data-live]`** 消费方；**纯 CSS/HTML 枢纽版式**见 [INTELLIGENCE · §2.2](docs/INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)，**不**写入本框架表）  
6. 全站 **页头 `lead` / `read-hint` 分层**：[SITE_REVIEW_THREE_PASSES.md](docs/SITE_REVIEW_THREE_PASSES.md) · §3.5 · **深链与本轮提要** §3.6 · **[四角色复查](docs/SITE_REVIEW_THREE_PASSES.md#four-perspectives-review)**；与 **[AGENTS.md · 枢纽首屏](AGENTS.md#agents-hub-lead)** 对读；枢纽 MPA **CSS 复用（`modular-intro-stack`、`toc--pilot` 等）**：[INTELLIGENCE_SIX_DOMAINS · §2.2](docs/INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)  
7. 分阶段升级：**[PHASED_UPGRADE_EXECUTION_GUIDE.md](docs/PHASED_UPGRADE_EXECUTION_GUIDE.md)**（按阶段执行）· [ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md](docs/ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md) · 可落地全景：[ARCHITECTURE_UPGRADE_ROADMAP.md](docs/ARCHITECTURE_UPGRADE_ROADMAP.md) · 模块对表：[MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md](docs/MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md) · 编排/事件流：[ORCHESTRATION_AND_EVENT_STREAMING.md](docs/ORCHESTRATION_AND_EVENT_STREAMING.md)  
8. 只读 API 集成：[INTEGRATION_AND_READONLY_API.md](docs/INTEGRATION_AND_READONLY_API.md) · 内容草稿插槽：[scripts/draft/README.md](scripts/draft/README.md)

**改 SPA 壳**（`spa/src/SpaLayout.tsx`、`spaRouteMeta.ts`、`LegacyFrame.tsx`）时：快捷链顺序须与 **`partials/skip-bar.inc.html`** 一致；总览 **`#read-guide`** / **`#three-questions`** / **`#hub-catalog`** / **`#index-intent-pick`** / **`#reader-next`** 的 **`document.title`·读屏** 与 **iframe `title`** 须在 **`spaRouteMeta`** 与 **`LegacyFrame`** 中成对更新（见 **[AGENTS.md · 双轨](AGENTS.md#agents-dual-track)**）。

PR 请使用模板 **[`.github/pull_request_template.md`](.github/pull_request_template.md)**。

**校验或 Actions 仍失败**：新建 Issue 可选用 **[流水线 / 校验失败排查](.github/ISSUE_TEMPLATE/pipeline-triage.md)**（模板文首链回本文，便于对照 **validate** / **spa-build**）。
