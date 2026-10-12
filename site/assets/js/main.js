/* Quincy Lou: scroll reveal and small niceties. The site works without it. */
(function () {
  "use strict";
  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // reveal on scroll; staged only when JS runs and motion is allowed
  var items = document.querySelectorAll("[data-r]");
  if (!reduce && "IntersectionObserver" in window && items.length) {
    root.classList.add("js");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var d = +(e.target.getAttribute("data-r") || 0);
        setTimeout(function () { e.target.classList.add("in"); }, d);
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    items.forEach(function (el) { io.observe(el); });
  }

  // close the mobile menu after choosing a link
  var menu = document.querySelector(".menu");
  if (menu) menu.addEventListener("click", function (e) {
    if (e.target.closest("a")) menu.removeAttribute("open");
  });
})();
