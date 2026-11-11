---
date: 2026-11-11
produced-by: three read-only survey agents (Claude Opus 5.5) started by the monitor-print-watcher session, one per area; four facts checked by hand afterwards.
feeds:
  - docs/design/process/users-and-surfaces-design.md
---

# Survey of every page for designing and printing, 2026-11-11

- **Date:** 2026-11-11
- **Produced by:** Claude Opus 5.5, through three read-only survey agents started by the
  monitor-print-watcher session, one per area (3d-models and the Print Hub; bikar; qiyas,
  youtube and the hand-offs between repos).
- **Feeds:** [`../design/process/users-and-surfaces-design.md`](../design/process/users-and-surfaces-design.md),
  the one-application design (step 0b of the plan Omar approved on 2026-11-11).
- **Why it was run:** Omar, 2026-11-11: "how I feel we have a disconeected system of pages ...
  how cna we unify into a single proper uX with use cases".

The three reports are kept below word for word, as the agents wrote them, with two changes:
their headings moved down one level so each sits under its own report heading, and the home
folder in absolute paths is written `~/`. File paths and port
numbers in them are as they stood on 2026-11-11 and are not kept up to date. Four facts were
checked by hand afterwards and are added at the end.

---

## Report 1: 3d-models and the Print Hub

Omar's sense that the pages are disconnected is borne out by the files. There are three page families with no common home and no shared navigation, plus a fourth way of working that has no page at all (the skills, run in chat). The "hub" is not the `-hub-ro`/`-hub-rw` folders. It is a separate private repo at `~/Workspace/git/3d-model-hub` (branch `main`, tip `423d79a`, Node app on 127.0.0.1:4717). `3d-models-hub-ro` is a detached checkout of 3d-models' master (`266f32ce`) that the hub reads and refreshes every 10 minutes. `3d-models-hub-rw` is a detached checkout at an older commit (`ad762b27`) that the hub writes answers into before opening PRs.

### Surfaces

| Surface | Job | Source | How served | Entry points | Links out | State |
|---|---|---|---|---|---|---|
| **Hub home** "Print Hub" | Printer state, print register, verdict per piece, read-only plate queue | `3d-model-hub/web/index.html`, `web/src/main.ts`, `server/src/app.ts` | launchd agent (`make agent-install`) on :4717 | Bookmark; `hub.yaml` launcher | plates, gallery, judge, vocabulary | Reads the hub-ro checkout; verdicts go to PRs via hub-rw |
| **Hub Plates** | Every plate by stage, plus "Waiting on you" (what Omar owes) | `web/plates.html`, `web/src/plates.ts` | :4717/plates.html | Hub home | home, gallery, vocabulary, plate.html, judge.html#plate | `plates_gate.py --rank --json` and the plate pages |
| **Hub Plate page** | One plate: clickable bed, prints, approvals, questions, timeline, log | `web/plate.html`, `plate.ts` | :4717/plate.html#/&lt;plate&gt;[/&lt;print&gt;] | Plates, vocabulary | plates (breadcrumb only), judge rows | `docs/design/plates/<plate>.md`, `-media/bed.json` |
| **Hub Judge** | Judge a finished plate, one question at a time | `web/judge.html`, `judge.ts` | :4717/judge.html#&lt;plate&gt;/&lt;row&gt;; comment layer on :8768 (skills say :8766) | Hub home, plates, plate page, links pasted in chat | **Only "Back to the Print Hub"** | Saves to `~/Library/Application Support/3d-model-hub/answers/<plate>.jsonl`, then one `After-print answers` PR into the `## Judged` table |
| **Hub Gallery** | Printed plates, newest first, with finish photos | `web/gallery.html`, `gallery.ts` | :4717/gallery.html | Home, plates | home, plates | Print logs and finished pictures |
| **Hub Vocabulary** | Print words, one card each | `web/vocabulary.html`, `vocabulary.ts` | :4717/vocabulary.html (dev copy on :4718) | Home, plates | home, plates, plate.html, GitHub docs | `vocabulary.py json` |
| **Public gallery** index | Browse cutters, orbs and coasters; download STLs | `3d-models/index.html` | `make site` :8613; `make deploy` to gh-pages at blog.bytesofpurpose.com/3d-models/ | Public | studio, lab, lego, coaster, prints, status, breakdown | build/images, manifests |
| Coaster, Orb and Lego Labs; Studio; Prints; Design notes; Breakdown | Tune designs; index of labs; print records; notes | Built in bikar and copied in (`LAB_PAGES`, Makefile:480) | Same :8613 and gh-pages | Gallery index | Labs link back to index and studio | `prints-manifest.json`, bikar build |
| **Status** | What the gallery was built from | `status.html` | Same | Gallery | index | `status-manifest.json` |
| **Vault home** | Map of plan, backlog, decisions, design docs | `docs/README.md` | Obsidian vault "docs" | Opening Obsidian | Most vault areas, Bases views | — |
| **Feedback-request pages** | Decide open calls by ticking boxes | `docs/working-model/feedback-requests/<date>-<slug>.md` (12 pages) | `obsidian://open?vault=docs&file=…` (request-feedback SKILL.md:38) | Link pasted in chat | Not listed on `docs/README.md` (verified) | Ticks are read back into `decisions-log.md` and the backlogs |
| **Plate pages and queue** | Yes or hold on a plate (Approvals), timeline, print log | `docs/design/plates/*.md` (71), `README.md` queue | Obsidian | Vault home, `bases/plates.base` | print-logs | Frontmatter plus tables; `approvals.yaml` |
| Catalog, Vocabulary README, Wiki, Theme galleries, price pages | Patterns; words; fixing print problems; colors; pricing | `docs/catalog/index.md`, `docs/vocabulary/README.md`, `docs/wiki/index.md`, `docs/design/coaster/themes/` | Obsidian | Vault home (catalog, vocabulary, wiki); themes only by link | — | YAML sources plus generators |
| Print watching | Timelapse and finished picture | monitor-print publishes to the plate page `## The print` | No live page; shows up in Obsidian and the hub plate page | Chat | — | `print-logs/<plate>.md`, `-media/` |

### Disconnects I found

1. **There are three homes and none knows about the others.** The hub home links only to hub pages. The gallery index has no link to the hub (expected, it is public). `docs/README.md` never mentions the hub or the judge page.
2. **The judge page is a dead end.** Its only link is "Back to the Print Hub" (`web/judge.html:15`). It has no link to the plate page or to Plates/"Waiting on you". In practice it is reached through a link pasted in chat (judge-page SKILL.md step 6).
3. **The comment-server port has drifted.** `3d-model-hub/hub.yaml` and `.page-comments/config.json` say 8768, "moved off 8766, which social-presence-hub keeps". But `.claude/skills/judge-page/scripts/open_questions.py:27`, judge-page SKILL.md:53, `.claude/memory/open-hub-at-owed-questions.md` and `.claude/plans/plates-and-feedback.md` all say :8766. Reading the script, it probes 8766, starts `make comments` (which listens on 8768), then likely times out and falls back to :4717 without comments. That last part is inferred, not run. A third address, :4718, is a dev copy (maintain-vocabulary SKILL.md:80).
4. **Two hub links into GitHub point at the wrong folder.** `main.ts:363` and `vocabulary.ts:32` build GitHub URLs. The plate link in `main.ts` uses `.../docs/plates/<plate>.md`, but plate pages live in `docs/design/plates/`. `docs/plates/` holds no plate pages, so those links are likely 404.
5. **"What do I owe?" lives in four places.** Hub Plates "Waiting on you" (the memory note `owed-items-live-on-plate-hub.md` says that box is the one place), `open_questions.py` output in chat, feedback-request pages in Obsidian, and the chat "Yours to do" list.
6. **Approving and judging live in two different tools.** Approving a plate is an Obsidian tick on the plate page. Judging it is a hub button. `plate-hub-design.md` §4 and slice 5 plan to move the Yes button to the hub; not built.
7. **The same information is shown more than once:**
   - Plate status: hub Plates, hub home queue, hub plate page, `docs/design/plates/README.md`, `bases/plates.base`.
   - Printed plates: public `prints.html`, hub gallery, `docs/prints.md`.
   - Vocabulary: hub page and `docs/vocabulary/README.md`.
   - Answers in flight: the hub state folder, an open `answers/` PR, then the `## Judged` table (`hub-answers-three-places.md`).
8. **The maps are out of date or partial:**
   - The use-case map (`.claude/skills/maintain-use-cases/use-cases.md`, UC1 to UC34) has no hub use case: no judging a plate, no approving, no feedback pages. Its only "judge" is UC32, a sampler sheet. `as_of` is pinned at `0352c9dc`.
   - `users-and-surfaces-design.md` (draft, 2026-10-08) still lists after-print answers as "Planned", and its surfaces table names only the "hub" as a whole, not its pages.
   - `plate-hub-design.md` still says "proposal, nothing built" although plates.html and plate.html exist.
   - `docs/site-graph.json` covers only the gallery and studio sites.

### Pieces that could be reused

- **`docs/design/process/users-and-surfaces-design.md`** is the nearest thing to an information-architecture doc. It sets out four roles (customer, owner, print operator, Claude session), three "rooms" (shop front, back office, workshop), a surfaces table and use cases per role (§§3–7). It needs updating for the hub pages.
- **D-112** puts the order pages (Plan, Price, Stock) in the hub, which makes the hub the back office. **D-067** says a Coaster Lab goes in bikar's lab, not the hub. **D-082** says the vault uses Obsidian's built-in Bases views. I found no D-xxx on a shared nav, a hub home or unifying the pages.
- **`plate-hub-design.md`** (in the hub repo) already decided "reading plates moves to the hub", with a 5-slice build order.
- **Indexes and generators that exist:**
   - Three `hub.yaml` files, read by the cross-repo launcher at `~/Workspace/git/hubs` (Print Hub, the gallery pages).
   - `docs/site-graph.json`, checked by `site_graph.py`.
   - `make experiences` and `make site`, which print a list of surfaces.
   - Bases views in `docs/bases/*.base`.
   - `plates_gate.py --rank --json`, `after_print.py questions`, `vocabulary.py json`.
- **Shared code:** the hub has one `web/src/style.css` and a common `<header class="top">` pattern on every page, but no shared nav component; links are typed into each page. `make phone-check` already checks all hub pages at phone width. Page comments are installed in the hub's `.page-comments/` (17 threads) but not in 3d-models.

### Verified versus inferred

I read the hub Makefile, README, `hub.yaml`, the six HTML headers, the link lines in the `.ts` files, `open_questions.py`, the judge-page skill and the relevant parts of the other skills. I also read the 3d-models Makefile site/deploy/validate-gallery targets, `hub.yaml`, the use-case map, `docs/README.md` link lines, `users-and-surfaces-design.md` §§1–7, D-112 and the memory notes, and listed the hub state folder.

These are inferred, not run: that the GitHub plate links 404, that `open_questions.py` falls back to :4717, and how the Lab/Studio pages copied in from bikar link to each other (their links are built in JavaScript; I took them from `site-graph.json`). I fetched no live pages.

---

## Report 2: bikar

I've mapped every page bikar ships. The core finding is that bikar has two separate front doors with two separate page lists. The Studio's landing (`/`) is built from `packages/web/src/catalog.ts`. The Lab's own index (`studio.html`) is built from `packages/lab/src/catalog.ts`. Nothing joins them, no page shares a header or nav component, and the Coaster Lab is reachable only through the 3d-models gallery or the 4613 dev server. All paths below are under `~/Workspace/git/bikar/`.

**Hosts.** The Studio is the Cloudflare Pages project `bikar-studio` (`packages/web/wrangler.toml`). It answers at `bikar.naqshcoffee.com` and `bikar-studio.pages.dev`, both behind Cloudflare Access (`packages/web/public-surface.json`). It deploys with `make web-deploy`. Its dev port is 7120 (`packages/web/vite.config.ts`). The Lab dev server is `make lab-dev`, port 4613, and `hub.yaml` notes it has no page at `/`. The Lab's own vite config says port 5174, but `make lab-dev` overrides it with 4613.

### Surfaces

| Surface | Job | Source | Served | Route / share URL | Links out |
|---|---|---|---|---|---|
| Studio landing | Front door with cards | `packages/web/index.html`, `src/landing.ts`, cards from `src/catalog.ts` via `landing-cards.ts` | Studio `/` | — | Cards to every web page, the vendored lab pages, and the gh-pages Gallery |
| Constructions (editor) | Write a pattern in the DSL and watch it render | `editor.html`, `src/editor.ts` | `/editor` | `?b=1&p=1&hl=…#Slug:s7@x,y` (`docs/url-params.md`) | `/` |
| Deconstructions (sessions) | Work back from a photo; machine read by qiyas | `sessions.html`, `src/sessions.ts` | `/sessions`, `/sessions/<name>/<iter>` (`make deconstruct`, `make feedback`) | `?qiyas=` | `/`; qiyas on :8731 or `/api/qiyas` |
| Decomposition study | Three ways to pin a rosette into pieces | `decomp.html`, `src/decomp.ts` | `/decomp` | — | `/` |
| Rosette pin explorer | Rosette on a LEGO baseplate, live pin solve | `rosette-explorer.html`, `src/rosette-explorer.ts` (d3) | `/rosette-explorer` | — | `/` |
| Orb instrument | What qiyas sees of an orb view | `orb-instrument.html`, `src/orb-instrument.ts` | `/orb-instrument` | `?qiyas=` | `/` |
| Notes (posts) | Reading list and research notes | `posts.html`, `src/posts.ts`, `posts/index.json` | `/posts` | post by URL | `/`; external references (e.g. YouTube) |
| Review | Plain-words reading of what the checker sees | `review.html`, `src/review.ts` | `/review` | `?qiyas=` | `/` |
| Review portal | qiyas React SPA (snapshot copy) | `public/review-portal.html` | `/review-portal` | — | none found |
| 404 | Real not-found page | `public/404.html` | Studio | — | `/`, `/editor`, `/sessions` |
| Orb Lab | Tune an orb, get a printable STL | `packages/lab/lab.html`, `src/main.ts` | 4613 `/lab.html`; Studio `/lab`; 3d-models gh-pages | `?v=1&f=<preset>&<param>=…&code=…&color.X=` (`src/url-state.ts`, 1800-char limit) | `./studio.html`, `./index.html` ("Gallery"), `./breakdown.html` |
| Lego Lab | Tune a brick's clutch fit | `lego.html`, `src/lego-main.ts` | 4613; Studio `/lego`; gh-pages | same scheme; fit kept out of the link | `./studio.html`, `./index.html` |
| Coaster Lab | Size a rosette coaster, live checks, colors, STL | `coaster.html`, `src/coaster-main.ts` | 4613; 3d-models gh-pages only | `f=`, params, `color.*`, saves | `./studio.html`, `./index.html` |
| Orb Breakdown | Watch an orb turn and get built | `breakdown.html`, `src/breakdown-main.ts` | 4613; Studio `/breakdown`; gh-pages | `?base=` | No links; on the Studio it loads frames from `blog.bytesofpurpose.com/3d-models/build/orb-breakdown` (`src/breakdown-base.ts:27`) |
| Design notes | Decision arguments beside compiled geometry | `design.html`, `src/design-main.ts` | 4613; Studio `/design`; gh-pages | — | none |
| Prints | Record of what was actually printed | `prints.html`, `src/prints-main.ts` | 4613; gh-pages only | — | none |
| Lab "Studio index" | Lab pages by actor and use case | `studio.html`, `src/studio-main.ts` | 4613; gh-pages only | anchors | lab pages |
| Thumbnail target | Headless render target for scripts, not visited by people | `thumbnail.html` | throwaway vite server | — | — |
| Pattern gallery | Static page of all patterns as SVG plus DSL | `scripts/generate-gallery.ts` → `docs/gallery.html` (`make gallery`) | Committed file; optional copy to `art.bytesofpurpose.com` (marked "dormant") | — | none |
| CLI | `bikar render/parse/validate` | `packages/cli/src/index.ts` | terminal | — | Writes SVG/STL/PNG/LDraw/JSON; **no HTML** |

### Disconnects

1. **Two front doors, two page lists.**
   - `packages/web/src/catalog.ts` builds the Studio landing.
   - `packages/lab/src/catalog.ts` builds the Lab's `studio.html`.
   - The vendoring decision deliberately leaves `studio.html` out because it "would be a second front door" (`docs/decisions/2026-08-07-labs-served-from-studio.md`).
2. **Coaster Lab and Prints are not on the Studio.**
   - The lab catalog marks both `status: 'live'`.
   - `VENDORED_FILES` is only `lab, lego, breakdown, design` (`packages/web/scripts/vendor-labs.mjs`).
   - 3d-models vendors all seven pages (`3d-models/Makefile:480 LAB_PAGES`).
   - I found no doc in bikar that decides where the Coaster Lab belongs.
3. **The Labs' header links break on the Studio.**
   - Verified: `lab.html:26-28` and `coaster.html:27-28` hard-code `./studio.html` and `./index.html` (labelled "Gallery").
   - Inferred from that: on the Studio, `/studio.html` returns 404 because it isn't vendored, and "Gallery" opens the Studio landing instead.
   - Inferred: on 4613, `./index.html` doesn't exist (the lab has no `index.html`).
   - These links only work in the 3d-models copy.
4. **Dead ends.** Breakdown, Design notes, Prints, the review portal and `docs/gallery.html` contain no navigation links at all. The Studio pages each have only a "← Bikar Studio" link to `/` and no links to each other.
5. **Three visual themes.**
   - `packages/web/src/styles.css`: gold `#C9A84C` on `#080810`.
   - `packages/lab/src/style.css`: `#d6b254` on `#14120d`.
   - `docs/gallery.html`: `#e94560`/`#d4af37` on `#1a1a2e`.
   - Breakdown, design, prints and the index use a teal `#1f6a65` icon (`breakdown.css` uses a light ground).
6. **"Studio" means three things:** the Cloudflare app, the lab's `studio.html` index, and a use-case actor ("Studio author").
7. **No link to the 8766 hub, Shopify or the YouTube repo from any bikar page** (no `8766` or `shopify` hits in either web package). The 3d-models gallery links back to `https://bikar.naqshcoffee.com` (`3d-models/index.html:279`). `hub.yaml` registers bikar with the separate launcher at `~/Workspace/git/hubs`.
8. **The surface audit is out of date.** `docs/design/cross-repo-ux-incorporation.md` §1 predates the Coaster Lab, Prints, the rosette explorer and the orb instrument, and still lists Breakdown and Design as "not in studio".

### Decisions found

- **The Q-HOME / Q-SHELL / Q-VOCAB / Q-DATA questions are about the d3 drawing layer, not a site shell or home page.** They are settled in `3d-models/docs/design/orb/d3-integration-design.md` §5 and mirrored in `docs/decisions/2026-08-31-d3-viz-adapter.md`:
  - **Q-HOME:** the core emits generic shapes; d3 is an optional converter (`packages/web/src/viz-d3.ts`).
  - **Q-SHELL:** pages are plain (vanilla or Lit) with d3 drawing inside the SVG; no React.
  - **Q-VOCAB:** all surfaces converge on one naming convention.
  - **Q-DATA:** the score overlay is a join of qiyas `/encoding` and `/diff`, with no new qiyas fields.
  - Also settled: the Studio is the org-gated home for the explorer.
- **2026-08-07:** the labs are copied into the Studio build rather than linked out; the lab's own index stays out.
- **2026-08-26/27 (`cross-repo-ux-incorporation.md`):** the review portal is remote-reachable through a same-origin `/api/qiyas` proxy. Still open there: Design notes vs `/posts` overlap (open question 2). Breakdown frame data (question 3) appears answered in code — the page probes locally, then falls back to gh-pages.
- I found no information-architecture, unified-shell or home-page design doc in bikar.

### Use cases and flows

- The use-case register lives in 3d-models at `.claude/skills/maintain-use-cases/use-cases.md`. It names 7 actors (`ACTORS` in `packages/lab/src/catalog.ts`) and UC1–UC34.
- The lab catalog maps each page to its use cases: lab UC5/UC4, lego UC15, breakdown UC23, design UC16, prints UC24, coaster UC30.
- From the register I skimmed: rosette explorer UC25, orb instrument UC26, coaster gallery UC28, YouTube reconstructions not yet coasters UC34.
- Playwright specs are in `packages/e2e/tests/` (21 specs; servers on 7120 and 4613 per `servers.ts`). Flows named:
  - **Lab pages:** Orb Lab custom mode and share-link round trip; Lego Lab presets, custom mode, fit kept out of the link, advisories; Coaster Lab boot, mini/standard chips, Printed panel, share link, orbits, pick, fill, loose lines; Breakdown beats.
  - **Studio pages:** posts index and reading list; the review portal card and its same-origin `/api/qiyas` base; sessions feedback (context menu, approve, flag); editor pick menu, hover, layer toggle, dials, round orb, animation loop; every page boots without error (`no-boot-error.spec.ts`).

### Reusable pieces

- **Both catalogs** already hold name, tagline, icon, href and kind, plus actor and use-case mapping. They are checked against the build inputs by `packages/web/tests/catalog.test.ts` and `packages/lab/tests/catalog.test.ts`. This is the natural seed for one shared page list and shared nav.
- `landing-cards.ts`: the card renderer, which runs at build time and works with scripting off.
- The `<meta name="bikar-page">` marker plus `scripts/check-deploy.sh`, which verifies every page actually serves.
- `vendor-labs.mjs`: the mechanism for bringing the Coaster Lab and Prints into the Studio.
- `@naqshcoffee/ui/vanilla` (identity bar and canvas comments), used through `packages/web/src/ch-widgets.ts` on the landing, editor and sessions pages only.
- `packages/knobs` (`dial.ts`, `knobs.ts`, `code-codec.ts`) and the lab `url-state.ts` share-link scheme.
- The two CSS custom-property sets, as candidates to merge into one set of design tokens.

**Read vs. inferred.** Everything above comes from reading the files cited. The inferred items are the runtime 404 and mislabelled-link behaviour in disconnect 3, which follow from relative-link resolution against what is deployed. I didn't open any page in a browser, or check the Shopify, YouTube or 8766-hub sides beyond searching bikar for references.

---

## Report 3: qiyas, youtube and the hand-offs

I covered qiyas, youtube and the seams between all the repos. Two corrections to the brief first. The Print Hub is its own repo, `~/Workspace/git/3d-model-hub` on :4717, not part of 3d-models. And the closest thing to a "single home" already exists in a sixth repo, `~/Workspace/git/hubs`: a launcher page at `hubs.localhost:7101`. None of the four repos you named mentions that address.

Legend: **R** = I read the code or doc. **I** = inferred. **L** = I checked what is listening on the port (`lsof`, plus one `curl` GET); nothing was started.

### A — qiyas surfaces

| Surface / job | Source | How it is served | URL shape | Links in / out | Data |
|---|---|---|---|---|---|
| **Review portal**: walk a pattern image through the 4 checker stages and record verdicts on 8 questions (R) | `src/qiyas/review/server.py`, `review/cli.py`, `web/src/App.tsx`, `SimpleReview.tsx` | `qiyas review` or `make review.serve` (FastAPI, 127.0.0.1:8731). The page `dist/review.html` must be built first with `make review.html` (Docker Node image). Live-edit copy: `make review.dev` on :8732 (R) | `/?image=<path>&ref=<path>`, no params = list of patterns to pick. API: `/encoding`, `/trace`, `/diff`, `/annotations`, `/sessions`, `/candidates` (R) | **In:** bikar `/review` and `/review-portal` (`bikar/hub.yaml:29-50`, `packages/web/src/review-read.ts:178` defaults to localhost:8731); the hubs launcher via `qiyas/hub.yaml`. **Out:** none found (I) | `out/review/<slug>-<sha1>/annotations.json` (R) |
| **Hosted review API** (R) | `qiyas serve --hosted` | ghcr.io/naqshcoffee/qiyas behind a Cloudflare Tunnel at `qiyas.naqshcoffee.com`. A browser gets 403 (service token only) | Reached through bikar's `/api/qiyas/*` proxy | used by bikar | container |
| **Review replay**: turns saved verdicts into backlog notes (R) | `cli.py:780` | CLI | — | — | `out/review-replay/backlog-stubs.md`, `review-verdict.json` |
| **Closeout report + feedback form**: detector closeout with a verdict per shape (R) | `closeout/report.py`, `closeout/feedback_server.py` | `qiyas validate-detector --closeout-report DIR`; feedback server on **:8765** while the command runs | `file://…/index.html`, which POSTs to `/feedback` | none | `<dir>/feedback.jsonl` |
| **Diff reports, 3 levels** (table / side-by-side / interactive) (R) | `report/html.py`; `qiyas diff --report-html*`, `qiyas validate` | Static file | `report.html` | none | wherever `--out` points |
| **Showcase indexes** (R) | `showcase/runner.py`; `make showcase`, `make local.canonical-showcase` | Static files, not tracked in git (R, via `git ls-files`) | `out/showcase/index.html` → `<fixture>/report.html`, `paired-report.html`; also `out/showcase-canonicals/` | the index links to each fixture's report | `out/` |
| **Fixture-drift report** (CI artifact) (R) | `qiyas fixtures report` / `report-index`; `make report-sample` | Static file | `dist/reports/report.html` → `report-<slug>.html` | — | `dist/reports/` |
| **Unknown-shapes report** (R) | `debug/show_unknown_html.py`; `--show-unknown-html` | Static file | — | — | — |
| **Calibration pages** (R) | `calibration/i1/index.html`, `calibration/i2/progress-story.html` (committed) | Open the file by hand | — | — | — |
| **Score / other CLIs** (I: from the command list only) | `score run/explain/replay`, `pixel-diff`, `orb-validate`, `mesh compare`, `iter analyze` | Terminal or JSON output | — | — | — |

### B — youtube

| Surface | Source | Served | URLs | Links | Data |
|---|---|---|---|---|---|
| **Study hub**: videos, reconstructions, discovery (R) | `hub/server.js`, `hub/src/App.jsx` | `make hub` → :5178 (Vite dev server on :5179) | `#/videos`, `#/v/<id>`, `#/reconstructions`, `#/r/<id>` (tabs: Code, Image, Video, History), `#/reconstructions?concept=`, `#/discovery`, `#/c/<slug>` | **Out:** YouTube embeds only. **No links to bikar, 3d-models or qiyas** (R, grep) | `$YT_DATA_DIR` (iCloud), `feedback.jsonl` per video |
| **Step-by-step breakdowns** (R) | `scripts/yt_breakdown.py`; `make breakdown ID= OPEN=1` | Obsidian, vault `yt0docs0vault001`, approve/deny ticks plus review-md comments | `obsidian://open?vault=…&file=breakdowns/<id>` | — | `docs/breakdowns/<id>.md` (2 so far) |
| **Rungs board**: one row per reconstruction and who has claimed it (R) | `make rung-sync` | Markdown | `docs/rungs.md` | — | `reconstructions/*/rung.yaml` |
| **CLI reports** (R) | `make ladder`, `screen-todo`, `registry`, `study-status-all`, `rescore-all` | Terminal | — | — | — |

### C — hand-offs

| # | Hand-off | Link exists? | Evidence |
|---|---|---|---|
| 1 | Gallery → studio | **Link**, behind a sign-in. The gallery uses `bikar.naqshcoffee.com`; the Lab's editor link uses `bikar-studio.pages.dev` (two hosts for one studio) | `3d-models/index.html:279`, `bikar/packages/lab/src/editor.ts:22` |
| 2 | Studio → gallery | **Link** (an "external" card) | `bikar/packages/web/src/catalog.ts:239-241` |
| 3 | Studio `/review` → qiyas server | **No.** You must run `qiyas review` yourself; the page only says "helper isn't running" | `bikar/.claude/skills/deploy-review-backend/SKILL.md:199` |
| 4 | Finished youtube rung → 3d-models coaster | **No link.** You must know `make intake` / `tools/reconstruction_intake.py`; it prints only at session start | `3d-models/tools/reconstruction_intake.py:1-40` |
| 5 | youtube hub → bikar / naqsh file / coaster | **None** | `youtube/hub/src/App.jsx` |
| 6 | Plate design → plate page (`docs/design/plates/<name>.md`) → yes **in that session's chat tab** → send → watch | **No.** Every step goes through chat and skills | `3d-models/.claude/plans/plates-and-feedback.md:20-40` |
| 7 | Judge on the hub → answers PR → `## Judged` table → print record | **Hub opens the PR automatically.** Answers sit in three places in turn: unsent file on disk, open PR, merged table | `3d-models/.claude/memory/hub-answers-three-places.md` |
| 8 | Getting the judging link with comments on | **Broken: the port has drifted.** Details below | — |
| 9 | Feedback request → Obsidian | **Link** (`obsidian://` opened by the skill) | `request-feedback/SKILL.md:38` |
| 10 | Breakdown → Obsidian | **Link** (`OPEN=1`) | `yt_breakdown.py:678` |
| 11 | Closeout report → feedback form | Works only while the CLI that started it is running | `feedback_server.py` |
| 12 | Any hub → hubs launcher | **No back-links.** Repos only register through `hub.yaml` | `hubs/design.md` |

**Hand-off 8, the comment-port drift (R+L).** `3d-model-hub` moved its comments server to **8768** on 2026-11-07 (`hub.yaml`, `Makefile:126`, commit dea512b on main). But 3d-models still says **8766** in four places: `judge-page/SKILL.md:53`, `open_questions.py:27`, `plates-and-feedback.md:31`, and the memory note. Right now 127.0.0.1:8766 answers "Print Hub" (L), so the old link works for the moment, probably from a process left over from before the move (I). If that process dies, `ensure_comments()` runs `make comments`, which starts on 8768, then waits on 8766 and gives up after 15 seconds. You land on the bare :4717 page with no comments (R, `open_questions.py:62-77`). The hubs plan also reserves the whole 8766–8799 range for page-comments (`hubs/design.md:705`).

**Places a person is asked something or shown "waiting on you"** (all R):
1. Obsidian feedback-request pages: `3d-models/docs/working-model/feedback-requests/` (12 pages).
2. The Print Hub's "Waiting on you" box (`/api/plates`).
3. The "plate decisions waiting on Omar" list in `plates-and-feedback.md`.
4. review-md threads: hidden `docs/.<name>.comments.md` sidecar files in 3d-models; youtube breakdowns.
5. Page-comment threads: 17 in 3d-model-hub, 30 in the storefront.
6. The storefront hub's own "Waiting on you (n)" on :9494 (`hub-review/DESIGN.md`).
7. Storefront `docs/decisions/asked/*.md`.
8. qiyas `docs/decisions-pending.md` ("🟡 DECIDE").
9. qiyas closeout `feedback.jsonl` and review-portal verdicts.
10. youtube hub thumbs up/down per video; youtube discovery review queue (read-only); youtube breakdown ticks.
11. AskUserQuestion: 3d-models skills `send-plate`, `review-print`, `find-model`, `request-feedback`, `print-model`; bikar's `start-deconstruction` and `iteratively-deconstruct-pattern`.
12. Plan files under `.claude/plans/`: 3d-models 17, bikar 31, qiyas 61, youtube 4.

That is two separate "Waiting on you" boxes and at least ten other places.

### D — existing unification material

- **Use-case map:** `3d-models/.claude/skills/maintain-use-cases/use-cases.md` (R).
  - A mermaid diagram of 7 actors and **34 use cases** (UC1–UC34), plus a table pinning each use case to code by commit (bikar, qiyas, youtube).
  - It lists **shipped capabilities with code pointers, not user journeys.** There is no ordering, no steps, and no hand-offs. Planned features are excluded by rule.
  - Only UC7, UC26 and UC34 cross repos. No use case covers judging on the hub, approving a plate, or the Obsidian feedback loop.
  - Checked by `validate.py` and the pre-commit hook `.githooks/pre-commit.d/20-use-cases`.
- **`hubs` repo (outside your named set):**
  - `design.md` builds the launcher plus the `hub.yaml` contract and explicitly rules out frames and a shared run-time shell.
  - `docs/one-hub-design.md` (2026-11-04) concludes "one hub already exists" (launcher + Caddy router; 16 repos, 34 pages). It proposes one comment watcher and a dispatcher that routes comments to sessions, and no shared package.
  - Also `docs/mental-model.md` and `docs/sitemap-design.md`.
- **bikar:** `docs/design/cross-repo-ux-incorporation.md` (2026-08) lists every surface across three repos and makes the **studio the front door**. Phases 1–3 and 5 shipped. It is stale: its line numbers and ports have moved, so treat it as background, not current fact. The companion plan is `.claude/plans/cross-repo-ux-realization.md`.
- **3d-models:** `docs/site-graph.md` is a declared link graph of the gallery and studio only. `docs/research/sitemap-link-graph-survey.md` found a localhost:8731 URL shipped in the public studio bundle.
- **Not found:** any doc mapping journeys across all repos, including youtube, the Print Hub, Obsidian and the storefront.

Not covered: bikar's and 3d-models' own pages (the other agents have those), and the storefront's code (docs only). I did not write the plan file the planning prompt offered, so as not to break the read-only rule.

---



---

## Checked by hand afterwards (2026-11-11)

1. **The tick boxes the plates gate reads.** `.claude/gates/plates_gate.py` matches a ticked
   Approve or Hold box with two patterns, `TICKED_APPROVE` and `TICKED_HOLD` (lines 244 and 245
   on 2026-11-11). A ticked box is only a notice until `plate_approve.py` writes it as a row in
   the page's Approvals table (lines 471 to 489 and 1171 to 1179). The test pages the gate
   builds for itself carry a `## Your call` section with both boxes (line 1561).
2. **What the editor does with no pattern store.** bikar `packages/web/src/main.ts` asks
   `/api/patterns` for the list; when that fails it keeps the built-in starter patterns and says
   nothing on the page (line 79). A failed save is a `console.warn` only (lines 128 to 129).
   So an editor served with no store looks as if it works and loses every save.
3. **The gallery and the Lab's own index page.** The public gallery's `index.html` links
   `studio.html` ("every page, and who it is for", line 270), and the `Makefile` copies
   `studio.html` in through `LAB_PAGES` (line 480). Deleting the Lab's index means changing
   that link and that list in the same change.
4. **The Print Hub's launcher card.** `~/Workspace/git/3d-model-hub/hub.yaml` names two
   runners (the hub on 4717, kept up by a launch agent; the comment page on 8768, started with
   it), one hub card ("Print Hub") and one API card (`/api/`, checked at `/api/plates`).
