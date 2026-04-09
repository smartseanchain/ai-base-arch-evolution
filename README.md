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

- `ci.yml`：PR/推送时校验 JSON、**manifest/候选对账**（页面与 `lab.js`）、`compileall`、`analysis_engine --check`
- `update-pipeline.yml`：定时/手动分析 artifact
- `ingest-pipeline.yml`：**每周二 UTC 定时**或手动抓取候选 artifact；Job Summary 汇总各 RSS 源成功/失败（`ingest-summary.json` 一并上传）
- 在 GitHub 开 PR 时自动带出 **`.github/pull_request_template.md`**（合并 manifest/候选请勾选自检项）

## 许可与合规

抓取须遵守各源站 robots.txt 与版权；候选线索须经人工审阅后再 `merge` 进 `evolution-manifest.json`。
