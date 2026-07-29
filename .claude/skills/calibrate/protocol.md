# Measurement protocol

The protocol is part of the coupon. A rung measured differently than the last
machine's rung produces a number that cannot be compared to it, which quietly
destroys the only thing calibration is for.

Every reading is recorded against a **profile header**. A reading without one is
anecdote, not calibration (bikar Tenet 30).

## Profile header — record before measuring anything

| Field | Note |
|---|---|
| Machine | model + firmware version |
| Material | brand, type, **and colour** — pigment changes effective flow; a "PLA" reading is not transferable across colours, let alone brands |
| Spool | so a re-measure can rule the spool in or out |
| Nozzle | diameter **and** type (brass / hardened / CHT — they do not flow alike) |
| Layer height | |
| Profile | the slicer profile name **verbatim**, plus any setting changed from it |
| Ambient | rough room temperature; enclosure open or closed |
| Date | |
| Instrument | caliper make + resolution; note when it was last zeroed |

## Before the caliper touches the part

- **Cool fully.** Measure no sooner than 30 min after the print finishes; longer
  for PETG/ABS. A warm part reads large, and it reads large *inconsistently*.
- **Deburr the measurement zone**, or measure above it. Elephant foot on the
  first layers is a real property of the machine but it is not the property this
  coupon is asking about — measure it deliberately (MC-6) rather than letting it
  contaminate every other reading.
- **Zero the caliper** at the start of each session and record that you did.

## Technique

- **Light, consistent jaw pressure.** Plastic deforms; over-clamping is the most
  common source of a bore that "measures" 0.1 mm small. Close until the jaws just
  contact.
- **Three readings per feature**, at distinct locations or rotations. Record all
  three, report the **median**. If the spread exceeds 0.05 mm, that spread is
  itself a result about the machine — write it down rather than averaging it away.
- **Bores: two orthogonal diameters** (along X and along Y), at mid-height. FDM
  bores are not round, and the X/Y difference is the anisotropy the fit classes
  actually live or die by. Never report a single bore diameter.
- **Walls: away from corners and seams.** The seam is a different thickness and
  measuring it answers a different question.

## Per-coupon judgement

Some rungs are not caliper questions, and pretending otherwise invents precision.

- **MC-1 fit classes** — judged **by hand**, and the judgement is recorded with
  *who made it*, because it is a human calibration:
  - *press* — needs a tool or bench pressure to seat;
  - *snug* — seats with firm thumb pressure, does not fall out inverted;
  - *sliding* — moves under its own weight with perceptible resistance;
  - *free* — drops under its own weight.
  Record the caliper reading of the mating pair too, so the hand judgement can
  later be mapped back to a gap in millimetres.
- **MC-3 bridge** — visual, per rung: clean / sagging / drooping / failed. Note
  the **first rung that sags**, not just the first that fails; the usable limit is
  the last clean one.
- **MC-4 overhang** — surface quality per angle. Record the first angle showing
  curl or droop, and photograph the fan.
- **MC-5 warp** — on a flat reference surface (granite plate or float glass), the
  gap at each of four corners by feeler gauge; if no feelers, caliper the part's
  edge-to-reference offset. Record all four, not the worst — the *pattern* tells
  you whether it is warp or a bed-levelling artifact.
- **MC-6 bed contact** — which towers survived, which detached, and at what point
  in the print if observed.

## Data sheet

Fill at the bench, not from memory.

```
PROFILE: machine ______ material ______ colour ______ spool ______
         nozzle ______ layer ______ profile ______ ambient ______
         date ______ caliper ______ (zeroed: y/n)

COUPON: MC-__          orientation as printed: ______________

rung | nominal | r1 | r2 | r3 | median | spread | note
-----+---------+----+----+----+--------+--------+-----------------

JUDGEMENTS (fit class / sag / curl):  by ______

FAILURES AND SURPRISES (a failed rung is a result):
```

## Rules

- A rung that did not print is a **result**, not a gap. Log it with what it
  looked like.
- Do not adjust a reading toward what it "should" be. If a number disagrees with
  the literature value, the number wins — that disagreement is why the coupon
  was printed.
- If the ladder brackets wrong (every rung passes, or every rung fails), the
  coupon is not a failure — it has told you which direction to re-centre. Log it
  and re-cut the ladder.
- Never fill a data sheet from a slicer preview or a render.
