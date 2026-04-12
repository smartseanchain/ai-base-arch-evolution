---
name: 流水线 / 校验失败排查
about: 本地或 GitHub Actions 失败时的自检清单（也可用于讨论定时任务告警 Issue）
title: "[triage] "
labels: []
---

开 Issue 前可先看环境与合并前底线、CI 双轨说明：**[CONTRIBUTING.md](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/CONTRIBUTING.md)**。若在讨论**编排器 / Kafka / 生产库**等改造与 CI 分工，先对表 **[按阶段升级执行指南](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/PHASED_UPGRADE_EXECUTION_GUIDE.md)** 与 **[升级决策全景图](https://github.com/smartseanchain/ai-base-arch-evolution/blob/main/docs/ARCHITECTURE_UPGRADE_ROADMAP.md#upgrade-panorama)**（Fork 后请将文首链改为本仓库 `blob/main` 路径）。

## 失败场景

- [ ] `make validate` / pre-commit
- [ ] **CI · spa-build**（仅当 PR 改了 `spa/`、registry、sync 输入等才运行；未改则 **skipped** 属正常，合并以 **validate** 为准）
- [ ] `make ingest` / **Ingest candidates** workflow
- [ ] `make analyze` / **Update pipeline** workflow
- [ ] 其他：<!-- 简述 -->

## 环境

- 本地 OS：
- Python 版本（`python3 --version`）：

## 已尝试

- [ ] 已看 Actions 对应 Run 的日志与 Job Summary
- [ ] 本地复现：<!-- 命令与末 20 行 stderr -->

## 日志摘要

```
粘贴关键报错
```

## 备注

<!-- 链到失败的 workflow run、相关 PR 等 -->
