# Fixture: D4 must fire on a withdrawn number restated as fact

Asserted FAIL fixture for rule D4 (K1), taken verbatim from the defect that
built the rule. The 2026-07-29 lego-lab audit found `±0.1–0.2 mm printer
accuracy` has no vendor source; the correction was applied to two docs, and this
line went on standing in `tile-wall-design.md`'s Appendix A for five days.
(The number is written as code above so it counts as a mention, not a use — the
same rule the other markers get.)

- **Precision + tolerance ecosystems**: LEGO ±0.01 mm vs FDM ±0.1–0.2 mm;
  [Multiboard](http://www.multiboard.io/) user tolerance sliders

The bullet names the number and says nothing about its status. Expected:
exactly one finding, `D4 (K1)`.

## What this fixture also shows about the rule's reach

The *same* defect had a second site — §2's "LEGO-class interference (±0.02 mm
sensitivity) is 10–20× beyond FDM tolerance". That one restates the withdrawn
figure as a multiple instead of quoting it, so it contains no literal for D4 to
match and **D4 does not catch it**. Confirmed by running the gate against the
pre-fix file: one finding, at Appendix A, not at §2. D4 is a floor on the
cheapest form of the mistake, not a proof the number is gone.
