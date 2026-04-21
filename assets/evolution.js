/**
 * 观测信号：evolution-manifest.json（已入库）+ evolution-candidates.json（抓取待审）。
 * 沙盘高亮合并两来源的 lab_factors；候选 review_state=noise 不参与高亮。
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

  function effectiveReviewState(sig) {
    var r = sig.review_state || "pending";
    if (r === "noise" || r === "queued_for_manifest" || r === "pending") {
      return r;
    }
    return "pending";
  }

  function reviewStateLabel(rs) {
    if (rs === "noise") return "噪点";
    if (rs === "queued_for_manifest") return "待入库";
    return "待审";
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
    var rs = isCandidate ? effectiveReviewState(sig) : "";
    var card = document.createElement("article");
    card.className =
      "evolution-signal-card" +
      (isCandidate ? " evolution-signal-card--candidate" : "") +
      (isCandidate && rs === "noise" ? " evolution-signal-card--noise" : "");
    card.setAttribute("data-signal-id", sig.id || "");
    var head = document.createElement("div");
    head.className = "evolution-signal-head";
    head.innerHTML =
      '<span class="' +
      weightClass(sig.weight) +
      '">' +
      esc(kindLabel(sig.kind)) +
      "</span>";
    if (isCandidate) {
      var rb = document.createElement("span");
      rb.className =
        "evolution-review-badge evolution-review-badge--" +
        rs.replace(/_/g, "-");
      rb.textContent = reviewStateLabel(rs);
      head.appendChild(rb);
    }
    var titleEl = document.createElement("span");
    titleEl.className = "evolution-signal-title";
    titleEl.textContent = sig.title || "";
    head.appendChild(titleEl);
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
      sig.maps_to.pages.forEach(function (p, i) {
        if (i > 0) links.appendChild(document.createTextNode(" · "));
        var a = document.createElement("a");
        a.href = p;
        a.textContent = p;
        links.appendChild(a);
      });
      card.appendChild(links);
    }
    if (isCandidate && sig.source) {
      var src = document.createElement("p");
      src.className = "muted evolution-signal-source";
      var st = sig.source.type || "";
      var link = sig.source.item_link || sig.source.url || "";
      var badge = document.createElement("span");
      badge.className = "evolution-candidate-badge";
      badge.textContent = "抓取";
      src.appendChild(badge);
      src.appendChild(document.createTextNode(" 来源：" + st));
      if (link) {
        src.appendChild(document.createTextNode(" · "));
        var la = document.createElement("a");
        la.href = link;
        la.rel = "noopener noreferrer";
        la.target = "_blank";
        la.textContent = "打开原文";
        src.appendChild(la);
      }
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
      var by = { pending: 0, noise: 0, queued_for_manifest: 0 };
      candOnly.forEach(function (s) {
        var r = effectiveReviewState(s);
        if (by[r] !== undefined) by[r] += 1;
        else by.pending += 1;
      });
      var meta2 = document.createElement("p");
      meta2.className = "muted evolution-feed-meta";
      meta2.innerHTML =
        "抓取时间 <time>" +
        esc(candidates.fetched_at || candidates.updated || "—") +
        '</time> · 待审 ' +
        by.pending +
        " · 噪点 " +
        by.noise +
        " · 待入库 " +
        by.queued_for_manifest +
        ' · 合并命令见 <a href="evolution-loop.html#ingest">进化闭环 · 抓取管道</a>';
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
        '<p class="muted">暂无清单数据。运行 <code>make ingest</code> 或 <code>python3 scripts/ingest_opinion_law.py</code> 抓取线索，或编辑 <code>assets/evolution-manifest.json</code>；双周节奏见 <a href="docs/EVOLUTION_RUNBOOK.md">运行手册</a>。</p>';
    }
  }

  function collectLabFactors(manifest, candidates) {
    var ids = {};
    function addFromManifest(list) {
      if (!list || !list.length) return;
      list.forEach(function (sig) {
        if (!sig.maps_to || !sig.maps_to.lab_factors) return;
        sig.maps_to.lab_factors.forEach(function (id) {
          ids[id] = true;
        });
      });
    }
    function addFromCandidates(list) {
      if (!list || !list.length) return;
      list.forEach(function (sig) {
        if (effectiveReviewState(sig) === "noise") return;
        if (!sig.maps_to || !sig.maps_to.lab_factors) return;
        sig.maps_to.lab_factors.forEach(function (id) {
          ids[id] = true;
        });
      });
    }
    addFromManifest(manifest && manifest.signals ? manifest.signals : []);
    addFromCandidates(
      candidates && candidates.signals ? candidates.signals : []
    );
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
        if (effectiveReviewState(s) === "noise") return;
        if (s.maps_to && s.maps_to.lab_factors && s.maps_to.lab_factors.length)
          nc++;
      });
    }
    if (n === 0 && nc === 0 && Object.keys(idsObj).length === 0) return;
    var banner = document.createElement("div");
    banner.className = "callout extend evolution-lab-banner";
    banner.setAttribute("role", "note");
    banner.innerHTML =
      "<p class=\"muted\"><strong>观测信号：</strong>已入库 " +
      n +
      " 条 · 候选（非噪点）" +
      nc +
      " 条含映射（<code>lab_factors</code> 已高亮；<code>noise</code> 不参与）；见 <a href=\"evolution-loop.html\">进化闭环</a>）。</p>";
    grid.parentNode.insertBefore(banner, grid);
  }

  function load() {
    var feed = document.getElementById("evolution-feed");
    if (feed) {
      feed.setAttribute("aria-busy", "true");
      feed.innerHTML =
        '<p class="muted evolution-feed-loading">正在加载 manifest 与候选清单…</p>';
    }

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
    Promise.all([p1, p2])
      .then(function (pair) {
        var manifest = pair[0];
        var candidates = pair[1];
        if (!manifest && !candidates && feed) {
          if (window.location.protocol === "file:") {
            feed.innerHTML =
              '<p class="muted"><strong>无法加载 JSON：</strong>当前为 <code>file://</code> 协议，浏览器会拦截 <code>fetch</code>。请用本地 HTTP（如 <code>python3 -m http.server</code>）或部署后的 <strong>https</strong> 打开；说明见 <a href="evolution-loop.html">进化闭环</a>。</p>';
          } else {
            feed.innerHTML =
              '<p class="muted"><strong>无法加载清单：</strong><code>assets/evolution-manifest.json</code> 与 <code>evolution-candidates.json</code> 均未取回（路径或网络）。请检查部署根目录是否含 <code>assets/</code>。</p>';
          }
          return;
        }
        renderFeedSections(feed, manifest, candidates);
        if (document.getElementById("simOptions")) {
          injectLabBanner(manifest, candidates);
          highlightLabFactors(collectLabFactors(manifest, candidates));
        }
      })
      .catch(function () {
        if (feed) {
          feed.innerHTML =
            '<p class="muted">无法加载清单（若用 file:// 打开，请改用本地 HTTP 服务）。说明见 <a href="evolution-loop.html">进化闭环</a>。</p>';
        }
      })
      .finally(function () {
        if (feed) feed.setAttribute("aria-busy", "false");
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
