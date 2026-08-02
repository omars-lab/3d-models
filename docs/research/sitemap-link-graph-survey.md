<!--
  Provenance
  ----------
  Date:        2026-08-02
  Produced by: a general-purpose research subagent, run from the 3d-models repo with
               web access and read access to 3d-models (master + gh-pages), bikar, and
               the live deployments. Six proof-of-concept implementations were built
               and run in a scratchpad; both repos and the gh-pages branch were left
               unmodified (`git status --porcelain` clean at the end, gh-pages read via
               `git show` / `git archive` and never checked out).
  Feeds:       docs/site-graph.json (the checked-in edge list and host exposures)
               docs/site-graph.md   (the rendered graph)
               .claude/gates/site_graph.py (the gate, POC E productionized)
  Question:    Is there a standardized way to describe a site's pages and the links
               between them, and what should this repo do about its cross-linked URLs?
  Answer:      No standard exists for a link graph. Do not add a link checker — every
               crawler run reported this repo's one live defect as green, because
               Cloudflare Access answers an unauthenticated request with HTTP 200.

  Preserved verbatim below, per CLAUDE.md's "Research is checked in" rule. Scratchpad
  paths named in §8 are gone; they are recorded so the measurements are attributable,
  not so they can be re-run in place.
-->

All POCs complete, both repos unmodified. Here is the deliverable.

---

# Sitemap and link-graph standards — survey and inventory

**Scope note / correction to the brief.** Two premises in the task turned out to be wrong on inspection and are corrected here: (1) `docs/gallery.html` **does not exist** — `git log --all -- '*gallery.html'` returns empty and `git ls-files | grep -i gallery` is empty; the gallery index is `3d-models/index.html`, tracked on `master` and deployed via `Makefile:35`. (2) `packages/web/vite.config.ts:541-543` has **three** Rollup inputs (`main`, `editor`, `sessions`), not four — `404.html` ships from `packages/web/public/` and is deliberately outside the input map.

---

## 1. Standards that exist (and what each does not express)

### 1.1 The sitemap: a real, adopted standard — and a flat list with no edges

**Confirmed from the spec, plainly: an XML sitemap cannot express a link between two pages.** The entire content vocabulary of https://www.sitemaps.org/protocol.html is `<urlset>`, `<url>`, `<loc>`, `<lastmod>`, `<changefreq>`, `<priority>` (plus `<sitemapindex>`/`<sitemap>`/`<loc>`/`<lastmod>` for index files). There is no element for a link, an edge, a parent, a child, a section, or navigation. The spec's own conformance list is exhaustive and ends *"All other tags are optional."* The only nesting is the container relation `<urlset>` → `<url>` → `<loc>`, which carries no semantics about how pages relate. `<priority>` is the closest thing to structure and is explicitly disclaimed: *"it only lets the search engines know which pages you deem most important for the crawlers."*

The only extension mechanism is DIY: *"You can extend the Sitemaps protocol using your own namespace."* Google's news/image/video extensions use it; none of them add edges.

**Sitemap index files are a file-of-files, not a hierarchy.** `<sitemapindex>` *"Encapsulates information about all of the Sitemaps in the file"*; `<sitemap>` *"Encapsulates information about an individual Sitemap."* The nesting is index → sitemap-file → URL, i.e. a partition of one URL list across files for size reasons. It cannot recurse into page structure.

**Size limits, confirmed:** *"each Sitemap file that you provide must have no more than 50,000 URLs and must be no larger than 50MB (52,428,800 bytes) … the sitemap file once uncompressed must be no larger than 50MB."* Index files: no more than 50,000 sitemaps, same 50MB.

**Cross-host — the strict part, and directly relevant to us:**

> *"The location of a Sitemap file determines the set of URLs that can be included in that Sitemap. … **Note that this means that all URLs listed in the Sitemap must use the same protocol (http, in this example) and reside on the same host as the Sitemap.** … URLs that are not considered valid are dropped from further consideration."*

Scheme mismatch alone disqualifies a URL — the spec's own example marks an `https://` entry invalid inside an `http://` sitemap. Index files inherit the restriction: *"A Sitemap index file can only specify Sitemaps that are found on the same site as the Sitemap index file."*

The one sanctioned cross-host route is the **cross-submit**: put `Sitemap: https://other-host/sitemap-thishost.xml` in *this* host's `robots.txt` as ownership proof. Even then, *"it is expected that … all the URLs belong to the host pointing to it."* Google (https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) is materially looser — it documents multi-domain sitemaps gated on Search Console verification *or* a robots.txt entry per host — and drops two elements outright: **"Google ignores `<priority>` and `<changefreq>` values."**

### 1.2 `robots.txt` `Sitemap:` — **not in RFC 9309**

Honest finding, verified against https://www.rfc-editor.org/rfc/rfc9309.txt: RFC 9309 (Robots Exclusion Protocol, 2022) formally defines exactly three fields — `user-agent`, `allow`, `disallow`. `Sitemap:` appears only in §2.2.4 "Other Records" as an *example of something the RFC does not define*:

> *"Crawlers MAY interpret other records that are not part of the robots.txt protocol -- for example, 'Sitemaps' [SITEMAPS]. … Parsing of other records MUST NOT interfere with the parsing of explicitly defined records."*

Its normative home is sitemaps.org plus vendor docs. Google's robots spec documents `sitemap: [absoluteURL]` and — load-bearing for us — **"The URL doesn't have to be on the same host as the robots.txt file."**

### 1.3 The link graph: no standard exists, and the one that did was deleted

**HTML4 had a genuine site-structure vocabulary** (https://www.w3.org/TR/html401/types.html): `Start`, `Next`, `Prev`, `Contents`, `Index`, `Chapter`, `Section`, `Subsection`, `Appendix`. Sequence *and* hierarchy *and* TOC pointers. **This is the high-water mark for standardized link-graph description in HTML, and it was reached in 1999.**

**WHATWG HTML today defines 26 link keywords**, extracted from the raw https://html.spec.whatwg.org/multipage/links.html#linkTypes table: `alternate, canonical, author, bookmark, dns-prefetch, expect, external, help, icon, manifest, modulepreload, license, next, nofollow, noopener, noreferrer, opener, pingback, preconnect, prefetch, preload, prev, privacy-policy, search, stylesheet, tag, terms-of-service`.

**Dropped and absent: `up`, `index`, `contents`, `chapter`, `section`, `subsection`, `start`, `first`, `last`, `glossary`, `appendix`.** The removal is datable — WHATWG commit r5924, `ianh`, 2011-03-01 (https://lists.whatwg.org/pipermail/commit-watchers-whatwg.org/2011/012791.html): *"Drop support for rel=up, rel=last, rel=index, rel=first, and any related synonyms."* The diff deletes the entire `#hierarchical-link-types` section. It was killed by design, not neglect — the only consumers those keywords ever had were the Mozilla Site Navigation Bar and Opera Presto's equivalent, both long removed.

**Registration confers nothing.** WHATWG delegates extensions to the microformats wiki: *"Anyone is free to edit the microformats page for existing rel values at any time to add a type."* The force of registration is conformance permission to write the attribute — **no behavior is required of any user agent.** The IANA registry (https://www.iana.org/assignments/link-relations/link-relations.xhtml) still lists `up` ("Refers to a parent document in a hierarchy of documents", RFC 8288), `index`, `contents`, `start`, `chapter`, `section`, `first`, `last` — so **these are IANA-registered but not HTML-conforming, and no browser or crawler acts on them.** There is no registered `rel="sitemap"`.

**`rel=next`/`prev` as an indexing signal is retired at Google**, verified from Google's own current docs (https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading): **"Google no longer uses these tags, although these links may still be used by other search engines."** Its recommended replacement is an ordinary `<a href>` — i.e. *infer the graph by crawling it, don't declare it*.

### 1.4 `rel=canonical` / `hreflang` — identity, not structure (but explicitly cross-host)

RFC 6596 (https://www.rfc-editor.org/rfc/rfc6596.txt, Informational, 2012) §3: *"The target (canonical) IRI **MUST** identify content that is either duplicative or a superset of the content at the context (referring) IRI."*

That MUST is why canonical is **not** a graph edge. You cannot say "B is the parent of A" without violating it. Canonical *removes* nodes (collapses duplicate identities) rather than adding edges. It is however unambiguously cross-host — §3: *"The target (canonical) IRI MAY: … **Exist on a different hostname or domain**"*, and may also differ in scheme. Google confirmed support (https://developers.google.com/search/blog/2009/12/handling-legitimate-cross-domain): *"While the rel='canonical' link element is seen as a hint and not an absolute command, we do try to follow it where possible."*

`hreflang`/`rel=alternate` is likewise a symmetric *equivalence* assertion over the same content, cross-domain-legal, and not a navigational edge.

### 1.5 schema.org — one consumed type, and it's a path not a graph

| Type | Status | Consumed by |
|---|---|---|
| `SiteNavigationElement` | Defined (V30.0, 2026-03-19). Full definition: *"A navigation element of the page."* **No properties of its own.** | **Nobody.** Absent from Google's supported-features gallery (https://developers.google.com/search/docs/appearance/structured-data/search-gallery). No primary doc from any consumer was found. |
| `BreadcrumbList` | *"an ItemList consisting of a chain of linked Web pages … typically ending with the current page"* | **Google** — the only structural type it consumes |
| `WebSite` / `WebPage` + `hasPart`/`isPartOf` | Expressive enough for arbitrary containment | Nothing in Google's list. The `WebSite` sitelinks search box was retired Oct 2024. |

`BreadcrumbList` is **one ordered ancestor chain per page**. It cannot express siblings, cross-links, or multiple parents within one list.

### 1.6 Everything else, and what's dead

- **`<nav>`** marks *where* navigation is, not what the structure *is*: *"a section with navigation links."* You still have to crawl the `<a href>`s.
- **WAI-ARIA** relationship attributes (`aria-owns`, `aria-controls`, `aria-flowto`, `aria-current`) reference elements by ID and operate **only within a single document**. No cross-document vocabulary.
- **Web App Manifest** (https://www.w3.org/TR/appmanifest/) gives `start_url` + `scope` (a URL-prefix containment test) + a flat `shortcuts` list. Entry point, boundary, deep links — no hierarchy.
- **`.well-known` (RFC 8615)**: there is **no registered suffix** for a sitemap, site structure, navigation, page inventory, `llms.txt` or `ai.txt`. Nearest neighbour is `resourcesync`, which is itself built on sitemaps.org XML.
- **llms.txt** (https://llmstxt.org/, Jeremy Howard, 2024-09-03): a required H1, optional summary, then H2-delimited markdown link lists. **Flat, hand-curated, no edges** — one level of categorical grouping more than a sitemap, still not a graph. Self-described as "A proposal"; no standards body has adopted it. *(Reported non-adoption by Google and single-digit uptake figures: **unverified snippet**, SEO-blog sourced only.)*
- **No W3C/WHATWG/IETF working group, past or present, has a deliverable that is a machine-readable description of a website's link graph.** That is the central negative finding.

| Want to express | Standard? | Consumed by |
|---|---|---|
| Flat inventory of pages | **Yes** — sitemaps.org XML | All major crawlers |
| "This page duplicates that one" | **Yes** — RFC 6596 canonical (cross-host OK) | Google (as a hint) |
| Ancestor chain of one page | **Yes** — `BreadcrumbList` | Google |
| "B is the parent of A" | **Dropped from HTML, 2011-03-01** | Nobody |
| Sequence of pages | `rel=next`/`prev` still in HTML | **Not Google** |
| **Arbitrary link graph / edge list** | **None exists** | — |

---

## 2. Tooling that emits a machine-readable link graph

Only four surveyed tools emit a real `source → target` edge in a file. Screaming Frog emits edges too, but only as CSV — **its famous crawl-map visualisation exports as HTML or SVG only**, no GraphML/GEXF/Gephi; the widely-described Gephi workflow bypasses the visualisation entirely via `Bulk Export > All Inlinks`. Sitebulb is the same story.

| Tool | Consumes | Emits | Offline? | Multi-host? | Cost | Maintained |
|---|---|---|---|---|---|---|
| **linkinator** | live URLs **and** local paths/globs; serves `dist/` itself | JSON + CSV `url,status,state,parent,failureDetails` | **Yes** | Checks off-host links; `--recurse` follows same root domain only | MIT | **Yes** — 8.0.3, 2026-07-30 |
| **linkchecker** | `http(s)://` **and** `file:` dirs | `-o dot` / `-o gml` — true edge output | **Yes** | External not checked without `--check-extern` | GPL-2.0 | v10.6.0 (2025-07-28), repo active |
| **lychee** | files, globs, URLs, stdin | `--format json`: `success_map`/`error_map` keyed by source, with `span{line,column}` | **Yes** (`--offline`) | N/A — **does not crawl** (own feature table: Recursion: no) | Apache-2.0/MIT | **Yes** — 0.24.2 |
| **muffet** | live URL only | `--format json` adjacency list | **No** | one host | MIT | Yes — 2.11.5 |
| **Screaming Frog** | live crawl / List mode (URLs must carry `http`) | All Inlinks/Outlinks CSV. Visualisations: **HTML or SVG only** | **No** | Yes | Free ≤500 URLs; ~$279/yr | Yes |
| **hyperlink** | folder of HTML | text errors; `dump-external-links` (**no source recorded**) | Yes | dump only | MIT | 0.3.2 |
| **htmltest** | local HTML dir | text + external status cache | Yes | checks external | MIT | **No** — v0.17.0, 2022-11 |
| **broken-link-checker (`blc`)** | HTML/URLs | **no machine-readable CLI output** | partly | yes | MIT | **Dead** — npm 0.7.8, **2018-03-13** |
| **wget --spider** | live URL | **nothing structured.** No option records which page a URL was found on | mirrors, doesn't emit | `-H` | GPL | Yes |
| **remark-validate-links** | local markdown in git | vfile diagnostics — **no edge list** | Yes | local links only | MIT | 13.1.0 |
| **next-sitemap / @astrojs/sitemap / sitemap** | build output | `sitemap.xml` only — **nodes, never edges** | Yes | N/A | MIT | astro/sitemap active; **next-sitemap last 2023-09** |
| **Rollup/Vite module graph** | JS/TS modules | `getModuleInfo().importedIds` | Yes | N/A | MIT | Yes |

**Three findings worth stating plainly:**

- **Rollup's module graph is not a page graph.** `ModuleInfo.importedIds` is "the module ids statically imported by this module" — ESM resolution, not `<a href>`. A Vite plugin can see `about.js` imports `nav.js`; it cannot see `/about` links to `/contact`. There is no href-level build graph to tap.
- **linkchecker's DOT keys nodes by page *title*, not URL** (`write_edge` emits `"{title or name}" -> ...`). Two pages sharing a `<title>` collapse into one node. Its GML logger is safer (integer ids + `url` attribute). Both loggers derive from a single `parent_url` per node, so you get a **spanning tree of first discovery, not the complete multigraph**. I reproduced both defects — see §8.4.
- **lychee's JSON is a link graph its own docs never show you.** The published Output Modes page documents only color/plain/emoji; the schema is pinned in the repo's formatter test. And per its source comment, *"`success_map` … remain empty if detailed statistics are disabled"* — without verbose output you get only broken edges. **No npm distribution exists** (`lychee-bin` and `@lycheeverse/lychee` are both npm 404 — verified, §8.4); it needs cargo or a package manager.

**Graph interchange formats**

| Format | Spec | Verdict for a <50-node graph in git |
|---|---|---|
| **Plain JSON edge list** | none | Lowest ceremony, best diffs, zero parse dependency; every other format generates from it in ten lines. |
| **Mermaid flowchart** | https://mermaid.js.org/syntax/flowchart.html | **The only format GitHub renders inline** (https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams — verified). |
| **DOT / Graphviz** | https://graphviz.org/doc/info/lang.html | One line per edge, diffable, `dot -Tsvg`. Not rendered by GitHub. |
| **GraphML** | http://graphml.graphdrawing.org/ *(spec content unverified — the site's TLS cert is misissued for `graphml.ethz.ch` and HTTPS fetch fails)* | Verbose XML, noisy diffs. Only if handing data to yEd/Gephi/NetworkX. |
| **GEXF** | https://gexf.net/ (v1.2, Gephi project) | Built for *dynamic* networks. Overkill. |
| **Cytoscape JSON** | https://js.cytoscape.org/#notation/elements-json | Pure JSON, verbose per edge, loadable by cytoscape.js. |
| **D2** | https://d2lang.com/ | MPL-2.0, v0.7.1 (2025-08). Nicer than DOT, smaller ecosystem, no GitHub rendering. |

---

## 3. The multi-host / same-content-two-hostnames problem

**Our exact case:** `bikar-studio.pages.dev` and `bikar.naqshcoffee.com` serve identical bytes from one Cloudflare Pages deployment, plus an unbounded set of `<hash>.bikar-studio.pages.dev` per-deployment aliases. `packages/web/public-surface.json:39-50` records this and its consequence: *"Every deployment gets a permanent per-deployment alias … Pages keeps serving it after the deployment stops being current. Measured 2026-08-01: `https://a7e934b1.bikar-studio.pages.dev/editor` returned 200. These are a third surface … putting Access in front of the other two would not touch them."*

**The standard answer is `rel="canonical"`, and it is the *only* widely-consumed relation that is cross-host by spec.** RFC 6596 §3 explicitly permits a different hostname or domain; Google confirmed cross-domain support in 2009. `bikar.naqshcoffee.com` and every `<hash>.` alias should carry `<link rel="canonical" href="https://bikar-studio.pages.dev/...">` (or the reverse, whichever is the intended public identity). **Note what this does and does not buy:** it deduplicates identity for search engines. It does not make either host reachable, does not express any edge, and no tool in §2 consumes it.

**Sitemaps cannot span our hosts.** A sitemap at `blog.bytesofpurpose.com` may not list `bikar-studio.pages.dev` URLs — same-host, same-scheme, path-prefix-scoped. Two sitemaps minimum, or a robots.txt cross-submit per host. My generator in §8.5 emits two files for exactly this reason.

**Tool capability against a cross-origin graph:**

| Tool | Cross-origin behaviour |
|---|---|
| linkinator | `--recurse` follows *"the same root domain"* only. Off-host links are **checked as leaves, never expanded.** Confirmed empirically (§8.3): two crawls produced two disconnected graphs. |
| linkchecker | `--check-extern` checks external links; recursion still bounded. Same leaf behaviour. |
| Screaming Frog / Sitebulb | Configurable external crawl — the only tools that *can* genuinely crawl both hosts in one project. Neither works offline; neither can reach a host behind Cloudflare Access without a service token. |
| lychee | No crawl at all — cross-origin is moot. |
| muffet / wget | Single-host in practice. |

**And the finding that dominates all of them:** none of these tools can distinguish "this cross-host link works" from "this cross-host link lands on a login wall." Measured in §8.3 and §8.4 — every crawler reported the Access-gated edge as OK/200/`valid=1`.

---

## 4. Inventory: pages by surface

Live status verified 2026-08-02 by `curl -o /dev/null -w '%{http_code} -> %{redirect_url}'`.

| Page file | Built by | Catalogued in | Host(s) | Live URL | Status |
|---|---|---|---|---|---|
| `3d-models/index.html` | none (hand-written, tracked on `master`) | **NO catalog** — only `Makefile:35 DEPLOY_PATHS` | blog.bytesofpurpose.com; omars-lab.github.io (301) | `http://blog.bytesofpurpose.com/3d-models/` | 200 |
| `studio.html` | bikar `packages/lab` (vite) | lab `catalog.ts:148` (`live`) | same | `…/3d-models/studio.html` | 200 |
| `lab.html` | bikar `packages/lab` | lab `catalog.ts:157` (`live`) | same | `…/3d-models/lab.html` | 200 |
| `lego.html` | bikar `packages/lab` | lab `catalog.ts:177` (`live`) | same | `…/3d-models/lego.html` | 200 |
| `design.html` | bikar `packages/lab` | lab `catalog.ts:197` (**`preview`**) | same | `…/3d-models/design.html` | 200 — **orphaned without JS**, see §6 |
| `index.html` | bikar `packages/web` (`vite.config.ts:541`) | web `catalog.ts:143` (`LANDING`) | bikar-studio.pages.dev **and** bikar.naqshcoffee.com **and** `*.bikar-studio.pages.dev` | `https://bikar-studio.pages.dev/` | 200 |
| `editor.html` | bikar `packages/web` (`:542`) | web `catalog.ts:86` | same three | `…/editor` | 200 |
| `sessions.html` | bikar `packages/web` (`:543`) | web `catalog.ts:97` | same three | `…/sessions` | 200 |
| `404.html` | bikar `packages/web/public/` | **NO catalog** — not a Rollup input | same three | `…/404.html` | served (`/nope` → 404) |

**Built but deployed nowhere:** all four of `packages/lab/dist/{studio,lab,lego,design}.html`. `packages/lab` has no deploy step in bikar; `3d-models/Makefile:146-168` (`LAB_PAGES` + `lab-vendor`) copies them into the gallery docroot. They exist on disk at `/Users/omareid/Workspace/git/bikar/packages/lab/dist/` and are served only after vendoring.

**Deployed but not in its build's catalog:** `404.html`. Benign and deliberate — `packages/web/tests/catalog.test.ts` pins catalog ↔ Rollup inputs, and `404.html` is outside both by design (`public/404.html:5-12` explains why its existence is the fix). Flagged because the ask requires it, not as a defect.

**Alias chain, measured:**
- `https://omars-lab.github.io/3d-models/` → **301** → `http://blog.bytesofpurpose.com/3d-models/` (note: redirects to **http**, not https; https also serves 200)
- `https://bikar.naqshcoffee.com/` → **302** → `https://naqshcoffee.cloudflareaccess.com/cdn-cgi/access/login/...`
- `https://3d-models.bytesofpurpose.com/` → **NXDOMAIN** (`nslookup`: *"server can't find … NXDOMAIN"*)

**No `CNAME`, `robots.txt`, `sitemap.xml` or `.nojekyll` on the `gh-pages` branch** — `git ls-tree -r --name-only gh-pages` (192 files) contains none. Both live robots.txt files are Cloudflare's edge-injected content-signals policy. The blog host's carries `Sitemap: https://blog.bytesofpurpose.com/sitemap.xml`, which returns 200 — and **contains zero `/3d-models/` URLs** (`curl … | grep -c '3d-models'` → `0`). All five gallery pages are absent from the only sitemap covering their host.

---

## 5. Inventory: edge list

Every row read out of a file. `gh-pages:` rows via `git --no-pager show gh-pages:<path>` — no branch checkout.

### 5.1 Source-of-truth edges (bikar + 3d-models `master`)

| # | From | To | `file:line` | Visibility |
|---|---|---|---|---|
| 1 | gallery index | `studio.html` | `3d-models/index.html:270` | static |
| 2 | gallery index | `lab.html` | `3d-models/index.html:304` | static |
| 3 | gallery index | `lego.html` | `3d-models/index.html:322` | static |
| 4 | gallery index | `https://bikar.naqshcoffee.com` | `3d-models/index.html:277` | static — **defect, §6.1** |
| 5 | gallery index | `https://github.com/omars-lab/3d-models` ×2 | `3d-models/index.html:278,339` | static |
| 6 | gallery index | `lab.html?v=1&f=…` ×11 | `3d-models/index.html:397-437` + renderer `:512` | JS-computed |
| 7 | gallery index | `lego.html?v=1&f=…` ×7 | `3d-models/index.html:453-477` + `:512` | JS-computed |
| 8 | gallery index | `…/blob/master/src/**` ×35 | `3d-models/index.html:352` (`const GH`) + `:510` | JS-computed |
| 9 | gallery index | `build/stls/*.stl` ×35 | `3d-models/index.html:511` | JS-computed |
| 10 | `lab.html` | `./studio.html` | `bikar packages/lab/lab.html:22` | static |
| 11 | `lab.html` | `./index.html` | `bikar packages/lab/lab.html:23` | static — see §6.4 |
| 12 | `lego.html` | `./studio.html` | `bikar packages/lab/lego.html:23` | static |
| 13 | `lego.html` | `./index.html` | `bikar packages/lab/lego.html:24` | static — see §6.4 |
| 14 | `lab.html` | `https://bikar-studio.pages.dev/editor#code/…` | `bikar packages/lab/src/editor.ts:22` via `src/main.ts:323` | JS-computed — **§6.3** |
| 15 | `lego.html` | same | `editor.ts:22` via `src/lego-main.ts:423` | JS-computed — **§6.3** |
| 16 | `studio.html` | `./lab.html`, `./lego.html`, `./design.html` | `bikar packages/lab/src/studio-main.ts:56` (cards) and `:78` (actor rows) | JS-computed |
| 17 | `design.html` | `./studio.html`, `./lego.html`, `./lab.html` | `bikar packages/lab/src/design-main.ts:39` | JS-computed |
| 18 | `design.html` | `./design.html` ×3 | `bikar packages/lab/src/design-main.ts:50,62,79` | JS-computed |
| 19 | studio `/` | `/editor` | `bikar packages/web/src/catalog.ts:91` → `dist/index.html:100` | static (built) |
| 20 | studio `/` | `/sessions` | `bikar packages/web/src/catalog.ts:102` → `dist/index.html:106` | static (built) |
| 21 | studio `/` | `https://blog.bytesofpurpose.com/3d-models/` | `bikar packages/web/src/catalog.ts:110` → `dist/index.html:111` | static (built) |
| 22 | studio `/` | `…/3d-models/lab.html` | `bikar packages/web/src/catalog.ts:119` → `dist/index.html:117` | static (built) |
| 23 | studio `/` | `…/3d-models/lego.html` | `bikar packages/web/src/catalog.ts:128` → `dist/index.html:123` | static (built) |
| 24 | `/editor` | `/` | `bikar packages/web/editor.html:26` | static |
| 25 | `/sessions` | `/` | `bikar packages/web/sessions.html:161` | static |
| 26 | `/404.html` | `/`, `/editor`, `/sessions` | `bikar packages/web/public/404.html:81,82,83` | static |
| 27 | `/sessions` | `/sessions/{name}/`, `/sessions/{name}/{n}` | `bikar packages/web/src/sessions.ts:178,210`; `src/main.ts:4331` | JS-computed |
| 28 | card renderer | `esc(page.href)` | `bikar packages/web/src/landing-cards.ts:44` | build-time template |

### 5.2 Edges baked into the deployed `gh-pages` bytes

| # | From | To | `file:line` |
|---|---|---|---|
| 29 | `gh-pages:index.html` | `studio.html` / `bikar.naqshcoffee.com` / github ×2 / `lab.html` / `lego.html` | `gh-pages:index.html:270, 277, 278, 304, 322, 339` |
| 30 | `gh-pages:lab.html` | `./studio.html`, `./index.html` | `gh-pages:lab.html:27, 28` |
| 31 | `gh-pages:lego.html` | `./studio.html`, `./index.html` | `gh-pages:lego.html:30, 31` |
| 32 | **`gh-pages:assets/style-BFfxPe7x.js`** | `https://bikar-studio.pages.dev/editor` | `gh-pages:assets/style-BFfxPe7x.js:3` — the **only** cross-host URL surviving minification; shared chunk loaded by both `lab.html` and `lego.html` |
| 33 | `gh-pages:assets/design-YI2JBonM.js` | `./lab.html`, `./lego.html`, `./studio.html`, `./design.html` ×3 | `:778, :789, :797, :809` |
| 34 | `gh-pages:assets/studio-7nKoSMTR.js` | **nothing extractable** | `"./"+X(e.file)` — string concatenation, so no URL literal exists in the bundle at all |
| 35 | `gh-pages:README.md:7` | `https://3d-models.bytesofpurpose.com/` | **NXDOMAIN — §6.2** |
| 36 | `gh-pages:README.md:105` | `https://omars-lab.github.io/3d-models/` | 301 (works) |

### 5.3 Cross-host URLs in deployed studio bundles (found only by scanning JS)

| From | To | `file:line` |
|---|---|---|
| `packages/web/dist/assets/sessions-CEysmZu7.js` | **`http://localhost:8731`** | `:1` — a localhost URL shipped in a public bundle |
| `packages/web/dist/assets/ch-widgets-DhMbpkqX.js` | `https://gmwmrcmfywsdescglijg.supabase.co` | `:7` |
| `packages/web/dist/assets/canvas-comments-BP_IFsFC.js` | `https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/…` | `:7` |

*(Not link-graph defects — noted because a whole-bundle URL scan is part of the recommended extractor and these are what it surfaces.)*

---

## 6. Defects found

### 6.1 The gallery's return edge lands on a login wall — `3d-models/index.html:277`

```html
<span><b>Grammar</b> <a href="https://bikar.naqshcoffee.com" target="_blank" rel="noopener">bikar studio ↗</a> <em>sign-in</em></span>
```

`packages/web/public-surface.json:53-56` declares that host `exposure: "access"`, `accessTeam: naqshcoffee.cloudflareaccess.com`, and requires: *"An unauthenticated GET must be answered by the login redirect, never by our HTML."* Measured: **302 → cloudflareaccess.com login**. The identical bytes are public at `https://bikar-studio.pages.dev/` (`public-surface.json:25-28`), and **no page on any surface links to that host.**

Both catalogs describe this as a working reciprocal link. `packages/lab/src/catalog.ts:74` calls the gallery *"the published gallery — 3d-models index.html, **which links here**"*; `packages/web/src/catalog.ts:34-39` says *"The Gallery entry closes a loop that was described but never walkable."* The loop is still not walkable for anyone but the owner — it closed onto the gated twin. The `<em>sign-in</em>` marker shows this was known; the line-276 comment (*"decided about the pages.dev alias"*) shows it was deferred. It remains a real asymmetry, and it is the one defect **every crawler in §8 reported as OK**.

### 6.2 Dangling edge: `gh-pages:README.md:7` → NXDOMAIN

`**👉 [View the Interactive Gallery](https://3d-models.bytesofpurpose.com/)**` — `nslookup` returns NXDOMAIN, `curl` returns `000`. This is the README's *primary* call to action, and it is on the deployed branch. `README.md:105` has the working `omars-lab.github.io` URL, so the file contradicts itself.

### 6.3 Edges that break if Access is extended to `bikar-studio.pages.dev`

Three, and all three fail silently — no build breaks, no test turns red:

1. `packages/lab/src/editor.ts:22` — `STUDIO_EDITOR_URL = 'https://bikar-studio.pages.dev/editor'`, consumed at `main.ts:323` and `lego-main.ts:423`. This is the "Open in Studio" handoff from **both** Labs, and it is baked into the deployed `gh-pages:assets/style-BFfxPe7x.js:3`. Its own docstring gives the reason it lives there — *"a redeployed studio that only one page followed is a dead link you cannot see from the page that still works"* — which is the same argument for checking it.
2. Edge 21-23 (`packages/web/src/catalog.ts:110,119,128`) run the other way and survive; they are the only cross-host edges that would not break.
3. Fixing §6.1 by repointing `index.html:277` at `bikar-studio.pages.dev` would **add a fourth** breakable edge. The two defects are coupled: you cannot fix the gate without deciding the pages.dev question.

Additionally, `public-surface.json:39-50` records that Access on both named hosts *"would not touch"* the `<hash>.bikar-studio.pages.dev` aliases — so the graph's exposure boundary cannot be closed by an Access change alone.

### 6.4 Edge that dangles in the build and resolves only after vendoring

`packages/lab/lab.html:23` and `lego.html:24` link `./index.html`. **No `index.html` exists in `packages/lab/`** — my extractor correctly reports both as dangling against `packages/lab/dist/` (§8.1). They resolve only after `make lab-vendor` (`3d-models/Makefile:155-168`) drops the four pages beside `3d-models/index.html`. Correct in production, unverifiable in the repo that owns the file — the cross-repo seam the Makefile comment names: *"Adding a page is two edits, in two repos, and saying so is cheaper than a cross-repo check that would have to run a build."*

### 6.5 Asymmetric: `studio.html` is the site index and links to nothing outside itself

`packages/lab/studio.html` is `<div id="app">` + one module script — no static nav at all. `studio-main.ts` renders `./lab.html`, `./lego.html`, `./design.html` and **no `./index.html`**. So `lab.html` and `lego.html` both offer "← Studio" *and* "← Gallery", while the Studio index they point at offers no way back to the gallery. Verified by live render (§8.6): 8 anchors, 3 distinct targets, none of them `index.html`.

### 6.6 `design.html` is an orphan to every non-JS consumer

Reachable only through `studio-main.ts:56`, whose href is built by concatenation and therefore does not exist as a string in `assets/studio-7nKoSMTR.js`. Consequences measured: the offline scraper missed it, both linkinator crawls missed it, linkchecker missed it. It is `status: 'preview'` in `catalog.ts:202`, so being hard to find is arguably intended — but it is *deployed* (`Makefile:146`), publicly served (200), and absent from the host's sitemap, which means no crawler on earth will index it.

### 6.7 All five gallery pages are missing from the only sitemap that covers their host

`https://blog.bytesofpurpose.com/sitemap.xml` returns 200 and lists blog content; `grep -c '3d-models'` → **0**. `gh-pages` ships no `sitemap.xml` of its own (404 at `/3d-models/sitemap.xml`).

### 6.8 Deployed bundles have drifted from local `dist/`

Live `bikar-studio.pages.dev` serves `assets/main-D9atgaom.js` and `assets/editor-DCmw5sYk.js`; the local `packages/web/dist/` has different hashes for both (`ch-widgets-DhMbpkqX.js` and `editor-De_8Yjfz.css` do match). Any offline extractor reads a build that is not what is deployed — a bounded, real limitation of the recommended approach.

---

## 7. Recommendation

*(Superseded by §10, which is the same recommendation with the POC evidence behind it. Kept here for the required section order.)*

**Do not add a link checker.** The repo already measured why: 8.4% of 737 URLs sampled, ~11% false alarms against a true dead-link rate under 1%, and *"a gate that cries wolf gets switched off, which is worse than having no gate."* Every crawler I ran (§8.3, §8.4) confirms the deeper problem — they cannot see the defect that actually exists here, and they mark it green.

**Check the invariant the repo already stated and does not enforce:** *no page on a surface declared `public` may link to a host declared `exposure: "access"`, and every cross-host edge must name a host that some checked-in surface declaration serves.* `packages/web/public-surface.json` is already the authority; nothing reads it for links.

**Store the graph as a plain JSON edge list**, generated Mermaid rendered into a doc for reading.

---

## 8. POCs built and run

All under `/private/tmp/claude-501/-Users-omareid-Workspace-git-3d-models/416aa36c-c7af-4cf1-91db-d2cdc9668841/scratchpad/sitemap-poc/`. **Both repos and the `gh-pages` branch were never modified** — `git status --porcelain` clean in both at the end; `gh-pages` read via `git show` / `git archive | tar -x` into the scratchpad, never checked out.

### 8.1 POC A — offline static extractor from built output

`a-static-extractor/extract.mjs` (9.2 KB, zero dependencies) + `surfaces.json` (a 40-line hand-written declaration, the only non-measured input). Reads a `dist/` on disk **or** a path prefix inside a git ref via `git show`.

```
$ node extract.mjs > graph.json      # 0.58s real, exit 0, 35 KB
nodes: 13   edgesTotal: 98   edgesPage: 86
byStatus: resolved 69, resolved-cross-surface 10, external-unknown-host 7,
          external-third-party 5, templated-unresolvable 4, dangling 3
```

It found, unprompted:

```
[resolved-cross-surface] gallery:/index.html -> https://bikar.naqshcoffee.com
                         @index.html:277   target-host-is-access-gated
[resolved-cross-surface] gallery:/assets/style-BFfxPe7x.js -> https://bikar-studio.pages.dev/editor
[dangling]  lab-build:/lab.html  -> ./index.html   @lab.html:28
[dangling]  lab-build:/lego.html -> ./index.html   @lego.html:31
[external-unknown-host] studio-public:/assets/sessions-CEysmZu7.js -> http://localhost:8731
```

**Two failures worth more than the successes.**

*False positive:* `[dangling] studio-public:/404.html -> https://bikar-studio.pages.dev/nope @404.html:9` — that URL is inside an HTML comment explaining the SPA-fallback bug. Scanning HTML for absolute URL literals (needed to catch URLs in inline `<script>`) also scans comments. Fix: strip comments before the literal pass. **This is exactly the false-alarm class the repo's no-link-checker decision was about, produced in the first run.**

*Miss:* it reported `gallery:/studio.html` with **zero** outbound page edges. The real count is 3 distinct targets. `studio-main.ts:56` emits `` href="./${esc(page.file)}" ``, which minifies to `"./"+X(e.file)` — `grep -o './[A-Za-z0-9_.-]*\.html' assets/studio-7nKoSMTR.js` returns **nothing**. No scraper can recover it.

### 8.2 POC A2 — catalog-driven graph (the fix for A's blind spot)

`a-static-extractor/catalog-graph.mts` — imports the two typed `catalog.ts` arrays directly and joins them against `Makefile` `LAB_PAGES`/`DEPLOY_PATHS`.

```
$ npx tsx catalog-graph.mts      # 1.23s real
nodes=11 edges=8 problems=1
  ! RECIPROCITY: packages/lab/src/catalog.ts:74 and packages/web/src/catalog.ts:34-39 both
    describe a gallery->studio link. 3d-models/index.html:277 points at bikar.naqshcoffee.com,
    which public-surface.json marks exposure="access" — so the return edge lands on a login
    wall for every visitor but the owner. The public twin (https://bikar-studio.pages.dev/)
    is never linked.
```

It sees the computed `studio.html → {lab, lego, design}` edges A missed, because the catalog declares them. **Cost:** requires the private bikar repo checked out — the graph cannot be computed from the public repo alone.

### 8.3 POC B — crawler against the live public surfaces

`npx linkinator@latest`, v8.0.3. **`bikar.naqshcoffee.com` was never crawled** — only the one unauthenticated probe in §4.

```
$ npx linkinator https://blog.bytesofpurpose.com/3d-models/ --recurse --format json   # 1.73s
OK: 20   BROKEN: 0

$ npx linkinator https://bikar-studio.pages.dev/ --recurse --format json              # 1.41s
OK: 12   BROKEN: 0
```

Gallery page→page edges recovered — **four**:

```
…/3d-models/ -> …/lab.html          …/3d-models/ -> …/lego.html
…/3d-models/ -> …/studio.html       …/3d-models/lab.html -> …/index.html
```

Plus leaves: `https://bikar.naqshcoffee.com/` **OK**, `https://github.com/…` OK, a Google Fonts stylesheet, and `https://static.cloudflareinsights.com/beacon.min.js/…` — the one thing the live crawl found that no offline method can, because Cloudflare injects it at the edge.

**Four defects in the output:**
1. **`https://bikar.naqshcoffee.com/` reported `OK`.** linkinator followed the 302 to the Access login page, which returns 200. A link checker cannot distinguish "works" from "login wall."
2. **Deduplication turns the graph into a spanning tree.** `lego.html → index.html` and `lego.html → studio.html` exist in the bytes and are absent from the output, because those targets were already discovered from elsewhere. One `parent` per URL, first-discovery only.
3. **`design.html` never visited** — unreachable without JS.
4. **Two disconnected graphs.** `--recurse` follows one root domain, so the studio crawl and the gallery crawl never join, even though edges run both ways.

The studio crawl did recover the outbound cross-host edges (`bikar-studio.pages.dev/ → …/3d-models/{,lab.html,lego.html}`) as checked leaves — matching `catalog.ts:110,119,128`.

### 8.4 POC D — off-the-shelf tools, offline, on a materialized `gh-pages` copy

`git archive gh-pages | tar -x -C …/ghpages-docroot` (27 MB, no checkout).

**linkinator, offline, local directory** — works, no server needed:
```
$ npx linkinator ghpages-docroot --recurse --format json    # 0.99s → 19 links, 0 broken
```
Same 4-edge spanning tree, same misses. **Gotcha:** the first attempt used `--format json --silent` and produced `{"links": []}` — `--silent` suppresses the OK rows, silently reducing the graph to broken edges only.

**linkchecker 10.6.0** (`pip install linkchecker` in a venv), DOT output:
```
$ linkchecker --no-status --check-extern -o dot "file://$PWD/ghpages-docroot/index.html"
# 2.5s, exit 1, 225 lines → d-offtheshelf/lc.dot
"That's it. 23 links in 24 URLs checked. 1 warning found. 0 errors found."
```
It produced a real DOT graph with edge labels — and three defects, two of which I had only read about and here reproduced:

1. **Nodes collapse by title.** Three *different* favicon data-URIs (studio's, lab's, lego's) all became one node named `"svg 3E"`, with three edges into it. Confirms the label-keyed-node problem.
2. **It rewrote the Access-gated node's `href` to the Cloudflare login URL** and emitted `valid=1` on the edge into it. So the checked-in graph would record the login endpoint as the gallery's link target.
3. Same first-discovery spanning tree — no `lab.html → index.html`, no `design.html`.

It was, however, **the only tool that surfaced the Access wall at all** — as a *warning*, not an error: `Warning [http-redirected] Redirected to 'https://naqshcoffee.cloudflareaccess.com/cdn-cgi/access/login/…' status: 302 Found. Result Valid: 200 OK`. That warning is the sole reason exit was 1.

**lychee — not installed, and honestly so.** `npm view lychee-bin` and `npm view @lycheeverse/lychee` both **E404**. There is no npm distribution; it needs cargo or brew. Not worth a Rust toolchain here, and I will not guess at output I did not produce. **hyperlink** installed via npx but dragged in ~20 deprecated transitive packages (`request`, `core-js@2`, `glob@7`, `inflight`) — I did not proceed; per §2 it does not record a link's source, so it cannot build edges anyway.

### 8.5 POC E — the invariant gate (the recommendation, running)

`e-sitemap/check-graph.mjs` — offline, zero dependencies, zero network. Reads `public-surface.json` as the authority for exposure, the `Makefile`, `packages/lab/vite.config.ts`, `packages/lab/src/catalog.ts`, and the checked-in edge list.

```
$ node check-graph.mjs --self-test
self-test FAIL-fixture caught: yes (correct)
self-test PASS-fixture clean:  yes (correct)

$ node check-graph.mjs                                    # 0.041s real, exit 1
I1       G.index -> S.index via bikar.naqshcoffee.com, declared exposure="access" in
         packages/web/public-surface.json. A visitor to a public page gets a login wall.
         The same bytes are public at bikar-studio.pages.dev. Anchor: 3d-models/index.html:277
I1-warn  G.lab  -> S.editor via bikar-studio.pages.dev (public today). If Access is put in
         front of bikar-studio.pages.dev this edge dies silently — no build breaks.
         Anchor: bikar packages/lab/src/editor.ts:22 via main.ts:323
I1-warn  G.lego -> S.editor via bikar-studio.pages.dev … via lego-main.ts:423
I3-info  G.design is reachable from G.index ONLY after JavaScript runs. Measured: a non-JS
         crawl of the live site never visits it.

1 failure(s), 3 note(s).
```

**41 milliseconds, no network, no install, and it fires on exactly the defect all four crawler runs marked green.** Invariant I2 (Makefile `LAB_PAGES` ≡ `vite.config.ts` inputs ≡ `catalog.ts` files) passed — the three lists agree today, which is worth pinning precisely because the Makefile comment says nothing checks it.

### 8.6 POC F — JS-rendering crawl (headless Chrome, live)

To measure what the static methods lose. `document.querySelectorAll('a[href]')` after render:

| Page | Anchors after JS | Anchors a non-JS crawler sees |
|---|---|---|
| `…/3d-models/` | **92** | 8 |
| `…/3d-models/studio.html` | **8** (3 distinct: `./lab.html`, `./lego.html`, `./design.html`) | **0** |

A non-JS crawl of the gallery index sees **9% of its outbound links**, and sees the site index as a dead end. This is why §10 does not recommend a crawler.

---

## 9. Format comparison

Same 11-node / 32-edge graph (90 counting multiplicity), rendered six ways by `c-formats/render.mjs` in **0.10s**:

| File | Bytes | Notes |
|---|---|---|
| `site-graph.json` | 9,249 | the source of truth — nodes, edges, `at` anchors, `visibility`, `defect` |
| `site-graph.mmd` | 2,194 | **renders inline on GitHub**; `linkStyle` colours the 4 defective edges red |
| `site-graph.dot` | 2,804 | `dot -Tsvg` → 23,742 B SVG in **0.17s**, exit 0 |
| `site-graph.tsv` | 2,755 | one line per edge; the best `git diff` of the six |
| `site-graph.graphml` | 5,938 | 2.1× the DOT for the same content |
| `site-graph.cyto.json` | 8,556 | 3.0× the DOT |
| `sitemap.gallery.xml` | 484 | 5 URLs |
| `sitemap.studio.xml` | 292 | 3 URLs — **two files, because one is illegal** (§1.1) |

Mermaid excerpt (the defect edges):

```
  G_index -. "!ACCESS-GATED bikar studio ↗ (sign-in)" .-> S_index
  G_lab   -. "!BREAKS-IF-ACCESS Open in Studio" .-> S_editor
  G_lego  -. "!BREAKS-IF-ACCESS Open in Studio" .-> S_editor
  G_index -. "!DANGLING-DNS View the Interactive Gallery" .-> X_dead
```

**Verdict.** JSON edge list as the checked-in artifact; Mermaid generated from it, because it is the only format GitHub renders and this graph's whole value is being *looked at*. DOT is a better engineering format and loses on that one point; GraphML and Cytoscape JSON cost 2-3× the bytes for a graph nobody will load into Gephi. **The two `sitemap.*.xml` files are the cleanest illustration of §1.1: the format physically cannot hold our graph, and cannot even hold our node list in one file.**

---

## 10. Revised recommendation, grounded in the POC results

| Approach | Setup | Network | Build | Multi-host | False positives observed | Ongoing cost |
|---|---|---|---|---|---|---|
| **A** static extractor | 0 deps, 9 KB | none | needs `dist/` | yes, by declaration | **1 in the first run** (URL in an HTML comment) | scraper rots with the bundler |
| **A2** catalog-driven | tsx | none | none | yes | 0 | needs the **private** repo |
| **B/D** crawler (linkinator) | `npx` | **required** | deployed site | **no — 2 disjoint graphs** | 0 false *alarms*, but **1 false PASS on the defect that matters** | rerun forever |
| **D** linkchecker | pip + venv | required | — | `--check-extern` only | node collapse + rewrote the target to a login URL | GPL dep |
| **F** headless JS crawl | Chrome | required | deployed | no | 0 | heaviest |
| **E** invariant gate | 0 deps, 7 KB | **none** | **none** | **yes, by declaration** | **0** | one JSON file to edit when a page is added |

**Recommend E, with the graph as a checked-in JSON edge list and a generated Mermaid block. Do not add a crawler, and do not add a link checker.**

The reasoning is the POC results, not preference:

1. **Every crawler passed the real defect.** linkinator: `OK`. linkchecker: `valid=1` plus a rewritten href. The Access-gated edge at `index.html:277` is invisible to network checking *by construction* — Cloudflare answers 200 with a login page. A tool class that reports green on the one live defect cannot be the gate.
2. **The one false alarm in this whole exercise came from the URL scraper**, in its first run, on a URL inside a comment. That is precisely the ~11%-false-alarm dynamic `docs/issue-register-evaluation.md` measured. A gate whose input is a hand-written declaration has no such failure mode: it fires on `public → access`, which is a fact about two checked-in JSON files, not a fact about the internet.
3. **The checkable invariant is not "does this URL resolve."** It is the same shape as the invariant `public-surface.json` already enforces for bytes, applied to links: *no page on a `public` surface may link to a host declared `exposure: "access"`, and every cross-host edge must name a host some checked-in surface declaration serves.* `public-surface.json` is already the authority and already tested (`packages/web/tests/public-surface.test.ts`, `scripts/check-deploy.sh`) — nothing reads it for links. That gap is §6.1.
4. **Second invariant, free:** `Makefile:146 LAB_PAGES` ≡ `packages/lab/vite.config.ts` inputs ≡ `packages/lab/src/catalog.ts` files. The Makefile comment states the risk in plain words and accepts it. I2 pins it in 20 lines, costs nothing, and would catch a fifth lab page vendored into nothing.
5. **Generate, don't scrape.** A2 proves the catalogs already *are* the graph declaration — `studio-main.ts:56` computes its hrefs from `PAGES`, so `PAGES` is authoritative and the bundle is its shadow. Ship POC A as a *drift detector* run manually (`make` target, not a hook): it caught the `localhost:8731` URL and the `style-BFfxPe7x.js` cross-host edge, which are worth a periodic look but not a commit block.

**Concretely, in this repo:**

- `docs/site-graph.json` — the edge list, ~9 KB, hand-edited when a page or a cross-host link is added. Every edge carries `at` (a `file:line`), `visibility` (`static` / `js-computed`), and `viaHost`.
- `.claude/gates/site_graph.py` (or `.mjs`) — POC E, wired into `.githooks/pre-commit.d/` beside `30-docs-gate`, with a `--self-test` that fails the counterexample and passes the twin. It already satisfies the repo's D2 shape: a `**Validator:**` with a PASS line and a FAIL line the auditor does not have to hand-construct, because §8.5 prints both.
- `docs/site-graph.md` — the generated Mermaid, so the graph is read rather than parsed.
- **Not** a `sitemap.xml`, unless you want the five gallery pages indexed. If you do, it is genuinely warranted — §6.7 shows they are in no sitemap anywhere — and it is `sitemap.gallery.xml` from §8.5, 484 bytes, dropped into `DEPLOY_PATHS` with a `Sitemap:` line. It buys crawler discovery and **nothing** for the link graph.
- **Add `rel="canonical"`** to the studio pages naming whichever of the two hostnames is the intended public identity (§3). It is the only cross-host relation any consumer acts on. It does not express an edge and is not part of the gate.

**What this deliberately does not do:** it does not verify a single URL resolves. The repo already decided that question with a measurement, and this survey found nothing to reopen it — the tools that check resolution are the tools that reported our one live defect as green.
