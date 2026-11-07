---
title: Print evidence log
---

# Print evidence log

What the prints have taught us, each line linked to the print that shows it. This page is
written by `.claude/skills/review-print/scripts/evidence_log.py` from the print records, the
decisions log, the issue write-ups, the calibration bets and the plate pages. Do not edit it by
hand: change the record, then run the script with `--write`.

## Decisions

Each decision a print led to, from the record's `feedback.decisions`. The full reasoning is in the [decisions log](../working-model/decisions-log.md).

| Decision | What it says | Print record | Plate page | Printed |
|---|---|---|---|---|
| [D-098](../working-model/decisions-log.md#d-098--production-is-one-good-run-as-laid-out-with-no-fill-bar) | Production is one good run as laid out, with no fill bar | [2026-10-04-phones-02](2026-10-04-phones-02/index.md) | [phones-02](../design/plates/phones-02.md) | 2026-10-04 |
| [D-115](../working-model/decisions-log.md#d-115--on-a-coupon-the-upper-halfs-id-goes-on-its-outer-face) | On a coupon, the upper half's id goes on its outer face | [2026-10-09-spl-1](2026-10-09-spl-1/index.md) | [spl-1](../design/plates/spl-1.md) | 2026-10-09 |
| [D-116](../working-model/decisions-log.md#d-116--a-split-coasters-stud-gap-is-025-mm) | A split coaster's stud gap is 0.25 mm | [2026-10-09-spl-2](2026-10-09-spl-2/index.md) | [spl-2](../design/plates/spl-2.md) | 2026-10-09 |
| [D-117](../working-model/decisions-log.md#d-117--the-coaster-bottom-slits-try-the-gold-plate-with-both-coasters) | The coaster-bottom slits: try the gold plate, with both coasters | [2026-10-12-bedface-2](2026-10-12-bedface-2/index.md) | [bedface-2](../design/plates/bedface-2.md) | 2026-10-12 |
| [D-119](../working-model/decisions-log.md#d-119--the-flange-coasters-socket-wall-is-07-mm) | The flange coaster's socket wall is 0.7 mm | [2026-10-25-split-08](2026-10-25-split-08/index.md) | [split-08](../design/plates/split-08.md) | 2026-10-25 |

## Issues

Write-ups in `docs/issues/` that a print record links: a print that went wrong and changed how we work.

| Issue | Print records that link it |
|---|---|
| [The bed-face preset: clean in the slicer's plan, no cleaner in print](../issues/bed-face-preset-failed-in-print.md) | [2026-10-11-bedface-1](2026-10-11-bedface-1/index.md), [2026-10-12-bedface-2](2026-10-12-bedface-2/index.md), [2026-10-12-bedface-3](2026-10-12-bedface-3/index.md), [2026-10-13-bedface-4](2026-10-13-bedface-4/index.md), [2026-10-14-bedface-5](2026-10-14-bedface-5/index.md) |
| [sheets-04g: the kites too tight, the middle piece too loose](../issues/sheets-04g-fit.md) | [2026-10-04-sheets-04g](2026-10-04-sheets-04g/index.md) |
| [sheets-04b was sliced for the wrong build plate](../issues/sliced-for-wrong-plate.md) | [2026-10-03-sheets-04b](2026-10-03-sheets-04b/index.md) |

## Assumptions

Calibration bets a print record names: a number we print by before a print has settled it. The state comes from `.claude/skills/calibrate/bets.md`.

| Bet | What it is about | State | Print records |
|---|---|---|---|
| CAL-FIT-01 | `FIT_GAP_MM` press/snug/sliding/free gap ladder | provisional | [2026-09-26-minis-03](2026-09-26-minis-03/index.md), [2026-09-26-minis-04](2026-09-26-minis-04/index.md), [2026-10-03-sheets-04b](2026-10-03-sheets-04b/index.md) |
| CAL-HOL-01 | `PrinterProfile.holeCompMm` per material | provisional | [2026-10-03-sheets-04b](2026-10-03-sheets-04b/index.md) |

## Risks

Plates printed and finished but not judged yet. Until they are, what they test is still a guess, and the longer they wait the more a later plate may replace them.

- [closeout-1 — one plate to close the flange coaster's open questions](../design/plates/closeout-1.md): 0 of 5 questions answered. Still open:
  - Row 1: a face that is flat out to its points, with no curve at the edges, and whether any of the four is flatter than STAR-GRID.
  - Row 2: halves that close flat and do not turn, where STAR-STOCK can turn round its one pin; and a bottom as clean as STAR-STOCK's.
  - Row 3: halves that close flat and hold without rocking. MIDDLE-STOCK has a centre pin and six round it, MIDDLE-PINS5 a centre pin and four.
  - Row 4: which kites go in without forcing and do not rattle. Both copies should agree.
  - Row 5: a brim kite whose bottom edge is straighter and whose corners are sharper than its plain twin, with no lip left from the brim, and whether it still fits the pocket like its twin.
- [dragon-egg-1 — one small dragon egg, in silk blue](../design/plates/dragon-egg-1.md): 0 of 1 questions answered. Still open:
  - Row 1: 1. Take the egg off the bed. 2. Turn it in your hand and look at the scale tips, most of all on the lower half. Do the scales come out clean, or do some tips droop or string? Clean, rough tips, or failed
