# Fixture: D1 must fire on a heading link whose heading is gone

Asserted FAIL fixture for rule D1 (K9), `#part` form. This reproduces the
commonest dead link measured on 2026-09-27: the file exists, but the heading was
renamed after the link was written, so a click opens the file and scrolls nowhere.
`decisions-log.md` had four of these to D-039 alone.

The taxonomy's K9 section is
[here](../../../../docs/grounding-defect-taxonomy.md#k9--broken-pointer).

Expected: exactly one finding, `D1 (K9)`.
