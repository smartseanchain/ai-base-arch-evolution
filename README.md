# 基础架构演变推演

静态站点 + **可进化观测管道**（manifest / 候选 / 分析 / 沉淀）。概念总览见站内 [可进化架构](evolvable-architecture.html)（本地打开 `evolvable-architecture.html` 或通过任意静态服务器访问）。

## 本地校验与流水线

```bash
make validate    # manifest + 候选 + analysis_engine --check
make ingest      # 抓取候选（需外网，依赖 scripts/ingest_config.json）
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
SITE_BASE=https://你的域名或GitHub Pages路径 make sitemap
```

未设置 `SITE_BASE` 时 `make sitemap` 会报错退出，避免误写占位域名。

## Docker

见仓库内 `docker-compose.yml`、`Dockerfile`（按需使用）。

## 持续集成

- `ci.yml`：PR/推送时校验 JSON、`compileall`、`analysis_engine --check`
- `update-pipeline.yml`：定时/手动分析 artifact
- `ingest-pipeline.yml`：手动抓取候选 artifact

## 许可与合规

抓取须遵守各源站 robots.txt 与版权；候选线索须经人工审阅后再 `merge` 进 `evolution-manifest.json`。
