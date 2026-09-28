# Fixture: D1 must fire on an obsidian link to a heading the note does not have

Asserted FAIL fixture for rule D1 (K9), `obsidian://` form. The CS-1 note has a
heading per coaster style; `frame` is not one of them (the style is
`minimal-frame`), so this link opens the note and lands nowhere:
[CS-1, frame](obsidian://open?vault=docs&file=catalog%2Fpatterns%2Fsimple-20-step-six-fold-star-rosette-cs-1.md%23frame).

Expected: exactly one finding, `D1 (K9)`.
