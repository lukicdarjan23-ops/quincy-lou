/* Quincy Lou homepage: journal slider arrows and the mobile menu. The page works without it. */
(function () {
  "use strict";
  var track = document.querySelector(".l-posts");
  var arrows = document.querySelectorAll(".l-arrow");
  if (track && arrows.length) {
    var step = function () {
      var card = track.querySelector(".l-post");
      return card ? card.getBoundingClientRect().width + 24 : track.clientWidth;
    };
    var update = function () {
      var max = track.scrollWidth - track.clientWidth - 2;
      arrows[0].disabled = track.scrollLeft <= 2;
      arrows[1].disabled = track.scrollLeft >= max;
    };
    arrows.forEach(function (btn) {
      btn.addEventListener("click", function () {
        track.scrollBy({ left: step() * +btn.getAttribute("data-dir"), behavior: "smooth" });
      });
    });
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // close the mobile menu after choosing a link
  var menu = document.querySelector(".l-menu");
  if (menu) menu.addEventListener("click", function (e) {
    if (e.target.closest("a")) menu.removeAttribute("open");
  });
})();
