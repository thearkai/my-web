/* ==========================================================================
   js/gallery.js — gallery grid, category filter and accessible lightbox
   --------------------------------------------------------------------------
   Add items to the GALLERY array. Set `src` to a real file path as soon as
   you have one (e.g. "assets/images/gallery/my-photo.jpg"); until then the
   item renders generated placeholder artwork and is labelled as such.
   ========================================================================== */

(function () {
  "use strict";

  var GALLERY = [
    {
      title: "Portrait",
      caption: "Karuhanga Syson · Creative Web Developer",
      category: "personal",
      src: "assets/images/gallery/portrait-480.jpg",
      full: "assets/images/gallery/portrait-800.jpg",
      // portrait images are cropped by the tile, so bias the framing upwards
      position: "50% 18%",
      alt: "Portrait of Karuhanga Syson wearing a blue pinstripe suit and bow tie"
    }

    // To add another, save the file in assets/images/gallery/ and append:
    //
    //   ,{
    //     title: "Code snippet",
    //     caption: "Building the interface, one line at a time",
    //     category: "screenshots",   // projects | screenshots | certificates | creative | personal
    //     src: "assets/images/gallery/code-snippet.jpg",
    //     full: "assets/images/gallery/code-snippet@2x.jpg",   // optional, used by the lightbox
    //     alt: "Describe the image for screen readers"
    //   }
  ];

  var grid = document.querySelector("[data-gallery-grid]");
  if (!grid) return;

  var filterBar = document.querySelector("[data-gallery-filters]");
  var lightbox = document.querySelector("[data-lightbox]");
  var stage = document.querySelector("[data-lightbox-stage]");
  var captionEl = document.querySelector("[data-lightbox-caption]");
  var countEl = document.querySelector("[data-lightbox-count]");
  var closeBtn = document.querySelector("[data-lightbox-close]");
  var prevBtn = document.querySelector("[data-lightbox-prev]");
  var nextBtn = document.querySelector("[data-lightbox-next]");

  var activeCategory = "all";
  var visibleItems = [];
  var currentIndex = 0;
  var lastFocused = null;

  /* ---------------------------------------------------------------- render */
  function media(item) {
    if (item.src) {
      var style = item.position
        ? ' style="object-position:' + item.position + '"'
        : "";
      return '<img src="' + item.src + '" alt="' + item.alt + '" loading="lazy"' + style + ">";
    }
    return window.Syson.art(item.title, item.title.toLowerCase().replace(/\s+/g, "-"), 640, 480);
  }

  function itemHTML(item, index) {
    var isPlaceholder = !item.src;
    return (
      '<button class="gallery-item" type="button" data-index="' + index +
      '" aria-label="Open ' + item.title + ' in the viewer">' +
        '<div class="gallery-thumb">' + media(item) + "</div>" +
        '<div class="gallery-caption">' +
          "<strong>" + item.title + "</strong>" +
          "<span>" + item.caption + (isPlaceholder ? " · placeholder" : "") + "</span>" +
        "</div>" +
      "</button>"
    );
  }

  function render() {
    visibleItems = GALLERY.filter(function (item) {
      return activeCategory === "all" || item.category === activeCategory;
    });

    if (visibleItems.length) {
      grid.innerHTML = visibleItems.map(itemHTML).join("");
    } else {
      var message = GALLERY.length
        ? "Nothing in this category yet."
        : "No images yet. Add photographs to assets/images/gallery/ and list them in js/gallery.js.";
      grid.innerHTML =
        '<div class="empty-state">' +
          '<svg class="icon" aria-hidden="true"><use href="#i-image"></use></svg>' +
          "<p>" + message + "</p>" +
        "</div>";
    }

    // One or two images shouldn't be squeezed into a four-column grid
    grid.classList.toggle("is-sparse", visibleItems.length > 0 && visibleItems.length <= 2);

    // The filters only earn their space once there is something to filter
    if (filterBar) {
      var categories = {};
      GALLERY.forEach(function (i) { categories[i.category] = true; });
      filterBar.style.display = Object.keys(categories).length > 1 ? "" : "none";
    }
  }

  /* --------------------------------------------------------------- filters */
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
      render();
    });
  }

  /* --------------------------------------------------------------- lightbox */
  function openLightbox(index) {
    if (!lightbox || !visibleItems.length) return;
    lastFocused = document.activeElement;
    currentIndex = index;
    updateLightbox();

    lightbox.classList.add("is-open");
    lightbox.removeAttribute("inert");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("nav-open");
    if (closeBtn) closeBtn.focus({ preventScroll: true });
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("inert", "");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("nav-open");
    if (lastFocused && lastFocused.focus) lastFocused.focus({ preventScroll: true });
  }

  function updateLightbox() {
    var item = visibleItems[currentIndex];
    if (!item || !stage) return;

    stage.innerHTML = item.src
      ? '<img src="' + (item.full || item.src) + '" alt="' + item.alt + '">'
      : window.Syson.art(item.title, item.title.toLowerCase(), 960, 640);

    if (captionEl) {
      captionEl.innerHTML =
        "<span><strong>" + item.title + "</strong> — " + item.caption + "</span>";
    }
    if (countEl) {
      countEl.textContent = currentIndex + 1 + " / " + visibleItems.length;
    }
    var single = visibleItems.length < 2;
    if (prevBtn) prevBtn.disabled = single;
    if (nextBtn) nextBtn.disabled = single;
  }

  function step(direction) {
    if (!visibleItems.length) return;
    currentIndex =
      (currentIndex + direction + visibleItems.length) % visibleItems.length;
    updateLightbox();
  }

  if (grid) {
    grid.addEventListener("click", function (event) {
      var card = event.target.closest(".gallery-item");
      if (!card) return;
      openLightbox(parseInt(card.getAttribute("data-index"), 10));
    });
  }

  if (closeBtn) closeBtn.addEventListener("click", closeLightbox);
  if (prevBtn) prevBtn.addEventListener("click", function () { step(-1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { step(1); });

  // Click on the backdrop closes
  if (lightbox) {
    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox) closeLightbox();
    });

    // Keyboard: arrows to navigate, Escape to close, Tab stays inside
    document.addEventListener("keydown", function (event) {
      if (!lightbox.classList.contains("is-open")) return;

      if (event.key === "Escape") {
        event.preventDefault();
        closeLightbox();
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        step(1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        step(-1);
      } else if (event.key === "Tab") {
        // Simple focus trap across the lightbox controls
        var focusable = lightbox.querySelectorAll("button:not([disabled])");
        if (!focusable.length) return;
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });
  }

  render();
})();
