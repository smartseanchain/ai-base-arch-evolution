# 可进化站点 · 常用目标（在项目根执行 make <target>）
.PHONY: validate phase-1 test test-readonly-api test-admin-console merge-ready pre-merge sync-nav check-site-nav ingest ingest-full analyze pipeline evolution-fast check-analysis help hooks sitemap trends status gen-nav-links spa-sync spa-install spa-build spa-preview docker-build docker-up docker-down docker-up-api docker-up-admin docker-up-stack docker-up-kafka-dev docker-down-kafka-dev

help:
	@echo "参与贡献 / 合并前自检：见根目录 CONTRIBUTING.md · 文档主线表：docs/README.md#docs-spine"
	@echo "按阶段升级（编排/Kafka/生产库前对表）：docs/PHASED_UPGRADE_EXECUTION_GUIDE.md · 决策全景：docs/ARCHITECTURE_UPGRADE_ROADMAP.md §1"
	@echo "make phase-1    - 等同 make validate（阶段 1 站内增强主验收；见 PHASED#phase-1）"
	@echo "make validate   - bash scripts/run_validate.sh（须先 pip install -r requirements.txt）；与 pre-commit 一致"
	@echo "make merge-ready / make pre-merge - validate + test-readonly-api + test-admin-console（推荐合并前；见 CONTRIBUTING / MERGE 清单）"
	@echo "make test       - registry Schema + unittest + navLinks + 沉淀/趋势 Schema + 可选 ai-overlay Schema"
	@echo "make test-readonly-api - pip 安装 requirements + requirements-api 后跑 test_readonly*.py（HTTP 契约 + 管理端白名单对账）"
	@echo "make test-admin-console - pip 安装 admin-console/requirements.txt 后跑 admin-console 烟测"
	@echo "make sync-nav   - 按 partials 写回各页 skip-bar + site-nav"
	@echo "make check-site-nav - 仅检查顶栏是否与模板一致（CI 同款）"
	@echo "make check-analysis - 分析引擎 --check（不写 snapshot，CI 同款）"
	@echo "make ingest     - 仅抓取候选（需外网）"
	@echo "make ingest-full - 同 ingest 但 --full-pool（忽略 require_route_match）"
	@echo "make analyze    - 校验 + 分析引擎 + 沉淀 + 趋势（无抓取）；默认写 artifacts/pipeline-metrics-*.json"
	@echo "                  可选 SKIP_PIPELINE_TELEMETRY=1 make analyze 跳过遥测"
	@echo "make evolution-fast - 仅刷新快照/沉淀/趋势（须先 make validate）；遥测同上"
	@echo "make trends     - 仅跑 sediment_trends.py（依赖已有沉淀）"
	@echo "make status     - 打印 analysis-snapshot 核心计数（无文件则提示 analyze）"
	@echo "make pipeline   - 同 analyze"
	@echo "make hooks      - 安装 Git 钩子（pre-commit 等同 make validate）"
	@echo "make sitemap    - 需 SITE_BASE=https://... 生成 sitemap.xml"
	@echo "make gen-nav-links - 由 spa/nav.config.json 生成 spa/src/navLinks.ts（增删注册页后先跑）"
	@echo "make spa-sync   - 同步根目录 HTML/assets/docs → spa/public（供全站 SPA）"
	@echo "make spa-build  - gen-nav-links + spa-sync + npm ci + vite build（产物 spa/dist，含 404 回退）"
	@echo "make spa-preview - 预览 spa 构建（默认端口见终端）"
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

gen-nav-links:
	python3 scripts/gen_nav_links_ts.py --write

spa-sync:
	python3 scripts/sync_spa_public.py

spa-install:
	cd spa && npm ci

spa-build: gen-nav-links spa-sync
	cd spa && npm ci && npm run build

spa-preview:
	cd spa && npm run preview

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
