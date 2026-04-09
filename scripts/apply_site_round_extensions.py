#!/usr/bin/env python3
"""一次性：在各注册页插入「推演扩展 · 本轮更新」卡片。已执行后可删本脚本。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sec(slug: str, title_suffix: str, p: str, bullets: list[str]) -> str:
    lis = "\n".join(f"        <li>{b}</li>" for b in bullets)
    return f"""    <section class="card site-round-extension" id="ext-round-{slug}" aria-labelledby="hre-{slug}">
      <h2 class="site-round-extension-h" id="hre-{slug}">推演扩展 · 本轮更新（{title_suffix}）</h2>
      <p class="muted" style="margin:0 0 0.5rem;font-size:0.88rem;line-height:1.7">{p}</p>
      <ul>
{lis}
      </ul>
    </section>"""


# (filename, old_snippet_must_exist_once, new_snippet_replacement)
PATCHES: list[tuple[str, str, str]] = [
    (
        "nexus.html",
        """      </svg>
    </div>

    <section>
      <h2>1. 依据：我们默认的「当前形态」锚点</h2>""",
        """      </svg>
    </div>

"""
        + sec(
            "nexus",
            "立体联结",
            "尺度枢轴页本轮强调：把<strong>「谁在什么尺度上先痛」</strong>写清，再接战略·舆情与十年场景；与 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>「立体联结」行对读。",
            [
                "为每个议题试写<strong>客厅一句话 / 机房一句话 / 公文一句话</strong>，三句主语是否一致；不一致处即为互译缺口。",
                "扩展时优先接 <a href=\"edu-nexus.html\">教育纵轴</a>、<a href=\"decade-us.html\">十年之问</a> 的接口变厚，而非新造抽象词。",
                "想象分叉须带<strong>可见征候</strong>（通知栏、账单、路由器策略、校讯字段等），避免纯态度词。",
                "与 <a href=\"national-strategy-opinion.html#dual-track\">双轨</a> 并读：问「公文已到哪、客厅是否仍不知道」。",
            ],
        )
        + """
    <section>
      <h2>1. 依据：我们默认的「当前形态」锚点</h2>""",
    ),
    (
        "analysis-hub.html",
        """      </svg>
    </div>

    <nav class="toc" aria-label="本页目录">
      <a href="#panorama">方法与演进全景</a>""",
        """      </svg>
    </div>

"""
        + sec(
            "analysis",
            "分析引擎",
            "总线页本轮把<strong>读数→叙事→改表/改 manifest</strong>串成责任链；热力与共现只作线索，结论须回到 <a href=\"synthesis.html#criteria\">§2 判据</a> 与 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>。",
            [
                "每条高优先级 <code>evolution_hints</code>：指定<strong>目标页锚点</strong>与「若落实则 §7 哪类行受益」。",
                "<code>hint_closure_gaps</code> 与 <code>evolution-hint-decisions</code> 同步看：拒绝「只刷新快照不写字」。",
                "共现上升的一对因子，试写<strong>最短传导链</strong>再与 <a href=\"lab.html\">沙盘</a> 旋钮对照。",
                "沉淀 / SQLite 趋势与正文漂移并读：问「结构化偏斜是否已在 §1 表中有位置」。",
            ],
        )
        + """
    <nav class="toc" aria-label="本页目录">
      <a href="#panorama">方法与演进全景</a>""",
    ),
    (
        "modules-map.html",
        """      </svg>
    </div>

    <nav class="toc" aria-label="本页目录">
      <a href="#taxonomy">五系分类</a>""",
        """      </svg>
    </div>

"""
        + sec(
            "modules-map",
            "模块图谱",
            "图谱页本轮要求：每次推演先选<strong>进门系</strong>与<strong>必须踏过的堆叠层</strong>，再打开路径/八镜头；与主篇 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>「模块图谱+三页」行自检。",
            [
                "路径预设与星丛：标注<strong>哪条边最容易被新信号打断</strong>（地缘、电力、校采、支付）。",
                "扩展三向里「向上显影」须接到 <a href=\"decade.html\">十年六维</a> 或 <a href=\"national-strategy-opinion.html\">战略·舆情</a> 之一，防悬空中枢。",
                "分系总表增行时同步想「是否应出现新的 <code>maps_to.pages</code> 路由」。",
                "八镜头演示与 <a href=\"synthesis-methods.html#deep-lens\">§13</a> 可互换使用，但镜头切换后要回扣 §2。",
            ],
        )
        + """
    <nav class="toc" aria-label="本页目录">
      <a href="#taxonomy">五系分类</a>""",
    ),
    (
        "edu-nexus.html",
        """        <text x="629" y="52" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">基建与规则</text>
      </svg>
    </div>

    <nav aria-label="本页章节">""",
        """        <text x="629" y="52" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">基建与规则</text>
      </svg>
    </div>

"""
        + sec(
            "edu",
            "教育纵轴",
            "本轮把<strong>评价权迁移</strong>与<strong>用工合同颗粒度</strong>绑读：校家平台三边谁在备份链路与仲裁上「默认兜底」；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 教育+人与AI行。",
            [
                "为每个学段增加一问：「模型输出进入<strong>哪张表、谁可申诉、留存多久</strong>」。",
                "跨境在线与学籍/考试叙事并读时，写明<strong>法域冲突的默认承担者</strong>（校/家/平台）。",
                "AI 触点链每一环尝试对应 <a href=\"synthesis.html#recipes\">配方 B</a> 的一条征候。",
                "与 <a href=\"decade-scenes.html#scene-edu\">十年场景·教育</a> 互证：同一政策在教室与家庭 UI 上的差异。",
            ],
        )
        + """
    <nav aria-label="本页章节">""",
    ),
    (
        "work-infra-energy.html",
        """        <text x="607" y="54" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">三线交汇</text>
      </svg>
    </div>

    <nav aria-label="本页章节">""",
        """        <text x="607" y="54" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">三线交汇</text>
      </svg>
    </div>

"""
        + sec(
            "wie",
            "职业·基建·能源",
            "本轮强调<strong>末端闭合</strong>：没有电/网/合同位点的「数字职业」一律标为叙事；与 <a href=\"synthesis.html#recipes\">配方 C</a>、<a href=\"synthesis.html#continuation\">继续推演矩阵</a> 硬栈行对读。",
            [
                "任一算力叙事旁注<strong>kW/冷却/区位</strong>三词中至少其一可来自公开线索或合同类型。",
                "基建段落与 <a href=\"architecture.html\">架构拓扑</a> 互写「负载实际落点」与「纸面分区」是否一致。",
                "能源紧张情景下优先问<strong>谁先被限电</strong>：云、制造、还是城市公共算力。",
                "与 <a href=\"risk-geo.html\">地缘</a> 并读时标明供应链与支付哪一环与电网同脆弱。",
            ],
        )
        + """
    <nav aria-label="本页章节">""",
    ),
    (
        "net-biz-capital.html",
        """        <text x="566" y="50" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">劳动回路</text>
      </svg>
    </div>

    <nav aria-label="本页章节">""",
        """        <text x="566" y="50" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">劳动回路</text>
      </svg>
    </div>

"""
        + sec(
            "icbw",
            "网·商·资·工",
            "主链本轮补<strong>反向塑形</strong>：劳动/合规成本回升后，产品形态与估值故事哪一段先变形；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 网商资工行。",
            [
                "从左到右扫链时，为每一环写<strong>谁承担不可达风险</strong>（用户、商户、平台股东）。",
                "多雇主/零工接口与 <a href=\"work-infra-energy.html\">职基能</a> 社保属地条款同屏。",
                "资本叙事与 CAPEX 段落旁注<strong>是否依赖单一云区或单一支付轨</strong>。",
                "与 <a href=\"decade-scenes.html\">十年场景</a>·办公并读：协作栈变更如何回流主链。",
            ],
        )
        + """
    <nav aria-label="本页章节">""",
    ),
    (
        "national-strategy-opinion.html",
        """        <text x="530" y="60" text-anchor="middle" fill="#8b9cb3" font-size="8" font-family="Noto Sans SC,sans-serif">2026—2036 · 六维表</text>
      </svg>
    </div>

    <nav class="toc" aria-label="本页目录">
      <a href="#dual-track">双轨时间轴</a>""",
        """        <text x="530" y="60" text-anchor="middle" fill="#8b9cb3" font-size="8" font-family="Noto Sans SC,sans-serif">2026—2036 · 六维表</text>
      </svg>
    </div>

"""
        + sec(
            "natstr",
            "战略·舆情",
            "双轨本轮强制问：<strong>预算—招标—考核</strong>链条是否出现文件热词；资本与跨境条款是否改写采购；与 <a href=\"synthesis-extensions.html#matrix\">§7</a>、<a href=\"synthesis.html#continuation\">继续推演矩阵</a> 社会责任+战略行并读。",
            [
                "每一议题画<strong>两轴时间线</strong>：制度输出 vs 舆论峰值，标注领先/滞后与可观察锚点。",
                "与 <a href=\"decade.html\">十年展望</a>·国家治理行对账：是否同一词汇两套节奏。",
                "多源台合成时禁止把热搜等同于政策已定；须写「仍在话语层」的征候。",
                "法律/规划类线索入库时同步想 <code>kind: law | policy</code> 与目标页映射。",
            ],
        )
        + """
    <nav class="toc" aria-label="本页目录">
      <a href="#dual-track">双轨时间轴</a>""",
    ),
    (
        "intelligent-evolution.html",
        """      </svg>
    </div>

    <nav class="toc" aria-label="本页目录">
      <a href="#boundary">概念与边界</a>""",
        """      </svg>
    </div>

"""
        + sec(
            "intevo",
            "智能进化",
            "本轮重申：<strong>模型输出默认进候选或侧车</strong>；每条自动摘要须配「人审检查点」与回滚路径；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 智能+改造+架构行。",
            [
                "分层（规则→LLM→RAG→微调）旁注<strong>哪一层可单独关掉而不伤站点真源</strong>。",
                "评测指标与 <a href=\"docs/ARCHITECTURE.md#decision-traceability\">决策追溯</a> 字段对齐，避免黑箱工单。",
                "与 <a href=\"evolution-loop.html\">进化闭环</a> 对读：哪些字段只能人改 manifest。",
                "§11 插槽⑨ 变更时同步更新 <a href=\"smart-overhaul.html\">整体改造</a> WBS 中的智能子项。",
            ],
        )
        + """
    <nav class="toc" aria-label="本页目录">
      <a href="#boundary">概念与边界</a>""",
    ),
    (
        "smart-overhaul.html",
        """      </svg>
    </div>

    <nav class="toc" aria-label="本页目录">
      <a href="#principles">目标与原则</a>""",
        """      </svg>
    </div>

"""
        + sec(
            "overhaul",
            "整体改造",
            "WBS 本轮与<strong>可验收里程碑</strong>绑定：每一域交付物对应 ARCHITECTURE 七层之一；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 工程三页。",
            [
                "六域任一条目补「<strong>若延期，哪条推演读数最先失真</strong>」。",
                "数据管道与 <a href=\"analysis-hub.html\">分析快照</a> 字段对照，避免双写无索引。",
                "P0→P2 分期旁注<strong>依赖的外部政策/云厂商节奏</strong>属短中长哪档。",
                "与 <a href=\"evolvable-architecture.html\">可进化架构</a> 插槽 ⑦—⑩ 映射表保持同文。",
            ],
        )
        + """
    <nav class="toc" aria-label="本页目录">
      <a href="#principles">目标与原则</a>""",
    ),
    (
        "evolvable-architecture.html",
        """      </svg>
    </div>

    <nav class="toc" aria-label="本页目录">
      <a href="#definition">定义与边界</a>""",
        """      </svg>
    </div>

"""
        + sec(
            "evoarch",
            "可进化架构",
            "总览页本轮把<strong>观测—编码—分析—反哺</strong>画成可审计闭环：每一步产物文件名与 <a href=\"docs/ARCHITECTURE.md\">ARCHITECTURE</a> 一致；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>。",
            [
                "七层闭环与 <a href=\"analysis-hub.html#panorama\">分析总线</a> 能力表交叉检查，防重复造轮子。",
                "人机闸门：列出<strong>三条永不准自动化</strong>的 merge 类型（与进化闭环一致）。",
                "插槽 ⑦—⑩ 任一扩展须说明「影响读者可见 HTML 还是仅 JSON」。",
                "与 <a href=\"social-responsibility-evolution.html\">社会责任</a> 页信号路由对照，防社会责任漂移成口号。",
            ],
        )
        + """
    <nav class="toc" aria-label="本页目录">
      <a href="#definition">定义与边界</a>""",
    ),
    (
        "social-responsibility-evolution.html",
        """      </svg>
    </div>

    <nav class="toc" aria-label="本页目录">
      <a href="#model">社会责任模型（站内含义）</a>""",
        """      </svg>
    </div>

"""
        + sec(
            "sre",
            "社会责任",
            "本轮把公共利益/代际/劳工/环境显式映射到 <code>kind</code> 与 <a href=\"synthesis-extensions.html#matrix\">§7</a> 行；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 社会责任+战略行。",
            [
                "多源输入表：每条信号写<strong>最小可检验影响陈述</strong>（对哪类主体的合同/账单可见）。",
                "自动分析输出禁止替代原文阅读；须链回 <a href=\"national-strategy-opinion.html\">战略·舆情</a> 双轨。",
                "与 <a href=\"decade-us.html#live\">十年之问 · 活得比较好</a> 同构：先底线再叙事。",
                "闸门：未经人审不得改 HTML 正文、不得把 deferred 当闭环。",
            ],
        )
        + """
    <nav class="toc" aria-label="本页目录">
      <a href="#model">社会责任模型（站内含义）</a>""",
    ),
    (
        "evolution-loop.html",
        """        <text x="510" y="50" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">§11 · 表行</text>
      </svg>
    </div>

    <aside id="evolution-closure-summary" class="card evolution-closure-summary" aria-live="polite" hidden></aside>""",
        """        <text x="510" y="50" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">§11 · 表行</text>
      </svg>
    </div>

"""
        + sec(
            "evloop",
            "进化闭环",
            "本轮强调 <strong>candidates → manifest</strong> 的 diff 可讲故事：哪些信号被路由丢弃、哪些升格；与 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 闭环+沙盘行对读。",
            [
                "每条 signal 补「建议读者先读的<strong>2 个站内锚点</strong>」再入库。",
                "ingest 路由变更记录简短理由，防「require_route_match 误杀」无声。",
                "OODA Decide 与 <code>lab_factors</code> 勾选一致：避免 manifest 与沙盘各说各话。",
                "与 <a href=\"analysis-hub.html\">分析引擎</a> 快照同天对照，看热力是否反映 manifest 更新。",
            ],
        )
        + """
    <aside id="evolution-closure-summary" class="card evolution-closure-summary" aria-live="polite" hidden></aside>""",
    ),
    (
        "evolution-triad.html",
        """        <text x="430" y="34" text-anchor="middle" fill="#5c6b7e" font-size="6.5" font-family="Noto Sans SC,sans-serif">每站：时代之门 × 行业之门</text>
      </svg>
    </div>

    <p class="read-hint" role="note">""",
        """        <text x="430" y="34" text-anchor="middle" fill="#5c6b7e" font-size="6.5" font-family="Noto Sans SC,sans-serif">每站：时代之门 × 行业之门</text>
      </svg>
    </div>

"""
        + sec(
            "triad",
            "人与AI演进",
            "五站本轮各加一问：<strong>「合同与技能谁先行」</strong>；出站时强制接 <a href=\"synthesis.html#recipes\">配方 B</a> 或 <a href=\"work-infra-energy.html\">职基能</a>；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>。",
            [
                "教育/职业两廊并读：标出<strong>同一技术词汇在两廊出现的时间差</strong>。",
                "家庭与个人站补「设备与账号<strong>默认归属</strong>」一句，防叙事飘在云上。",
                "走向合成站必须产出<strong>至少两枝</strong>可区分征候，再链接 §8 簇。",
                "读数条刷新后自问：manifest 是否应增一条 <code>maps_to.pages</code> 指向本页某站。",
            ],
        )
        + """
    <p class="read-hint" role="note">""",
    ),
    (
        "risk-geo.html",
        """        <text x="492" y="48" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">多路径 · Exit</text>
      </svg>
    </div>

    <section>
      <h2>冲击通道 × 热力</h2>""",
        """        <text x="492" y="48" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">多路径 · Exit</text>
      </svg>
    </div>

"""
        + sec(
            "risk",
            "地缘与商业",
            "热力条本轮当<strong>检查单</strong>用：每条「高」旁须有一句架构响应是否已在跑；对表 <a href=\"synthesis.html#recipes\">配方 D/G</a> 与 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>。",
            [
                "SME vs 大型组织：分开写<strong>最薄环</strong>（常在支付或身份，而非骨干网）。",
                "与 <a href=\"architecture.html\">架构</a> Cell 化叙事交叉：纸面多活是否经过年检演练。",
                "制裁情景下标注<strong>合同 force majeure 与数据出境</strong>谁先触发。",
                "热力调整时同步想沙盘因子 <code>sanction</code>、<code>geo</code> 是否勾选。",
            ],
        )
        + """
    <section>
      <h2>冲击通道 × 热力</h2>""",
    ),
    (
        "lab.html",
        """        <text x="629" y="48" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">§5 · 五域</text>
      </svg>
    </div>

    <section>
      <h2>业务连续性依赖流（SVG）</h2>""",
        """        <text x="629" y="48" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">§5 · 五域</text>
      </svg>
    </div>

"""
        + sec(
            "lab",
            "沙盘工坊",
            "本轮七步向导每步补<strong>「若旋钮拧紧，哪条 §7 表行先绷紧」</strong>；依赖流与 manifest 高亮同读；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 沙盘点。",
            [
                "因子勾选后写一句<strong>可对账输出</strong>（哪类账单/工单会先变）。",
                "与 <a href=\"synthesis-extensions.html#stack-domains\">§6 五域</a> 叠加时标明域间中介变量。",
                "本地 HTTP 打开以加载 JSON 时，记录一次「高亮因子 ↔ 信号 id」对照。",
                "压测推翻簇判断时，把反例写入 <a href=\"synthesis-methods.html#perpetual\">§11</a> 笔记而非口头。",
            ],
        )
        + """
    <section>
      <h2>业务连续性依赖流（SVG）</h2>""",
    ),
    (
        "architecture.html",
        """        <text x="406" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">并存 · 色标驱动力</text>
      </svg>
    </div>

    <section>
      <h2>单区域逻辑视图（SVG）</h2>""",
        """        <text x="406" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">并存 · 色标驱动力</text>
      </svg>
    </div>

"""
        + sec(
            "arch",
            "架构拓扑",
            "本轮每张图旁强制<strong>数据重力句</strong>：主负载与主数据实际落在哪一边界；与 <a href=\"model.html\">分层</a>、<a href=\"synthesis.html#continuation\">继续推演矩阵</a> 硬栈行对读。",
            [
                "六种形态对比时写清<strong>切换成本由谁承担</strong>（业务、平台还是法务）。",
                "Cell/多区域叙事必须接 <a href=\"risk-geo.html\">地缘</a> 支付与身份通道。",
                "与 <a href=\"work-infra-energy.html\">职基能</a> 对读：拓扑变更是否受电价/机位约束。",
                "引用生成式组件时标注<strong>模型 API 所属法域与日志落点</strong>。",
            ],
        )
        + """
    <section>
      <h2>单区域逻辑视图（SVG）</h2>""",
    ),
    (
        "model.html",
        """        <text x="514" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">社会技术系统</text>
      </svg>
    </div>

    <section>
      <h2>全景标签</h2>""",
        """        <text x="514" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">社会技术系统</text>
      </svg>
    </div>

"""
        + sec(
            "model",
            "分层模型",
            "本轮三平面+L 层旁各加<strong>责任可命名性</strong>：故障时哪层出现在对外公告；与 <a href=\"synthesis.html#recipes\">配方 E/F</a>、<a href=\"synthesis.html#continuation\">继续推演矩阵</a> 对读。",
            [
                "十层栈与七层模块表冲突时，以<strong>可对账合同与 SLA</strong> 为准。",
                "策略即代码叙事须接 <a href=\"architecture.html\">拓扑</a> 变更管道，防纸面策略。",
                "与 <a href=\"timeline.html\">历史演进</a> 并读：哪层词汇来自哪波投资记忆。",
                "平面—议题条形图每次更新问「是否改变中小企业固定成本假设」。",
            ],
        )
        + """
    <section>
      <h2>全景标签</h2>""",
    ),
    (
        "decade.html",
        """        <text x="532" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">互证压测</text>
      </svg>
    </div>

    <div class="decade-banner">假设：算力↑ · 监管细化 · 地缘不确定 · AI 嵌入生产</div>""",
        """        <text x="532" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">互证压测</text>
      </svg>
    </div>

"""
        + sec(
            "decade",
            "十年展望",
            "六维本轮每条补<strong>「最可能互相卡死的另一维」</strong>一句；三色条迁移须解释机制，不单换色；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 时间族行。",
            [
                "与 <a href=\"national-strategy-opinion.html\">战略·舆情</a>：治理维与双轨是否同一词汇两套节拍。",
                "与 <a href=\"decade-scenes.html\">十年场景</a>：每维至少指到一个场景切片锚点。",
                "职业维与 <a href=\"work-infra-energy.html\">职基能</a> 用工叙事对读，防技能叙事脱离电网。",
                "地域维与 <a href=\"risk-geo.html\">地缘热力</a> 对照，标明友岸叙事是否已进采购。",
            ],
        )
        + """
    <div class="decade-banner">假设：算力↑ · 监管细化 · 地缘不确定 · AI 嵌入生产</div>""",
    ),
    (
        "timeline.html",
        """        <text x="488" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">文末示意</text>
      </svg>
    </div>

    <section>
      <h2>五代演进（横向轴）</h2>""",
        """        <text x="488" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">文末示意</text>
      </svg>
    </div>

"""
        + sec(
            "timeline",
            "历史演进",
            "五代本轮强调<strong>叠加非替代</strong>：每条写清「仍与谁并存」；词汇锁定如何绑架组织 KPI；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 时间族。",
            [
                "为每代补<strong>仍在付账单的技术债</strong>典型一条（许可、维保、专用硬件）。",
                "与 <a href=\"past-future.html\">廿年视角</a>：过去十年主轴是否在本轴找到对应波次。",
                "与 <a href=\"model.html\">分层</a>：当前默认 L 层词汇来自哪两波叠床。",
                "滚动时间轴阅读时标注读者所在组织的<strong>主要遗留代际</strong>。",
            ],
        )
        + """
    <section>
      <h2>五代演进（横向轴）</h2>""",
    ),
    (
        "past-future.html",
        """        <text x="406" y="40" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">结构 + 情景</text>
      </svg>
    </div>

    <div class="yy-banner">""",
        """        <text x="406" y="40" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">结构 + 情景</text>
      </svg>
    </div>

"""
        + sec(
            "yy",
            "廿年视角",
            "双窗本轮各写<strong>一条制度/地缘否决技术乐观的机制链</strong>；雷达位移须可观察；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>。",
            [
                "过去十年 pill 与未来十年 pill 各挑<strong>一个可核对公开线索类型</strong>（采购、立法、事故通报）。",
                "与 <a href=\"decade.html\">十年展望</a> 对齐：2026—2036 窗是否被廿年叙事覆盖或矛盾，须解释。",
                "情景位移时禁止单点终局，至少两枝结构与征候。",
                "与 <a href=\"nexus.html\">立体联结</a> 尺度并读：国家叙事与客厅体验的时差。",
            ],
        )
        + """
    <div class="yy-banner">""",
    ),
    (
        "decade-scenes.html",
        """        <text x="612" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">0—3…7—10</text>
      </svg>
    </div>

    <div class="decade-banner">与六维表共用假设：算力↑ · 监管细化 · 地缘不确定 · AI 嵌入生产</div>""",
        """        <text x="612" y="44" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">0—3…7—10</text>
      </svg>
    </div>

"""
        + sec(
            "scenes",
            "十年场景",
            "八境本轮每境补<strong>「钩子问题 → 机制叠层 → 一条可见征候」</strong>缩句；与 <a href=\"decade.html\">六维表</a>、<a href=\"synthesis.html#continuation\">继续推演矩阵</a> 场景行对读。",
            [
                "三帧画面与 <a href=\"synthesis-methods.html#deep-lens\">§13</a> 镜头切换可互换，但须回扣同一变量。",
                "跨境/政务境与 <a href=\"national-strategy-opinion.html\">战略·舆情</a> 对时：文件与 UI 哪边先行。",
                "家庭/教育境与 <a href=\"decade-us.html\">十年之问</a> 四问交叉标注不同步点。",
                "热力矩阵增格时同步想是否应写入 <a href=\"synthesis-extensions.html#matrix\">§7</a>。",
            ],
        )
        + """
    <div class="decade-banner">与六维表共用假设：算力↑ · 监管细化 · 地缘不确定 · AI 嵌入生产</div>""",
    ),
    (
        "decade-us.html",
        """        <text x="604" y="48" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">治理叙事</text>
      </svg>
    </div>

    <nav aria-label="本页目录">""",
        """        <text x="604" y="48" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">治理叙事</text>
      </svg>
    </div>

"""
        + sec(
            "dcus",
            "十年之问",
            "四问本轮强制写<strong>同一家庭日程下的四段不同步</strong>（不必同一答案）；要做/不要/活得较好与 <a href=\"synthesis.html#criteria\">§2</a> 对表；链 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>。",
            [
                "我们/孩子两问与 <a href=\"edu-nexus.html\">教育纵轴</a> 数据权力句互链。",
                "家庭问与路由器/账号/账单等<strong>可观察物</strong>绑定，少用抽象「焦虑」。",
                "国家问与 <a href=\"national-strategy-opinion.html\">双轨</a> 并读：叙事是否已进预算。",
                "不同步节（§5）补一条<strong>短中长</strong>各自最典型的错峰例子。",
            ],
        )
        + """
    <nav aria-label="本页目录">""",
    ),
    (
        "synthesis-extensions.html",
        """        <text x="604" y="52" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">形态切片</text>
      </svg>
    </div>
    <section id="stack-domains">""",
        """        <text x="604" y="52" text-anchor="middle" fill="#5c6b7e" font-size="7" font-family="Noto Sans SC,sans-serif">形态切片</text>
      </svg>
    </div>

"""
        + sec(
            "synext",
            "扩展图景",
            "§6—§9 本轮统一纪律：<strong>每增一域/一行/一簇，必写中介变量与判据编号</strong>；与主篇 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>「三页」行对读。",
            [
                "五域 I—V 与 <a href=\"lab.html\">沙盘</a> 因子名尽量同文，避免翻译损耗。",
                "§7 新行模板：焦点句 + 规制/资本/舆论三向至少其一落地。",
                "§8 三簇与 §9 五维：簇—维映射写清，防「簇是簇、维是维」两张皮。",
                "与 <a href=\"national-strategy-opinion.html#integrated-deduction\">多源台</a> 互链时标明条目编号习惯。",
            ],
        )
        + """
    <section id="stack-domains">""",
    ),
    (
        "synthesis-methods.html",
        """      </ul>
    </nav>
    <section id="perpetual">""",
        """      </ul>
    </nav>
"""
        + sec(
            "synmeth",
            "方法与透镜",
            "§11—§13 本轮：梳理/扩展/推演三环各配<strong>一条「完成定义」</strong>；办法表与 RESEARCH_METHODS_MAP 同学名；对表 <a href=\"synthesis.html#continuation\">继续推演矩阵</a>。",
            [
                "§12 每手法试标 <strong>A/B/C 证据强度</strong>与「本手法不能回答什么」。",
                "§13 四穿透后必须回到 <a href=\"synthesis.html#criteria\">§2</a> 指名使用了哪几条判据。",
                "插槽⑦—⑩ 变更时同步 <a href=\"evolvable-architecture.html\">可进化架构</a> 映射一节。",
                "持续迭代笔记建议链到具体 <code>signals[].id</code> 或 §7 表行草稿。",
            ],
        )
        + """
    <section id="perpetual">""",
    ),
    (
        "index.html",
        """      <aside class="card site-data-live-strip-host" data-site-data-live aria-live="polite" hidden></aside>
    </div>

    <div class="hub-map" role="region" aria-label="模块关系示意">""",
        """      <aside class="card site-data-live-strip-host" data-site-data-live aria-live="polite" hidden></aside>
    </div>

"""
        + sec(
            "index",
            "总览",
            "总览本轮强调<strong>入口纪律</strong>：从三问出发，经 <a href=\"modules-map.html\">模块图谱</a> 或 <a href=\"synthesis.html#continuation\">继续推演矩阵</a> 选题，再下钻分页；避免只读卡片不读判据。",
            [
                "新读者默认路径：<a href=\"nexus.html\">立体联结</a> → <a href=\"synthesis.html#criteria\">§2</a> → 议题相关分页。",
                "维护者路径：分析快照 → manifest → 选一矩阵行改正文或 JSON。",
                "hub 卡片与 <a href=\"evolution-loop.html\">闭环</a> 同周期检查，防链接漂移。",
                "单页归档仅作备用索引，深度推演以分页与三问为准。",
            ],
        )
        + """
    <div class="hub-map" role="region" aria-label="模块关系示意">""",
    ),
]


def main() -> int:
    failed = []
    for name, old, new in PATCHES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        if "site-round-extension" in text and "ext-round-" in text:
            print(f"skip (already patched): {name}")
            continue
        if old not in text:
            failed.append(name)
            print(f"MISS anchor: {name}", file=sys.stderr)
            continue
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        print(f"ok: {name}")
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
