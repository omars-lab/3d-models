<!--
provenance
  date:         2026-08-02
  produced-by:  Claude Opus 5 (Claude Code), adversarial audit at the user's request
  feeds:        docs/lego-lab-design.md (studio preview surface); no design doc yet
                owns the studio editor's 3D preview gate — this file is the
                first written record of it.
  method:       (a) static read of both pipelines in three local repos;
                (b) local re-render of all 7 single-brick presets through the
                    bikar CLI from two independently-built `packages/core/dist`
                    bundles, compared by SHA-256;
                (c) a local probe script running the *same* `compileToGeometry`
                    entry point the studio's worker calls, printing which
                    result fields each preset populates — run first over the
                    seven single-brick presets, then re-run over all ten
                    `patterns/Lego/*.bkr` as a follow-up, which closed open
                    question §7.4;
                (d) HTTP fetch of the deployed studio HTML + all three of its
                    JS bundles, and of the deployed gallery HTML + two of its
                    preview PNGs, grepped for string literals (not identifiers
                    — minification mangles those);
                (e) `git ls-tree`/`git show` against the local `gh-pages` branch.
  VERIFIED:     both deploys' freshness at the bundle; byte-identical STL
                geometry across both bikar checkouts; the exact source line
                that gates the studio's 3D preview; the gallery's rendered
                output (two PNGs viewed directly).
  NOT VERIFIED: **the studio's on-screen appearance was never observed.** Both
                browser tool-chains were unavailable this session
                (`claude-in-chrome`: "Browser extension is not connected";
                `chrome-devtools`: "The browser is already running for
                .../chrome-profile"). I did not run a local vite dev server
                either. Everything in §1 about surface A is *inferred* from
                code plus the local evaluator probe, and is labelled as such.
                A five-minute screenshot would confirm or refute it and should
                be step 0 of acting on this report.
  CAVEAT:       the repo state changed underneath this audit — see §3.4. One
                intermediate measurement was invalidated and is reported rather
                than deleted.
-->

# Studio ↔ gallery brick render mismatch — audit and plan

**Verdict: H3 (DEFECT), high confidence, on the STUDIO side.**
Both surfaces are freshly deployed and the underlying geometry is byte-identical.
The studio editor has no code path that renders a `brick` in 3D at all.

---

## 1. What differs

### 1.1 Surface B — the gallery (OBSERVED)

I fetched and viewed two of the eight preview PNGs directly:

- `EdgeStudTile.png` (21,852 bytes, HTTP 200 from
  `http://blog.bytesofpurpose.com/3d-models/build/images/web/EdgeStudTile.png?v=20260731a`)
  — a solid gold three-quarter view of a square plate. Twenty studs run around
  the rim only, leaving a clear field in the middle into which a sunburst /
  starburst relief is cut as visible recessed slots. The side walls are shaded a
  darker gold. Background is transparent/white. This matches the card's spec
  text `6 × 6 studs / perimeter ring / 17 tube anchors`
  (`3d-models:index.html:459-462`).
- `ClassicBrick.png` (15,608 bytes, HTTP 200) — a gold 2×4 brick, eight studs,
  no art, same three-quarter camera.

Both are unmistakably **3D renders of the printed solid**.

### 1.2 Surface A — the studio editor (INFERRED, NOT OBSERVED)

I could not load `https://bikar-studio.pages.dev/editor#Edge-Stud-Tile` in a
browser. What I did instead: ran the studio's own entry point,
`compileToGeometry`, from the same `@naqshcoffee/bikar-core` build, over every
preset, and printed which result fields it populates. The studio's render
dispatch keys off exactly one of those fields.

| preset | `orb3d` | `orbMesh` | `brick3d` | 2D faces | 2D segs |
|---|---|---|---|---|---|
| Classic-Brick | **false** | true | true | 0 | 0 |
| Star-Brick | **false** | true | true | 18 | 8 |
| Edge-Stud-Tile | **false** | true | true | 50 | 12 |
| Grid-Field-Tile | **false** | true | true | 18 | 36 |
| Pin-Rail | **false** | true | true | 0 | 0 |
| Hex-Field-Tile | **false** | true | true | 18 | 36 |
| Rational-Repeat-Tile | **false** | true | true | 132 | 60 |
| Star-Mural | **false** | true | false | 162 | 72 |

The studio's dispatch is `if (geom.orb3d)` — `bikar:packages/web/src/main.ts:1985`.
`orb3d` is false for **all eight presets I loaded** (the seven single bricks the
brief named plus Star-Mural; I did not probe Rosette-Brick or Seam-Coupon, which
have no gallery card). So all eight fall through to line 1993,
`container.innerHTML = buildSvgFromGeom(geom)` — the flat 2D pattern SVG.

**The inferred delta, per preset:**

- **Edge-Stud-Tile, Star-Brick, Grid-Field-Tile, Hex-Field-Tile,
  Rational-Repeat-Tile** — the studio draws the *inscribed 2D art alone*: a flat
  line-and-face drawing of the rosette / octagram / lattice, with no plate, no
  studs, no walls, no relief depth, no 3D at all. The gallery draws the solid
  those patterns are cut *into*.
- **Classic-Brick and Pin-Rail** — these declare no `pattern`, so
  `compileToGeometry` returns `emptyPiece2DResult()`
  (`bikar:packages/core/src/dsl/evaluator.ts:2455`) with **0 faces, 0 segments,
  0 circles**. The studio's 2D path therefore has nothing to draw. I expect a
  blank or near-blank canvas. This is the sharpest prediction in the report and
  the easiest to check with one screenshot.

**That it is all presets, not one, is the diagnostic fact.** A data problem
(one bad `.bkr`, one stale PNG) cannot be uniform across eight files; a missing
branch in a dispatch is uniform by construction.

Corroborating the inference at the deployed bundle: the string `brick3d` occurs
**0 times** in the deployed `editor-6xf9K3gW.js`, while `orb3d` occurs twice and
`orbMesh` three times. The shipped studio editor contains no brick-specific
rendering code whatsoever. (String literals survive minification; identifiers do
not, which is why this grep is for the former.)

### 1.3 The same engine already renders bricks in 3D — elsewhere

This is not a missing capability in bikar. `bikar:packages/lab/src/viewer.ts:1-8`
is `OrbViewer`, described in its own header as "ported from the studio's orb
preview (packages/web/src/main.ts drawOrbMesh/setupOrbCanvas)". The Lego Lab
instantiates it over a brick canvas (`bikar:packages/lab/src/lego-main.ts:138`)
and feeds it the mesh (`:1220`). So `lego.html` shows bricks in 3D and
`editor.html` does not. The gallery cards even link to it —
`lab:"lego.html?v=1&f=edge-stud-tile"` (`3d-models:index.html:462`).

---

## 2. The two pipelines, side by side

| stage | A — STUDIO | B — GALLERY |
|---|---|---|
| source | `bikar:patterns/Lego/*.bkr`, globbed into the bundle at build time (`bikar:packages/web/src/starter-patterns.ts:1-36`) | same `.bkr` files, copied in by `3d-models:Makefile:176` |
| routing | `#Edge-Stud-Tile` → file slug (`bikar:packages/web/src/hash-fragment.ts:13-31`) | hardcoded `BRICKS` array, `3d-models:index.html:450-484` |
| evaluate | `compileToGeometry` in a browser worker | same function via the CLI, `3d-models:Makefile:34` |
| geometry | `bikar:packages/core/src/kernel3d/brick.ts` → `buildBrick` | identical — same package |
| gate | none in the preview path | `--check` (mesh gate), `3d-models:Makefile:174` |
| **render** | **`if (geom.orb3d)` → 3D; else flat 2D SVG — `bikar:packages/web/src/main.ts:1985`, `:1993`** | **OpenSCAD `import()` of the STL, `3d-models:build/brick_previews.py:59-78`** |
| camera | n/a on the 2D path | `CAMERA = "0,0,0,60,0,25,0"` + `--viewall --autocenter`, `brick_previews.py:42`, `:70-72` |
| palette | n/a on the 2D path | `--colorscheme=Cornfield` (gold on cream), keyed to transparency by `process_images.py` — `brick_previews.py:73`, `:13-17` |
| post | — | `make web-images` → `build/process_images.py` (`Makefile:334-341`) |
| publish | Cloudflare Pages `bikar-studio` | `make deploy` → `gh-pages` worktree (`Makefile:356`) |

Two asymmetries worth recording:

- The 3D renderer the studio *does* have (`drawOrbMesh`,
  `bikar:packages/web/src/main.ts:1760`) is reachable only through
  `renderOrbViews` (`:1925`), whose signature demands
  `NonNullable<EvaluationResult['orb3d']>` because it builds symmetry-axis tabs
  from `orb.base` (`:1926`). A brick has no symmetry-axis view set — the gallery
  pipeline says so in its own words (`3d-models:Makefile:155-161`,
  `brick_previews.py:4-8`). So the fix is *not* "set `orb3d` on a brick"; it is
  a mesh-only view with no axis tabs. See §6.
- `make bricks` skips murals (`3d-models:Makefile:171`); `make pattern-sets`
  handles them separately (`:191-210`).

---

## 3. Evidence

### 3.1 Studio freshness, at the bundle

`https://bikar-studio.pages.dev/editor` → HTTP 200, references
`/assets/editor-6xf9K3gW.js`, `/assets/dist-Cgxo6fwq.js`,
`/assets/ch-widgets-DhMbpkqX.js`. All three fetched (269,337 / 301,664 / 4,165
bytes).

String-literal probes in `dist-Cgxo6fwq.js` (the core bundle):

| literal | count | introduced by |
|---|---|---|
| `cavity wall thins to` | 1 | `bfb1bae`'s `insetBodyCavity`, added in `bf6c602` |
| `collapsed the body outline` | 1 | same |
| `inverted the body outline` | 1 | same |

And in `editor-6xf9K3gW.js`: `Rosette-Brick` ×4 and `Seam-Coupon` ×4 — two
`.bkr` files that exist only in `bikar` `main` (`73514f1`, `bf6c602`) and not on
the branch the gallery build was pointed at.

**The deployed studio is built from `bf6c602` or later — i.e. current `main`.
It is not stale.**

### 3.2 Gallery freshness, at the artefact

- `gh-pages` HEAD: `de88ce6`, `2026-08-02 07:32:29 -0500`, "Deploy gallery from
  master (ed074c0)".
- Live `index.html` fetched from `http://blog.bytesofpurpose.com/3d-models/`
  hashes to `f2aa1e31…` — **byte-identical** to `git show gh-pages:index.html`
  and to master's working-tree `index.html`. The CDN is serving exactly what is
  on the branch.
- All eight brick PNGs are present on `gh-pages` under `build/images/web/`.
- `master` has moved to `5b4d986` since the deploy, but the three commits since
  `ed074c0` touch only `docs/`, `.claude/`, and `CLAUDE.md` — no `index.html`,
  no `build/`. Nothing renderable is undeployed.

**The gallery is not stale either.** `ASSET_VER = "20260731a"`
(`index.html:353`) has not been bumped since 2026-07-31, which *would* matter if
the PNGs had been re-rendered — see §7.

### 3.3 Commit provenance and the geometry comparison

The brief flagged that `3d-models:Makefile:33` hardcodes
`BIKAR_DIR := ${HOME}/Workspace/git/bikar`, and that this checkout sat on the
stale, remote-deleted branch `feat/edge-to-edge-relief` (`760b5cb`), 9 commits
behind `main` (`bfb1bae`). **That was true at the start of this audit and I
expected it to be the answer. It is not.**

*Empirical.* I rendered all seven single-brick presets twice — once through
`~/Workspace/git/bikar/packages/cli/dist/index.js` and once through
`~/Workspace/git/bikar-lego-lab/…`. These load two genuinely different
`packages/core/dist/index.js` builds:

| | bytes | mtime | SHA-256 (head) | has `cavity wall thins to` |
|---|---|---|---|---|
| `bikar` | 685,056 | Aug 2 06:23 | `40786bbe…` | **no** |
| `bikar-lego-lab` | 688,918 | Aug 2 13:55 | `e1533be1…` | **yes** |

`dist/` is gitignored, so these two builds are real and distinct: one predates
`bf6c602`, one includes it. Result — **all seven STLs are byte-identical by
SHA-256** (Classic-Brick, Edge-Stud-Tile, Grid-Field-Tile, Hex-Field-Tile,
Pin-Rail, Rational-Repeat-Tile, Star-Brick). Triangle counts and volumes match
exactly, e.g. Edge-Stud-Tile 14,508 triangles / 16.6 cm³ from both, and both
report `mesh gate: watertight=true euler=2 degenerate=0 minFeature=0.7568…mm — PASS`.

*Static, and independent of the above.* `git diff 760b5cb bfb1bae` over
`packages/core/src` + `packages/cli/src` touches seven files. Every change is
confined to a path the seven presets do not enter:

- `ast.ts`, `parser.ts`, `evaluator.ts` — the `footprint outline` keyword.
  Reached only via `spec.bodyOutline`; none of the seven declares it (only
  `Rosette-Brick.bkr` does, and it has no gallery card).
- `kernel3d/brick.ts` — `insetBodyCavity` on the `spec.bodyOutline` branch only.
- `kernel3d/grid-gate.ts` — `anchorability` gained a third parameter
  `outlineBody = false` (`bikar:packages/core/src/kernel3d/grid-gate.ts:345-349`).
  The default preserves the old behaviour, and the only use of it appends text
  to a failure *message*. No geometric effect.
- `render/ldraw-emitter.ts` — LDraw output; the gallery emits STL.
- `kernel3d/calibration.ts` — new `CAL-*` registrations.

Both lines of evidence agree: **the stale `BIKAR_DIR` cannot be producing a
geometry difference for these presets.** It is a real latent hazard (§6, step 4)
but it is not this bug.

### 3.4 A measurement that was invalidated mid-audit — reported, not deleted

At roughly 14:47 the `bikar` worktree read `760b5cb`. At **14:51:46** it was
checked out to `origin/main` by something outside this audit (reflog:
`bfb1bae HEAD@{2026-08-02 14:51:46 -0500}: checkout: moving from
feat/edge-to-edge-relief to origin/main`). My STL renders ran at 14:52:02 and
14:52:25 — *after* that checkout.

This briefly produced a false reading: I grepped the "stale" checkout's
`brick.ts` source for `cavity wall thins to`, found it, and concluded the
worktree was dirty. It was not; the source tree had simply been moved under me.
The STL comparison in §3.3 nevertheless survives, because the CLI loads
`packages/core/dist/`, which is gitignored and was untouched by the checkout —
verified by the differing hashes and mtimes in the table above. Had `dist/`
been rebuilt, the comparison would have been worthless and this section would
be the whole finding.

Note also that `BIKAR_DIR` now points at a **detached HEAD** at `bfb1bae`
(`git worktree list`), not at a branch.

---

## 4. Verdict

**H3 — DEFECT. Confidence: high on the cause, medium-high on the exact
on-screen symptom** (the symptom is inferred, not observed — §1.2).

The studio editor gates its entire 3D preview on `geom.orb3d`
(`bikar:packages/web/src/main.ts:1985`). A `brick` evaluation returns
`orbMesh`, `piece3d` and `brick3d` but never `orb3d`
(`bikar:packages/core/src/dsl/evaluator.ts:2455-2472`). Every brick therefore
renders as flat 2D art — or as nothing at all when it declares no art. The
gallery renders the actual print mesh. The two surfaces are showing different
*kinds of thing*, not different versions of the same thing.

**Secondary, both real but not causal:**

- *H2, partial.* `BIKAR_DIR` pointed at a 9-commits-behind branch when this
  audit began (§3.3–3.4). Proven not to affect these presets' geometry, but it
  would silently affect `make lab`, which vendors `packages/lab` from the same
  variable (`3d-models:Makefile:236-249`) — and `main` adds
  `lab/src/ldraw-preview.ts`, `ldraw-readback.ts`, `ldraw.ts`, which that branch
  lacks entirely.
- *H1, minor.* Even once bricks render in 3D, the two will not look identical:
  the studio uses an orthographic painter's-algorithm renderer with **no
  backface culling on purpose** (`bikar:packages/web/src/main.ts:1755-1759`)
  and a fixed yaw/pitch of `-0.6 / 0.35` (`:1749-1750`), while the gallery uses
  OpenSCAD Cornfield at `0,0,0,60,0,25,0` with `--viewall --autocenter`
  (`brick_previews.py:42`, `:70-73`). Expect a different angle and palette.
  That is presentation and is not worth chasing.

**What would falsify H3:** a screenshot of
`https://bikar-studio.pages.dev/editor#Classic-Brick` showing a 3D brick. Given
`brick3d` appears 0 times in the deployed editor bundle and `orb3d` is false for
every preset probed, I do not expect that — but it is the check that settles it,
and it has not been run.

---

## 5. Which pipeline is authoritative, and severity

**The GALLERY (CLI → STL) is authoritative for what gets printed**, and the
evidence supports the brief's prior rather than merely restating it:

- `make bricks` renders with `--check` (`3d-models:Makefile:174`); every one of
  the seven presets reported `mesh gate: … PASS` in §3.3.
- The repo states the reason in the pipeline itself: "a brick's claim is made by
  its two grid gates and the mesh gate, not by a render"
  (`3d-models:Makefile:157-159`, echoed at `build/brick_previews.py:6-8`).
- The STL the gallery draws *is* the download the card offers
  (`build/stls/${m.id}.stl`, `3d-models:index.html:498`).
- The studio preview path runs no gate at all.

**Severity: MEDIUM.** Nothing printable is wrong — the STLs are gated, correct,
and identical across both checkouts. What is broken is comprehension: the
studio is the surface an author edits a `.bkr` in, and for the whole `brick`
family it shows them something that is not the piece. For `Classic-Brick` and
`Pin-Rail` it plausibly shows them nothing, which reads as "the studio is
broken" rather than "this view does not apply here". A user comparing the two
surfaces, as this user did, reasonably concludes one of them is lying.

It is *not* high severity precisely because the authoritative path is intact.
Had the defect been on the gallery side it would be high — that render is the
only picture anyone has of a mesh no `qiyas` view set covers.

---

## 6. Prioritized plan

**Step 0 — confirm the symptom (blocks everything below).**
Open `https://bikar-studio.pages.dev/editor#Classic-Brick` and
`#Edge-Stud-Tile` in a browser and screenshot both.
*Touches:* nothing. *Check:* `#Classic-Brick` shows a blank/near-blank canvas
and `#Edge-Stud-Tile` shows flat art with no plate. If either shows a 3D brick,
stop — §4 is wrong and this plan does not apply.

**Step 1 — render the mesh in the studio editor when there is a mesh but no
orb.** *Touches:* `bikar:packages/web/src/main.ts` around `:1985`.
Split the mesh-only view out of `renderOrbViews` (`:1925`), which currently
requires `orb3d` solely to build symmetry-axis tabs from `orb.base` (`:1926`) —
tabs a brick must not have. Add a branch: when `geom.orbMesh` is present and
`geom.orb3d` is not, call `setupOrbCanvas(geom.orbMesh)` (`:1839`) with no tab
bar. `drawOrbMesh` (`:1760`) needs no change; `OrbMeshLike` is
`EvaluationResult['orbMesh']` (`:1753`) and a brick already populates that field.
*Check:* a `packages/web` test asserting that a source containing a `brick`
declaration produces a 3D canvas and zero `.orb-view-btn` elements — red before,
green after. Then re-run step 0's screenshots.

**Step 2 — surface the brick's own facts beside the mesh.**
*Touches:* the same region of `bikar:packages/web/src/main.ts`.
`brick3d` (`evaluator.ts:375-383`) carries the solved footprint, anchor report,
grid-fit score and warnings — the studio currently reads none of it (`brick3d`:
0 occurrences in the deployed bundle). At minimum show the V8/V12/V13 warnings
the CLI prints; `Hex-Field-Tile` grid-fit 0.48 and `Star-Brick`'s V13 dead-border
warning are exactly the feedback an author editing a `.bkr` needs.
*Check:* loading `#Hex-Field-Tile` displays the 0.48 grid-fit score, matching
the CLI's `grid fit: 0.48 at 15.0°` and the gallery card's `grid fit 0.48`
(`3d-models:index.html:473`).

**Step 3 — make the two surfaces' preset lists agree.**
*Touches:* `3d-models:index.html:450-484`.
The studio bundle ships `Rosette-Brick` and `Seam-Coupon`; the gallery's
hardcoded `BRICKS` array has 8 entries against 10 `.bkr` files in
`bikar:patterns/Lego/`. A visitor who sees a preset in one place and not the
other has a second, smaller version of this same complaint. Decide deliberately
whether each belongs (`Seam-Coupon` is a coupon, and may well not).
*Check:* a count assertion, or an explicit comment naming each omission and why
— the file already carries that habit at `:479-480`.

**Step 4 — remove the staleness that made this invisible.**
*Touches:* `3d-models:Makefile:33`.
`BIKAR_DIR` is a bare path with no ref discipline; it spent this audit pointing
first at a 9-commits-behind deleted branch and now at a detached HEAD. It did
not cause this bug, but it is the mechanism by which the next one would ship
silently — `make lab` vendors the Lego Lab through the same variable
(`:236-249`), and the branch it pointed at lacks `ldraw-preview.ts`,
`ldraw-readback.ts` and `ldraw.ts` outright.
Cheapest sufficient fix: have `bricks`/`lab-vendor` print
`git -C $(BIKAR_DIR) rev-parse --short HEAD` and its branch, and fail on a dirty
tree. This is in the spirit of `.claude/gates/doc_pointers.py`, which already
holds sibling-repo pointers *to a git ref* rather than to whatever is checked
out (`CLAUDE.md`, K9 / pointer gate).
*Check:* run `make bricks` with `BIKAR_DIR` on a deliberately old ref and
confirm it refuses or announces the ref; the STLs it writes should still be
byte-identical, per §3.3.

**Step 5 — bump `ASSET_VER` if and only if a render changes.**
*Touches:* `3d-models:index.html:353`.
Only relevant once steps 1–3 cause a re-render. See §7 — I could not determine
whether the current PNGs post-date the last `ASSET_VER` bump.

Steps 1 and 2 are one PR in `bikar`. Steps 3–5 are one PR in `3d-models`. They
are independent.

---

## 7. Open questions / what I could not verify

1. **The studio's actual appearance was never seen.** Both browser tool-chains
   failed (see the provenance header). §1.2 is inference from the dispatch line
   plus a local probe of the same entry point, corroborated by `brick3d`
   appearing 0 times in the deployed bundle. It is strong, and it is still not
   an observation. Step 0 exists for this.
2. **Whether the gallery PNGs are older than `ASSET_VER = "20260731a"`.** The
   PNGs are on `gh-pages` and the CDN serves them, but I did not compare their
   bytes against a freshly-rendered pair — that needs OpenSCAD, which I did not
   invoke. If `make bricks` has run since 2026-07-31 without an `ASSET_VER`
   bump, some visitors may hold a cached older PNG. The two I fetched look
   correct for their specs, so I have no positive evidence of a problem.
3. **Which bikar commit the deployed studio is built from, exactly.** I pinned
   it to "`bf6c602` or later" via three string literals and the presence of
   `Rosette-Brick` / `Seam-Coupon`. I did not find a build-stamp literal that
   would name the commit outright. Adding one would make this check trivial next
   time.
4. ~~**`Rosette-Brick` and `Seam-Coupon` were not probed** for `orb3d`.~~
   **Closed 2026-08-02 by a follow-up probe** (same `compileToGeometry` entry
   point, all ten `patterns/Lego/*.bkr` rather than the seven above). Every one
   returns `orb3d=false` and `orbMesh=true`, so the §4 verdict covers the whole
   directory, not just the carded presets:

   | preset | `orb3d` | `brick3d` | `orbMesh` | 2D fallback (faces / segs) |
   |---|---|---|---|---|
   | `Classic-Brick` | false | true | true | 0 / 0 |
   | `Edge-Stud-Tile` | false | true | true | 50 / 12 |
   | `Grid-Field-Tile` | false | true | true | 18 / 36 |
   | `Hex-Field-Tile` | false | true | true | 18 / 36 |
   | `Pin-Rail` | false | true | true | 0 / 0 |
   | `Rational-Repeat-Tile` | false | true | true | 132 / 60 |
   | `Rosette-Brick` | false | true | true | 31 / 100 |
   | `Seam-Coupon` | false | **false** | true | 4 / 8 |
   | `Star-Brick` | false | true | true | 18 / 8 |
   | `Star-Mural` | false | **false** | true | 162 / 72 |

   Two things this adds to §6. **`orbMesh` is populated on every preset**, so
   step 1 is a dispatch change and needs no new geometry — the mesh the gallery
   renders is already in the object the editor holds. And the `faces=0, segs=0`
   rows put a floor under §1.2's inference: `Classic-Brick` and `Pin-Rail` have
   no 2D art for the fallback to draw, so the fallback cannot be showing the
   user anything. `Rosette-Brick` (the only `footprint outline` preset) behaves
   as the others do, so step 1's hand-check of it is a confirmation, not a risk.
   Still not an observation of the screen — step 0 stands.
5. **`Star-Mural` is a different case and I did not chase it.** It returns
   `piece3d` and `orbMesh` but `brick3d=false`, and the gallery builds it
   through `make pattern-sets` (`Makefile:191-210`) from a *composed, ungated*
   panel STL rather than the gated per-piece files. Step 1 would give it a 3D
   preview too, but whether the studio should show the composed panel or one
   piece is a product question this audit did not open.
6. **Why `bikar`'s worktree was on a deleted branch at all**, and whether
   anything was built and shipped from it, I did not investigate. The reflog
   (§3.4) shows the checkout to `origin/main` at 14:51:46 today was made outside
   this audit; I do not know by whom or why.
