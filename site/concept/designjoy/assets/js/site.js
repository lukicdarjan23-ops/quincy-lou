/* Quincy Lou — scroll reveal.
   Staging classes are added by JS only, so the page reads fine without it. */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var targets = document.querySelectorAll("[data-reveal]");

  if (reduced || !("IntersectionObserver" in window) || !targets.length) return;

  root.setAttribute("data-anim", "on");

  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var delay = Number(el.getAttribute("data-reveal-delay") || 0);
      window.setTimeout(function () { el.classList.add("is-in"); }, delay);
      seen.unobserve(el);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

  targets.forEach(function (el) { seen.observe(el); });
})();
