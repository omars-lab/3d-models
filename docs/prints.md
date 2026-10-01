# Prints

A **print** is the one event this repository records nowhere else: a physical
plate came off a machine, taught something, and that lesson belongs to the exact
geometry-and-process that produced it. This page is the reader for those records.
It records nothing of its own — each print is a checked-in directory, and its
format and gate are defined in [the prints-tab design doc](design/printing/prints-tab-design.md)
§4 and [`prints_gate.py`](../.claude/gates/prints_gate.py). Why one register and
not two: [D-046](working-model/decisions-log.md).

The reader is deliberately plain markdown at this rung (S6). The gallery-facing
`prints.html` surface — the styled version a visitor lands on — is a later rung
(S7); see the design doc §8–§9. Nothing here waits on that.

## Records — what has actually printed

Newest first. Each record names its run, its plate and a verdict per piece; the prints gate
checks every one.

- [2026-09-26-minis-04](prints/2026-09-26-minis-04/index.md) — minis-03 at 80 mm and half the
  height, plus the twist. Every piece `adjust`; the slice had fallen back to Bambu Studio's
  built-in settings.
- [2026-09-26-minis-03](prints/2026-09-26-minis-03/index.md) — minimal-frames at 40 mm and a
  dovetail pair. Every piece `adjust`: much too small, the pair loose.

Nothing was measured with a tool on either, so no bet has moved yet. `make validate-prints`
prints how many records it checked.

## Queue — what to print next

The order lives on [the plates page](plates/README.md), computed from each plate's review page
and the weights in the
[prioritize-prints skill](../.claude/skills/prioritize-prints/scoring.md). This page stores no
rank of its own, because a second scheduler is the one thing the design forbids
([design doc](design/printing/prints-tab-design.md) §6). A plate page also records whether
Omar approved it and how many times it printed, counted from the records above.

The calibration plates the [print register](tasks/coaster-pipeline/backlog.md) §2 sequences —
Plate 1, the machine card, then Plate 4, the star orb — have no plate page yet, so they are not
in that queue. Plate 4 settles no calibration bet at all, which is why the queue's value and
"bets it would settle" are never the same number.

## What a record holds

A record pins the two identities that together decide what a plate can teach
(design doc §3):

- **Geometry** — the `.bkr` source, the blob's `sha256`, the bikar commit it was
  read at, and the piece selected. The same file at two commits is two versions.
- **Process** — the nine-field profile header the print protocol already defines
  ([`protocol.md`](../.claude/skills/calibrate/protocol.md)): machine, material,
  spool, nozzle, layer height, slicer profile, ambient, instrument. The same
  geometry at two layer heights is two versions.

On top of that pair: the outcome, the readings (each linked to the bet it moves),
and the photos of the plate. The prose body is the operator's account, and is
ungated on purpose — a plate may measure a number a later audit kills (design doc
§4.2).

## Consumes (read-only)

This page owns none of these; it points at them:

- [`bets.md`](../.claude/skills/calibrate/bets.md) — the calibration bets a
  reading settles.
- [`protocol.md`](../.claude/skills/calibrate/protocol.md) — the measurement
  ceremony and the profile header a reading must carry.
- [`design/printing/calibration-design.md`](design/printing/calibration-design.md) — the machine-card
  expectations a Plate 1 reading is checked against.
- [the prototype catalog](../.claude/skills/prototype/catalog.md) — the backlog of
  prototypes to print, and where a learning lands when it propagates.
