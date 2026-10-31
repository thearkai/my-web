#!/usr/bin/env python3
"""
tools/build_preview.py — builds preview/*.html

Each page is rewritten as a single self-contained file: the stylesheets and
scripts are inlined and every local image reference (in markup *and* inside the
JavaScript data arrays) becomes a data URI. This exists so the site can be shown
in sandboxed viewers that block external requests.

    python3 tools/build_preview.py

Deploy the root .html files — never this folder.
"""

import base64
import mimetypes
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "preview"
PAGES = ["index", "about", "skills", "projects", "gallery",
         "contact", "blog", "404"]

CSS_FILES = ["css/style.css", "css/theme.css", "css/animations.css", "css/responsive.css"]
JS_CORE = ["js/main.js", "js/theme.js", "js/navigation.js", "js/animations.js"]

# Attributes may be written with ' or "
Q = r"""["']"""


def data_uri(path: pathlib.Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode())


def inline_local_paths(text: str) -> str:
    """Replace any 'assets/images/...' path with a data URI (used for JS + HTML)."""
    def repl(match):
        raw = match.group(0)
        path = ROOT / raw
        if path.exists() and path.is_file():
            return data_uri(path)
        return raw

    return re.sub(r"assets/images/[A-Za-z0-9_./-]+\.(?:png|jpe?g|webp|gif|svg)", repl, text)


def build(name: str) -> None:
    html = (ROOT / (name + ".html")).read_text(encoding="utf-8")

    # Page-specific scripts must be collected before the tags are stripped.
    extras = re.findall(r"<script\s+src=" + Q + r"(js/[^\"']+)" + Q, html)

    # ---- 1. stylesheets --------------------------------------------------
    css = "\n".join((ROOT / f).read_text(encoding="utf-8") for f in CSS_FILES)
    html = re.sub(r"\s*<link\s+rel=" + Q + r"stylesheet" + Q +
                  r"\s+href=" + Q + r"css/[^\"']+" + Q + r"\s*/?>", "", html)
    html = html.replace("</head>", "  <style>\n" + css + "\n  </style>\n</head>")

    # ---- 2. scripts ------------------------------------------------------
    bundle = "\n".join((ROOT / f).read_text(encoding="utf-8") for f in JS_CORE)
    for extra in extras:
        if extra not in JS_CORE:
            bundle += "\n" + (ROOT / extra).read_text(encoding="utf-8")

    html = re.sub(r"\s*<script\s+src=" + Q + r"js/[^\"']+" + Q + r"\s*>\s*</script>", "", html)
    # image paths referenced from the JS data arrays
    bundle = inline_local_paths(bundle)
    html = html.replace("</body>", "  <script>\n" + bundle + "\n  </script>\n</body>")

    # ---- 3. images in the markup ----------------------------------------
    html = inline_local_paths(html)

    # ---- 4. references that can't resolve inside a single file ----------
    # Social-preview images are pointless in a file:// preview and are the
    # single biggest thing in the document, so drop them. srcset is dropped too:
    # it would inline the same logo a second time for no visual gain.
    for pattern in (
        r"\s*<link\s+rel=" + Q + r"icon" + Q + r"[^>]*>",
        r"\s*<link\s+rel=" + Q + r"apple-touch-icon" + Q + r"[^>]*>",
        r"\s*<link\s+rel=" + Q + r"manifest" + Q + r"[^>]*>",
        r"\s*<meta\s+(?:property|name)=" + Q + r"(?:og:image|og:image:alt|og:image:width|og:image:height|twitter:image)" + Q + r"[^>]*>",
        r"\s*srcset=" + Q + r"[^\"']*" + Q,
    ):
        html = re.sub(pattern, "", html)

    (OUT / (name + ".html")).write_text(html, encoding="utf-8")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name in PAGES:
        build(name)
        size = (OUT / (name + ".html")).stat().st_size / 1024
        print("  preview/%-20s %7.1f KB" % (name + ".html", size))
    print("\npreview built — deploy the root files, not this folder")


if __name__ == "__main__":
    main()
