/**
 * 分析引擎仪表盘：读取 analysis-snapshot.json，渲染热力与共现。
 */
(function () {
  "use strict";

  var URL_SNAP = "assets/analysis-snapshot.json";
  var URL_TRENDS = "assets/sediment-trends.json";
  var URL_HINT_DECISIONS = "assets/evolution-hint-decisions.json";

  var ACTION_LABEL = { done: "已落实", rejected: "已否决", deferred: "延期" };

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
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
      '</span><div class="analysis-bar-track"><div class="analysis-bar-fill" style="width:' +
      pct +
      '%"></div></div>';
    return row;
  }

  function render(container, data) {
    if (!container || !data) return;
    container.innerHTML = "";

    var meta = document.createElement("p");
    meta.className = "muted analysis-snap-meta";
    var src0 = data.sources || {};
    var metaHtml =
      "生成时间 <time>" +
      esc(data.generated_at || "—") +
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
    meta.innerHTML = metaHtml;
    container.appendChild(meta);

    var gaps = data.hint_closure_gaps;
    if (Array.isArray(gaps) && gaps.length) {
      var gbox = document.createElement("div");
      gbox.className = "card analysis-closure-gaps";
      gbox.setAttribute("role", "status");
      var gh = document.createElement("h4");
      gh.style.marginTop = "0";
      gh.textContent = "规则闭环缺口（待落实或否决并记录）";
      gbox.appendChild(gh);
      var gp = document.createElement("p");
      gp.className = "muted";
      gp.style.fontSize = "0.82rem";
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
      h4.style.marginTop = "0";
      h4.textContent = "自我进化提示（规则引擎）";
      hc.appendChild(h4);
      var ul = document.createElement("ul");
      ul.className = "muted";
      ul.style.margin = "0";
      ul.style.fontSize = "0.88rem";
      ul.style.lineHeight = "1.75";
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
            sp.className = "muted";
            sp.style.marginLeft = "0.35em";
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
    wrap.style.marginTop = "1rem";
    var h4 = document.createElement("h4");
    h4.style.marginTop = "0";
    h4.textContent = "提示项处理记录（evolution-hint-decisions）";
    wrap.appendChild(h4);
    var p0 = document.createElement("p");
    p0.className = "muted";
    p0.style.fontSize = "0.82rem";
    p0.style.marginTop = "0.25rem";
    p0.textContent =
      "双周闭环中落实或否决规则提示时，请在仓库内追加 JSON 记录（make validate 会校验）。";
    wrap.appendChild(p0);
    var ul = document.createElement("ul");
    ul.className = "muted analysis-hint-decisions-list";
    ul.style.fontSize = "0.88rem";
    ul.style.lineHeight = "1.75";
    ul.style.marginBottom = "0";
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
      ul2.style.fontSize = "0.88rem";
      ul2.style.margin = "0";
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
    var n = t.summary.entry_count || 0;
    if (n < 1 && (!t.longterm_hints || !t.longterm_hints.length)) return;

    var wrap = document.createElement("div");
    wrap.className = "card analysis-trends";
    wrap.style.marginTop = "1.25rem";
    var h = document.createElement("h3");
    h.style.marginTop = "0";
    h.textContent = "长期沉淀与趋势（自 sediment）";
    wrap.appendChild(h);

    var meta = document.createElement("p");
    meta.className = "muted";
    meta.style.fontSize = "0.88rem";
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
      esc(t.generated_at || "—") +
      "</time>";
    wrap.appendChild(meta);

    var hints = t.longterm_hints || [];
    if (hints.length) {
      var ul = document.createElement("ul");
      ul.className = "muted";
      ul.style.fontSize = "0.88rem";
      ul.style.lineHeight = "1.75";
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
      sec.className = "analysis-panel";
      sec.style.marginTop = "0.75rem";
      var h4 = document.createElement("h4");
      h4.style.fontSize = "1rem";
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

    container.appendChild(wrap);
  }

  function load() {
    var el = document.getElementById("analysis-dashboard");
    fetch(URL_SNAP)
      .then(function (r) {
        if (!r.ok) throw new Error("snap");
        return r.json();
      })
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
        return fetch(URL_TRENDS);
      })
      .then(function (r) {
        if (!r.ok) return null;
        return r.json();
      })
      .then(function (trends) {
        if (!trends) return;
        var el = document.getElementById("analysis-dashboard");
        renderTrends(el, trends);
      })
      .catch(function () {
        var el = document.getElementById("analysis-dashboard");
        if (el && !el.querySelector(".analysis-snap-meta")) {
          if (window.location.protocol === "file:") {
            el.innerHTML =
              '<p class="muted"><strong>无法加载 JSON：</strong>当前为 <code>file://</code>，请用本地 HTTP 或部署后的 <strong>https</strong> 打开。生成数据：<code>make analyze</code> 或 <code>python3 scripts/analysis_engine.py</code>。</p>';
          } else {
            el.innerHTML =
              '<p class="muted">无法加载 <code>assets/analysis-snapshot.json</code>。请在仓库根运行 <code>make analyze</code>（或 <code>python3 scripts/analysis_engine.py</code>）后提交/部署；并确认 <code>assets/</code> 路径正确。</p>';
          }
        }
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
