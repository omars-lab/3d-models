# Scoring: how a plate earns its place in the queue

Read at run time by [`plates_gate.py`](../../gates/plates_gate.py) and by the skill. Change the
weights here, run `python3 .claude/gates/plates_gate.py --write`, and the queue on
[`docs/plates/README.md`](../../../docs/plates/README.md) follows. Add a line to the round log
when you do, saying what changed and why.

## The sum

**Value** is what a plate teaches:

- each calibration bet in `bets:` that the plate can move with a reading taken by hand or tool
  (not a bet it merely touches), times `per_bet`;
- each open decision in `unblocks:` that the print lets Omar make, times `per_unblock`;
- a bonus for its `kind`: a `new` question, a `taste` look at something already understood, or
  a `repeat` of a plate already printed.

**Cost** is hours on the machine: `minutes / 60`, plus `grams / grams_per_hour`, so filament
counts as time at a fixed rate.

**ROI** is value divided by cost. The queue lists plates highest ROI first.

Two things override the sum:

- `risk: hold` leaves a plate out of the queue, listed as held. A plate that could damage the
  printer is not ranked until its risk is dealt with. `watch` stays in the queue, and the page
  says what to watch.
- `after: <plate>` keeps a plate below another one until that one has printed, for a plate whose
  question depends on another's answer.

## Weights

These are a first guess, set on 2026-09-30, not measured. Nothing yet says a bet is worth
exactly one unblocked decision. Change them when a ranking looks wrong to Omar, and write down
the case that showed it.

```yaml
weights:
  per_bet: 2
  per_unblock: 2
  kind: {new: 2, taste: 1, repeat: 0}
  grams_per_hour: 100
```

- `per_bet: 2` and `per_unblock: 2`: a bet and a decision count the same. A bet feeds every later
  design, a decision feeds the one design that asked; they are equal until a case shows one
  should lead.
- `kind`: a new question beats a look at something known, which beats a reprint.
- `grams_per_hour: 100`: 100 g of PLA counts as one hour. At these plates' sizes filament barely
  moves the order; it matters for a heavy plate.

## Round log

| Date | What changed | Why |
|---|---|---|
| 2026-09-30 | First weights, above | The queue starts; minis-05 and minis-06 are the first plates ranked |
