#!/usr/bin/env node
// snapshot.mjs - capture pages of an OLD website into a local folder so an AI
// (which cannot browse) can read the HTML, CSS, images, fonts and screenshots.
//
//   node scripts/snapshot.mjs <out-folder> <url|name=url> [...]
//   node scripts/snapshot.mjs <out-folder> --list urls.txt
//
// Options: --no-shots  --width 1440  --mobile  --max-mb 200  --timeout 20000
//
// Zero-install: HTML + assets use Node 18+ built-in fetch only.
// Screenshots need Playwright: when it is not installed the script stops before downloading anything and prints how to
// install it (into the skill folder); --no-shots captures HTML/CSS/images only.
//
// Output layout:
//   pages/<name>.html           raw server HTML (re-encoded as UTF-8)
//   pages/<name>.local.html     same page, asset refs pointing at assets/ (open offline)
//   pages/<name>.rendered.html  DOM after JavaScript ran (Playwright only)
//   assets/<host>/<path>        stylesheets (rewritten), images, fonts
//   shots/<name>-top.png, <name>-full.png (+ <name>-mobile-*.png)
//   manifest.json               merged when you run again into the same folder (to add pages)

import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

// the skill folder (scripts/..): Node resolves `import("playwright")` from here upward, so install it here
const SKILL_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const INSTALL_HELP = [
  "Install Playwright into the skill folder (once, usually under a minute; it prints little, the next run's `shots N` confirms it):",
  `  npm i --prefix "${SKILL_DIR}" playwright`,
  `  cd "${SKILL_DIR}" && npx playwright install chromium`,
  "Or rerun with --no-shots to save HTML/CSS/images without screenshots (you then cannot see the old pages).",
].join("\n");

const USAGE = `Usage:
  node scripts/snapshot.mjs <out-folder> <url|name=url> [<url|name=url> ...]
  node scripts/snapshot.mjs <out-folder> --list urls.txt
Options:
  --no-shots       skip screenshots and the rendered DOM copy (Playwright not needed)
  --width <px>     desktop viewport width (default 1440)
  --mobile         also take a 390px wide shot set
  --max-mb <n>     total download cap in MB (default 200)
  --timeout <ms>   per-request / per-navigation timeout (default 20000)`;

const UA =
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";
const CONCURRENCY = 6;
// tracking pixels / analytics beacons: pointless offline, and polite not to hit them
const TRACKER_RE = /^https?:\/\/([^/]*\.)?(facebook\.com\/tr\b|google-analytics\.com|doubleclick\.net|googletagmanager\.com)|^https?:\/\/www\.facebook\.com\/tr[/?]/i;
const RETRIES = 2;

// ---------------------------------------------------------------- args

function parseArgs(argv) {
  const o = { out: null, urls: [], list: null, shots: true, width: 1440, mobile: false, maxMb: 200, timeout: 20000 };
  const pos = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => {
      const v = argv[++i];
      if (v === undefined) fail(`missing value for ${a}`);
      return v;
    };
    if (a === "--help" || a === "-h") {
      console.log(USAGE);
      process.exit(0);
    } else if (a === "--no-shots") o.shots = false;
    else if (a === "--mobile") o.mobile = true;
    else if (a === "--list") o.list = val();
    else if (a === "--width") o.width = num(val(), a);
    else if (a === "--max-mb") o.maxMb = num(val(), a);
    else if (a === "--timeout") o.timeout = num(val(), a);
    else if (a.startsWith("--")) fail(`unknown option ${a}`);
    else pos.push(a);
  }
  if (!pos.length) fail("missing <out-folder>");
  o.out = path.resolve(pos.shift());
  o.urls = pos;
  if (o.list) {
    const txt = fs.readFileSync(o.list, "utf8");
    for (const line of txt.split(/\r?\n/)) {
      const l = line.trim();
      if (l && !l.startsWith("#")) o.urls.push(l);
    }
  }
  if (!o.urls.length) fail("no URLs given");
  return o;
}
function num(v, flag) {
  const n = Number(v);
  if (!Number.isFinite(n) || n <= 0) fail(`${flag} needs a positive number`);
  return n;
}
function fail(msg) {
  console.error(`error: ${msg}\n${USAGE}`);
  process.exit(2);
}

// ---------------------------------------------------------------- small helpers

const sha = (s) => createHash("sha1").update(s).digest("hex").slice(0, 6);
const stripHash = (u) => u.replace(/#.*$/, "");
const hashOf = (u) => (u.includes("#") ? u.slice(u.indexOf("#")) : "");
const safeDecode = (s) => {
  try {
    return decodeURIComponent(s);
  } catch {
    return s;
  }
};
const decodeEntities = (s) =>
  s.replace(/&(amp|quot|lt|gt|#39|apos);/g, (_, e) => ({ amp: "&", quot: '"', lt: "<", gt: ">", "#39": "'", apos: "'" })[e]);
const escapeAttr = (s) => s.replace(/&/g, "&amp;").replace(/"/g, "&quot;");

function resolveUrl(raw, base) {
  raw = (raw || "").trim();
  if (!raw || /^(#|data:|javascript:|mailto:|tel:|about:|blob:|sms:)/i.test(raw)) return null;
  let u;
  try {
    u = new URL(raw, base);
  } catch {
    return null;
  }
  return u.protocol === "http:" || u.protocol === "https:" ? u.href : null;
}

function makeLimiter(n) {
  let active = 0;
  const q = [];
  const next = () => {
    if (active >= n || !q.length) return;
    active++;
    const { fn, res, rej } = q.shift();
    fn().then(res, rej).finally(() => {
      active--;
      next();
    });
  };
  return (fn) =>
    new Promise((res, rej) => {
      q.push({ fn, res, rej });
      next();
    });
}

function withDeadline(p, ms, label) {
  let t;
  return Promise.race([p, new Promise((_, rej) => (t = setTimeout(() => rej(new Error(`${label} timed out`)), ms)))]).finally(() =>
    clearTimeout(t),
  );
}

const fmtMb = (b) => (b / 1048576).toFixed(2) + " MB";

// ---------------------------------------------------------------- charset / decoding

function sniffCharset(buf, contentType, isCss) {
  let cs = /charset\s*=\s*["']?([\w:.-]+)/i.exec(contentType || "")?.[1];
  if (cs) return cs;
  if (buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf) return "utf-8";
  if (buf[0] === 0xff && buf[1] === 0xfe) return "utf-16le";
  if (buf[0] === 0xfe && buf[1] === 0xff) return "utf-16be";
  const head = buf.subarray(0, 4096).toString("latin1");
  if (isCss) return /^\s*@charset\s+["']([\w-]+)["']/i.exec(head)?.[1] || null;
  const m = /<meta[^>]*?\bcharset\s*=\s*["']?([\w:.-]+)/i.exec(head);
  return m ? m[1] : null;
}

// Returns { text, charset, guessed }. Undeclared + invalid UTF-8 falls back to big5 (old Taiwanese sites).
function decodeText(buf, contentType, { isCss = false, fallback = null } = {}) {
  let cs = sniffCharset(buf, contentType, isCss) || fallback;
  let guessed = false;
  if (cs) {
    try {
      return { text: new TextDecoder(cs).decode(buf), charset: cs.toLowerCase(), guessed };
    } catch {
      cs = null;
    }
  }
  try {
    return { text: new TextDecoder("utf-8", { fatal: true }).decode(buf), charset: "utf-8", guessed };
  } catch {
    return { text: new TextDecoder("big5").decode(buf), charset: "big5", guessed: true };
  }
}

function forceUtf8Meta(html) {
  const re = /(<meta\b[^>]*?\bcharset\s*=\s*["']?)[\w:.-]+/i;
  if (re.test(html)) return html.replace(re, "$1utf-8");
  if (/<head\b[^>]*>/i.test(html)) return html.replace(/<head\b[^>]*>/i, (m) => `${m}<meta charset="utf-8">`);
  return `<meta charset="utf-8">\n${html}`;
}

// ---------------------------------------------------------------- reference scanning / rewriting
// A mapper is (kind, absUrl) => replacement string | undefined (leave as is).
// kinds: css (stylesheet / @import), image, asset (css url()), script, link (make absolute only)

const CSS_RE =
  /\/\*[\s\S]*?\*\/|@import\s+(?:url\(\s*(["']?)([^"')]+?)\1\s*\)|(["'])([^"']+)\3)|url\(\s*(["']?)((?:\\.|[^"'\\)])*?)\5\s*\)/gi;

function processCss(css, base, mapper, q = '"') {
  return css.replace(CSS_RE, (m, _q1, u1, _q2, u2, _q3, u3) => {
    if (m.startsWith("/*")) return m;
    if (m[0] === "@") {
      const abs = resolveUrl(u1 ?? u2, base);
      const r = abs && mapper("css", abs);
      return r === undefined || r === null ? m : `@import url(${q}${r}${q})`;
    }
    const abs = resolveUrl(u3, base);
    const r = abs && mapper("asset", abs);
    return r === undefined || r === null ? m : `url(${q}${r}${q})`;
  });
}

const HTML_RE =
  /<!--[\s\S]*?-->|<(script|style)\b((?:"[^"]*"|'[^']*'|[^>"'])*)>([\s\S]*?)<\/\1\s*>|<([a-zA-Z][\w:-]*)((?:"[^"]*"|'[^']*'|[^>"'])*)>/gi;
const ATTR_RE = /([^\s"'<>\/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+)))?/g;
const IMG_EXT = /\.(jpe?g|png|gif|webp|svg|bmp|avif|ico)$/i;

function scanHtml(html, base, mapper, { stripCors = false } = {}) {
  const one = (kind, val) => {
    const abs = resolveUrl(decodeEntities(val), base);
    return abs ? mapper(kind, abs) : undefined;
  };
  const srcset = (val) => {
    let changed = false;
    const out = val.split(",").map((part) => {
      const t = part.trim();
      if (!t) return part;
      const [u, ...desc] = t.split(/\s+/);
      const r = one("image", u);
      if (r === undefined) return part;
      changed = true;
      return [r, ...desc].join(" ");
    });
    return changed ? out.join(", ") : undefined;
  };
  const handle = (tag, name, val, attrs) => {
    if (name === "style") {
      const dec = decodeEntities(val);
      const r = processCss(dec, base, mapper, "'");
      return r === dec ? undefined : r;
    }
    switch (tag) {
      case "link": {
        if (name !== "href") return;
        const rel = (attrs.rel || "").toLowerCase().split(/\s+/);
        if (rel.includes("stylesheet")) return one("css", val);
        if (rel.some((r) => /^(icon|shortcut|apple-touch-icon|apple-touch-icon-precomposed|mask-icon|image_src)$/.test(r))) return one("image", val);
        if (rel.includes("preload") || rel.includes("prefetch")) {
          const as = (attrs.as || "").toLowerCase();
          if (as === "style") return one("css", val);
          if (as === "image" || as === "font") return one("asset", val);
        }
        return;
      }
      case "script":
        return name === "src" ? one("script", val) : undefined;
      case "img":
        if (["src", "data-src", "data-original", "data-lazy-src"].includes(name)) return one("image", val);
        if (name === "srcset" || name === "data-srcset") return srcset(val);
        return;
      case "source":
        if (name === "srcset" || name === "data-srcset") return srcset(val);
        if (name === "src") return /^image\//i.test(attrs.type || "") ? one("image", val) : one("link", val);
        return;
      case "video":
        if (name === "poster") return one("image", val);
        return name === "src" ? one("link", val) : undefined;
      case "input":
        return name === "src" && /^image$/i.test(attrs.type || "") ? one("image", val) : undefined;
      case "body":
      case "table":
      case "tr":
      case "td":
      case "th":
        return name === "background" ? one("image", val) : undefined;
      case "a": {
        if (name !== "href") return;
        const abs = resolveUrl(decodeEntities(val), base);
        if (!abs) return;
        return mapper(IMG_EXT.test(new URL(abs).pathname) ? "image" : "link", abs);
      }
      case "form":
        return name === "action" ? one("link", val) : undefined;
      case "iframe":
      case "audio":
      case "embed":
        return name === "src" ? one("link", val) : undefined;
      case "object":
        return name === "data" ? one("link", val) : undefined;
      default:
    }
  };
  const processAttrs = (tag, attrStr) => {
    const attrs = {};
    for (const m of attrStr.matchAll(ATTR_RE)) attrs[m[1].toLowerCase()] = m[2] ?? m[3] ?? m[4] ?? "";
    return attrStr.replace(ATTR_RE, (m, n, dq, sq, uq) => {
      // crossorigin/integrity make file:// loads fail (CORS) or break after CSS rewriting
      if (stripCors && /^(crossorigin|integrity)$/i.test(n)) return "";
      const val = dq ?? sq ?? uq;
      if (val === undefined) return m;
      const nv = handle(tag, n.toLowerCase(), val, attrs);
      return nv === undefined || nv === null || nv === val ? m : `${n}="${escapeAttr(nv)}"`;
    });
  };
  return html.replace(HTML_RE, (m, sname, sattrs, sbody, tname, tattrs) => {
    if (m.startsWith("<!--")) return m;
    if (sname) {
      const tag = sname.toLowerCase();
      const close = m.slice(m.lastIndexOf("</"));
      const body = tag === "style" ? processCss(sbody, base, mapper) : sbody;
      return `<${sname}${processAttrs(tag, sattrs)}>${body}${close}`;
    }
    return `<${tname}${processAttrs(tname.toLowerCase(), tattrs)}>`;
  });
}

// ---------------------------------------------------------------- naming

const EXT_BY_TYPE = {
  "image/jpeg": [".jpg", ".jpeg", ".jpe"],
  "image/jpg": [".jpg", ".jpeg"],
  "image/png": [".png"],
  "image/gif": [".gif"],
  "image/webp": [".webp"],
  "image/avif": [".avif"],
  "image/svg+xml": [".svg"],
  "image/x-icon": [".ico"],
  "image/vnd.microsoft.icon": [".ico"],
  "image/bmp": [".bmp"],
  "image/x-ms-bmp": [".bmp"],
  "text/css": [".css"],
  "font/woff2": [".woff2"],
  "font/woff": [".woff"],
  "font/ttf": [".ttf"],
  "font/otf": [".otf"],
  "application/font-woff": [".woff"],
  "application/font-woff2": [".woff2"],
  "application/x-font-woff": [".woff"],
  "application/x-font-ttf": [".ttf"],
  "application/vnd.ms-fontobject": [".eot"],
};

const segClean = (s) => {
  s = safeDecode(s).replace(/[^\p{L}\p{N}._\-@+~,()]/gu, "_");
  if (s === "" || /^\.+$/.test(s)) s = "_";
  if (s.length > 90) {
    const ext = path.posix.extname(s).slice(0, 10);
    s = s.slice(0, 70) + "-" + sha(s) + ext;
  }
  return s;
};

/** The manifest of an earlier run into the same folder, or null. */
function readManifest(file) {
  try {
    const m = JSON.parse(fs.readFileSync(file, "utf8"));
    return m && Array.isArray(m.pages) ? m : null;
  } catch {
    return null;
  }
}

/** Playwright's chromium, or null when neither playwright nor playwright-core can be imported. */
async function loadChromium() {
  for (const mod of ["playwright", "playwright-core"]) {
    try {
      const m = await import(mod);
      const pw = m.chromium || m.default?.chromium;
      if (pw) return pw;
    } catch {
      /* try next */
    }
  }
  return null;
}

function pageNameFromUrl(url) {
  const u = new URL(url);
  let stem = u.pathname.replace(/\/+$/, "").replace(/\.[A-Za-z0-9]{1,5}$/, "").split("/").filter(Boolean).map((s) => safeDecode(s)).join("-");
  if (!stem) stem = "index";
  const skip = /^(lang|phpsessid|sid|utm_.*|fbclid|gclid)$/i;
  const params = [...u.searchParams].filter(([k]) => !skip.test(k));
  const idp = params.find(([k]) => /^id$/i.test(k));
  const use = idp ? [idp] : params;
  let name = stem + use.map(([k, v]) => `-${k}${v.slice(0, 16)}`).join("");
  name = name.replace(/[^\p{L}\p{N}_.-]+/gu, "_").replace(/^[._-]+/, "").slice(0, 60);
  return name || "index";
}

// ---------------------------------------------------------------- main

async function main() {
  const opt = parseArgs(process.argv.slice(2));
  const out = opt.out;
  const cap = opt.maxMb * 1048576;
  const limit = makeLimiter(CONCURRENCY);
  const t0 = Date.now();

  // screenshots are what lets an AI see the old site: without Playwright stop now instead of finishing without them
  const chromium = opt.shots ? await loadChromium() : null;
  if (opt.shots && !chromium) {
    console.error(`\n${"!".repeat(72)}\nSTOPPED: screenshots need Playwright, which is not installed.\n${INSTALL_HELP}\n${"!".repeat(72)}`);
    process.exit(3);
  }

  fs.mkdirSync(out, { recursive: true });

  const writeOut = (rel, data) => {
    const parts = rel.split("/");
    if (parts.some((p) => p === ".." || p === "." || p === "")) throw new Error(`unsafe path ${rel}`);
    const abs = path.resolve(out, rel);
    if (!abs.startsWith(out + path.sep)) throw new Error(`path escapes out folder: ${rel}`);
    fs.mkdirSync(path.dirname(abs), { recursive: true });
    fs.writeFileSync(abs, data);
  };

  // ------ network
  let totalBytes = 0;
  async function fetchBuf(url, referer) {
    let lastErr = "unknown error";
    for (let attempt = 0; attempt <= RETRIES; attempt++) {
      if (attempt) await new Promise((r) => setTimeout(r, 400 * attempt));
      const ac = new AbortController();
      const timer = setTimeout(() => ac.abort(), opt.timeout);
      try {
        const res = await fetch(url, {
          redirect: "follow",
          signal: ac.signal,
          headers: {
            "user-agent": UA,
            accept: "*/*",
            "accept-language": "zh-TW,zh;q=0.9,en;q=0.8",
            ...(referer ? { referer } : {}),
          },
        });
        if (!res.ok) {
          await res.body?.cancel().catch(() => {});
          return { error: `HTTP ${res.status}`, status: res.status };
        }
        const len = Number(res.headers.get("content-length") || 0);
        if (len && totalBytes + len > cap) {
          await res.body?.cancel().catch(() => {});
          return { error: "skipped: --max-mb cap would be exceeded", status: res.status };
        }
        const buf = Buffer.from(await res.arrayBuffer());
        return { buf, status: res.status, finalUrl: res.url || url, type: (res.headers.get("content-type") || "").split(";")[0].trim().toLowerCase(), contentType: res.headers.get("content-type") || "" };
      } catch (e) {
        lastErr = ac.signal.aborted ? `timeout after ${opt.timeout}ms` : `${e.name}: ${e.cause?.code || e.message}`;
      } finally {
        clearTimeout(timer);
      }
    }
    return { error: lastErr };
  }

  // ------ asset registry
  const assets = new Map(); // key (url without #) -> entry
  const failures = [];
  const scripts = new Set();
  const usedLocal = new Map(); // local path -> key
  const tasks = new Set();
  const notes = [];
  let capHit = false;

  function assignLocal(key, kind, type) {
    const u = new URL(key);
    const host = segClean(u.host.replace(":", "_"));
    const segs = u.pathname.split("/").filter(Boolean).map(segClean);
    if (u.pathname.endsWith("/") || !segs.length) segs.push("index");
    let file = segs[segs.length - 1];
    const want = EXT_BY_TYPE[type] || (kind === "css" ? [".css"] : null);
    if (want && !want.includes(path.posix.extname(file).toLowerCase())) file += want[0];
    segs[segs.length - 1] = file;
    let local = ["assets", host, ...segs].join("/");
    const taken = (l) => {
      if (usedLocal.has(l) && usedLocal.get(l) !== key) return true;
      for (const other of usedLocal.keys()) if (other.startsWith(l + "/") || l.startsWith(other + "/")) return true;
      return false;
    };
    if (taken(local)) {
      const ext = path.posix.extname(file);
      const flat = `${file.slice(0, file.length - ext.length)}-${sha(key)}${ext}`;
      local = ["assets", host, ...segs.slice(0, -1), flat].join("/");
      if (taken(local)) local = `assets/${host}/_/${sha(key)}-${file}`;
    }
    usedLocal.set(local, key);
    return local;
  }

  function want(abs, kind, ctx) {
    const key = stripHash(abs);
    if (assets.has(key) || TRACKER_RE.test(key)) return;
    const entry = { url: key, kind, status: "pending", from: ctx.from, referer: ctx.referer, charset: ctx.charset };
    assets.set(key, entry);
    const p = limit(() => fetchAsset(entry)).catch((e) => {
      entry.status = "fail";
      failures.push({ url: key, reason: `internal: ${e.message}`, from: entry.from });
    });
    tasks.add(p);
    p.finally(() => tasks.delete(p));
  }

  function failAsset(entry, reason) {
    entry.status = "fail";
    failures.push({ url: entry.url, reason, from: entry.from });
  }

  async function fetchAsset(entry) {
    if (totalBytes >= cap) {
      capHit = true;
      return failAsset(entry, "skipped: --max-mb cap reached");
    }
    const r = await fetchBuf(entry.url, entry.referer);
    if (r.error) {
      if (r.error.includes("--max-mb")) capHit = true;
      return failAsset(entry, r.error);
    }
    if (r.type === "text/html" && !/\.html?$/i.test(new URL(entry.url).pathname)) {
      return failAsset(entry, "got text/html instead of an asset (soft 404?)");
    }
    totalBytes += r.buf.length;
    entry.bytes = r.buf.length;
    entry.type = r.type;
    entry.local = assignLocal(entry.url, entry.kind, r.type);
    entry.status = "ok";
    if (entry.kind === "css" || r.type === "text/css") {
      entry.isCss = true;
      const d = decodeText(r.buf, r.contentType, { isCss: true, fallback: entry.charset });
      entry.cssText = d.text;
      const ctx = { from: entry.from, referer: entry.url, charset: d.charset };
      processCss(d.text, r.finalUrl, (kind, abs) => {
        want(abs, kind, ctx);
      });
      entry.cssBase = r.finalUrl;
    } else {
      writeOut(entry.local, r.buf);
    }
  }

  async function drain() {
    while (tasks.size) await Promise.allSettled([...tasks]);
  }

  // ------ phase 1: pages
  const pageSpecs = [];
  const usedNames = new Set();
  for (const spec of opt.urls) {
    const m = /^([\w.\-]+)=(https?:\/\/.+)$/i.exec(spec);
    const url = m ? m[2] : spec;
    if (!/^https?:\/\//i.test(url)) {
      console.error(`skipping non-http(s) URL: ${spec}`);
      continue;
    }
    let name = m ? segClean(m[1]) : pageNameFromUrl(url);
    const baseName = name;
    for (let i = 2; usedNames.has(name); i++) name = `${baseName}-${i}`;
    usedNames.add(name);
    pageSpecs.push({ name, url });
  }

  const pages = [];
  await Promise.all(
    pageSpecs.map((spec) =>
      limit(async () => {
        const page = { name: spec.name, url: spec.url, status: null, title: null, files: [] };
        pages.push(page);
        const r = await fetchBuf(spec.url);
        if (r.error) {
          page.status = r.status ?? null;
          page.error = r.error;
          failures.push({ url: spec.url, reason: r.error, from: "page" });
          return;
        }
        page.status = r.status;
        page.finalUrl = r.finalUrl;
        totalBytes += r.buf.length;
        const d = decodeText(r.buf, r.contentType);
        page.charset = d.charset + (d.guessed ? " (guessed)" : "");
        if (d.guessed) notes.push(`${spec.name}: no charset declared and not valid UTF-8, decoded as big5`);
        page.html = d.text;
        const t = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(d.text);
        page.title = t ? decodeEntities(t[1]).replace(/\s+/g, " ").trim() : null;
        const bm = /<base\b[^>]*?\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/i.exec(d.text);
        page.base = (bm && resolveUrl(decodeEntities(bm[1] ?? bm[2] ?? bm[3]), r.finalUrl)) || r.finalUrl;
        const ctx = { from: spec.name, referer: r.finalUrl, charset: d.charset };
        scanHtml(d.text, page.base, (kind, abs) => {
          if (kind === "script") scripts.add(abs);
          else if (kind === "css" || kind === "image" || kind === "asset") want(abs, kind, ctx);
        });
      }),
    ),
  );
  pages.sort((a, b) => pageSpecs.findIndex((s) => s.name === a.name) - pageSpecs.findIndex((s) => s.name === b.name));
  await drain();

  // ------ phase 2: write CSS + pages with rewritten references
  const relFrom = (fromFile, toFile) =>
    path.posix
      .relative(path.posix.dirname(fromFile), toFile)
      .split("/")
      .map(encodeURIComponent)
      .join("/");
  const mapperFor = (fromFile) => (kind, abs) => {
    if (kind === "script" || kind === "link") return abs;
    const e = assets.get(stripHash(abs));
    if (e && e.status === "ok") return relFrom(fromFile, e.local) + hashOf(abs);
    return abs;
  };

  for (const e of assets.values()) {
    if (e.status !== "ok" || !e.isCss) continue;
    let css = processCss(e.cssText, e.cssBase, mapperFor(e.local));
    css = css.replace(/^(\s*@charset\s+)["'][\w-]+["']/i, '$1"utf-8"');
    writeOut(e.local, css);
    delete e.cssText;
  }

  for (const p of pages) {
    if (!p.html) continue;
    const rawRel = `pages/${p.name}.html`;
    const localRel = `pages/${p.name}.local.html`;
    writeOut(rawRel, forceUtf8Meta(p.html));
    let local = scanHtml(p.html, p.base, mapperFor(localRel), { stripCors: true });
    local = local.replace(/<base\b[^>]*>/i, "<!-- base removed in local copy -->");
    writeOut(localRel, forceUtf8Meta(local));
    p.files.push(rawRel, localRel);
    delete p.html;
  }

  // ------ screenshots (optional)
  const shotFiles = [];
  let shotNote = null;
  const okPages = pages.filter((p) => p.files.length);
  if (chromium && okPages.length) {
    {
      let browser;
      try {
        browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
      } catch (e) {
        shotNote = `screenshots skipped: browser failed to launch (${String(e.message).split("\n")[0]}); run: cd "${SKILL_DIR}" && npx playwright install chromium`;
        console.log(shotNote);
      }
      if (browser) {
        const sets = [{ tag: "", width: opt.width, height: 900, mobile: false }];
        if (opt.mobile) sets.push({ tag: "-mobile", width: 390, height: 844, mobile: true });
        for (const p of okPages) {
          for (const set of sets) {
            const ctx = await browser.newContext({
              viewport: { width: set.width, height: set.height },
              isMobile: set.mobile,
              deviceScaleFactor: 1,
              locale: "zh-TW",
            });
            const pg = await ctx.newPage();
            pg.setDefaultTimeout(opt.timeout);
            try {
              await withDeadline(
                (async () => {
                  await pg.goto(p.url, { waitUntil: "domcontentloaded", timeout: opt.timeout });
                  await pg.waitForLoadState("networkidle", { timeout: opt.timeout }).catch(() => {});
                  const top = `shots/${p.name}${set.tag}-top.png`;
                  fs.mkdirSync(path.join(out, "shots"), { recursive: true });
                  await pg.screenshot({ path: path.join(out, top) });
                  shotFiles.push(top);
                  p.files.push(top);
                  await pg.evaluate(async () => {
                    const step = Math.max(300, Math.floor(innerHeight * 0.8));
                    let y = 0;
                    for (let i = 0; i < 80; i++) {
                      window.scrollTo(0, y);
                      await new Promise((r) => setTimeout(r, 150));
                      if (y + innerHeight >= document.documentElement.scrollHeight) break;
                      y += step;
                    }
                    window.scrollTo(0, 0);
                  });
                  await pg.waitForLoadState("networkidle", { timeout: Math.min(opt.timeout, 5000) }).catch(() => {});
                  await pg.waitForTimeout(300);
                  const full = `shots/${p.name}${set.tag}-full.png`;
                  await pg.screenshot({ path: path.join(out, full), fullPage: true });
                  shotFiles.push(full);
                  p.files.push(full);
                  if (!set.mobile) {
                    const rel = `pages/${p.name}.rendered.html`;
                    writeOut(rel, await pg.content());
                    p.files.push(rel);
                  }
                })(),
                opt.timeout * 4,
                "screenshot step",
              );
            } catch (e) {
              failures.push({ url: p.url, reason: `screenshot${set.tag}: ${String(e.message).split("\n")[0]}`, from: p.name });
            } finally {
              await ctx.close().catch(() => {});
            }
          }
        }
        await browser.close().catch(() => {});
      }
    }
  }

  // ------ manifest
  const assetMap = {};
  let assetBytes = 0;
  for (const e of assets.values()) {
    if (e.status !== "ok") continue;
    assetMap[e.url] = { path: e.local, bytes: e.bytes, contentType: e.type };
    assetBytes += e.bytes;
  }
  // a second run into the same folder (pages added later) merges into the existing manifest instead of replacing it
  const prev = readManifest(path.join(out, "manifest.json"));
  const names = new Set(pages.map((p) => p.name));
  const run = {
    generated: new Date().toISOString(),
    options: { width: opt.width, mobile: opt.mobile, shots: opt.shots, maxMb: opt.maxMb, timeout: opt.timeout },
    pagesRequested: pages.length,
    pages: okPages.length,
    shots: shotFiles.length,
    downloadedBytes: totalBytes,
    capHit,
    seconds: Math.round((Date.now() - t0) / 1000),
  };
  const allPages = [
    ...(prev?.pages || []).filter((p) => !names.has(p.name)),
    ...pages.map((p) => ({ name: p.name, url: p.url, finalUrl: p.finalUrl, status: p.status, title: p.title, charset: p.charset, files: p.files })),
  ];
  const allAssets = { ...(prev?.assets || {}), ...assetMap };
  const now = new Set(failures.map((f) => f.url));
  const allFailures = [...(prev?.failures || []).filter((f) => !now.has(f.url) && !(f.url in assetMap) && !(f.from && names.has(f.from))), ...failures];
  const allScripts = [...new Set([...(prev?.scripts || []), ...scripts])];
  const manifest = {
    generated: run.generated,
    runs: [...(prev?.runs || (prev ? [{ generated: prev.generated, pagesRequested: prev.totals?.pagesRequested, pages: prev.totals?.pages }] : [])), run],
    pages: allPages,
    assets: allAssets,
    failures: allFailures,
    scripts: allScripts,
    totals: {
      pages: allPages.filter((p) => p.files?.length).length,
      pagesRequested: allPages.length,
      assets: Object.keys(allAssets).length,
      assetBytes: Object.values(allAssets).reduce((n, a) => n + (a.bytes || 0), 0),
      downloadedBytes: totalBytes,
      failures: allFailures.length,
      scripts: allScripts.length,
      shots: allPages.reduce((n, p) => n + (p.files || []).filter((f) => f.startsWith("shots/")).length, 0),
      capHit,
      seconds: run.seconds,
    },
  };
  if (shotNote) manifest.notes = [shotNote, ...notes];
  else if (notes.length) manifest.notes = notes;
  fs.writeFileSync(path.join(out, "manifest.json"), JSON.stringify(manifest, null, 2));

  // ------ summary
  const t = manifest.totals;
  console.log(`\nSnapshot -> ${out}`);
  for (const p of pages) console.log(`  ${p.files.length ? "ok  " : "FAIL"} ${p.name}  [${p.status ?? p.error}]  ${p.title || ""}`);
  console.log(`this run: pages ${run.pages}/${run.pagesRequested}, shots ${run.shots}, ${fmtMb(totalBytes)} downloaded, failures ${failures.length}, ${run.seconds}s`);
  if (prev) console.log(`merged into the existing manifest.json: ${t.pages} pages in the folder now`);
  console.log(`folder: pages ${t.pages}/${t.pagesRequested}, assets ${t.assets} (${fmtMb(t.assetBytes)}), scripts listed ${t.scripts}, shots ${t.shots}, failures ${t.failures}`);
  if (opt.shots && !run.shots) console.log(`\n${"!".repeat(72)}\nWARNING: NO SCREENSHOTS were taken. ${shotNote || ""}\n${"!".repeat(72)}`);
  if (capHit) console.log(`WARNING: --max-mb ${opt.maxMb} cap reached, some assets were not downloaded`);
  for (const f of failures.slice(0, 15)) console.log(`  fail: ${f.url}  (${f.reason})`);
  if (failures.length > 15) console.log(`  ... ${failures.length - 15} more in manifest.json`);
  process.exit(run.pages ? 0 : 1);
}

main().catch((e) => {
  console.error(`fatal: ${e.stack || e.message}`);
  process.exit(1);
});
