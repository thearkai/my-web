# syson actin. — portfolio

A premium, futuristic dark portfolio for **Syson Actin** (Karuhanga Syson), built with plain
HTML, CSS and JavaScript. Eight pages, no frameworks, no build step required to run it.

---

## Quick start

Open `index.html` in a browser — that's it. For a local server (so relative paths behave exactly
like production):

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Deploy free on GitHub Pages

1. Create a repository, e.g. `syson-portfolio`.
2. Push everything in this folder to the `main` branch.
3. Repo → **Settings → Pages → Source: Deploy from a branch → `main` / root**.
4. Your site is live at `https://thearkai.github.io/syson-portfolio/`.
5. Custom domain later: add a `CNAME` file containing your domain and point a CNAME DNS record at
   `thearkai.github.io`.

Then update the URL in two places so metadata stays correct:

- `tools/build.py` → `SITE_URL`
- `sitemap.xml` and `robots.txt`

---

## File structure

```
/
├── index.html              home
├── about.html              get to know me
├── skills.html             what i work with
├── projects.html           project grid (JS-driven)
├── gallery.html            gallery + lightbox (JS-driven)
├── contact.html            contact info + form
├── blog.html               insights & articles
├── 404.html                custom error page
│
├── css/
│   ├── style.css           tokens, base styles, every shared component
│   ├── theme.css           light theme (dark is the default)
│   ├── responsive.css      breakpoints: 560 / 760 / 1000 / 1240 px
│   └── animations.css      keyframes, scroll reveals, reduced-motion overrides
│
├── js/
│   ├── main.js             CONFIG: social links, toast, year, placeholder art
│   ├── theme.js            dark/light toggle + localStorage
│   ├── navigation.js       mobile drawer, sticky header, active page
│   ├── animations.js       star canvas, reveals, terminal typing, back-to-top
│   ├── projects.js         project data + filters + search
│   ├── gallery.js          gallery data + filters + lightbox
│   ├── blog.js             article filters + search
│   └── contact.js          form validation + submission
│
├── assets/
│   └── images/
│       ├── brand/          crest, og-image, app icon
│       ├── gallery/        ← put gallery photographs here
│       ├── profile/        ← put your photograph here
│       └── projects/       ← put project screenshots here
│
├── tools/
│   ├── build.py            rebuilds the eight HTML pages from shared partials
│   └── build_preview.py    builds the single-file copies in preview/
│
├── preview/                self-contained copies (for in-app viewing only — never deploy)
├── site.webmanifest · robots.txt · sitemap.xml · favicon-16.png · favicon-32.png
```

### Why `tools/build.py` exists

Every page needs the same header, footer and ~50-icon SVG sprite. Rather than paste that into nine
files by hand (and let them drift apart), `tools/build.py` holds them once and writes the HTML:

```bash
python3 tools/build.py
```

The generated `.html` files are normal, hand-editable static files — you can ignore the builder
entirely and edit them directly. Just don't run the builder afterwards, or it will overwrite your
edits (it rebuilds from the Python templates).

---

## What to edit, and where

| I want to change… | Edit |
|---|---|
| Social links (currently only GitHub is connected) | `SOCIALS` object at the top of `js/main.js` |
| Projects, descriptions, live/repo links | `PROJECTS` array in `js/projects.js` |
| Gallery images and captions | `GALLERY` array in `js/gallery.js` (empty — add objects there) |
| Your real photograph | save it as `assets/images/profile/profile.jpg`, then replace the `.portrait-placeholder` block in `about.html` (the exact snippet is in an HTML comment there) |
| The contact form's delivery | `FORM_ENDPOINT` at the top of `js/contact.js` — paste a Formspree/Getform/Basin endpoint |
| Text, headings, sections | the page's `.html` file, or the matching string in `tools/build.py` |
| Adding a CV back | put a PDF in `assets/documents/` and add a link like `<a class='btn btn-outline' href='assets/documents/your-cv.pdf' download>download cv</a>` in `about.html` |
| Colours, radii, spacing | `:root` tokens at the top of `css/style.css` |
| Light-theme colours | `css/theme.css` |
| Breakpoints | `css/responsive.css` |
| SEO title/description per page | `PAGES` list at the bottom of `tools/build.py` |

---

## Honest placeholders (read this)

The brief was explicit: never invent qualifications, repositories or achievements. So:

- **Gallery** — one real photograph (the portrait), plus the empty-state handling for when there
  are none. Category filters only appear once there are at least two categories to choose from.
- **Projects** — The Ark AI is real. The other two cards are labelled placeholders. Where a demo or
  repository URL hasn't been supplied, the button renders **disabled** rather than linking nowhere.
- **Blog** — four sample articles, badged `sample`. None claim to be published.
- **Socials** — only GitHub is connected. The rest show with a dashed border and, when clicked, a
  short message explaining the link isn't added yet. No dead links anywhere.

---

## How the contact form behaves

There is **no backend**. On submit the form sends to **actinsyson24@gmail.com** — it:

1. validates every field (required checks, email format, minimum lengths),
2. shows inline errors, sets `aria-invalid`, and moves focus to the first problem,
3. then opens the visitor's email app with the message pre-filled and addressed to
   `actinsyson24@gmail.com`,
4. and says so plainly — it never claims a message was "sent".

To receive messages properly, create a free form endpoint and set `FORM_ENDPOINT` in
`js/contact.js`. The `fetch()` delivery path is already written and activates automatically, along
with real success/error states.

---

## Accessibility & performance notes

- One `h1` per page, landmark elements, skip link, visible focus rings, labelled fields,
  `aria-live` status messages, `aria-expanded` on the menu button, `aria-current` on the active page.
- The mobile drawer and both lightboxes are keyboard operable: Escape closes, arrows navigate,
  focus returns to where it came from, and background scroll is locked.
- `prefers-reduced-motion` disables the starfield, the terminal typing, reveals and hover motion.
- All icons are an **inline SVG sprite** instead of Font Awesome. Same icons, zero network
  requests, no icon flash, and they inherit text colour — this replaces the Font Awesome CDN
  deliberately. If you specifically want Font Awesome, add its `<link>` to `HEAD` in
  `tools/build.py` and swap the `<svg class="icon"><use …></svg>` markup back to `<i class="fa …">`.
- The starfield is a capped canvas (≤120 particles, 30fps, paused when the tab is hidden).
- No images are loaded above the fold except a small crest, so first paint is fast; everything else
  uses `loading="lazy"`.
- Google Fonts is the only external request. The font stack falls back to system fonts instantly
  if it fails, so the site still looks right offline.

### A note on `preview/`

`preview/` contains single-file copies of each page with CSS, JS and images inlined. They exist so
the site can be shown inside sandboxed viewers that block external requests. **Deploy the root
files, not `preview/`.**

---

## Browser support

Current Chrome, Edge, Firefox and Safari. Uses `IntersectionObserver`, CSS custom properties,
`clamp()`, `inert` and `backdrop-filter` — all widely supported. Pages degrade gracefully without
JavaScript: content, links and navigation all remain usable, and reveal animations are skipped.

---

© 2026 Syson Actin. All rights reserved.
