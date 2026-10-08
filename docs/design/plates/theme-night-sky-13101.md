---
plate: theme-night-sky-13101
recipe: theme-night-sky-13101.yaml
iteration: 2
stage: waiting
times_printed: 0
runs: []
answers: "Night sky, one of its 4 plates: does its frame ×1 come out as the theme draws it, in PLA Sparkle Onyx Black Sparkle (13101)?"
kind: taste
maturity: experiment
bets: []
unblocks: []
minutes: 58
grams: 16.04
bed_plates: 1
risk: ok
pictures:
  - ../coaster/themes/gbv/night-sky.svg
  - theme-night-sky-13101-media/bed.png
---

# theme-night-sky-13101 — Night sky in Onyx Black Sparkle

**In short.** You picked Night sky as one of the first four themes to print (D-106: "all the
bottom row"). It prints as one plate per color, 4 plates in all; this one is PLA Sparkle Onyx Black Sparkle (13101):
frame ×1. Not on the printer: it prints once the spool is bought and loaded (see the buy list). The plate is [`theme-night-sky-13101.yaml`](theme-night-sky-13101.yaml). One bed, 58 minutes, about
16.04 g, $0.40 of filament. The other plates and the colors to buy are on
[the theme plates page](../coaster/themes/gbv-theme-plates.md).

## What it is

- **frame ×1**, in PLA Sparkle Onyx Black Sparkle (13101), the gBV coaster at sheets-04g's size
  (112.5 mm).
- Sparkling gold stars in deep blue, in a black frame with a fleck of glitter of its own.

**The color is picked at the send:** `bambu print send … --color "#2D2B28"`.
The recipe names no color (call 18), so say the color with the yes.

**Before you say yes:**

- **The pieces are cut at `gap: 0`, as sheets-04g printed them, and that fit was off:** the kites were too tight and the middle too loose. [sheets-04g-fit](sheets-04g-fit.md) tries kites from 0.05 to 0.25 mm and the middle from 0 to 0.15 mm, and has not printed (CAL-LSE-01). Printing this plate first repeats the old fit; printing the fit plate first lets these plates take its gaps, as a new iteration of each recipe.

## Why print it

A theme on a screen is a guess at how the colors sit together. Printing its plates and putting the
pieces in the frame settles it for this theme. The persona scores beside each theme are simulated,
not customer research; these prints are the first thing to hold them against.

## After the print

What gets asked when it comes off the bed, one row at a time (the review-print skill asks them).

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| frame ×1 | Does Onyx Black Sparkle look the way the theme picture draws it, beside the theme's other colors in the frame? | Close, not exact: the picture draws the color catalog's screen color, not a printed surface. | Looks right: the color stays in the theme. Off: the color-themes skill swaps in the nearest color and draws the theme again, and this plate is cut again in it. |
| frame ×1 | Does the frame lie flat, with no corner lifted, and do the other plates' pieces drop into it? | Flat: it is the frame sheets-04g printed at this size, on the same bed. | Flat: the frame is kept as it is. A lifted corner: the frame recipe gets a brim, as a new iteration, before the rest of the theme is printed. |

## Pictures

The theme as the gallery draws it.

![Night sky: the gBV coaster drawn flat in the theme's colors](../coaster/themes/gbv/night-sky.svg)

The slice: this plate's pieces on the bed.

![theme-night-sky-13101 on the bed: frame ×1 in Onyx Black Sparkle](theme-night-sky-13101-media/bed.png)

## Cost and risk

One bed, 58 minutes, about 16.04 g, $0.40 of filament (local slice, 2026-10-05, the X2D preset and
PLA Sparkle's own filament preset, nothing sent). One color, so no swaps.

**Risk: ok.** One frame, flat on one bed, the frame sheets-04g printed at this size.

## Your call

- [ ] **Approve as it stands**
- [ ] **Hold** — say why in the notes

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-05 | proposed — Night sky in Onyx Black Sparkle, by the color-themes skill's theme_plates.py (D-106) | this page |
| 2026-10-05 | sliced — local slice, 58 minutes, 16.04 g | this page |
