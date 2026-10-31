/* ==========================================================================
   js/projects.js — project data, filtering and search
   --------------------------------------------------------------------------
   To add a project, add an object to the PROJECTS array below.
   Leave `demo` or `repo` as "" if the link doesn't exist yet — the button is
   then rendered as disabled with an honest label instead of pointing nowhere.
   ========================================================================== */

(function () {
  "use strict";

  var PROJECTS = [
    {
      id: "ark-ai",
      title: "The Ark AI",
      category: "ai",
      categoryLabel: "ai · web app",
      description:
        "An AI-powered assistant designed to support students and teachers with questions, learning, research and discovery.",
      tech: ["HTML", "CSS", "JavaScript"],
      demo: "",                                       // TODO: live demo URL
      repo: "https://github.com/thearkai",            // TODO: point at the exact repository
      image: "",                                      // e.g. "assets/images/projects/ark-ai.jpg"
      placeholder: false,
      year: "in progress"
    },
    {
      id: "project-two",
      title: "Your next project",
      category: "placeholder",
      categoryLabel: "placeholder",
      description:
        "This card is a placeholder. Replace it with a real project — a title, one honest sentence about what it does, and the stack you used.",
      tech: ["—"],
      demo: "",
      repo: "",
      image: "",
      placeholder: true,
      year: "—"
    },
    {
      id: "project-three",
      title: "Another project slot",
      category: "placeholder",
      categoryLabel: "placeholder",
      description:
        "Add as your portfolio grows. Cards are defined in one array at the top of js/projects.js, so new work appears here automatically.",
      tech: ["—"],
      demo: "",
      repo: "",
      image: "",
      placeholder: true,
      year: "—"
    }
  ];

  var grid = document.querySelector("[data-project-grid]");
  if (!grid) return;

  var searchInput = document.querySelector("[data-project-search]");
  var pillBar = document.querySelector("[data-project-filters]");
  var countEl = document.querySelector("[data-project-count]");

  var activeCategory = "all";
  var query = "";

  /* ------------------------------------------------------------- rendering */
  function mediaFor(project) {
    if (project.image) {
      return (
        '<img src="' + project.image + '" alt="' + project.title +
        ' — project preview" loading="lazy" width="640" height="360">'
      );
    }
    // No screenshot supplied yet: use generated placeholder artwork
    return window.Syson.art(project.id, project.title.toLowerCase(), 640, 360);
  }

  function linkButton(label, url, iconId, variant, todoLabel) {
    if (url) {
      return (
        '<a class="btn btn-sm ' + variant + '" href="' + url +
        '" target="_blank" rel="noopener noreferrer">' +
        '<svg class="icon"><use href="#i-' + iconId + '"></use></svg>' + label +
        "</a>"
      );
    }
    return (
      '<button class="btn btn-sm ' + variant +
      '" type="button" disabled aria-disabled="true" title="' + todoLabel + '">' +
      '<svg class="icon"><use href="#i-' + iconId + '"></use></svg>' + label +
      "</button>"
    );
  }

  function cardHTML(project) {
    var ribbon = project.placeholder
      ? '<span class="ribbon">placeholder</span>'
      : "";

    var tags = project.tech
      .map(function (t) { return "<li>" + t + "</li>"; })
      .join("");

    return (
      '<article class="card card--hover project-card reveal" data-category="' +
      project.category + '" data-search="' +
      (project.title + " " + project.description + " " + project.tech.join(" ")).toLowerCase() +
      '">' +
        '<div class="project-media">' + ribbon + mediaFor(project) + "</div>" +
        '<div class="project-body">' +
          '<div class="meta">' + project.categoryLabel + " · " + project.year + "</div>" +
          "<h3>" + project.title + "</h3>" +
          "<p>" + project.description + "</p>" +
          '<ul class="project-tags">' + tags + "</ul>" +
          '<div class="project-actions">' +
            linkButton("view project", project.demo, "external", "btn-outline", "demo link not added yet") +
            linkButton("source code", project.repo, "github", "btn-outline", "repository link not added yet") +
          "</div>" +
        "</div>" +
      "</article>"
    );
  }

  function matches(project) {
    var catOk = activeCategory === "all" || project.category === activeCategory;
    if (!catOk) return false;
    if (!query) return true;
    var haystack = (
      project.title + " " + project.description + " " + project.tech.join(" ")
    ).toLowerCase();
    return haystack.indexOf(query) !== -1;
  }

  function render() {
    var visible = PROJECTS.filter(matches);
    grid.innerHTML = visible.length
      ? visible.map(cardHTML).join("")
      : '<div class="empty-state">' +
          '<svg class="icon" aria-hidden="true"><use href="#i-search-x"></use></svg>' +
          "<p>No projects match that search yet.</p>" +
        "</div>";

    if (countEl) {
      countEl.textContent =
        visible.length + (visible.length === 1 ? " project" : " projects");
    }

    // Cards are injected after the scroll observer has run, so reveal
    // them straight away (or animate if the observer is available).
    var cards = grid.querySelectorAll(".reveal");
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    for (var i = 0; i < cards.length; i++) {
      if (reduce || !("IntersectionObserver" in window)) {
        cards[i].classList.add("is-visible");
      } else {
        cards[i].style.setProperty("--reveal-delay", (i % 3) * 70 + "ms");
        cards[i].classList.add("is-visible");
      }
    }
  }

  /* --------------------------------------------------------------- filters */
  if (pillBar) {
    pillBar.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-category]");
      if (!btn) return;

      activeCategory = btn.getAttribute("data-category");

      var pills = pillBar.querySelectorAll(".pill");
      for (var i = 0; i < pills.length; i++) {
        pills[i].classList.toggle("is-active", pills[i] === btn);
        pills[i].setAttribute("aria-pressed", pills[i] === btn ? "true" : "false");
      }
      render();
    });
  }

  /* ---------------------------------------------------------------- search */
  if (searchInput) {
    var debounce;
    searchInput.addEventListener("input", function () {
      window.clearTimeout(debounce);
      var value = searchInput.value.trim().toLowerCase();
      debounce = window.setTimeout(function () {
        query = value;
        render();
      }, 120);
    });

    // Escape clears the field
    searchInput.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        searchInput.value = "";
        query = "";
        render();
      }
    });
  }

  render();
})();
