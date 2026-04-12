# 管理端 Web 化扩展路线图：登录、用户与审核

本文在不变量之内，**依次**梳理若将「后端管理」从 **CLI + PR + 文档链** 演进为 **带登录的管理 Web** 时，各能力应如何分层、与 Git 真源及人审闸门如何对齐。**非采购清单**、非当前实现契约；落地前须同步 **[DATA_CONTRACTS](./DATA_CONTRACTS.md)**、**[INTEGRATION_AND_READONLY_API](./INTEGRATION_AND_READONLY_API.md)**、**[USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)** 与 **[PLATFORM_EXTENSIBILITY](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md)**。

**当前 `admin-console` 实现与 HTTP/UI 对表**（是否符合阶段 0 预期）：**[ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md](./ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md)**。**读者面三源呈现 + 管理 Web 四可**的用语与表：**[USER_ADMIN_SPLIT · §1c](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#front-three-sources)**。

**硬边界（与 [AGENTS.md](../AGENTS.md)、[PLATFORM · 不变量](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#invariants) 一致）**：

- **不**设计或默认实现「管理页一键写入已审 **`evolution-manifest.json`**」或绕过 **`review_state`** / **`merge_candidates_to_manifest.py`** 的审计语义。  
- **分析引擎不写 HTML**；管理 UI 若展示分析结果，仍只消费已提交 JSON 或只读 API。  
- **Git + PR** 仍为**事实与审计主轴**；Web 管理台是**体验与门禁层**，替代不了 merge 的可 diff 记录，除非另立**显式第二真源**并在文档中命名（不推荐轻率引入）。

**读者面 / 管理面分拆**真源叙述：**[USER_ADMIN_SPLIT · 节 1a](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)**。**六域协同**中与本路线图最相关：**治理**、**运维**、**数据**。**智能化边界**：[§1.1](./PLATFORM_EXTENSIBILITY_AND_EVOLUTION.md#automation-and-evolution)。

**管道 UI、数据源与「自动拉取 → 沉淀分析」**（模块迁移矩阵、配置真源、作业执行者分层）：**[ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)**。

---

<a id="layer-1-authn"></a>

## 1. 身份认证（用户登录）

| 子主题 | 建议内容 | 与现状关系 |
|--------|----------|------------|
| **1.1 目标** | 仅**管理端**（独立子域 / 内网路径 / 独立部署单元）要求登录；**读者面 MPA/SPA** 可保持匿名或仅「可选账号」用于个性化（若需要再分轨）。 | 当前静态站无登录；新增须**物理或路由隔离**，避免与公共 CDN 混同一 Cookie 域。 |
| **1.2 身份源（IdP）** | 优先 **OIDC / SAML 2.0** 对接企业 IdP（Azure AD、Okta、Keycloak 等）或 **GitHub OAuth**（小团队）；避免在业务库里自建「唯一长期密码表」为唯一方案。 | 与「审计要落到谁」一致：IdP 日志 + 应用审计双份。 |
| **1.3 会话形态** | **BFF（Backend-for-Frontend）+ HttpOnly Cookie** 或 **短期 Access Token + Refresh**；管理 API **须 HTTPS**、**防 CSRF**（若 Cookie 会话）。 | **`readonly_api`** 今日无会话；新管理 API 为**另一服务**或同进程**挂载在 `/admin` 下受鉴权路由**（实现阶段再定），不在本文锁技术栈。 |
| **1.4 最小可行（阶段 1）** | 单租户、固定白名单组（OIDC `groups` / `roles` claim）即可区分「能否进管理台」。 | 与 **[DOCKER](./DOCKER.md)** 编排：管理容器与只读 API 分端口或分服务，网关统一 TLS。 |

**展开要点**：登录只解决「你是谁」；**授权（能做什么）**见第 2 节；**审核（业务是否通过）**见第 3 节——三者勿混为一谈。

---

<a id="layer-2-authz-users"></a>

## 2. 用户管理与授权（RBAC / ABAC）

| 子主题 | 建议内容 | 与仓库闸门关系 |
|--------|----------|----------------|
| **2.1 角色模型（RBAC）** | 建议粗粒度起步：**`admin`**（系统与集成配置）、**`curator`**（候选/manifest 流程与规则 JSON）、**`analyst`**（触发分析/管道只读重跑）、**`viewer`**（只看板与日志）。 | 角色**不**等价于 **`review_state`**；后者仍是**数据字段**，见 [DATA_CONTRACTS](./DATA_CONTRACTS.md)。 |
| **2.2 用户生命周期** | 邀请、禁用、强退会话、API Token 轮换（机器用户）：走 IdP 或 BFF 管理表；**审计日志**记录操作者 id、时间、对象。 | 人审合并仍建议 **PR + 本地脚本** 为默认；Web 上「点通过」若存在，须生成**可引用事件 id** 并**可回放到 Git 提交**（见第 4 节）。 |
| **2.3 与 GitHub 分工** | 若团队已用 GitHub **CODEOWNERS**、**branch protection**，管理台可**展示** PR 状态，**不重复**实现整套代码评审。 | 减少「第二套审批系统」漂移。 |
| **2.4 权限与 JSON 真源** | **写** `assets/*.json` / `scripts/*.json`：**仅** `curator` + 二次确认 + 与 CI 相同校验链（或提交为 PR）；**禁止**低权限角色直接写 manifest。 | 与 **[MERGE_AND_RELEASE_CHECKLIST](./MERGE_AND_RELEASE_CHECKLIST.md)** 对齐。 |

---

<a id="layer-3-review-workflow"></a>

## 3. 审核与工作流（业务「过不过」）

| 子主题 | 建议内容 | 与现有一致化 |
|--------|----------|--------------|
| **3.1 审核对象分层** | 与 [USER_ADMIN · L0—L5](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#governance-review) 对齐：**L1 候选**、**L2 manifest**、**L3 规则闭环**、**L4 发布叙事**、**L5 分析血缘**。管理 UI 按层展示队列与过滤器。 | 字段语义仍以 **DATA_CONTRACTS** 为准。 |
| **3.2 候选审核（L1）** | 展示 `evolution-candidates.json` 条目、改 **`review_state`**（pending / noise / **queued_for_manifest** 等）的**拟议变更**；落盘方式优先：**导出 patch / 开 PR**，而非生产库直连写（除非内网工具且仍有 Git 镜像）。 | 与 **`merge_candidates_to_manifest`** 前置条件一致。 |
| **3.3 manifest 入库（L2）** | **默认路径**：维护者在本地或 CI 信任环境执行 **`merge_candidates_to_manifest`**，再 **PR**。可选增强：管理台发起「合并请求」→ 后台生成 **artifact / 分支** → 仍经 **PR + `make validate`**。 | **不**将「合并进 manifest」做成无日志的按钮写生产分支。 |
| **3.4 规则与闭环（L3）** | 编辑 **`evolution-hint-rules.json`**、登记 **`evolution-hint-decisions.json`**：宜走 **PR** 或「提案 JSON + 审批流生成 PR」。 | 保持 **`rule_id`** 可审计。 |
| **3.5 工作流引擎（可选）** | 若需多步审批链（「数据管家 → 编辑负责人」），优先 **状态机 + 审计表**（Who/when/what），与 **Git 提交**建立引用键（commit / PR / artifact id）。 | 与 [ORCHESTRATION](./ORCHESTRATION_AND_EVENT_STREAMING.md) 阶段 2 区分：那是**管道 DAG**，不是业务审批替代 Git。 |

---

<a id="layer-4-data-git-audit"></a>

## 4. 数据真源、Git 审计与「写路径」

| 子主题 | 建议内容 |
|--------|----------|
| **4.1 单一真源** | 结构化事实仍以 **Git 内路径** 为真源；管理台为**投影**或**暂存（staging）+ PR**。 |
| **4.2 写路径分类** | **A**：只读展示（拉 **`readonly_api`** 或读部署快照）；**B**：提交变更 → **PR**（推荐）；**C**：特权直连写（仅.break-glass 流程 + 双人复核 + 事后审计）。 |
| **4.3 与 `readonly_api` 关系** | 今日 API **只读**；若管理台需「服务端代写 Git」，应 **独立服务**（带鉴权、审计），**不**混在 `readonly_api` 进程语义里，避免「只读」名实不符。见 [INTEGRATION](./INTEGRATION_AND_READONLY_API.md)。 |
| **4.4 审计字段** | 每次通过管理台触发的变更，建议记录：`actor_sub`、`action`、`target_path`、`before_hash`、`after_hash`、`correlation_id`、关联 **PR 或 run_id**。 |

---

<a id="layer-5-ops-sec"></a>

## 5. 运维、安全与合规（横切）

| 子主题 | 建议内容 |
|--------|----------|
| **5.1 部署** | 管理台与读者站 **分域名或前缀路径**；**TLS 终止**在网关；**安全头**（CSP、HSTS）。参见 [DOCKER](./DOCKER.md)、[INTEGRATION · CORS/鉴权](./INTEGRATION_AND_READONLY_API.md)。 |
| **5.2 密钥** | IdP Client Secret、Webhook、集成 Token：**环境变量 / 密钥管理器**；**不入库**。 |
| **5.3 备份与恢复** | 若引入管理库（审批状态表）：须备份策略与 **与 Git 对账** 的修复剧本。 |
| **5.4 六域落点** | **治理**：角色、审批、不变量；**运维**：部署、日志、密钥；**数据**：Schema、真源路径；**管道/分析**：仅「触发/只读」入口，不降级闸门。 |

---

<a id="phasing"></a>

## 6. 分阶段落地建议（与阶段 0—3 对表）

| 阶段 | 管理端能力范围 | 读者面影响 |
|------|----------------|------------|
| **0（现状）** | CLI、PR、Actions artifact、**maintainer-hub** 文档链 | 无登录；无改 |
| **1** | **只读**管理看板（OIDC 登录 + **`readonly_api`** + 链接回 GitHub PR/Issue） | 仍无写；可选展示 `site_version` / `run_id` |
| **2** | **提案式写**：表单 → 生成 JSON diff / 开分支 PR → **`make validate` 在 PR 上必过** | 读者仍只消费合并后的静态/json |
| **3（慎选）** | 特权路径直连写 Git（强审计、双人、熔断） | 仅组织成熟且合规要求明确时 |

与 [ARCHITECTURE_UPGRADE · 阶段](./ARCHITECTURE_UPGRADE_AND_EXTENSIONS.md#upgrade-tiers) 一致：**不必跳级**；阶段 1 尽量用满 **只读 API + IdP** 再评估阶段 2。

---

<a id="checklist-anti"></a>

## 7. 能力扩展检查单与反模式

**合并前自检（管理端相关 PR）**：

1. 是否新增**写** JSON 路径？→ 是否仍经 **PR + `make validate`** 或等价闸门。  
2. 是否弱化 **`review_state`** 语义？→ 与 **`merge_candidates_to_manifest`** 文档对表。  
3. 是否把 **`readonly_api`** 扩展成写接口？→ **禁止**；应新服务名与契约。  
4. 登录与会话：是否有 **CSRF/XSS/会话固定** 评审？  
5. 是否更新 **[USER_ADMIN_SPLIT](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md)** 本节互链与 [MERGE 清单](./MERGE_AND_RELEASE_CHECKLIST.md)。

**反模式**：

- 管理页直接写生产 **`evolution-manifest.json`** 且无 PR。  
- 用审批工作流**替代** Git 作为**唯一**审计源。  
- 与读者站**同 Cookie 域**混用高权限会话。  
- 「先上线 UI 再补审计」导致无法回答「谁在何时改了哪条候选」。

---

<a id="scaffold-implementation"></a>

## 8. 当前仓库内落地（脚手架）

| 项 | 说明 |
|----|------|
| **目录** | **`admin-console/`**（FastAPI **`app/main.py`**、静态 **`static/index.html`**、**`Dockerfile`**） |
| **运行** | 见 **`admin-console/README.md`**；Compose：**`docker compose --profile admin up -d`** 或 **`make docker-up-admin`** → **http://localhost:8100/** |
| **能力** | **`GET /health`**、**`GET /api/me`**（匿名或 **`ADMIN_DEV_BYPASS`** 演示用户）、**`GET /api/bootstrap`**、**`GET /api/readonly/{segment}`**（只读 API **GET** 白名单代理；含 **`registry`**、**`candidates`**（敏感）、**`hint-decisions`**（宜受控）、**`hint-rules`**、**`maps-to-hints`**、**`ingest-config`** 等与 **`readonly_api`** 对齐的单段路径；**`snapshot-history`** 转发 **`limit`** / **`offset`** 查询参数）、**`GET /api/readonly/snapshot-history/{run_id}`**（**`run_id`** 字符白名单）、**`GET /`** 可视化控制台（**`static/index.html`**）、**`/docs`** / **`/openapi.json`** |
| **CORS** | 环境变量 **`ADMIN_CORS_ORIGINS`**（逗号分隔）；未设则不加跨域中间件 |
| **闸门** | 与上文硬边界一致：**不提供**写 manifest、写候选 JSON 或绕过 **`review_state`** 的接口；代理仅白名单单段路径 |
| **校验** | **`make validate`** → **`compileall admin-console/app`**；**`make test-admin-console`** → 烟测（需安装 **`admin-console/requirements.txt`**） |

与 **`readonly-api`** 同栈时，可导出 **`READONLY_API_BASE_URL=http://readonly-api:8099`** 再 **`docker compose --profile api --profile admin up -d`**，便于后续管理前端对接只读 API。

---

## 延伸阅读

- [USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md) · [节 1a · 前端读者 · 后端管理](./USER_ADMIN_SPLIT_AND_EVOLUTION_DESIGN.md#reader-frontend-admin-backend)  
- [INTELLIGENCE_SIX_DOMAINS.md](./INTELLIGENCE_SIX_DOMAINS.md)  
- [INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md) · [扩展只读路由](./INTEGRATION_AND_READONLY_API.md#extend-readonly-routes)  
- [ORCHESTRATION_AND_EVENT_STREAMING.md](./ORCHESTRATION_AND_EVENT_STREAMING.md)  
- [MERGE_AND_RELEASE_CHECKLIST.md](./MERGE_AND_RELEASE_CHECKLIST.md)  
- [docs/README · 文档主线](./README.md#docs-spine)  
- [ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)（**管道 UI · 数据源 · 沉淀分析链**）

---

*随主分支迭代；扩展认证或写路径时同步更新 §8 与 **[DOCKER.md](./DOCKER.md)**、**[INTEGRATION](./INTEGRATION_AND_READONLY_API.md)**、**[ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION](./ADMIN_PIPELINE_UI_AND_DATA_SOURCE_MIGRATION.md)**。*
