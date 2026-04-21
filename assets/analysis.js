/**
 * 分析引擎仪表盘：读取 analysis-snapshot.json，渲染热力与共现。
 *
 * @typedef {Object} AnalysisRunLineage
 * @property {string} [run_id] 单次 analyze 标识（与沉淀/SQLite 对齐）
 * @property {string} [repo_revision] git short HEAD 或 unknown
 *
 * @typedef {Object} AnalysisSourcesMeta
 * @property {number} [combined_for_analysis] 合并后参与统计的条数
 * @property {number} [candidates_in_file] 候选文件内条数
 * @property {Object<string,number>} [candidate_review_breakdown] pending / noise / queued_for_manifest
 * @property {Object} [hint_decisions] total、by_action（done / rejected / deferred）
 *
 * @typedef {Object} AnalysisSnapshot
 * @property {number} schema_version
 * @property {string} generated_at ISO 时间（北京时间 +08:00，或历史 UTC「Z」）
 * @property {AnalysisRunLineage} [run]
 * @property {AnalysisSourcesMeta} [sources]
 * @property {Array<{page:string,count:number}>} [module_heat]
 * @property {Array<{factor:string,count:number}>} [factor_heat]
 * @property {Object<string,number>} [kind_distribution]
 * @property {Array<{pair:string[],count:number}>} [cooccurrence]
 * @property {Array<string|Object>} [evolution_hints]
 * @property {Array<{rule_id:string,text?:string}>} [hint_closure_gaps]
 */
(function () {
  "use strict";

  var URL_SNAP = "assets/analysis-snapshot.json";
  var URL_TRENDS = "assets/sediment-trends.json";
  var URL_HINT_DECISIONS = "assets/evolution-hint-decisions.json";
  var URL_AI_OVERLAY = "assets/ai-analysis-overlay.json";
  var BEIJING_TZ = "Asia/Shanghai";

  var ACTION_LABEL = { done: "已落实", rejected: "已否决", deferred: "延期" };
  var KIND_LABEL = {
    opinion: "舆情",
    policy: "政策",
    law: "法规线索",
    market: "市场",
    tech: "技术",
    unknown: "其他",
  };

  /** @type {AnalysisSnapshot|null} */
  var currentSnap = null;
  /** @type {Record<string, unknown>|null} */
  var currentTrends = null;

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  /** @param {string|number|null|undefined} isoOrMs */
  function formatTimeBeijingReadable(isoOrMs) {
    if (isoOrMs == null || isoOrMs === "") return "—";
    var ms = typeof isoOrMs === "number" ? isoOrMs : Date.parse(String(isoOrMs));
    if (isNaN(ms)) return String(isoOrMs);
    try {
      return (
        new Date(ms).toLocaleString("zh-CN", {
          timeZone: BEIJING_TZ,
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: false,
        }) + "（北京时间）"
      );
    } catch (_) {
      return String(isoOrMs);
    }
  }

  function barRow(label, count, max) {
    var pct = max > 0 ? Math.round((count / max) * 100) : 0;
    var row = document.createElement("div");
    row.className = "analysis-bar-row";
    row.innerHTML =
      '<span class="analysis-bar-label">' +
      esc(label) +
      '</span><span class="analysis-bar-count">' +
      esc(String(count)) +
      '</span><div class="analysis-bar-track"><div class="analysis-bar-fill"></div></div>';
    row
      .querySelector(".analysis-bar-fill")
      .style.setProperty("--analysis-bar-pct", String(pct));
    return row;
  }

  function kindLabel(k) {
    return KIND_LABEL[k] || k || "—";
  }

  /**
   * 聚合解读：把快照中的来源、热力、共现、类型、提示条数拼成可读摘要（展示 + 供导出）。
   * @param {AnalysisSnapshot} data
   * @returns {string[]}  bullet 文本
   */
  function aggregateSnapshotLines(data) {
    var lines = [];
    var src = data.sources || {};
    var n = src.combined_for_analysis != null ? src.combined_for_analysis : 0;
    var mm = src.manifest_signals != null ? src.manifest_signals : 0;
    var cc = src.candidate_signals != null ? src.candidate_signals : 0;
    lines.push(
      "合并分析样本 **" +
        n +
        "** 条（已入库 manifest **" +
        mm +
        "** · 参与统计的候选 **" +
        cc +
        "**）。"
    );
    var mod = (data.module_heat || []).slice(0, 5);
    if (mod.length) {
      lines.push(
        "模块页映射热度领先：" +
          mod
            .map(function (x) {
              return "`" + x.page + "`（" + x.count + "）";
            })
            .join("、") +
          "。"
      );
    }
    var fac = (data.factor_heat || []).slice(0, 5);
    if (fac.length) {
      lines.push(
        "沙盘因子热度领先：" +
          fac
            .map(function (x) {
              return "`" + x.factor + "`（" + x.count + "）";
            })
            .join("、") +
          "。"
      );
    }
    var co = (data.cooccurrence || [])[0];
    if (co && co.pair && co.pair.length >= 2) {
      lines.push(
        "同一信号内共现最强：**" +
          co.pair[0] +
          " × " +
          co.pair[1] +
          "**（" +
          co.count +
          " 次）。"
      );
    }
    var kd = data.kind_distribution || {};
    var kk = Object.keys(kd);
    if (kk.length) {
      lines.push(
        "信号类型分布：" +
          kk
            .map(function (k) {
              return kindLabel(k) + " " + kd[k];
            })
            .join("；") +
          "。"
      );
    }
    var hints = data.evolution_hints || [];
    var gaps = data.hint_closure_gaps || [];
    if (hints.length) {
      lines.push(
        "规则 / 相较上期 / Top 因子等提示共 **" +
          hints.length +
          "** 条（详见下文清单）。"
      );
    }
    if (gaps.length) {
      lines.push(
        "规则闭环缺口 **" +
          gaps.length +
          "** 条（须在 `evolution-hint-decisions` 中落实或否决）。"
      );
    }
    if (!mod.length && !fac.length && n === 0) {
      lines.push("当前快照无热力条目；请检查 manifest / 候选是否含 `maps_to`。");
    }
    return lines;
  }

  /**
   * @param {Record<string, unknown>} t
   * @returns {string[]}
   */
  function aggregateTrendLines(t) {
    var lines = [];
    var sum = t.summary || {};
    var n = sum.entry_count != null ? sum.entry_count : 0;
    var dr = sum.date_range || {};
    if (n > 0) {
      lines.push(
        "跨日沉淀 **" +
          n +
          "** 日" +
          (dr.first && dr.last
            ? "（" + dr.first + " → " + dr.last + "）"
            : "") +
          "。"
      );
    }
    var fp = t.factor_persistence || [];
    var topF = fp
      .slice()
      .sort(function (a, b) {
        return (b.days_in_top || 0) - (a.days_in_top || 0);
      })
      .slice(0, 3);
    if (topF.length) {
      lines.push(
        "因子在多日 Top 中较持久：" +
          topF
            .map(function (r) {
              return (
                "`" +
                r.factor +
                "`（" +
                r.days_in_top +
                " 天 · 覆盖率 " +
                (r.coverage != null ? Math.round(r.coverage * 100) : "—") +
                "%）"
              );
            })
            .join("、") +
          "。"
      );
    }
    var pp = t.page_persistence || [];
    var topP = pp
      .slice()
      .sort(function (a, b) {
        return (b.days_in_top || 0) - (a.days_in_top || 0);
      })
      .slice(0, 3);
    if (topP.length) {
      lines.push(
        "页面在多日 Top 中较持久：" +
          topP
            .map(function (r) {
              return (
                "`" +
                r.page +
                "`（" +
                r.days_in_top +
                " 天 · 覆盖率 " +
                (r.coverage != null ? Math.round(r.coverage * 100) : "—") +
                "%）"
              );
            })
            .join("、") +
          "。"
      );
    }
    var lh = t.longterm_hints || [];
    if (lh.length) {
      lh.forEach(function (x) {
        if (x) lines.push(String(x));
      });
    }
    return lines;
  }

  /**
   * @param {string[]} linesMd — 含 ** ` 等 markdown 片段
   */
  function linesToPlainUl(linesMd) {
    var ul = document.createElement("ul");
    ul.className = "analysis-aggregate-list";
    linesMd.forEach(function (line) {
      var li = document.createElement("li");
      li.innerHTML = line
        .replace(/\*\*([^*]+)\*\*/g, function (_, m) {
          return "<strong>" + esc(m) + "</strong>";
        })
        .replace(/`([^`]+)`/g, function (_, m) {
          return "<code>" + esc(m) + "</code>";
        });
      ul.appendChild(li);
    });
    return ul;
  }

  function renderAggregateReport(container, data) {
    var lines = aggregateSnapshotLines(data);
    var card = document.createElement("div");
    card.className = "card analysis-aggregate-report";
    card.setAttribute("role", "region");
    card.setAttribute("aria-label", "聚合解读");

    var h4 = document.createElement("h4");
    h4.textContent = "聚合解读（当日快照）";
    card.appendChild(h4);

    var sub = document.createElement("p");
    sub.className = "muted";
    sub.textContent =
      "由分析引擎 JSON 自动拼接的定性摘要，便于扫读与复制；非预测，不替代 §2 判据与人工叙事。";
    card.appendChild(sub);

    card.appendChild(linesToPlainUl(lines));

    var trendsHold = document.createElement("div");
    trendsHold.id = "analysis-aggregate-trends";
    trendsHold.className = "analysis-aggregate-trends";
    trendsHold.hidden = true;
    card.appendChild(trendsHold);

    var btnRow = document.createElement("div");
    btnRow.className = "analysis-aggregate-actions";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn analysis-aggregate-copy-btn";
    btn.textContent = "复制 Markdown 摘要";
    btn.setAttribute(
      "title",
      "含当日快照要点；若已加载趋势则一并复制"
    );
    btn.addEventListener("click", function () {
      copyMarkdownBrief();
    });
    btnRow.appendChild(btn);
    card.appendChild(btnRow);

    container.appendChild(card);
  }

  function fillAggregateTrendsSection(t) {
    var hold = document.getElementById("analysis-aggregate-trends");
    if (!hold || !t) return;
    var tlines = aggregateTrendLines(t);
    if (!tlines.length) return;
    hold.hidden = false;
    hold.innerHTML = "";
    var h5 = document.createElement("h5");
    h5.className = "analysis-aggregate-trends-title";
    h5.textContent = "跨日补充（sediment-trends）";
    hold.appendChild(h5);
    hold.appendChild(linesToPlainUl(tlines));
  }

  function buildMarkdownBrief() {
    var parts = [];
    parts.push("# 分析引擎 · 聚合摘要\n");
    if (!currentSnap) return parts.join("");
    parts.push("> 自动生成于仪表盘；定性脚手架，非预测。\n\n");
    parts.push("## 元数据\n");
    parts.push(
      "- 生成时间: " + formatTimeBeijingReadable(currentSnap.generated_at) + "\n"
    );
    var run = currentSnap.run || {};
    if (run.run_id) parts.push("- run_id: `" + run.run_id + "`\n");
    if (run.repo_revision) parts.push("- repo_revision: `" + run.repo_revision + "`\n");
    parts.push("\n## 当日要点\n");
    aggregateSnapshotLines(currentSnap).forEach(function (L) {
      parts.push("- " + L.replace(/<\/?[^>]+>/g, "") + "\n");
    });
    if (currentTrends && aggregateTrendLines(currentTrends).length) {
      parts.push("\n## 跨日要点\n");
      aggregateTrendLines(currentTrends).forEach(function (L) {
        parts.push("- " + L + "\n");
      });
    }
    parts.push("\n---\n全页路径: `analysis-hub.html` · 数据: `assets/analysis-snapshot.json`\n");
    return parts.join("");
  }

  function copyMarkdownBrief() {
    var md = buildMarkdownBrief();
    function ok() {
      var b = document.querySelector(".analysis-aggregate-copy-btn");
      if (b) {
        var t = b.textContent;
        b.textContent = "已复制";
        setTimeout(function () {
          b.textContent = t;
        }, 2000);
      }
    }
    function fail() {
      alert("复制失败：请手动全选摘要或换用 https 环境。");
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(md).then(ok).catch(function () {
        var ta = document.createElement("textarea");
        ta.value = md;
        document.body.appendChild(ta);
        ta.select();
        try {
          document.execCommand("copy");
          ok();
        } catch (e) {
          fail();
        }
        document.body.removeChild(ta);
      });
    } else {
      var ta2 = document.createElement("textarea");
      ta2.value = md;
      document.body.appendChild(ta2);
      ta2.select();
      try {
        document.execCommand("copy");
        ok();
      } catch (e2) {
        fail();
      }
      document.body.removeChild(ta2);
    }
  }

  function render(container, data) {
    if (!container || !data) return;
    container.innerHTML = "";
    currentSnap = data;

    var meta = document.createElement("p");
    meta.className = "muted analysis-snap-meta";
    var src0 = data.sources || {};
    var metaHtml =
      "生成时间 <time>" +
      esc(formatTimeBeijingReadable(data.generated_at)) +
      "</time> · 合并分析样本 <strong>" +
      esc(String(src0.combined_for_analysis || 0)) +
      "</strong> 条";
    var br = src0.candidate_review_breakdown;
    if (br && typeof br === "object") {
      metaHtml +=
        " · 候选文件 <strong>" +
        esc(String(src0.candidates_in_file || 0)) +
        "</strong>（待审 " +
        esc(String(br.pending || 0)) +
        " · 噪点 " +
        esc(String(br.noise || 0)) +
        " · 待入库 " +
        esc(String(br.queued_for_manifest || 0)) +
        "）";
    }
    var hd = src0.hint_decisions;
    if (hd && typeof hd === "object") {
      var ba = hd.by_action || {};
      metaHtml +=
        " · 提示决策 <strong>" +
        esc(String(hd.total != null ? hd.total : 0)) +
        "</strong> 条（落实 " +
        esc(String(ba.done != null ? ba.done : 0)) +
        " · 否决 " +
        esc(String(ba.rejected != null ? ba.rejected : 0)) +
        " · 延期 " +
        esc(String(ba.deferred != null ? ba.deferred : 0)) +
        "）";
    }
    var gapList = data.hint_closure_gaps;
    if (Array.isArray(gapList) && gapList.length) {
      metaHtml +=
        ' · <span class="analysis-meta-gaps">规则闭环缺口 <strong>' +
        esc(String(gapList.length)) +
        "</strong> 条</span>";
    }
    var run = data.run;
    if (run && typeof run === "object") {
      var runBits = [];
      if (run.run_id != null && String(run.run_id) !== "") {
        runBits.push("<code>run_id</code> " + esc(String(run.run_id)));
      }
      if (run.repo_revision != null && String(run.repo_revision) !== "") {
        runBits.push("<code>rev</code> " + esc(String(run.repo_revision)));
      }
      if (runBits.length) {
        metaHtml +=
          ' · 运行 <span class="analysis-run-lineage">' +
          runBits.join(" · ") +
          "</span>";
      }
    }
    meta.innerHTML = metaHtml;
    container.appendChild(meta);

    renderAggregateReport(container, data);

    var gaps = data.hint_closure_gaps;
    if (Array.isArray(gaps) && gaps.length) {
      var gbox = document.createElement("div");
      gbox.className = "card analysis-closure-gaps";
      gbox.setAttribute("role", "status");
      var gh = document.createElement("h4");
      gh.textContent = "规则闭环缺口（待落实或否决并记录）";
      gbox.appendChild(gh);
      var gp = document.createElement("p");
      gp.className = "muted";
      gp.textContent =
        "以下规则已触发且配置了 track_closure，但 evolution-hint-decisions 中尚无同 rule_id 的 done/rejected。延期 deferred 不算闭环。";
      gbox.appendChild(gp);
      var gul = document.createElement("ul");
      gul.className = "analysis-closure-gaps-list";
      gaps.forEach(function (g) {
        if (!g || !g.rule_id) return;
        var gli = document.createElement("li");
        var code = document.createElement("code");
        code.className = "analysis-closure-rule-id";
        code.textContent = g.rule_id;
        gli.appendChild(code);
        if (g.text) {
          gli.appendChild(document.createTextNode(" — " + g.text));
        }
        gul.appendChild(gli);
      });
      gbox.appendChild(gul);
      container.appendChild(gbox);
    }

    var hints = data.evolution_hints || [];
    if (hints.length) {
      var hc = document.createElement("div");
      hc.className = "card analysis-hints";
      var h4 = document.createElement("h4");
      h4.textContent = "自我进化提示（规则引擎）";
      hc.appendChild(h4);
      var ul = document.createElement("ul");
      ul.className = "muted";
      hints.forEach(function (t) {
        var li = document.createElement("li");
        var text = typeof t === "string" ? t : t && t.text;
        if (!text) return;
        li.appendChild(document.createTextNode(text));
        if (typeof t === "object" && t !== null) {
          var pages = t.target_pages;
          if (Array.isArray(pages) && pages.length) {
            li.appendChild(document.createTextNode(" "));
            pages.forEach(function (p, i) {
              if (i > 0) li.appendChild(document.createTextNode(" · "));
              var a = document.createElement("a");
              a.href = p;
              a.textContent = p;
              a.className = "analysis-hint-link";
              li.appendChild(a);
            });
          }
          if (t.anchor_hint) {
            var sp = document.createElement("span");
            sp.className = "muted analysis-hint-anchor-note";
            sp.textContent = "（" + t.anchor_hint + "）";
            li.appendChild(sp);
          }
        }
        ul.appendChild(li);
      });
      hc.appendChild(ul);
      container.appendChild(hc);
    }

    renderHeatAndRest(container, data);
  }

  function renderDecisions(container, decDoc) {
    if (!container || !decDoc) return;
    var list = decDoc.decisions;
    if (!Array.isArray(list) || !list.length) return;
    var recent = list
      .filter(function (d) {
        return d && typeof d === "object";
      })
      .slice()
      .sort(function (a, b) {
        return String(b.recorded_at || "").localeCompare(
          String(a.recorded_at || "")
        );
      })
      .slice(0, 10);
    if (!recent.length) return;

    var wrap = document.createElement("div");
    wrap.className = "card analysis-hint-decisions";
    var h4 = document.createElement("h4");
    h4.textContent = "提示项处理记录（evolution-hint-decisions）";
    wrap.appendChild(h4);
    var p0 = document.createElement("p");
    p0.className = "muted";
    p0.textContent =
      "双周闭环中落实或否决规则提示时，请在仓库内追加 JSON 记录（make validate 会校验）。";
    wrap.appendChild(p0);
    var ul = document.createElement("ul");
    ul.className = "muted analysis-hint-decisions-list";
    recent.forEach(function (d) {
      var li = document.createElement("li");
      var act = ACTION_LABEL[d.action] || d.action;
      var span = document.createElement("span");
      span.className = "analysis-decision-pill";
      span.textContent = act;
      li.appendChild(span);
      li.appendChild(
        document.createTextNode(
          " · " + (d.recorded_at || "—") + " · " + (d.id || "—")
        )
      );
      if (d.rule_id) {
        li.appendChild(document.createTextNode(" "));
        var rid = document.createElement("code");
        rid.className = "analysis-decision-rule-id";
        rid.textContent = d.rule_id;
        li.appendChild(rid);
      }
      var sum = d.hint_summary || d.note;
      if (sum) {
        li.appendChild(document.createTextNode(" — "));
        var em = document.createElement("span");
        em.textContent =
          sum.length > 120 ? sum.slice(0, 120) + "…" : sum;
        li.appendChild(em);
      }
      if (d.pr_url) {
        li.appendChild(document.createTextNode(" "));
        var a = document.createElement("a");
        a.href = d.pr_url;
        a.rel = "noopener noreferrer";
        a.target = "_blank";
        a.textContent = "PR";
        li.appendChild(a);
      }
      ul.appendChild(li);
    });
    wrap.appendChild(ul);
    container.appendChild(wrap);
  }

  function renderHeatAndRest(container, data) {
    if (!container || !data) return;

    var maxM = 0;
    (data.module_heat || []).forEach(function (x) {
      if (x.count > maxM) maxM = x.count;
    });
    if (data.module_heat && data.module_heat.length) {
      var sec = document.createElement("section");
      sec.className = "analysis-panel";
      var h3 = document.createElement("h3");
      h3.textContent = "模块页热力（信号映射次数）";
      sec.appendChild(h3);
      var wrap = document.createElement("div");
      wrap.className = "analysis-bars";
      data.module_heat.forEach(function (x) {
        wrap.appendChild(barRow(x.page, x.count, maxM));
      });
      sec.appendChild(wrap);
      container.appendChild(sec);
    }

    var maxF = 0;
    (data.factor_heat || []).forEach(function (x) {
      if (x.count > maxF) maxF = x.count;
    });
    if (data.factor_heat && data.factor_heat.length) {
      var sec2 = document.createElement("section");
      sec2.className = "analysis-panel";
      var h32 = document.createElement("h3");
      h32.textContent = "沙盘因子热力";
      sec2.appendChild(h32);
      var wrap2 = document.createElement("div");
      wrap2.className = "analysis-bars";
      data.factor_heat.forEach(function (x) {
        wrap2.appendChild(barRow(x.factor, x.count, maxF));
      });
      sec2.appendChild(wrap2);
      container.appendChild(sec2);
    }

    var co = data.cooccurrence || [];
    if (co.length) {
      var sec3 = document.createElement("section");
      sec3.className = "analysis-panel";
      var h33 = document.createElement("h3");
      h33.textContent = "因子共现（同一信号内）";
      sec3.appendChild(h33);
      var tbl = document.createElement("table");
      tbl.innerHTML =
        "<thead><tr><th>因子对</th><th>次数</th></tr></thead><tbody></tbody>";
      var tb = tbl.querySelector("tbody");
      co.forEach(function (row) {
        var tr = document.createElement("tr");
        tr.innerHTML =
          "<td>" +
          esc(row.pair.join(" + ")) +
          "</td><td>" +
          esc(String(row.count)) +
          "</td>";
        tb.appendChild(tr);
      });
      sec3.appendChild(tbl);
      container.appendChild(sec3);
    }

    var kd = data.kind_distribution || {};
    var kdKeys = Object.keys(kd);
    if (kdKeys.length) {
      var sec4 = document.createElement("section");
      sec4.className = "analysis-panel";
      var h34 = document.createElement("h3");
      h34.textContent = "信号类型分布";
      sec4.appendChild(h34);
      var ul2 = document.createElement("ul");
      ul2.className = "muted kind-distribution";
      kdKeys.forEach(function (k) {
        var li = document.createElement("li");
        li.textContent = k + "：" + kd[k];
        ul2.appendChild(li);
      });
      sec4.appendChild(ul2);
      container.appendChild(sec4);
    }
  }

  function renderTrends(container, t) {
    if (!container || !t || !t.summary) return;
    currentTrends = t;
    fillAggregateTrendsSection(t);

    var n = t.summary.entry_count || 0;
    if (n < 1 && (!t.longterm_hints || !t.longterm_hints.length)) return;

    var wrap = document.createElement("div");
    wrap.className = "card analysis-trends";
    var h = document.createElement("h3");
    h.textContent = "长期沉淀与趋势（自 sediment）";
    wrap.appendChild(h);

    var meta = document.createElement("p");
    meta.className = "muted";
    var dr = t.summary.date_range;
    meta.innerHTML =
      "沉淀日数 <strong>" +
      esc(String(n)) +
      "</strong>" +
      (dr && dr.first
        ? " · 自 <time>" +
          esc(dr.first) +
          "</time> 至 <time>" +
          esc(dr.last) +
          "</time>"
        : "") +
      " · 生成 <time>" +
      esc(formatTimeBeijingReadable(t.generated_at)) +
      "</time>";
    wrap.appendChild(meta);

    var hints = t.longterm_hints || [];
    if (hints.length) {
      var ul = document.createElement("ul");
      ul.className = "muted";
      hints.forEach(function (line) {
        var li = document.createElement("li");
        li.textContent = line;
        ul.appendChild(li);
      });
      wrap.appendChild(ul);
    }

    function smallTable(title, rows, keyField) {
      if (!rows || !rows.length) return;
      var sec = document.createElement("section");
      sec.className = "analysis-panel analysis-panel--stack";
      var h4 = document.createElement("h4");
      h4.textContent = title;
      sec.appendChild(h4);
      var tbl = document.createElement("table");
      tbl.innerHTML =
        "<thead><tr><th>" +
        (keyField === "factor" ? "因子" : "页面") +
        "</th><th>出现在 Top 的天数</th><th>覆盖率</th></tr></thead><tbody></tbody>";
      var tb = tbl.querySelector("tbody");
      rows.slice(0, 12).forEach(function (row) {
        var tr = document.createElement("tr");
        var name = row[keyField] || "—";
        tr.innerHTML =
          "<td>" +
          esc(name) +
          "</td><td>" +
          esc(String(row.days_in_top)) +
          "</td><td>" +
          esc(String(row.coverage)) +
          "</td>";
        tb.appendChild(tr);
      });
      sec.appendChild(tbl);
      wrap.appendChild(sec);
    }

    smallTable("因子持久度（多日 Top）", t.factor_persistence, "factor");
    smallTable("页面持久度（多日 Top）", t.page_persistence, "page");

    var cb = t.closure_backlog;
    if (Array.isArray(cb) && cb.length && n >= 1) {
      var csec = document.createElement("section");
      csec.className = "analysis-panel analysis-closure-backlog-panel";
      var ch = document.createElement("h4");
      ch.textContent = "规则闭环 backlog（按日 · 近 14 日）";
      csec.appendChild(ch);
      var cp = document.createElement("p");
      cp.className = "muted";
      cp.textContent =
        "缺口 = 当日 analysis 中 hint_closure_gaps 条数；决策累计 = evolution-hint-decisions 总条数（当日晚快照时刻）。";
      csec.appendChild(cp);
      var ctbl = document.createElement("table");
      ctbl.className = "analysis-closure-backlog-table";
      ctbl.innerHTML =
        "<thead><tr><th>日期</th><th>闭环缺口</th><th>决策累计</th></tr></thead><tbody></tbody>";
      var ctb = ctbl.querySelector("tbody");
      cb.forEach(function (row) {
        var tr = document.createElement("tr");
        var gn = row.hint_closure_gaps_n != null ? row.hint_closure_gaps_n : 0;
        var dt = row.hint_decisions_total != null ? row.hint_decisions_total : 0;
        tr.innerHTML =
          "<td><time>" +
          esc(String(row.date || "—")) +
          "</time></td><td>" +
          esc(String(gn)) +
          "</td><td>" +
          esc(String(dt)) +
          "</td>";
        if (gn > 0) {
          tr.className = "analysis-closure-backlog-row--gaps";
        }
        ctb.appendChild(tr);
      });
      csec.appendChild(ctbl);
      wrap.appendChild(csec);
    }

    container.appendChild(wrap);
  }

  /**
   * 可选：渲染 AI/辅助解读叠加层（独立 JSON；与快照 run_id 对读）。
   * @param {HTMLElement} container
   * @param {Record<string, unknown>} overlay
   */
  function renderAiOverlay(container, overlay) {
    if (!container || !overlay || typeof overlay !== "object") return;
    var snapRun =
      currentSnap && currentSnap.run && currentSnap.run.run_id
        ? String(currentSnap.run.run_id)
        : "";
    var srcRun = overlay.source_run_id != null ? String(overlay.source_run_id) : "";
    var sec = document.createElement("section");
    sec.className = "analysis-panel analysis-ai-overlay";
    sec.setAttribute("aria-labelledby", "analysis-ai-overlay-title");
    var h3 = document.createElement("h3");
    h3.id = "analysis-ai-overlay-title";
    h3.textContent = "AI 辅助解读（可选叠加层）";
    sec.appendChild(h3);
    var prov = overlay.provider || {};
    var meta = document.createElement("p");
    meta.className = "muted analysis-ai-overlay-meta";
    meta.innerHTML =
      "来源：<code>assets/ai-analysis-overlay.json</code> · provider <code>" +
      esc(String(prov.kind || "—")) +
      "</code> / model <code>" +
      esc(String(prov.model || "—")) +
      "</code> · 生成 <time>" +
      esc(formatTimeBeijingReadable(overlay.generated_at)) +
      "</time>";
    sec.appendChild(meta);
    if (snapRun && srcRun && snapRun !== srcRun) {
      var warn = document.createElement("p");
      warn.className = "muted analysis-ai-overlay-warn";
      warn.textContent =
        "提示：overlay 的 source_run_id 与当前页快照 run_id 不一致，可能为旧文件或未刷新。";
      sec.appendChild(warn);
    }
    var disc = document.createElement("p");
    disc.className = "muted analysis-ai-overlay-disclaimer";
    disc.textContent = String(overlay.disclaimer_zh || "");
    sec.appendChild(disc);
    if (overlay.summary_md) {
      var sum = document.createElement("div");
      sum.className = "analysis-ai-overlay-summary";
      sum.textContent = String(overlay.summary_md);
      sec.appendChild(sum);
    }
    var sections = Array.isArray(overlay.sections) ? overlay.sections : [];
    sections.forEach(function (s) {
      if (!s || typeof s !== "object") return;
      var h4 = document.createElement("h4");
      h4.className = "analysis-ai-overlay-section-title";
      h4.textContent = String(s.title_zh || "—");
      sec.appendChild(h4);
      var body = document.createElement("div");
      body.className = "analysis-ai-overlay-body";
      body.textContent = String(s.body_md != null ? s.body_md : "");
      sec.appendChild(body);
    });
    container.appendChild(sec);
  }

  function fetchSnapshotShared() {
    if (window.SiteDataBus && typeof SiteDataBus.loadSnapshot === "function") {
      return SiteDataBus.loadSnapshot();
    }
    return fetch(URL_SNAP).then(function (r) {
      if (!r.ok) throw new Error("snap");
      return r.json();
    });
  }

  function fetchTrendsShared() {
    if (window.SiteDataBus && typeof SiteDataBus.loadTrends === "function") {
      return SiteDataBus.loadTrends();
    }
    return fetch(URL_TRENDS).then(function (r) {
      if (!r.ok) return null;
      return r.json();
    });
  }

  function load() {
    var el = document.getElementById("analysis-dashboard");
    if (!el) return;
    el.setAttribute("aria-busy", "true");
    el.classList.add("analysis-dashboard--loading");
    el.innerHTML =
      '<p class="muted analysis-dashboard-loading">正在加载分析快照与仪表盘…</p>';

    fetchSnapshotShared()
      .then(function (data) {
        render(el, data);
        return fetch(URL_HINT_DECISIONS)
          .then(function (r) {
            return r.ok ? r.json() : { decisions: [] };
          })
          .catch(function () {
            return { decisions: [] };
          });
      })
      .then(function (decDoc) {
        renderDecisions(el, decDoc);
        return fetchTrendsShared();
      })
      .then(function (trends) {
        if (trends) renderTrends(el, trends);
        return fetch(URL_AI_OVERLAY)
          .then(function (r) {
            if (!r.ok) return null;
            return r.json();
          })
          .catch(function () {
            return null;
          });
      })
      .then(function (overlay) {
        if (overlay) renderAiOverlay(el, overlay);
      })
      .catch(function () {
        if (el && !el.querySelector(".analysis-snap-meta")) {
          if (window.location.protocol === "file:") {
            el.innerHTML =
              '<p class="muted"><strong>无法加载 JSON：</strong>当前为 <code>file://</code>，请用本地 HTTP 或部署后的 <strong>https</strong> 打开。生成数据：<code>make analyze</code> 或 <code>python3 scripts/analysis_engine.py</code>。</p>';
          } else {
            el.innerHTML =
              '<p class="muted">无法加载 <code>assets/analysis-snapshot.json</code>。请在仓库根运行 <code>make analyze</code>（或 <code>python3 scripts/analysis_engine.py</code>）后提交/部署；并确认 <code>assets/</code> 路径正确。</p>';
          }
        }
      })
      .finally(function () {
        el.classList.remove("analysis-dashboard--loading");
        el.setAttribute("aria-busy", "false");
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
