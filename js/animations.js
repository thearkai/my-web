/* ==========================================================================
   js/animations.js — starfield, scroll reveals, terminal typing, back-to-top
   All motion is skipped when the visitor prefers reduced motion.
   ========================================================================== */

(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ======================================================================
     1. STARFIELD
     A lightweight canvas: ~90 stars, capped at 30fps, paused when the tab
     is hidden or the section is off-screen.
     ==================================================================== */
  (function starfield() {
    var canvas = document.getElementById("stars");
    if (!canvas || reduceMotion) {
      if (canvas) canvas.style.display = "none";
      return;
    }

    var ctx = canvas.getContext("2d");
    var stars = [];
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var rafId = null;
    var lastFrame = 0;
    var FRAME_MS = 1000 / 30; // 30fps is plenty for slowly twinkling dots

    function size() {
      var w = window.innerWidth;
      var h = window.innerHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      build(w, h);
    }

    function build(w, h) {
      var count = Math.round(Math.min(120, (w * h) / 16000));
      stars = [];
      for (var i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * w,
          y: Math.random() * h,
          r: Math.random() * 1.4 + 0.3,
          base: Math.random() * 0.5 + 0.25,
          speed: Math.random() * 0.0015 + 0.0004,
          phase: Math.random() * Math.PI * 2,
          drift: Math.random() * 0.06 + 0.01
        });
      }
    }

    function draw(time) {
      if (time - lastFrame < FRAME_MS) {
        rafId = window.requestAnimationFrame(draw);
        return;
      }
      lastFrame = time;

      var w = window.innerWidth;
      var h = window.innerHeight;
      ctx.clearRect(0, 0, w, h);

      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        var alpha = s.base + Math.sin(time * s.speed + s.phase) * 0.28;
        if (alpha < 0.05) alpha = 0.05;

        // Slow horizontal drift, wrapping at the edges
        s.x += s.drift;
        if (s.x > w + 2) s.x = -2;

        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = i % 7 === 0
          ? "rgba(147, 197, 253, " + alpha + ")"   // cool blue stars
          : "rgba(226, 232, 240, " + alpha + ")";  // white stars
        ctx.fill();
      }

      rafId = window.requestAnimationFrame(draw);
    }

    function start() {
      if (rafId === null) rafId = window.requestAnimationFrame(draw);
    }
    function stop() {
      if (rafId !== null) {
        window.cancelAnimationFrame(rafId);
        rafId = null;
      }
    }

    size();
    start();

    // Debounced resize
    var resizeTimer;
    window.addEventListener("resize", function () {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(size, 200);
    });

    // Save battery: pause when the tab is in the background
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop();
      else start();
    });
  })();

  /* ======================================================================
     2. REVEAL ON SCROLL
     ==================================================================== */
  (function reveals() {
    var items = document.querySelectorAll(".reveal, .reveal-group");
    if (!items.length) return;

    if (reduceMotion || !("IntersectionObserver" in window)) {
      for (var i = 0; i < items.length; i++) items[i].classList.add("is-visible");
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    for (var j = 0; j < items.length; j++) {
      // Slight stagger for consecutive blocks
      items[j].style.setProperty("--reveal-delay", (j % 4) * 70 + "ms");
      observer.observe(items[j]);
    }
  })();

  /* ======================================================================
     3. TERMINAL TYPING EFFECT
     The code is stored as tokens so syntax highlighting survives while the
     characters are revealed one by one.
     ==================================================================== */
  (function terminal() {
    var body = document.querySelector("[data-terminal]");
    if (!body) return;

    /* Each line is a list of [cssClass, text] tokens. */
    var CODE = [
      [["tk-com", "<!-- hero.html -->"]],
      [["tk-punc", "<"], ["tk-tag", "h1"], ["tk-attr", " class"], ["tk-punc", "="], ["tk-str", "\"hero-title\""], ["tk-punc", ">"]],
      [["tk-str", "  Creative developer"], ["tk-tag", "."]],
      [["tk-punc", "</"], ["tk-tag", "h1"], ["tk-punc", ">"]],
      [["tk-com", ""]],
      [["tk-com", "/* theme.css */"]],
      [["tk-key", ":root"], ["tk-punc", " {"]],
      [["tk-prop", "  --brand"], ["tk-punc", ": "], ["tk-str", "#2563EB"], ["tk-punc", ";"]],
      [["tk-prop", "  --glow"], ["tk-punc", ":  "], ["tk-str", "#8B5CF6"], ["tk-punc", ";"]],
      [["tk-punc", "}"]],
      [["tk-com", ""]],
      [["tk-com", "// app.js"]],
      [["tk-key", "const"], ["tk-punc", " "], ["tk-fn", "dev"], ["tk-punc", " = {"]],
      [["tk-prop", "  name"], ["tk-punc", ": "], ["tk-str", "\"Syson Actin\""], ["tk-punc", ","]],
      [["tk-prop", "  role"], ["tk-punc", ": "], ["tk-str", "\"Creative Web Developer\""], ["tk-punc", ","]],
      [["tk-prop", "  stack"], ["tk-punc", ": ["], ["tk-str", "\"HTML\""], ["tk-punc", ", "], ["tk-str", "\"CSS\""], ["tk-punc", ", "], ["tk-str", "\"JavaScript\""], ["tk-punc", "],"]],
      [["tk-punc", "};"]]
    ];

    /* Build the DOM up-front so layout never jumps while typing. */
    var lines = [];

    function buildShell() {
      body.innerHTML = "";
      for (var i = 0; i < CODE.length; i++) {
        var line = document.createElement("span");
        line.className = "terminal-line";
        // Reserve a non-breaking space so empty lines keep their height
        line.innerHTML = "&nbsp;";
        body.appendChild(line);
        lines.push(line);
      }
    }

    function renderLine(lineEl, tokens) {
      lineEl.innerHTML = "";
      for (var i = 0; i < tokens.length; i++) {
        var span = document.createElement("span");
        if (tokens[i][0]) span.className = tokens[i][0];
        span.textContent = tokens[i][1];
        lineEl.appendChild(span);
      }
    }

    var caret = document.createElement("span");
    caret.className = "caret";
    caret.setAttribute("aria-hidden", "true");

    function typeAll() {
      var lineIndex = 0;

      function nextLine() {
        if (lineIndex >= CODE.length) {
          // Finished — leave the caret blinking on the last line
          lines[lines.length - 1].appendChild(caret);
          return;
        }

        var tokens = CODE[lineIndex];
        var lineEl = lines[lineIndex];
        var totalChars = 0;
        for (var t = 0; t < tokens.length; t++) totalChars += tokens[t][1].length;

        // Empty line: show it immediately and move on
        if (totalChars === 0) {
          lineIndex++;
          window.setTimeout(nextLine, 40);
          return;
        }

        renderLine(lineEl, tokens);
        lineEl.appendChild(caret);

        // Hide every character, then reveal progressively
        var spans = lineEl.querySelectorAll("span:not(.caret)");
        var full = [];
        for (var s = 0; s < spans.length; s++) {
          full.push(spans[s].textContent);
          spans[s].textContent = "";
        }

        var shown = 0;
        var speed = 14; // ms per character

        (function tick() {
          shown++;
          var remaining = shown;
          for (var k = 0; k < spans.length; k++) {
            var len = full[k].length;
            var take = Math.max(0, Math.min(len, remaining));
            spans[k].textContent = full[k].slice(0, take);
            remaining -= take;
          }

          if (shown < totalChars) {
            window.setTimeout(tick, speed);
          } else {
            lineEl.appendChild(caret); // keep the caret at the line end
            lineIndex++;
            window.setTimeout(nextLine, 90);
          }
        })();
      }

      nextLine();
    }

    buildShell();

    if (reduceMotion) {
      // Show the finished code instantly
      for (var i = 0; i < CODE.length; i++) renderLine(lines[i], CODE[i]);
      return;
    }

    // Start when the terminal scrolls into view, not on page load
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              typeAll();
              io.disconnect();
            }
          });
        },
        { threshold: 0.25 }
      );
      io.observe(body);
    } else {
      typeAll();
    }
  })();

  /* ======================================================================
     4. BACK TO TOP
     ==================================================================== */
  (function backToTop() {
    var btn = document.querySelector("[data-to-top]");
    if (!btn) return;

    btn.addEventListener("click", function () {
      window.scrollTo({
        top: 0,
        behavior: reduceMotion ? "auto" : "smooth"
      });
      // Return focus to the start of the document for keyboard users
      var skip = document.querySelector(".skip-link");
      if (skip) skip.focus({ preventScroll: true });
    });
  })();
})();
