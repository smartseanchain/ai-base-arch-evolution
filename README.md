# 基础架构演变推演

静态站点 + **可进化观测管道**（manifest / 候选 / 分析 / 沉淀）。

- **仓库**：https://github.com/smartseanchain/ai-base-arch-evolution  
- **GitHub Pages**（开启后）：https://smartseanchain.github.io/ai-base-arch-evolution/ — 在仓库 **Settings → Pages** 中选择 **Deploy from a branch**，分支 **main**，文件夹 **/ (root)**，保存后约 1～2 分钟可访问。  
- 本地预览：直接打开 `index.html`，或用任意静态服务器（`evolution.js` 等需 **http(s)** 才能 `fetch` JSON）。

概念总览见站内 [可进化架构](evolvable-architecture.html)。**双周反哺节奏**（可打印照做）：[docs/EVOLUTION_RUNBOOK.md](docs/EVOLUTION_RUNBOOK.md)。

## 本地校验与流水线

```bash
make validate    # manifest + 候选 + analysis_engine --check
make ingest      # 抓取候选（需外网，依赖 scripts/ingest_config.json）
make ingest-full # 同上但单次 --full-pool（忽略 require_route_match）
make analyze     # 校验 + 分析引擎 --sediment + 长期趋势
```

脚本说明：[scripts/README.md](scripts/README.md)。抓取配置：复制 [scripts/ingest_config.example.json](scripts/ingest_config.example.json) 为 `ingest_config.json` 后填写 RSS / 法规索引页。

## Git 钩子（可选）

```bash
bash scripts/install-git-hooks.sh
```

提交前会跑与 `make validate` 等价的检查。

## 站点地图

需设置站点根 URL（无尾斜杠）。**部署前**用真实域名生成并提交 `sitemap.xml`：

```bash
# 示例：当前默认 GitHub Pages 基址（无尾斜杠）
SITE_BASE=https://smartseanchain.github.io/ai-base-arch-evolution make sitemap
```

未设置 `SITE_BASE` 时 `make sitemap` 会报错退出，避免误写占位域名。

## Docker

见仓库内 `docker-compose.yml`、`Dockerfile`（按需使用）。

## 持续集成

- `ci.yml`：PR/推送时校验 JSON、**manifest/候选/ingest 配置对账**（见 `scripts/evolution-registry.json`）、`compileall`、`scripts/tests` **unittest**、`analysis_engine --check`
- `update-pipeline.yml`：定时/手动分析 artifact
- `ingest-pipeline.yml`：**每周二 UTC 定时**或手动抓取候选 artifact；Job Summary 汇总各 RSS 源成功/失败；**定时失败**会新建 Issue 提醒
- `update-pipeline.yml`：**定时失败**时同样会新建 Issue（与 ingest 对称），便于发现分析脚本或校验回归
- `pr-candidates.yml`：**手动**跑 ingest 并直接向 `main` 开 PR 更新 `evolution-candidates.json`（需在仓库 **Settings → Actions → General** 将 workflow 权限设为可读写；合并仍人审）
- 在 GitHub 开 PR 时自动带出 **`.github/pull_request_template.md`**（合并 manifest/候选请勾选自检项）。新建 Issue 可选用 **「流水线 / 校验失败排查」** 模板（`.github/ISSUE_TEMPLATE/`）。

### 定时流水线与仓库写入（预期）

- **默认**：上述定时/手动 workflow 产出 **artifact**，**不会**自动 push 到 `main`。线上站点里的 `analysis-snapshot.json`、`sediment.json` 等与 Git 一致，仍依赖你在本地 **`make analyze`**（或下载 artifact 人工合并后提交）。
- **合并 artifact 到主分支（建议）**：在 Actions 运行页下载 `analysis-outputs-*` → 解压后替换仓库内 `assets/analysis-snapshot.json`、`assets/sediment-trends.json`、`data/sediment.json` → 执行 **`make validate`** → `git commit` & push。
- **候选 PR**：可用 **`PR · refresh candidates`**（`pr-candidates.yml`）触发 bot 分支；**manifest 仍不自动 merge**，须本地/PR 内 `merge_candidates_to_manifest` 且 `review_state=queued_for_manifest`。

### 单一注册表

- **`scripts/evolution-registry.json`**：声明允许出现在 `maps_to.pages` 的根目录 HTML（不含 `404.html`）及全部 **`lab_factors`**；须与 **`assets/lab.js`** 中因子 `id` **集合完全一致**。
- **`check_manifest_drift.py`** 同时校验 `ingest_config.json`、`maps_to_hints.json` 内的页面/因子引用，以及 **`gen-sitemap.py` 的 `PRIORITY` 键** ⊆ 注册表页面。

本地：`make test` 仅跑单测；`make validate` 含单测与全套校验。

### 全站顶栏与 skip-bar

- **`<div class="skip-bar">`** 与 **`<header class="site-nav">`** 由模板生成：**`partials/skip-bar.inc.html`**、**`partials/site-nav.inc.html`**。`make sync-nav` 写回二者，`make check-site-nav` 校验（已含于 `make validate` 与 CI）。
- 增删导航链或无障碍快捷链时**只改对应 partial** 再跑 `make sync-nav`。`index.html` 上「三问导读 / 顶栏三问」为 `#three-questions`，其余页为 `index.html#three-questions`（脚本自动区分）。
- 顶栏内各 `href="*.html"` 须落在 **`scripts/evolution-registry.json`** 的 `pages` 内（`check_manifest_drift` 会查）。

## 许可与合规

抓取须遵守各源站 robots.txt 与版权；候选线索须经人工审阅后再 `merge` 进 `evolution-manifest.json`。
