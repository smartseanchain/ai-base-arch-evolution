/**
 * 观测信号：evolution-manifest.json（已入库）+ evolution-candidates.json（抓取待审）。
 * 沙盘高亮合并两来源的 lab_factors。
 */
(function () {
  "use strict";

  var MANIFEST = "assets/evolution-manifest.json";
  var CANDIDATES = "assets/evolution-candidates.json";

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function kindLabel(k) {
    if (k === "opinion") return "舆情";
    if (k === "policy") return "政策";
    if (k === "law") return "法律/条文线索";
    if (k === "market") return "市场";
    if (k === "tech") return "技术";
    return k || "信号";
  }

  function weightClass(w) {
    if (w === "high") return "evolution-weight evolution-weight--high";
    if (w === "medium") return "evolution-weight evolution-weight--med";
    return "evolution-weight evolution-weight--low";
  }

  function renderSignalCard(sig, isCandidate) {
    var card = document.createElement("article");
    card.className =
      "evolution-signal-card" +
      (isCandidate ? " evolution-signal-card--candidate" : "");
    card.setAttribute("data-signal-id", sig.id || "");
    var head = document.createElement("div");
    head.className = "evolution-signal-head";
    head.innerHTML =
      '<span class="' +
      weightClass(sig.weight) +
      '">' +
      esc(kindLabel(sig.kind)) +
      "</span>" +
      '<span class="evolution-signal-title">' +
      esc(sig.title || "") +
      "</span>";
    if (sig.since) {
      var since = document.createElement("span");
      since.className = "evolution-signal-since";
      since.textContent = sig.since;
      head.appendChild(since);
    }
    var body = document.createElement("p");
    body.className = "muted evolution-signal-summary";
    body.textContent = sig.summary || "";
    card.appendChild(head);
    card.appendChild(body);
    if (sig.maps_to && sig.maps_to.pages && sig.maps_to.pages.length) {
      var links = document.createElement("p");
      links.className = "evolution-signal-links";
      links.innerHTML = sig.maps_to.pages
        .map(function (p) {
          return '<a href="' + esc(p) + '">' + esc(p) + "</a>";
        })
        .join(" · ");
      card.appendChild(links);
    }
    if (isCandidate && sig.source) {
      var src = document.createElement("p");
      src.className = "muted evolution-signal-source";
      var st = sig.source.type || "";
      var link = sig.source.item_link || sig.source.url || "";
      src.innerHTML =
        '<span class="evolution-candidate-badge">待审</span> 来源：' +
        esc(st) +
        (link
          ? ' · <a href="' +
            esc(link) +
            '" rel="noopener noreferrer" target="_blank">打开原文</a>'
          : "");
      card.appendChild(src);
    }
    return card;
  }

  function renderFeedSections(container, manifest, candidates) {
    if (!container) return;
    container.innerHTML = "";

    if (manifest && manifest.signals && manifest.signals.length) {
      var h2a = document.createElement("h3");
      h2a.className = "evolution-feed-subhead";
      h2a.textContent = "已入库（manifest）";
      container.appendChild(h2a);
      var meta = document.createElement("p");
      meta.className = "muted evolution-feed-meta";
      meta.innerHTML =
        "版本 <strong>" +
        esc(String(manifest.schema_version || "?")) +
        "</strong> · 更新 <time>" +
        esc(manifest.updated || "—") +
        "</time>";
      container.appendChild(meta);
      manifest.signals.forEach(function (sig) {
        container.appendChild(renderSignalCard(sig, false));
      });
    }

    var candList =
      candidates && candidates.signals ? candidates.signals : [];
    var candOnly = candList.filter(function (s) {
      return s.status === "candidate" || s.status === undefined;
    });
    if (candOnly.length) {
      var h2b = document.createElement("h3");
      h2b.className = "evolution-feed-subhead";
      h2b.textContent = "待审候选（自动抓取）";
      container.appendChild(h2b);
      var meta2 = document.createElement("p");
      meta2.className = "muted evolution-feed-meta";
      meta2.innerHTML =
        "抓取时间 <time>" +
        esc(candidates.fetched_at || candidates.updated || "—") +
        '</time> · 合并命令见 <a href="evolution-loop.html#ingest">进化闭环 · 抓取管道</a>';
      container.appendChild(meta2);
      candOnly.forEach(function (sig) {
        container.appendChild(renderSignalCard(sig, true));
      });
    }

    if (
      (!manifest || !manifest.signals || !manifest.signals.length) &&
      !candOnly.length
    ) {
      container.innerHTML =
        '<p class="muted">暂无清单数据。运行 <code>python3 scripts/ingest_opinion_law.py</code> 抓取舆情/法规线索，或编辑 <code>assets/evolution-manifest.json</code>。</p>';
    }
  }

  function collectLabFactors(manifest, candidates) {
    var ids = {};
    function add(list) {
      if (!list || !list.length) return;
      list.forEach(function (sig) {
        if (!sig.maps_to || !sig.maps_to.lab_factors) return;
        sig.maps_to.lab_factors.forEach(function (id) {
          ids[id] = true;
        });
      });
    }
    add(manifest && manifest.signals ? manifest.signals : []);
    add(candidates && candidates.signals ? candidates.signals : []);
    return ids;
  }

  function highlightLabFactors(idsObj) {
    Object.keys(idsObj).forEach(function (fid) {
      var inp = document.getElementById("f_" + fid);
      if (!inp) return;
      var wrap = inp.closest(".sim-option");
      if (wrap) {
        wrap.classList.add("sim-option--evolution");
        wrap.setAttribute(
          "title",
          "manifest 或候选清单建议关注此因子"
        );
      }
    });
  }

  function injectLabBanner(manifest, candidates) {
    var grid = document.getElementById("simOptions");
    if (!grid) return;
    var idsObj = collectLabFactors(manifest, candidates);
    var n = 0;
    if (manifest && manifest.signals) {
      manifest.signals.forEach(function (s) {
        if (s.maps_to && s.maps_to.lab_factors && s.maps_to.lab_factors.length)
          n++;
      });
    }
    var nc = 0;
    if (candidates && candidates.signals) {
      candidates.signals.forEach(function (s) {
        if (s.maps_to && s.maps_to.lab_factors && s.maps_to.lab_factors.length)
          nc++;
      });
    }
    if (n === 0 && nc === 0 && Object.keys(idsObj).length === 0) return;
    var banner = document.createElement("div");
    banner.className = "callout extend evolution-lab-banner";
    banner.setAttribute("role", "note");
    banner.innerHTML =
      "<p class=\"muted\" style=\"margin:0\"><strong>观测信号：</strong>已入库 " +
      n +
      " 条 · 候选 " +
      nc +
      " 条（含 <code>lab_factors</code> 映射时已高亮；见 <a href=\"evolution-loop.html\">进化闭环</a>）。</p>";
    grid.parentNode.insertBefore(banner, grid);
  }

  function load() {
    var p1 = fetch(MANIFEST)
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .catch(function () {
        return null;
      });
    var p2 = fetch(CANDIDATES)
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .catch(function () {
        return null;
      });
    Promise.all([p1, p2]).then(function (pair) {
      var manifest = pair[0];
      var candidates = pair[1];
      var feed = document.getElementById("evolution-feed");
      renderFeedSections(feed, manifest, candidates);
      if (document.getElementById("simOptions")) {
        injectLabBanner(manifest, candidates);
        highlightLabFactors(collectLabFactors(manifest, candidates));
      }
    }).catch(function () {
      var feed = document.getElementById("evolution-feed");
      if (feed) {
        feed.innerHTML =
          '<p class="muted">无法加载清单（若用 file:// 打开，请改用本地 HTTP 服务）。说明见 <a href="evolution-loop.html">进化闭环</a>。</p>';
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
