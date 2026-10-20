# Evomni site package spec

Part of the evomni-html skill; its version is the skill's (`VERSION`).

Read this whole file before generating any HTML. Rules marked MUST are checked by `scripts/check-site.mjs`; a violation blocks or degrades the import.

Visual design is unrestricted: layout, colors, fonts, animation, interaction and any front-end library (any version, local file or CDN) are your choice. What is restricted is **function and data**: only the page types, fields and features listed here exist in the target CMS (Evomni).

## R. Hard rules (summary)

R1. Every `.html` file MUST declare its page type on `<body data-evo-page="…">` (section 2).
R2. Every page MUST have exactly one `<header data-evo-shared="header">`, one `<main>`, one `<footer data-evo-shared="footer">`, in that order, as direct children of `<body>` (scripts may follow). Header and footer MUST be byte-identical on every page except the `class`/`aria-current` on the current menu item, which you should not set at all.
R3. Pages of the same collection MUST share one layout: outside `[data-evo-body]` they may differ only in the text/`src`/`href`/`alt` of `[data-evo-field]` elements (section 5). All text pages (a `page` that contains `[data-evo-body]`, section 5.6) likewise share one layout, differing only in the `title` field text.
R4. Data MUST be written in HTML. Never render content (cards, posts, products, menu items) from JavaScript arrays or fetch calls. JavaScript is for effects only.
R5. No inline event handlers (`onclick=`, `onload=`, any `on*` attribute), no `javascript:` URLs, no `eval()` / `new Function()`, no JS that injects `<script>` tags from other domains. (Blocked by the site's Content-Security-Policy.)
R6. Only the features in this spec. If the brief asks for something not listed (member-only pages, booking, multi-level categories, comments, custom checkout, client-side filtering/sorting of lists…), do not build it; tell the designer it is not supported.
R7. One language per folder: the root holds the site's main language (Traditional Chinese unless told otherwise). Other languages only when the brief asks, as language folders (section 1A); the importer handles them when redrawing an existing multi-language site (references/redraw.md). A new site is built in the main language only: do not add language folders or a language switcher to a new site.
R8. All internal links are relative links to `.html` files in the package; every link target and every image/CSS/JS/font file MUST exist in the package (CDN URLs for libraries/fonts are allowed).
R9. A replaceable image MUST be an `<img>` (or `<picture>`). CSS `background-image` is decoration only and cannot be changed by the site admin. Text, gradients and overlays on top of images are fine (the admin selects covered images from the layer panel), except inside a product `gallery`.
R10. Use `data-evo-*` attributes exactly as specified. Do not invent new `data-evo-*` names or values.
R11. Never use the platform's own binding attributes `data-loop`, `data-field`, `data-if`, `data-href`, `data-src` (the front end rewrites or drops elements that carry them).

## 1. Package layout

```
index.html                 home page (required)
<slug>.html                one file per page, all in the root folder (language folders: section 1A)
assets/…                   images, css, js, fonts (folder names free)
```
- File name = URL slug: lowercase letters, digits, hyphens (`news-spring-launch.html`), 2–64 characters, not only digits, and not a reserved word (admin, login, logout, api, user(s), settings, category, categories, data, menu, captcha, sitemap, submit, complete, action, search, article, product, eform, download, faq, album, member, forms, cart, checkout, inquiry-cart, get, post, put, patch, delete). `index.html` is the home page. The final site URLs are decided by the system; the importer rewrites your internal links, so just link to the `.html` files.
- Page SEO: write these in `<head>`; each maps to one admin SEO field. Nothing you leave out is invented (the field stays empty and the system falls back to the page title / summary / cover image).

| Tag | Admin SEO field | Applies to |
|---|---|---|
| `<title>` | page title. Write the page name only: the system appends ` | <site name>` to every page title itself, so a brand suffix you add (` | Brand`) would show twice. A suffix shared by all non-home pages is removed on import | home, page, article detail, product detail |
| `<meta name="description" content="…">` | description | same |
| `<meta name="keywords" content="a, b">` (comma-separated) | keywords | same |
| `<meta property="og:title" content="…">` | share title | same |
| `<meta property="og:description" content="…">` | share description | same |
| `<meta property="og:image" content="…">` | share image: a package file (jpg/png/webp) or an external https URL | same |
| `<meta name="evo:search-keywords" content="a, b">` | site-search keywords (tags) of the record; not shown on the page | article detail, product detail (not for e-commerce plans' products) |

  List pages (`article-list`, `product-list`): the same six SEO tags are read and become the SEO of the collection (main list page) or of the category (a list page with `data-evo-category`).
- CSS: put site-wide styles in shared stylesheet(s) linked by every page; put page-only styles in a stylesheet linked only by that page. The same class name MUST NOT be styled differently in two stylesheets (all shared CSS becomes one site stylesheet).
- Do not style through your own `<body>`/`<html>` classes or attributes; they are not kept. Put a page-specific wrapper class on the first element inside `<main>` instead. The system adds these classes to `<body>`, which you may use: home `index-page`; list pages `page-list`; article/product detail pages `page-detail`. Standalone pages (`page`) get no class of their own: always use your wrapper class.

## 1A. Language folders (redrawing a multi-language site only)

```
index.html, *.html        main language (root)
en/index.html, en/*.html  another language: folder name = the site's language prefix (from the site context pack)
assets/…                  shared by every language (en pages link ../assets/…)
```
- One folder level only. Each language folder is a whole site: its own `index.html` (home, header, footer, menu in that language's titles).
- Same file name = the same page in another language (`en/about.html` is About in English). A page in a language folder that is not home or a list page MUST have a root page with the same name, page type and collection.
- Detail pages: keep the same file names and give `data-evo-category` the categories in the same order as the root page (names are matched by position: write the translated names).
- Layout pages may be left out: a language folder without a collection's list/detail pages or without text pages reuses the root layout (its fixed texts stay in the main language; the import preview lists them).
- Single pages: leaving one out means that language reuses the root page whole, its text too (the import preview lists it). To translate a page, do not leave it out.
- Custom fields keep the root `custom:<name>` names in every folder.
- Language switcher: one element with `data-evo-lang-switch` in the header of every language, holding one `<a>` per language that links to that language's `index.html` (in root pages: `index.html` and `en/index.html`; in `en/` pages: `../index.html` and `index.html`). Style it freely; the system marks the current language's link `is-active` and points each link to the same page in that language.

```html
<div class="lang" data-evo-lang-switch><a href="index.html">中文</a><a href="en/index.html">EN</a></div>
```

## 2. Page types

| Page type | `<body>` attributes | Count | Becomes |
|---|---|---|---|
| Home | `data-evo-page="home"` | exactly 1 (`index.html`) | home page |
| Page | `data-evo-page="page"` | any | standalone page (about, services, contact…). With one `[data-evo-body]` in `<main>` it is a **text page** (privacy, terms…; section 5.6) |
| Article list | `data-evo-page="article-list" data-evo-collection="<key>"` | 1 per collection (+ optional 1 per category) | article category list |
| Article detail | `data-evo-page="article-detail" data-evo-collection="<key>"` | 1 per article | one article record |
| Product list | `data-evo-page="product-list" data-evo-collection="<key>"` | 1 per collection (+ optional 1 per category) | product category list |
| Product detail | `data-evo-page="product-detail" data-evo-collection="<key>"` | 1 per product | one product record |

- `<key>`: lowercase letters/digits, e.g. `news`, `cases`, `products`. A site may have several article collections and several product collections.
- Category: add `data-evo-category="<name>"` to a detail page; several categories separated by `|`. Categories are one level only (no sub-categories). A list page with `data-evo-category="<name>"` is that category's list page; a list page without it lists the whole collection. A category list page MUST use exactly the same layout as the collection's main list page (only the cards differ).
- Anything with an "add to inquiry" or "add to cart" button MUST be a product detail page. Brand pages that need an inquiry button are products. Content without price or buttons (portfolio works, cases, news) is an article collection.
- Do not build these pages; the system provides them with its own fixed design: search results, 404 / error pages, member login / register / member center, inquiry cart, shopping cart, checkout, order pages. You may link to them with the markers in section 7.

## 3. Shared header, footer and main menu

```html
<header data-evo-shared="header">
  <a class="logo" href="index.html"><img src="assets/img/logo.svg" alt="Brand"></a>
  <nav data-evo-menu>
    <ul>
      <li><a href="about.html">關於我們</a></li>
      <li><a href="services.html">服務項目</a>
        <ul><li><a href="service-design.html">設計服務</a></li></ul>
      </li>
      <li><a href="news.html">最新消息</a></li>
    </ul>
  </nav>
</header>
```
- Exactly one `nav[data-evo-menu]`, inside the header. Nested `ul > li > a`, max 3 levels. Every `<li>` at the same level has the same classes and inner structure, except that any item may additionally contain one nested `<ul>` submenu (the first item of each level is the template for all items, which the admin can add/remove/reorder).
- Menu links point to pages in the package (or full external URLs). No `#` placeholder links.
- The system adds `is-active` to the current item's `<li>` and `<a>`, and `is-active-parent` to its ancestors. Style these classes; never hard-code them.
- Mobile menu toggles, dropdown animation, sticky header: your own CSS/JS.
- Other links in the header/footer (social icons, footer link columns) are fixed content: kept as written, editable in the admin canvas.
- No forms in the header or footer (a search box is allowed, see 7.3).

## 4. Editable content on pages

All visible text, `<img>` and links outside the structures below can be edited by the admin in the page editor. Two structures add item-by-item editing:

| Content | Marker | Admin can |
|---|---|---|
| Repeating items (cards, slides, team members, features, logos) | container `data-evo-repeat` | add / delete / reorder / edit each item |
| Repeating items whose count is part of the layout (e.g. exactly 4 service tiles) | container `data-evo-repeat="fixed"` | edit each item only |

```html
<div class="team-grid" data-evo-repeat>
  <article class="member">
    <img src="assets/img/team-amy.jpg" alt="Amy Chen">
    <h3>Amy Chen</h3>
    <p class="role">Design Director</p>
  </article>
  <article class="member"> …identical structure… </article>
</div>
```
Repeat rules (MUST):
- The container's direct children are the items. Every item has the identical element structure and classes; only text, `src`, `href`, `alt` differ. The first item is the template for "add item".
- One text value per element: do not split a title with `<br>`; use two elements.
- For a Swiper/slider, put `data-evo-repeat` on the element whose direct children are the slides (e.g. `.swiper-wrapper`).
- `<ul>/<ol>` lists inside an item whose `<li>` contain plain text only become one multi-line field.
- No nested `data-evo-repeat`.

FAQ:
```html
<div class="faq" data-evo-faq>
  <details><summary>Question text</summary><div class="answer"><p>Answer, one or more paragraphs.</p></div></details>
  <details><summary>…</summary><div class="answer"><p>…</p></div></details>
</div>
```
Each `<details>` = one Q&A (admin can add/reorder). `<summary>` contains text only. Search engines get FAQ structured data automatically. A page may have several FAQ blocks (e.g. one per topic).

Tables: a normal `<table>` with `<thead>/<tbody>/<tr>/<th>/<td>` becomes an editable table. No merged cells (`rowspan`/`colspan`).

## 5. Collections: detail pages and list pages

### 5.1 Detail page = one record

```html
<body data-evo-page="article-detail" data-evo-collection="news" data-evo-category="Events">
  <header data-evo-shared="header">…</header>
  <main>
    <div class="news-detail">
      <nav class="breadcrumb" data-evo-breadcrumb>…section 5.4…</nav>
      <h1 data-evo-field="title">Spring launch event</h1>
      <time data-evo-field="date">2026-03-15</time>
      <img data-evo-field="cover" src="assets/img/news-spring.jpg" alt="Launch event">
      <div class="post-body" data-evo-body>
        <p>This article's own content: free layout, images, sliders, tables…</p>
      </div>
      <nav class="post-nav" data-evo-adjacent>
        <a data-evo-field="prev-link" href="news-winter-sale.html"><img data-evo-field="prev-image" src="assets/img/news-spring.svg" alt=""><span data-evo-field="prev-title">Winter sale</span></a>
        <a data-evo-field="next-link" href="news-summer-camp.html"><span data-evo-field="next-title">Summer camp</span></a>
      </nav>
    </div>
  </main>
  <footer data-evo-shared="footer">…</footer>
</body>
```
- Exactly one `[data-evo-body]` per detail page and per text page (5.6); no other page type has one. It holds the record's own content (free layout, may differ per page; editable by the admin per record) and MUST NOT sit inside `data-evo-repeat` or `data-evo-list`.
- Content inside `[data-evo-body]` SHOULD use semantic tags only: `p`, `h2`-`h4`, `ul`/`ol`/`li`, `img`, `figure`/`figcaption`, `table`, `blockquote`, `a`, `strong`/`em`. Write its styles as descendant selectors of the layout's body container (`.post-body p`, `.post-body h2`, `.post-body table`…), and avoid custom classes and inline `style` inside the body. Reason: when the site is re-skinned later the record bodies are NOT re-imported, so a new design must be able to dress the existing body content using these selectors alone. (Not enforced by the checker.)
- Everything outside `[data-evo-body]` is the collection layout, written once and repeated identically on every detail page of the collection, with only `[data-evo-field]` values changing (R3). If a piece of content differs between records, it is either a field or it belongs inside `[data-evo-body]`. Exceptions that may differ freely: the contents of `[data-evo-breadcrumb]` (generated), the number of images in `gallery` and of options in `variants`.
- A field element contains only its value (no child elements), except `cover`/`gallery`/`price` described below.
- Empty value: if a record has no value for a field, keep the element and leave its value empty (`price-original` keeps its currency span with no number). The system hides empty `author`, `date`, custom fields.

Article fields (`data-evo-field` value):

| Field | Element | Notes |
|---|---|---|
| `title` | any text element | required, one line of text |
| `date` | `<time>` with text `YYYY-MM-DD` | publish date. To show parts separately use `date-year`, `date-month`, `date-day` elements instead |
| `cover` | `<img>` | ONE image; also used on list cards. Articles have no multi-image field: put extra images inside `[data-evo-body]` |
| `summary` | text element | plain text, used on list cards |
| `author` | text element | plain text |
| `date-full` | text element | publish date written out as `YYYY年MM月DD日` (the sample text is replaced) |
| `update-date` | `<time>` with text `YYYY-MM-DD` | last-updated date (set by the system when the record is saved). Parts: `update-date-year`, `update-date-month`, `update-date-day`; written out: `update-date-full` (`YYYY年MM月DD日`). Hidden when empty |
| `prev-link` / `next-link` | `<a>` inside `[data-evo-adjacent]` | previous/next record in admin order; `prev-title`/`next-title` inside. Sample values: link to any detail page of the same collection; the system fills the real ones |
| `prev-image` / `next-image` | `<img>` inside `[data-evo-adjacent]` (inside the matching `prev-link`/`next-link`) | cover thumbnail of the previous/next record: `src` is replaced; a record without a cover loses the whole `<img>`, so do not rely on it for layout. Give it a package image as sample |
| `category` | text element (article detail only) | name of the article's category (the main one when it has several); removed when the article has no category |
| `custom:<name>` | text element | custom field, see 5.5 |

Product fields:

| Field | Element | Notes |
|---|---|---|
| `title` | text element | product name, ONE field (no separate brand line + model line; let it wrap) |
| `summary` | text element | plain text only; line breaks as plain newlines in the text (style with `white-space: pre-line`), no `<br>`, badges, bullets, bold, colors |
| `gallery` | container whose children are either all `<img>`, or all slides (one element per image holding exactly one `<img>`, optionally inside a link, and nothing else) (max 20) | product images; each `<img>`'s `alt` becomes that image's alt text; nothing overlaid on the images; captions not supported. The children are product images, nothing else: put carousel buttons, dots and counters outside the `gallery` element (or create them in JS). A main image + thumbnail strip may be two `gallery` elements; both show the same product images (the first one's are imported). After import the system writes one child per product image (the admin uploads them on the product form), copying your first child with its classes. A carousel is your own JS: count the slides from the DOM when the page loads, never a fixed number, and show no controls for a single image. In the admin page editor your JS does not run and only the first image is shown, as a placeholder; style the gallery so the first image looks right without JS |
| `cover` | `<img>` | list-card image (if omitted, the first gallery image is used) |
| `price` | element containing `<span data-evo-field="currency">NT$</span>` followed by the number | selling price; leave the number empty for inquiry-only products (the system then hides it) |
| `price-original` | same structure as `price` | crossed-out original price; shown only when set |
| `sku` | text element | product code |
| `update-date` (+ `-year/-month/-day/-full`) | as for articles | last-updated date |
| `spec-table` | `<table>` of plain `<tr>` rows, each row two cells (`<th>` name, `<td>` values); no `<thead>`/`<tfoot>`/`<caption>` | shows the product's variant groups as name / values (the same data as the variant selector). Write one sample row. Other product facts belong in custom fields or the body |
| `stock-count`, `sold-count`, `temp-zone` | text element each | e-commerce sites only: stock quantity, units sold (only when the admin shows it), temperature zone label (only when set). On a site without e-commerce, or when there is no value, the element disappears. Put labels in CSS (`::before { content: "Stock " }`) so they vanish with it |
| `custom:<name>` | text element | custom field, see 5.5 |

Product variants (color, size…) and buttons: section 6.

### 5.2 List page

```html
<body data-evo-page="article-list" data-evo-collection="news">
  …
  <main>
    <div class="news-list-page">
      <ul class="news-grid" data-evo-list data-evo-page-size="9">
        <li class="news-card" data-evo-item>
          <a data-evo-field="link" href="news-spring-launch.html">
            <img data-evo-field="cover" src="assets/img/news-spring.jpg" alt="">
            <time data-evo-field="date">2026-03-15</time>
            <h3 data-evo-field="title">Spring launch event</h3>
            <p data-evo-field="summary">Short summary…</p>
          </a>
        </li>
        <li class="news-card" data-evo-item>…same structure, links to another detail page…</li>
      </ul>
      <p class="empty" data-evo-empty>No articles yet.</p>
      <nav class="pager" data-evo-pagination>
        <a data-evo-page-link="prev" href="#">Prev</a>
        <a data-evo-page-link="number" href="#">1</a>
        <span data-evo-page-link="current">2</span>
        <a data-evo-page-link="next" href="#">Next</a>
      </nav>
    </div>
  </main>
```
- `[data-evo-list]` holds `[data-evo-item]` cards. Include at least 2 sample cards, each linking (`data-evo-field="link"`) to a real detail page of the same collection. All cards identical in structure. The real cards are generated from the records; your cards are the template (so the number of sample cards may differ between list pages).
- Card fields: `link`, `title`, `cover`, `summary`, `category` (the record's category name), `custom:<name>`; articles also `date` (or `date-year/-month/-day`); products also `price`, `price-original`, `sku` (product model/code; the element is removed when the product has none). Product cards have no date. The sale badge (`data-evo-if="sale"`) is for detail pages only; on cards show `price-original`, which disappears when empty.
- `data-evo-page-size` is required when there is a pagination block. Pagination has only prev / page number / current / next (no first/last). It is hidden automatically when there is one page. `href="#"` is allowed only inside `[data-evo-pagination]`.
- `[data-evo-empty]` is shown only when the list has no records.
- Category navigation: plain links to the category list pages (section 2), identical on every list page of the collection (there is no "current category" highlight). Never point every category link at the main list page: they would all open the full list (checker CATEGORY-LINKS warning). The heading is the same on all of them too: category names cannot be shown as a page heading. No JS filtering, no sort dropdown, no "load more" button.
- Records appear in the order set in the admin (not automatically by date). There is no "featured"/"best seller" flag: to feature records, the admin puts them first (a "latest N" block then shows them), so don't invent a fake category for it.

Category fields (optional, on a list page outside the cards; the first element of each kind is read, nothing is invented when absent). The main list page fills the collection's own category, a list page with `data-evo-category` fills that category:

| Field | Element | Admin field |
|---|---|---|
| `category-cover` | `<img>` (its `alt` is used too) | category list image |
| `category-summary` | text element | category list summary |
| `category-banner` | `<img>` | category banner image |

Count line (optional, outside the cards): `<p data-evo-list-total>共 <span data-evo-field="total-count">12</span> 筆</p>`. The text around the number is kept as written; the number becomes the count of records (after search/filter). One per page, list pages only.

Hot keywords: see section 6A.

### 5.3 "Latest N" on other pages (home, etc.)

```html
<div class="home-news" data-evo-list data-evo-source="news" data-evo-limit="3">
  <article class="news-card" data-evo-item>…card fields as in 5.2…</article>
</div>
```
- `data-evo-source` = collection key; optional `data-evo-source-category="<name>"`. `data-evo-limit` = number of records (1–50). No pagination here.

### 5.4 Breadcrumb

```html
<nav class="breadcrumb" data-evo-breadcrumb>
  <ol>
    <li data-evo-crumb><a href="index.html">Home</a></li>
    <li data-evo-crumb-sep aria-hidden="true">/</li>
    <li data-evo-crumb><a href="news.html">News</a></li>
    <li data-evo-crumb-sep aria-hidden="true">/</li>
    <li data-evo-crumb-current>Spring launch event</li>
  </ol>
</nav>
```
- Generated from the main-menu path; home is always first. Only use a breadcrumb on pages reachable from the main menu (or detail pages of a collection whose list page is in the main menu). Each level is a real clickable page.

### 5.5 Custom fields (use sparingly)

A custom field adds a structured field to every record of a collection. Use one ONLY if all are true:
1. Every record of the collection has this information and the value differs between records (e.g. product origin, case completion year).
2. The value is short: one word, a number, or one of a few options. Not a paragraph.
3. It is shown at a fixed place in the collection layout (detail layout and/or list card). Information that appears only in one record's text belongs in `[data-evo-body]`.
4. No built-in field fits (never duplicate title, date, summary, cover, price, sku, category).

Syntax: `data-evo-field="custom:<name>"`, e.g. `<span data-evo-field="custom:產地">日本</span>`. `<name>` is shown as the field label in the admin, any language. Same `<name>` = same field across the collection. At most 5 custom fields per collection.
Optional `data-evo-type="option"` when the values come from a small fixed set shared by many records (e.g. Japan / Germany / Taiwan); otherwise it is free text. Put it on every element of that field (detail pages and cards). Multiple options in one record: separate with `|`; option values may contain spaces.
Not supported (do not design for them): sorting by a custom field, numeric ranges (price/size sliders), free-text fields as filters, finding custom-field values via site search, image/link/date/long-text custom fields.
Option fields can power a filter form on a list page — see 7.4.

### 5.6 Text pages (privacy, terms, single-content pages)

A text page is a `page` whose `<main>` contains exactly one `[data-evo-body]`. Use it when several pages share one frame and only the text differs. A `page` WITHOUT `[data-evo-body]` is a custom standalone page (about us, landing…): the whole page is its content, and none of the rules below apply.

```html
<body data-evo-page="page">
  <header data-evo-shared="header">…</header>
  <main>
    <div class="text-page">
      <h1 data-evo-field="title">Privacy policy</h1>
      <div class="text-body" data-evo-body>
        <h2>1. What we collect</h2>
        <p>The page's own text…</p>
      </div>
    </div>
  </main>
  <footer data-evo-shared="footer">…</footer>
</body>
```
- Outside `[data-evo-body]` is the text-page layout: written once, byte-identical on every text page. The only thing that may differ is the text of `[data-evo-field="title"]`. No other `data-evo-field` outside the body. Violations are reported as LAYOUT-DIFF (can be force-imported, but fix them).
- Inside `[data-evo-body]` is the page's own text, edited per page in the admin. The semantic-tag rule of 5.1 applies.
- The frame belongs to the design (replaced on a re-skin); the body belongs to the data (not re-imported on a re-skin). So keep everything that is part of the design OUTSIDE the body.

## 6. Product buttons, variants, e-commerce

All buttons below MUST be inside a product detail page, inside one container `data-evo-buy`. When it has cart or buy buttons it MUST also contain the product's `price`.

| Button / element | Marker | Notes |
|---|---|---|
| Add to inquiry | `<button data-evo-action="inquiry">` | for sites using inquiry (no online payment) |
| Variant selector | `<div data-evo-field="variants">` with sample options inside: `<button data-evo-option>Red</button>` | only when the product has variants (color, size). Options come from the admin. Do not build "1 variant with 1 value" for a single-variant product: just omit the selector |
| Quantity | `<input type="number" data-evo-field="qty" value="1" min="1">` | your own +/- buttons and JS are fine |
| Add to cart | `<button data-evo-action="cart">` | e-commerce sites |
| Buy now | `<button data-evo-action="buy">` | e-commerce sites |
| Notify when back in stock | `<button data-evo-action="notify">` | e-commerce sites; shown when sold out |
| Favorite | `<button data-evo-action="favorite">` | e-commerce sites; visitors who are not logged in are asked to log in |

- The system sets `data-pdstate="normal|soldout|nosale"` on the `[data-evo-buy]` container. Style each state (e.g. hide the cart button and show the notify button when `[data-pdstate="soldout"]`).
- A sale badge: put it in an element with `data-evo-if="sale"`; it is removed when the product has no original price.
- Do not build: variant images, a shipping-weight display, countdown timers, bundles, add-on deals, reviews. (Not supported or still in development.) Variant values such as `75g` / `150g` are fine.
- On sites without e-commerce, the cart/buy/notify/favorite buttons are removed automatically; the inquiry button works on all sites.

## 6A. Other blocks the platform fills

Keep your own markup and classes; the markers only say what is what. Details are checked by the COMPONENT rule.

**Newsletter signup** (any page, header/footer allowed). No `<form>`:
```html
<div class="newsletter" data-evo-newsletter>
  <input type="email" placeholder="Email">
  <button type="button" data-evo-newsletter-action="subscribe">Subscribe</button>
  <button type="button" data-evo-newsletter-action="unsubscribe">Unsubscribe</button>
</div>
```
Exactly one `<input type="email">`; at least one action (`subscribe` / `unsubscribe`) on a `<button>` or `<a>` (`href="#"` is fine). Messages are shown by the platform.

**Hot keywords** (any page). Keywords come from the article tags:
```html
<div class="hot-kw" data-evo-hot-keywords="auto" data-evo-limit="8">
  <h3>Hot keywords</h3>
  <ul><li><a href="#"><span>Lighting</span></a></li></ul>
</div>
```
- `auto` = the most used article tags (the page's own records on a list page; `data-evo-limit` 1–30, default 10). `manual` = a fixed list: write every keyword as an `<li>` (no limit attribute). Clicking a keyword searches for it. In `manual`, a keyword is shown only if some published article carries it as a search keyword (`evo:search-keywords`); other words are dropped, and the block disappears if none remain.
- One `<ul>`/`<ol>`; the first `<li>` is the template; each `<a>` holds the keyword text directly or in one inner element. An optional heading outside the list is the block title. The block is removed when there are no keywords.

**Related content** (detail pages only, once per page):
```html
<aside class="related" data-evo-related="latest-category" data-evo-limit="3">
  <h2>Read more</h2>
  <div class="track">
    <a class="card" data-evo-item data-evo-field="link" href="news-b.html">
      <img data-evo-field="cover" src="assets/img/b.jpg" alt="">
      <span data-evo-field="category">News</span>
      <h3 data-evo-field="title">Title</h3>
      <div data-evo-field="keywords"><span>tag</span></div>
    </a>
    <a class="card" data-evo-item …same structure…></a>
  </div>
</aside>
```
- Article pages: value `latest-category` (same category, default) or `similar-tags` (most shared tags); `data-evo-limit` 1–12 (default 6). Card fields: `link`, `title`, `cover`, `category`, `keywords` (tags).
- Product pages: no value; shows the products chosen in the product's "related products" tab; `data-evo-limit` 1–20. Card fields: `link`, `title`, `cover`, `sku`, `price`, `price-original` (as in 5.2); other card fields are not filled (warning).
- Each card is itself `<a data-evo-item data-evo-field="link">` linking to a real record of the same collection; cards sit in one wrapper element inside the container. The whole block is removed when there is nothing to show.

**Payment and shipping methods** (product-detail pages, e-commerce sites only; on a site without e-commerce the importer removes the whole list and warns, so do not rely on it for inquiry sites):
```html
<ul data-evo-payment>
  <li data-evo-payment-item="credit_card"><img src="assets/img/card.svg" alt=""><span data-evo-field="payment-name">Credit card</span></li>
  <li data-evo-payment-item="cod"><span data-evo-field="payment-name">Cash on delivery</span></li>
</ul>
```
Payment codes: `credit_card`, `line_pay`, `atm_transfer`, `cvs_code`, `cvs_barcode`, `bank_transfer`, `cod`, `aftee`, `custom_offline`. Shipping (`data-evo-shipping`, `data-evo-shipping-item`, `data-evo-field="shipping-name"`): `home`, `cvs_c2c`, `cvs_b2c`, `warehouse`. Only the methods the shop has enabled are shown, with the names set in the admin; the rest of your items are removed.

**Share buttons** (any page, header/footer allowed). Shares the current page (its canonical URL):
```html
<div class="post-share" data-evo-share>
  <a href="#" data-evo-share-platform="facebook">Facebook</a>
  <a href="#" data-evo-share-platform="line">LINE</a>
  <button type="button" data-evo-share-platform="copy">Copy link</button>
</div>
```
- Platforms: `facebook`, `line`, `x`, `linkedin`, `copy`. Put the marker on an `<a>` (`href="#"` is fine) or `<button>`. After `copy` the button gets class `is-copied` for 2 seconds; style any "copied" hint yourself.

**Table of contents** (once per page, usually inside the article layout). Built from the `h2`/`h3` of the article:
```html
<nav class="post-toc" data-evo-toc>
  <ol><li><a href="#">Heading</a></li></ol>
</nav>
<div class="post-body" data-evo-body data-evo-article-region>…</div>
```
- One `<ul>`/`<ol>`; the first `<li>` (containing an `<a href="#">`) is the sample item, one copy is made per heading. Items get `toc-item--lvl2` / `toc-item--lvl3`; the current section's link gets `is-active`. The whole block is hidden when the page has no headings.
- `data-evo-article-region` (at most one per page) marks where to look for headings; without it the platform scans `<main>`, else `<article>`.

**Video** (any page). YouTube or Vimeo only; the platform builds the embed itself:
```html
<section class="hero-video" data-evo-video="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
         data-evo-video-mode="background" data-evo-video-mobile-image="assets/img/hero-mobile.jpg">
  <h1>Title</h1>
</section>
<div class="video-box" data-evo-video="https://vimeo.com/76979871" data-evo-video-mode="popup" data-evo-video-poster="assets/img/cover.jpg">
  <button type="button" data-video-play>Play</button>
</div>
```
- `data-evo-video-mode`: `background` (default; muted loop filling the container) or `popup` (click the container, or an inner `[data-video-play]`, to open a dialog). `data-evo-video-poster` / `data-evo-video-mobile-image` are image files in the package (mobile image: at 768px or narrower the image is shown instead of the video, background mode).
- In `popup` mode with a `[data-video-play]` button, only that button opens the dialog, and the poster image is laid over the container: give the button `position: relative; z-index: 1` so it stays clickable above the poster.
- Any other address is not embedded (ERROR). The site's CSP is widened for YouTube/Vimeo automatically.

**Download list** (home page and standalone pages, once per page). The platform shows file lists only through its download templates, so this is the one place where **you accept the template's look**: draw the list as a preview, mark the data, and the importer replaces your block with the template filled with your rows. Style it afterwards only through the template's own options and high-specificity CSS (the template's CSS is scoped under its wrapper, so write selectors at least as specific, for example `body .tpl-download001 .download-row { … }`; plain class selectors can lose).
```html
<section class="dl" data-evo-download="table" data-evo-page-size="10">
  <h2>Downloads</h2>
  <ul>
    <li data-evo-download-item>
      <span data-evo-download-name>2026 Catalog</span>
      <time data-evo-download-date>2026-03-01</time>
      <a data-evo-download-file href="assets/files/catalog.pdf" target="_blank">PDF</a>
      <a data-evo-download-file href="assets/files/prices.xlsx">Excel</a>
    </li>
  </ul>
</section>
```
- `table` (download001): search bar + table, up to 3 file kinds. The link text is the column label; give each file kind the same label in every row (a row may lack some). Date = `YYYY-MM-DD`. The heading outside the rows becomes the block title. `data-evo-page-size` 5–100 (default 10).
- `cards` (download002): cover cards with a year filter. Each item has exactly one file link (its text is the button label, same for all cards), an optional `<img data-evo-download-cover>` and a date given as a year (`2026`) or `YYYY-MM-DD` (only the year is kept; the card shows no date). `data-evo-page-size` 1–60 (default 9).
- `href` is a file in the package (PDF, Word, Excel, ZIP… uploaded to the media library) or an `https://` URL. `target="_blank"` opens a new tab. Year filter, keyword search and pagination come with the template.
- Not for article / product detail pages.

No marker needed:
- Social links: plain `<a href="https://…" target="_blank" rel="noopener">`.
- Home-page news carousel: a "latest N" list (5.3) plus your own slider JS (see section 8).

Not supported yet (do not build): regex / pattern validation of form fields. (Share buttons, the table of contents and background/popup video are the blocks above; previous/next thumbnails and the article category name are fields, section 5.1.)

## 7. Forms, search, member and cart links

### 7.1 Forms
```html
<form data-evo-form="Contact us">
  <label for="f-name">Name</label><input id="f-name" name="name" type="text" required>
  <label for="f-mail">Email</label><input id="f-mail" name="email" type="email" required>
  <label for="f-msg">Message</label><textarea id="f-msg" name="message" maxlength="500"></textarea>
  <label><input type="checkbox" data-evo-consent required> I agree to the privacy policy</label>
  <div data-evo-captcha></div>
  <button type="submit">Send</button>
</form>
```
- Field types: `text`, `email`, `tel`, `number`, `url`, `date`, `time`, `datetime-local`, `textarea` (optional `maxlength`), `select`, radio group, checkbox group, `file` (one file ≤10 MB). Each field has a `<label>`. Optional consent checkbox (max 1, last; its label is plain text, no links) and captcha.
- The system builds the form from your fields and renders it with its own fixed HTML: your form markup is only read for its fields, and its look in your preview is replaced. To make the live form look like your design, write your form CSS on these system classes (the example site's site.css shows how):
```html
<form class="eforms-wrapper">
  <div class="form-row">
    <div class="form-tag">Name<span class="main-red">*</span></div>
    <div class="form-col">
      <div class="form-item"><input class="form-style" type="text"></div>
      <div class="form-require-alert">Required</div>
    </div>
  </div>
  <div class="form-row"><div class="form-col btn-group"><button class="outline-btn submit-btn">Send</button></div></div>
</form>
```
  Radio/checkbox options: `<label class="form-radio">` / `<label class="form-checkbox">` containing `<input>` + `<span class="text">`; selects have an extra `form-select-style` class.
- Optional form description: put `data-evo-field="form-description"` on the text element that introduces the form (same page, outside the form). Its text is stored as the form description in the admin; the element stays on the page as written.
- At most one form per page; not in header/footer; not inside sliders or `data-evo-repeat`. The success message is shown by the system: no thank-you page, no submit JS.

### 7.2 Member, cart, inquiry links (header)
`<a data-evo-link="login">`, `<a data-evo-link="register">`, `<a data-evo-link="member">` (member center), `<a data-evo-link="cart">` (e-commerce), `<a data-evo-link="inquiry-cart">`. Write them without `href`; the system fills it. Login/register are hidden when logged in, member is hidden when logged out. Cart item count badges are not supported.

### 7.3 Search box
`<form data-evo-search><input type="search" name="q"><button type="submit">Search</button></form>` (header or any page). Results use the system search page.

### 7.4 List filter (product/article list pages)
`<form data-evo-filter>` with `<select name="custom:<name>">` or checkbox groups whose values are the options of an option-type custom field. Exact-match only. The system handles the query; no JS filtering.
```html
<form data-evo-filter>
  <label for="f-mat">材質</label>
  <select id="f-mat" name="custom:材質">
    <option value="">全部</option>
    <option value="軸承鋼 SUJ2">軸承鋼 SUJ2</option>   <!-- value = the exact text used on the product pages -->
    <option value="不鏽鋼">不鏽鋼</option>
  </select>
  <button type="submit">篩選</button>
</form>
```

## 8. CSS and JavaScript

- Any CSS, any library and version. Libraries may be CDN links or files in the package; they are stored locally on import.
- Script and stylesheet ORDER is kept per page, but only the common prefix of every page's list is made site-wide: keep shared libraries/CSS first and in the same order on every page.
- ES modules: name them `.mjs` (that is how the platform marks `type=module`); relative `import`/`export … from`/`import()` targets inside the package are uploaded with the script, keep their relative paths. A local `<script type="module">` that points to a `.js` file is an ERROR (it would load as a classic script and fail on `import`); rename it to `.mjs`.
- External (CDN) URLs must be plain `https://host/...` (no port other than 443): the site's security policy allows host names only.
- Site-wide JS runs on every page: guard every block (`const el = document.querySelector('.x'); if (!el) return;`).
- JS must work when content is regenerated by the server (cards, menu items, slides may change count). Initialize sliders/animations by querying the DOM at load, never by hard-coded item counts.
- You may select on `data-evo-*` attributes in CSS/JS; the ones you use are kept on import. Prefer your own classes, though: system-generated elements (list cards, menu items, pagination) only carry what your template item carries.
- Embedded iframes (YouTube, Google Maps) are allowed. Background/hero `<video>` (local .mp4 ≤ 50 MB, `muted autoplay loop playsinline`, with a `poster` image) is allowed but is fixed content: the admin cannot replace it.
- Brand colors for system pages (cart, checkout, member): define in your shared CSS `:root{--brand:#…;--brand-hover:#…;--brand-active:#…;--brand-soft:#…;--brand-on:#…}` (`--brand-on` = text color on brand background). System pages otherwise keep their fixed design.

## 9. Before delivering

Run `node scripts/check-site.mjs <site-folder>` and fix every ERROR. Review WARNINGs. Then deliver the site folder as a zip: `index.html` at the zip root or inside one wrapping folder; at most 200 MB unpacked and 2000 files.
