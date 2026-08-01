# Four studio defects with one root cause: nothing ties a published surface to its source

> Supersedes the Calibrate plan previously in this file; that plan is complete and
> preserved in git at `de777e3`. (The draft of this line said `4c3b900`, which is
> where the *Lego Lab R0* plan is preserved — the hash was carried over from the
> sentence it replaced without being re-checked. Exactly the K9 the docs gate
> exists for, in a file the gate does not read.)

**Status: complete, 2026-08-01.** All five sections shipped and are live.

| § | What landed | Where |
|---|---|---|
| Zero | dev `/api/patterns` GET emits `bkr_source`, so dev rows stop being silently dropped | bikar |
| A | `patterns/index.json` + disk glob replaces `STARTER_FILES`; bijection gate; gallery regenerated at 102 | bikar |
| B | landing page rendered from `src/catalog.ts` at build time; five cards; count measured from the manifest | bikar |
| C | `packages/web/public/404.html`; `appType: 'mpa'`; `resolvePageForUrl` | bikar |
| D | per-page `<meta name="bikar-page">` + `scripts/check-deploy.sh`, retried against propagation | bikar |
| — | the reciprocal link both `catalog.ts:74,85` described and neither site carried | 3d-models |

Two items in §D were only learned by running the gate live, and are worth carrying
forward: Cloudflare Pages **308**-canonicalises `/404.html` to `/404`, so the literal
filename is the one address that asset is never served at; and a deployment is not
visible at every edge when `wrangler` prints "Deployment complete", so an assertion
set needs a settle window rather than a guessed `sleep`.

Left open deliberately: `scripts/cf-setup.sh:99` still omits `bikar-studio.pages.dev`
from `self_hosted_domains` (Cloudflare settings, Omar's call — see §Security finding),
and confirming the folder round-trip against the live studio needs a signed-in session.

## Context

Four complaints, one shape. In each case a surface the user sees is **hand-maintained
beside** the thing it describes, with no mechanism tying the two together — so it drifts
silently and nothing reports the drift.

| Surface | Source of truth | How it drifted |
|---|---|---|
| `STARTER_FILES` in `packages/web/src/main.ts` | `patterns/**/*.bkr` on disk | 17 files missing (all of `Lego/`), 5 files stale |
| `docs/gallery.html` | `STARTER_FILES` | inherits all 17; 53 cards vs 85 entries; no `Orbs` group |
| `packages/web/index.html` landing | the Rollup `input` map | 2 cards vs 3 entries; "74 starter patterns" vs 102 |
| `deploy.yml` post-deploy check | the deployed site | asserts nothing; cannot fail |

`packages/lab` already solved this twice, and both fixes are copied rather than invented:

- `packages/lab/src/catalog.ts:146-211` — a typed `PAGES` array `studio.html` renders from,
  with `packages/lab/tests/catalog.test.ts` asserting every `*.html` beside
  `vite.config.ts` is both a Rollup input and a `PAGES` entry. Its header (`:1-25`) states
  the rule: *a stale index is worse than none because it is confidently wrong about what
  the site can do.*
- `packages/lab/src/lego-scripts.ts:44-46` — the Lego preset registry, pinned against its
  directory by `packages/lab/tests/lego-presets.test.ts` *"so a preset added to one and not
  the other fails rather than silently missing its param-box sweep."*

The second is exactly the check `STARTER_FILES` lacks. The precedent existed; it was never
applied here.

**Intended outcome:** every pattern on disk appears in the studio; the landing page cannot
omit a page that ships; an unknown URL returns 404; and each is held by a gate rather than
by remembering.

---

## Root cause — the rule was never written, not merely not followed

`bikar/.claude/skills/bikar-dsl/SKILL.md:85-89` is the **only** registration statement in
either repo, and both its globs are literally `Orbs/`:

> `patterns/Orbs/*.bkr` has two downstream copies that must track it in the same change:
> the studio's embedded `STARTER_FILES` entries in `packages/web/src/main.ts`, and
> 3d-models' vendored `src/Orbs/*.bkr`.

Every folder created since — `Pieces`, `Walls`, `Assemblies`, `Coupons`, `Lego` — falls
outside it. A search of both repos' `.claude/skills/`, `CLAUDE.md`s and `docs/*.md` for any
general phrasing returns no other hit. That is **K10**: a rule ported from one domain with
its transfer conditions never stated.

The authoring skills confirm it from the other side. `pattern-construction/SKILL.md:114-116`
— *the* on-ramp — terminates at *"Step 3: Write the File… then tell the user to load it in
the web UI."* `pattern-management` (227 lines) and `blueprint-design` (185 lines) mention no
downstream surface at all. `pattern-construction:342` names `STARTER_FILES` only as a
precondition on files already in it. The one skill in either repo that models registration
properly is 3d-models' `design-note/SKILL.md:91` — *"### 4. Land it in the catalogue"*.

**The use-case map already claims these shipped.** UC12/UC13/UC15/UC17 pin
`Walls/Nail-Wall.bkr`, `Coupons/Machine-Card.bkr`, `Lego/Hex-Field-Tile.bkr`,
`Assemblies/Brick-Stack.bkr`, `Pieces/Nail-Tile.bkr` as delivered capability. There is no UC
row for registration, which is why the commit-blocking use-case hook has never fired.

---

## Zero — the bug that makes all of this invisible in dev too

**Fix this first; it is independent of everything below and is one line.**

`loadPatternsFromAPI()` (`main.ts:3456-3489`) calls `fromPatternRows`, which requires
`bkr_source` (`pattern-api.ts:127-129`) and `continue`s past any row lacking it. The dev
API's `readPatternsDir` emits `{ name, content, folder }` (`vite.config.ts:385`). So **every
dev row is dropped**, `patterns.length > 0` is never true, and the dev studio silently falls
back to `STARTER_FILES` — the fallback comment at `:3487` makes it silent by design.

Half-finished migration in `7c73d02` ("the studio has never been able to save a pattern"):
the dev **PUT** handler was moved to `bkr_source` (`vite.config.ts:74-80`, with a comment
saying so) and the **GET** side was left on `content`.

**Fix:** `readPatternsDir` emits `bkr_source`. Regression test: a dev-shaped payload through
`fromPatternRows` must yield rows, not `[]`. Today it yields `[]` — that inversion is the
test, and `packages/web/tests/pattern-api.test.ts` is where it goes.

Consequence worth stating: until this lands, an author writing a new pattern sees it in
**neither** dev nor prod. That is the real reason the drift went unnoticed for 2.5 months.

---

## A. Seed source — a manifest for order, disk for content

**Decided (Omar, 2026-08-01): manifest + glob, and all 102 patterns are included.**

### What the loss audit settled

Adversarial byte-level audit of all 85 entries against disk:

- **No content dies.** 85 entries, 85 disk counterparts, **zero orphans**. 69 byte-identical;
  11 `Orbs/` differ by a trailing newline only; 5 `Petal Tutorial` files where **disk is
  newer** (`3029677` fixed disk and skipped `main.ts`). Deleting the array *repairs* those 5,
  which `packages/core/tests/dsl/option-b-template-regen.test.ts:31,42,49` already asserts
  against.
- **0 folder mismatches**, spaces and all. The 4 `folder`-less entries are genuinely at root.
- **Exactly four keys across all 85**: `name` 85, `dirty` 85, `content` 85, `folder` 81. No
  fifth field anywhere; `transient` appears on **zero** entries.
- **All 102 disk files compile** — `starter-compile.test.ts` run green at 103/103.
- **What does die is order and inclusion**, which exist only in the array. All 9 folders
  reorder under `localeCompare`; `Petal Tutorial`'s curated
  `Blueprint → First-Arc → 1-Ring → 2-Ring → Full → Spin → Outer-Glow → Warm → Strapwork`
  *is* the tutorial and is unrecoverable from disk.
- History: across all 25 commits touching `main.ts` since extraction, exactly one
  main.ts-only window ever existed (`f5b89ae`, 3 orbs, closed next day by `d1a0d43`). The
  Petal difference never runs the other way.

### The design

`patterns/index.json` — an **ordered list of every pattern**, checked in, reviewable:

```json
{ "order": ["Star-8.bkr", "Sq-Oct.bkr", "Hexagram.bkr", "Rosette-12.bkr",
            "Petal Tutorial/Petal-Blueprint.bkr", "Petal Tutorial/Petal-First-Arc.bkr",
            "Petal Tutorial/Petal-1-Ring.bkr", "..."] }
```

No `exclude` key. Since all 102 ship, the gate is a **bijection**: every manifest path
resolves on disk, every disk `.bkr` appears in the manifest, exactly once each. That is
strictly stronger than an allow/deny list and has no dead branch. Add `exclude` only when
something actually needs excluding.

`main.ts` replaces 3392 lines with a seed built from
`import.meta.glob('../../patterns/**/*.bkr', { query: '?raw', eager: true })` ordered by the
manifest. Note the path: **Vite root is `packages/web`**, so a leading-slash glob would
resolve to a nonexistent `packages/web/patterns/`. Vite 8.0.13 supports
`{ query: '?raw', eager: true }` (verified in the installed `importGlob.d.ts`). Do not rely
on glob key order — the manifest is the only ordering authority.

### Non-negotiables the implementation must carry (from the audit)

1. **Manifest order is authoritative**; glob key order is not.
2. **Entry 0 pinned to `Star-8.bkr`.** `activeIndex = 0` (`:3437`) is the cold-boot file and
   `resolveHashToIndex()` (`:4681`) falls back to it. Assert it.
3. **Folder labels verbatim, including spaces** — `Flower of Life`, `Petal Tutorial`,
   `Tiled Patterns`. No slugging; `collapsedFolders`/`knownFolders` and the gallery group
   titles key on the exact string.
4. **The 4 root patterns keep an absent `folder` key** — never `''` (`pattern-api.ts:107-110`
   and its tests already state why).
5. **Apply the `.folders.json` overlay** (`vite.config.ts:243-256`, `applyFolderOverlay`
   `:330-344`) with its three states intact, `null` meaning *delete the key*. `patterns/.folders.json`
   is tracked and currently `{}`, so disk and overlay agree today — they diverge the moment
   anyone drags a pattern, and a naive read would resurrect a folder the user emptied.
6. **`dirty: false` synthesized on every seeded file**, or `autoSaveToAPI` (`:3493`) fires on
   files nobody touched.
7. **`transient` stays in-memory only** — no disk representation; the `[...patterns,
   ...transients]` merge at `:3471` keeps working; `:7635` remains its only producer.
8. **Trailing newlines: take disk bytes verbatim, no normalization.** 28 of 102 files end
   with `\n` and no embedded entry does. Disk is the source of truth; document the change
   rather than silently rewriting 28 files.

### Downstream, in the same change

- **`scripts/generate-gallery.ts:24-138`** — its `indexOf('const STARTER_FILES')` scraper
  throws the moment the array is gone. Rewrite it to read the manifest + disk, then re-run
  `make gallery`: the checked-in `docs/gallery.html` is 53 cards / 8 groups against a real
  102 and is missing `Orbs` entirely.
- **`scripts/extract-patterns.ts` — delete, do not port.** Its direction (main.ts → disk) is
  now backwards; running it would overwrite the 5 correct Option-B Petal files with the
  stale embedded ones. It is in no Makefile target.
- **Generalize the rule that caused this**: rewrite `bikar-dsl/SKILL.md:85-89` to state the
  general obligation (any `patterns/**/*.bkr` must appear in `patterns/index.json`), and add
  a registration step to `pattern-construction/SKILL.md` after `:116`, modelled on
  `design-note/SKILL.md:91`. Drop that skill's now-obsolete backtick-pitfall note at `:355`.
- **Stale references to update**: `CLAUDE.md:58` (Tenet 25's "not added to `STARTER_FILES`"
  ship gate) and `:447`; `.claude/skills/generate-gallery/SKILL.md:10,17,29,43,61`;
  `pattern-construction/SKILL.md:342`; `compact-prompt/SKILL.md:189`; `dev-workflow/SKILL.md:44`.
- **3d-models vendored copies** under `src/Orbs/` (11) and `src/Lego/` (7) were verified
  **all 18 byte-identical** to `patterns/`. Unaffected, but the generalized rule should name
  them.

**All 102 ship, including `Coupons/`.** That is a deliberate call — the audit's view was that
calibration hardware is instruments rather than designs, and it is overridden here. Practical
effect: 5 new folders appear in the tree (`Assemblies`, `Coupons`, `Lego`, `Pieces`, `Walls`),
all collapsed on first load per `:3441`.

---

## B. Landing page — the lab's catalog, with its test

`packages/web/index.html:71-86` is hand-written static HTML: two `<a class="card">`, a
hard-coded "74 starter patterns", and both hrefs carrying a trailing slash that Cloudflare
308-redirects away (`/editor/` → `/editor`), costing a round trip per click.

**Approach:** port `packages/lab/src/catalog.ts`'s shape into `packages/web` — a typed
`PAGES` array rendered by `src/landing.ts`, plus a vitest mirroring
`packages/lab/tests/catalog.test.ts` asserting every Rollup input
(`vite.config.ts:456-464`) has a catalog entry and vice versa. Reuse the lab's
`status: 'live' | 'preview'` field (`catalog.ts:142`).

Same omission, same change:

- Link the two published sites to each other. `catalog.ts:74,85` already *describes* the
  relationship in both directions; neither site carries the link.
- `editor.html` has **no navigation at all** — `href=` returns exactly one hit, the
  stylesheet at `:7`. Add a link home.
- Derive the pattern count from the manifest instead of hard-coding it.

---

## C. 404 — one file

No `404.html` in source or `dist/`; no `_routes.json`, `_redirects`, `_headers`, `public/`,
or `functions/_middleware.js` either. Cloudflare Pages treats an output with no top-level
`404.html` as an SPA and serves `index.html` with **HTTP 200** for every unmatched path.
Confirmed live — `/404.html` itself returns the 2388-byte landing page, proving the asset is
absent.

**Fix:** add `packages/web/public/404.html` (Vite copies `public/` verbatim; the directory
does not exist yet). Its presence disables the fallback.

Dev note: `vite.config.ts` sets no `appType`, so it defaults to `'spa'` and reproduces the
same 200 locally — which is why this was never caught. `multiPagePlugin` (`:428-447`) is
`configureServer`-only and its prefix match is greedy (`/editorial-nonsense` → `editor.html`).

---

## D. Deploy validation that can fail

`.github/workflows/deploy.yml:63-82` is `continue-on-error: true` (`:64`), checks two bare
roots (`:80`, `:82`), and treats 200 **and** 302 as ✓ (`:73`). Every branch `echo`s and
returns 0; nothing calls `exit 1`.

Worse than blind: given the SPA fallback, *any* path on pages.dev returns 200, so even
checking `/editor` would pass a deploy that dropped `editor.html`. And 302 counts as success
on the custom domain, where Access redirects unknown paths too — so that check asserts only
that Cloudflare Access is up.

**Fix:** drop `continue-on-error`, assert on **body content** (a per-page marker string per
entry point), and add a negative assertion that a known-bad path returns 404 — meaningful
only once §C lands, and the check that would have caught the 4-day/34-run outage.

---

## Security finding — surfaced, not fixed here

`scripts/cf-setup.sh:99` provisions the Access app with
`self_hosted_domains: ["bikar.naqshcoffee.com"]`. **`bikar-studio.pages.dev` is not in it.**
Verified live: the custom domain 302s to Access login; pages.dev returns 200 with no auth for
landing, `/editor` and `/sessions` alike. APIs still fail closed there — Access sets
`CF_Authorization` only on the custom domain, so `functions/api/_cf-auth.js:31-73` returns
`null` and every route 401s. The pages are public; the data is not.

Cloudflare settings change, not code. **Left to Omar.**

---

## Critical files

**bikar, new:** `patterns/index.json`, `packages/web/public/404.html`,
`packages/web/src/catalog.ts`, `packages/web/tests/catalog.test.ts`,
`packages/web/tests/pattern-manifest.test.ts` (the bijection gate).

**bikar, modified:** `packages/web/src/main.ts` (`:43-3434` deleted, `:3436-3441` reseeded),
`packages/web/vite.config.ts` (§Zero `bkr_source`; glob/fs config),
`packages/web/index.html`, `src/landing.ts`, `editor.html`,
`scripts/generate-gallery.ts`, `.github/workflows/deploy.yml`, `CLAUDE.md:58,447`, and the
skill files listed in §A.

**bikar, deleted:** `scripts/extract-patterns.ts`.

**3d-models, modified:** `index.html` (reciprocal link); `use-cases.md` if registration earns
a UC row.

**Reused rather than written:** `packages/lab/src/catalog.ts` (shape + `status`),
`packages/lab/tests/catalog.test.ts` (input↔entry assertion),
`packages/lab/tests/lego-presets.test.ts` (registry↔directory assertion — the direct model
for the manifest gate), `applyFolderOverlay` (`vite.config.ts:330`), `setPatternFolder`
(`pattern-api.ts:107`), `design-note/SKILL.md:91` (registration-step shape).

---

## Verification

- **§Zero** — a dev-shaped `{name, content, folder}` payload through `fromPatternRows`
  returns `[]` **before** the fix and rows **after**. Then boot `vite dev` and confirm the
  Lego folder actually renders.
- **§A** — the manifest gate goes red three ways, each tested: a disk file absent from the
  manifest; a manifest path with no disk file; a duplicate entry. Plus: entry 0 asserted to
  be `Star-8.bkr`; `Petal Tutorial` order asserted explicitly against the curated sequence
  (it is the case alphabetical destroys); the 5 Petal patterns the studio serves match the
  disk copies `option-b-template-regen.test.ts` asserts against;
  `starter-compile.test.ts` stays green at 103/103; `make gallery` regenerated and its card
  count matches the manifest length.
- **§B** — the catalog test fails when a Rollup input has no entry (add a throwaway input,
  watch it go red) and passes on the real tree.
- **§C** — after deploy, `curl -o /dev/null -w '%{http_code}' https://bikar-studio.pages.dev/nope`
  returns **404**, and `/404.html` returns the new asset rather than the 2388-byte landing
  page. Both are 200 today — that inversion is the test.
- **§D** — show the new step actually failing against a URL known to be missing its marker
  before wiring it in.
- **Tenet 25** — the 17 newly-visible patterns get a portal look before shipping. They
  compile, which that tenet says is necessary and not sufficient.
- `npm run ci` green in bikar.
- **Deploy-verification discipline** (learned the hard way): the studio is `editor.html` →
  `editor-*.js`, **not** the 0.07 kB `main-*.js` landing shim; check `bikar-studio.pages.dev`,
  **not** the stale `-aur` alias; grep **string literals or CSS class names**, never
  identifiers — minification mangles those.

## Out of scope

Deploying `packages/lab` to `bikar-studio` (it is vendored to 3d-models gh-pages via
`Makefile:146,153-166`; linking out costs nothing). Deploying `docs/gallery.html`, which is
generated, committed, and served from nowhere. Adding `bikar-studio.pages.dev` to the Access
app. Page-level auth middleware. A 3D authoring on-ramp skill — the skills audit found none
exists for `piece`/`tile`/`wall`/`assembly`/`brick` (corpus census in `docs/grammar.md` §12:
`pattern` 342 uses, `piece` 28, `assembly` 3, `wall` 2, `brick` 1), which is real but is its
own work and would swallow this fix. Any change to a pattern's `.bkr` content. Printing.
