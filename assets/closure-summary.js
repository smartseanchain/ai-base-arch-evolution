/**
 * 进化闭环页：拉取 analysis-snapshot.json，展示规则闭环缺口摘要（链到 analysis-hub）。
 */
(function () {
  "use strict";

  var el = document.getElementById("evolution-closure-summary");
  if (!el) return;

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

  if (window.location.protocol === "file:") {
    show(
      '<p class="muted" style="margin:0;font-size:0.88rem">规则闭环摘要需通过 <strong>http(s)</strong> 加载快照；本地请用静态服务器打开本站，或直看 <a href="analysis-hub.html">分析引擎</a>。</p>',
      "muted"
    );
    return;
  }

  fetch("assets/analysis-snapshot.json")
    .then(function (r) {
      if (!r.ok) throw new Error("snap");
      return r.json();
    })
    .then(function (data) {
      var gaps = data.hint_closure_gaps;
      var n = Array.isArray(gaps) ? gaps.length : 0;
      var hd = (data.sources && data.sources.hint_decisions) || {};
      var tot = hd.total != null ? hd.total : 0;
      var gen = data.generated_at || "—";

      var p = document.createElement("p");
      p.className = "muted";
      p.style.margin = "0";
      p.style.fontSize = "0.9rem";
      p.style.lineHeight = "1.75";

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
        '<p class="muted" style="margin:0;font-size:0.88rem">无法加载 <code>assets/analysis-snapshot.json</code>。请在仓库根运行 <code>make analyze</code> 后部署，或前往 <a href="analysis-hub.html">分析引擎</a> 查看说明。</p>',
        "muted"
      );
    });
})();
