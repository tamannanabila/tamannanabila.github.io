# Tamanna Nabila Islam - Academic Portfolio

Static portfolio site with a small Python build workflow for the Research Projects section.

## Files

| File           | What it is                                                        |
|----------------|-------------------------------------------------------------------|
| `index.html`   | The website (everything except projects is edited directly here)  |
| `content.json` | Your research projects — **edit this** to add logos/pictures/info |
| `build.py`     | Regenerates the projects section of index.html from content.json  |
| `assets/`      | Put your logo and picture files here                              |

## Add a logo, pictures, or details to a project

1. Copy the image files into `assets/logos/` or `assets/img/`.
2. Open `content.json` and fill in the fields, e.g.:

```json
{
  "title": "IWIQ — Greywater Recycling & Heat Recovery",
  "logo": "assets/logos/iwiq.png",
  "description": "Your updated description...",
  "tools": ["Python", "Revit / IFC"],
  "images": ["assets/img/bim-model.png", "assets/img/network.png"],
  "link": "https://project-website.example"
}
```

3. Run:

```bash
python build.py
```

4. Refresh the page in your browser. Done. (The script warns you if a
   referenced image file is missing.)

To add a brand-new project, copy one of the `{ ... }` blocks in the list,
edit it, and re-run `python build.py`. All fields except `title` and
`description` are optional — leave `""` or `[]` to hide them.

## Preview locally

```bash
python -m http.server 8000    # then open http://localhost:8000
```

## Deploy free on GitHub Pages

1. Create a public repo named `<your-username>.github.io`.
2. Push this whole folder (including `assets/`).
3. Site goes live at `https://<your-username>.github.io` within minutes.
4. After every edit: `python build.py`, then commit & push.

## Notes

- Home address and phone number are deliberately not on the site.
- Everything outside the `<!-- PROJECTS:START -->` / `<!-- PROJECTS:END -->`
  markers in index.html is yours to edit by hand; the script never touches it.
