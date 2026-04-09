## 变更类型（删无关项）

- [ ] 仅 HTML/CSS/文案
- [ ] `evolution-manifest.json` / `evolution-candidates.json`
- [ ] 脚本 / CI / Makefile
- [ ] 其他：<!-- 简述 -->

## 若涉及 manifest / 候选入库

- [ ] 入库条目的 `review_state` 已为 **`queued_for_manifest`**（噪点用 **`noise`**；默认 **`pending`**）
- [ ] 已本地执行 `make validate`（含对账与 `analysis_engine --check`）
- [ ] 每条新信号能回答「三问」判据（见站内 `evolution-loop.html` §5 · 人必须做什么）
- [ ] `maps_to.pages` 与 `lab_factors` 已人工核对；对账脚本无报错
- [ ] 若新增根目录 HTML 或沙盘因子：已同步 **`scripts/evolution-registry.json`** 与 **`assets/lab.js`**
- [ ] 若改全站顶栏或 skip-bar：已更新 **`partials/site-nav.inc.html`** / **`partials/skip-bar.inc.html`** 并执行 **`make sync-nav`**

## 若本周期处理了分析引擎的 evolution_hints

- [ ] 已在 **`assets/evolution-hint-decisions.json`** 追加对应记录（或注明为何本轮无提示可处理）

## 备注

<!-- 可选：链接相关 issue、说明为何否决某条候选等 -->
