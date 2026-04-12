# Docker 部署说明

与根目录 **[Dockerfile](../Dockerfile)**、**[docker-compose.yml](../docker-compose.yml)**、**[docker-compose.dev.yml](../docker-compose.dev.yml)**、**[docker-compose.kafka-dev.yml](../docker-compose.kafka-dev.yml)**（可选 Kafka 协议 PoC）、**[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)** 一致。默认镜像为 **根目录 MPA**（与 CI **`validate` 默认真源**一致）；**不写 manifest**、不启动抓取管道（仅静态 + 可选只读 API）。

<a id="quickstart"></a>

## 1. 快速开始（MPA 生产）

```bash
docker compose build
docker compose up -d
```

浏览器访问 **http://localhost:8765/**（端口见 `docker-compose.yml` 的 `ports` 映射 `8765:80`）。

- **健康检查**：`web` 服务带 `wget` 探活；`docker compose ps` 可见 `healthy`。  
- **改站后**：须 **`docker compose build --no-cache`** 或 **`docker compose up -d --build`** 重新打镜像（镜像内 `COPY` 全仓上下文）。

<a id="dev-mount"></a>

## 2. 本地开发（挂载仓库，免重建）

```bash
docker compose -f docker-compose.dev.yml up -d
```

将当前目录**只读**挂载到容器 `/www`，改 HTML/CSS/JS 后**刷新浏览器**即可。停止：`docker compose -f docker-compose.dev.yml down`。

<a id="profile-api"></a>

## 3. 只读 API（Compose profile `api`）

与 **[INTEGRATION_AND_READONLY_API.md](./INTEGRATION_AND_READONLY_API.md)** 相同语义：读磁盘已提交 JSON，**CORS/鉴权请在反向代理配置**。

**生产 compose（镜像内数据，与 web 同源 COPY）**：

```bash
docker compose --profile api up -d
```

- 静态站：**http://localhost:8765/**  
- API：**http://localhost:8099/**（`/health`、`/openapi.json`、`/docs` 等）

**开发 compose（API 挂载当前仓库，便于改 JSON 后重启容器或依赖宿主文件）**：

```bash
docker compose -f docker-compose.dev.yml --profile api up -d
```

<a id="profile-admin"></a>

## 3a. 管理端脚手架（Compose profile `admin`）

与 **[ADMIN_WEB_CONSOLE_ROADMAP.md · §8](./ADMIN_WEB_CONSOLE_ROADMAP.md)**、`admin-console/README.md` 一致：**独立 FastAPI**（**8100**），首页为**可视化控制台**（**`static/index.html`**），**不写 manifest**、不提供写 JSON 接口；用于后续接 IdP / RBAC 等。

```bash
docker compose --profile admin up -d --build
```

- 管理端控制台：**http://localhost:8100/**（**`/`** 仪表盘、`/health`、`/docs`、`/api/bootstrap`）  
- 与 **只读 API** 同启：`docker compose --profile api --profile admin up -d`。**`docker-compose.yml`** 已为 **`admin-console`** 默认 **`READONLY_API_BASE_URL=http://readonly-api:8099`**（未设置环境变量时）；仅 **`--profile admin`** 时起 **`api`** 则代理可能 **502**，属预期（见 **`admin-console/README.md`**）。

Makefile：**`make docker-up-admin`**。

常用环境变量（`admin-console` 服务）：

| 变量 | 说明 |
|------|------|
| **`READONLY_API_BASE_URL`** | 默认 **`http://readonly-api:8099`**（与 compose 服务名一致）；显式置空则代理对未配置返回 **503**；仅 admin 无 **api** 时默认仍指向该主机名，可能 **502** |
| **`ADMIN_CORS_ORIGINS`** | 若管理页与 API 不同源，填浏览器来源列表（逗号分隔） |
| **`ADMIN_DEV_BYPASS`** / **`ADMIN_DEV_USER_JSON`** | 仅内网演示 **`/api/me`**；**生产勿开** |
| **`ADMIN_REPO_WEB_BASE`** | 控制台 **`pipeline_links`** 的 Git **blob** 前缀；未设置时默认上游 **`main`**；Fork 改指向本仓；显式空字符串则无 **`href`**（见 **`admin-console/README.md`**） |

单测：仓库根 **`make test-readonly-api`**（**`test_readonly*.py`**；只读 HTTP + 管理端白名单对账）、**`make test-admin-console`**（见 **`admin-console/README.md`**）。若代理 **503**，见 **[§9](#troubleshoot-admin-readonly)**。

<a id="spa-image"></a>

## 4. 全站 SPA 镜像（可选）

1. 在仓库根执行 **`make spa-build`**（生成 **`spa/dist/`**）。  
2. 构建 SPA 镜像：

```bash
docker build -f Dockerfile.spa -t ai-arch-evolution:spa .
```

3. 运行（示例端口 **8776**）：

```bash
docker run --rm -p 8776:80 ai-arch-evolution:spa
```

**`VITE_BASE`**：若站点不在域名根路径，须在 **`make spa-build`** 前按 [spa/README.md](../spa/README.md) 设置 `VITE_BASE`，再打镜像。

<a id="kafka-dev-overlay"></a>

## 4a. 可选：Kafka 协议本地栈（`docker-compose.kafka-dev.yml`）

与 **[ORCHESTRATION_AND_EVENT_STREAMING.md · §3.4](./ORCHESTRATION_AND_EVENT_STREAMING.md#34-本地最小栈本仓库-overlay)** 一致：**独立**于默认站点 Compose，用于 **Redpanda（Kafka 协议兼容）** + **Console** 的本地试验；**不**进入 CI，**不**替代仓库内 Git JSON 真源。

```bash
docker compose -f docker-compose.kafka-dev.yml up -d
# 或：make docker-up-kafka-dev
```

停止：`docker compose -f docker-compose.kafka-dev.yml down` 或 **`make docker-down-kafka-dev`**。

| 宿主机端口 | 用途 |
|------------|------|
| **19092** | Kafka 协议（客户端 `bootstrap.servers=localhost:19092`） |
| **18081** | Schema Registry（HTTP） |
| **18082** | Pandaproxy（HTTP） |
| **19644** | Redpanda Admin API（容器内 9644） |
| **8888** | Redpanda Console → **http://localhost:8888** |

从**本机**连 Broker 用 **`localhost:19092`**；从**同一 Compose 网络内其它容器**连 **`redpanda-0:9092`**。可选 Python 客户端见根目录 **`requirements-kafka-dev.txt`**。

<a id="makefile"></a>

## 5. Makefile 快捷目标

根目录 **`make docker-build`** / **`make docker-up`** / **`make docker-down`** / **`make docker-up-api`** / **`make docker-up-admin`** / **`make docker-up-stack`** / **`make docker-up-kafka-dev`** / **`make docker-down-kafka-dev`**（等价于上述 compose 命令，见 **`make help`**）。**`make docker-build`** 与 **`make docker-up-stack`** 默认 **`COMPOSE_BAKE=false`** 且 **`DOCKER_BUILDKIT=0`**，减轻中文路径下 Buildx/gRPC 报错（见 **[§8](#troubleshoot-bake-grpc)**）。

<a id="ignorefile"></a>

## 6. 构建上下文与 `.dockerignore`

- **`.dockerignore`**：排除 **`.git`**、**`spa/node_modules`**、**`artifacts`** 等；**`docs/`** 下 Markdown **会进入**默认 MPA 镜像，以便站内链到设计文档。  
- **根目录** `README.md` / `CONTRIBUTING.md` / `AGENTS.md` 默认不进镜像（可在浏览器打开仓库页阅读）。

<a id="reverse-proxy"></a>

## 7. 反向代理（生产建议）

典型部署：外层 **Nginx / Caddy / Traefik** 终止 TLS，反代到 `web:80`；若启用 API，再反代 **`/api/` → readonly-api:8099** 并配置 **CORS**、**限流**、**mTLS** 等。API 容器**不**应对公网裸奔。

<a id="troubleshoot-bake-grpc"></a>

## 8. 故障：`x-docker-expose-session-sharedkey` / 非可打印 ASCII（gRPC）

**现象**（节选）：

```text
failed to dial gRPC: ... header key "x-docker-expose-session-sharedkey" contains value with non-printable ASCII characters
```

**常见原因**

1. **项目路径含非 ASCII**（例如中文目录名）。Compose **Bake** 经 **Buildx** 建会话时，路径/会话信息进入 gRPC 头，易触发该限制。  
2. 新版 Docker / Compose 可能仍经 **Buildx** 执行构建；日志里出现 **`[internal] load local bake definitions`** 时，仅设 **`COMPOSE_BAKE=false` 往往不够**，仍会走 gRPC 会话头逻辑。  
3. **`.env` 或环境变量**里混入了不可见字符（BOM、错误换行等）。

**建议按顺序尝试**

1. **同时关闭 Bake 与 BuildKit**（中文路径下最稳；构建较慢）：

```bash
COMPOSE_BAKE=false DOCKER_BUILDKIT=0 docker compose --profile api --profile admin up -d --build
```

仓库根 **Makefile**：**`make docker-up-stack`**、**`make docker-build`** 已包含上述环境变量（**须在仓库根**执行，以便读到根目录 **`docker-compose.yml`**）。根目录 **`.env`** 亦默认写入 **`COMPOSE_BAKE=false`** 与 **`DOCKER_BUILDKIT=0`**，便于直接执行 **`docker compose ...`**（**`.dockerignore`** 已排除 **`.env`**，不会进入镜像上下文）。

2. 若仅想先试 Bake： **`COMPOSE_BAKE=false`**（纯 ASCII 路径上有时已足够）。

3. **路径**：将仓库放在**仅英文路径**下再执行 compose（例如克隆到 `~/works/ai-arch-evolution`），或在该路径建立**纯 ASCII 符号链接**后从链接目录进入；长期使用英文路径可再开 BuildKit（`DOCKER_BUILDKIT=1`）加速构建。

4. **升级与清理**：升级 **Docker Desktop** / **Engine** 与 **Compose** 插件到当前稳定版；必要时执行 **`docker buildx prune -f`** 后重试。

<a id="troubleshoot-admin-readonly"></a>

## 9. 故障：管理端 **`/api/readonly/*`** 返回 **503**（`READONLY_API_BASE_URL not configured`）

**常见原因**：在启动 Compose 的 shell 里执行过 **`export READONLY_API_BASE_URL=`**（空字符串）。Compose 会把该变量传入 **`admin-console`** 容器，覆盖 **`docker-compose.yml`** 中的 **`${READONLY_API_BASE_URL-http://readonly-api:8099}`** 默认（「已设置但为空」不再回退）。

**处理**：

1. 仓库根执行 **`unset READONLY_API_BASE_URL`** 后重新 **`docker compose ... up`**；或  
2. 使用 **`make docker-up-stack`**（会先对**空串** **`unset`** 再 **`up`**）；或  
3. 显式导出非空值，例如 **`export READONLY_API_BASE_URL=http://readonly-api:8099`**。

---

*与主分支同步；新增服务或端口时请更新本节与根目录 README「Docker」段。*
