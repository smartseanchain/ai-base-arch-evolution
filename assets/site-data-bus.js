/**
 * 全站数据总线：并行缓存加载 analysis-snapshot 与 sediment-trends；
 * 自动挂载 [data-site-data-live]（可选 data-site-data-live="snapshot-only" 跳过趋势请求）。
 */
(function () {
  "use strict";

  var URL_SNAPSHOT = "assets/analysis-snapshot.json";
  var URL_TRENDS = "assets/sediment-trends.json";
  var URL_SITE_META = "assets/site-meta.json";

  /** @type {object|null} */
  var _snap = null;
  /** @type {Promise<object>|null} */
  var _snapPromise = null;
  /** @type {object|null} */
  var _trends = null;
  /** @type {Promise<object|null>|null} */
  var _trendsPromise = null;
  /** @type {object|null} */
  var _siteMeta = null;
  /** @type {Promise<object>|null} */
  var _siteMetaPromise = null;

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function loadSnapshot() {
    if (_snap) return Promise.resolve(_snap);
    if (_snapPromise) return _snapPromise;
    _snapPromise = fetch(URL_SNAPSHOT)
      .then(function (r) {
        if (!r.ok) throw new Error("snapshot " + r.status);
        return r.json();
      })
      .then(function (d) {
        _snap = d;
        return d;
      });
    return _snapPromise;
  }

  function loadTrends() {
    if (_trendsPromise) return _trendsPromise;
    _trendsPromise = fetch(URL_TRENDS)
      .then(function (r) {
        if (!r.ok) throw new Error("trends " + r.status);
        return r.json();
      })
      .then(function (d) {
        _trends = d;
        return d;
      })
      .catch(function () {
        _trends = null;
        return null;
      });
    return _trendsPromise;
  }

  function clearCache() {
    _snap = null;
    _snapPromise = null;
    _trends = null;
    _trendsPromise = null;
    _siteMeta = null;
    _siteMetaPromise = null;
  }

  function loadSiteMeta() {
    if (_siteMeta) return Promise.resolve(_siteMeta);
    if (_siteMetaPromise) return _siteMetaPromise;
    _siteMetaPromise = fetch(URL_SITE_META)
      .then(function (r) {
        if (!r.ok) throw new Error("site-meta " + r.status);
        return r.json();
      })
      .then(function (d) {
        _siteMeta = d;
        return d;
      });
    return _siteMetaPromise;
  }

  function mountSiteMetaVersion() {
    var nodes = document.querySelectorAll("[data-site-meta-version]");
    if (!nodes.length) return;
    loadSiteMeta()
      .then(function (m) {
        if (!m || m.site_version == null || m.site_version === "") return;
        var label = "v" + String(m.site_version);
        var tip = m.codename ? String(m.codename) : "";
        if (m.summary) {
          tip = tip ? tip + " — " + String(m.summary) : String(m.summary);
        }
        if (m.updated) {
          tip = tip ? tip + " · " + String(m.updated) : String(m.updated);
        }
        for (var i = 0; i < nodes.length; i++) {
          var el = nodes[i];
          el.textContent = label;
          el.setAttribute("aria-label", "站点发布版本 " + label);
          if (tip) el.setAttribute("title", tip);
        }
        try {
          window.dispatchEvent(
            new CustomEvent("sitedatabus:meta", { detail: { meta: m } })
          );
        } catch (err) {}
      })
      .catch(function () {
        for (var j = 0; j < nodes.length; j++) {
          nodes[j].textContent = "v?";
          nodes[j].setAttribute("title", "无法加载 assets/site-meta.json");
        }
      });
  }

  /**
   * @param {object} data snapshot
   * @returns {string} HTML 片段
   */
  function briefSnapshotHtml(data) {
    var parts = [];
    var src = data.sources || {};
    var n = src.combined_for_analysis != null ? src.combined_for_analysis : 0;
    parts.push("当日合并样本 <strong>" + esc(String(n)) + "</strong> 条");
    var run = data.run || {};
    if (run.run_id) {
      parts.push("run <code>" + esc(run.run_id) + "</code>");
    }
    if (data.generated_at) {
      parts.push(
        "快照 " + esc(String(data.generated_at).slice(0, 10))
      );
    }
    var fac = (data.factor_heat || []).slice(0, 3);
    if (fac.length) {
      parts.push(
        "因子 Top：" +
          fac
            .map(function (x) {
              return "<code>" + esc(x.factor || "") + "</code>";
            })
            .join(" · ")
      );
    }
    return parts.join(" · ");
  }

  /**
   * @param {object|null} t trends doc
   * @param {string} hubHref
   * @returns {string} HTML 或 ""
   */
  function briefTrendsHtml(t, hubHref) {
    if (!t || !t.summary) return "";
    var sum = t.summary;
    var n = sum.entry_count != null ? sum.entry_count : 0;
    if (n < 1) return "";
    var dr = sum.date_range || {};
    var span =
      dr.first && dr.last
        ? esc(String(dr.first)) + " → " + esc(String(dr.last))
        : "";
    return (
      '<p class="site-data-live-strip-trends muted">' +
      "跨日沉淀 <strong>" +
      esc(String(n)) +
      "</strong> 日" +
      (span ? "（" + span + "）" : "") +
      ' · <a href="' +
      esc(hubHref) +
      '#longterm">长期趋势</a> · <a href="' +
      esc(hubHref) +
      '#dashboard">仪表盘</a></p>'
    );
  }

  function showStripLoading(el) {
    el.hidden = false;
    el.classList.add("site-data-live-strip", "site-data-live-strip--loading");
    el.setAttribute("aria-busy", "true");
    el.innerHTML =
      '<div class="site-data-live-strip-inner">' +
      '<p class="muted site-data-live-strip-loading">正在加载分析读数…</p>' +
      "</div>";
  }

  /**
   * 占位符可设 data-site-data-hub（如本页 "#dashboard"）覆盖默认 analysis-hub.html。
   * @param {HTMLElement} el
   * @param {{ hubHref?: string, showError?: boolean, trends?: boolean }} [options]
   */
  function mountLiveStrip(el, options) {
    if (!el || el.nodeType !== 1) return;
    options = options || {};
    var hubHref =
      options.hubHref != null && options.hubHref !== ""
        ? options.hubHref
        : el.getAttribute("data-site-data-hub") || "analysis-hub.html";
    var wantTrends = options.trends !== false;
    var attr = el.getAttribute("data-site-data-live");
    if (attr === "snapshot-only") wantTrends = false;

    showStripLoading(el);

    var p1 = loadSnapshot();
    var p2 = wantTrends ? loadTrends() : Promise.resolve(null);

    Promise.all([p1, p2])
      .then(function (pair) {
        var data = pair[0];
        var trends = pair[1];
        el.classList.remove("site-data-live-strip--loading");
        el.setAttribute("aria-busy", "false");
        var inner = document.createElement("div");
        inner.className = "site-data-live-strip-inner";
        inner.innerHTML =
          '<p class="site-data-live-strip-kicker">数据驱动的读数（随仓库内 JSON 与 <code>make analyze</code> 更新）</p>' +
          '<p class="site-data-live-strip-body">' +
          briefSnapshotHtml(data) +
          ' · <a href="' +
          esc(hubHref) +
          '">分析引擎仪表盘</a> · <a href="docs/SITE_DATA_UPDATE_FRAMEWORK.md">全站数据更新框架</a></p>' +
          briefTrendsHtml(trends, hubHref) +
          '<p class="muted site-data-live-strip-foot">定性摘要，非预测；各页论述仍由人工维护。</p>';
        el.textContent = "";
        el.appendChild(inner);
        try {
          window.dispatchEvent(
            new CustomEvent("sitedatabus:ready", {
              detail: { snapshot: data, trends: trends },
            })
          );
        } catch (err) {}
      })
      .catch(function () {
        el.classList.remove("site-data-live-strip--loading");
        el.setAttribute("aria-busy", "false");
        if (options.showError === false) {
          el.hidden = true;
          return;
        }
        el.classList.add("site-data-live-strip");
        el.innerHTML =
          '<div class="site-data-live-strip-inner"><p class="muted">无法加载 <code>analysis-snapshot.json</code>（请用 HTTP 打开站点，并先运行 <code>make analyze</code>）。<a href="' +
          esc(hubHref) +
          '">分析引擎</a> · <a href="docs/SITE_DATA_UPDATE_FRAMEWORK.md">更新框架</a></p></div>';
      });
  }

  function mountAllLiveStrips() {
    var nodes = document.querySelectorAll("[data-site-data-live]");
    for (var i = 0; i < nodes.length; i++) {
      mountLiveStrip(nodes[i], {});
    }
  }

  window.SiteDataBus = {
    loadSnapshot: loadSnapshot,
    loadTrends: loadTrends,
    loadSiteMeta: loadSiteMeta,
    clearCache: clearCache,
    mountLiveStrip: mountLiveStrip,
    mountAllLiveStrips: mountAllLiveStrips,
    getCachedSnapshot: function () {
      return _snap;
    },
    getCachedTrends: function () {
      return _trends;
    },
  };

  function boot() {
    mountAllLiveStrips();
    mountSiteMetaVersion();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
