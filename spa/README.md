# 全站 SPA（React）

**产品视角四条动线**（读者 / 贡献 / 数据 / 部署）：[README · 产品视角](../README.md#pm-four-journeys) · [README · 从这里开始](../README.md#readme-start-here) · [README · 双轨真源](../README.md#readme-dual-track-map)（本目录偏 **读者壳 + iframe**；registry / CI / 合并闸门仍以根目录真源为准）。

<a id="spa-default-read"></a>

**默认读站**：以根目录 **MPA**（多页 HTML）为主——**`make validate`**、深链与「读者五枢纽」叙述均以分页为默认真源。本 **`spa/`** 为**可选并行壳**（React Router + iframe）；需要单页导航或将 **`dist/`** 挂到 **GitHub Pages 项目子路径** 时再启用（见下文 **GitHub Pages**）。

**架构师梳理（五步）**：[ARCHITECTURE_ONE_PAGER · #architect-stewardship](../docs/ARCHITECTURE_ONE_PAGER.md#architect-stewardship) · [不变量索引](../docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [PR 证据三联](../CONTRIBUTING.md#contributing-pr-evidence-triad) · [动手→命令速查](../CONTRIBUTING.md#contributing-change-to-command)。

**整体内容框架 / 前后台模块一页表 / 组件×功能一条表**：[docs/README · #content-framework](../docs/README.md#content-framework) · [#front-back-modules](../docs/README.md#front-back-modules) · [#system-components-fusion](../docs/README.md#system-components-fusion)。

与仓库根目录**多页静态 HTML**并行存在：本目录构建产物为**单页应用壳**，路由由 **React Router** 管理；各「页」实际为 **iframe** 加载同步自根目录的 HTML（已去掉顶栏/skip-bar，避免与壳重复）。壳与 iframe 内页共同服务**读者面（前端）**；**脚本、CI、merge、只读 API** 等管理动作仍在 **[USER_ADMIN_SPLIT · 节 1a](../docs/USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)** 所述**后端管理面**。**首次贡献**（**`make validate`** / **`make merge-ready`**（与 CI 对齐推荐）/ **`make test`**（子集）、`navLinks` 与 registry、CI）：根目录 [CONTRIBUTING.md](../CONTRIBUTING.md#contributing-env-and-cmd) · [开 PR 前速览](../CONTRIBUTING.md#contributing-five-minute) · [MERGE_AND_RELEASE_CHECKLIST.md](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)。**自动化助手（MPA+SPA 双轨 · `spa-build` 不含于 `merge-ready`）**：[AGENTS.md · 双轨](../AGENTS.md#agents-dual-track) · [合并前闸门](../AGENTS.md#agents-pre-merge)。**`spa/` 在仓库物理分层中的位置 · 主链验收入口**：**[勿混粒度 · 五维/六域/七类](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain)** · [PROJECT_ARCHITECTURE_OVERVIEW · §1b](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#physical-layout) · **[§1a](../docs/PROJECT_ARCHITECTURE_OVERVIEW.md#module-linkage-validation)**。**按改动判型**（**0c**）：**[docs/README · #quick-paths](../docs/README.md#quick-paths)**（表内「**情报 ingest · 管理控制台 · SPA 壳**」行常与 **`nav.config` ≡ registry** 同轮改动一起打开）。

**读者 MPA 上维护枢纽**：[维护导读](../maintainer-hub.html) · [关系视图](../maintainer-hub.html#mh-spine-map)（本页 ↔ 注册表 ↔ 文档锚点，与壳内路由对读）· [系统边界速查](../maintainer-hub.html#mh-boundaries) · [衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)。

## 命令

| 命令 | 说明 |
|------|------|
| `npm run sync` | 在仓库根执行 `python3 scripts/sync_spa_public.py`，刷新 `public/` |
| `npm run dev` | 开发服务器（`predev` 会先 sync） |
| `npm run build` | 生产构建 → `dist/`，并复制 `index.html` → `404.html`（Pages 深链） |
| `npm run preview` | 本地预览 `dist/` |

仓库根等价：`make gen-nav-links`、`make spa-sync`、`make spa-build`、`make spa-preview`（**`spa-build` 会先跑 `gen-nav-links`**）。

**`sync_spa_public`** 会整棵复制根目录 **`assets/`** 至 **`spa/public/assets/`**（含 **`site-data-bus.js`**、**`site.css`**；若仓库内已有 **`site-search-index.json`** 亦一并同步）。**MPA 顶栏内嵌的轻量搜索**随 **`site-nav` 剥壳**不会出现在 iframe 内页；壳内全局搜索若需与 MPA 对齐，须单独产品决策（当前未默认实现）。

**根目录任意 `.html`**（**`index.html`** 读站指路/总览、**其它注册页的页脚/导读**等）变更后须 **`make spa-sync`**（或 **`npm run sync`**），否则 **`spa/public/`** 内 iframe 源页、**`legacy-index.html`** 与 **`public/docs/`** 仍为旧版；CI **`spa-build`** 会在构建前同步。动线见 **[MERGE · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge)** · **[MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence)**；维护者收束 **[维护导读](../maintainer-hub.html)** · **[关系视图](../maintainer-hub.html#mh-spine-map)** · **[系统边界](../maintainer-hub.html#mh-boundaries)** · **[衔接矩阵](../maintainer-hub.html#mh-reader-admin-matrix)**。

## 顶栏配置（`nav.config.json`）

- **`spa/nav.config.json`**：`items` 为 `{ "page": "foo.html", "label": "中文" }` 有序列表；**`page` 集合须与 `scripts/evolution-registry.json` 的 `pages` 完全一致**。可选 **`group`**：连续相同 **`group`** 的条目在壳顶栏合成一组 **`<details>`**（与 MPA **`partials/site-nav.inc.html`** 分组一致）。结构契约：[**`docs/schemas/spa-nav-config.schema.json`**](../docs/schemas/spa-nav-config.schema.json)（由 **`check_nav_links_registry`** / **`make validate`** 校验）。
- **`src/navLinks.ts`**：由 **`python3 scripts/gen_nav_links_ts.py --write`** 或 **`make gen-nav-links`** 生成，**请勿手改**。导出 **`NAV_LINKS`**（扁平，供路由元数据）与 **`NAV_GROUPS`**（分组，供 **`SpaLayout`** 渲染）。
- 增删注册页：先改 registry → 再改 **`nav.config.json`** → **`make gen-nav-links`** → **`make sync-nav`**（顶栏 partial）按需；**`maintainer-hub.html`** 五链后三锚由 **`build_skip_bar`** 生成，勿手改 HTML；若本轮动到 **`partials/`**，**`404.html`** 顶栏/skip 须**手调**（`sync_site_nav` 不写回）— [MERGE · §1](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge) · [MERGE · partials 手顺](../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence) · [scripts/README · #sync-site-nav-source](../scripts/README.md#sync-site-nav-source)。

## CI

**Cursor**：编辑 **`src/**`** 时适用 [`.cursor/rules/spa-nav-registry.mdc`](../.cursor/rules/spa-nav-registry.mdc)（与根目录 [AGENTS.md · Cursor 规则](../AGENTS.md#agents-cursor-rules) 对读）；编辑 **`nav.config.json`** 见 [`.cursor/rules/spa-nav-config.mdc`](../.cursor/rules/spa-nav-config.mdc)（**`pages`** 集合与 **`scripts/evolution-registry.json`** 一致；改 registry 见 [`.cursor/rules/evolution-registry.mdc`](../.cursor/rules/evolution-registry.mdc)）。

根目录 [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) 中 **`spa-build`** 仅在变更影响同步产物、**`scripts/evolution-registry.json`**、**`docs/schemas/evolution-registry.schema.json`**、**`scripts/validate_evolution_registry_schema.py`**（与壳内路由 / 契约对齐）或 SPA 源码时执行（`dorny/paths-filter`）；其余提交该 job 为 **skipped**。合并闸门建议以 **`validate`** job 为准，避免将 **spa-build** 设为必选（否则无相关变更的 PR 会一直等待跳过项）。

## GitHub Pages（项目站）

<a id="spa-github-pages"></a>

构建时指定与 Pages 一致的 **base**（示例仓库路径）：

```bash
cd spa && npm run sync && VITE_BASE=/ai-base-arch-evolution/ npm run build
```

将 **`dist/` 下全部文件** 部署到站点根。原 `404.html` 在同步中写入 **`standalone-404.html`**，避免被 SPA 的 `404.html` 覆盖。

## 路由

路由段来自 **`scripts/evolution-registry.json`** 的 `pages`（`index.html` → 首页 iframe 使用 `legacy-index.html`）。顶栏顺序与文案见 **`nav.config.json`**（生成 **`src/navLinks.ts`**）；增页时请与 **`partials/site-nav.inc.html`** 对齐。

## 壳层体验（与 MPA 对齐）

- **读者面 / 管理面**：顶栏 **`SpaLayout.tsx`** 第二段说明含至 **[PLATFORM_MASTER_MAP · 1a](../docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)** 的链（`platformMasterReaderAdminHref`）及壳内 **`/maintainer-hub`**；**iframe 内 MPA** 首屏版式复用类见 **[INTELLIGENCE_SIX_DOMAINS · §2.2](../docs/INTELLIGENCE_SIX_DOMAINS.md#reader-layout-contract)**（与壳顶栏解耦）。外链 Markdown 须已同步 **`spa/public/docs/`**（**`make spa-sync`** / **`npm run sync`**）。
- **快捷跳转**：与 **`partials/skip-bar.inc.html`** 前五链同序——跳到正文、三问导读、读站指路、分区速跳、常见下一站；壳内于其后另增 **跳到分页导航**（`#spa-site-nav`），因分页链接集中在顶栏。
- **药丸**：「三问」「分区」指向总览锚点，语义与 **`partials/site-nav.inc.html`** 中顶栏链一致（总览另有 `#read-guide`，见快捷链）。
- **标题与读屏**：**`src/spaRouteMeta.ts`** 统一 `document.title` 与 `aria-live` 文案；总览带 hash 时含「读站指路」「三问导读」「分区速跳」等，与 skip 文案一致。
- **iframe `title`**：**`src/LegacyFrame.tsx`** 里 **`legacy-index.html`** 的 hash 分支（**`#read-guide`**、**`#three-questions`**、**`#hub-catalog`**、**`#index-intent-pick`**（壳层与 MPA 均用 **四条动线** 短名）、**`#reader-next`**）须与 **`spaRouteMeta`** 语义对齐，避免无障碍名称不一致。
- **子路径部署**：**`src/main.tsx`** 中 **`basename`** 须与 **`vite.config.ts`** 的 **`base`**（环境变量 **`VITE_BASE`**）一致，见上文 GitHub Pages 示例。

## 技术选型说明

当前为 **React 18** + **Vite 6** + **TypeScript 5.7**（非 Vue）；若需 Vue，可另起 `spa-vue/` 或替换为 Vite + Vue 模板，路由与 `sync_spa_public` 策略可复用。
