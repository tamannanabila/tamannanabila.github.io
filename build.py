#!/usr/bin/env python3
"""
build.py — regenerates the Research Projects section of index.html from content.json.

Usage:
    python build.py

How to add or edit a project:
    1. Open content.json and edit the "projects" list. Each project supports:
         title        (required)  e.g. "IWIQ — Greywater Recycling & Heat Recovery"
         description  (required)  a few sentences
         tools        (optional)  list of short labels shown as chips
         logo         (optional)  a path, or list of paths, to logo image(s)
         images       (optional)  list of picture paths, e.g. ["assets/img/site1.jpg"]
         link         (optional)  a URL, or list of URLs, for a "More →" link
    2. Put logo/image files in the assets/ folder (any subfolders you like).
    3. Run: python build.py
    4. Refresh index.html in your browser. Commit & push to publish.

Only the block between the PROJECTS:START / PROJECTS:END markers in index.html
is touched — everything else on the page stays exactly as you wrote it.

Gallery images are rendered with an onclick handler that opens the site-wide
lightbox (openLightbox(this.src, this.alt)) — the lightbox HTML/CSS/JS must
already be present in index.html near the closing </body> tag.

Requires only the Python standard library.
"""

import json
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
INDEX = HERE / "index.html"
CONTENT = HERE / "content.json"

START = "<!-- PROJECTS:START"
END = "<!-- PROJECTS:END -->"


def _as_list(value) -> list:
    """Accept a string, a list, or nothing — always return a clean list of strings."""
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    return [str(v).strip() for v in value if str(v).strip()]


def render_project(p: dict) -> str:
    title = escape(p["title"])
    desc = escape(p["description"])
    logos = _as_list(p.get("logo"))
    images = _as_list(p.get("images"))
    tools = _as_list(p.get("tools"))
    links = _as_list(p.get("link"))

    parts = ['      <div class="project">']

    # Header: title + optional logo(s)
    if logos:
        parts.append('        <div class="head">')
        parts.append(f"          <h3>{title}</h3>")
        parts.append('          <div class="logos">')
        for lg in logos:
            parts.append(
                f'            <img class="logo" src="{escape(lg, quote=True)}" alt="{title} logo">'
            )
        parts.append("          </div>")
        parts.append("        </div>")
    else:
        parts.append(f'        <div class="head"><h3>{title}</h3></div>')

    parts.append(f"        <p>{desc}</p>")

    # Optional picture gallery — clickable to open the lightbox
    if images:
        parts.append('        <div class="gallery">')
        for img in images:
            src = escape(img, quote=True)
            parts.append(
                f'          <img src="{src}" alt="{title} — project picture" loading="lazy" '
                f'onclick="openLightbox(this.src, this.alt)" style="cursor:zoom-in">'
            )
        parts.append("        </div>")

    # Optional tool chips
    if tools:
        chips = "".join(f'<span class="chip">{escape(t)}</span>' for t in tools)
        parts.append(f'        <div class="tools">{chips}</div>')

    # Optional external link(s)
    for url in links:
        parts.append(
            f'        <a class="more" href="{escape(url, quote=True)}">More &rarr;</a> '
        )

    parts.append("      </div>")
    return "\n".join(parts)


def main() -> None:
    if not INDEX.exists():
        sys.exit("index.html not found — run this script from the portfolio folder.")
    try:
        data = json.loads(CONTENT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"content.json has a syntax error: {e}\n"
                 "Tip: check for a missing comma or quote near that line.")

    projects = data.get("projects", [])
    if not projects:
        sys.exit("content.json contains no projects — nothing to build.")

    html = INDEX.read_text(encoding="utf-8")
    try:
        pre, rest = html.split(START, 1)
        marker_line, rest = rest.split("-->", 1)
        _, post = rest.split(END, 1)
    except ValueError:
        sys.exit("Could not find the PROJECTS:START / PROJECTS:END markers in index.html.")

    body = "\n\n".join(render_project(p) for p in projects)
    new = (
        pre
        + START + marker_line + "-->\n"
        + body + "\n"
        + END
        + post
    )
    INDEX.write_text(new, encoding="utf-8")

    # Warn about missing image files so broken links are caught before publishing
    for p in projects:
        for path in _as_list(p.get("logo")) + _as_list(p.get("images")):
            if not (HERE / path).exists():
                print(f"  ! file not found: {path}  (referenced by '{p['title']}')")

    print(f"OK - rebuilt index.html with {len(projects)} projects.")


if __name__ == "__main__":
    main()