/**
 * 分析引擎仪表盘：读取 analysis-snapshot.json，渲染热力与共现。
 */
(function () {
  "use strict";

  var URL_SNAP = "assets/analysis-snapshot.json";
  var URL_TRENDS = "assets/sediment-trends.json";

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
    meta.innerHTML =
      "生成时间 <time>" +
      esc(data.generated_at || "—") +
      "</time> · 合并分析样本 <strong>" +
      esc(String((data.sources && data.sources.combined_for_analysis) || 0)) +
      "</strong> 条";
    container.appendChild(meta);

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
        li.textContent = t;
        ul.appendChild(li);
      });
      hc.appendChild(ul);
      container.appendChild(hc);
    }

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
    fetch(URL_SNAP)
      .then(function (r) {
        if (!r.ok) throw new Error("snap");
        return r.json();
      })
      .then(function (data) {
        var el = document.getElementById("analysis-dashboard");
        render(el, data);
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
          el.innerHTML =
            '<p class="muted">无法加载 <code>analysis-snapshot.json</code>。请在项目根运行 <code>python3 scripts/analysis_engine.py</code> 后刷新；本地需 HTTP 服务。</p>';
        }
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
