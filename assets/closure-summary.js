/**
 * 进化闭环页：拉取 analysis-snapshot.json，展示规则闭环缺口摘要（链到 analysis-hub）。
 */
(function () {
  "use strict";

  var el = document.getElementById("evolution-closure-summary");
  if (!el) return;

  function formatGenAtBeijing(iso) {
    if (!iso) return "—";
    var ms = Date.parse(String(iso));
    if (isNaN(ms)) return String(iso);
    try {
      return (
        new Date(ms).toLocaleString("zh-CN", {
          timeZone: "Asia/Shanghai",
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
      return String(iso);
    }
  }

  function show(msg, kind) {
    el.hidden = false;
    el.className =
      "card evolution-closure-summary" +
      (kind === "warn"
        ? " evolution-closure-summary--warn"
        : kind === "ok"
          ? " evolution-closure-summary--ok"
          : " evolution-closure-summary--muted");
    el.innerHTML = msg;
  }

  function fetchSnapshotShared() {
    if (window.SiteDataBus && typeof SiteDataBus.loadSnapshot === "function") {
      return SiteDataBus.loadSnapshot();
    }
    return fetch("assets/analysis-snapshot.json")
      .then(function (r) {
        if (!r.ok) throw new Error("snap");
        return r.json();
      });
  }

  if (window.location.protocol === "file:") {
    show(
      '<p class="muted">规则闭环摘要需通过 <strong>http(s)</strong> 加载快照；本地请用静态服务器打开本站，或直看 <a href="analysis-hub.html">分析引擎</a>。</p>',
      "muted"
    );
    return;
  }

  el.hidden = false;
  el.setAttribute("aria-busy", "true");
  el.className =
    "card evolution-closure-summary evolution-closure-summary--muted";
  el.innerHTML = '<p class="muted">正在读取分析快照…</p>';

  fetchSnapshotShared()
    .then(function (data) {
      var gaps = data.hint_closure_gaps;
      var n = Array.isArray(gaps) ? gaps.length : 0;
      var hd = (data.sources && data.sources.hint_decisions) || {};
      var tot = hd.total != null ? hd.total : 0;
      var gen = formatGenAtBeijing(data.generated_at);

      var p = document.createElement("p");
      p.className = "muted evolution-closure-summary__snap-body";

      var strong = document.createElement("strong");
      strong.textContent = "分析快照 · 规则闭环";
      p.appendChild(strong);
      p.appendChild(document.createTextNode("（生成 "));
      p.appendChild(document.createTextNode(String(gen)));
      p.appendChild(
        document.createTextNode(
          "）· 已记录决策 " + String(tot) + " 条 · "
        )
      );

      if (n === 0) {
        p.appendChild(
          document.createTextNode(
            "当前无待闭环的 track_closure 规则（或已全部 done/rejected）。详情："
          )
        );
      } else {
        p.appendChild(
          document.createTextNode(
            "尚有 " + String(n) + " 条规则待落实或否决并写入 evolution-hint-decisions（含 rule_id）。详情："
          )
        );
      }

      var a = document.createElement("a");
      a.href = "analysis-hub.html";
      a.textContent = "打开分析引擎仪表盘";
      p.appendChild(a);
      p.appendChild(document.createTextNode("。"));

      el.innerHTML = "";
      el.appendChild(p);
      el.hidden = false;
      el.className =
        "card evolution-closure-summary" +
        (n > 0 ? " evolution-closure-summary--warn" : " evolution-closure-summary--ok");
    })
    .catch(function () {
      show(
        '<p class="muted">无法加载 <code>assets/analysis-snapshot.json</code>。请在仓库根运行 <code>make analyze</code> 后部署，或前往 <a href="analysis-hub.html">分析引擎</a> 查看说明。</p>',
        "muted"
      );
    })
    .finally(function () {
      el.removeAttribute("aria-busy");
    });
})();
