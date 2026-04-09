---
name: 流水线 / 校验失败排查
about: 本地或 GitHub Actions 失败时的自检清单（也可用于讨论定时任务告警 Issue）
title: "[triage] "
labels: []
---

## 失败场景

- [ ] `make validate` / pre-commit
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
