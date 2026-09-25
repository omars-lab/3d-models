# Backlog — first print and calibration

Loop: [`coaster-pipeline.md`](../../../.claude/loop-prompts/coaster-pipeline.md). Done list:
[`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: minis-01 printed, its record in [`docs/prints/`](../../prints), the CAL-CST bets it
covers settled (P4.3), and the standard-size plate (P5.2) built from the measured numbers.

## Open, in ROI order

1. **Turn a finished print into data** — waits on Omar printing minis-01, or a
   `bambu print capture` showing up. Then follow the `print-model` skill's compare loop:
   record in `docs/prints/<date>-minis-01/`, settle the CAL-CST bets it measures, update the
   counts in [`../../backlog.md`](../../backlog.md) §1. Record what was measured, not what was
   expected. (P4.3, board #4.)
2. **Keep [minis-01](../../plates/minis-01.yaml) ready to send.** Re-compose after any coaster
   change; slice, preflight and filament-sync against the live AMS trays; check each item's
   bikar pin against bikar main. Stops at the send.
3. **Tooling that blocks this plate** — fix only friction that stops minis-01. General tooling
   goes in the [print-infrastructure backlog](../print-infrastructure/backlog.md), new designs
   in the [catalog backlog](../catalog-expansion/backlog.md).
4. **Standard-size plate (P5.2)** — only after item 1 settles the CAL-CST numbers (board #6).
5. **FAQ (board #10)** — waits on Omar marking the six candidates (regenerate them with
   `python3 tools/session_reflect.py update-faq`) keep or discard and writing the answers.
   Then one PR, per the `session-reflect` skill; ids from `python3 tools/next_id.py next Q`.
   Never write an FAQ answer yourself.
6. **frame block (P5.3)** — only if a public GeoGebra file needs one (board #7).

## Owner-gated

Sending a print, which filament to load, `make setup-secrets` for bikar CI (board #9), the FAQ
review.

## After this plate

The prints beyond minis-01 — the machine card, the LEGO ladder, the W-series joint, the first
full orb — are sequenced in [`../../backlog.md`](../../backlog.md) §2, with every coupon and
bet in §3. When this goal is met, the next print is taken from there.
