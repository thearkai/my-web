/* ==========================================================================
   Syson Actin — portfolio
   js/theme.js — dark/light theme toggle
   --------------------------------------------------------------------------
   Dark is the default. The chosen theme is remembered in localStorage and,
   on first visit, the visitor's operating-system preference is respected.
   A tiny inline script in <head> applies the saved theme before first paint
   so the page never flashes the wrong colours.
   ========================================================================== */

(function () {
  "use strict";

  var STORAGE_KEY = "syson-theme";
  var root = document.documentElement;

  function readStored() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (err) {
      return null; // private mode / storage disabled
    }
  }

  function writeStored(theme) {
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch (err) {
      /* ignore */
    }
  }

  /* Reflect the current theme in the toggle buttons' accessible state. */
  function syncButtons(theme) {
    var buttons = document.querySelectorAll("[data-theme-toggle]");
    for (var i = 0; i < buttons.length; i++) {
      var next = theme === "light" ? "dark" : "light";
      buttons[i].setAttribute("aria-label", "Switch to " + next + " mode");
      buttons[i].setAttribute("aria-pressed", theme === "light" ? "true" : "false");
      buttons[i].setAttribute("title", "Switch to " + next + " mode");
    }
  }

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    syncButtons(theme);
    // Let other scripts (e.g. the star canvas) react to the change.
    document.dispatchEvent(
      new CustomEvent("themechange", { detail: { theme: theme } })
    );
  }

  function getTheme() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function toggle() {
    var next = getTheme() === "light" ? "dark" : "light";
    apply(next);
    writeStored(next);
  }

  /* Wire up every button on the page marked [data-theme-toggle]. */
  function init() {
    var buttons = document.querySelectorAll("[data-theme-toggle]");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener("click", toggle);
    }
    syncButtons(getTheme());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Expose for other modules if needed.
  window.SysonTheme = { toggle: toggle, apply: apply, get: getTheme };
})();
