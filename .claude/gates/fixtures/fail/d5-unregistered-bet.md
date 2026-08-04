# Fixture: a default that rests on a bet nobody registered

Asserted FAIL fixture for `docs_gate.py`. Expected: exactly one finding,
`D5 (K9)`.

## The default

**Default:** relief depth `0.6` mm — no source can settle it; it is bet
CAL-ZZZ-99 and ships from the coupon reading.

This satisfies D3, which asks only that a default name a bet id *or* a citation
and never asked whether the bet exists. That is the gap D5 closes, and this
file is the shape it shipped in: `docs/text-emit-design.md` carried three
gate-green defaults on two ids that were registered nowhere.

`CAL-ZZZ-99` is chosen so it can never become real by accident — `ZZZ` is not a
subsystem and `99` is past the end of every series.

## What is deliberately *not* a finding

A bet id in ordinary prose is a mention, not a discharge, so the paragraph
below must stay clean even though `CAL-ZZZ-98` is equally unregistered:

Appendix B considered minting CAL-ZZZ-98 for the seam-strength measurement and
declined, because the same quantity is already open as a question elsewhere and
one quantity is one bet. Recording a decision *not* to mint an id is correct
prose, and a rule that fired here would be a rule someone switches off.
