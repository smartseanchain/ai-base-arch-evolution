# 管理端 Web 控制台（脚手架）

与 **[docs/ADMIN_WEB_CONSOLE_ROADMAP.md](../docs/ADMIN_WEB_CONSOLE_ROADMAP.md)** 配套的可运行落地：独立 **FastAPI**，**不写 manifest**、不提供写 JSON 接口。**`/api/readonly/*`** 在进程内复用单个 **`httpx.Client`**（连接池，超时 30s）；单测可 patch **`app.main._shared_httpx_client`**。

**整体框架与预期边界（评审用）**：[docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md](../docs/ADMIN_CONSOLE_FRAMEWORK_OVERVIEW.md)。

**`GET /`** 为单页 **Web 控制台**（暗色主题）：运行时摘要、身份卡片、快照历史表、只读片段探索器（同源代理）；无前端构建链。

首页 **「数据源参考目录」**：浏览器侧勾选关注项保存在 **localStorage**；外链在**新标签**打开，供个人正常阅读或 RSS 阅读器使用。与 **`ingest-config`** 可对账显示「在 ingest」；**「复制勾选 RSS 为 ingest 草案片段」** 将勾选且含订阅 URL 的条目导出为 **`rss_feeds` 形状 JSON**（剪贴板）。同卡下方 **「HTTPS JSON 侧车（json_feeds）」** 用表单维护另一份 **localStorage** 草稿（`id`、**https** `url`、`items_path`、`max_items`、`default_kind`、可选逗号分隔键序），**「复制 json_feeds 草案片段」** 导出可合并 JSON；**「复制完整 ingest_config 预览」** 在已拉取 **`ingest-config`** 时深拷贝后同时追加：**(1)** 数据源目录**已勾选**且不在仓库的 **`rss_feeds`** 条目（与「复制勾选 RSS」同一规则）；**(2)** **`json_feeds`** 草稿新项。根级含 **`_preview_comment`**（合并说明，入库前删除）。未拉取时仅输出含占位 **`notes` / 空数组** 的骨架并提示先配置只读基址并刷新。若 **`ingest-config`** 已含相同 **`id` 或 URL**，会列入 **`omitted_already_in_ingest`**。若只读 **`ingest-config`** 已拉取，与仓库配置**重复**的 RSS 勾选项同样进入 **`omitted_already_in_ingest`**。须**手工合并**进 **`scripts/ingest_config.json`** 并经 **PR**；纳入自动抓取仍以 **`make validate`** 对账为准。

**「控制面能力」**：自 **`admin-console/data/control_plane_roadmap.json`** 经 bootstrap 下发，用表格对照**市面分析/治理后台**常见模块（数据源、策略、审批、发布）与**本仓阶段 0—3**及不变量；仅叙事与链接，**不**新增写接口。

## 能力一览

| 路径 | 作用 |
|------|------|
| **`GET /`** | **可视化控制台**（请求 **`/api/bootstrap`**、**`/api/me`**、**`/api/readonly/*`**） |
| **`GET /health`** | 存活与配置摘要 |
| **`GET /api/me`** | 身份占位；生产接 IdP 前为匿名 |
| **`GET /api/bootstrap`** | 前端引导：只读 API 基址、代理白名单片段、**`pipeline_links`**、**`pipeline_cli_hints`**、**`github_actions_href`**、**`pipeline_workflows`**、**`data_source_catalog`**、**`control_plane_roadmap`**（自 **`admin-console/data/*.json`**；**不**由服务端请求外网、**不**写 manifest）、**`admin_accounts_enabled`**（是否配置了管理员账户 API 密钥）等 |
| **`GET/PATCH/DELETE /api/admin/accounts`**、**`POST /api/admin/accounts`** | **管理员账户**（JSON 文件持久化 + **bcrypt** 密码哈希）。须设置 **`ADMIN_ACCOUNTS_API_SECRET`**；请求头 **`X-Admin-Accounts-Secret`** 或 **`Authorization: Bearer <同一密钥>`**。未配置密钥时返回 **503**。数据文件默认 **`data/admin_accounts.json`**（见 **`.gitignore`**，可参考 **`data/admin_accounts.example.json`**） |
| **`GET /api/readonly/{segment}`** | **受控 GET 代理** → `READONLY_API_BASE_URL/{segment}`（白名单见 bootstrap，与 **`readonly_api`** 单段路径一致，如 **`registry`**、**`ingest-config`**、**`candidates`** 等）；**`snapshot-history`** 会转发 **`limit`** / **`offset`** |
| **`GET /api/readonly/snapshot-history/{run_id}`** | 代理单条历史快照；**`run_id`** 仅允许 `[A-Za-z0-9._-]` |
| **`GET /docs`** · **`/openapi.json`** | OpenAPI |

## 环境变量

| 变量 | 说明 |
|------|------|
| **`READONLY_API_BASE_URL`** | 根目录 **`docker-compose.yml`** 默认 **`http://readonly-api:8099`**（与 **`readonly-api`** 服务名一致）；本地 **`uvicorn`** 须自行设为 **`http://127.0.0.1:8099`** 等；未配置（空字符串）时代理 **503** |
| **`ADMIN_CORS_ORIGINS`** | 逗号分隔允许来源（如 `http://localhost:8100,http://127.0.0.1:5173`）；空则不加 CORS 中间件 |
| **`ADMIN_DEV_BYPASS`** | 设为 `1` / `true` / `yes` 时启用下方演示用户（**仅本地/内网**） |
| **`ADMIN_DEV_USER_JSON`** | 与 **`ADMIN_DEV_BYPASS`** 联用：JSON 对象合并进 **`/api/me`**（如 `{"sub":"alice","roles":["curator"]}`） |
| **`ADMIN_REPO_WEB_BASE`** | GitHub/GitLab **blob** 视图前缀（无尾 **`/`** 亦可），形如 **`https://github.com/org/repo/blob/main`**；用于 **`/api/bootstrap`** 的 **`pipeline_links[].href`**。未设置环境变量时默认指向上游公开仓 **`smartseanchain/ai-base-arch-evolution`** 的 **`main`**；**Fork 或内网 Forge** 请设为本仓对应前缀。**显式置空**（`ADMIN_REPO_WEB_BASE=`）则 **`href`** 为空，控制台仍列出相对 **`path`**（无出站外链） |
| **`ADMIN_ACCOUNTS_API_SECRET`** | 非空时启用 **`/api/admin/accounts`** 的列表/创建/更新/删除。请使用足够长的随机串；**勿**提交仓库或与 **`ADMIN_DEV_BYPASS`** 混为「生产认证」 |
| **`ADMIN_ACCOUNTS_FILE`** | 账户 JSON 路径；默认 **`data/admin_accounts.json`**（相对 **`admin-console/`** 根）。可设为绝对路径 |

**安全**：**勿**在生产环境开启 **`ADMIN_DEV_BYPASS`**。管理员账户 API 仅依赖共享密钥，适合内网或过渡阶段；对外暴露时请置于 **TLS + 网络策略** 之后，并规划 **OIDC**（见路线图）。

**审计**：创建 / 更新 / 删除管理员账户及鉴权失败（错误密钥）时，进程会向 logger **`admin_console.admin_accounts`** 输出**单行 JSON**（`event`、`ts`、`user_id`、`username` 等），**不含**密码与 API 密钥；便于接入集中日志。生产请配置日志驱动/级别，避免默认吞掉 **INFO**。

**Docker**：若 **`/api/readonly/*`** 报 **503** 且 health 正常，多为 shell 里 **`READONLY_API_BASE_URL=`** 空导出覆盖了 compose 默认，见 **[docs/DOCKER.md §9](../docs/DOCKER.md#troubleshoot-admin-readonly)**；可用 **`make docker-up-stack`** 规避。

## 本地运行（不依赖 Docker）

仓库根：

```bash
python3 -m venv .venv-admin && . .venv-admin/bin/activate
pip install -r admin-console/requirements.txt
cd admin-console && PYTHONPATH=. uvicorn app.main:app --reload --port 8100
```

可选（与只读 API 同机调试代理）：

```bash
export READONLY_API_BASE_URL=http://127.0.0.1:8099
# 另开终端：PYTHONPATH=scripts python3 -m uvicorn readonly_api:app --port 8099
```

浏览器：<http://127.0.0.1:8100/> · <http://127.0.0.1:8100/health> · <http://127.0.0.1:8100/docs>

## 单测

仓库根（会安装 **`admin-console/requirements.txt`**）：

```bash
make test-admin-console
```

## Docker Compose（profile `admin`）

根目录：

```bash
docker compose --profile admin up -d --build
```

默认端口 **8100**。与只读 API 同栈时：

```bash
export READONLY_API_BASE_URL=http://readonly-api:8099
docker compose --profile api --profile admin up -d --build
```

Makefile：**`make docker-up-admin`**（见根目录 **`make help`**）。编排说明：**[docs/DOCKER.md#profile-admin](../docs/DOCKER.md#profile-admin)**。

## 校验

根目录 **`make validate`** 对 **`admin-console/app`** 执行 **`compileall`**（语法闸门）。
