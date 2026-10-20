---
name: evomni-html
description: Build or revise a static HTML website that will be imported into an Evomni CMS site. Use whenever a designer asks to design, generate, modify or fix a website, landing page, product or article pages "for Evomni" / "符合 Evomni", to redraw an existing site from its site context pack, or to make an Evomni site package pass the import checker.
metadata:
  version: 1.1.0
---

# Evomni HTML

If you received this as a zip instead of an installed skill (e.g. in ChatGPT): unzip it and follow this file; paths below are relative to the unzipped `evomni-html/` folder.

Skill version: 1.1.0. The `VERSION` file is authoritative (this line and `metadata.version` above are copies). Quote it when you report a problem with these instructions.

You produce a folder of static HTML/CSS/JS that an importer turns into an Evomni CMS site. The visual design is completely free. The CMS functions and data fields are fixed: only use what `references/spec.md` allows, and mark data with `data-evo-*` attributes so the importer knows where each piece goes.

## Workflow

1. Read `references/spec.md` completely before writing any HTML.
2. Plan the site map first and show it to the user: for every page, its page type (home / page / article-list / article-detail / product-list / product-detail), its collection, and its category. A `page` with a `[data-evo-body]` is a text page (privacy, terms: one shared frame, only the text differs); a `page` without one is a custom standalone page. Put every article and every product on its own detail page.
3. If the brief needs something the spec does not support, say so and propose the closest supported alternative. Never invent new `data-evo-*` attributes and never fake a feature with JavaScript data.
4. Write the shared header and footer once; copy them byte-identical into every page.
5. For each collection, design ONE detail layout and ONE list-card layout, then fill them with each record's data. Only `[data-evo-field]` values and `[data-evo-body]` content may differ between pages of a collection.
6. Run `node scripts/check-site.mjs <site-folder>` (Node.js 18+, no install needed). Fix every ERROR and re-run until it reports 0 errors. Review each WARNING. When redrawing an existing site, add `--context <site-context.md>` (see references/redraw.md).
7. Zip the site folder (root of the zip = the folder containing `index.html`; no `zip` command: `python3 -m zipfile -c ../site.zip .` inside the folder) and hand it over together with the checker's final output. Limits: 200 MB unpacked, 2000 files. A passing check writes `evomni-check.json` into the site root (it records which skill version checked the site): the zip must include it; never edit or write that file by hand.

## Revising an imported site

When the designer asks for changes to a site that was already imported (or delivered to you before), revise in place:

- Edit the existing folder. Never regenerate the whole site.
- Never rename files, change collection keys or category names. The file name is the slug and the identity of the page.
- Touch only the pages that need it. Shared CSS/JS affects every page: say so before changing it.
- Do not reorder or reformat unrelated files. The importer lists every unit that changed, so "changed A, also touched B" shows up there.
- Deliver with a short "what changed in this round" note.
- Re-skin mode (site already has data in the admin): record content (article/product fields and body), menus, forms and SEO are NOT updated from the package; the admin is the source of truth. Record pages in the package only supply the layout.

## Redrawing an existing site

When the site already exists with its data (an old webtech2 site converted into Evomni, or any site whose admin already holds the content) and you are given its site context pack: follow `references/redraw.md`. You make a re-skin package whose file names claim the site's collections, pages and forms; capture the old pages first with `node scripts/snapshot.mjs` (screenshots need Playwright installed in this skill folder: the script prints the two commands when it is missing).

## When you cannot run the checker

If Node.js is not available: go through `references/checklist.md` item by item and fix what fails, then tell the designer to upload the zip to the 整站匯入 page of the Evomni admin (pre-check step) and paste the report back to you. That report is produced by the same checker. Without a local check there is no `evomni-check.json`; do not create one.

## Reference files

- `references/spec.md`: the full rules (read first).
- `references/checklist.md`: the same rules as a flat checklist.
- `example-site/`: a small complete site that passes the checker (home, about, contact form, news list + 3 articles, product list + 3 products). Copy its marker patterns, not its look.
- `scripts/check-site.mjs`: the checker (generated single file; same code as the admin import page).
- `references/redraw.md`: redrawing an existing site from its site context pack (full / hybrid).
- `references/legacy-body.css`: makes old body content readable inside a new frame.
- `scripts/snapshot.mjs`: captures old pages (HTML, CSS, images, screenshots) for redrawing.
