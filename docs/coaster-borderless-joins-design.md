# Coaster joins without a wide border

*Status: proposal, 2026-09-26. Nothing here is built or printed. The sources and what
each one shows are in
[`research/2026-09-26-borderless-coaster-joins.md`](research/2026-09-26-borderless-coaster-joins.md).
This doc extends [`coaster-interlock-design.md`](coaster-interlock-design.md) (the shipped
dovetail, D-069) and does not change any decision in it.*

## 1. The problem

Omar, 2026-09-26: "can we brainstorm different pegging techniques / approaches where we
don't need to even add a border for peg, can re-use frames own border."

The **minimal-pegs** style is the minimal-frame coaster (straps standing free inside a
solid frame, holes between them) with a dovetail on every edge. The dovetail's slot cuts
into the frame, so the frame has to be wide enough to hold a slot *and* keep a wall behind
it (bikar `docs/design/coaster-openwork.md` §3):

    frame ≥ depth + clearance + 1.6 mm      (1.6 mm = the free-standing wall floor, CAL-CST-07)

The committed pegs files use `frame = depth + clearance + 2.5`, so 3 + 0.15 + 2.5 = 5.65 mm.
Everything below is measured with one number, the **seam band**: the solid you see between
two patterns when two coasters are joined. That is about two frames' worth.

| Style | Frame per coaster | Seam band when joined | Source |
|---|---|---|---|
| minimal-frame, just placed side by side (no joint) | 3 mm | about 6 mm | the committed files |
| minimal-pegs today (depth 3, clearance 0.15) | 5.65 mm | about 11 mm | [sample-rules](../.claude/skills/print-coaster-samples/sample-rules.md), minis-03 |
| minimal-pegs, 2 mm tabs | 4.1 mm | about 8.2 mm | measured by the session that asked for this doc, 2026-09-26; passes the mesh and joint gates; not re-run here |
| the same, with the art only 0.6 mm into the frame | 3.7 mm | about 7.4 mm | same |

Omar's feedback on the printed samples: the pegs border is "still too big". From minis-03
(40 mm): joined pairs were "a bit loose", with "big spaces between the patterns". Samples
are now 80 mm across and 2.6 mm tall: a 1.4 mm frame or slab, with straps standing 1.2 mm
above it.

**The goal:** a joint whose seam band is no wider than two minimal frames (≤ 6 mm), and
ideally close to *one* frame, that holds no looser than today's.

## 2. What any joint here has to live with

These come from the kernel and the printer. The approaches in §3 are scored against them.

1. **It has to be a height field.** bikar's coaster is a flat bottom with a top height at
   each point (`coaster-height-field.md` in bikar). A cut straight through the piece is
   fine: holes, notches and slots are all through-cuts. Anything with an undercut in Z
   (a groove in a side wall, a lap that hangs over air, a channel in the bottom) is not.
2. **It prints flat with no supports**, at 1.4 mm of frame and 2.6 mm of strap, with a
   0.4 mm nozzle. A free-standing wall is floored at 1.6 mm (CAL-CST-07, an unsettled
   bet), and a neck that takes the pull at CAL-CST-06 (also unsettled).
3. **Any edge joins any edge** with no rule to remember (D-069, Omar's "like legos").
4. **Walls that set the fit have to be exact.** The kernel samples the top on a 0.4 mm
   grid. A wall made from that grid has up to ±0.2 mm of stair per face, which is more than
   the clearance the joint is trying to hold. That is why the dovetail emits its outer
   wall exactly ([`coaster-interlock-design.md`](coaster-interlock-design.md) §5.3). Any
   new joint needs the same for every face it bears on.
5. **Only same-size, same-outline coasters join**, as today.

## 3. The approaches

Every seam-band figure below assumes the frame `f` is the same on both coasters, so the
band is `2f`. Nothing here was printed, and none of the proposed sizes is a default.

### A. A butterfly key through the frames, into the pattern's own openings (recommended)

Cut a narrow notch straight through the frame at the **midpoint of every edge**. A separate
**key** shaped like a bow tie joins two coasters. Its narrow waist runs through both
notches, and each wide end (a **wing**) drops into the pattern opening just inside the
frame. Pulling the coasters apart presses the wings against the inner face of each frame,
so the pattern's own openings do the job that the dovetail slot's pocket does today. The
frame needs no extra width, because nothing is cut behind it: the opening is already
empty.

The idea is the woodworker's butterfly key (S10, S11), with the pattern openings standing in
for the pockets a woodworker would rout. It also follows the grid systems' rule of putting
the joint in holes the part already has (Gridfinity seam clips S6; openGrid S2, whose details
are unverified).

- **Seam band:** 2f. With the minimal-frame's 3 mm that is **6 mm**, down from 11. With
  f = 2 it is 4 mm, and with f = 1.6 (the floor) 3.2 mm, about one minimal frame.
- **Proposed sizes (a starting point to test):** a waist of 2 mm (above the 1.6 floor,
  because it takes the pull), running `2f + 2c` long through both notches. Each notch is
  `2 + 2c` wide. Wings about 2 mm deep and wide enough to overlap each notch by ≥ 1 mm
  a side.
- **The key's shoulders bite about 0.2 mm into the frame's inner face.** Cut the key's
  pocket as an exact bow-tie shape, with a waist slightly shorter than the two frames. That
  way the faces the wings press on are cut exact, not left as grid stairs (§2.4).
- **Prints:** the key is a flat prism, printed on its own with no supports. The notch is a
  through-cut. Both fit in a height field.
- **Any edge to any edge, on every polygon we offer:** the key sits at the midpoint and is
  symmetric end to end. Every candidate outline (square, hexagon, octagon) is centrally
  symmetric, so a neighbour's opening is the mirror of ours across the seam. There is no
  tab/slot parity to track (compare study §3).
- **Fit:** play in the pull direction is the clearance at *both* wings, `2c`. Today's
  dovetail has one face, `c`. So a key at c = 0.05 plays about like a dovetail at 0.10.
  **Tuning the fit only means reprinting keys:** a clearance ladder of keys is a
  five-minute plate, not a plate of coasters.
- **How it looks:** a key as tall as the frame (1.4 mm) sits flush and shows as a low plug
  in each opening. A key as tall as the straps (2.6 mm) looks like **a strap crossing the
  seam**, so the art reads as continuing from one coaster to the next. It can also be a
  contrasting colour, as Nakashima's walnut keys are (S10).
- **Kernel work (medium):** (1) a new coaster clause, for example `interlock key $waist
  clearance $c`, that cuts the exact bow-tie pocket at each edge midpoint and needs
  `openwork`; (2) the wing-room check in §5; (3) the key itself as a solid, which may
  fit an existing `piece … extrude` (not tried).
- **Risks:** (a) **The joint depends on the pattern.** It needs an opening at each edge
  midpoint big enough for a wing. GimTvN9hw4U has a wide one (about 8–12 mm by eye).
  7apC5Q9QS-8 has only a small one, about 2 mm deep by eye (research §10). (b) A
  coaster on its own has a gap in its frame at each edge midpoint. The frame becomes
  separate arcs held together by the art; the mesh gate's one-body check catches it if the
  art doesn't hold them. (c) The keys are loose parts that can get lost. (d) The waist
  is a loaded neck, so it rides on CAL-CST-06.
- **A variant, A2 (a recessed notch):** leave a 0.6 mm floor (3 layers) under the waist
  instead of cutting through, so a coaster's frame stays closed. The key then has a
  thinner waist, and it prints **upside down** (flat top on the bed) so it stays a
  height field. This costs one more exact-wall case in the kernel. Build it only if A's
  gaps look wrong on a coaster used alone.

**Pros:** the narrowest band of any approach that still locks; the fit can be tuned
without reprinting coasters; any edge joins any edge on every polygon; the key can add to
the look. **Cons:** loose parts; a coaster alone has notched edges; it only works where the
pattern has a midpoint opening. **Implications:** pegs stops being a style of its own. Any
minimal-frame file with a midpoint opening can take keys, so which patterns support keys
becomes a property the check reports. It also makes the key's clearance a new question for
CAL-FIT-01.

### J. Shrink today's dovetail (the baseline)

Keep D-069 and just pick smaller numbers: depth 2 mm tabs and a thinner frame.

- **Seam band:** 8.2 mm (f = 4.1), or 7.4 mm (f = 3.7) with the art 0.6 mm into the frame.
- **Prints / fit:** unchanged, a known quantity. The 0.10 clearance is on minis-04.
- **Kernel work:** none (parameters only).
- **Risks:** a 2 mm-deep tab has less head to hold. It is still wider than any
  minimal-frame.

**Pros:** ready now, no new code, already passes the gates. **Cons:** the band is still
about 1.3× a pair of minimal frames, which is the "still too big" Omar objected to.
**Implications:** it is the control on the coupon (§6), not the answer.

### B. Tabs that reach into the neighbour's openings (integral, no loose parts)

Like A, but the key is part of the coaster. A tab sticks out from one coaster's frame,
passes through a notch in the neighbour's frame, and its head sits in the neighbour's
opening.

- **Seam band:** 2f, as in A.
- **Pairing:** a tab and a notch can't both sit at the edge midpoint. The options: (i)
  **alternate edges**, tab, notch, tab, …, which joins by translation on the **hexagon
  only** (study §3); or (ii) keep D-069's tab at ¼ and notch at ¾ of each edge, which needs
  openings at both quarter points. On GimTvN9hw4U those are exactly where the corner
  hexagons meet the frame (research §10), so (ii) fails for that pattern.
- **Fit:** play is `c` at one face, tighter than A for the same clearance.
- **Prints:** a flat tab, fine. It sticks out `f + c + head` ≈ 5.5 mm past the outline of a
  coaster on its own (today's tabs stick out 3 mm).
- **Kernel work (medium–high):** the tab's length depends on `f`, the notch is as in A,
  and the head-room check runs on the *neighbour's* opening.

**Pros:** no loose parts; tighter than A for the same clearance. **Cons:** hexagon-only if it
stays any-to-any; longer tabs on a coaster used alone; tuning the fit means reprinting
coasters. **Implications:** squares and octagons would need a turn-every-other-tile rule,
which breaks D-069's "like legos". Good as a hexagon-only follow-up if Omar rejects loose
keys.

### E. Bevelled overlap (a lap cut at 45°)

On half of each edge, chamfer the top at 45°. On the other half, chamfer the bottom at 45°.
The neighbour's bottom-chamfered half then rests over our top-chamfered half.

- **Seam band:** 2f minus the overlap, and the overlap is at most the frame height (1.4 mm).
  At f = 3 that is 4.6 mm.
- **Prints:** a 45° underside is the usual limit that prints without supports (S22,
  search-only). A square-stepped **half-lap** (S12) would be a 90° overhang, and at 1.4 mm
  each lap would be 0.7 mm thick. That is out.
- **Fit / lock:** **no pull lock at all.** It only hides the seam. It still needs A or J
  to hold.
- **Kernel work (low–medium):** `edge chamfer top|bottom` already exists, but only around
  the whole outline, and openwork refuses a bottom edge (openwork §4). This would need
  chamfers on half an edge.
- **Risks:** thin edges that chip.

**Pros:** saves up to 1.4 mm of band on top of A. **Cons:** holds nothing on its own.
**Implications:** worth adding to A later, not a joint by itself.

### F. Magnets, laid out like Magna-Tiles

Two magnets per edge, poles pointing up and down, one at ¼ and one at ¾, pointing opposite
ways (S15). A neighbour reverses the edge, so its ¾ magnet faces our ¼ magnet with the
opposite pole, and they attract, so any edge joins any edge. It is the same half-edge rule
as D-069.

- **Seam band:** the frame has to hold the magnet: about ⌀ + 1.2 mm. With ⌀3 mm that is
  8.4 mm, no better than J. With ⌀2 mm it is 6.4 mm.
- **Prints:** a pocket open at the top is just a lower region of the frame, so it fits a
  height field. With a 1 mm magnet, the floor under it is 0.4 mm (2 layers). Burying it
  instead needs a pause at a layer (S17), which is Omar's step at the printer.
- **Fit:** no play and it lines itself up, but it doesn't stop the coasters sliding along
  the seam. We have **no number** for the pull between two tiny magnets through 1–2 mm of
  PLA (S17 has none).
- **Kernel work:** low for the pockets. The cost is buying magnets, gluing them in, and
  keeping the poles the right way round.

**Pros:** no loose keys, clicks together. **Cons:** a wider band than A; hand assembly; unknown
hold. **Implications:** it adds a bought part to what was an all-printed product.

### H. A tray instead of a joint

Leave the coasters as plain minimal-frames and print a shallow tray that holds a set side
by side (the Gridfinity base-plate idea, S6/S7).

- **Seam band:** 6 mm (two minimal frames), or less if the tray fixes the spacing and the
  frames thin down.
- **Kernel work:** low for the coasters (none). The tray is a new, large print.
- **Risks:** the mat only holds together inside its tray.

**Pros:** no joint to tune. **Cons:** not the "plug together" Omar asked for.
**Implications:** a different product (a mat with loose tiles).

### C. Let the art cross the seam (the girih principle)

Girih tiles carry strap lines that "cross the boundaries of the tiles at the center of an
edge at 54°", so the pattern runs unbroken across tiles (S13, S14). For us, the art would be
laid out so its straps meet the frame at points that line up with the neighbour's. The
joined pair then reads as one field with a thin line through it.

- This is a **layout rule, not a joint.** It pairs with A (the key can *be* the strap that
  crosses) or with J.
- **Kernel/importer work (high):** the importer fits the art inside the frame by
  `margin`/`unit` (D-065). Lining the straps up to the edge means laying the art out to
  its repeat, which is new importer work, and it depends on the pattern.

**Pros:** the biggest visual payoff, since the seam disappears into the pattern. **Cons:**
the most work, and done pattern by pattern. **Implications:** a later step once a joint is
chosen.

### D. Joints on the strap ends themselves (no frame at all)

Use the minimal coaster (`outline pattern`, no frame) and interlock each strap that crosses
the seam with its continuation on the neighbour.

- A socket needs a wall on both sides of its neck: `2 × 1.6 + neck + 2c` ≈ 5 mm. A 2 mm
  strap can't hold one, so each crossing strap would need a knob at its end, which reads as
  a blob.
- `outline pattern` refuses `interlock` today (grammar §10.3). **Kernel work: high. Risk:
  high** (many tiny joints, each below the loaded-neck bet).

**Pros:** truly borderless. **Cons:** the knobs, the effort, and fragile joints.
**Implications:** revisit only if C is built and A's keys look wrong.

### Ruled out

| Idea | Why not |
|---|---|
| Square half-lap (S12) | 90° overhang on the upper lap; 0.7 mm laps at 1.4 mm frame; wood's strength comes from a glued face, which we don't have |
| Sliding dovetail or tongue-and-groove in the side wall | an undercut in Z, not a height field; the groove's roof overhangs (S9, S22); features of about 0.5 mm at 1.4 mm height |
| A clip pushed on from below (Gridfinity style, S7) | needs a channel in the flat bottom (not a height field), or lifts the coaster off the table; the S7 snippet says clips are often not reusable after taking the grid apart |
| Pins or dowels into the frame's side | a 1.4 mm frame can't hold a horizontal pin; a vertical pin needs a part across the seam, which is A |

## 4. Side by side

"Band" is the seam band at the frame each row assumes. "Kernel" is the bikar work to express
it.

| Rank | Approach | Band | Prints flat, no supports | Fit / play | Kernel | Main risk |
|---|---|---|---|---|---|---|
| 1 | **A. Butterfly key into the openings** | 6 mm at f=3; 4 at f=2; 3.2 at f=1.6 | yes (key and notch are both straight cuts) | 2c; tuned by reprinting keys only | medium: new clause, exact bow-tie pocket, wing-room check, key solid | needs a midpoint opening; loose keys |
| 2 | J. Smaller dovetail | 7.4–8.2 mm | yes | c; known | none | still wider than two minimal frames |
| 3 | B. Tab into the neighbour's opening | 2f (6 at f=3) | yes | c | medium–high | hexagon-only to stay any-to-any |
| 4 | E. 45° bevelled overlap | 2f − ≤1.4 | yes at 45° | no lock | low–medium | thin chipping edges; needs A or J |
| 5 | F. Magnets (Magna-Tiles layout) | 6.4–8.4 mm | yes, with pockets open at the top | no play, but slides along the seam | low | unknown hold; bought parts, glue |
| 6 | H. Tray | ~6 mm | yes | none needed | none for coasters | not a joint |
| 7 | C. Art crosses the seam | pairs with A/J | n/a | n/a | high (importer) | pattern by pattern |
| 8 | D. Strap-end joints | ~0 frame, knobs at the straps | yes | many tiny joints | high | fragile, knobby |

A ranks first on value for the work: it is the only approach that locks with a band at or
under two minimal frames, and it isolates the fit question in a part that costs minutes to
reprint. J ranks second because it is free and is the control.

## 5. Checking that a key fits the pattern

A's one new check. It runs during evaluation like CV8, and names the worst place.

**Validator:** CV-K1 (wing room). For every edge, the bow-tie pocket at its midpoint,
grown by the clearance `c`, has to sit wholly in the openwork's cut region plus the frame's
notch. The only exception is the 0.2 mm shoulder bite into the frame's inner face. It also
has to stay at least `strap/2 + c` from every strap centreline, so no wing ever lands on a
strap. The report names the edge and the nearest strap.
- PASS: GimTvN9hw4U minimal-frame at size 80, f = 3, waist 2, wings 2 mm deep: the
  midpoint opening is about 8–12 mm wide by eye (research §10). It is expected to clear.
  The first real run of the check is what measures it.
- FAIL: the same key moved to the ¼ point of each edge, where GimTvN9hw4U's corner hexagons
  meet the frame. The wing lands on a strap, and the check should name that strap. The
  hard case that occurs naturally is 7apC5Q9QS-8 at size 80. Its midpoint opening is about
  2 mm deep by eye, which is less than a 2 mm wing plus clearance. That pattern would need
  shallower wings or no keys, and the check, not a person, should be what says so.

A's other failure, a frame broken into arcs the art doesn't hold, is already caught by the
mesh gate's one-body check. It needs no new validator.

## 6. First prototype and the coupon

**Recommended:** A (a through-notch, key as tall as the frame) on GimTvN9hw4U minimal-frame
at 80 mm, with J as the control on the same plate.

Proposed coupon, **KEY-1** (a name for now, not yet in the prototype catalog):

| Item | Copies | Tests |
|---|---|---|
| GimTvN9hw4U minimal-frame + key notches, f = 3 | 2 | band 6 mm; whether the notched frame stays flat and in one piece |
| the same at f = 2 | 2 | band 4 mm; whether a 2 mm frame survives handling (CAL-CST-07) |
| keys, waist 2, as tall as the frame, c = 0.05 / 0.10 / 0.15 | 2 of each | the clearance ladder: which one is neither loose nor stuck |
| one key as tall as the straps, c = 0.10 | 2 | whether the key reads as a strap crossing the seam |
| J control: 2 mm tabs, f = 4.1, c = 0.10 | 2 | the band and feel to beat |

What Omar reads off it: the band, side by side with the control; the pull feel for each key
clearance; whether a key falls out when you lift one coaster; whether a coaster on its own
looks wrong with its notches. Before any of it goes to the printer, it passes the mesh gate
and [review-print](../.claude/skills/review-print/SKILL.md), and the send is Omar's.

**Two ways to get the first physical answer.** Pick one (open question 4):

| | Mock-up in OpenSCAD first | Build the bikar clause first |
|---|---|---|
| What it is | take the rendered minimal-frame STL, cut the bow-tie pocket as a boolean, extrude the key polygon | `interlock key` in the coaster kernel, with CV-K1 and exact walls |
| Buys | a printed answer to "does it look and hold right" in hours | the real thing, with the check and the importer knob |
| Costs | throwaway code in this repo, outside bikar; no CV-K1 | days of kernel work before anyone holds a key |
| Verifies | fit and look only; the pocket walls are exact because the boolean cuts them | fit, look, *and* that the check runs per pattern |
| Implies | the kernel work waits on the print; if keys lose, nothing was spent in bikar | if keys lose, the clause is dead code to remove |

Recommended: **the mock-up first**, because the open questions are physical (feel, look,
loss), and the mock answers them without committing bikar to a clause.

## 7. What transfers from other materials, and why

- **Butterfly key (wood → PLA): the shape transfers, the angles don't.** The lock is purely
  shape in the plane: a wing wider than the notch can't pass through it. That holds for any
  rigid material, dry or glued. The wood numbers don't transfer. The 8–10° wing angle and
  ~1° side bevel (S11) are for a hand-fitted, glued inlay pressed into wood fibre. PLA
  doesn't crush into a tight fit the way wood does, and our walls are vertical by
  construction.
- **Half-lap (wood → PLA): does not transfer.** Its strength is a glued long-grain face
  (S12). We have no glue, 0.7 mm laps, and an overhang.
- **Magna-Tiles polarity: transfers exactly,** because it rests only on geometry and on how
  magnets attract. The Magna-Tiles pairing is the same half-edge rule as D-069. Its hold
  does **not** transfer, because nothing tells us the pull for 2–3 mm magnets 1–2 mm apart.
- **Girih layout: transfers as a drawing rule.** Straps meeting the edge at fixed points and
  angles don't depend on the material. It gives no joint: the architectural tiles were set
  in mortar.
- **Grid-ecosystem clips (openGrid, Gridfinity): the principle transfers, the sizes don't.**
  "Put the joint in holes the part already has" is geometry. Their plates are 4–6.8 mm thick
  (S2), about 3–5× our 1.4 mm frame.
- **BOSL2's slop convention transfers,** because it is our convention already: the socket
  grows by `2·slop` across and `slop` in depth (S1).
- **Generic PLA clearances (0.3 mm, S18; 0.5 mm, S8) do not transfer.** They are for other
  printers and larger joints, and our X2D evidence runs the other way: 0.15 felt loose.

## 8. Open questions for Omar

1. **Loose keys or tabs built into the coaster?** Keys (A) give the narrowest band and fit
   tuning without reprinting coasters, and can be an accent colour; they can get lost.
   Tabs (B) can't get lost, but on squares and octagons they need a turn-every-other-tile
   rule.
2. **Notches on a coaster used alone:** fine, or worth the recessed-notch version (A2), where
   a coaster's frame stays closed and the key prints upside down?
3. **How thin should the mat's outer edge be?** f = 3 (band 6 mm, today's minimal-frame), f =
   2 (band 4 mm), or f = 1.6 (band 3.2 mm, at the unproven free-standing floor)?
4. **Mock-up first, or bikar first?** (§6's table.)
5. **Patterns without a midpoint opening** (7apC5Q9QS-8 by eye): drop keys for those, use
   shallower wings, or keep today's dovetail there?
