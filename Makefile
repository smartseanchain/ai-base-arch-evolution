# 可进化站点 · 常用目标（在项目根执行 make <target>）
SHELL := /bin/bash
.PHONY: validate validate-fast clean-pipeline-metrics clean-pipeline-metrics-dry-run clean-overlay-artifacts phase-1 test test-readonly-api test-admin-console merge-ready pre-merge sync-nav check-site-nav ingest ingest-full analyze pipeline evolution-fast check-analysis digest maintainer-roundup ai-overlay ai-overlay-stub help hooks sitemap site-search-index trends status gen-nav-links spa-sync spa-install spa-build spa-preview serve-reader docker-build docker-up docker-down docker-up-api docker-up-admin docker-up-stack docker-up-kafka-dev docker-down-kafka-dev

help:
	@echo "参与贡献 / 合并前自检：见根目录 CONTRIBUTING.md · 整体内容框架：docs/README.md#content-framework · 文档主线表：docs/README.md#docs-spine · 五条架构红线：docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index · PR 证据三联：CONTRIBUTING.md#contributing-pr-evidence-triad"
	@echo "前后台按域：docs/README.md#front-back-modules · 组件×主链：docs/README.md#system-components-fusion · 按改动判型（0c）：docs/README.md#quick-paths"
	@echo "维护者一页收束（枢纽↔注册表↔文档锚点）：maintainer-hub.html#mh-spine-map · #mh-boundaries（系统边界） · #mh-reader-admin-matrix（衔接矩阵） · merge/spa 动线：docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence"
	@echo "整体架构（五维/六域/七类勿混）：docs/PROJECT_ARCHITECTURE_OVERVIEW.md#architecture-grain · 主链/验收入口 §1a · 物理分层 §1b · 模块矩阵 docs/MODULE_INVENTORY_AND_ARCHITECTURE_UPGRADE_MATRIX.md"
	@echo "改 scripts/evolution-registry.json 后：make sync-nav（maintainer-hub 五链后三锚由 sync_site_nav·build_skip_bar 生成，勿手改 HTML）；维护 SPA 须 spa/nav.config.json 与 pages 一致 + make gen-nav-links 或 make spa-build（见 docs/PROJECT §1a · CONTRIBUTING 常见变更）"
	@echo "按阶段升级（编排/Kafka/生产库前对表）：docs/PHASED_UPGRADE_EXECUTION_GUIDE.md · 决策全景：docs/ARCHITECTURE_UPGRADE_ROADMAP.md §1"
	@echo "make phase-1    - 等同 make validate（阶段 1 站内增强主验收；见 PHASED#phase-1）"
	@echo "make validate     - bash scripts/run_validate.sh（须先 pip install -r requirements.txt）；与 pre-commit 一致"
	@echo "make validate-fast - 轻量子集（compileall + 核心 JSON/nav/单测 + analysis --check + 快照/遥测/overlay Schema）；CI/pre-commit 不跑；合并前仍须 validate"
	@echo "make clean-pipeline-metrics - 删除 artifacts/pipeline-metrics-*.json（旧遥测；gitignore；见 EVOLUTION_RUNBOOK）"
	@echo "make clean-pipeline-metrics-dry-run - 仅列出将删除的 pipeline-metrics 文件（不删除）"
	@echo "make clean-overlay-artifacts - 删除 artifacts/ai-overlay-step.json 与 ai-overlay-llm-dead-letter.txt（若存在）"
	@echo "make merge-ready / make pre-merge - validate + test-readonly-api + test-admin-console（推荐合并前；见 CONTRIBUTING / MERGE 清单）"
	@echo "make test       - registry Schema + unittest + navLinks + 沉淀/趋势 Schema + 可选 ai-overlay-step / ai-analysis-overlay Schema"
	@echo "make test-readonly-api - pip 安装 requirements + requirements-api 后跑 test_readonly*.py（HTTP 契约 + 管理端白名单对账）"
	@echo "make test-admin-console - pip 安装 admin-console/requirements.txt 后跑 admin-console 烟测"
	@echo "make sync-nav   - 按 partials 写回各页 skip-bar + site-nav；maintainer-hub 另拼 #mh-*（build_skip_bar）；改 partials 后建议 make sync-nav → make validate，并手调 404.html（见 docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence）"
	@echo "make check-site-nav - 仅检查顶栏是否与模板一致（CI 同款）"
	@echo "make check-analysis - 分析引擎 --check（不写 snapshot，CI 同款）"
	@echo "make ingest     - 仅抓取候选（需外网）"
	@echo "make ingest-full - 同 ingest 但 --full-pool（忽略 require_route_match）"
	@echo "make analyze    - 校验 + 分析引擎 + 沉淀 + 趋势（无抓取）；默认写 artifacts/pipeline-metrics-*.json"
	@echo "                  可选 SKIP_PIPELINE_TELEMETRY=1 make analyze 跳过遥测"
	@echo "make evolution-fast - 仅刷新快照/沉淀/趋势（须先 make validate）；遥测同上"
	@echo "make trends     - 仅跑 sediment_trends.py（依赖已有沉淀）"
	@echo "make status     - site-meta + 可选 overlay 侧车行 + analysis-snapshot 核心计数（无快照则提示 analyze）"
	@echo "make digest     - Markdown 进化摘要（快照 + 可选趋势/沉淀；无 LLM，便于贴 PR）"
	@echo "make maintainer-roundup - status + digest（维护者贴 PR 前快速一条）"
	@echo "make ai-overlay-stub - 写入 assets/ai-analysis-overlay.json 占位（须已有快照）"
	@echo "make ai-overlay - 按 AI_OVERLAY_ENABLE / API 环境变量可选生成 overlay（见 docs/AI_ASSISTED_ANALYSIS_LAYER.md）"
	@echo "make pipeline   - 同 analyze"
	@echo "make hooks      - 安装 Git 钩子（pre-commit 等同 make validate）"
	@echo "make sitemap    - 需 SITE_BASE=https://... 生成 sitemap.xml"
	@echo "make site-search-index - 由 registry pages + 各页 <title> 生成 assets/site-search-index.json（可选；不入 validate）"
	@echo "make gen-nav-links - 由 spa/nav.config.json 生成 spa/src/navLinks.ts（增删注册页后先跑）"
	@echo "make spa-sync   - 同步根目录 HTML/assets/docs → spa/public（供全站 SPA）；merge/双轨见 docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix"
	@echo "make spa-build  - gen-nav-links + spa-sync + npm ci + vite build（产物 spa/dist，含 404 回退）；MERGE §1 · partials 手顺 · 关系视图（docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map）"
	@echo "make spa-preview - 预览 spa 构建（默认端口见终端）"
	@echo "make serve-reader - 本机起静态服务读 MPA（127.0.0.1:8000；见 README 读者站排障）"
	@echo "make docker-build - docker compose build（MPA 镜像）"
	@echo "make docker-up    - docker compose up -d（默认仅 web:8765）"
	@echo "make docker-up-api - docker compose --profile api up -d（web + 只读 API:8099）"
	@echo "make docker-up-admin - docker compose --profile admin up -d（管理端脚手架:8100）"
	@echo "make docker-up-stack - web+api+admin 一次起（COMPOSE_BAKE=false + DOCKER_BUILDKIT=0；空 READONLY_API_BASE_URL 会先 unset 以用 compose 默认；见 docs/DOCKER.md）"
	@echo "make docker-down  - docker compose down"
	@echo "make docker-up-kafka-dev - 可选 Redpanda+Console（Kafka 协议 PoC；见 docker-compose.kafka-dev.yml、docs/ORCHESTRATION）"
	@echo "make docker-down-kafka-dev - 停止上述 Kafka-dev 栈"

validate:
	bash scripts/run_validate.sh

validate-fast:
	bash scripts/run_validate_fast.sh

clean-pipeline-metrics-dry-run:
	@ad="$(CURDIR)/artifacts"; \
	if [ ! -d "$$ad" ]; then echo "OK: dry-run · 0 files（无 artifacts 目录）" >&2; exit 0; fi; \
	find "$$ad" -maxdepth 1 -name 'pipeline-metrics-*.json' -type f 2>/dev/null | sort | sed 's/^/would remove: /'; \
	n=$$(find "$$ad" -maxdepth 1 -name 'pipeline-metrics-*.json' -type f 2>/dev/null | wc -l | tr -d '[:space:]'); \
	echo "OK: dry-run · $$n file(s)（未删除；make clean-pipeline-metrics 删除）" >&2

clean-pipeline-metrics:
	@rm -f "$(CURDIR)"/artifacts/pipeline-metrics-*.json
	@echo "OK: 已删除 artifacts/pipeline-metrics-*.json（若存在；见 docs/EVOLUTION_RUNBOOK.md）" >&2

clean-overlay-artifacts:
	@rm -f "$(CURDIR)"/artifacts/ai-overlay-step.json "$(CURDIR)"/artifacts/ai-overlay-llm-dead-letter.txt
	@echo "OK: 已删除 ai-overlay 侧车 / dead-letter（若存在；见 docs/DATA_CONTRACTS.md#pipeline-telemetry）" >&2

phase-1: validate
	@echo "OK: phase-1 gate（与 validate 同源）· docs/PHASED_UPGRADE_EXECUTION_GUIDE.md#phase-1"

sync-nav:
	python3 scripts/sync_site_nav.py

check-site-nav:
	python3 scripts/sync_site_nav.py --check

test:
	python3 scripts/validate_evolution_registry_schema.py
	PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v
	python3 scripts/check_nav_links_registry.py
	python3 scripts/validate_sediment_artifacts_schema.py
	python3 scripts/validate_ai_overlay_step_schema.py
	python3 scripts/validate_ai_analysis_overlay_schema.py

test-readonly-api:
	python3 -m pip install -r requirements.txt -r requirements-api.txt
	PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_readonly*.py' -v

test-admin-console:
	python3 -m pip install -r admin-console/requirements.txt
	cd admin-console && PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_*.py' -v

merge-ready: validate
	$(MAKE) test-readonly-api
	$(MAKE) test-admin-console

# 与 merge-ready 同义，便于记忆「合并前一条命令」
pre-merge: merge-ready
	@:

check-analysis:
	python3 scripts/analysis_engine.py --check

hooks:
	bash scripts/install-git-hooks.sh

sitemap:
	@test -n "$${SITE_BASE:-}" || (echo '用法: SITE_BASE=https://example.org make sitemap' >&2; exit 1)
	SITE_BASE="$${SITE_BASE}" python3 scripts/gen-sitemap.py

site-search-index:
	PYTHONPATH=scripts python3 scripts/gen_site_search_index.py

ingest:
	bash scripts/run_ingest_only.sh

ingest-full:
	python3 scripts/ingest_opinion_law.py --full-pool
	python3 scripts/validate-evolution-candidates.py

analyze pipeline:
	bash scripts/run_update_pipeline.sh

evolution-fast:
	@echo >&2 "[evolution-fast] 跳过 manifest/漂移/单测/顶栏；若未先跑 make validate 请勿提交。" >&2
	bash scripts/run_analyze_write.sh

trends:
	python3 scripts/sediment_trends.py

status:
	python3 scripts/print_evolution_status.py

digest:
	python3 scripts/evolution_intelligence_digest.py

maintainer-roundup: status digest
	@echo "OK: maintainer-roundup（status + digest）" >&2

ai-overlay-stub:
	python3 scripts/write_ai_analysis_overlay.py --stub

ai-overlay:
	@echo "提示: 须 AI_OVERLAY_ENABLE=1 与 API 环境变量；默认 analyze 已静默跳过本步 — docs/AI_ASSISTED_ANALYSIS_LAYER.md" >&2
	python3 scripts/write_ai_analysis_overlay.py

gen-nav-links:
	python3 scripts/gen_nav_links_ts.py --write

# 改根 *.html / docs / sync 输入后维护 SPA iframe 与 public/docs 时须跑；动线 docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix
spa-sync:
	python3 scripts/sync_spa_public.py

spa-install:
	cd spa && npm ci

spa-build: gen-nav-links spa-sync
	cd spa && npm ci && npm run build

spa-preview:
	cd spa && npm run preview

# 读者站（根目录 MPA）：须 http(s) 才能 fetch JSON；端口 8000 与 compose web 8765 错开
serve-reader:
	@echo "读者站（MPA）：http://127.0.0.1:8000/  （Ctrl+C 停止）"
	cd "$(CURDIR)" && python3 -m http.server 8000 --bind 127.0.0.1

# Compose 在部分版本下即使用 COMPOSE_BAKE=false 仍可能走 Buildx（日志仍见 load local bake definitions）；
# 中文路径会触发 x-docker-expose-session-* gRPC 头错误，故构建类命令默认关 BuildKit（见 docs/DOCKER.md §8）。
docker-build:
	COMPOSE_BAKE=false DOCKER_BUILDKIT=0 docker compose build

docker-up:
	COMPOSE_BAKE=false docker compose up -d

docker-up-api:
	COMPOSE_BAKE=false docker compose --profile api up -d

docker-up-admin:
	COMPOSE_BAKE=false docker compose --profile admin up -d

# 若 shell 里 ``export READONLY_API_BASE_URL=``（空串），Compose 会传入空值覆盖 yaml 默认；先 unset 再 up。
docker-up-stack:
	bash -c 'if [ "$${READONLY_API_BASE_URL+x}" = "x" ] && [ -z "$$READONLY_API_BASE_URL" ]; then unset READONLY_API_BASE_URL; fi; \
		COMPOSE_BAKE=false DOCKER_BUILDKIT=0 docker compose --profile api --profile admin up -d --build'

docker-down:
	docker compose down

docker-up-kafka-dev:
	docker compose -f docker-compose.kafka-dev.yml up -d

docker-down-kafka-dev:
	docker compose -f docker-compose.kafka-dev.yml down
