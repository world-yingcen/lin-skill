# Redrawing an existing site

Use this when the site already exists in Evomni with its data (typically an old webtech2 site whose data was converted) and you are asked to give it a new skin. You produce a **re-skin package**: the importer claims the site's existing collections, pages and forms by file name and replaces only the design. Records, menus, forms and SEO stay as they are on the site.

## Inputs

1. **Site context pack** (`site-context-<domain>-<date>.zip`, from the "下載重畫附件（給 AI）" button on the admin's 整站匯入 page): `site-context.md` lists the site type (brochure / e-commerce), the collections, categories, menu tree, single pages and forms (with their fields) with their **suggested file names** and frontend URLs, 3 sample records per collection (with their body HTML) and the classes / inline styles the old bodies use; `images/` holds the logo and the sample covers only; `snapshot-urls.txt` lists the frontend URLs for the snapshot script.
2. **Snapshot of the site** (the pages to look at), made with `scripts/snapshot.mjs --list <pack>/snapshot-urls.txt` (add one detail page URL per collection): raw HTML, an offline copy with local CSS/images, and screenshots (first screen and full page). Take: home, one list and one detail page per collection, every custom page, every text page you will excerpt. Every other image you need (home slides, galleries, banners) comes from the snapshot's `assets/`, not from the pack; slides are often background images, so search both the snapshot CSS and the page HTML (inline `style="…url(…)"`) for `url(`. The pack's URLs are the new Evomni site's; if you cannot open them (an internal test host), snapshot the old site from the URL the site owner gives instead. If the old site (before it moved to Evomni) is still online and the brief wants its look, snapshot it too; its URLs are not in the pack, ask the site owner. Old URLs, ids and page splits rarely match the pack one to one: see "When the old site does not match" below. A converted site may split one old page into several (e.g. one old "Interior Design" page with four articles became four single pages): follow the menu tree of site-context.md.
3. **The brief**: which mode (below), and what may change (same look, refreshed look, new home only…).

Read `site-context.md` first, then the screenshots. Open the old CSS only to pick colours, fonts and spacing (search it; do not read it whole). Screenshots need Playwright: if `snapshot.mjs` stops with "STOPPED: screenshots need Playwright", run the two install commands it prints (they install into the skill folder), then run it again. Do not redraw from HTML alone; if you cannot run commands at all, ask the designer for screenshots of every page listed above.

## Two modes

- **Full redraw**: home, header/footer, every collection's list and detail layout, the text-page frame and the custom pages are all drawn to match the old site (or the brief's refresh of it).
- **Hybrid redraw**: only home and header/footer are drawn. The inner layouts are copied from `example-site/` (products.html + product-*.html, news.html + news-*.html, privacy.html as the text-page frame; renamed to the file names and keys of site-context.md, filled with its samples) and fitted to the brand through `example-site/assets/css/site.css`:
  - change the variables at its top (`--brand*`, `--ink*`, `--line`, `--bg*`, `--radius`) to the old site's colours, and the `font-family` of `body` (line ~20) to its fonts;
  - delete the block between `/* ===== header + footer` and `/* ===== end header + footer ===== */` (it holds every header/footer rule, the responsive ones too): your own header/footer CSS replaces it;
  - the inner pages stay light (the example hard-codes white surfaces). For a dark brand, use the dark colour in header, footer and home, and the brand colour as the accent inside. If the designer wants dark inner pages, tell them that is a full redraw of the inner layouts (more work, and every inner layout must then be checked against the old bodies); do not darken the copied layouts piecemeal.
  Do not restyle the inner layouts beyond that; removing blocks the site cannot use (prices and buy buttons, below) is fine.

## What goes in the package

| Site part (from site-context.md) | File(s) | Notes |
|---|---|---|
| Home | `index.html` | New design. Copy the old home's texts and images from the snapshot. "Latest N" blocks (spec 5.3) use the collection key. A site name with a test marker (`[95 - 測試]…`) is not the real name: site-context.md says so; never copy the marker. |
| Header / footer | in every page | Draw the main menu from the menu tree (titles and levels as listed; skip items marked （關閉）: closed, not shown on the site). A group without its own page links to its first child (a group with a single child may be drawn as that one link). Links are placeholders: the site keeps its own menu. |
| Each collection | ONE list page + one category list page per category + 2–3 detail pages | Use the file names and the `data-evo-collection` key site-context.md gives for the collection. When the suggested name is reserved (e.g. `product`), only the file names change (`products.html`, `products-{word}.html`); `data-evo-collection` keeps the suggested key (`product`), which is what the import matches first, and the list page `<title>` is the collection title site-context.md shows (e.g. `Product`; never the site name). The list page is the whole collection (no `data-evo-category` on its `<body>`); its layout is what the site shows on every category. Then make one category list page per category site-context.md lists, with the file name it gives (e.g. `products-tables.html`): a copy of the list page with the layout unchanged, `data-evo-category="<exact category title>"` on `<body>` and the category title as `<title>` (every `<title>` is the page name only, spec 1: the system appends the site name). They are what category links point to (below). Make the detail pages from the sample records (`{file-name}-{word}.html`; if two samples share a title, add their reference code to `<title>` to avoid the duplicate-title warning); on a re-skin they are layout examples only, no record is created. Give the sample detail pages `data-evo-category` listing every category with `|` (site-context.md prints the exact value): the CATEGORY rule needs each category list page's category on some detail page. |
| Single pages whose content is text and images (most converted pages) | one **text page** per site page: `{suggested-name}.html` | All share one frame (spec 5.6). The body is NOT imported on a re-skin: put a short excerpt of the old content there, only to show the design. **Copy the excerpt word for word from the snapshot of that page; never write or paraphrase it** (the site owner reads it as the real content, and the checker cannot tell made-up text). Every page you want in the new frame must have its file; a page with no file keeps no layout. |
| Pages the brief redesigns as a whole | `{suggested-name}.html` as a custom page (no `data-evo-body`) | The whole page becomes the design and the old body no longer shows; copy its texts from the snapshot. Use only when asked. |
| A page with an empty body in site-context.md | custom page | Usually a placeholder the converter left (e.g. a curated product list). Rebuild it from the snapshot; a product list can be a "Latest N" block. "Latest N" shows at most 50 records and has no pagination: when the old page paginated, show its first page's count and add a link to the collection's list page for the rest. "Latest N" follows the admin order, not "newest first": say so in the delivery note. |
| Forms | the page that holds the form, `{suggested-name}.html` (a custom page, not a text page) | The form's title must equal the site form's title. Draw the fields site-context.md lists for the form (same labels, types and order); they are only the style template, the live form keeps the site's fields. On a converted site the form is its own menu page: the importer claims this file onto it, publishes the page design there (the form sits where your form is) and points links to this file at it. |

**Products without prices; site type.** site-context.md gives the site type and, per product collection, how many sampled products have a price. A brochure site (形象站) has no online shop: do not draw cart / buy / favorite / notify buttons, stock or payment/shipping lists (the importer removes them anyway); an inquiry button (`data-evo-action="inquiry"`) only if the old site has inquiry. When no product has a price, drop the price, quantity and buy area, the spec table and the stock from the detail layout and the price from the cards, on any site type. Some with and some without: keep the price field (an empty price is hidden). With an inquiry button but no price, keep `data-evo-buy` holding only that button and drop its box look (the example's `pd-buy pd-buy--inquiry`). After removing a price row or buy area, look at the screenshot again: spacing that came from the removed element must move to what remains (the example cards keep their bottom space on the card itself).

**Category links.** Point the category items of the menu and every category navigation (a sidebar on the list page, home tiles) at that category's list page, never all at the collection list page: the checker warns CATEGORY-LINKS when 3 or more links with different texts on one level all go to the same collection list page. The import rewrites links to a category list page into that category's address on the site (matched by the exact category title; an unmatched name falls back to the whole collection and the import preview warns). Links to the collection list page itself open the collection's first category on a converted site.

**Other languages.** When site-context.md lists another language's menu (`### en 的選單`) and the brief asks for it, add that language as a folder (spec 1A): `en/index.html` with the header/footer/menu in that language's titles (the table gives each node's main-language counterpart), and the pages you redraw under the same file names with translated texts. Layout pages you leave out reuse the root layout. A single page you leave out makes that language reuse the root page whole, its text too: to translate a page, do not leave it out. Links in `en/` pages may name the root file directly (`about.html`): a page the folder omits resolves to the root page of the same name, and later to `en/about.html` once you add it. Put the language switcher (`data-evo-lang-switch`, spec 1A) in the header of every language. When the old site's other language has no translated content (its pages show the main language), translate only what you draw (menu, home, header/footer texts) and tell the designer those texts are your translation, to be checked. A language whose menu is not listed is not used on the site: do not add its folder.

**When the old site does not match.** The pack describes the site as it is in Evomni now; the old site may differ: one old page with tabs split into several single pages, old ids and category numbers that appear nowhere in the pack, pages whose old title order differs from the menu, curated pages ("New Arrival") that no Evomni block reproduces exactly, fixed blocks (an old web agency's "Designed by …" credit, a search icon, a visitor counter). Find the old sub-page URLs in the old page's HTML and add them to the snapshot list (run again into the same folder). Match by the titles shown on the old pages; build what the spec supports (a search icon becomes a `data-evo-search` box); drop what it does not and agency credits. Never guess silently: list every item you could not match, or decided to drop or approximate, in the page plan and the delivery note, for the designer to confirm.

A text-page frame may hold a breadcrumb (`data-evo-breadcrumb`: its content is generated and may differ). Do not add pages the site does not have unless the brief asks; they are created only if the operator ticks "只新增新資料". Never use custom fields (`data-evo-field="custom:…"`): converted sites have none.

## The old body content

Bodies stay as they are on the site: old markup with inline styles (tables with fixed widths, `<font>`, `<br>` runs, images without size limits). The new frame must make them readable:

1. Give every body container (`[data-evo-body]` on detail and text pages) the extra class `evo-legacy`.
2. Copy `references/legacy-body.css` into the package (e.g. `assets/css/legacy-body.css`) and link it on every page after your own CSS.
3. For each class listed under "本文用語統計" in site-context.md, add a rule scoped to `.evo-legacy .that-class` in your CSS if the old look matters (check it in the snapshot).

Promise readable, not pixel-identical, old content.

## Steps

1. Read `site-context.md`; list the pages you will produce (table above) and show the list to the user with the mode.
2. Look at the snapshot screenshots of each page you redraw; note colours, fonts, header/footer structure.
3. Build the shared header/footer and the home, then the inner layouts (full) or the copied example layouts (hybrid). Then review by eye what no checker sees: every excerpt word for word against the snapshot, images cropped and with fitting `alt`, every link going to the page its text names.
4. Run `node scripts/check-site.mjs <folder> --context <site-context.md>` until 0 errors. A clean first run is normal. `--context` compares your file names, list-page `<title>`s, `data-evo-category` values and form titles with the site (rule CONTEXT, WARN); fix or explain each one. If it stops with exit code 2, read the message: site-context.md is too old or damaged (ask for a new one), or it was made by a newer admin than this skill ("made by a newer admin": get the latest evomni-html skill). The import preview shows the claims.
5. Zip and hand over with the checker output and a note of the rounds you took (no `zip` command: run `python3 -m zipfile -c ../site.zip .` inside the site folder, so the zip root holds index.html; folder entries in the zip and one wrapping folder are fine). A passing check writes `evomni-check.json` into the site root (it records which skill version checked the site): the zip must include it; never edit or write that file by hand. Limits: 200 MB unpacked, 2000 files; scale images to their display width first (full-width about 1920px, content about 1200px, cards about 600px).

## Snapshot script

```
node scripts/snapshot.mjs <out-folder> <url|name=url> [<url|name=url> ...]
node scripts/snapshot.mjs <out-folder> --list urls.txt   # one URL per line; "name=URL" to name a page; # comments

Options: --no-shots  --width 1440  --mobile  --max-mb 200  --timeout 20000
Needs Node 18+. Screenshots also need Playwright, installed into the skill folder:
  npm i --prefix <skill-folder> playwright
  cd <skill-folder> && npx playwright install chromium
Without it the script stops before downloading and prints these commands with the real path. The install prints little; `shots N` in the next snapshot summary confirms it works.
Run it again into the same folder to add pages: manifest.json is merged, not replaced.
--no-shots saves HTML/CSS/images only (no screenshots: you cannot see the pages).
```

Output:
- `pages/<name>.html`: raw server HTML (UTF-8); `pages/<name>.local.html`: the same page with assets pointing at `assets/` (open offline to compare); `pages/<name>.rendered.html`: DOM after JavaScript (Playwright only).
- `assets/<host>/<path>`: CSS (rewritten), images, fonts. Scripts are not downloaded, only listed.
- `shots/<name>-top.png`, `-full.png` (and `-mobile-*.png`).
- `manifest.json`: pages, assets (url → path, bytes, type), failures, scripts, totals.

Read the screenshots first, then `pages/<name>.rendered.html` (or `.html`) for texts and structure, and search the CSS under `assets/` for colours and fonts. 404s on old fonts and icons are normal (dead references in old CSS).
