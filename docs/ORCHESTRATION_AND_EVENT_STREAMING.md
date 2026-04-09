# 任务编排器与事件流：选型说明（相对本站默认栈）

本文回答：**Dagster / Prefect** 与 **Kafka / Redpanda** 在本仓库语境下何时值得引入、如何与现有 **GitHub Actions + `evolution_pkg.pipeline` + JSON 真源** 并存。定性脚手架、非采购建议——落地前须结合团队运维能力与合规要求。

## 1. 本站默认「编排」是什么

| 层级 | 现状 |
|------|------|
| **调度** | GitHub Actions（定时 / 手动 workflow） |
| **本地/合并前** | `make validate`、`make analyze`（`evolution_pkg.pipeline.runner` + 遥测 JSON） |
| **事实源** | Git 中的 `assets/*.json`、`data/sediment.json`；人审闸门不进自动 manifest |
| **可观测性** | `artifacts/pipeline-metrics-*.json`、workflow 日志、Issue 告警 |

这一组合在**低并发、强审计、以 PR 为节奏**的场景下通常足够；不必为「用上工业级编排/消息队列」而引入。

---

## 2. 任务编排器：Dagster vs Prefect

两者都解决：**依赖图、重试、计划执行、可视化、告警**——与「一串 shell/python 顺序调用」相比，多了**状态机、运行历史、参数化分区**。

### 2.1 何时值得考虑

在出现以下**多条**时再评估（单条往往可用 Actions 加强即可）：

- 多条并行 DAG（ingest / 多数据源 / 多环境），且依赖关系**经常变**；
- 需要**按日或按分区回填**（backfill）历史，且要与「资产版本」对齐；
- 同一逻辑要在**开发 / 预发 / 生产**多环境跑，且配置矩阵复杂；
- 团队有**专职数据/平台**能维护编排集群与升级节奏。

### 2.2 Dagster 与 Prefect 对照（简表）

| 维度 | **Dagster** | **Prefect** |
|------|-------------|-------------|
| 心智模型 | **资产（Assets）** 与数据产品优先；适合「数据平台」式治理 | **Flow / Task** 偏 Python 工作流；上手曲线常更平缓 |
| 强项 | 血缘、分区、与 dbt/仓库结构深度整合的常见实践 | 轻量部署、动态流、云/自托管产品成熟 |
| 运维负担 | 通常更重（含 UI、代码位置、存储后端等） | 相对可小步试点（Agent + 云或自建） |
| 与本站 JSON 管道 | 若未来 manifest/快照/沉淀被视作「分区资产」，映射自然 | 把 `run_pipeline_steps.py` 包成 Task 即可渐进迁移 |

**实践建议**：若团队尚无专职运维，**先**用 **Prefect** 做「定时 + 失败告警 + 重试」试点；当出现强 **资产分区 + 跨团队数据契约** 需求时，再评估 **Dagster**。

---

## 3. 事件流：Kafka vs Redpanda

### 3.1 事件流解决什么问题

**消息中间件**适合：**多生产者 / 多消费者**、**异步解耦**、**高吞吐顺序/分区语义**、**可回放日志型事件**。  

本站当前「事件」主要是：**Git 提交、PR 合并、artifact 下载**——本质是 **以仓库为日志**，不需要常驻 broker。

### 3.2 Kafka 与 Redpanda 对照（简表）

| 维度 | **Apache Kafka** | **Redpanda** |
|------|------------------|--------------|
| 协议 | 生态事实标准（大量客户端与运维经验） | **Kafka 协议兼容**，多数客户端可复用 |
| 部署 | 通常 ZooKeeper/KRaft + Broker，组件多 | 常为**单二进制**、资源占用与运维面更小 |
| 适用 | 大规模、多团队、已有 Kafka 运维体系 | 希望 **Kafka 语义** 但降低运维复杂度时 |

**与本站关系**：只有在出现例如「**多服务实时写入候选池**」「**站外多订阅方同时消费同一事件流**」「**毫秒级横向扩展**」时，才值得上 Kafka 系；否则 **Webhook + Queue（如云厂商队列）+ Git** 往往更简单。

---

## 4. 与本仓库的推荐组合（分阶段）

| 阶段 | 编排 | 事件 / 集成 | 说明 |
|------|------|-------------|------|
| **A（默认）** | GitHub Actions + `evolution_pkg.pipeline` | 无独立消息总线 | 保持人审与 Git 真源 |
| **B** | 在 **Prefect**（或 Dagster）中封装现有 Python 步骤 | 仍无 Kafka；失败走邮件/Slack/Issue | 获得 UI、重试、历史运行 |
| **C** | 编排不变或升级 | **仅当** 出现多服务实时写入/多消费者回放需求时引入 **Redpanda/Kafka** | 事件 schema 与 manifest 契约需单独治理 |

**原则**：**不要为了「架构听起来更先进」而同时上编排器 + Kafka**——二者解决不同问题；本站优先保证 **JSON 契约 + validate + 人审** 不被绕开。

---

## 5. 反模式（在本站语境下）

- 用 Kafka 替代 Git 作为**主事实源**（审计与 PR 流程会被削弱）。
- 让编排器**直接写** `evolution-manifest.json`（绕过 `review_state` / merge 闸门）。
- 在单进程、每日一次的分析场景强行上 **多节点 Kafka 集群**（运维成本远大于收益）。

---

## 6. 延伸阅读

- 仓库数据流与闸门：[ARCHITECTURE.md](./ARCHITECTURE.md)
- 技术栈与已实现能力：[TECH_ARCHITECTURE_CAPABILITIES.md](./TECH_ARCHITECTURE_CAPABILITIES.md)
- 双周节奏与命令：[EVOLUTION_RUNBOOK.md](./EVOLUTION_RUNBOOK.md)
