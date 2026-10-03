---
plate: minis-01
recipe: minis-01.yaml
iteration: 1
stage: sent
times_printed: 0
runs: []
answers: "Do the first two patterns read as coasters at 40 mm, with the straps at their floor?"
kind: new
maturity: experiment
bets:
  - CAL-CST-01
  - CAL-CST-02
unblocks: []
minutes: 73
grams: 22
bed_plates: 1
risk: ok
pictures:
  - minis-01-media/sheet.png
  - minis-01-media/art.png
  - minis-01-media/bed.png
---

# minis-01 — the first coaster plate

**In short.** Two solid 40 mm coasters each of CS-1 and CS-2, the first coaster plate. It went
to the printer from Bambu Studio on 2026-09-25, but there is no print record, so this page
cannot say whether it printed or what it looked like. That is the one thing to answer below.

## What it is

Recipe: [minis-01.yaml](minis-01.yaml). CS-1 ×2 and CS-2 ×2, the plain solid style (the
pattern raised on a slab), size 40. One bed, about 1 h 13 m and 22 g.

## Why it was printed

It checks how narrow a raised strap can be (CAL-CST-01) and the smallest feature that stays
readable at mini size (CAL-CST-02) ([bets.md](../../../.claude/skills/calibrate/bets.md)).

## Pictures

![minis-01 review sheet](minis-01-media/sheet.png)

![minis-01 art](minis-01-media/art.png) ![minis-01 on the bed](minis-01-media/bed.png)

## Your call

The send is written down in the
[dispatch notes](../../issues/first-party-dispatch.md#2026-09-26-the-send-picks-the-tray); nothing
says what came off the bed.

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
| 2026-09-19 | proposed — the first compose plate, plan step P4.2 | 3d-models #280 |
| 2026-09-25 | sent — from Bambu Studio, after `print send` could not pick the tray | [dispatch notes](../../issues/first-party-dispatch.md#2026-09-26-the-send-picks-the-tray) |
