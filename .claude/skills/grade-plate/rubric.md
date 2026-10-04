# Plate maturity rubric

Read at run time by `tools/plate_grade.py` and by the plates gate's P8 rule
(`.claude/gates/plates_gate.py`, `read_rubric`). Change a number here, add a line to the round
log saying why, and both pick it up. The levels and what each must show are in
[plate-maturity-design.md](../../../docs/design/printing/plate-maturity-design.md).

```yaml
maturity:
  keeps_for_repeatable: 1
  production_fill: 0
```

## What each number means

- **`keeps_for_repeatable`** — how many of a piece's latest verdicts, across every print record
  on any plate, must all be `keep` before the piece counts as repeatable. A plate is repeatable
  when every piece in its recipe is. One since 2026-10-04: one clean print, judged good by
  Omar, is enough. It was two, because one keep can be luck. The latest K still counts, so a
  piece whose last verdict is `adjust` or `drop` is not repeatable, whatever came before.
- **`production_fill`** — the share of the first bed the pieces must cover, outline from above,
  for a plate to be production. Measured by `python3 tools/plate_grade.py --fill <plate.3mf>`.
  `0` means no bar, which is the setting since 2026-10-04: a plate must still carry a measured
  `bed_fill` on its page, so how empty a production bed is stays in view, but no number stops
  it. It was 0.45, a first guess never measured against a packed plate. Worked by hand at
  0.45: four 100 mm round coasters in a 2 × 2 on the 256 mm bed cover about 0.48 and pass;
  four 90 mm coasters cover about 0.39 and do not, and five in rows of 2, 1, 2 cover about
  0.49. Packing a bed is still worth doing for time and filament (the plate-packing skill on
  the backlog); it is no longer what makes a plate production.

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
| 2026-10-04 | 1 keep, no fill bar (0) | Omar after phones-02 printed: "print good, lets save it as prod ready", then picked "Change the production rule" over reprinting it once or packing it first. phones-02 had one print and covers about 2% of the bed, so both numbers had to move. Production now means "printed once, judged good, recipe frozen", not "packed and proven twice" (D-098) |
