(function () {
  var factors = [
    {
      id: "reg",
      label: "强监管 / 关基",
      hints: [
        "优先：数据分级分类、审计日志标准、运维与密钥管辖条款书面化。",
        "架构：区域 cell + 明确网关；监管报送或审计导出接口插件化。",
        "组织：安全/合规在变更门禁中有签字权或带条件通过机制。"
      ]
    },
    {
      id: "geo",
      label: "地缘紧张 / 冲突风险",
      hints: [
        "网络：多路径、多 POP；关键解析与证书的韧性设计。",
        "供应商：识别「法律上可单方面切断」的依赖，准备数据导出与 IaC exit。",
        "运营：runbook 属地化，减少对单一跨境差旅链路的依赖。"
      ]
    },
    {
      id: "sanction",
      label: "制裁 / 长臂管辖敞口",
      hints: [
        "合同：多司法辖区主体与支付路径情景分析；技术支持与更新条款复审。",
        "技术：替代云/API 冷备、密钥与镜像可迁移；避免隐性单一外方锁定。",
        "合规：客户与供应链筛查流程与架构选型同步记录。"
      ]
    },
    {
      id: "ai",
      label: "AI / 大模型爆发采用",
      hints: [
        "数据：训练/推理数据管线与 RAG 知识库的权限与同源审计。",
        "安全：提示注入、模型制品与权重纳入供应链与权限模型。",
        "成本：推理与 FinOps 挂钩，队列与配额与业务分级一致。"
      ]
    },
    {
      id: "capital",
      label: "资本紧缩 / 估值承压",
      hints: [
        "产品：单位经济与现金流优先；合规包可模块化售卖而非无限定制。",
        "技术：减少「为叙事而全栈自研」，优先可替换托管与开源基线。",
        "治理：董事会材料中显式披露安全与地缘依赖，避免尽调惊喜。"
      ]
    },
    {
      id: "enterprise",
      label: "大客户 / 准入驱动",
      hints: [
        "交付：SOC2/等保/行业认证路线图与数据流图对外一致。",
        "架构：租户隔离、日志驻留与客户自带密钥选项。",
        "商业：定价中单列驻场、审计与韧性，避免吞噬毛利。"
      ]
    },
    {
      id: "global",
      label: "激进全球化 / 多区域扩张",
      hints: [
        "策略：先进法律清晰、支付顺畅的样板市场，再攻硬法域。",
        "架构：策略模板 + 本地参数，避免一国一套黑盒。",
        "运营：总部—区域责任边界与数据地图同源维护。"
      ]
    },
    {
      id: "talent",
      label: "关键人才稀缺 / 英雄主义",
      hints: [
        "组织：文档化、二级支持、禁止单人独占核心密钥与发布。",
        "个人：T 型能力 + 合规翻译能力；声誉与客户类型纳入职业风险。",
        "平台：自助服务降低对少数专家的调用频率。"
      ]
    },
    {
      id: "oss_export",
      label: "开源模型栈 × 出口/备案收紧",
      hints: [
        "制品：内网镜像、许可清单、训练区/推理区与「可下载权重」三分离；CI 日志可对账。",
        "人力：JD 与出境设备策略写清；影子权重与声明模型族不一致时按事故预案升级。",
        "架构：合规托管与自研双栈的 API 路由、密钥与审计边界分 Cell，接综合推演·配方 Q。"
      ]
    },
    {
      id: "attention_minors",
      label: "未成年人注意力 / 家校屏幕治理",
      hints: [
        "产品：校采与家长端避免与 Feed 同源增长技艺混用；时长与广告加载可审计。",
        "家庭：路由器白名单、系统级屏幕策略与校规显式对齐，减少「只说不用」的摩擦。",
        "治理：政策讨论带上技术可行性与阶层公平（纯净栈订阅），接综合推演·配方 R。"
      ]
    },
    {
      id: "water_cooling",
      label: "取水 / 冷却水平衡 / 园区邻避",
      hints: [
        "设施：环评与 SLA 同步写清取水许可 tier、中水比例、枯水季限流与蒸发量；与 PUE 并列披露。",
        "选址：干旱风险升高时评估干冷、浸没式或异地推理分流，对接架构·数据重力与 Cell。",
        "舆情：与「让电」叙事并备「让水」问答口径，接综合推演·配方 S。"
      ]
    },
    {
      id: "gig_multiemployer",
      label: "平台用工 × 多雇主 / 社保锚定",
      hints: [
        "合同：岗位描述写清默认承保方、工伤与医保缴纳主体；AI 派单与人工仲裁责任切分附件化。",
        "跨境：远程 payroll 与支付制裁、数据驻留同屏；维护 payroll Cell 图并与 Q 双栈对齐。",
        "商业：评估「正式化反弹」情景下平台固定成本，接综合推演·配方 T。"
      ]
    },
    {
      id: "esg_compute_carbon",
      label: "ESG 披露 × 算力碳足迹 / 绿证对账",
      hints: [
        "计量：机柜/租户级 kWh 与时间粒度对齐推理队列；限电时段占比可审计，接 P/S。",
        "披露：范围 2/3 与云侧分配因子写进合同；警惕 REC 与实时 dispatch 脱节，接综合推演·配方 U。",
        "资本：IR 与尽调复制气候诉点；中小企业评估托管 ESG 模板成本。"
      ]
    },
    {
      id: "dual_use_research",
      label: "双重用途 × 科研数据 / 出境审查",
      hints: [
        "合规：数据集字段、合作方国籍、算力位置可点名；联合训练走白名单走廊，接综合推演·配方 V。",
        "组织：高校分区科研栈（对外区/内需区）与伦理审查前置；防范影子协作与作者列表不一致。",
        "战略：区域小循环内互认数据与算力券 vs 区外高摩擦，与 Q、K 友岸叙事对照。"
      ]
    }
  ];

  var grid = document.getElementById("simOptions");
  var out = document.getElementById("simOutput");
  if (!grid || !out) return;

  factors.forEach(function (f) {
    var wrap = document.createElement("div");
    wrap.className = "sim-option";
    var inp = document.createElement("input");
    inp.type = "checkbox";
    inp.id = "f_" + f.id;
    inp.value = f.id;
    var lab = document.createElement("label");
    lab.htmlFor = "f_" + f.id;
    lab.textContent = f.label;
    inp.addEventListener("change", render);
    wrap.appendChild(inp);
    wrap.appendChild(lab);
    grid.appendChild(wrap);
  });

  function selectedFactors() {
    return factors.filter(function (f) {
      var el = document.getElementById("f_" + f.id);
      return el && el.checked;
    });
  }

  function render() {
    var sel = [];
    factors.forEach(function (f) {
      var el = document.getElementById("f_" + f.id);
      if (el && el.checked) sel.push(f);
    });

    if (sel.length === 0) {
      out.innerHTML =
        '<h4>合成启示</h4><p class="muted" style="margin:0">请至少选择一个因子。</p>';
      return;
    }

    var merged = [];
    sel.forEach(function (f) {
      f.hints.forEach(function (h) {
        merged.push(h);
      });
    });

    if (sel.length >= 3) {
      merged.push(
        "【叠加】多因子同时成立时，单独可承受的风险可能合并为不可承受——更新风险登记册并做一次跨部门桌面推演。"
      );
    }

    if (
      sel.some(function (f) {
        return f.id === "geo" || f.id === "sanction";
      }) &&
      sel.some(function (f) {
        return f.id === "global";
      })
    ) {
      merged.push(
        "【地缘 × 全球化】扩张节奏与数据驻留策略绑定：每新区域先完成数据流 + 子处理者 + 支付路径三联表。"
      );
    }

    if (
      sel.some(function (f) {
        return f.id === "reg";
      }) &&
      sel.some(function (f) {
        return f.id === "ai";
      })
    ) {
      merged.push(
        "【监管 × AI】将模型与提示审计纳入个人信息与重要数据处理记录；RAG 检索前授权过滤必做。"
      );
    }

    var ul = document.createElement("ul");
    merged.forEach(function (line) {
      var li = document.createElement("li");
      li.textContent = line;
      ul.appendChild(li);
    });
    out.innerHTML = "";
    var h4 = document.createElement("h4");
    h4.textContent = "合成启示（已选 " + sel.length + " 项）";
    out.appendChild(h4);
    out.appendChild(ul);
  }

  document.getElementById("simClear").addEventListener("click", function () {
    factors.forEach(function (f) {
      var el = document.getElementById("f_" + f.id);
      if (el) el.checked = false;
    });
    render();
  });

  document.getElementById("simRandom").addEventListener("click", function () {
    factors.forEach(function (f) {
      var el = document.getElementById("f_" + f.id);
      if (el) el.checked = Math.random() > 0.55;
    });
    if (selectedFactors().length === 0) {
      var pick = factors[Math.floor(Math.random() * factors.length)];
      document.getElementById("f_" + pick.id).checked = true;
    }
    render();
  });
})();

(function () {
  var steps = [
    {
      title: "第 1 步：业务与连续性目标",
      items: [
        "梳理关键业务清单与可接受降级级别（非所有系统都要同城双活）。",
        "为每类业务定义 RTO/RPO，并区分「技术恢复」与「持续运营」（含支付、合同、人力）。",
        "识别不可中断链路：身份、DNS、证书、密钥托管。"
      ]
    },
    {
      title: "第 2 步：数据分级与驻留",
      items: [
        "完成数据分类分级与个人/重要/核心数据识别（或等同框架）。",
        "画数据流图：产生、处理、存储、出境、第三方子处理者。",
        "决定 Cell 边界：按法域、按业务线或按数据敏感度切分。"
      ]
    },
    {
      title: "第 3 步：网络与身份基线",
      items: [
        "零信任假设：默认拒绝，按身份与设备姿态授权；南北向与东西向策略分工。",
        "用户与机器身份分轨：CIAM + 工作负载身份（如 SPIFFE/mTLS）。",
        "SASE/SDP 与内网微分段路线图，与远程办公场景对齐。"
      ]
    },
    {
      title: "第 4 步：算力与平台形态",
      items: [
        "在部署形态谱系中选定主形态（专有云、混合、多云、边缘协同等），允许子系统不同。",
        "平台工程：自助服务、配额、模板、黄金路径；避免「只有专家能发布」。",
        "异构算力：通用 CPU 与 GPU/推理池分层，队列与 FinOps 挂钩。"
      ]
    },
    {
      title: "第 5 步：合规与可审计性",
      items: [
        "审计日志：字段标准、留存周期、不可变存储与导出接口。",
        "密钥与运维管辖：BYOK/HYOK、谁能在何种审批下接触明文。",
        "监管与合同：技术控制与法律路径（跨境机制）一致，避免对外口径冲突。"
      ]
    },
    {
      title: "第 6 步：地缘、供应链与 Exit",
      items: [
        "列出「法律上可单方面切断」的依赖：云、SaaS、支付、技术支持。",
        "Exit：数据导出、IaC、镜像与替代 API 的冷备演练频率。",
        "品牌与采购敏感场景下的多源策略与 RFP 条款。"
      ]
    },
    {
      title: "第 7 步：运营、演练与治理闭环",
      items: [
        "技术依赖图与非技术依赖图（合同、关键人、牌照）季度对表。",
        "混沌与恢复演练：含备份篡改/勒索情景与跨部门桌面推演。",
        "董事会或管委会材料：安全、地缘、合规 KPI 与重大依赖披露。"
      ]
    }
  ];

  var dotsEl = document.getElementById("stepperDots");
  var bodyEl = document.getElementById("stepperBody");
  var progEl = document.getElementById("stepProgress");
  var btnPrev = document.getElementById("stepPrev");
  var btnNext = document.getElementById("stepNext");
  if (!dotsEl || !bodyEl || !progEl || !btnPrev || !btnNext) return;

  var idx = 0;

  function renderDots() {
    dotsEl.innerHTML = "";
    steps.forEach(function (_, i) {
      var d = document.createElement("span");
      d.className =
        "stepper-dot" + (i === idx ? " active" : i < idx ? " done" : "");
      d.title = "第 " + (i + 1) + " 步";
      d.addEventListener("click", function () {
        idx = i;
        renderStep();
      });
      dotsEl.appendChild(d);
    });
  }

  function renderStep() {
    var s = steps[idx];
    bodyEl.innerHTML = "";
    var h = document.createElement("h4");
    h.textContent = s.title;
    bodyEl.appendChild(h);
    var ul = document.createElement("ul");
    s.items.forEach(function (line) {
      var li = document.createElement("li");
      li.textContent = line;
      ul.appendChild(li);
    });
    bodyEl.appendChild(ul);
    progEl.textContent = "步骤 " + (idx + 1) + " / " + steps.length;
    btnPrev.disabled = idx === 0;
    btnNext.textContent =
      idx === steps.length - 1 ? "回到第 1 步" : "下一步";
    renderDots();
  }

  btnPrev.addEventListener("click", function () {
    if (idx > 0) {
      idx--;
      renderStep();
    }
  });

  btnNext.addEventListener("click", function () {
    if (idx === steps.length - 1) idx = 0;
    else idx++;
    renderStep();
  });

  renderStep();
})();
