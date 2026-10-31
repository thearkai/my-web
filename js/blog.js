/* ==========================================================================
   js/blog.js — filters and search for the article grid
   Works on the cards already present in blog.html, so the content stays
   indexable without JavaScript.
   ========================================================================== */

(function () {
  "use strict";

  var grid = document.querySelector("[data-blog-grid]");
  if (!grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".post-card"));
  var filterBar = document.querySelector("[data-blog-filters]");
  var sidebar = document.querySelector(".sidebar");
  var searchInput = document.querySelector("[data-blog-search]");

  var activeCategory = "all";
  var query = "";

  function apply() {
    var shown = 0;

    cards.forEach(function (card) {
      var cat = card.getAttribute("data-category");
      var text = (card.getAttribute("data-text") || "").toLowerCase();

      var catOk = activeCategory === "all" || cat === activeCategory;
      var textOk = !query || text.indexOf(query) !== -1;
      var visible = catOk && textOk;

      card.style.display = visible ? "" : "none";
      if (visible) shown++;
    });

    var empty = grid.querySelector(".empty-state");
    if (!shown) {
      if (!empty) {
        var div = document.createElement("div");
        div.className = "empty-state";
        div.innerHTML =
          '<svg class="icon" aria-hidden="true"><use href="#i-search-x"></use></svg>' +
          "<p>No articles match that search yet.</p>";
        grid.appendChild(div);
      }
    } else if (empty) {
      empty.remove();
    }
  }

  /* ---------------------------------------------------------- top filters */
  if (filterBar) {
    filterBar.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-category]");
      if (!btn) return;

      activeCategory = btn.getAttribute("data-category");
      var pills = filterBar.querySelectorAll(".pill");
      for (var i = 0; i < pills.length; i++) {
        pills[i].classList.toggle("is-active", pills[i] === btn);
        pills[i].setAttribute("aria-pressed", pills[i] === btn ? "true" : "false");
      }
      syncSidebar();
      apply();
    });
  }

  /* ------------------------------------------------------ sidebar filters */
  function sidebarButtons() {
    return sidebar ? sidebar.querySelectorAll("[data-side-category]") : [];
  }

  function syncSidebar() {
    var buttons = sidebarButtons();
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].classList.toggle(
        "is-active",
        buttons[i].getAttribute("data-side-category") === activeCategory
      );
    }
    // Mirror the sidebar state in the pill bar
    if (filterBar) {
      var pills = filterBar.querySelectorAll(".pill");
      for (var j = 0; j < pills.length; j++) {
        var on = pills[j].getAttribute("data-category") === activeCategory;
        pills[j].classList.toggle("is-active", on);
        pills[j].setAttribute("aria-pressed", on ? "true" : "false");
      }
    }
  }

  if (sidebar) {
    sidebar.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-side-category]");
      if (!btn) return;
      activeCategory = btn.getAttribute("data-side-category");
      syncSidebar();
      apply();
      // Move focus somewhere sensible on long pages
      if (grid.offsetTop < window.scrollY - 300) {
        grid.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  }

  /* --------------------------------------------------------------- search */
  if (searchInput) {
    var debounce;
    searchInput.addEventListener("input", function () {
      window.clearTimeout(debounce);
      var value = searchInput.value.trim().toLowerCase();
      debounce = window.setTimeout(function () {
        query = value;
        apply();
      }, 120);
    });

    searchInput.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        searchInput.value = "";
        query = "";
        apply();
      }
    });
  }

  apply();
})();
