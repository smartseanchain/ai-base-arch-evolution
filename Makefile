# 可进化站点 · 常用目标（在项目根执行 make <target>）
.PHONY: validate test sync-nav check-site-nav ingest ingest-full analyze pipeline check-analysis help hooks sitemap

help:
	@echo "make validate   - 校验 manifest/候选/hint 决策 + 对账 + 顶栏 + 单测 + analysis_engine --check（与 pre-commit 一致）"
	@echo "make test       - scripts/tests 下 unittest（PYTHONPATH=scripts）"
	@echo "make sync-nav   - 按 partials 写回各页 skip-bar + site-nav"
	@echo "make check-site-nav - 仅检查顶栏是否与模板一致（CI 同款）"
	@echo "make check-analysis - 分析引擎 --check（不写 snapshot，CI 同款）"
	@echo "make ingest     - 仅抓取候选（需外网）"
	@echo "make ingest-full - 同 ingest 但 --full-pool（忽略 require_route_match）"
	@echo "make analyze    - 校验 + 分析引擎 + 沉淀 + 趋势（无抓取）"
	@echo "make pipeline   - 同 analyze"
	@echo "make hooks      - 安装 Git 钩子（pre-commit 跑 validate + check-analysis）"
	@echo "make sitemap    - 需 SITE_BASE=https://... 生成 sitemap.xml"

validate:
	python3 scripts/validate-evolution-manifest.py
	python3 scripts/validate-evolution-candidates.py
	python3 scripts/validate_evolution_hint_decisions.py
	python3 scripts/check_manifest_drift.py
	python3 scripts/sync_site_nav.py --check
	PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_*.py' -q
	python3 scripts/analysis_engine.py --check

sync-nav:
	python3 scripts/sync_site_nav.py

check-site-nav:
	python3 scripts/sync_site_nav.py --check

test:
	PYTHONPATH=scripts python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v

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
