# 综合推演 · 分子页说明

原单文件 `synthesis.html`（约 1300 行）已拆为**三页**，顶栏仍只保留「综合推演」入口（`synthesis.html`），子页从主篇 TOC 与页脚进入。

| 文件 | 内容（原章节） | 适用读者 |
|------|----------------|----------|
| [synthesis.html](../synthesis.html) | §1—§5、§10（模块表、判据、毗邻、合成轴、配方 A—H、工作台） | 先建立全站变量与判据 |
| [synthesis-extensions.html](../synthesis-extensions.html) | §6—§9（叠加五域与 I—V、复合表、三簇、五维切片） | 叠乘域、表行、形态分叉 |
| [synthesis-methods.html](../synthesis-methods.html) | §11—§13（持续迭代插槽、跨学科办法、深读透镜） | 迭代纪律与研究套路 |

**站外锚点迁移**（书签与文档链接已批量替换）：

- `synthesis.html#perpetual` → `synthesis-methods.html#perpetual`
- `synthesis.html#methods` → `synthesis-methods.html#methods`
- `synthesis.html#deep-lens` → `synthesis-methods.html#deep-lens`
- `synthesis.html#stack-domains` / `#matrix` / `#forks` / `#dimensions` → `synthesis-extensions.html#…`

主篇仍保留 `#inventory`、`#criteria`、`#graph`、`#axes`、`#recipes`、**`#continuation`（继续推演 · 全站深描矩阵）**、`#workflow`。

**再拆分**：若 `modules-map.html` 或 `legacy-all-in-one.html` 仍觉过长，可按本模式增子页并更新 `scripts/evolution-registry.json` 与 `scripts/gen-sitemap.py` 的 `PRIORITY`。

**重建页面**（从当前三页反推不推荐；仅当需从旧单文件重生时）：仓库内 `scripts/_build_synthesis_subpages.py` 曾用于首次切分，日常维护请直接编辑三个 HTML。
