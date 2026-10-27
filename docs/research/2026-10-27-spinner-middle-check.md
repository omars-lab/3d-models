---
date: 2026-10-27
produced-by: spinner-middle checker (Claude Opus 5.5) — re-opened the load-bearing sources of both research passes with WebFetch and one WebSearch, and re-rendered the middle piece and the lower half from bikar origin/main 0d48ac4 in a scratch export (the shared bikar checkout was not touched)
feeds:
  - docs/design/coaster/spinner-middle-design.md
checks: docs/research/2026-10-27-spinner-middle-research-a.md, docs/research/2026-10-27-spinner-middle-research-b.md
---

# A middle piece that turns: what the checker re-opened, and what it says

Two researchers answered the same question on their own: what would it take to print the split
flange coaster's middle piece, the ten-pointed star, so it turns in place like a spinner.
Researcher A is PR #802 ([research](2026-10-27-spinner-middle-research-a.md),
[design](../design/coaster/spinner-middle-design-a.md)); researcher B is PR #801
([research](2026-10-27-spinner-middle-research-b.md),
[design](../design/coaster/spinner-middle-design-b.md)). This file records what I re-opened
myself, so the doc to act on, [spinner-middle-design](../design/coaster/spinner-middle-design.md),
rests on checked text and a fresh render rather than on either summary.

Nothing was printed. Each line below is a page fetched on 2026-10-27, a render I measured, or my
own arithmetic, and says which.

## 1. The render, re-measured on bikar main

A measured the middle star and the frame round it on a 2026-10-06 bikar checkout (951995a). B
could not render (its built CLI was older than the file). I exported bikar origin/main at 0d48ac4
(2026-10-27) to a scratch folder, built its core, knobs and CLI, and rendered
`patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr` at split-06's fit (`gap 0.10`,
`room 0.2`): `--piece Middle` and `--piece Lower`. A small script sliced each mesh flat at a height
and walked out from the centre along a ray every 3°. The lower half was also rendered with
split-10's peg settings (ring 3 at 13.0 mm, `stud_boss 1`, `stud_wall 0.7`).

### 1.1 The middle star (A's M1)

| Height | Tips, largest radius | Notches, smallest radius |
|---|---|---|
| Faces (cut at 0.3 and 3.9 mm) | 9.475 mm | 7.351 mm |
| Band (cut at 1.0, 2.0 and 3.0 mm) | 10.837 mm | 8.151 mm |

The piece is 4.2 mm tall (the coaster's 4.4 less `room` 0.2) and 20.6 × 21.7 mm across at the band.

- A's tips at the faces (9.48) and at the band (10.84), and notches at the faces (7.35):
  **confirmed**.
- A's notch radius **at the band** (7.35): **contradicted**. It is 8.15; the flange steps out at
  the notches too. Nothing in A's argument rests on this cell.

### 1.2 The frame round the middle (A's M2)

Solid frame along a ray from the centre, lower half; the star's tips point at 18°, its notches at 0°.

| Height | At a notch (0°) | 6° | At a tip (18°) |
|---|---|---|---|
| 0.3 mm, in the face block | 7.45 to 11.64 | 7.67 to 12.68 | 9.65 to 16.03 |
| 1.5 mm, in the undercut | 8.25 to 10.65 | 8.71 to 11.60 | 11.01 to 14.66 |

**Confirmed** within 0.05 mm of A's table (A: 7.50–11.65, 7.70–12.70, 9.65–16.05; 8.30–10.70,
8.75–11.60, 11.05–14.70). The small kites' undercuts come in to **10.65 mm** at the notch angles,
not 10.70. With split-10's ring of pegs at 13.0 mm the same rays read the same at 0°, 3°, 6° and
18° (the boss only fills the undercut between 12.88 and 12.94 mm at 12°): **the pegs are not the
binding limit; the kites' undercuts are.**

The arithmetic that follows (mine): a round opening that clears the tips at a 0.10 mm gap is
9.58 mm; with today's 0.8 mm undercut it reaches 10.38 mm; that leaves **0.27 mm** of wall before
the kites' undercuts at 10.65. At a 0.15 gap the wall is 0.22 mm. bikar's least wall (`stud_wall`,
range floor 0.4, "one line") is wider than either.

The picture is [middle-top-view.png](../design/coaster/spinner-middle-media/middle-top-view.png),
drawn from the same slices.

### 1.3 What the render does to B's "turning ring" option

B's option B keeps today's star loose inside a round, frame-colored ring that turns, and B flagged
it as needing "a measured render first". The render settles it against B: at the band the star's
own tips reach 10.84 mm and the kites' undercuts reach in to 10.65 mm at the notch angles, so the
star's undercut already crosses the circle where the ring's outer flange would have to run. A ring
round the star must hold the star's flange inside it, so at the band the ring runs from 10.84 plus
the gap out to at least one 0.4 mm line more, about 11.4 mm, and its own undercut is wider still.
That cuts through the kites' undercuts (from 10.65) and comes to their holes at the face (from
11.64). B's
§5 item 4 cleared the pegs at 13 mm but did not look at the kites. **A's "does not fit" is the side
the render supports**, unless the ten small kites around the middle are redrawn.

## 2. Sources re-opened

| Claim | Who used it | Source | Result |
|---|---|---|---|
| Bambu X1 Carbon, PLA, 0.4 mm nozzle, 0.2 mm layers: joints "moveable at 0,15"; per side not stated | A S1, B S1 | [Fab Academy Ísafjörður 2025, week 5](https://fabacademy.org/2025/labs/isafjordur/group_assignments/group_week05/) | **Confirmed**, quote verbatim; the table lists PLA horizontal 0.15 and vertical 0.15 for the X1C; Prusa MK4S PLA 0.15 and 0.2 (table only, no text). Per side or across: not stated. |
| Bambu A1, PLA: 0.05–0.10 fused, 0.15 friction, 0.20–0.25 free, 0.30 loose | A S2 | [Fab Academy Kochi 2026, M. Sharaf, week 5](https://fabacademy.org/2026/labs/kochi/students/mishael-sharaf/assignments/week05.html) | **Confirmed** in substance; the page's words are "movable with friction" and "smooth free movement", A paraphrased. Layer height for the gauge not stated (0.08–0.28 mm range). Per side not stated. |
| The print-in-place coin: "0.25 mm clearance around the inner edge was sufficient" | A S2 | same page | **Number confirmed, wording not found.** The page says "I then offset this profile by 0.25 mm to create clearance". |
| PLA 0.4 mm: minimum 0.15, recommended 0.25–0.3; 0.3 sliding, 0.2 rotate-once-and-lock | A S4 (snippet), B S2 | [uavmodel guide](https://blog.uavmodel.com/?p=4008) | **Confirmed.** The table does not say per side; its hinge example alone says "0.2mm clearance on each side". |
| 0.25 mm per side as a PLA hinge baseline | A S3, B S3 | [Sovol blog](https://www.sovol3d.com/blogs/news/print-in-place-3d-printing-how-to-design-hinges-joints-and-moving-parts-that-actually-work) | **Unreachable** (HTTP 429 again). A snippet in both passes; carries no weight. |
| 6700ZZ is 10 × 15 × 4 mm | A S9, B S12 | [Simply Bearings 6700ZZ](https://www.simplybearings.co.uk/products/6700-zz-eu) | **Confirmed** (sizes). Prices are left out of this file; A's quantity price was not on the page I fetched. |
| 6704 is 20 × 27 × 4 mm, and cheap in tens | A S10 | [Henderson 61704/6704](https://www.hendersonbearings.co.uk/61704-6704-thin-section-ball-bearing-20x27x4mm.html) | **Confirmed** (sizes, and that the page sells it in quantity tiers). Prices are left out of this file. |
| AXK1024 needle cage is 10 × 24 × 2 mm, washers sold apart | B S14 | [Klium SKF AXK 1024](https://www.klium.be/en/skf-axk-1024-needle-roller-bearing-10-x-24-mm-46430) | **Confirmed.** Roller diameter is not on the page; B's 2 mm rollers and 4 mm with washers stay snippets (B S15). |
| 440C stainless resists rust better than 52100 chrome steel but "may corrode" | B S17 | [SCA Shinyei AISI 440C](https://sca-shinyei.com/ballbearing/bearing_aisi440c) | **Confirmed** verbatim; the page points to AISI 304 or 630 where more resistance is needed, and rates seawater "slightly affected" for 440C. |
| Printed balls needed "massaging"; printed 608s "just too rough to make for decent bearings" | B S8 | [Bambu forum thread](https://forum.bambulab.com/t/bearings-balls-or-no-balls-i-e-rollers-nothing-etc/94119) | **Confirmed** verbatim. |
| Every thin bearing near our size is 4 mm tall | A S11 (snippet), B §4 | one WebSearch for a 20 mm bore, 3 mm wide thin-section ball bearing | **Not contradicted, not proven.** The search found no 20 × 27 × 3 mm bearing, and one more 4 mm one (an ET2520, 20 × 25 × 4). "Not found in one search" is not "not made". |
| Spin time: a printed spinner with a 608 gives "several seconds" | A S20, B §6 | MakerWorld and listing snippets | **Not re-opened** (403 in both passes). Neither design leans on a number from it. |

## 3. Where A and B agree

- A star cannot turn in a star-shaped hole; the boundary between the turning part and the frame
  must be a circle at every height, faces included, so the ten bits of frame between the star's
  points either go onto the turning part or go.
- The turning surface to try first is printed PLA on printed PLA: today's flange-under-a-lip, made
  round. Nothing to buy, the height stays 4.4 mm.
- Expect a part that **turns** when pushed and stops, not a spinner that coasts for seconds. No
  PLA-on-PLA friction figure was found by either.
- Every clearance found online is for parts printed in place, which have to break apart; ours are
  printed apart. Both read them as an upper bound, not a target, and both start the ladder at
  0.15 mm with 0.10 and 0.20 beside it.
- No bought bearing among those checked (6700, 6704, AXK1024 with washers) fits 4.4 mm with both
  faces covered; a 4 mm bearing hidden behind both faces needs a taller coaster (A: 5.2 mm with
  0.6 mm faces; B: 5.5 to 6 mm with 0.75 to 1 mm faces). bikar's `height` reaches 6.
- Steel balls would go in by hand when the halves close; no paused print is needed.
- The turning part's faces should sit one 0.2 mm layer in from the coaster's faces so the mug
  stands on the frame.
- Up-and-down play (`room`) is the rattle half of the fit; Omar did not take a pin that "shakes a
  bit" (A) and a turning part with play "will click" (B).

## 4. Where they disagree

| Point | A | B | Which side the evidence supports |
|---|---|---|---|
| What fits round the middle | A round disc; a ring round today's star does not fit (kites' undercuts from 10.70) | A turning ring round today's star is the preferred look, pending a render | **A.** The render (§1.3) shows the star's band and the kites' undercuts already overlap the circle the ring would need. |
| The binding neighbour | The small kites' undercuts | The ring of pegs at 13 mm | **A.** The pegs leave the inner edge unchanged (§1.2). |
| The first test print | A 36° slice of the real coaster (`wedge 36 wedge_from 9 wedge_center 1`) with a round middle at three gaps and a stock slice, which needs bikar to draw a round middle first | A round OpenSCAD coupon, 32 mm across, printable now, eight coupons, and the stock middle in a `wedge 36` slice | **Neither is wrong; they verify different things.** The coupon reads the turning gap and rattle only; the slice also reads the 0.3 mm wall to the kites, the set-in faces and the real pegs. Omar's standing rule (2026-10-12: one repeat of the shape, several settings, a stock control, not a whole coaster and not a tiny coupon) points at the slice. The consolidated doc picks the slice. |
| `room` 0 as a rung | Not a rung: 0 "would jam" | One pair at `room` 0 to separate rattle from turning | **A, on repo evidence, not a measurement.** The coaster file records that split-02's halves, with full-height pieces (`room` 0), "closed with a space between them". A piece that holds the halves apart is clamped, not free to turn. |
| A wet test | Not in the validator | Turn again after a rinse and dry; the hard case is 0.10 wet | **B adds a real failure mode.** The consolidated validator keeps it. |
| Height a hidden 4 mm bearing needs | 5.2 mm | 5.5 to 6 mm | Both arithmetic; they differ only in how thick a face skin they allow (0.6 vs 0.75 to 1 mm). |

## 5. What only one found

**Only A:**

- The render of the middle and the frame (M1, M2), now confirmed on bikar main with one cell
  corrected (§1).
- The Kochi A1 ladder (fused at 0.10, friction 0.15, free 0.20–0.25, loose 0.30), confirmed.
- The 6704's 20 mm bore is the smallest that clears the star's 19 mm face, and its 27 mm outside
  would cut the ten small kites. Arithmetic, from a confirmed size. (The disc's band, 21.7 mm across,
  would not pass that bore, so the disc would sit in the bearing without its flange.)
- Two ways the disc can show the art: two colors on its face, or one color with the star as a
  groove.
- Two turning coasters on MakerWorld (a three-ring "Kinetic Coaster", a moiré coaster), snippets.

**Only B:**

- The 440C corrosion page, confirmed: stainless balls "may corrode". A found no source on rust.
- The AXK1024 needle cage, 2 mm thick but 24 mm across (confirmed), which fits the height without
  washers but is wider than the middle's band and would reach the kites' holes at 11.64 mm.
- The middle's flange already prints poorly: split-07's middle had a "webbed duck feel" at its
  flange step, and split-10 tests `slope` and supports for it. A round flange has the same step
  over air, so split-10's answer carries over.
- CAL-LSE-01 is the open bet that governs a loose piece's fit; the coaster file's `gap` comment
  names it.
- A flat disc's resistance to slowing grows with the fourth power of its radius (mass with r², and
  inertia with mass times r²), so a 21 mm middle has very little; physics, not a source.
- The forum's printed-bearing reports (confirmed) and the Hackaday 64-variant calibration.
- A wet-and-dry turn in the validator.

## 6. What I did not check

- The MakerWorld, Printables and Thangs pages both passes saw as snippets (403 to the fetcher).
- The 67xx series beyond 6700 and 6704, and the 61800 (B S13).
- Whether a 0.27 mm wall to the kites' undercuts prints at all: no render can say; it is below the
  one-line floor bikar enforces for a peg's socket, which is why the design fills those undercuts
  instead.
