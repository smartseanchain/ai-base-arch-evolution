#!/usr/bin/env python3
"""One-off builder: split synthesis.html into main + extensions + methods subpages."""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def nav_block(current: str | None) -> str:
    links = [
        ("index.html", "总览"),
        ("nexus.html", "立体联结"),
        ("edu-nexus.html", "教育纵轴"),
        ("evolution-triad.html", "人与AI演进"),
        ("work-infra-energy.html", "职业·基建·能源"),
        ("model.html", "分层模型"),
        ("architecture.html", "架构拓扑"),
        ("timeline.html", "历史演进"),
        ("past-future.html", "廿年视角"),
        ("decade.html", "十年展望"),
        ("decade-scenes.html", "十年场景"),
        ("decade-us.html", "十年之问"),
        ("modules-map.html", "模块图谱"),
        ("synthesis.html", "综合推演"),
        ("risk-geo.html", "地缘与商业"),
        ("net-biz-capital.html", "网·商·资·工"),
        ("national-strategy-opinion.html", "战略·舆情"),
        ("social-responsibility-evolution.html", "社会责任"),
        ("evolution-loop.html", "进化闭环"),
        ("analysis-hub.html", "分析引擎"),
        ("intelligent-evolution.html", "智能进化"),
        ("smart-overhaul.html", "整体改造"),
        ("evolvable-architecture.html", "可进化架构"),
        ("lab.html", "沙盘工坊"),
    ]
    parts = []
    for href, label in links:
        c = ' class="current"' if current == "synthesis" and href == "synthesis.html" else ""
        parts.append(f'        <a href="{href}"{c}>{label}</a>')
    return "\n".join(parts)


def main() -> None:
    syn_path = REPO / "synthesis.html"
    lines = syn_path.read_text(encoding="utf-8").splitlines(keepends=True)

    HEAD_SYN = (
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta name="description" content="综合推演主篇：模块表（§1）、五条判据（§2）、毗邻图（§3）、合成轴（§4）、推演配方 A—H（§5）、工作台（§10）。叠加五域与复合表见 synthesis-extensions；持续迭代与 §12§13 见 synthesis-methods。" />
  <meta name="theme-color" content="#0c1118" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="基础架构演变推演" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:title" content="综合推演（主篇）· 模块组合与判据 · 基础架构演变推演" />
  <meta property="og:description" content="§1—§5 与 §10 工作台；§6—§9 与 §11—§13 已拆至子页以减轻阅读负担。" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="综合推演（主篇）· 基础架构演变推演" />
  <meta name="twitter:description" content="模块表、判据、配方 A—H 与工作台；扩展图景与方法见子页。" />
  <title>综合推演（主篇）· 模块组合与判据 · 基础架构演变推演</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/site.css" />
</head>
<body>
  <div class="wrap">
    <div class="skip-bar" role="navigation" aria-label="快捷跳转">
      <a class="skip-link" href="#main">跳到正文</a>
      <a class="skip-link" href="index.html#three-questions">三问导读</a>
    </div>
    <header class="site-nav">
      <div class="site-nav-start">
        <a class="brand" href="index.html">基础架构演变推演</a>
        <a href="index.html#three-questions" class="site-nav-threeq" title="我们在哪 · 要做什么 · 将在哪">三问</a>
      </div>
      <nav class="site-links" aria-label="站内分页">
"""
        + nav_block("synthesis")
        + """
      </nav>
    </header>



    <div id="main" class="page-head" tabindex="-1">
      <h1>综合推演（主篇）：模块、判据、配方与工作台</h1>
      <p class="lead">
        整站鸟瞰见 <a href="index.html#three-questions">总览 · 三问导读</a>。本页保留<strong>元梳理主干</strong>：<strong>§1</strong> 模块变量表、<strong>§2</strong> 五条判据、<strong>§3—§4</strong> 关联与合成轴、<strong>§5</strong> 配方 A—H，以及 <strong>§10</strong> 工作台。为减轻单页过长，<strong>§6—§9</strong>（叠加五域、复合总表、三簇图景、五维切片）已迁至 <a href="synthesis-extensions.html">综合推演 · 扩展图景</a>；<strong>§11—§13</strong>（持续迭代、跨学科办法、深读透镜）迁至 <a href="synthesis-methods.html">综合推演 · 方法与透镜</a>。读数与闭环仍与全站一致：<a href="docs/DEDUCTION_STRATEGY.md">科学推演策略</a>、<a href="evolution-loop.html">进化闭环</a>、<a href="analysis-hub.html">分析引擎</a>。
      </p>
      <aside class="card site-data-live-strip-host" data-site-data-live aria-live="polite" hidden></aside>
    </div>

    <div class="nexus-legend" aria-label="三色标签说明">
      <span class="nexus-tag evidence">依据 — 站内各页已写明的结构与可观察现象</span>
      <span class="nexus-tag extend">扩展 — 变量如何在模块间传导、放大或抵消</span>
      <span class="nexus-tag imagine">想象 — 多种可能形态与可见征候（可证伪的叙述）</span>
    </div>

    <nav aria-label="本页章节">
      <ul class="edu-toc">
        <li><a href="#inventory">§1 模块·五系七层</a></li>
        <li><a href="#criteria">§2 组合合理性</a></li>
        <li><a href="#graph">§3 关联与毗邻</a></li>
        <li><a href="#axes">§4 三条合成轴</a></li>
        <li><a href="#recipes">§5 推演配方 A—H</a></li>
        <li><a href="synthesis-extensions.html#stack-domains">§6—§9 扩展图景 →</a>（五域 · 复合表 · 三簇 · 五维）</li>
        <li><a href="national-strategy-opinion.html#integrated-deduction">战略·舆情多源台</a></li>
        <li><a href="#workflow">§10 工作台</a></li>
        <li><a href="synthesis-methods.html#perpetual">§11—§13 方法与透镜 →</a></li>
        <li><a href="docs/DEDUCTION_STRATEGY.md">科学推演策略</a> · <a href="docs/RESEARCH_METHODS_MAP.md">方法·工具匹配</a></li>
        <li><a href="evolution-loop.html">进化闭环</a></li>
        <li><a href="analysis-hub.html">分析引擎</a></li>
        <li><a href="intelligent-evolution.html">智能进化</a></li>
        <li><a href="evolvable-architecture.html">可进化架构</a></li>
        <li><a href="social-responsibility-evolution.html">社会责任</a></li>
        <li><a href="net-biz-capital.html">网·商·资·工链</a></li>
      </ul>
    </nav>
"""
    )

    HEAD_EXT = (
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta name="description" content="综合推演 · 扩展图景：§6 叠加五域、§7 复合焦点总表、§8 三簇未来图景、§9 五维形态切片。" />
  <meta name="theme-color" content="#0c1118" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="基础架构演变推演" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:title" content="综合推演 · 扩展图景（§6—§9）· 基础架构演变推演" />
  <meta property="og:description" content="叠加五域与配方 I—V、复合表、三簇分叉、五维可见切片。" />
  <title>综合推演 · 扩展图景（§6—§9）· 基础架构演变推演</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/site.css" />
</head>
<body>
  <div class="wrap">
    <div class="skip-bar" role="navigation" aria-label="快捷跳转">
      <a class="skip-link" href="#main">跳到正文</a>
      <a class="skip-link" href="index.html#three-questions">三问导读</a>
    </div>
    <header class="site-nav">
      <div class="site-nav-start">
        <a class="brand" href="index.html">基础架构演变推演</a>
        <a href="index.html#three-questions" class="site-nav-threeq" title="我们在哪 · 要做什么 · 将在哪">三问</a>
      </div>
      <nav class="site-links" aria-label="站内分页">
"""
        + nav_block(None)
        + """
      </nav>
    </header>



    <div id="main" class="page-head" tabindex="-1">
      <h1>综合推演 · 扩展图景（§6—§9）</h1>
      <p class="lead">
        本页为 <a href="synthesis.html">综合推演主篇</a> 的<strong>扩展子页</strong>，承载原 §6—§9：<strong>叠加五域</strong>、<strong>复合焦点总表</strong>、<strong>三簇图景</strong>、<strong>五维形态切片</strong>。判据与配方 A—H 见主篇 <a href="synthesis.html#criteria">§2</a>、<a href="synthesis.html#recipes">§5</a>；工作台见 <a href="synthesis.html#workflow">§10</a>；持续迭代与跨学科办法见 <a href="synthesis-methods.html">方法与透镜</a>。
      </p>
      <aside class="card site-data-live-strip-host" data-site-data-live aria-live="polite" hidden></aside>
    </div>

    <div class="nexus-legend" aria-label="三色标签说明">
      <span class="nexus-tag evidence">依据 — 站内各页已写明的结构与可观察现象</span>
      <span class="nexus-tag extend">扩展 — 变量如何在模块间传导、放大或抵消</span>
      <span class="nexus-tag imagine">想象 — 多种可能形态与可见征候（可证伪的叙述）</span>
    </div>

    <nav aria-label="本页章节">
      <ul class="edu-toc">
        <li><a href="synthesis.html">← 综合推演主篇（§1—§5、§10）</a></li>
        <li><a href="#stack-domains">§6 叠加五域</a></li>
        <li><a href="#matrix">§7 复合焦点总表</a> · <a href="national-strategy-opinion.html#integrated-deduction">战略·舆情多源台</a></li>
        <li><a href="#forks">§8 三簇未来图景</a></li>
        <li><a href="#dimensions">§9 五维形态展现</a></li>
        <li><a href="synthesis-methods.html#perpetual">§11—§13 方法与透镜 →</a></li>
      </ul>
    </nav>
"""
    )

    HEAD_METH = (
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta name="description" content="综合推演 · 方法与透镜：§11 持续迭代、§12 跨学科推演办法、§13 深读透镜。" />
  <meta name="theme-color" content="#0c1118" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="基础架构演变推演" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:title" content="综合推演 · 方法与透镜（§11—§13）· 基础架构演变推演" />
  <meta property="og:description" content="持续梳理扩展推演、跨学科办法表、深读透镜四穿透与多场景。" />
  <title>综合推演 · 方法与透镜（§11—§13）· 基础架构演变推演</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/site.css" />
</head>
<body>
  <div class="wrap">
    <div class="skip-bar" role="navigation" aria-label="快捷跳转">
      <a class="skip-link" href="#main">跳到正文</a>
      <a class="skip-link" href="index.html#three-questions">三问导读</a>
    </div>
    <header class="site-nav">
      <div class="site-nav-start">
        <a class="brand" href="index.html">基础架构演变推演</a>
        <a href="index.html#three-questions" class="site-nav-threeq" title="我们在哪 · 要做什么 · 将在哪">三问</a>
      </div>
      <nav class="site-links" aria-label="站内分页">
"""
        + nav_block(None)
        + """
      </nav>
    </header>



    <div id="main" class="page-head" tabindex="-1">
      <h1>综合推演 · 方法与透镜（§11—§13）</h1>
      <p class="lead">
        本页为 <a href="synthesis.html">综合推演主篇</a> 的<strong>方法子页</strong>：原 <strong>§11</strong> 持续迭代与扩展插槽、<strong>§12</strong> 跨学科推演办法、<strong>§13</strong> 深读透镜。模块表与判据见主篇 <a href="synthesis.html#inventory">§1</a>、<a href="synthesis.html#criteria">§2</a>；五域与复合表见 <a href="synthesis-extensions.html">扩展图景</a>；工作台见 <a href="synthesis.html#workflow">§10</a>。
      </p>
      <aside class="card site-data-live-strip-host" data-site-data-live aria-live="polite" hidden></aside>
    </div>

    <div class="nexus-legend" aria-label="三色标签说明">
      <span class="nexus-tag evidence">依据 — 站内各页已写明的结构与可观察现象</span>
      <span class="nexus-tag extend">扩展 — 变量如何在模块间传导、放大或抵消</span>
      <span class="nexus-tag imagine">想象 — 多种可能形态与可见征候（可证伪的叙述）</span>
    </div>

    <nav aria-label="本页章节">
      <ul class="edu-toc">
        <li><a href="synthesis.html">← 综合推演主篇</a></li>
        <li><a href="synthesis-extensions.html">← 扩展图景（§6—§9）</a></li>
        <li><a href="#perpetual">§11 持续迭代</a></li>
        <li><a href="#methods">§12 跨学科办法</a></li>
        <li><a href="#deep-lens">§13 深读透镜</a></li>
        <li><a href="docs/DEDUCTION_STRATEGY.md">科学推演策略</a> · <a href="docs/RESEARCH_METHODS_MAP.md">方法·工具匹配</a></li>
      </ul>
    </nav>
"""
    )

    main_mid = "".join(lines[104:475])
    workflow_sec = "".join(lines[957:974])

    def fix_ext(s: str) -> str:
        s = s.replace('href="#criteria"', 'href="synthesis.html#criteria"')
        s = s.replace('href="#perpetual"', 'href="synthesis-methods.html#perpetual"')
        return s

    def fix_meth(s: str) -> str:
        pairs = [
            ('href="#inventory"', 'href="synthesis.html#inventory"'),
            ('href="#criteria"', 'href="synthesis.html#criteria"'),
            ('href="#graph"', 'href="synthesis.html#graph"'),
            ('href="#axes"', 'href="synthesis.html#axes"'),
            ('href="#recipes"', 'href="synthesis.html#recipes"'),
            ('href="#forks"', 'href="synthesis-extensions.html#forks"'),
            ('href="#stack-domains"', 'href="synthesis-extensions.html#stack-domains"'),
            ('href="#dimensions"', 'href="synthesis-extensions.html#dimensions"'),
            ('href="#matrix"', 'href="synthesis-extensions.html#matrix"'),
        ]
        for a, b in pairs:
            s = s.replace(a, b)
        return s

    ext_body = fix_ext("".join(lines[476:956]))
    meth_body = fix_meth("".join(lines[974:1277]))

    FOOT_EXT = """    <footer>
      <a href="synthesis.html">← 综合推演主篇</a> · <a href="synthesis-methods.html">方法与透镜</a> · <a href="modules-map.html">模块图谱</a> · <a href="lab.html">沙盘工坊</a> · <a href="evolution-loop.html">进化闭环</a> · <a href="analysis-hub.html">分析引擎</a> · <a href="index.html">总览</a> · <a href="index.html#three-questions">三问</a>
    </footer>
  </div>
  <script src="assets/site-data-bus.js"></script>
  <script src="assets/motion.js"></script>
</body>
</html>
"""

    FOOT_METH = """    <footer>
      <a href="synthesis.html">← 综合推演主篇</a> · <a href="synthesis-extensions.html">扩展图景</a> · <a href="modules-map.html">模块图谱</a> · <a href="lab.html">沙盘工坊</a> · <a href="evolution-loop.html">进化闭环</a> · <a href="analysis-hub.html">分析引擎</a> · <a href="index.html">总览</a> · <a href="index.html#three-questions">三问</a>
    </footer>
  </div>
  <script src="assets/site-data-bus.js"></script>
  <script src="assets/motion.js"></script>
</body>
</html>
"""

    wf = workflow_sec
    wf = wf.replace(
        "先读 <strong>§6</strong>，再选 §5（A—H）或 §6.2（<strong>I—V</strong>）",
        "先读 <a href=\"synthesis-extensions.html#stack-domains\"><strong>§6</strong></a>，再选 §5（A—H）或 §6.2（<strong>I—V</strong>）",
    )
    wf = wf.replace(
        "按 <a href=\"#perpetual\">§11</a> 自增一行",
        "按 <a href=\"synthesis-methods.html#perpetual\">§11</a> 自增一行",
    )
    wf = wf.replace(
        "回到 <strong>§7</strong> 表",
        "回到 <a href=\"synthesis-extensions.html#matrix\"><strong>§7</strong></a> 表",
    )
    wf = wf.replace(
        "对照 <strong>§8</strong> 三簇",
        "对照 <a href=\"synthesis-extensions.html#forks\"><strong>§8</strong></a> 三簇",
    )
    wf = wf.replace(
        "并用 <strong>§9</strong>（含 9.1—9.3）",
        "并用 <a href=\"synthesis-extensions.html#dimensions\"><strong>§9</strong></a>（含 9.1—9.3）",
    )
    wf = wf.replace(
        "回到 §6 换配方",
        "回到 <a href=\"synthesis-extensions.html#stack-domains\">§6</a> 换配方",
    )
    wf = wf.replace(
        "<a href=\"#perpetual\">§11</a> 的<strong>梳理",
        "<a href=\"synthesis-methods.html#perpetual\">§11</a> 的<strong>梳理",
    )
    wf = wf.replace('<a href="#methods">§12</a>', '<a href="synthesis-methods.html#methods">§12</a>')
    wf = wf.replace(
        '<a href="#deep-lens">§13 深读透镜</a>',
        '<a href="synthesis-methods.html#deep-lens">§13 深读透镜</a>',
    )
    wf = wf.replace(
        "再回 §7/§6。",
        "再回 <a href=\"synthesis-extensions.html#matrix\">§7</a>/<a href=\"synthesis-extensions.html#stack-domains\">§6</a>。",
    )

    FOOT_MAIN = """    <footer>
      <a href="decade-scenes.html">← 十年场景</a> · <a href="synthesis-extensions.html">扩展图景 §6—§9</a> · <a href="synthesis-methods.html">方法与透镜 §11—§13</a> · <a href="modules-map.html">模块图谱</a> · <a href="evolvable-architecture.html">可进化架构</a> · <a href="evolution-loop.html">进化闭环</a> · <a href="analysis-hub.html">分析引擎</a> · <a href="intelligent-evolution.html">智能进化</a> · <a href="smart-overhaul.html">整体改造</a> · <a href="lab.html">沙盘工坊</a> · <a href="evolution-triad.html">人与AI演进</a> · <a href="index.html">总览</a> · <a href="index.html#three-questions">三问</a>
    </footer>
  </div>
  <script src="assets/site-data-bus.js"></script>
  <script src="assets/motion.js"></script>
</body>
</html>
"""

    main_full = HEAD_SYN + main_mid + wf + FOOT_MAIN

    syn_path.write_text(main_full, encoding="utf-8")
    (REPO / "synthesis-extensions.html").write_text(HEAD_EXT + ext_body + FOOT_EXT, encoding="utf-8")
    (REPO / "synthesis-methods.html").write_text(HEAD_METH + meth_body + FOOT_METH, encoding="utf-8")
    print("OK: wrote synthesis.html + synthesis-extensions.html + synthesis-methods.html")


if __name__ == "__main__":
    main()
