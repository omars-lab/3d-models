# Spaced Rosette — a rosette as individual pieces on a spaced grid — design doc

Status: **v1 plan — drafted 2026-09-02, after a live concept prototype (this session) that
the owner drove to two decisions below. Not yet built; not yet grounded by an adversarial
audit (that comes when the language surface firms up, as it did for the mural).** No claim
here rests on a printed part.

Scope: lay a Rosette-*n* out as its **own** pieces — bikar's decomposition is already exactly
*n* hexagon petals + 1 central star — each printed on its own and placed on a grid whose
inter-piece **spacing is a tunable dial**. At spacing zero the pieces compose the rosette; open
the dial and they step apart. This is the "spacing for dials" the owner asked for, applied to
the rosette's natural pieces.

Builds on / evolves:
- [`lego-pattern-set-design.md`](lego-pattern-set-design.md) (the `mural`) — this is its sibling
  and, in one axis, its **opposite**: see §1.
- [`rosette-pin-explorer-design.md`](rosette-pin-explorer-design.md) — the shipped page that
  already draws these *n*+1 pieces and their anchors; the dial lives here (§4).
- [`lego-lab-design.md`](lego-lab-design.md) — the `brick` declaration and anchor solver a
  spaced piece still is.

**Decisions locked by Omar, 2026-09-02**, from the concept prototype (Spaced Rosette, this
session — an artifact drawing the real geometry with the two toggles live):
1. **Radial layout** is the primary — the rosette blooms outward and keeps its symmetry (the
   star holds the centre). A rectangular "sheet" layout stays available for the print bed (§3).
2. **Both mounts ship**, as a `snap studs` toggle: **continuous** (any-mm gap, a dedicated
   spaced mount) and **snap-to-studs** (gap quantised to whole 8 mm studs, so the array still
   seats on a stock LEGO baseplate). Neither is a fallback (§3).

---

## 1. Goals, non-goals, and the one axis that separates this from the `mural`

**Goal.** One rosette → *n*+1 individually-printed pieces on a spaced grid, spacing driven by a
dial, in the rosette explorer first (diagnostic) and as a bikar declaration second (product).

**The `mural` is the same inter-piece gap driven to the opposite end.** The
[`mural`](lego-pattern-set-design.md) takes one *continuous* pattern, **cuts** it into rectangular
tiles, and drives the seam to the physical minimum (0.2 mm) so the art runs edge-to-edge — which
is why it needed a kernel rebuild (its §7, Milestone A) to let relief cross piece boundaries. The
spaced rosette does the reverse on all three counts, and that is the whole reason it is a separate
doc, not a `mural` mode:

| | `mural` | spaced rosette |
|---|---|---|
| decomposition | **cuts** a pattern into a c×r grid | uses the pattern's **own** pieces (no cut) |
| the gap | driven to the 0.2 mm physical minimum | **opened** as a tunable dial |
| art across the gap | continuous (relief crosses seams) | deliberately **separated** (whole pieces) |
| kernel work | Milestone A, edge-to-edge relief | **none** — see §2 |

**Non-goals.** Cutting a pattern (that is the `mural`); carrying relief across a gap (there is no
shared seam here — every piece is whole); colour; and any claim that a *continuous*-mount array
mates a stock baseplate (it does not — §3, and this is the K2 line the doc must not cross).

## 2. The pieces are bikar's, and spacing never touches them

bikar's `rosetteGeometry` already yields the decomposition: one reference petal solved on the
axis, rotated *n* times, giving **n hexagon petals**, plus **1 star** built from the petals' inner
vertices (adjacent petals share their outer corner, so the star is a 2*n*-gon). That is *n*+1
pieces — the exact port [`rosette-pin-explorer-design.md`](rosette-pin-explorer-design.md) §2
documents and the shipped explorer draws. Nothing in this feature re-derives it.

**The load-bearing simplification: spacing is a *placement* transform, not a geometry edit.** Each
piece keeps its outline; only its position changes. This is the finding the prototype made
concrete, and it collapses most of the plan:

- **No kernel change.** The `mural`'s hard part — relief that survives crossing a piece boundary —
  does not arise, because pieces are never cut and no relief crosses anything. The spaced rosette
  needs neither Milestone A nor any new `kernel3d` geometry.
- **The anchor solve is unchanged per piece.** Each piece's tube/pin/none verdict is a function of
  its *outline*, which spacing does not alter. In the explorer's shared-baseplate model, moving a
  piece re-registers it against the studs (which studs it covers can change) — so spacing feeds the
  existing `solveAnchorsOnGlobalGrid` re-registration, it does not modify it.
- **Individual printing already exists.** bikar exports one STL per piece via `--format parts`
  (the `mural`'s Milestone B path); a spaced layout is a placement of those parts.

## 3. The layout, and the two mounts (the K10 line)

**Radial (primary).** Translate each piece outward along the direction from the rosette centre to
its own centroid, by the spacing gap; the star's centroid is the centre, so it stays put. The
figure keeps its *n*-fold symmetry and reads as a rosette at every gap. **Rectangular sheet
(secondary).** Place the *n*+1 pieces in a grid of equal cells sized to the largest piece plus the
gap — the print-bed / catalogue view. Both were in the prototype; the owner chose radial as the
hero.

**The mounts, and the transfer condition (K10).** The 8.0 mm stud pitch and the 0.2 mm inter-brick
gap are **physical LEGO constants** grounded in the [seam
survey](research/lego-baseplate-seam-survey.md) — they describe brick moulding, not this feature's
grout. A spaced grid adds a **new pitch on top of the lattice**, and whether that still mates a
stock baseplate depends entirely on *how* the gap lands:

- **Snap-to-studs.** The gap is quantised to whole studs (8 mm steps), so every piece origin stays
  on the baseplate lattice and the array **seats on a stock LEGO baseplate**. The dial is coarse.
- **Continuous.** The gap is any millimetre value; the array no longer sits on integer studs, so it
  is **not** a stock-baseplate mount — it needs its own printed spaced mount. The dial is smooth.

The transfer sentence, written so it cannot be silently ported: *snap-to-studs inherits stock
baseplate compatibility because it never leaves the 8 mm lattice; continuous does not, and the doc
must never call a continuous array "baseplate-compatible."*

## 4. The dial — a schema param, not bespoke UI

The rosette explorer's dials are **generated from a pattern's declared `param` specs** (its
Track 2, shipped): `compileToGeometry(src).params` returns one spec per `param` line, and
`buildPatternDials` renders a dial for each. So the honest path makes spacing a **declared
parameter**, and the dial appears with no per-pattern UI code:

- a `spacing` param (mm, floored at 0, default 0 → composes the rosette);
- a `snap studs` toggle (§3), which the schema surfaces as a boolean control.

Sequenced work (small, because §2 removed the kernel item):

1. **Explorer dial (diagnostic, first).** Add spacing as a placement transform in the explorer's
   layout step and a `snap` toggle; the pieces already draw, the anchor re-solve already runs.
   Radial primary, sheet secondary. This is where "watch the rosette bloom, and watch which pins
   drop as it re-registers" becomes visible — the explorer's own reason to exist.
2. **bikar declaration (product, second).** A layout that emits the *n*+1 pieces at their spaced
   positions via `--format parts`, with `spacing` / `snap studs` as declared params so the
   explorer dial is schema-driven rather than hand-wired. Scoped in a follow-up once the explorer
   confirms the geometry.
3. **This doc's grounding pass** when the language surface firms up (the `mural`'s C4 precedent).

## 5. Validators

### 5.1 Piece conservation

**Validator:** the spaced layout emits exactly the pieces the rosette has, at every spacing.
PASS: for *n* = 8, the layout returns 8 petals + 1 star = 9 pieces at spacing 0 and at spacing 40 mm.
FAIL: a layout that drops the star (centroid-at-centre, zero translation) and returns 8.

### 5.2 Snap-mode registration

**Validator:** in snap-to-studs, every piece origin lands on an integer multiple of the 8 mm pitch.
PASS: spacing 12 mm snaps to 8 mm (one stud), every origin on the lattice.
FAIL: spacing 12 mm placed at a raw 12 mm in snap mode — origins 12 mm apart, off the lattice, while
the readout still claims baseplate compatibility (the §3 line crossed).

### 5.3 Continuous-mode honesty

**Validator:** a continuous-mount layout is never reported as stock-baseplate compatible.
PASS: continuous at 3 mm labels the mount "dedicated / off-lattice".
FAIL: the same layout labelled "seats on a stock baseplate" (the K2 non-goal asserted).

## 6. What gates each step

- **Explorer dial** — unblocked; needs only the work. No printer, no kernel change (§2). This is
  the first deliverable and the one the owner can see move.
- **bikar declaration** — unblocked engine-side; a normal bikar PR (grammar, params, `--format
  parts`, tests, a decision doc), sequenced after the explorer confirms the layout.
- **The empirical residue is already someone else's bet.** Whether a *snap-to-studs* spaced array
  actually seats on a printed-onto-stock plate is plate fit and stud entry — the same measurements
  the LEGO coupons in [`backlog.md`](backlog.md) §3.2 already hold (held on a printer). Per the
  grounding process, one measurement is one bet: this feature mints **no** new bet, it inherits
  those. A *continuous* mount is a new printed object whose own fit is the same wall.

## 7. Provenance

The geometry, dimensions, and anchor rules are bikar's, grounded line-by-line in
[`rosette-pin-explorer-design.md`](rosette-pin-explorer-design.md) §2 and §4 and its checked-in
[audit](research/rosette-pin-explorer-grounding-audit.md); this doc adds no new number. The two
decisions in the header were made by the owner against a live prototype (this session) that draws
the real pieces with the radial/grid and continuous/snap toggles. The `mural` relationship (§1) is
read against [`lego-pattern-set-design.md`](lego-pattern-set-design.md) directly.
