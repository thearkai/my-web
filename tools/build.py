#!/usr/bin/env python3
"""
tools/build.py — assembles the static pages from shared partials.

The published site is plain HTML: running this script rewrites the nine
.html files at the project root. You can edit those files directly if you
prefer — this builder exists so the header, footer and icon sprite stay
identical across every page.

    python3 tools/build.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

SITE_NAME = "Syson Actin"
SITE_URL = "https://thearkai.github.io/syson-portfolio"   # change after deploying
EMAIL = "actinsyson24@gmail.com"
LOCATION = "Rurehe, Mitooma District, Uganda"

# ---------------------------------------------------------------------------
# ICON SPRITE
# ---------------------------------------------------------------------------
STROKE = ('<g fill="none" stroke="currentColor" stroke-width="1.8" '
          'stroke-linecap="round" stroke-linejoin="round">%s</g>')

ICONS = {
    # --- interface -------------------------------------------------------
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "sun": '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.2 5.2l1.4 1.4M17.4 17.4l1.4 1.4M18.8 5.2l-1.4 1.4M6.6 17.4l-1.4 1.4"/>',
    "moon": '<path d="M20.8 13.2A8.6 8.6 0 1 1 10.8 3.2a6.7 6.7 0 0 0 10 10Z"/>',
    "arrow-right": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M20 12H5M11 6l-6 6 6 6"/>',
    "arrow-up": '<path d="M12 20V5M6 11l6-6 6 6"/>',
    "chevron-left": '<path d="M15 5.5 8.5 12 15 18.5"/>',
    "chevron-right": '<path d="M9 5.5 15.5 12 9 18.5"/>',
    "search": '<circle cx="11" cy="11" r="6.6"/><path d="M16 16l4.5 4.5"/>',
    "search-x": '<circle cx="11" cy="11" r="6.6"/><path d="M16 16l4.5 4.5M9 9l4 4M13 9l-4 4"/>',
    "external": '<path d="M14 4h6v6M20 4l-8.5 8.5"/><path d="M18 14v4.5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 18.5v-11A1.5 1.5 0 0 1 5.5 6H10"/>',
    "check": '<path d="M4.5 12.5l4.8 4.8L19.5 7"/>',
    "alert": '<path d="M12 3.5 21.5 20H2.5L12 3.5Z"/><path d="M12 9.5v4.5M12 17h.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.8h.01"/>',
    "download": '<path d="M12 3.5v11.5M7.5 10.5 12 15l4.5-4.5"/><path d="M4.5 19.5h15"/>',
    "send": '<path d="M21 3 10.5 13.5"/><path d="M21 3l-6.8 18-3.7-7.5L3 9.8 21 3Z"/>',
    "sparkle": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3Z"/>',
    "code": '<path d="M8.5 7 3.5 12l5 5M15.5 7l5 5-5 5"/>',
    "terminal": '<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M7 10.5l2.5 2L7 14.5M12.5 15H17"/>',
    "layers": '<path d="M12 3 3 7.8l9 4.8 9-4.8L12 3Z"/><path d="M3 12.6 12 17.4l9-4.8M3 17l9 4.8L21 17"/>',
    "zap": '<path d="M13 2.5 4.5 14H11l-1 7.5L20 9.5h-6.5l1-7Z"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.2 0 2-.9 2-2 0-1.6-1.4-2-1.4-3.2 0-1 .8-1.8 2-1.8H17a4 4 0 0 0 4-4c0-3.9-4-7-9-7Z"/><circle cx="7.8" cy="10.5" r="1.1" fill="currentColor" stroke="none"/><circle cx="11" cy="7.5" r="1.1" fill="currentColor" stroke="none"/><circle cx="15.2" cy="8.6" r="1.1" fill="currentColor" stroke="none"/>',
    "rocket": '<path d="M5 15c-1 2.5-1 5-1 5s2.5 0 5-1"/><path d="M9 19c-1.5-1.5-2-3.5-1.5-5.5C9.5 8 13 4 20 3c1 7-3 10.5-8.5 12.5C9.5 16 7.5 15.5 6 14Z"/><circle cx="15" cy="9" r="1.6"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5V5.5Z"/><path d="M8 7.5h8M8 11h5"/>',
    "monitor": '<rect x="2.5" y="4" width="19" height="13" rx="2.5"/><path d="M8.5 21h7M12 17v4"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>',
    "graduation": '<path d="M2.5 9 12 4.5 21.5 9 12 13.5 2.5 9Z"/><path d="M6.5 11.4V16c0 1.7 2.5 3 5.5 3s5.5-1.3 5.5-3v-4.6"/>',
    "briefcase": '<rect x="2.5" y="7" width="19" height="12.5" rx="2.5"/><path d="M8.5 7V5.5A1.5 1.5 0 0 1 10 4h4a1.5 1.5 0 0 1 1.5 1.5V7M2.5 12.5h19"/>',
    "pin": '<path d="M12 21s7-5.8 7-11a7 7 0 1 0-14 0c0 5.2 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
    "mail": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M3.5 7 12 13l8.5-6"/>',
    "phone": '<path d="M6.5 3.5h3l1.5 4-2 1.5a11.5 11.5 0 0 0 6 6l1.5-2 4 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.7a2 2 0 0 1 2-2.2Z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.4l3.4 2"/>',
    "camera": '<path d="M3 8.5A2.5 2.5 0 0 1 5.5 6h1.7l1.3-2h7l1.3 2h1.7A2.5 2.5 0 0 1 21 8.5v9A2.5 2.5 0 0 1 18.5 20h-13A2.5 2.5 0 0 1 3 17.5v-9Z"/><circle cx="12" cy="13" r="3.4"/>',
    "certificate": '<rect x="3" y="3.5" width="18" height="13" rx="2"/><path d="M7 7.5h6M7 11h3.5"/><path d="M16.5 16.5v4l2-1.3 2 1.3v-4"/>',
    "quote": '<path d="M9 6.5c-3 1.4-4.5 3.7-4.5 6.8 0 2.4 1.4 4.2 3.4 4.2 1.8 0 3.1-1.3 3.1-3 0-1.6-1.1-2.8-2.6-2.8-.3 0-.6 0-.8.1.4-1.6 1.6-2.9 3.3-3.8L9 6.5Zm9 0c-3 1.4-4.5 3.7-4.5 6.8 0 2.4 1.4 4.2 3.4 4.2 1.8 0 3.1-1.3 3.1-3 0-1.6-1.1-2.8-2.6-2.8-.3 0-.6 0-.8.1.4-1.6 1.6-2.9 3.3-3.8L18 6.5Z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3.2 9.5h17.6M3.2 14.5h17.6"/><path d="M12 3c2.6 2.5 3.9 5.6 3.9 9s-1.3 6.5-3.9 9c-2.6-2.5-3.9-5.6-3.9-9S9.4 5.5 12 3Z"/>',
    "git-branch": '<circle cx="6.5" cy="6" r="2.5"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="9" r="2.5"/><path d="M6.5 8.5v7M17.5 11.5c0 3-2.5 4-6.5 4.5"/>',
    "image": '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><circle cx="8.5" cy="10" r="1.6"/><path d="M4 17l5-4.5 4 3.5 3-2.5 4 3.5"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-9.4A4.1 4.1 0 0 1 12 7.6a4.1 4.1 0 0 1 7.5 3C19.5 15.4 12 20 12 20Z"/>',
    "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 1 3.5 10.9c-.6.4-.9 1-.9 1.7v.4H9.4v-.4c0-.7-.3-1.3-.9-1.7A6 6 0 0 1 12 3Z"/>',
    "filter": '<path d="M3.5 6h17M6.5 12h11M10 18h4"/>',
    # --- social (filled) -------------------------------------------------
    "github": '<path fill="currentColor" stroke="none" d="M12 2C6.48 2 2 6.58 2 12.25c0 4.53 2.87 8.37 6.84 9.73.5.09.68-.22.68-.49 0-.24-.01-1.05-.01-1.9-2.78.61-3.37-1.2-3.37-1.2-.45-1.17-1.11-1.48-1.11-1.48-.91-.63.07-.62.07-.62 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.34 1.12 2.91.85.09-.66.35-1.12.63-1.38-2.22-.26-4.56-1.14-4.56-5.05 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.71 0 0 .84-.28 2.75 1.05a9.4 9.4 0 0 1 2.5-.34c.85 0 1.71.12 2.51.34 1.91-1.33 2.75-1.05 2.75-1.05.55 1.41.2 2.45.1 2.71.64.72 1.03 1.63 1.03 2.75 0 3.92-2.35 4.79-4.57 5.04.36.32.68.94.68 1.9 0 1.37-.01 2.47-.01 2.81 0 .27.18.59.69.49A10.02 10.02 0 0 0 22 12.25C22 6.58 17.52 2 12 2Z"/>',
    "linkedin": '<path fill="currentColor" stroke="none" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3V9Zm6 0h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.7 8.65 22 10.6 22 14v7h-4v-6.2c0-1.5-.5-2.5-1.85-2.5-1.1 0-1.75.75-2.03 1.47-.1.26-.12.62-.12.98V21H9V9Z"/>',
    "instagram": '<rect x="3.2" y="3.2" width="17.6" height="17.6" rx="5.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.1" cy="6.9" r="1.2" fill="currentColor"/>',
    "facebook": '<path fill="currentColor" stroke="none" d="M13.5 21v-8h2.7l.4-3h-3.1V8.1c0-.87.24-1.46 1.49-1.46H17V4.06c-.3-.04-1.3-.13-2.47-.13-2.44 0-4.11 1.49-4.11 4.23V10H7.7v3h2.72v8h3.08Z"/>',
    "x": '<path fill="currentColor" stroke="none" d="M17.53 3h3.2l-7.01 8.01L22 21h-6.44l-5.05-6.6L4.7 21H1.5l7.5-8.57L1.5 3h6.6l4.56 6.03L17.53 3Zm-1.12 16.1h1.77L7.62 4.8H5.72l10.69 14.3Z"/>',
    "youtube": '<path fill="currentColor" stroke="none" fill-rule="evenodd" d="M21.6 7.2a2.5 2.5 0 0 0-1.76-1.77C18.25 5 12 5 12 5s-6.25 0-7.84.43A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.76 1.77C5.75 19 12 19 12 19s6.25 0 7.84-.43a2.5 2.5 0 0 0 1.76-1.77A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8ZM10 15.2V8.8l5.2 3.2-5.2 3.2Z"/>',
    "tiktok": '<path fill="currentColor" stroke="none" d="M16.6 5.8c.9.7 2 1.1 3.2 1.2v2.6c-1.2 0-2.4-.3-3.4-.9v5.6a5.4 5.4 0 1 1-5.4-5.4c.2 0 .4 0 .6.03v2.7a2.7 2.7 0 1 0 1.9 2.6V2h2.6c.1 1.5.6 2.8 1.5 3.8Z"/>',
}

# Tech logos (filled, brand colours handled by CSS)
TECH_LOGOS = {
    "html": '<svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path fill="#E34F26" d="M3 2h18l-1.6 18L12 22 4.6 20 3 2Z"/><path fill="#F06529" d="M12 20.4V3.6h7.9L18.4 19 12 20.4Z"/><path fill="#EBEBEB" d="M7.4 6.6h9.2l-.25 2.9H10.5l.2 2.2h5.4l-.6 6.6L12 19.2l-3.5-.9-.2-2.6h2.7l.1 1.1 1.9.5 1.9-.5.2-2.1H8.1L7.4 6.6Z"/></svg>',
    "css": '<svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path fill="#1572B6" d="M3 2h18l-1.6 18L12 22 4.6 20 3 2Z"/><path fill="#33A9DC" d="M12 20.4V3.6h7.9L18.4 19 12 20.4Z"/><path fill="#EBEBEB" d="M16.2 9.5H9.4l.2 2.3h6.4l-.6 6.4-3.4.9-3.4-.9-.2-2.6h2.6l.1 1.1 1.9.5 1.9-.5.2-2.4H7.1l-.6-6.8h11l-.3 2.3Z"/></svg>',
    "js": '<svg viewBox="0 0 24 24" role="img" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="2.5" fill="#F7DF1E"/><path fill="#0B1220" d="M12.2 17.2c0 2.2-1.3 3.3-3.2 3.3-1.7 0-2.7-.9-3.2-2.2l1.8-1.1c.3.6.6 1.1 1.4 1.1.7 0 1.1-.3 1.1-1.3v-6.6h2.1v6.8ZM18.6 20.5c-2 0-3.3-1-3.9-2.3l1.8-1c.4.8 1 1.3 2 1.3.9 0 1.4-.4 1.4-1s-.6-.9-1.6-1.3l-.6-.3c-1.7-.7-2.8-1.6-2.8-3.5 0-1.7 1.3-3 3.3-3 1.5 0 2.5.5 3.3 1.9l-1.7 1.1c-.4-.7-.8-.9-1.6-.9-.7 0-1.1.4-1.1 1s.4.8 1.5 1.2l.6.3c2 .9 3.1 1.7 3.1 3.7 0 2.1-1.6 3.2-3.7 3.2Z"/></svg>',
}

def sprite() -> str:
    """Inline SVG sprite — one symbol per icon, referenced with <use href="#i-name">."""
    parts = []
    for name, body in ICONS.items():
        wrapped = body
        if 'fill="currentColor"' not in body or "stroke=" in body:
            # stroke icons go in a group with shared stroke settings
            if "fill=\"currentColor\"" in body and "<rect" in body:
                wrapped = body  # mixed icons (instagram) keep their own attributes
            else:
                wrapped = STROKE % body
        parts.append(
            '<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (name, wrapped)
        )
    return (
        '<svg aria-hidden="true" focusable="false" '
        'style="position:absolute;width:0;height:0;overflow:hidden">'
        + "".join(parts) +
        "</svg>"
    )


def icon(name: str, cls: str = "icon") -> str:
    return '<svg class="%s" aria-hidden="true"><use href="#i-%s"></use></svg>' % (cls, name)


# ---------------------------------------------------------------------------
# HEAD
# ---------------------------------------------------------------------------
HEAD = """<!DOCTYPE html>
<html lang="en" class="no-js" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>${title}</title>
  <meta name="description" content="${description}">
  <meta name="author" content="Karuhanga Syson">
  <meta name="theme-color" content="#080B12">

  <link rel="canonical" href="${canonical}">

  <!-- Open Graph / Twitter -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Syson Actin">
  <meta property="og:title" content="${og_title}">
  <meta property="og:description" content="${description}">
  <meta property="og:url" content="${canonical}">
  <meta property="og:image" content="${site_url}/assets/images/brand/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${og_title}">
  <meta name="twitter:description" content="${description}">
  <meta name="twitter:image" content="${site_url}/assets/images/brand/og-image.jpg">

  <!-- Icons -->
  <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="favicon-16.png" sizes="16x16" type="image/png">
  <link rel="apple-touch-icon" href="assets/images/brand/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  <!-- Styles -->
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/theme.css">
  <link rel="stylesheet" href="css/animations.css">
  <link rel="stylesheet" href="css/responsive.css">

  <!-- Apply the saved theme before first paint (avoids a flash of the wrong colour) -->
  <script>
    (function () {
      document.documentElement.classList.remove("no-js");
      try {
        // Dark is the designed default. Only an explicit choice changes it.
        var saved = localStorage.getItem("syson-theme");
        if (saved === "light" || saved === "dark") {
          document.documentElement.setAttribute("data-theme", saved);
        }
      } catch (e) {}
    })();
  </script>
</head>
"""

# ---------------------------------------------------------------------------
# HEADER / FOOTER
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    ("index.html", "home"),
    ("about.html", "about"),
    ("skills.html", "skills"),
    ("projects.html", "projects"),
    ("gallery.html", "gallery"),
    ("blog.html", "blog"),
    ("contact.html", "contact"),
]

# Shorter list for the desktop bar; the drawer and footer carry the rest.
NAV_PRIMARY = NAV_ITEMS[:6] + [("contact.html", "contact")]

BRAND_MARK = """<img class="brand-mark"
             src="assets/images/brand/crest-96.png"
             srcset="assets/images/brand/crest-96.png 1x, assets/images/brand/crest-128.png 2x"
             alt="" width="36" height="36" loading="eager" decoding="async">"""

HEADER = """<header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Syson Actin — home">
        ${brand}
        <span>syson actin.</span>
      </a>

      <nav class="nav" aria-label="Primary">
        <ul class="nav-list">
${nav_links}
        </ul>
      </nav>

      <div class="header-actions">
        <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch to light mode">
          <svg class="icon icon-moon" aria-hidden="true"><use href="#i-moon"></use></svg>
          <svg class="icon icon-sun" aria-hidden="true"><use href="#i-sun"></use></svg>
        </button>
        <button class="icon-btn nav-toggle" type="button" data-nav-toggle
                aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">
          <svg class="icon" aria-hidden="true"><use href="#i-menu"></use></svg>
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile drawer -->
  <div class="mobile-menu" id="mobile-menu" data-mobile-menu>
    <nav aria-label="Mobile">
      <ul class="mobile-nav-list">
${mobile_links}
      </ul>
    </nav>
    <div class="mobile-menu-foot">
      <p>${email}</p>
      <p>${location}</p>
    </div>
  </div>
"""

FOOTER = """<footer class="site-footer">
    <div class="container">
      <div class="footer-main">
        <div class="footer-brand">
          <a class="brand" href="index.html" aria-label="Syson Actin — home">
            ${brand}
            <span>syson actin.</span>
          </a>
          <p>Building clean, responsive interfaces with HTML, CSS and JavaScript — and learning something new with every project.</p>
          <p class="tagline">The Innovator | Creative Web Developer</p>
        </div>

        <div class="footer-col">
          <h3>explore</h3>
          <ul class="footer-links">
            <li><a href="index.html">home</a></li>
            <li><a href="about.html">about</a></li>
            <li><a href="skills.html">skills</a></li>
            <li><a href="projects.html">projects</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h3>more</h3>
          <ul class="footer-links">
            <li><a href="gallery.html">gallery</a></li>
            <li><a href="blog.html">blog</a></li>
            <li><a href="contact.html">contact</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h3>contact</h3>
          <ul class="footer-contact">
            <li>${icon_mail}<a href="mailto:${email}">${email}</a></li>
            <li>${icon_pin}<span>${location}</span></li>
          </ul>
          <h3 class="mt-3">follow</h3>
          <ul class="socials">
${social_links}
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© <span data-year>2026</span> Syson Actin. All rights reserved.</p>
        <ul class="footer-nav">
${footer_nav}
        </ul>
      </div>
    </div>
  </footer>

  <button class="to-top" type="button" data-to-top aria-label="Back to top">
    ${icon_up}
  </button>
"""

SOCIALS = [
    ("github", "GitHub"),
    ("linkedin", "LinkedIn"),
    ("instagram", "Instagram"),
    ("facebook", "Facebook"),
    ("x", "X"),
    ("youtube", "YouTube"),
    ("tiktok", "TikTok"),
]


def social_list(indent="            ") -> str:
    rows = []
    for key, label in SOCIALS:
        rows.append(
            '%s<li><a href="#" data-social="%s" aria-label="%s">%s</a></li>'
            % (indent, key, label, icon(key))
        )
    return "\n".join(rows)


def header(active: str) -> str:
    nav_links = "\n".join(
        '          <li><a class="nav-link%s" href="%s"%s>%s</a></li>'
        % (" is-active" if href == active else "", href,
           ' aria-current="page"' if href == active else "", label)
        for href, label in NAV_PRIMARY
    )
    mobile_links = "\n".join(
        '        <li><a href="%s"%s>%s%s</a></li>'
        % (href,
           ' class="is-active" aria-current="page"' if href == active else "",
           label,
           icon("chevron-right"))
        for href, label in NAV_ITEMS
    )
    return (
        HEADER.replace("${brand}", BRAND_MARK)
        .replace("${nav_links}", nav_links)
        .replace("${mobile_links}", mobile_links)
        .replace("${email}", EMAIL)
        .replace("${location}", LOCATION)
    )


def footer() -> str:
    footer_nav = "\n".join(
        '          <li><a href="%s">%s</a></li>' % (href, label)
        for href, label in NAV_ITEMS
    )
    return (
        FOOTER.replace("${brand}", BRAND_MARK)
        .replace("${icon_mail}", icon("mail", "icon"))
        .replace("${icon_pin}", icon("pin", "icon"))
        .replace("${icon_up}", icon("arrow-up", "icon"))
        .replace("${social_links}", social_list())
        .replace("${footer_nav}", footer_nav)
        .replace("${email}", EMAIL)
        .replace("${location}", LOCATION)
    )


# ---------------------------------------------------------------------------
# SHARED BLOCKS
# ---------------------------------------------------------------------------
def page_head_block(kicker: str, title_html: str, lead: str) -> str:
    return """    <div class="page-head">
      <p class="kicker">%s</p>
      <h1 class="page-title">%s</h1>
      <p class="lead">%s</p>
    </div>""" % (kicker, title_html, lead)


WG_FRAMES = """      <div class="wireframes" aria-hidden="true">
        <div class="wireframe wireframe--1">
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="1"><path d="M50 6 90 30v40L50 94 10 70V30L50 6Z"/><path d="M50 6v88M10 30l40 24 40-24M10 70l40-16 40 16"/></svg>
        </div>
        <div class="wireframe wireframe--2">
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="1"><path d="M50 8 88 50 50 92 12 50 50 8Z"/><path d="M50 26 70 50 50 74 30 50 50 26Z"/></svg>
        </div>
        <div class="wireframe wireframe--3">
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="1"><path d="M20 80 20 30l30-16 30 16v50"/><path d="M35 80V45l15-8 15 8v35"/></svg>
        </div>
      </div>"""


def art_inline(seed_label: str, w: int = 640, h: int = 360, variant: int = 0) -> str:
    """Python twin of window.Syson.art — decorative artwork for static markup."""
    import hashlib
    n = int(hashlib.md5(seed_label.encode()).hexdigest(), 16)
    hue1 = 208 + (n % 42)
    hue2 = 258 + ((n >> 7) % 42)
    uid = "p%d" % (n % 99999)

    if variant == 1:                       # stacked code lines
        shapes = "".join(
            '<rect x="%d" y="%d" width="%d" height="9" rx="4.5" fill="url(#%s-g)" opacity="%s"/>'
            % (w * 0.14, h * 0.24 + i * (h * 0.105), 80 + ((n >> i) % 5) * 44,
               uid, round(0.85 - i * 0.13, 2))
            for i in range(5)
        )
        shapes += ('<rect x="%d" y="%d" width="34" height="9" rx="4.5" fill="url(#%s-g)" opacity=".3"/>'
                   % (w * 0.14, h * 0.24 + 5 * (h * 0.105), uid))
    elif variant == 2:                     # orbit rings
        shapes = "".join(
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="url(#%s-g)" stroke-width="1.2" opacity="%s"/>'
            % (w * 0.68, h * 0.46, 46 + i * 34, uid, round(0.6 - i * 0.14, 2))
            for i in range(3)
        )
        shapes += ('<circle cx="%d" cy="%d" r="7" fill="url(#%s-g)"/>' % (w * 0.68, h * 0.46, uid))
    else:                                  # isometric terrain
        pts = " ".join(
            "%d,%d" % (w * 0.14 + i * (w * 0.115), h * 0.6 + ((n >> i) % 7) * 9 - 27)
            for i in range(7)
        )
        shapes = "".join(
            '<polyline points="%s" fill="none" stroke="url(#%s-g)" stroke-width="1.5" opacity="%s" transform="translate(0,%d)"/>'
            % (pts, uid, op, off)
            for off, op in ((0, 0.75), (30, 0.35), (60, 0.16))
        )

    # corner brackets give every tile the same "technical" framing
    brackets = ""
    for (bx, by, sx, sy) in ((26, 26, 1, 1), (w - 26, 26, -1, 1), (26, h - 26, 1, -1), (w - 26, h - 26, -1, -1)):
        brackets += '<path d="M%d %d h%d M%d %d v%d" stroke="#243049" stroke-width="1.4" fill="none"/>' % (
            bx, by, 16 * sx, bx, by, 16 * sy)

    return (
        '<svg viewBox="0 0 %d %d" role="img" aria-label="%s placeholder artwork" preserveAspectRatio="xMidYMid slice">'
        "<defs>"
        '<linearGradient id="%s-g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="hsl(%d,88%%,64%%)"/>'
        '<stop offset="1" stop-color="hsl(%d,82%%,68%%)"/>'
        "</linearGradient>"
        '<linearGradient id="%s-bg" x1="0" y1="0" x2=".7" y2="1">'
        '<stop offset="0" stop-color="hsl(%d,44%%,13%%)"/>'
        '<stop offset="1" stop-color="#080B12"/>'
        "</linearGradient>"
        '<radialGradient id="%s-glow" cx=".68" cy=".4" r=".65">'
        '<stop offset="0" stop-color="hsl(%d,92%%,62%%)" stop-opacity=".30"/>'
        '<stop offset="1" stop-color="hsl(%d,92%%,62%%)" stop-opacity="0"/>'
        "</radialGradient>"
        "</defs>"
        '<rect width="%d" height="%d" fill="url(#%s-bg)"/>'
        '<rect width="%d" height="%d" fill="url(#%s-glow)"/>'
        '<g stroke="#1B2637" stroke-width=".7" opacity=".55">'
        '<path d="M0 %d H%d"/><path d="M0 %d H%d"/><path d="M%d 0 V%d"/><path d="M%d 0 V%d"/>'
        "</g>%s%s"
        '<rect x="26" y="%d" width="26" height="2.4" rx="1.2" fill="url(#%s-g)" opacity=".9"/>'
        '<text x="26" y="%d" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#5A6B82" letter-spacing=".4">%s</text>'
        "</svg>"
    ) % (
        w, h, seed_label,
        uid, hue1, hue2,
        uid, hue2,
        uid, hue2, hue2,
        w, h, uid, w, h, uid,
        h * 0.33, w, h * 0.66, w, w * 0.33, h, w * 0.66, h,
        shapes, brackets,
        h - 40, uid, h - 24, seed_label.replace("&", "and"),
    )


# ---------- bespoke artwork for the featured project ----------------------
ARK_MOCK = """<svg viewBox='0 0 800 500' role='img' aria-label='Concept mockup of The Ark AI assistant interface' preserveAspectRatio='xMidYMid slice'>
            <defs>
              <linearGradient id='arkbg' x1='0' y1='0' x2='.8' y2='1'>
                <stop offset='0' stop-color='#101A2E'/><stop offset='1' stop-color='#080B12'/>
              </linearGradient>
              <linearGradient id='arkgrad' x1='0' y1='0' x2='1' y2='1'>
                <stop offset='0' stop-color='#2563EB'/><stop offset='1' stop-color='#8B5CF6'/>
              </linearGradient>
              <radialGradient id='arkglow' cx='.75' cy='.2' r='.7'>
                <stop offset='0' stop-color='#8B5CF6' stop-opacity='.30'/>
                <stop offset='1' stop-color='#8B5CF6' stop-opacity='0'/>
              </radialGradient>
            </defs>
            <rect width='800' height='500' fill='url(#arkbg)'/>
            <rect width='800' height='500' fill='url(#arkglow)'/>
            <g stroke='#1B2637' stroke-width='.8' opacity='.5'>
              <path d='M0 125H800'/><path d='M0 250H800'/><path d='M0 375H800'/>
              <path d='M200 0V500'/><path d='M400 0V500'/><path d='M600 0V500'/>
            </g>
            <g opacity='.35' stroke='url(#arkgrad)' stroke-width='1' fill='none'>
              <circle cx='640' cy='150' r='70'/><circle cx='640' cy='150' r='110'/>
              <path d='M540 60 700 120 660 230 520 180Z'/>
            </g>
            <!-- window chrome -->
            <rect x='64' y='58' width='672' height='384' rx='16' fill='#0B1220' stroke='#1E293B'/>
            <circle cx='88' cy='84' r='5' fill='#FF5F57'/><circle cx='106' cy='84' r='5' fill='#FEBC2E'/><circle cx='124' cy='84' r='5' fill='#28C840'/>
            <text x='148' y='88' font-family='ui-monospace, Menlo, monospace' font-size='12' fill='#64748B'>the ark ai — assistant</text>
            <path d='M64 104H736' stroke='#1E293B'/>
            <!-- user message -->
            <rect x='404' y='128' width='300' height='52' rx='14' fill='url(#arkgrad)' opacity='.9'/>
            <rect x='424' y='145' width='210' height='7' rx='3.5' fill='#FFFFFF' opacity='.85'/>
            <rect x='424' y='160' width='140' height='7' rx='3.5' fill='#FFFFFF' opacity='.55'/>
            <!-- assistant reply -->
            <rect x='92' y='200' width='344' height='112' rx='14' fill='#111B2E' stroke='#243049'/>
            <circle cx='116' cy='226' r='9' fill='url(#arkgrad)'/>
            <text x='132' y='230' font-family='Inter, Arial, sans-serif' font-size='12' fill='#93A3B8'>ark</text>
            <rect x='112' y='248' width='290' height='7' rx='3.5' fill='#3B4A61'/>
            <rect x='112' y='264' width='248' height='7' rx='3.5' fill='#33415A'/>
            <rect x='112' y='280' width='170' height='7' rx='3.5' fill='#2B383F'/>
            <!-- second user message -->
            <rect x='464' y='284' width='240' height='44' rx='14' fill='url(#arkgrad)' opacity='.55'/>
            <rect x='484' y='300' width='150' height='7' rx='3.5' fill='#FFFFFF' opacity='.7'/>
            <!-- input bar -->
            <rect x='92' y='356' width='612' height='52' rx='26' fill='#0E1727' stroke='#243049'/>
            <text x='120' y='387' font-family='Inter, Arial, sans-serif' font-size='13' fill='#4B5A70'>ask about your homework…</text>
            <circle cx='672' cy='382' r='17' fill='url(#arkgrad)'/>
            <path d='M665 382h14M673 376l6 6-6 6' stroke='#fff' stroke-width='1.8' fill='none' stroke-linecap='round' stroke-linejoin='round'/>
            <text x='64' y='476' font-family='ui-monospace, Menlo, monospace' font-size='12' fill='#4B5A70'>concept mockup — not a screenshot of finished software</text>
          </svg>"""



# ---------------------------------------------------------------------------
# SMALL COMPONENT HELPERS
# ---------------------------------------------------------------------------
def tpl(s: str, **kw) -> str:
    for k, v in kw.items():
        s = s.replace("${%s}" % k, str(v))
    return s


def skill_card(logo_key, name, blurb, status):
    return """          <article class='card card--hover skill-card reveal'>
            <span class='skill-logo'>%s</span>
            <h3>%s</h3>
            <p>%s</p>
            <span class='skill-status'>%s</span>
          </article>""" % (TECH_LOGOS[logo_key], name, blurb, status)


def strength_card(ic, title, text):
    return """          <article class='card card--hover card-pad reveal'>
            <span class='icon-tile' style='margin-bottom:.9rem'>%s</span>
            <h3 class='card-title'>%s</h3>
            <p class='card-text'>%s</p>
          </article>""" % (icon(ic), title, text)


def cta_block(title, lead, primary=("contact.html", "start a conversation"),
              secondary=("projects.html", "see my work")):
    return """      <div class='card card-pad glow-border reveal' style='padding:clamp(1.4rem,4vw,2.6rem)'>
        <div class='section-head' style='margin-bottom:0'>
          <div>
            <h2 class='section-title'>%s</h2>
            <p class='lead mt-2'>%s</p>
          </div>
          <div class='badge-row'>
            <a class='btn btn-primary' href='%s'>%s %s</a>
            <a class='btn btn-outline' href='%s'>%s</a>
          </div>
        </div>
      </div>""" % (title, lead, primary[0], primary[1], icon("arrow-right"),
                   secondary[0], secondary[1])


# ============================== HOME =======================================
HOME = """
    <section class='hero'>
      <div class='container'>
        <div class='hero-grid'>
          <div class='hero-copy'>
            <p class='badge badge--accent'>creative web developer · a-level student</p>

            <h1 class='hero-title page-enter'>Welcome! I'm <span class='grad-text'>Syson Actin</span> — A Creative Web Developer.</h1>

            <p class='hero-sub'>The Innovator<span class='sep'>|</span>Turning creative ideas into powerful digital experiences.</p>

            <p class='hero-desc'>
              I'm <strong>Karuhanga Syson</strong>, professionally known as Syson Actin — an A-Level
              student from Rurehe, Mitooma District, Uganda. I build clean, responsive websites with
              HTML, CSS and JavaScript, and I'm currently developing <strong>The Ark AI</strong>, an
              assistant designed to help students and teachers learn.
            </p>

            <div class='hero-actions'>
              <a class='btn btn-primary' href='projects.html'>explore my projects %s</a>
              <a class='btn btn-outline' href='contact.html'>contact me</a>
            </div>

            <div class='hero-tech'>
              <span class='label'>working with</span>
              <span class='badge'>%s HTML</span>
              <span class='badge'>%s CSS</span>
              <span class='badge'>%s JavaScript</span>
            </div>
          </div>

          <div class='hero-visual'>
            <div class='terminal' aria-hidden='false'>
              <div class='terminal-bar'>
                <span class='dot dot--red'></span>
                <span class='dot dot--amber'></span>
                <span class='dot dot--green'></span>
                <span class='terminal-file'>syson-actin.js</span>
              </div>
              <div class='terminal-body' data-terminal aria-label='Animated sample of HTML, CSS and JavaScript'></div>
            </div>
          </div>
        </div>
      </div>
      <div class='wireframes' aria-hidden='true'>
        <div class='wireframe wireframe--1'><svg viewBox='0 0 100 100' fill='none' stroke='currentColor' stroke-width='1'><path d='M50 6 90 30v40L50 94 10 70V30L50 6Z'/><path d='M50 6v88M10 30l40 24 40-24M10 70l40-16 40 16'/></svg></div>
        <div class='wireframe wireframe--2'><svg viewBox='0 0 100 100' fill='none' stroke='currentColor' stroke-width='1'><path d='M50 8 88 50 50 92 12 50 50 8Z'/><path d='M50 26 70 50 50 74 30 50 50 26Z'/></svg></div>
      </div>
    </section>

    <!-- ============================ short intro ============================ -->
    <section class='section'>
      <div class='container'>
        <div class='split'>
          <div class='reveal'>
            <p class='kicker'>a little about me</p>
            <h2 class='section-title'>Curiosity first, code second.</h2>
            <p class='lead mt-3'>
              My interest in technology started with one question — <em>how does this actually
              work?</em> — and it never really stopped. Today I turn that curiosity into working
              websites, and I care about the details most people never notice: fast page loads,
              readable code, layouts that survive a small screen, and interfaces that make sense
              to someone using them for the first time.
            </p>
            <a class='btn btn-quiet mt-3' href='about.html'>read the full story %s</a>
          </div>

          <div class='stack reveal'>
            <blockquote class='quote'>
              The Innovator — turning creative ideas into powerful digital solutions.
              <footer>— Syson Actin</footer>
            </blockquote>
            <div class='card card-pad'>
              <h3 class='card-title'>currently</h3>
              <ul class='footer-contact' style='margin-top:.6rem'>
                <li>%s<span>Studying for A-Level</span></li>
                <li>%s<span>Building The Ark AI</span></li>
                <li>%s<span>Learning JavaScript, one project at a time</span></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================ skills preview ========================= -->
    <section class='section'>
      <div class='container'>
        <div class='section-head reveal'>
          <div>
            <p class='kicker'>what i work with</p>
            <h2 class='section-title'>The toolkit, honestly.</h2>
          </div>
          <a class='btn btn-outline btn-sm' href='skills.html'>all skills %s</a>
        </div>

        <div class='grid grid-3 reveal-group'>
%s
        </div>
      </div>
    </section>

    <!-- ============================ featured project ======================= -->
    <section class='section'>
      <div class='container'>
        <div class='section-head reveal'>
          <div>
            <p class='kicker'>featured project</p>
            <h2 class='section-title'>The Ark AI</h2>
          </div>
          <a class='btn btn-outline btn-sm' href='projects.html'>all projects %s</a>
        </div>

        <article class='card card--hover reveal' style='overflow:hidden'>
          <div class='split' style='gap:0'>
            <div class='project-media' style='border-bottom:0;aspect-ratio:16/10'>
              %s
            </div>
            <div class='project-body' style='padding:clamp(1.2rem,3vw,2rem)'>
              <div class='meta'>ai · web app · in progress</div>
              <h3 style='font-size:1.25rem'>An assistant for students and teachers</h3>
              <p>
                The Ark AI is an AI-powered assistant designed to support students and teachers
                with questions, learning, research and discovery. I'm building it to be clear and
                forgiving to use — good feedback, honest limits, and no dead ends when something
                goes wrong.
              </p>
              <ul class='project-tags'>
                <li>HTML</li><li>CSS</li><li>JavaScript</li>
              </ul>
              <div class='project-actions'>
                <a class='btn btn-outline btn-sm' href='projects.html'>project details %s</a>
              </div>
            </div>
          </div>
        </article>
      </div>
    </section>

    <!-- ============================ strengths ============================== -->
    <section class='section'>
      <div class='container'>
        <div class='section-head reveal'>
          <div>
            <p class='kicker'>how i work</p>
            <h2 class='section-title'>What you can count on.</h2>
          </div>
        </div>
        <div class='grid grid-4 reveal-group'>
%s
        </div>
      </div>
    </section>

    <!-- ============================ cta ==================================== -->
    <section class='section'>
      <div class='container'>
%s
      </div>
    </section>
""" % (
    icon("arrow-right"),
    icon("code", "icon"), icon("palette", "icon"), icon("zap", "icon"),
    icon("arrow-right"),
    icon("graduation"), icon("rocket"), icon("bulb"),
    icon("arrow-right"),
    "\n".join([
        skill_card("html", "HTML", "Clean, semantic markup that search engines and screen readers both understand.", "comfortable"),
        skill_card("css", "CSS", "Responsive layouts, custom properties and a design system that stays consistent.", "comfortable"),
        skill_card("js", "JavaScript", "Interactivity without frameworks — DOM, events, forms and small utilities.", "in progress"),
    ]),
    icon("arrow-right"),
    ARK_MOCK,
    icon("arrow-right"),
    "\n".join([
        strength_card("target", "Attention to detail", "Spacing, alignment and wording get the same care as the code. The small things are the product."),
        strength_card("code", "Readable code", "Indented, commented and organised so the next person — usually future me — can pick it up."),
        strength_card("monitor", "Responsive by default", "Designed mobile-first, then tested up through tablet and desktop sizes."),
        strength_card("bulb", "Fast learner", "New tools and ideas get picked up quickly. When I don't know something, I say so and go and learn it."),
    ]),
    cta_block(
        "Let's build something together.",
        "I'm open to collaborations, projects and honest feedback. If you've got an idea worth building, I'd like to hear about it.",
    ),
)


# ============================== ABOUT ======================================
def fact(ic, label, value):
    return """              <div class='fact'>
                <span class='icon-tile'>%s</span>
                <div class='fact-body'>
                  <span class='fact-label'>%s</span>
                  <span class='fact-value'>%s</span>
                </div>
              </div>""" % (icon(ic), label, value)


ABOUT = """
    <div class='container'>
%s

      <div class='split about-hero'>
        <!-- portrait -->
        <div class='reveal'>
          <div class='portrait-frame'>
            <div class='portrait-inner'>
              <!-- Replace this placeholder block with:
                   <img src='assets/images/profile/profile.jpg'
                        alt='Karuhanga Syson (Syson Actin)' width='600' height='650'> -->
              <div class='portrait-placeholder'>
                <span class='initials'>SA</span>
                <span class='hint'>photograph slot — add your image at assets/images/profile/profile.jpg</span>
              </div>
              <img class='portrait-brand' src='assets/images/brand/crest-96.png'
                   alt='' width='26' height='26' loading='lazy' decoding='async'>
            </div>
          </div>
          <blockquote class='quote mt-4'>
            Small steps in coding today, big dreams for tomorrow.
            <footer>— Syson Actin</footer>
          </blockquote>
        </div>

        <!-- biography + quick facts -->
        <div class='stack reveal'>
          <div class='card card-pad'>
            <h2 class='section-title' style='font-size:1.35rem'>About me</h2>
            <p class='mt-3'>
              I'm <strong>KARUHANGA SYSON</strong>, professionally known as
              <strong>Syson Actin</strong>, a creative web developer and A-Level student from
              Rurehe, Mitooma District, Uganda.
            </p>
            <p>
              I'm passionate about building modern, responsive web applications that solve real
              problems and create value. I enjoy learning new technologies, exploring creative ideas
              and turning them into digital solutions.
            </p>
            <p>
              My work so far is front-end: semantic HTML, CSS that adapts properly to the screen
              it's on, and JavaScript that does something useful without dragging in a framework.
              I'm still early in this journey — which means I ask a lot of questions, test things
              properly, and would rather ship something honest than something impressive-looking
              that breaks.
            </p>
            <div class='badge-row mt-4'>
              <a class='btn btn-outline btn-sm' href='projects.html'>see my projects</a>
            </div>
          </div>

          <div class='card facts'>
            <h3 class='facts-title'>quick facts</h3>
%s
          </div>
        </div>
      </div>

      <!-- fact strip -->
      <div class='card card-pad mt-4 reveal'>
        <div class='fact-strip'>
          <div class='fact-strip-item'>
            <span class='icon-tile'>%s</span>
            <div class='fact-body'><span class='fact-label'>Real name</span><span class='fact-value'>KARUHANGA SYSON</span></div>
          </div>
          <div class='fact-strip-item'>
            <span class='icon-tile'>%s</span>
            <div class='fact-body'><span class='fact-label'>Professional name</span><span class='fact-value'>Syson Actin</span></div>
          </div>
          <div class='fact-strip-item'>
            <span class='icon-tile'>%s</span>
            <div class='fact-body'><span class='fact-label'>Location</span><span class='fact-value'>Rurehe, Mitooma District, Uganda</span></div>
          </div>
          <div class='fact-strip-item'>
            <span class='icon-tile'>%s</span>
            <div class='fact-body'><span class='fact-label'>Email</span><a class='fact-value' href='mailto:actinsyson24@gmail.com'>actinsyson24@gmail.com</a></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================ journey ================================ -->
    <section class='section'>
      <div class='container'>
        <div class='section-head reveal'>
          <div>
            <p class='kicker'>my journey</p>
            <h2 class='section-title'>How I got here.</h2>
          </div>
        </div>

        <div class='timeline reveal'>
          <div class='timeline-item'>
            <h3>A question, not a plan</h3>
            <p>It started with wondering how websites actually work underneath. Curiosity came first; the tutorials came after.</p>
          </div>
          <div class='timeline-item'>
            <h3>Learning the basics properly</h3>
            <p>HTML for structure, CSS for layout and responsive design, then JavaScript for behaviour — practised by rebuilding interfaces I liked until they made sense.</p>
          </div>
          <div class='timeline-item'>
            <h3>Building something of my own</h3>
            <p>That led to <strong>The Ark AI</strong>, an assistant for students and teachers, where the ideas finally have somewhere to go.</p>
          </div>
          <div class='timeline-item'>
            <h3>Next</h3>
            <p>Going deeper on JavaScript, writing about what I learn, and collaborating with other developers — including anyone reading this.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================ interests ============================== -->
    <section class='section'>
      <div class='container'>
        <div class='section-head reveal'>
          <div>
            <p class='kicker'>my interests</p>
            <h2 class='section-title'>What keeps me curious.</h2>
          </div>
        </div>
        <div class='grid grid-4 reveal-group'>
%s
        </div>
      </div>
    </section>

    <!-- ============================ philosophy ============================= -->
    <section class='section'>
      <div class='container'>
        <div class='split'>
          <div class='reveal'>
            <p class='kicker'>development philosophy</p>
            <h2 class='section-title'>Three rules I try to code by.</h2>
            <div class='timeline mt-4'>
              <div class='timeline-item'>
                <h3>Simple beats clever</h3>
                <p>If a piece of code needs a paragraph to explain it, it probably needs rewriting instead.</p>
              </div>
              <div class='timeline-item'>
                <h3>Design for the smallest screen first</h3>
                <p>If it works on a phone with a slow connection, it works everywhere else.</p>
              </div>
              <div class='timeline-item'>
                <h3>Be honest about what I don't know</h3>
                <p>Claiming more than I can do helps nobody — least of all the person trusting me with their project.</p>
              </div>
            </div>
          </div>

          <div class='card card-pad reveal'>
            <p class='kicker'>my goals</p>
            <h3 class='card-title' style='font-size:1.15rem'>Where this is going</h3>
            <ul class='footer-links mt-3' style='gap:.6rem'>
%s
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class='section'>
      <div class='container'>
%s
      </div>
    </section>
""" % (
    page_head_block("about", "get to <span class='grad-text'>know me</span>",
                    "I'm KARUHANGA SYSON, professionally known as Syson Actin — a creative web developer and A-Level student from Rurehe, Mitooma District, Uganda."),
    "\n".join([
        fact("user", "Real name", "KARUHANGA SYSON"),
        fact("sparkle", "Professional name", "Syson Actin"),
        fact("pin", "Location", "Rurehe, Mitooma District, Uganda"),
        fact("graduation", "Education", "A-Level student"),
        fact("briefcase", "Profession", "Web Developer"),
        fact("mail", "Email", "actinsyson24@gmail.com"),
    ]),
    icon("user"), icon("sparkle"), icon("pin"), icon("mail"),
    "\n".join([
        strength_card("code", "Web development", "Turning an idea into an interface that works on every screen."),
        strength_card("rocket", "AI and new tools", "Curious about applied AI — The Ark AI is where I'm exploring it."),
        strength_card("palette", "Design", "Layout, spacing and type. A page should feel calm to read."),
        strength_card("target", "Problem solving", "Breaking a vague problem down until the next step is obvious."),
    ]),
    "\n".join([
        "              <li style='display:flex;gap:.5rem'>%s<span>Build projects real people actually use.</span></li>" % icon("check"),
        "              <li style='display:flex;gap:.5rem'>%s<span>Get properly fluent in JavaScript, then keep going.</span></li>" % icon("check"),
        "              <li style='display:flex;gap:.5rem'>%s<span>Collaborate with other developers and learn from how they work.</span></li>" % icon("check"),
        "              <li style='display:flex;gap:.5rem'>%s<span>Build a professional identity that stands up internationally.</span></li>" % icon("check"),
        "              <li style='display:flex;gap:.5rem'>%s<span>Finish A-Level with results I'm proud of.</span></li>" % icon("check"),
    ]),
    cta_block("Want to know more?", "The fastest way is to talk to me — I answer every message.",
              ("contact.html", "get in touch"), ("skills.html", "see what i use")),
)


# ============================== SKILLS =====================================
SKILLS = """
    <div class='container'>
%s

      <section class='section' style='padding-top:.5rem'>
        <div class='section-head reveal'>
          <div>
            <p class='kicker'>core technologies</p>
            <h2 class='section-title'>Three tools, used properly.</h2>
          </div>
        </div>
        <div class='grid grid-3 reveal-group'>
          <article class='card card--hover skill-card'>
            <span class='skill-logo'>%s</span>
            <h3>HTML</h3>
            <p>Website structure. Semantic elements, sensible document order, forms and landmarks that assistive technology can navigate.</p>
            <span class='skill-status'>comfortable</span>
          </article>
          <article class='card card--hover skill-card'>
            <span class='skill-logo'>%s</span>
            <h3>CSS</h3>
            <p>Styling, responsive layouts and visual design. Flexbox, grid, custom properties, mobile-first breakpoints and light/dark theming.</p>
            <span class='skill-status'>comfortable</span>
          </article>
          <article class='card card--hover skill-card'>
            <span class='skill-logo'>%s</span>
            <h3>JavaScript</h3>
            <p>Interactivity and functionality. DOM manipulation, events, form validation and small utilities — written without frameworks.</p>
            <span class='skill-status'>in progress</span>
          </article>
        </div>
      </section>

      <section class='section'>
        <div class='section-head reveal'>
          <div>
            <p class='kicker'>tools &amp; technologies</p>
            <h2 class='section-title'>Room to grow.</h2>
            <p class='lead mt-2'>These are slots, not claims. Each one gets filled in only when I've actually built something with it.</p>
          </div>
        </div>

        <div class='grid grid-4 reveal-group'>
%s
        </div>

        <div class='notice mt-4'>
          %s
          <div>
            <strong>An honest note:</strong> this portfolio lists only the technologies I currently
            work with — HTML, CSS and JavaScript. Everything below is a placeholder for future
            learning, so that nothing here overstates what I can do yet.
          </div>
        </div>
      </section>

      <section class='section'>
        <div class='split'>
          <div class='reveal'>
            <p class='kicker'>how i learn</p>
            <h2 class='section-title'>Practice over promises.</h2>
            <p class='lead mt-3'>
              I learn by building: pick something small and real, finish it, then work out what I'd
              do differently. That's why this site, The Ark AI and every project card is a genuine
              work in progress rather than a list of things I intend to do.
            </p>
          </div>
          <div class='card card-pad reveal'>
            <h3 class='card-title'>what that looks like in practice</h3>
            <ul class='footer-links mt-3' style='gap:.55rem'>
%s
            </ul>
          </div>
        </div>
      </section>
    </div>

    <section class='section'>
      <div class='container'>
%s
      </div>
    </section>
""" % (
    page_head_block("skills", "what i <span class='grad-text'>work with</span>",
                    "The technologies I currently use to build websites — plus honest space for what comes next."),
    TECH_LOGOS["html"], TECH_LOGOS["css"], TECH_LOGOS["js"],
    "\n".join([
        "<div class='slot'>%s<span>git &amp; github<br><span class='faint'>next up</span></span></div>" % icon("git-branch"),
        "<div class='slot'>%s<span>a css framework<br><span class='faint'>to evaluate</span></span></div>" % icon("layers"),
        "<div class='slot'>%s<span>javascript framework<br><span class='faint'>to learn</span></span></div>" % icon("zap"),
        "<div class='slot'>%s<span>design tool<br><span class='faint'>to explore</span></span></div>" % icon("palette"),
        "<div class='slot'>%s<span>backend &amp; apis<br><span class='faint'>later</span></span></div>" % icon("terminal"),
        "<div class='slot'>%s<span>your suggestion<br><span class='faint'>open to it</span></span></div>" % icon("sparkle"),
    ]),
    icon("info"),
    "\n".join(
        "              <li style='display:flex;gap:.5rem'>%s<span>%s</span></li>" % (icon("check"), txt)
        for txt in [
            "Reading the documentation before copying a solution.",
            "Testing layouts on real phones, not just a resized browser.",
            "Writing down what broke, so it doesn't break twice.",
            "Asking better questions each time.",
        ]
    ),
    cta_block("See these skills in action.", "The projects page shows what I've actually built with them.",
              ("projects.html", "browse projects"), ("contact.html", "contact me")),
)


# ============================== PROJECTS ===================================
PROJECTS = """
    <div class='container'>
%s

      <div class='section-head' style='align-items:center'>
        <div class='filter-bar' data-project-filters style='margin:0'>
          <button class='pill is-active' type='button' data-category='all' aria-pressed='true'>all</button>
          <button class='pill' type='button' data-category='ai' aria-pressed='false'>ai</button>
          <button class='pill' type='button' data-category='placeholder' aria-pressed='false'>placeholders</button>
        </div>
        <div class='search'>
          %s
          <label class='sr-only' for='project-search'>Search projects</label>
          <input id='project-search' type='search' data-project-search placeholder='search projects…' autocomplete='off'>
        </div>
      </div>

      <p class='meta mb-4' data-project-count aria-live='polite'></p>

      <div class='project-grid' data-project-grid></div>

      <div class='notice mt-5'>
        %s
        <div>
          <strong>Links are configurable.</strong> Project entries live in
          <code>js/projects.js</code>. Any demo or repository that doesn't exist yet shows a
          disabled button rather than a link that goes nowhere — nothing here points at a URL
          that hasn't been supplied.
        </div>
      </div>
    </div>

    <section class='section'>
      <div class='container'>
%s
      </div>
    </section>
""" % (
    page_head_block("projects", "my <span class='grad-text'>projects</span>",
                    "A small, honest collection — built or in progress. Everything here is real work; slots marked as placeholders are waiting for real work."),
    icon("search"),
    icon("info"),
    cta_block("Have something in mind?", "I'd rather build one useful thing with you than ten impressive-looking ones alone.",
              ("contact.html", "start a conversation"), ("skills.html", "what i work with")),
)


# ============================== GALLERY ====================================
GALLERY = """
    <div class='container'>
%s

      <div class='filter-bar' data-gallery-filters>
        <button class='pill is-active' type='button' data-category='all' aria-pressed='true'>all</button>
        <button class='pill' type='button' data-category='projects' aria-pressed='false'>projects</button>
        <button class='pill' type='button' data-category='screenshots' aria-pressed='false'>screenshots</button>
        <button class='pill' type='button' data-category='certificates' aria-pressed='false'>certificates</button>
        <button class='pill' type='button' data-category='creative' aria-pressed='false'>creative work</button>
        <button class='pill' type='button' data-category='personal' aria-pressed='false'>personal moments</button>
      </div>

      <div class='gallery-grid' data-gallery-grid></div>

      <div class='notice mt-5'>
        %s
        <div>
          <strong>More photographs are on the way.</strong> To add one, save it in
          <code>assets/images/gallery/</code> and list it in <code>js/gallery.js</code> — the grid,
          the category filters and the lightbox pick it up automatically.
        </div>
      </div>

    <!-- ============================ lightbox =============================== -->
    <div class='lightbox' data-lightbox role='dialog' aria-modal='true' aria-label='Image viewer' aria-hidden='true' inert>
      <button class='icon-btn lightbox-close' type='button' data-lightbox-close aria-label='Close viewer'>%s</button>
      <button class='lightbox-nav lightbox-prev' type='button' data-lightbox-prev aria-label='Previous image'>%s</button>
      <button class='lightbox-nav lightbox-next' type='button' data-lightbox-next aria-label='Next image'>%s</button>
      <figure class='lightbox-figure'>
        <div class='lightbox-stage' data-lightbox-stage></div>
        <figcaption>
          <span data-lightbox-caption></span>
          <span class='count' data-lightbox-count></span>
        </figcaption>
      </figure>
    </div>

    <section class='section'>
      <div class='container'>
%s
      </div>
    </section>
""" % (
    page_head_block("gallery", "my <span class='grad-text'>gallery</span>",
                    "A collection of moments, projects and experiences that inspire my journey in tech and creativity."),
    icon("info"),
    icon("close"), icon("chevron-left"), icon("chevron-right"),
    cta_block("Like what you see?", "The projects page has the details behind the work.",
              ("projects.html", "view projects"), ("contact.html", "contact me")),
)


# ============================== CONTACT ====================================
CONTACT = """
    <div class='container'>
%s

      <div class='contact-layout'>
        <!-- left column -->
        <div class='stack reveal'>
          <div class='card card-pad'>
            <div class='contact-card' style='padding:0'>
              <span class='icon-tile'>%s</span>
              <div class='fact-body'>
                <span class='fact-label'>email</span>
                <a class='fact-value' href='mailto:actinsyson24@gmail.com'>actinsyson24@gmail.com</a>
              </div>
            </div>
            <button class='btn btn-outline btn-sm mt-3' type='button' data-copy-email='actinsyson24@gmail.com'>
              %s copy address
            </button>
          </div>

          <div class='card card-pad'>
            <div class='contact-card' style='padding:0'>
              <span class='icon-tile icon-tile--violet'>%s</span>
              <div class='fact-body'>
                <span class='fact-label'>location</span>
                <span class='fact-value'>Rurehe, Mitooma District, Uganda</span>
              </div>
            </div>
            <p class='meta mt-3'>Eastern Africa Time (EAT, UTC+3). I usually reply within a day.</p>
          </div>

          <div class='card card-pad'>
            <div class='contact-card' style='padding:0'>
              <span class='icon-tile'>%s</span>
              <div class='fact-body'>
                <span class='fact-label'>professional name</span>
                <span class='fact-value'>Syson Actin</span>
              </div>
            </div>
            <p class='meta mt-3'>Real name: KARUHANGA SYSON</p>
          </div>

          <div class='card card-pad'>
            <h3 class='card-title'>find me online</h3>
            <ul class='socials mt-3'>
%s
            </ul>
            <p class='meta mt-3'>Only GitHub is connected so far — the rest are placeholders until I add the links.</p>
          </div>
        </div>

        <!-- right column: form -->
        <div class='card form-card reveal'>
          <h2 class='section-title' style='font-size:1.25rem'>send a message</h2>
          <p class='meta mt-2 mb-4'>Fields marked <span class='req'>*</span> are required.</p>

          <form data-contact-form novalidate>
            <div class='form-grid'>
              <div class='field'>
                <label for='cf-name'>your name <span class='req'>*</span></label>
                <input id='cf-name' name='name' type='text' autocomplete='name' placeholder='e.g. Alex Mukasa' required>
                <p class='field-error' id='cf-name-error' role='alert'></p>
              </div>

              <div class='field'>
                <label for='cf-email'>your email <span class='req'>*</span></label>
                <input id='cf-email' name='email' type='email' autocomplete='email' placeholder='you@example.com' required>
                <p class='field-error' id='cf-email-error' role='alert'></p>
              </div>

              <div class='field'>
                <label for='cf-subject'>subject <span class='req'>*</span></label>
                <input id='cf-subject' name='subject' type='text' placeholder='What is this about?' required>
                <p class='field-error' id='cf-subject-error' role='alert'></p>
              </div>

              <div class='field'>
                <label for='cf-message'>message <span class='req'>*</span></label>
                <textarea id='cf-message' name='message' rows='6' placeholder='Tell me a little about what you have in mind…' required></textarea>
                <p class='field-error' id='cf-message-error' role='alert'></p>
              </div>

              <button class='btn btn-primary btn-block' type='submit'>
                %s send message
              </button>

              <p class='form-status' data-form-status role='status' aria-live='polite'></p>

              <p class='meta'>
                This form isn't connected to a mail service yet. It validates your message and then
                opens your email app with everything filled in — so nothing is lost, and nothing is
                pretended.
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>

    <section class='section'>
      <div class='container'>
%s
      </div>
    </section>
""" % (
    page_head_block("contact", "let's <span class='grad-text'>work together</span>",
                    "I'm always open to new opportunities, collaborations, projects and innovative ideas. Feel free to reach out!"),
    icon("mail"), icon("check"), icon("pin"), icon("briefcase"),
    social_list("              "),
    icon("send"),
    cta_block("Prefer to look around first?", "Have a browse — and come back when something catches your eye.",
              ("projects.html", "see projects"), ("about.html", "about me")),
)


# ============================== BLOG =======================================
def post_card(cat, cat_label, title, desc, read, seed, variant):
    return """          <article class='card card--hover post-card reveal' data-category='%s'
                   data-text='%s %s'>
            <div class='post-media'>
              <span class='ribbon'>sample</span>
              %s
            </div>
            <div class='post-body'>
              <span class='post-cat'>%s</span>
              <h3>%s</h3>
              <p>%s</p>
              <div class='post-foot'>
                <span>sample post</span>
                <span class='dotsep'></span>
                <span>%s min read</span>
              </div>
            </div>
          </article>""" % (
        cat, title.lower(), desc.lower(), art_inline(seed, 640, 360, variant),
        cat_label, title, desc, read,
    )


BLOG = """
    <div class='container'>
%s

      <div class='blog-layout'>
        <div>
          <div class='section-head' style='align-items:center'>
            <div class='filter-bar' data-blog-filters style='margin:0'>
              <button class='pill is-active' type='button' data-category='all' aria-pressed='true'>all</button>
              <button class='pill' type='button' data-category='javascript' aria-pressed='false'>javascript</button>
              <button class='pill' type='button' data-category='web' aria-pressed='false'>web development</button>
              <button class='pill' type='button' data-category='future' aria-pressed='false'>tech &amp; future</button>
            </div>
            <div class='search'>
              %s
              <label class='sr-only' for='blog-search'>Search articles</label>
              <input id='blog-search' type='search' data-blog-search placeholder='search articles…' autocomplete='off'>
            </div>
          </div>

          <div class='blog-grid' data-blog-grid>
%s
          </div>

          <div class='notice mt-4'>
            %s
            <div>
              <strong>These are sample articles.</strong> They exist to show the layout — none of
              them have been published. Replace them with your own writing as you go, or delete the
              section until you have something to say.
            </div>
          </div>
        </div>

        <!-- sidebar -->
        <aside class='sidebar'>
          <div class='card sidebar-card'>
            <h3>categories</h3>
            <ul class='cat-list'>
              <li><button type='button' class='is-active' data-side-category='all'>all articles <span class='count'>4</span></button></li>
              <li><button type='button' data-side-category='web'>web development <span class='count'>2</span></button></li>
              <li><button type='button' data-side-category='javascript'>javascript <span class='count'>1</span></button></li>
              <li><button type='button' data-side-category='future'>tech &amp; future <span class='count'>1</span></button></li>
            </ul>
          </div>

          <div class='card sidebar-card'>
            <h3>recent posts</h3>
            <ul class='recent-list'>
              <li class='recent-item'>
                <span class='recent-thumb'>%s</span>
                <div>
                  <h4>Why I chose web development</h4>
                  <p class='meta'>sample · 5 min read</p>
                </div>
              </li>
              <li class='recent-item'>
                <span class='recent-thumb'>%s</span>
                <div>
                  <h4>JavaScript tips for beginners</h4>
                  <p class='meta'>sample · 4 min read</p>
                </div>
              </li>
              <li class='recent-item'>
                <span class='recent-thumb'>%s</span>
                <div>
                  <h4>The future of web development</h4>
                  <p class='meta'>sample · 6 min read</p>
                </div>
              </li>
            </ul>
          </div>

          <div class='card sidebar-card'>
            <h3>writing soon</h3>
            <p class='meta'>Notes on learning JavaScript, building The Ark AI, and the mistakes I make along the way.</p>
            <a class='btn btn-outline btn-sm mt-3' href='contact.html'>suggest a topic</a>
          </div>
        </aside>
      </div>
    </div>

    <section class='section'>
      <div class='container'>
%s
      </div>
    </section>
""" % (
    page_head_block("blog", "insights &amp; <span class='grad-text'>articles</span>",
                    "Thoughts, tips and updates from my journey in web development and technology."),
    icon("search"),
    "\n".join([
        post_card("web", "web development", "Why I chose web development",
                  "Discover what inspired me to start coding and how it's shaping my future.", 5, "why-web", 0),
        post_card("javascript", "javascript", "JavaScript tips for beginners",
                  "Simple tips to help you write cleaner, better and more efficient JavaScript code.", 4, "js-tips", 1),
        post_card("future", "tech & future", "The future of web development",
                  "Exploring how AI and new technologies are changing the web.", 6, "future-web", 2),
        post_card("web", "web development", "Starting small: my first responsive layout",
                  "What I learned rebuilding a page until it finally worked on a phone.", 3, "first-layout", 0),
    ]),
    icon("info"),
    art_inline("recent-1", 120, 120, 1),
    art_inline("recent-2", 120, 120, 2),
    art_inline("recent-3", 120, 120, 0),
    cta_block("Want to talk about any of this?", "I'm happy to discuss ideas, take feedback, or just compare notes.",
              ("contact.html", "get in touch"), ("about.html", "about me")),
)


# ============================== 404 ========================================
NOT_FOUND = """
    <div class='container'>
      <div class='error-page'>
        <div class='error-art' aria-hidden='true'>
          <svg viewBox='0 0 240 200' fill='none'>
            <defs>
              <linearGradient id='e404' x1='0' y1='0' x2='1' y2='1'>
                <stop offset='0' stop-color='#60A5FA'/><stop offset='1' stop-color='#A78BFA'/>
              </linearGradient>
            </defs>
            <circle cx='120' cy='100' r='58' stroke='url(#e404)' stroke-width='1.6' opacity='.55'/>
            <ellipse cx='120' cy='100' rx='92' ry='30' stroke='url(#e404)' stroke-width='1.2' opacity='.4' transform='rotate(-18 120 100)'/>
            <path d='M120 42v116M62 100h116' stroke='#1E293B' stroke-width='1'/>
            <g transform='translate(96 62)'>
              <rect x='0' y='0' width='48' height='48' rx='14' fill='#0E1727' stroke='url(#e404)' stroke-width='1.6'/>
              <path d='M16 24h16M24 16v16' stroke='url(#e404)' stroke-width='2' stroke-linecap='round'/>
            </g>
            <circle cx='52' cy='54' r='4' fill='url(#e404)' opacity='.9'/>
            <circle cx='192' cy='142' r='3' fill='url(#e404)' opacity='.7'/>
            <circle cx='176' cy='46' r='2.4' fill='#93C5FD' opacity='.8'/>
            <circle cx='40' cy='150' r='2.2' fill='#A78BFA' opacity='.8'/>
          </svg>
        </div>

        <p class='error-code'>404</p>
        <h1>This page drifted off course.</h1>
        <p>The page you're looking for doesn't exist, or it has been moved. Nothing is broken — you just took a wrong turn.</p>

        <div class='error-actions'>
          <a class='btn btn-primary' href='index.html'>%s back to home</a>
          <a class='btn btn-outline' href='projects.html'>browse projects</a>
          <a class='btn btn-outline' href='contact.html'>contact me</a>
        </div>
      </div>
    </div>
""" % icon("arrow-left")


# ---------------------------------------------------------------------------
# PAGE REGISTRY
# ---------------------------------------------------------------------------
PAGES = [
    # file, nav key, title, description, content, extra scripts
    ("index.html", "index.html",
     "Syson Actin — Creative Web Developer | Karuhanga Syson",
     "Karuhanga Syson, professionally known as Syson Actin, is a creative web developer and A-Level student from Rurehe, Mitooma District, Uganda, building responsive websites with HTML, CSS and JavaScript.",
     HOME, []),
    ("about.html", "about.html",
     "About — Syson Actin | Karuhanga Syson",
     "Get to know Karuhanga Syson (Syson Actin): a creative web developer and A-Level student from Rurehe, Mitooma District, Uganda.",
     ABOUT, []),
    ("skills.html", "skills.html",
     "Skills — Syson Actin | HTML, CSS & JavaScript",
     "The technologies Syson Actin currently works with: HTML, CSS and JavaScript — with honest space for what comes next.",
     SKILLS, []),
    ("projects.html", "projects.html",
     "Projects — Syson Actin",
     "Projects by Syson Actin, including The Ark AI — an AI-powered assistant for students and teachers.",
     PROJECTS, ["js/projects.js"]),
    ("gallery.html", "gallery.html",
     "Gallery — Syson Actin",
     "A visual collection of work, design concepts and moments from Syson Actin's development journey.",
     GALLERY, ["js/gallery.js"]),
    ("contact.html", "contact.html",
     "Contact — Syson Actin",
     "Get in touch with Karuhanga Syson (Syson Actin) — email, location and a contact form.",
     CONTACT, ["js/contact.js"]),
    ("blog.html", "blog.html",
     "Insights & Articles — Syson Actin",
     "Thoughts, tips and updates from Syson Actin's journey in web development and technology.",
     BLOG, ["js/blog.js"]),
    ("404.html", "", 
     "Page not found — Syson Actin",
     "That page doesn't exist. Head back to the homepage of Syson Actin's portfolio.",
     NOT_FOUND, []),
]

BODY = """${sprite}
  <a class='skip-link' href='#main'>Skip to main content</a>

  <div class='bg-layers' aria-hidden='true'><canvas id='stars'></canvas></div>

${header}

  <main id='main'>
    <div class='page'>
${content}
    </div>
  </main>

${footer}

  <script src='js/main.js'></script>
  <script src='js/theme.js'></script>
  <script src='js/navigation.js'></script>
  <script src='js/animations.js'></script>
${extra_js}
</body>
</html>
"""


def build_page(filename, nav_key, title, description, content, extra):
    canonical = "%s/%s" % (SITE_URL, "" if filename == "index.html" else filename)
    head = tpl(
        HEAD,
        title=title,
        description=description,
        canonical=canonical,
        og_title=title,
        site_url=SITE_URL,
    )

    body = tpl(
        BODY,
        sprite=sprite(),
        header=header(nav_key),
        content=content.rstrip(),
        footer=footer(),
        extra_js="\n".join("  <script src='%s'></script>" % s for s in extra),
    )

    out = ROOT / filename
    out.write_text(head + "<body>\n" + body, encoding="utf-8")
    return out


def main():
    written = []
    for filename, nav_key, title, description, content, extra in PAGES:
        written.append(build_page(filename, nav_key, title, description, content, extra))
    for path in written:
        size = path.stat().st_size / 1024
        print("  %-24s %6.1f KB" % (path.name, size))
    print("\n%d pages written to %s" % (len(written), ROOT))


if __name__ == "__main__":
    main()
