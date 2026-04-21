/**
 * 全站数据总线：并行缓存加载 analysis-snapshot、sediment-trends、site-meta；
 * 可选加载 assets/site-search-index.json 并在 [data-site-quick-search] 提供轻量页题搜索。
 * 自动挂载 [data-site-data-live]（可选 data-site-data-live="snapshot-only" 跳过趋势请求）。
 */
(function () {
  "use strict";

  var URL_SNAPSHOT = "assets/analysis-snapshot.json";
  var URL_TRENDS = "assets/sediment-trends.json";
  var URL_SITE_META = "assets/site-meta.json";
  var URL_SITE_SEARCH = "assets/site-search-index.json";

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

  /** 快照日标签：按北京日历日从 ISO 解析（兼容历史 UTC「Z」）。 */
  function snapshotDayLabelBeijing(generatedAt) {
    if (!generatedAt) return "";
    var ms = Date.parse(String(generatedAt));
    if (isNaN(ms)) return String(generatedAt).slice(0, 10);
    try {
      return new Intl.DateTimeFormat("en-CA", {
        timeZone: "Asia/Shanghai",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      }).format(new Date(ms));
    } catch (_) {
      return String(generatedAt).slice(0, 10);
    }
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
    _siteSearch = null;
    _siteSearchPromise = null;
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

  /**
   * 轻量页题索引（可选）；404 或缺文件时返回 null，不抛错。
   * @returns {Promise<object|null>}
   */
  function loadSiteSearchIndex() {
    if (_siteSearchPromise) return _siteSearchPromise;
    _siteSearchPromise = fetch(URL_SITE_SEARCH)
      .then(function (r) {
        if (!r.ok) return null;
        return r.json();
      })
      .then(function (d) {
        if (!d || !Array.isArray(d.entries) || d.entries.length < 1) return null;
        _siteSearch = d;
        return d;
      })
      .catch(function () {
        return null;
      });
    return _siteSearchPromise;
  }

  function currentHtmlBasename() {
    var p = window.location.pathname || "";
    var i = p.lastIndexOf("/");
    var base = i >= 0 ? p.substring(i + 1) : p;
    return base || "index.html";
  }

  /**
   * 在 [data-site-quick-search] 挂载标题/路径过滤框（依赖 site-search-index.json）。
   * @param {HTMLElement} host
   */
  function mountSiteQuickSearch(host) {
    if (!host || host.nodeType !== 1) return;
    loadSiteSearchIndex().then(function (doc) {
      if (!doc) {
        host.innerHTML = "";
        host.setAttribute("hidden", "");
        return;
      }
      host.removeAttribute("hidden");
      var entries = doc.entries.slice();

      var wrap = document.createElement("div");
      wrap.className = "site-quick-search";

      var inp = document.createElement("input");
      inp.type = "search";
      inp.className = "site-quick-search-input";
      inp.setAttribute("aria-label", "站内页面搜索");
      inp.setAttribute("autocomplete", "off");
      inp.setAttribute("spellcheck", "false");
      inp.placeholder = "搜页面…";

      var list = document.createElement("ul");
      list.className = "site-quick-search-list";
      list.setAttribute("hidden", "");
      list.setAttribute("role", "listbox");

      var cur = currentHtmlBasename();
      var debounceId = 0;

      function renderFiltered(q) {
        var needle = (q || "").trim().toLowerCase();
        list.innerHTML = "";
        if (!needle) {
          list.setAttribute("hidden", "");
          return;
        }
        var hits = [];
        for (var i = 0; i < entries.length && hits.length < 14; i++) {
          var e = entries[i];
          var path = String(e.path || "");
          var title = String(e.title || path);
          var hay = (title + " " + path).toLowerCase();
          if (hay.indexOf(needle) === -1) continue;
          hits.push({ path: path, title: title });
        }
        if (!hits.length) {
          var empty = document.createElement("li");
          empty.className = "site-quick-search-empty muted";
          empty.setAttribute("role", "option");
          empty.textContent = "无匹配";
          list.appendChild(empty);
          list.removeAttribute("hidden");
          return;
        }
        for (var j = 0; j < hits.length; j++) {
          var h = hits[j];
          var li = document.createElement("li");
          li.setAttribute("role", "presentation");
          var a = document.createElement("a");
          a.href = h.path;
          a.setAttribute("role", "option");
          a.textContent = h.title;
          if (h.path === cur) a.classList.add("site-quick-search-current");
          li.appendChild(a);
          list.appendChild(li);
        }
        list.removeAttribute("hidden");
      }

      inp.addEventListener("input", function () {
        window.clearTimeout(debounceId);
        var v = inp.value;
        debounceId = window.setTimeout(function () {
          renderFiltered(v);
        }, 100);
      });

      inp.addEventListener("keydown", function (ev) {
        if (ev.key === "Escape") {
          inp.value = "";
          renderFiltered("");
          inp.blur();
        }
      });

      inp.addEventListener("focus", function () {
        renderFiltered(inp.value);
      });

      wrap.appendChild(inp);
      wrap.appendChild(list);
      host.appendChild(wrap);
    });
  }

  var _quickSearchDocCloseBound = false;

  function mountAllQuickSearch() {
    var nodes = document.querySelectorAll("[data-site-quick-search]");
    for (var i = 0; i < nodes.length; i++) {
      mountSiteQuickSearch(nodes[i]);
    }
    if (!nodes.length || _quickSearchDocCloseBound) return;
    _quickSearchDocCloseBound = true;
    document.addEventListener("click", function (ev) {
      var wraps = document.querySelectorAll(".site-quick-search");
      for (var j = 0; j < wraps.length; j++) {
        if (wraps[j].contains(ev.target)) continue;
        var listEl = wraps[j].querySelector(".site-quick-search-list");
        if (listEl) {
          listEl.innerHTML = "";
          listEl.setAttribute("hidden", "");
        }
      }
    });
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
      parts.push("快照 " + esc(snapshotDayLabelBeijing(data.generated_at)));
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
    loadSiteSearchIndex: loadSiteSearchIndex,
    clearCache: clearCache,
    mountLiveStrip: mountLiveStrip,
    mountAllLiveStrips: mountAllLiveStrips,
    getCachedSnapshot: function () {
      return _snap;
    },
    getCachedTrends: function () {
      return _trends;
    },
    getCachedSiteSearchIndex: function () {
      return _siteSearch;
    },
  };

  function mountBackToTopFab() {
    if (document.querySelector(".back-to-top-fab")) return;
    var main = document.getElementById("main");
    if (!main) return;
    var a = document.createElement("a");
    a.className = "back-to-top-fab";
    a.href = "#main";
    a.title = "回到页首";
    a.setAttribute("aria-label", "回到页首");
    a.innerHTML = '<span aria-hidden="true">↑</span>';
    document.body.appendChild(a);
  }

  function mountReadingProgressBar() {
    if (document.body.getAttribute("data-no-reading-progress") === "1") return;
    if (document.querySelector(".reading-progress")) return;
    var bar = document.createElement("div");
    bar.className = "reading-progress";
    bar.setAttribute("role", "progressbar");
    bar.setAttribute("aria-valuemin", "0");
    bar.setAttribute("aria-valuemax", "100");
    bar.setAttribute("aria-valuenow", "0");
    bar.setAttribute("aria-label", "页面阅读进度");
    document.body.insertBefore(bar, document.body.firstChild);

    var rafPending = false;
    function updateProgress() {
      if (rafPending) return;
      rafPending = true;
      requestAnimationFrame(function () {
        rafPending = false;
        var root = document.documentElement;
        var scrollTop = root.scrollTop || document.body.scrollTop || 0;
        var scrollHeight = root.scrollHeight || document.body.scrollHeight || 0;
        var clientH = root.clientHeight || window.innerHeight || 1;
        var maxScroll = Math.max(0, scrollHeight - clientH);
        var pct = maxScroll > 0 ? Math.min(100, Math.round((scrollTop / maxScroll) * 100)) : 0;
        bar.style.setProperty("--reading-pct", String(pct));
        bar.setAttribute("aria-valuenow", String(pct));
      });
    }

    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress, { passive: true });
    updateProgress();
  }

  function boot() {
    mountReadingProgressBar();
    mountBackToTopFab();
    mountAllLiveStrips();
    mountSiteMetaVersion();
    mountAllQuickSearch();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
