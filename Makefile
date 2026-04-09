# 可进化站点 · 常用目标（在项目根执行 make <target>）
.PHONY: validate ingest analyze pipeline check-analysis help hooks sitemap

help:
	@echo "make validate   - 校验 manifest/候选 + analysis_engine --check（与 pre-commit 一致）"
	@echo "make check-analysis - 分析引擎 --check（不写 snapshot，CI 同款）"
	@echo "make ingest     - 仅抓取候选（需外网）"
	@echo "make analyze    - 校验 + 分析引擎 + 沉淀 + 趋势（无抓取）"
	@echo "make pipeline   - 同 analyze"
	@echo "make hooks      - 安装 Git 钩子（pre-commit 跑 validate + check-analysis）"
	@echo "make sitemap    - 需 SITE_BASE=https://... 生成 sitemap.xml"

validate:
	python3 scripts/validate-evolution-manifest.py
	python3 scripts/validate-evolution-candidates.py
	python3 scripts/analysis_engine.py --check

check-analysis:
	python3 scripts/analysis_engine.py --check

hooks:
	bash scripts/install-git-hooks.sh

sitemap:
	@test -n "$${SITE_BASE:-}" || (echo '用法: SITE_BASE=https://example.org make sitemap' >&2; exit 1)
	SITE_BASE="$${SITE_BASE}" python3 scripts/gen-sitemap.py

ingest:
	bash scripts/run_ingest_only.sh

analyze pipeline:
	bash scripts/run_update_pipeline.sh
