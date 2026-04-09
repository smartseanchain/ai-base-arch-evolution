/**
 * 滚动揭示：IntersectionObserver → html.motion-scroll + .motion-scroll-target / .is-revealed。
 * 与 site.css 中 perspective + rotateX 的「推入景深」配套；body.page-triad-future 时加 html.motion-corridor（廊道斜向）。
 * 仅观察 .wrap 内 section 与直接子级 .scene-journey，避免嵌套双重透明。
 * 演进页：.is-station-current / 脊钉 / 展台纵深由 journey-stepper.js 与 triad 专段 CSS 负责，本文件不读写。
 * prefers-reduced-motion: reduce 时整段跳过；change 时 teardown 卸观察器与类名。
 * 详见 assets/MOTION-ARCHITECTURE.md
 */
(function () {
  var mq = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!mq || mq.matches) {
    return;
  }

  var wrap = document.querySelector(".wrap");
  if (!wrap) return;

  var seen = new Set();
  var nodes = [];

  function add(el) {
    if (!el || seen.has(el)) return;
    seen.add(el);
    nodes.push(el);
  }

  wrap.querySelectorAll("section").forEach(add);

  Array.prototype.forEach.call(wrap.children, function (el) {
    if (el.classList && el.classList.contains("scene-journey")) {
      add(el);
    }
  });

  if (!nodes.length) return;

  nodes.sort(function (a, b) {
    var pos = a.compareDocumentPosition(b);
    if (pos & Node.DOCUMENT_POSITION_FOLLOWING) return -1;
    if (pos & Node.DOCUMENT_POSITION_PRECEDING) return 1;
    return 0;
  });

  var root = document.documentElement;
  var vh = window.innerHeight || 800;
  var io = null;

  function mostlyVisible(el) {
    var r = el.getBoundingClientRect();
    var margin = vh * 0.12;
    return r.top < vh - margin && r.bottom > margin * 0.35;
  }

  function teardownMotion() {
    if (io) {
      io.disconnect();
      io = null;
    }
    root.classList.remove("motion-scroll", "motion-corridor");
    nodes.forEach(function (el) {
      el.classList.remove("motion-scroll-target", "is-revealed");
      el.style.removeProperty("--motion-reveal-delay");
    });
  }

  io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        el.classList.add("is-revealed");
        io.unobserve(el);
      });
    },
    { root: null, rootMargin: "0px 0px -5% 0px", threshold: [0, 0.06, 0.12] }
  );

  root.classList.add("motion-scroll");
  if (document.body.classList.contains("page-triad-future")) {
    root.classList.add("motion-corridor");
  }

  var staggerMs = document.body.classList.contains("page-triad-future") ? 34 : 26;

  nodes.forEach(function (el, i) {
    el.classList.add("motion-scroll-target");
    el.style.setProperty("--motion-reveal-delay", Math.min(i, 16) * staggerMs + "ms");
    if (mostlyVisible(el)) {
      el.classList.add("is-revealed");
    } else {
      io.observe(el);
    }
  });

  window.addEventListener(
    "resize",
    function () {
      vh = window.innerHeight || vh;
    },
    { passive: true }
  );

  if (mq.addEventListener) {
    mq.addEventListener("change", function () {
      if (mq.matches) {
        teardownMotion();
      }
    });
  } else if (mq.addListener) {
    mq.addListener(function () {
      if (mq.matches) {
        teardownMotion();
      }
    });
  }
})();
