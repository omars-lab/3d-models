---
plate: minis-02
recipe: minis-02.yaml
iteration: 1
stage: sent
times_printed: 0
runs: []
answers: "What does each coaster style look like in the hand, for both patterns?"
kind: taste
maturity: experiment
bets:
  - CAL-CST-01
  - CAL-CST-07
  - CAL-CST-08
unblocks: []
minutes: 156
grams: 36
bed_plates: 1
risk: ok
pictures:
  - minis-02-media/sheet.png
  - minis-02-media/bed.png
---

# minis-02 — one mini of each style

**In short.** One 40 mm coaster in each style, for CS-1 and CS-2: solid, minimal, interlock,
and the CS-1 twist. Omar asked for it on 2026-09-25 after minis-01 showed only the solid style.
It went out from Bambu Studio the same day, but there is no print record, so this page cannot
say whether it printed.

## What it is

Recipe: [minis-02.yaml](minis-02.yaml). Seven pieces, size 40: solid, minimal and interlock for
each pattern, plus the CS-1 twist at height 6, twist 15. One bed, about 2 h 36 m and 36 g.

## Why it was printed

To see every style side by side before choosing one. It also touches the strap floors
(CAL-CST-01, CAL-CST-07) and the twist lean ceiling (CAL-CST-08)
([bets.md](../../../.claude/skills/calibrate/bets.md)).

## After the print

What gets asked when it comes off the bed, one row at a time (the review-print skill asks them).

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| all seven | For each pattern, which style looks best in the hand: solid, minimal, interlock, or the CS-1 twist? | No guess: this is a taste call, and the reason the plate exists. | The style picked is the one the next coaster plates for that pattern are made in; the others stay in the Lab. |
| minimal and interlock, both patterns | Do the open straps stand up whole at 40 mm? | Whole, if the floors CAL-CST-01 and CAL-CST-07 bet on hold. | Whole: both bets move. Broken: the floor goes up for open styles. |
| CS-1 twist | Does the twist (height 6, twist 15) print clean, with no droop where it leans? | Clean, if the lean ceiling CAL-CST-08 bets on holds. | Clean: the twist stays a style at that lean and CAL-CST-08 moves. Drooped: the lean ceiling comes down. |

## Pictures

The sheet shows one thing to know: at 40 mm the minimals read almost solid. Openness is 0.05
and 0.07 for the two minimals and 0.03 for the twist. The review-print rubric flags anything at
0.15 or under, and minis-03 moved to minimal-frames for that reason.

![minis-02 review sheet](minis-02-media/sheet.png)

![minis-02 on the bed](minis-02-media/bed.png)

## Your call

- [ ] **It printed** — I write the record, with your verdict per piece if you give one
- [ ] **It did not print, or it failed** — say what happened in the notes
- [ ] **I don't remember** — the page stays at sent

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-09-25 | proposed — one mini of each style, at Omar's request | 3d-models #314, #315 |
| 2026-09-25 | sent — from Bambu Studio | [dispatch notes](../../issues/first-party-dispatch.md#2026-09-26-the-send-picks-the-tray) |
