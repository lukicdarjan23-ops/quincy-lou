/* Quincy Lou homepage: case study filter and the mobile menu. The page works without it. */
(function () {
  "use strict";

  // filter the case studies by industry
  var buttons = document.querySelectorAll(".l-filter");
  var cases = document.querySelectorAll(".l-case");
  var apply = function (sector) {
    buttons.forEach(function (b) {
      var on = b.getAttribute("data-filter") === sector;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
    cases.forEach(function (c) {
      c.hidden = sector !== "All" && c.getAttribute("data-sector") !== sector;
    });
  };
  buttons.forEach(function (b) {
    b.addEventListener("click", function () { apply(b.getAttribute("data-filter")); });
  });
  // "See the work" on an industry card opens the case studies already filtered
  document.querySelectorAll("[data-set-filter]").forEach(function (a) {
    a.addEventListener("click", function () { apply(a.getAttribute("data-set-filter")); });
  });

  // close the mobile menu after choosing a link
  var menu = document.querySelector(".l-menu");
  if (menu) menu.addEventListener("click", function (e) {
    if (e.target.closest("a")) menu.removeAttribute("open");
  });
})();
