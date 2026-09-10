# Prints

A **print** is the one event this repository records nowhere else: a physical
plate came off a machine, taught something, and that lesson belongs to the exact
geometry-and-process that produced it. This page is the reader for those records.
It records nothing of its own — each print is a checked-in directory, and its
format and gate are defined in [the prints-tab design doc](prints-tab-design.md)
§4 and [`prints_gate.py`](../.claude/gates/prints_gate.py). Why one register and
not two: [D-046](decisions-log.md).

The reader is deliberately plain markdown at this rung (S6). The gallery-facing
`prints.html` surface — the styled version a visitor lands on — is a later rung
(S7); see the design doc §8–§9. Nothing here waits on that: this page renders the
true empty state today and the same shape, populated, the day the first plate
lands.

## Records — what has actually printed

Nothing yet. No plate has come off a machine, so there is no record to read. The
gate agrees, and says so out loud rather than passing silently over an empty set:

```
$ make validate-prints
prints: 0 records checked — docs/prints/ is empty (nothing printed yet)
```

That printed count is the honest zero-state, not a false green — it is the whole
reason the gate could ship before the first print ([the design doc](prints-tab-design.md)
§7, [D-046](decisions-log.md)).

When the first record lands, this section becomes a list — one row per run, newest
first — each naming its run, plate, status, what it measured, and which bet (if
any) the reading moved. The first run will be Plate 1, the machine card, because
it defines the process-profile header every later plate reuses (design doc §10).

## Queue — what to print next

The order is not decided here. It is [`backlog.md`](backlog.md) §3.8's argument,
presented — this page stores no rank of its own, because a second scheduler is the
one thing the design forbids ([design doc](prints-tab-design.md) §6). Read the
backlog for the live order and the reasoning; the plates in flight are:

- **Plate 1 — Machine Card.** Defines the profile header and carries the readings
  the most bets depend on; it is first for that reason, not because it is cheap.
  → [`backlog.md`](backlog.md) §3.8, [`bets.md`](../.claude/skills/calibrate/bets.md)
- **Plate 4 — the star orb.** The flagship confidence print. It settles no
  calibration bet at all — which is exactly why the queue order and the
  "bets it would settle" figure are shown as two different things, never one. A
  plate can rank high and settle nothing.
  → [`backlog.md`](backlog.md) §3.8

Beside each plate, the populated tab shows how many bets a run would settle. That
figure is **not** the rank, and the number itself is owned by
[`bets.md`](../.claude/skills/calibrate/bets.md) and the backlog, not restated
here — this reader points at the owner rather than keeping a copy that could drift.

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
- [`calibration-design.md`](calibration-design.md) — the machine-card
  expectations a Plate 1 reading is checked against.
- [the prototype catalog](../.claude/skills/prototype/catalog.md) — the backlog of
  prototypes to print, and where a learning lands when it propagates.
