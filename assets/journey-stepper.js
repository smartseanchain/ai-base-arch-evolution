/**
 * 仅 body.page-triad-future（evolution-triad.html）。
 *
 * 流程：#corridor-gate 默认跳过入场 → kick 后 updateFromStepper（步进器 is-current / is-passed、aria-current）
 * → setEpoch（epoch-corridor|now|future）→ syncStationState（.triad-station）
 * → corridorFill（--corridor-fill）→ updateSpineMarks（.corridor-spine-mark）。
 *
 * 站点 ID 须与 HTML section#、步进器 href、脊钉数量一致，见文件内 STATION_IDS。
 * 详见 assets/MOTION-ARCHITECTURE.md
 */
(function () {
  var body = document.body;
  if (!body.classList.contains("page-triad-future")) return;

  var mqReduce = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;

  function prefersReducedMotion() {
    return mqReduce && mqReduce.matches;
  }

  var gate = document.getElementById("corridor-gate");
  var chip = document.getElementById("corridor-epoch-chip");
  var spine = document.querySelector(".corridor-spine");
  var stepper = document.querySelector(".journey-stepper");

  /* 与全站其他模块页一致：不做双扉大门入场长动画，直接跳过（仍保留脊轨/步进逻辑） */
  if (gate) {
    gate.classList.add("corridor-gate--skip");
  }

  var epochLabels = [
    "历史纵深 · 教育",
    "历史纵深 · 职业",
    "当下交汇 · 家庭与个人",
    "未来分叉 · 走向合成",
    "未来出口 · 接回全站",
  ];

  /** 与 evolution-triad.html 中五段 section#id 顺序一致（勿单独改序而不改 HTML） */
  var STATION_IDS = ["evo-edu", "evo-career", "fai-merge", "directions", "cross"];

  function syncStationState(currentIdx) {
    var stations = document.querySelectorAll(".triad-station");
    stations.forEach(function (el, i) {
      el.classList.toggle("is-station-current", i === currentIdx);
      el.classList.toggle("is-station-past", i < currentIdx);
    });
    body.dataset.triadStation = String(currentIdx);
  }

  function setEpoch(idx) {
    idx = Math.max(0, Math.min(epochLabels.length - 1, idx));
    body.classList.remove("epoch-corridor", "epoch-now", "epoch-future");
    if (idx <= 1) {
      body.classList.add("epoch-corridor");
    } else if (idx === 2) {
      body.classList.add("epoch-now");
    } else {
      body.classList.add("epoch-future");
    }
    if (chip) {
      var label = epochLabels[idx];
      chip.textContent = label;
      chip.setAttribute("aria-label", "阅读进度，当前站点：" + label);
    }
  }

  function corridorFill() {
    if (!spine) return;
    var doc = document.documentElement;
    var maxScroll = doc.scrollHeight - window.innerHeight;
    var pct = maxScroll > 0 ? Math.min(100, Math.max(0, (window.scrollY / maxScroll) * 100)) : 0;
    spine.style.setProperty("--corridor-fill", String(Math.round(pct)));
  }

  /** 五站在视口中的纵向位置 → 左侧固定脊上的投影点（当前站高亮） */
  function updateSpineMarks() {
    if (!spine) return;
    var dots = spine.querySelectorAll(".corridor-spine-mark");
    if (!dots.length) return;
    var vh = window.innerHeight || 600;
    var current = parseInt(body.dataset.triadStation || "0", 10);
    STATION_IDS.forEach(function (id, i) {
      var sec = document.getElementById(id);
      var dot = dots[i];
      if (!sec || !dot) return;
      var r = sec.getBoundingClientRect();
      var cy = r.top + Math.min(Math.max(r.height * 0.22, 24), 140);
      var pct = vh > 0 ? (cy / vh) * 100 : 50;
      dot.style.setProperty(
        "--corridor-mark-top",
        Math.max(-6, Math.min(106, pct)) + "%"
      );
      var near = pct > -14 && pct < 114;
      dot.classList.toggle("is-active", i === current);
      dot.classList.toggle("is-offscreen", !near);
    });
  }

  function updateFromStepper() {
    if (!stepper) return;
    var links = stepper.querySelectorAll('a[href^="#"]');
    var items = stepper.querySelectorAll("li");
    var sections = [];
    links.forEach(function (a) {
      var id = a.getAttribute("href").replace(/^#/, "");
      sections.push(id ? document.getElementById(id) : null);
    });
    var mid = (window.innerHeight || 600) * 0.36;
    var current = 0;
    for (var i = 0; i < sections.length; i++) {
      var el = sections[i];
      if (!el) continue;
      if (el.getBoundingClientRect().top <= mid) {
        current = i;
      }
    }
    items.forEach(function (li, i) {
      li.classList.toggle("is-current", i === current);
      li.classList.toggle("is-passed", i < current);
    });
    links.forEach(function (a, i) {
      if (i === current) {
        a.setAttribute("aria-current", "step");
      } else {
        a.removeAttribute("aria-current");
      }
    });
    setEpoch(current);
    syncStationState(current);
  }

  var scheduled = false;
  function onScroll() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      updateFromStepper();
      corridorFill();
      updateSpineMarks();
    });
  }

  if (stepper) {
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
  } else {
    var scheduledNoStepper = false;
    function onScrollNoStepper() {
      if (scheduledNoStepper) return;
      scheduledNoStepper = true;
      requestAnimationFrame(function () {
        scheduledNoStepper = false;
        corridorFill();
        updateSpineMarks();
      });
    }
    window.addEventListener("scroll", onScrollNoStepper, { passive: true });
    window.addEventListener("resize", onScrollNoStepper, { passive: true });
  }

  function kick() {
    if (stepper) {
      updateFromStepper();
    } else {
      setEpoch(0);
      syncStationState(0);
    }
    corridorFill();
    updateSpineMarks();
  }

  function onReduceMotionChange() {
    if (!prefersReducedMotion()) return;
    if (gate) {
      gate.classList.add("corridor-gate--skip");
      gate.classList.remove("corridor-gate--opening");
    }
    kick();
  }

  if (mqReduce) {
    if (mqReduce.addEventListener) {
      mqReduce.addEventListener("change", onReduceMotionChange);
    } else if (mqReduce.addListener) {
      mqReduce.addListener(onReduceMotionChange);
    }
  }

  kick();

  window.addEventListener(
    "hashchange",
    function () {
      requestAnimationFrame(kick);
    },
    false
  );

  window.addEventListener(
    "pageshow",
    function (ev) {
      if (ev.persisted) {
        requestAnimationFrame(kick);
      }
    },
    false
  );
})();
