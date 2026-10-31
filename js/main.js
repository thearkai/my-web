/* ==========================================================================
   js/main.js — shared configuration and site-wide helpers
   --------------------------------------------------------------------------
   EDIT THIS FILE to plug in your real links. Everything is configured here,
   in one place, and the whole site picks it up.
   ========================================================================== */

(function () {
  "use strict";

  /* ======================================================================
     SOCIAL LINKS
     Paste the full URL for each profile. Leave "" if you don't have one yet —
     the icon stays visible but is marked "not configured" and shows a short
     message instead of leading nowhere.
     ==================================================================== */
  var SOCIALS = {
    github: "https://github.com/thearkai", // confirmed
    tiktok: "",                            // TODO: e.g. "https://www.tiktok.com/@yourhandle"
    linkedin: "",                          // TODO
    instagram: "",                         // TODO
    facebook: "",                          // TODO
    x: "",                                 // TODO
    youtube: ""                            // TODO
  };

  /* ======================================================================
     TOAST — small, accessible message used for unconfigured links
     ==================================================================== */
  var toastEl = null;
  var toastTimer = null;

  function toast(message) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      toastEl.setAttribute("role", "status");
      toastEl.setAttribute("aria-live", "polite");
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = message;
    // Force a frame so the transition runs again
    void toastEl.offsetWidth;
    toastEl.classList.add("is-visible");

    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () {
      toastEl.classList.remove("is-visible");
    }, 3200);
  }

  /* ======================================================================
     APPLY SOCIAL CONFIG
     ==================================================================== */
  function applySocials() {
    var links = document.querySelectorAll("[data-social]");
    for (var i = 0; i < links.length; i++) {
      (function (link) {
        var key = link.getAttribute("data-social");
        var url = SOCIALS[key];

        if (url) {
          link.setAttribute("href", url);
          link.setAttribute("target", "_blank");
          link.setAttribute("rel", "noopener noreferrer");
          link.removeAttribute("aria-disabled");
          link.classList.remove("is-unconfigured");
        } else {
          link.setAttribute("href", "#");
          link.classList.add("is-unconfigured");
          link.setAttribute("aria-disabled", "true");
          link.setAttribute("title", key + " — link not added yet");

          link.addEventListener("click", function (event) {
            event.preventDefault();
            toast(
              "“" + key + "” isn't connected yet — add your link in js/main.js"
            );
          });
        }
      })(links[i]);
    }
  }

  /* ======================================================================
     COPY EMAIL TO CLIPBOARD (contact page convenience)
     ==================================================================== */
  function initCopyEmail() {
    var buttons = document.querySelectorAll("[data-copy-email]");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener("click", function () {
        var email = this.getAttribute("data-copy-email");

        function done() { toast("Email copied — " + email); }

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(email).then(done, function () {
            toast("Copy failed — the address is " + email);
          });
        } else {
          toast("Your email is " + email);
        }
      });
    }
  }

  /* ======================================================================
     FOOTER YEAR — keeps the copyright current automatically
     ==================================================================== */
  function initYear() {
    var els = document.querySelectorAll("[data-year]");
    var year = new Date().getFullYear();
    for (var i = 0; i < els.length; i++) els[i].textContent = year;
  }

  /* ======================================================================
     PLACEHOLDER ART
     Deterministic SVG artwork used wherever a real image hasn't been
     supplied yet, so empty slots still look designed instead of broken.
     Swap these out by adding real files in assets/images/ and filling in
     the `src` property in js/gallery.js / js/projects.js.
     ==================================================================== */
  function hashString(str) {
    var h = 0;
    for (var i = 0; i < str.length; i++) {
      h = (h << 5) - h + str.charCodeAt(i);
      h |= 0;
    }
    return Math.abs(h);
  }

  /**
   * Build a decorative SVG for a placeholder tile.
   * @param {string} seed   text used to pick the colours/layout
   * @param {string} label  small caption baked into the artwork
   * @param {number} w,h    viewBox size
   */
  function art(seed, label, w, h) {
    w = w || 640;
    h = h || 400;

    var n = hashString(seed);
    var hue1 = 208 + (n % 42);
    var hue2 = 258 + ((n >> 7) % 42);
    var id = "a" + (n % 100000);
    var variant = n % 3;
    var shapes = "";

    if (variant === 0) {
      // orbit rings
      for (var i = 1; i <= 3; i++) {
        shapes +=
          '<circle cx="' + (w * 0.68) + '" cy="' + (h * 0.46) + '" r="' + (46 + i * 34) +
          '" fill="none" stroke="url(#' + id + 'g)" stroke-width="1.2" opacity="' +
          (0.6 - i * 0.14).toFixed(2) + '"/>';
      }
      shapes += '<circle cx="' + (w * 0.68) + '" cy="' + (h * 0.46) + '" r="7" fill="url(#' + id + 'g)"/>';
    } else if (variant === 1) {
      // stacked code lines
      for (var r = 0; r < 5; r++) {
        shapes +=
          '<rect x="' + (w * 0.14) + '" y="' + (h * 0.24 + r * (h * 0.105)) + '" width="' +
          (80 + ((n >> r) % 5) * 44) + '" height="9" rx="4.5" fill="url(#' + id + 'g)" opacity="' +
          (0.85 - r * 0.13).toFixed(2) + '"/>';
      }
    } else {
      // isometric terrain
      var pts = [];
      for (var px = 0; px < 7; px++) {
        pts.push(
          (w * 0.14 + px * (w * 0.115)) + "," + (h * 0.6 + ((n >> px) % 7) * 9 - 27)
        );
      }
      shapes +=
        '<polyline points="' + pts.join(" ") + '" fill="none" stroke="url(#' + id +
        'g)" stroke-width="1.5" opacity=".75"/>';
      shapes +=
        '<polyline points="' + pts.join(" ") + '" fill="none" stroke="url(#' + id +
        'g)" stroke-width="1.5" opacity=".35" transform="translate(0,30)"/>';
      shapes +=
        '<polyline points="' + pts.join(" ") + '" fill="none" stroke="url(#' + id +
        'g)" stroke-width="1.5" opacity=".16" transform="translate(0,60)"/>';
    }

    // corner brackets
    var brackets =
      '<path d="M26 26h16M26 26v16" stroke="#243049" stroke-width="1.4" fill="none"/>' +
      '<path d="M' + (w - 26) + ' 26h-16M' + (w - 26) + ' 26v16" stroke="#243049" stroke-width="1.4" fill="none"/>' +
      '<path d="M26 ' + (h - 26) + 'h16M26 ' + (h - 26) + 'v-16" stroke="#243049" stroke-width="1.4" fill="none"/>' +
      '<path d="M' + (w - 26) + ' ' + (h - 26) + 'h-16M' + (w - 26) + ' ' + (h - 26) + 'v-16" stroke="#243049" stroke-width="1.4" fill="none"/>';

    return (
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + " " + h +
      '" role="img" aria-label="' + label.replace(/"/g, "&quot;") +
      ' placeholder artwork" preserveAspectRatio="xMidYMid slice">' +
      "<defs>" +
      '<linearGradient id="' + id + 'g" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0%" stop-color="hsl(' + hue1 + ',88%,64%)"/>' +
      '<stop offset="100%" stop-color="hsl(' + hue2 + ',82%,68%)"/>' +
      "</linearGradient>" +
      '<linearGradient id="' + id + 'bg" x1="0" y1="0" x2=".7" y2="1">' +
      '<stop offset="0%" stop-color="hsl(' + hue2 + ',44%,13%)"/>' +
      '<stop offset="100%" stop-color="#080B12"/>' +
      "</linearGradient>" +
      '<radialGradient id="' + id + 'glow" cx=".68" cy=".4" r=".65">' +
      '<stop offset="0%" stop-color="hsl(' + hue2 + ',92%,62%)" stop-opacity=".3"/>' +
      '<stop offset="100%" stop-color="hsl(' + hue2 + ',92%,62%)" stop-opacity="0"/>' +
      "</radialGradient>" +
      "</defs>" +
      '<rect width="' + w + '" height="' + h + '" fill="url(#' + id + 'bg)"/>' +
      '<rect width="' + w + '" height="' + h + '" fill="url(#' + id + 'glow)"/>' +
      '<g stroke="#1B2637" stroke-width="0.7" opacity=".55">' +
      '<path d="M0 ' + h * 0.33 + "H" + w + '"/><path d="M0 ' + h * 0.66 + "H" + w + '"/>' +
      '<path d="M' + w * 0.33 + " 0V" + h + '"/><path d="M' + w * 0.66 + " 0V" + h + '"/>' +
      "</g>" + shapes + brackets +
      '<rect x="26" y="' + (h - 40) + '" width="26" height="2.4" rx="1.2" fill="url(#' + id + 'g)" opacity=".9"/>' +
      '<text x="26" y="' + (h - 22) + '" font-family="ui-monospace, Menlo, monospace" font-size="12" fill="#5A6B82" letter-spacing="0.4">' +
      label.toLowerCase().replace(/[<>&]/g, "") + "</text>" +
      "</svg>"
    );
  }

  /* ======================================================================
     BOOT
     ==================================================================== */
  function init() {
    applySocials();
    initCopyEmail();
    initYear();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  /* Public helpers */
  window.Syson = {
    SOCIALS: SOCIALS,
    toast: toast,
    art: art
  };
})();
