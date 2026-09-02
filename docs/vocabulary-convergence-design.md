# Vocabulary convergence — one face-list vocabulary across the d3 surfaces and sacred-patterns

**Status:** Shipped 2026-09-02 (A↔B rename bikar #151 `1083046`; grow-C sacred-patterns #45 `76e3c17`). Settles plan §2 row 2.4 / d3 doc §4 Phase 3
(Q-VOCAB). Two research files on disk ground it: the vocabulary survey
([`research/vocabulary-survey-q-vocab.md`](research/vocabulary-survey-q-vocab.md)) and the
sacred-patterns rendering-architecture read
([`research/sacred-patterns-render-arch.md`](research/sacred-patterns-render-arch.md)). No
empirical residue — this is a naming-and-structure change decided by tests, not by a printer
(Appendix B). Reversal condition recorded as D-050 in
[`decisions-log.md`](decisions-log.md).

## 1. What this settles

The [d3 integration](d3-integration-design.md) shipped two surfaces that draw Islamic-geometry
faces with d3 — the `/rosette-explorer` (**Surface A**) and the `/orb-instrument` (**Surface
B**) — and a fourth repo, sacred-patterns (**Surface C**), draws the same *kind* of figure with
its own, older vocabulary. Q-VOCAB asked whether to share that vocabulary or keep C a separate
gallery. The owner decision (d3 doc §5.3 item 3, resolved 2026-08-31) is neither "import C's
names as-is" nor "leave it": **converge on one common naming convention, refactoring either side
to get there.** This doc names that convention from source and states the work each surface
needs to reach it.

The **deciding fact**, measured in the survey: the three surfaces disagree by *two different
magnitudes*, not one. A and B differ by a **thin rename** — they already share d3's
`.data().join()` model and a face-list shape; only two field names collide (§2). C differs by a
**structural gap** — it has no face-list and no data-join at all; it constructs geometry and
serializes it to SVG inline, discarding it (§4). One convergence, two efforts: rename A↔B to fix
the canon, then grow C the missing layer so its names have something to attach to.

### 1.1 Non-goals

- **Not** a bikar-core d3 dependency. Core stays rendering-agnostic; the face-list
  (`FaceConstruct`) already lives in `packages/core/src/viz/` and the join
  (`joinFaces`) in `packages/web/src/` — a web concern, not a kernel one. Convergence
  moves names, it does not move the layering.
- **Not** a cross-repo build dependency from the bikar explorers *into* sacred-patterns. The two
  keep separate build graphs; they converge on **names and shapes**, so a reader moving between
  them meets one vocabulary — not on a shared package. (This is the lighter half of the Q-VOCAB
  fork: "share the vocabulary" ≠ "import the code".)
- **Not** a visual redesign of any surface. Every pixel sacred-patterns emits today it must
  still emit after (§6, the golden-file validator); the refactor is invisible in the output.
- **Not** colour, animation, or curved-face vocabulary. C has no curved primitives and A/B's
  `isCurved` has no C analog; that field stays bikar-only until a curved figure needs it.

## 2. The canonical shared vocabulary

Locked from bikar source — A is the reference surface (d3 doc §4 Phase 1), so where A and B
disagree, **A's name wins** and B is renamed to it. Five load-bearing terms:

| term | meaning | source of truth |
|---|---|---|
| `index` | a face's **identity ordinal** — its raw position in the geometry's face list, the key every per-face map and the data-join is keyed by | A: `FaceConstruct.index`, `packages/core/src/viz/face-constructs.ts` |
| `polygon` | a face's **boundary** — the closed, ordered ring of points, in pattern units | A: `FaceConstruct.polygon`, same file |
| `ring` | a **concentric styling index** — which rosette ring a face sits in, for `ring ==` style rules; **not** a boundary and **not** an identity | A: `FaceConstruct.ring?`, same file |
| `faceKey(f)` | the **shared join key** — `String(f.index)`, the one written convention for keying a face; A's `joinFaces()` uses it by default and B's status-binding join calls it directly, so both surfaces key a face the same way | A: `faceKey`, `packages/web/src/viz-d3.ts` |
| `joinFaces()` | A's **path-creating enter/update/exit data-join** — `selectAll('path.face').data(constructs, faceKey).join('path')` | A: `joinFaces()`, `packages/web/src/viz-d3.ts` |

The collisions to remove (measured in the survey, §"divergence summary"):

| surface | today | → canonical | why it collides |
|---|---|---|---|
| B | `FaceStatus.faceIndex` | `index` | same concept as A's `index`, spelled differently — a reader can't tell they're one thing |
| B | `SvgFace.ring` (holds the **boundary**) | `polygon` / `boundary` | B's `ring` names the boundary; A's `ring` names the concentric index. Same word, two meanings — the worst collision, because it reads as agreement |
| B | face join **keyed ad-hoc** | adopt the shared `faceKey` as the join key | the two surfaces must key a face the same way or "shared vocabulary" is a fiction at the join. B keeps its own `.data().join()` **by design** — it binds `FaceStatus` onto the pre-rendered `<path data-face-index>` nodes and asserts enter/exit are empty, which the path-*creating* `joinFaces()` cannot do; what converges is the key, not the call |
| B | `ringKey()` (keyed on the boundary) | a boundary-keyed name (e.g. `boundaryKey()`) | follows the `ring`→`polygon` rename so the key's name matches what it keys on |

After the rename, `ring` means exactly one thing across A and B (concentric styling index),
`index` means exactly one thing (face identity), and both surfaces key their face joins by the
same `faceKey` — A through `joinFaces()`, B through its own status-binding join.

## 3. The three surfaces today (grounding)

Full tables are in the survey; the shape that matters here:

- **A — rosette explorer.** `FaceConstruct` (`face-constructs.ts`) is the compiled-geometry →
  face-list record; `faceConstructs()` maps `EvaluationResult.faces` to it; `joinFaces()`
  (`viz-d3.ts`) binds it. This is the reference model both other surfaces converge toward.
- **B — orb instrument.** Has a face-list shape (`SvgFace`) and a status record
  (`FaceStatus`), but names them differently (`faceIndex`, `ring`-as-boundary) and inlines its
  own `.data().join()` instead of calling `joinFaces()`. A **thin rename**, no new structure.
- **C — sacred-patterns.** OO primitives (`Point`/`Line`/`Circle`/`Polygon`/`Star`) whose
  boundaries are lazy `points` getters; eight `draw*` functions construct geometry and emit SVG
  **inline** through `canvas.ts`'s five `append*` helpers (30 call sites in `index.ts`, 23 of them `appendPolygon` across seven `draw*` functions), keeping **no
  face-list** and using d3 only as a DOM shim — never `.data()`/`.join()`
  ([`research/sacred-patterns-render-arch.md`](research/sacred-patterns-render-arch.md) §2–4). A
  **structural gap**, not a rename.

## 4. The sacred-patterns structural refactor (the C work)

C cannot adopt the vocabulary by renaming, because the things the words name — a face-list, a
keyed data-join — do not exist in it yet. Grow them. The seam is shallow (arch read §6): d3 is
**already** a sacred-patterns dependency (`d3@^7.9.0`, used as a DOM shim), so no new dependency;
the geometry layer needs **zero** changes; two new modules slot in and the eight `draw*` render
call sites regroup.

1. **New `sacred-patterns/src/ts/faces.ts`** — a `faceConstructs()`-analog: a pure function mapping a
   `Polygon[]`/`Star[]`/`Circle[]` collection to a `FaceConstruct`-shaped array (`index`,
   `polygon`, `centroid`, `classes`, optional `ring`). It reuses the existing `.points`/`.lines`
   getters verbatim — a thin adapter, exactly as bikar's `faceConstructs()` is a thin adapter
   over `EvaluationResult.faces`. Honors sacred-patterns' **relative-to-origin** rule
   (`sacred-patterns/CLAUDE.md`): every coordinate stays a ratio of the originating circle's
   `(cx,cy)`/`R`; the mapper introduces no absolute or pixel coordinates. Typed interface, not a
   `Record<string,unknown>` bag (Tenet 15); pure/immutable (Tenet 10).
2. **New d3 data-join renderer** — a `joinFaces(g, constructs, opts)` mirroring
   `bikar/packages/web/src/viz-d3.ts`: `selectAll('path.face').data(constructs, key).join('path')`,
   key `String(f.index)`, emitting one `<path class="face">` per face in place of per-shape
   `<polyline>`.
3. **Regroup the eight `draw*` call sites** — each changes from *N* inline `appendPolygon(...)`
   calls to: build the shape array → map to `FaceConstruct[]` → one `joinFaces()` call. Mechanical
   for the six static drawings. The two animated ones (`drawRotatingCircles`,
   `drawCirclesRecursively`) mix polygon + circle emission with a `.transition()` spin
   (`rotateOuterCircles`); their spin runs through the d3 `.join()` **update** branch — a distinct
   code path the join already supports, not a new mechanism.

**What does not change:** the geometry classes (`Circle`/`Polygon`/`Star` and their getters), the
relative-to-origin coordinate discipline, and — crucially — the emitted pixels.

## 5. Options, and the chosen direction

**Option 0 — do nothing (rejected).** Leave C a separate gallery with its own names. Cheap now,
but it verifies nothing and permanently forks the vocabulary the d3 stream was built to unify;
"one convention" becomes two dialects, and the next surface has to pick one. Rejected: it is the
"do nothing is not neutral" trap — the fork is a standing cost paid at every future surface.

**Option A — thin rename only, A↔B (deferred, not sufficient).** Fix the A/B collisions and stop.
Real value (it removes the `ring` double-meaning), but leaves C — the surface with the actual
Islamic-geometry catalogue — outside the convention. Adopted as **step one**, not the whole job.

**Option B — full convergence, refactor C (CHOSEN).** A↔B rename **and** grow C the face-list +
data-join layer so its vocabulary attaches to real structure. This is the owner's selection
("full convergence, refactor C"). It is the robust-over-cheap call
(`3d-models/CLAUDE.md`): the deeper refactor deletes the divergence rather than routing around it,
and it is the only option under which all three surfaces read one vocabulary.

**Recommendation:** Option B, sequenced A↔B first (§7) so the canon is fixed before C is grown
against it.

## 6. Validators

Each is checkable in the surface's own test suite; a rename that skips these is how the `ring`
collision would silently survive.

**Validator:** after the A↔B rename, the token `faceIndex` and any boundary-holding `ring` field
appear **nowhere** in bikar's web sources — one grep proves the collision is gone, not just
shadowed.
PASS: `grep -rE '\bfaceIndex\b' packages/web/src` returns nothing, and every remaining `.ring`
in web sources is the concentric styling index (typed as such), never a boundary.
FAIL: `SvgFace` still carries a `ring` field holding a point array while `FaceConstruct.ring` is
a number — the two-meanings collision the rename exists to remove, now merely split across files
so no single grep catches it.

**Validator:** B keys its face join by the shared `faceKey`, not an ad-hoc key — the orb
instrument's status join and A's path join identify a face the same way.
PASS: the `/orb-instrument` page imports `faceKey` from `viz-d3` and its `.data(faces, …)` key
function returns `faceKey(d)`; the one written keying convention (`viz-d3.ts`, where `faceKey` is
"shared by every face join") has a single definition and two callers.
FAIL: the page hard-codes its own key expression (a bare inline `String(d.index)`, or a different
field) so the two surfaces could key the same face differently — the divergence the shared key
exists to remove, now merely hidden across two call sites. B keeping its *own* `.data().join()`
is **not** a failure: it binds status onto existing nodes, a structurally different join from A's
path-creating one (§2).

**Validator:** sacred-patterns' output is **pixel-identical** across the C refactor — the
face-list is an internal seam, invisible in the SVG. This is the load-bearing by-design case: a
refactor that changes a coordinate is a regression, not a convergence.
PASS: `node test/regression/capture-baseline.js` regenerated once (deliberately, for the
`<polyline>`→`<path>` element-name change), then `sacred-patterns/test/regression/check.js` passes with the same
count of boundaries and the same sorted set of point strings as before the refactor.
FAIL: any face's boundary point-string differs from the pre-refactor baseline, or the boundary
**count** changes — the mapper dropped, merged, or reordered a face's vertices.

**Validator:** C's face-list mapper is origin-relative — it introduces no absolute coordinate
(`sacred-patterns/CLAUDE.md` relative-to-origin rule).
PASS: every field the mapper writes is derived from an input primitive's `(cx,cy)`/`R`; a unit
test scaling the originating circle by *k* scales every `FaceConstruct.polygon` point by *k*.
FAIL: the mapper hard-codes a pixel offset or a bare constant (an `R*0.52`-style literal), so the
same figure at two scales yields non-proportional face lists.

## 7. Build plan and sequencing

Two PRs, one per repo, in order — the canon is fixed before C is built against it:

1. **bikar (A↔B rename)** — fresh bikar worktree. Rename `FaceStatus.faceIndex`→`index`; rename
   B's boundary-holding `ring`→`polygon`/`boundary` and `ringKey()`→a boundary-keyed name; factor
   the shared `faceKey` into `viz-d3` and key the orb-instrument page's status join by it. Tests fail-before / pass-after
   (the grep validators of §6 as unit assertions). Full `npm run ci` green (grammar conformance,
   keywords snapshot, pointers, decisions). Merge to bikar main.
2. **sacred-patterns (grow C)** — fresh sacred-patterns worktree. Add `sacred-patterns/src/ts/faces.ts` and the
   `joinFaces` renderer; regroup the eight `draw*` call sites; regenerate the golden baseline
   deliberately (`capture-baseline.js`) as part of the same change, with the diff called out in
   review. Honor Tenets 10/15 and relative-to-origin. `make local.ci` green. Merge to
   sacred-patterns master.
3. **3d-models (record the ship)** — plan §2 row 2.4 → 🟢 + a §3 row; d3 doc §4 Phase 3 →
   shipped; D-050 in the decisions log with the reversal condition; memory bullet. Same PR moves
   §2 and §3 (plan currency rule).

Each repo's change is self-contained and independently revertible — no stacked PRs, no cross-repo
merge ordering beyond "canon before C".

## 8. Open questions

- **B's `ring`→`polygon` vs `boundary`.** A already spells the boundary `polygon`
  (`FaceConstruct.polygon`), so `polygon` is the convergent choice; `boundary` is more literal
  but introduces a *third* word for a thing A already named. Leaning `polygon` for exact A-match;
  settle at rename time by which reads clearest against A's call sites.
- **C's `classes` source.** bikar's `FaceConstruct.classes` carries category tags the kernel
  emits; sacred-patterns has no equivalent tagging today (`LineTheme` is per-append styling, not
  per-face class). The mapper can leave `classes` empty initially — the field exists for
  vocabulary parity; populating it is a later, separate enrichment, not part of convergence.
- **The two animated C drawings.** Whether the `.transition()` spin is cleanest expressed through
  the `.join()` update selection or kept as a post-join imperative `.transition()` is a
  render-detail call best made against the actual d3 update branch during step 2; both preserve
  the pixels.

## 9. Transfer conditions (K10)

Porting bikar's face-list model into sacred-patterns carries a rule across a repo boundary; the
sentence that must hold:

> The `FaceConstruct` shape (`index` = list-position identity, `polygon` = origin-relative
> boundary, keyed data-join on `String(index)`) transfers to sacred-patterns **because** both
> surfaces draw a static set of closed straight-edged faces derived from an originating circle,
> and both need per-face identity for enter/update/exit. It transfers **only** in that scope.

Where it does **not** transfer, stated so it is not assumed:

- **`isCurved` does not transfer.** sacred-patterns has no curved primitives; every boundary is
  straight `Line` segments. The field stays bikar-only until a curved C figure exists to need it
  — importing it now would be a bag field with no producer (Tenet 15 violation).
- **`ring` transfers only where a concentric index exists.** C's one grouping analog is
  `Circle.metadata.level` (recursion depth), and it is **Circle-only** — `Polygon`/`Star` have no
  ring. The mapper writes `ring` only for faces that have a real concentric index; it does not
  synthesize one, and it does not reuse `level` as a `ring` for shapes where "ring" would mean
  nothing.
- **The identity key transfers, the identity *ordering* does not.** `String(index)` keys the
  join in both, but A's `index` is a position into `EvaluationResult.faces` (kernel order) and
  C's is a position into whatever order the `draw*` builds its shape array. The key works within
  each surface for enter/update/exit; it is **not** a cross-surface identifier (a face #3 in A is
  not "the same" as face #3 in C).

## Appendix A — survey sources

- [`research/vocabulary-survey-q-vocab.md`](research/vocabulary-survey-q-vocab.md) — the
  cross-surface vocabulary tables (A/B/C) and the divergence measurement (thin-rename A↔B vs
  deep-refactor C), read from bikar and sacred-patterns source at the pinned commits in its
  provenance header.
- [`research/sacred-patterns-render-arch.md`](research/sacred-patterns-render-arch.md) — the
  sacred-patterns rendering-architecture read: render entry path, the `append*` layer, the
  primitive object model, d3-as-shim, the golden-file constraint, and the refactor seam.
- Primary source of the canonical names: bikar's `packages/core/src/viz/face-constructs.ts`
  (`FaceConstruct`, `faceConstructs()`) and `packages/web/src/viz-d3.ts` (`joinFaces()`).

## Appendix B — bets and empirical residue

**None.** Convergence is a naming-and-structure change decided entirely by tests — the grep
validators, the shared-key assertion, and the pixel-identical golden-file check of §6. Nothing
here waits on a printed object or a physical measurement, so no `CAL-*` bet is registered and the
status line's "no empirical residue" claim holds. The one by-design failure case that carries the
weight is the golden-file validator: the refactor must leave sacred-patterns' output
pixel-identical, and the baseline regeneration is the deliberate, reviewed exception — not a
silent drift.

---

*Provenance: written 2026-09-02 for plan §2 row 2.4 / d3 doc §4 Phase 3 (Q-VOCAB). Grounded in
the two research files linked in Appendix A, read from bikar@5b9fb27 and sacred-patterns@0d3ad1e.
Owner decision "full convergence, refactor C" (D-050). No network sources — the canonical
vocabulary is read from checked-in sibling source.*
