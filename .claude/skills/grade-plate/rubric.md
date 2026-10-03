# Plate maturity rubric

Read at run time by `tools/plate_grade.py` and by the plates gate's P8 rule
(`.claude/gates/plates_gate.py`, `read_rubric`). Change a number here, add a line to the round
log saying why, and both pick it up. The levels and what each must show are in
[plate-maturity-design.md](../../../docs/design/printing/plate-maturity-design.md).

```yaml
maturity:
  keeps_for_repeatable: 2
  production_fill: 0.45
```

## What each number means

- **`keeps_for_repeatable`** — how many of a piece's latest verdicts, across every print record
  on any plate, must all be `keep` before the piece counts as repeatable. A plate is repeatable
  when every piece in its recipe is. Two because one keep can be luck, and a keep followed by
  an adjust is a piece judged wrong last. A first guess: nothing has been printed twice yet.
- **`production_fill`** — the share of the first bed the pieces must cover, outline from above,
  for a plate to be production. Measured by `python3 tools/plate_grade.py --fill <plate.3mf>`.
  0.45 is a first guess, not measured against a packed plate (there is none yet). Worked by
  hand: four 100 mm round coasters in a 2 × 2 on the 256 mm bed cover about 0.48 and pass.
  Four 90 mm coasters (the gBV coaster's size) cover about 0.39 and do not; with 2 mm between
  them, rows of 2, 1, 2 fit five in 251 mm of bed, about 0.49, which passes. So at 0.45 a bed
  of 90 mm coasters passes only when it holds the fifth one a square grid leaves room for. A
  plate of small pieces reaches the number by printing more of them; a plate of one large piece
  by being large. Whether 0.45 is right is Omar's call 2 in the design.

## What the plates sliced so far cover

Measured 2026-10-03 with `--fill`, on the slices in the vault's `build/plates/`. None of these
plates was packed: each was laid out to answer a question, as an experiment should be.

| Plate | Objects on bed 1 | Fill |
|---|---|---|
| minis-01 | 4 | 0.092 |
| minis-02 | 7 | 0.169 |
| minis-03 | 5 | 0.121 |
| minis-04 | 6 | 0.552 |
| sheets-04 | 7 | 0.278 |
| sheets-04b | 6 | 0.208 |

## Round log

| Date | Change | Why |
|---|---|---|
| 2026-10-03 | first numbers: 2 keeps, 0.45 fill | no plate has printed twice and none was packed, so neither can be measured yet; see above |
