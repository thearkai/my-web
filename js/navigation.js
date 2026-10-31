/* ==========================================================================
   js/navigation.js — mobile drawer, sticky header, active page state
   ========================================================================== */

(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  var toggle = document.querySelector("[data-nav-toggle]");
  var menu = document.querySelector("[data-mobile-menu]");
  var DESKTOP = window.matchMedia("(min-width: 1000px)");

  /* ---------------------------------------------------------------- drawer */
  function isOpen() {
    return menu && menu.classList.contains("is-open");
  }

  function setOpen(open) {
    if (!menu || !toggle) return;

    menu.classList.toggle("is-open", open);
    document.body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");

    // Prevent screen readers / tabbing from reaching the hidden drawer.
    if (open) {
      menu.removeAttribute("inert");
      var firstLink = menu.querySelector("a, button");
      if (firstLink) firstLink.focus({ preventScroll: true });
    } else {
      menu.setAttribute("inert", "");
    }
  }

  if (toggle && menu) {
    menu.setAttribute("inert", "");

    toggle.addEventListener("click", function () {
      setOpen(!isOpen());
    });

    // Close after picking a destination
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) setOpen(false);
    });

    // Escape closes and returns focus to the trigger
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen()) {
        setOpen(false);
        toggle.focus();
      }
    });

    // Growing to desktop width closes the drawer
    DESKTOP.addEventListener("change", function (event) {
      if (event.matches) setOpen(false);
    });
  }

  /* ------------------------------------------------------- sticky header */
  var ticking = false;

  function onScroll() {
    if (header) header.classList.toggle("is-stuck", window.scrollY > 10);

    var toTop = document.querySelector("[data-to-top]");
    if (toTop) toTop.classList.toggle("is-visible", window.scrollY > 600);

    ticking = false;
  }

  window.addEventListener(
    "scroll",
    function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(onScroll);
      }
    },
    { passive: true }
  );

  onScroll();

  /* ----------------------------------------------------- active nav link */
  /* Pages are separate files, so the active link is normally baked into the
     HTML by the build. This is a safety net for any link left unmarked:
     it matches the file name in the URL. */
  function markActive() {
    var file = window.location.pathname.split("/").pop() || "index.html";
    var links = document.querySelectorAll(".nav-link, .mobile-nav-list a");
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute("href");
      if (!href) continue;
      if (href === file || (file === "index.html" && href === "index.html")) {
        links[i].classList.add("is-active");
        links[i].setAttribute("aria-current", "page");
      }
    }
  }

  markActive();
})();
