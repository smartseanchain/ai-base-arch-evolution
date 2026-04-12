# PR 切片模板（增量构建）

从 **[INCREMENTAL_BUILD_PLAYBOOK · §5](../INCREMENTAL_BUILD_PLAYBOOK.md#pr-slice-template)** 复制到 PR 描述；与 **[INTELLIGENCE_SIX_DOMAINS · §6 PR 自检](../INTELLIGENCE_SIX_DOMAINS.md#pr-checklist)**、**[PLATFORM_EXTENSIBILITY · 新增能力检查单](../PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#new-capability-checklist)** 合并使用。

```markdown
## 域（INTELLIGENCE §6）
- [ ] 数据  [ ] 管道  [ ] 分析  [ ] 前端  [ ] 运维  [ ] 治理

## 本 PR 骨架（已完成）
- [ ] Schema / validate 入口
- [ ] 单测或 smoke
- [ ] 文档（DATA_CONTRACTS / INTEGRATION / DOCKER 择一）

## 故意延后（后续 PR）
- …

## 验证
- [ ] make validate
- [ ] （推荐合并前）make merge-ready（**`validate`** + **`test-readonly-api`** · **`test_readonly*.py`** + **`test-admin-console`**）
```
