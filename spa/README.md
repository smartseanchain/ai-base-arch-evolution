# 全站 SPA（React）

与仓库根目录**多页静态 HTML**并行存在：本目录构建产物为**单页应用壳**，路由由 **React Router** 管理；各「页」实际为 **iframe** 加载同步自根目录的 HTML（已去掉顶栏/skip-bar，避免与壳重复）。壳与 iframe 内页共同服务**读者面（前端）**；**脚本、CI、merge、只读 API** 等管理动作仍在 **[USER_ADMIN_SPLIT · 节 1a](../docs/USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)** 所述**后端管理面**。**首次贡献**（**`make validate`** / **`make merge-ready`**（与 CI 对齐推荐）/ **`make test`**（子集）、`navLinks` 与 registry、CI）：根目录 [CONTRIBUTING.md](../CONTRIBUTING.md) · [MERGE_AND_RELEASE_CHECKLIST.md](../docs/MERGE_AND_RELEASE_CHECKLIST.md)。

## 命令

| 命令 | 说明 |
|------|------|
| `npm run sync` | 在仓库根执行 `python3 scripts/sync_spa_public.py`，刷新 `public/` |
| `npm run dev` | 开发服务器（`predev` 会先 sync） |
| `npm run build` | 生产构建 → `dist/`，并复制 `index.html` → `404.html`（Pages 深链） |
| `npm run preview` | 本地预览 `dist/` |

仓库根等价：`make gen-nav-links`、`make spa-sync`、`make spa-build`、`make spa-preview`（**`spa-build` 会先跑 `gen-nav-links`**）。

**根目录 `index.html`（读站指路、总览正文等）** 变更后须 **`make spa-sync`**（或 **`npm run sync`**），否则壳内 **`legacy-index.html`** 与 **`public/docs/`** 仍为旧版；CI **`spa-build`** 会在构建前同步。

## 顶栏配置（`nav.config.json`）

- **`spa/nav.config.json`**：`items` 为 `{ "page": "foo.html", "label": "中文" }` 有序列表；**`page` 集合须与 `scripts/evolution-registry.json` 的 `pages` 完全一致**。结构契约：[**`docs/schemas/spa-nav-config.schema.json`**](../docs/schemas/spa-nav-config.schema.json)（由 **`check_nav_links_registry`** / **`make validate`** 校验）。
- **`src/navLinks.ts`**：由 **`python3 scripts/gen_nav_links_ts.py --write`** 或 **`make gen-nav-links`** 生成，**请勿手改**。
- 增删注册页：先改 registry → 再改 **`nav.config.json`** → **`make gen-nav-links`** → **`make sync-nav`**（顶栏 partial）按需。

## CI

**Cursor**：编辑 **`src/**`** 时适用 [`.cursor/rules/spa-nav-registry.mdc`](../.cursor/rules/spa-nav-registry.mdc)；编辑 **`nav.config.json`** 见 [`.cursor/rules/spa-nav-config.mdc`](../.cursor/rules/spa-nav-config.mdc)（**`pages`** 集合与 **`scripts/evolution-registry.json`** 一致；改 registry 见 [`.cursor/rules/evolution-registry.mdc`](../.cursor/rules/evolution-registry.mdc)）。

根目录 [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) 中 **`spa-build`** 仅在变更影响同步产物、**`scripts/evolution-registry.json`**、**`docs/schemas/evolution-registry.schema.json`**、**`scripts/validate_evolution_registry_schema.py`**（与壳内路由 / 契约对齐）或 SPA 源码时执行（`dorny/paths-filter`）；其余提交该 job 为 **skipped**。合并闸门建议以 **`validate`** job 为准，避免将 **spa-build** 设为必选（否则无相关变更的 PR 会一直等待跳过项）。

## GitHub Pages（项目站）

构建时指定与 Pages 一致的 **base**（示例仓库路径）：

```bash
cd spa && npm run sync && VITE_BASE=/ai-base-arch-evolution/ npm run build
```

将 **`dist/` 下全部文件** 部署到站点根。原 `404.html` 在同步中写入 **`standalone-404.html`**，避免被 SPA 的 `404.html` 覆盖。

## 路由

路由段来自 **`scripts/evolution-registry.json`** 的 `pages`（`index.html` → 首页 iframe 使用 `legacy-index.html`）。顶栏顺序与文案见 **`nav.config.json`**（生成 **`src/navLinks.ts`**）；增页时请与 **`partials/site-nav.inc.html`** 对齐。

## 壳层体验（与 MPA 对齐）

- **读者面 / 管理面**：顶栏 **`SpaLayout.tsx`** 第二段说明含至 **[PLATFORM_MASTER_MAP · 1a](../docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces)** 的链（`platformMasterReaderAdminHref`）及壳内 **`/maintainer-hub`**；外链 Markdown 须已同步 **`spa/public/docs/`**（**`make spa-sync`** / **`npm run sync`**）。
- **快捷跳转**：与 **`partials/skip-bar.inc.html`** 同序——跳到正文、三问导读、读站指路、分区速跳；壳内另增 **跳到分页导航**（`#spa-site-nav`），因分页链接集中在顶栏。
- **药丸**：「三问」「分区」指向总览锚点，语义与 **`partials/site-nav.inc.html`** 中顶栏链一致（总览另有 `#read-guide`，见快捷链）。
- **标题与读屏**：**`src/spaRouteMeta.ts`** 统一 `document.title` 与 `aria-live` 文案；总览带 hash 时含「读站指路」「三问导读」「分区速跳」等，与 skip 文案一致。
- **iframe `title`**：**`src/LegacyFrame.tsx`** 里 **`legacy-index.html`** 的 hash 分支（**`#read-guide`**、**`#three-questions`**、**`#hub-catalog`**）须与 **`spaRouteMeta`** 语义对齐，避免无障碍名称不一致。
- **子路径部署**：**`src/main.tsx`** 中 **`basename`** 须与 **`vite.config.ts`** 的 **`base`**（环境变量 **`VITE_BASE`**）一致，见上文 GitHub Pages 示例。

## 技术选型说明

当前为 **React 18** + **Vite 6** + **TypeScript 5.7**（非 Vue）；若需 Vue，可另起 `spa-vue/` 或替换为 Vite + Vue 模板，路由与 `sync_spa_public` 策略可复用。
