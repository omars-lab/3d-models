# Text emit on printed parts — implementation design doc

Status: **v1 — grounded in two research files and one reversal.**
[`research/text-emit-survey.md`](research/text-emit-survey.md) measured the
single-stroke centreline route and found it needs a polygon offset this repo does
not have; [`research/outline-font-emit.md`](research/outline-font-emit.md) then
measured the outline-font route the survey had talked itself out of, over eight
faces and 296 glyphs, and found it needs no offset at all. **The survey's §4 and
§5.3 carry marked corrections**; everything else in it stands.

Scope: closing the gap [`calibration-design.md`](calibration-design.md) §3.2
records — *"bikar has no text emit. There is no `text`, no emboss, no engrave"* —
which §8 of the same doc calls the machine card's biggest structural weakness,
because a card whose 23 coupons cannot say which rung they are is a card you have
to keep in order by hand.

Deliverable: a rung label that survives being printed and read. `MC-4 R12`,
emitted onto the coupon it names, legible at arm's length, with the gate that
would have caught it if it were not.

Builds on: [`calibration-design.md`](calibration-design.md) (§7's 23-row
expectation table is what the labels are *for*, and D-014's mesh gate is where a
text failure should surface). Rides:
[`piece-composition-design.md`](piece-composition-design.md) — text is a feature
on a piece, not a piece.

---

## 1. The decision

**Bake outline-font glyph contours into a build-time constant, and extrude
them.** No offset, no union, no runtime font parser.

The reasoning is short because the measurement is:

- A TrueType/CFF glyph is **already closed contours with counters as holes**.
  The survey's whole problem — a centreline has no width, so it needs an offset,
  so it needs a union — does not arise.
  ([`research/outline-font-emit.md`](research/outline-font-emit.md) §0, §2.)
- The flattening runs in a **build script**, so what ships is 13,710 bytes of
  coordinates against a single-stroke face's 7,503 — under 2×, for a route that
  adds no geometry machinery to the engine (§3 of the research).
- Six of the eight faces measured need no union for these 37 glyphs, and the
  condition is **checkable per font at bake time** (§2 of the research).

### 1.1 The case against, stated before the case for

Four things are genuinely worse under this route than under a single-stroke font,
and none of them is a reason to change the decision:

1. **The font becomes a correctness input.** DM Sans draws `A B H Q R` as
   overlapping contours; an extruder that treats each contour as a ring produces
   interpenetrating prisms. A font can be wrong for us and right for everyone
   else. §4's bake-time checks exist because of this and for no other reason.
2. **The payload is ~1.8× a minified single-stroke face.** Measured, not
   estimated. It buys the removal of an offset implementation.
3. **Licensing narrows the field hard.** Arial, Verdana and Tahoma cannot ship at
   any price. The shippable set is two OFL families, and the best-behaved member
   of it is a monospace.
4. **The thing that binds is not in the font at all.** §5 — and it would have
   bound under *every* route, including the ones the survey preferred.

### 1.2 What this decision does not settle

**Emboss or engrave** stays open, on purpose. The sources disagree
([`research/text-emit-survey.md`](research/text-emit-survey.md) §3.3 and §6 give
three arguments pointing two ways), and one coupon settles what no amount of
reading will. It is registered as a bet in §6, per the standing preference for
turning an ungrounded empirical number into a bet rather than into a confident
default.

## 2. Why not the other four routes

The survey's routes A–D are all ways to acquire a polygon offset. They are
compared here rather than deleted, because "we chose E" is worth less than "we
know what E is better *than*".

| | A. Union of strokes | B. Overlapping solids, let the slicer union | C. Third-party offset lib | D. Redraw the font | **E. Outline font** |
|---|---|---|---|---|---|
| Needs a polygon offset | yes | no | yes | yes | **no** |
| Needs a union | yes, ~90 primitives/label | no — deferred to the slicer | yes | yes | **no** (per font, checked) |
| Runtime payload | 7.5 KB | 7.5 KB | 7.5 KB + library | 7.5 KB | 13.7 KB |
| New runtime dependency | no | no | **yes** | no | **no** |
| Emits a valid single mesh | yes | **no** — relies on slicer behaviour | yes | yes | yes |
| Glyph coverage | 37/37 after the union works | 37/37 | 7/37 clean today ([survey](research/text-emit-survey.md) §5.3, corrected) | fixes 2 of 4 break classes | **37/37 measured** |
| Real kerned type | no | no | no | no | **yes** |

Two of those cells deserve a sentence rather than a tick:

- **Route B fails the repo's own standard, not a taste test.** It ships a mesh
  that is not a solid and asks the slicer to fix it. The survey's evidence that
  slicers do so is documentary and partly from search summaries; nothing was
  sliced. Shipping geometry whose correctness lives in someone else's default
  setting is the trade this repo has a written rule against.
- **Route A got worse when the code was read.** `unionShapes` in
  `packages/core/src/graph/polygon-union.ts` computes *the outer perimeter* of
  the union and throws on a disconnected result — so a glyph with a counter
  (`0`, `A`, `8`, `B`, …) comes back with its counter filled in, and a glyph
  drawn as separate strokes throws. Route A is not "a union we have"; it is a
  union we would have to write.

Route A's one real advantage survives and is now somebody else's argument: a
general polygon offset would also unblock print-gate rows F4/F5/F6 and MC-4's
wall-thickness sweep, which are deferred in bikar's own source *precisely
because* they need it. **Text is no longer the fifth item on that list**, which
makes offsetting a print-gate decision to take on its own merits rather than a
text decision.

## 3. The shape of the feature

### 3.1 Three pieces, in order

1. **A bake script** (`scripts/bake-glyphs.py`, Python + `fontTools`) that reads one
   font file, flattens the 37 glyphs to closed rings at cap height 1.0, runs the
   §4 checks, and writes a TypeScript constant. It runs by hand when the face
   changes, not on every build — the output is committed, and a committed
   generated file is reviewable in a way a build step is not.
2. **The constant** in bikar, alongside the other vendored-rather-than-depended-on
   data. Rings, per-glyph advance widths, and the kern pairs the 37 glyphs use.
   Nothing else from the font.

   The shipping face's `kern` is **empty, and correctly so**: Source Code Pro
   Bold is monospaced (`post.isFixedPitch = 1`) and its GPOS carries `mark`,
   `mkmk` and `size` but no `kern` feature. That is worth writing down because
   the bake reads only the legacy `kern` table, so an empty result could equally
   mean *this script cannot see where the face kerns* — which would mis-space
   every label silently. T1 separated the two by warning on the GPOS **`kern`
   feature tag**, not on GPOS itself; DM Sans trips it and the shipping face does
   not. A proportional face is a shaper away, and that is a decision to take when
   one is chosen, not a gap in this one.
3. **An extruder**, `solidifyText`, and *not* `solidifyExtrudedPiece`. The latter's
   holes are circles — `PieceHoleSpec` is `{name, x, y, bands: {d, from, to}[]}` in
   `packages/core/src/kernel3d/solidify-piece.ts` — so it cannot take a polygonal
   counter, for any font. What *is* reusable is one level down: the same file's cap
   builder already lays a section out as outer ring plus reversed hole rings for
   earcut's `holeIndices`, with a deviation check and sliver absorption. That takes
   arbitrary polygons and is the thing to call.

### 3.2 DSL surface

```bkr
piece MC-4-R12
  ...
  text "MC-4 R12"
    at (0, -18)
    cap 5
    engrave 0.6
```

`face` is deliberately **not** a statement in v1. One shipping face, chosen once
in §6, keeps the "which faces have we checked?" question answerable — the moment
a `.bkr` can name a font, the bake-time checks in §4 stop covering the set of
fonts actually in use. A second face is a bake run and a constant, not a grammar
change.

### 3.3 Where a failure surfaces

In the mesh gate, next to everything else — D-014's principle that a verifier
gets a build target as its front door. A label that fails §5 fails `make coupons`
with the label, the pair, and the measured gap in the message. It does not warn.

## 4. What the bake script checks, and why each check exists

Each of these was found by running it, not by imagining it. Naming the glyph that
produced it is the point: a check whose motivating case is hypothetical is a
check nobody can tell is still working.

**B1 — no two contours of a glyph cross, and none crosses itself.**
Found by DM Sans, which draws `H` as three overlapping rectangles with four
proper crossings, and does the same in `A Q` (four each) and `R` (two). `B` is
the other kind: one contour that crosses *itself*, in a 0.15 mm tangle at the
waist. TrueType permits both and renderers resolve them by non-zero winding; an
extruder treating each contour as a ring does not. Six of the eight faces
measured are clean; two are not. **This is per-font and must not be written as a
general property of outline fonts** — that is the K2 shape exactly, and it was
drafted that way once before the eighth face was measured.

That glyph list is the corrected one. The research file's first measurement said
`A B H Q R Y`; `Y` is a single 9-point straight-line contour and cannot cross,
and the self-intersection in `B` was uncounted. See
[`outline-font-emit.md` §2a](research/outline-font-emit.md) — the error was
caught by writing the bake, because the bake had to name the failing glyphs one
at a time and the survey only had to count them.

**B2 — ring nesting is at most one deep, or the emitter carries depth.**
Found by Source Code Pro Bold's `0`, which is a **dotted zero**: shell, counter,
and a dot inside the counter — ink at depth 2. An `outline + holes` model cannot
express it, and the first implementation of the winding check declared the font
broken rather than its own model. Either the emitter applies the even-odd rule by
ring depth, or the bake rejects the face and says which glyph. Silence — where the
dot is quietly dropped or quietly cut — is the option that is not available.

**B3 — every check runs on the quantised, rounded rings that would ship**, never
on the font's curves. Rounding to 3 decimal places at cap height 1.0 is 5 µm at a
5 mm cap, far below anything printable, and it can still move a point across a
neighbour. Checking the ideal curve and shipping the rounded one is checking a
different artifact than the one that fails.

The four faces run through B1–B3 by the research script came out: Arial Bold,
Verdana Bold and Tahoma Bold clean on all six sub-checks; Source Code Pro Bold
clean on five and failing the winding check on `0` — which is B2's motivating
case and a defect in the model, not in the font.

**T1 took B2's first branch: the bake carries depth.** `GlyphRing.depth` is
nesting depth, not a hole flag, and the orientation rule is stated on the type —
even depths wind CCW, odd depths CW. Source Code Pro Bold's `0` bakes to three
rings at depths 0, 1 and 2 and passes. The face is not rejected and the dot is
not dropped.

## 5. The validator: the gap between letters, not the width of one

Every glyph in every bold face measured clears a 0.4 mm nozzle comfortably. Real
labels do not, and no per-glyph check can see it, because the failure is a
property of *the string* — which glyphs are adjacent and what the kern pair does.

**Validator:** after layout, every pair of distinct ink islands in the label's
2D outline is separated by at least one nozzle width. Measured as the minimum
distance between any two rings that are not nested in each other, over the whole
laid-out label, at the cap height and face in use.

PASS: `LG-B2` in Arial Bold at a 5 mm cap → minimum gap **0.563 mm** at the `-B`
pair, ≥ 0.4 mm. In Source Code Pro Bold the same label clears **0.898 mm**. All
four real labels — `MC-2 R08`, `LG-B2`, `W-F1`, `0000` — pass in both faces.

FAIL: `MC-4 R12` in Arial Bold at a 5 mm cap → **0.181 mm** between the `-` and
the `4`. Under half a nozzle width: the two beads merge and the label reads
`MC4`. This is not a constructed counterexample — it is a rung label this project
wants, in the face a reasonable person would have picked. The harder case is
`WWW`, at **0.031 mm** in Arial Bold and **0.061 mm** in Source Code Pro Bold,
which is the one that shows the failure is not confined to one face.

Two properties of this validator are deliberate:

- **It is not an aggregate.** "Mean gap" or "gap at the tightest kern pair the
  font declares" would both pass `MC-4 R12`. The repo's rule that an aggregate
  cannot discharge a claim about every part applies to spacing exactly as it
  applied to glyph stems, and to the survey's per-join bound — which named three
  failing glyphs where direct testing of the produced outline finds thirty.
- **Its FAIL case is a label the project actually wants**, not a synthetic
  string. A gate whose by-design failure is something nobody would ever emit is a
  gate that has stopped testing the thing it exists for.

What the validator does *not* do is fix the label. Whether a too-tight label is
opened by tracking (`MC-4 R12` needs +0.219 mm, `WWW` needs +0.369 mm), by a
larger cap height, by the monospace face, or by refusing the string, is §7's
open question. Failing loudly with the number is worth shipping before the fix
is chosen.

## 6. Defaults

**Default:** the shipping face is **Source Code Pro Bold**, licensed under the
[SIL Open Font License 1.1](https://scripts.sil.org/OFL), which permits embedding
and redistribution. It is chosen on measurement, not taste: zero crossing
contours across 37 glyphs, a 0.573 mm thinnest stem at a 5 mm cap, and every real
label clearing the nozzle by ~1.9× or better. Its one blemish is the dotted zero
of §4's B2. DM Sans is the alternative and is disqualified for v1 by B1.

**Default:** cap height **5.0 mm**, relief depth **0.6 mm**. Both are provisional
and both are bets — CAL-TXT-02 covers the cap height at which a rung label stays
legible on this machine, and it governs the flattening tolerance too, since the
0.05 mm chord tolerance is set as a fraction of the nozzle rather than of the type
size. 5.0 mm is the height at which the measurements in §5 were taken and is the
smallest at which a bold face's thinnest stem stays above one nozzle width with
margin; it is not a legibility measurement, because none was made.

**Default:** **engrave**, at CAL-TXT-01. This is a coin-flip recorded as a bet,
not a conclusion — §1.2 says why, and the sources genuinely disagree. Engrave is
the provisional side because a recessed feature that prints badly leaves a
readable part and an emboss that prints badly leaves debris on the surface that
matters. One coupon replaces this paragraph with a measurement.

> **Both ids are registered, and the gate now checks that.** `CAL-TXT-01` and
> `CAL-TXT-02` are in bikar's `CAL_BETS`, settled by coupon `MC-7`, which has a
> catalog entry of its own. They ship no `Calibrated<T>` record yet, because the
> constants they govern do not exist until T2 — the same shape as `CAL-OVH-01`,
> and the registry names it as an open bet rather than a missing one.
>
> This paragraph used to admit that the ids were invented and that D3 accepted
> them anyway. That admission is now a gate: **D5** fails any `**Default:**`
> discharged by a bet id the registry does not carry. Run against this file at
> the commit before T0 it reports two findings; after, none.

## 7. Open questions

1. **Emboss or engrave.** §6 bets engrave; `CAL-TXT-01` settles it. A coupon
   carrying both at three relief depths is the whole experiment.
2. **What to do with a label that fails §5.** Tracking, cap height, face, or
   refusal. Measured need: +0.219 mm for `MC-4 R12`, +0.369 mm for `WWW`.
   Automatic tracking is tempting and would make the validator unfalsifiable by
   construction, which is an argument for refusing rather than fixing.
3. **Whether any of this survives a print.** Nothing was printed and no slicer
   was run. §5's connectivity results describe the geometry a slicer is handed;
   a slicer's thin-wall handling could rescue or worsen them. This is the single
   largest gap in the whole investigation and one coupon closes most of it.
4. **Whether the five DM Sans glyphs are repairable by a build-time union.**
   Almost certainly for the four cross-contour cases — three overlapping
   rectangles is the well-conditioned case — and less obviously for `B`, whose
   defect is a sub-0.2 mm self-crossing that a union must resolve rather than
   merge. No union was run, and B1's claim is that the condition is
   *detectable*, not that it is repaired.
5. **Whether text belongs on the coupon or beside it.** A label engraved into a
   coupon changes the coupon's own geometry near the label. For MC-2, whose
   measurand is a minimum feature size, that is not obviously harmless.

## 8. Milestones

**T0 — register the bets. Done, 2026-08-04.** `CAL-TXT-01` and `CAL-TXT-02` are
in bikar's `CAL_BETS` with coupon `MC-7`, `MC-7` has a catalog entry, and the
hole §6 used to admit to is now the docs gate's D5 rule rather than a paragraph.
No `Calibrated<T>` record ships yet: the constants those bets govern arrive with
`solidifyText` in T2, and a bet with no record is a registered open bet, not an
absent one.

**T1 — bake and check. Done, 2026-08-04** (bikar
[#74](https://github.com/NaqshCoffee/bikar/pull/74)). `scripts/bake-glyphs.py`,
`glyph-data.ts` (Source Code Pro Bold: 37 glyphs, 52 rings, 1158 points, max
depth 2), `glyph-checks.ts` re-running B1–B3 over the baked data, and 18 tests.
The DM Sans case is *asserted to fail*, not skipped — a check that only ever sees
clean input stops being a check — and asserted to fail on **exactly** `A B H Q R`,
because an aggregate cannot discharge a claim about every part. `Y` and `0` ride
in the same fixture and are asserted to **pass**, so B1 is shown to discriminate
rather than merely to be loud on this face.

Two things the implementation found that this doc had wrong. The flattener's
first closed-form segment count delivered 0.018 cap heights of chord error when
asked for 0.01, on Source Code Pro Bold's `3`; recursive de Casteljau
subdivision against the convex-hull bound replaced it, so `chordTolerance` is a
guarantee (0.00498 worst case, re-measured against a 0.00005 reference) rather
than an estimate. And the DM Sans glyph list was wrong — see §4's B1 paragraph
and [`outline-font-emit.md` §2a](research/outline-font-emit.md).

**T2 — extrude and validate.** `solidifyText` over the cap-section machinery, the
`text` statement, and §5's validator wired into the mesh gate with `MC-4 R12` as
its asserted failure.

**T3 — label the 23 coupons**, and reprint the machine card that started this.
Not before T2: labelling coupons with an unvalidated emitter is how you get 23
parts that say `MC4`.

## Appendix A — what changed in the research, and what it cost

The first pass of this investigation spent its entire budget measuring the wrong
input. Four routes were analysed, a break-class taxonomy was built, and a
recommendation was nearly written — all on the assumption that a single-stroke
centreline font was the starting material, an assumption that was never stated
and therefore never checked.

It was dislodged by a question, not by a gate: *is there a better way to print
letters — does anything support text natively?* The answer took one measurement
pass and inverted the conclusion.

The generalisable part is not "consider outline fonts". It is that
[`research/text-emit-survey.md`](research/text-emit-survey.md) §4 had already
written the reason to dismiss them, and its reason was a K10 failure in plain
sight: a constraint that is true of **font matching in a static bundle** was
carried to **outline extraction** without the sentence saying why it transfers.
It does not transfer. The rule the repo already has would have caught it, applied
to the doc's own load-bearing dismissal rather than only to its claims.

Two smaller ones, recorded because both were nearly published as facts:

- A **per-join** bound on when an offset self-intersects named three failing
  glyphs. Testing the produced outline directly found **thirty**, in four break
  classes, three of which are non-local and which no per-join property can see.
  *An aggregate cannot discharge a claim about every part — and neither can a
  local test.*
- A stem-width measurement reported **DM Sans Bold `H` at 0.01 mm**, which would
  have been published as "unprintable" and is false. The distance transform was
  taken from the drawn segments rather than from the ink mask, and those agree
  only when no contours overlap — which is the very condition B1 had just found
  DM Sans to violate. *A finding about the input is also a finding about every
  tool that reads the input*, and nothing made that connection until the number
  came out absurd.
