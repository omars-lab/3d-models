# Fixture: D6 must fire on a code span that runs onto the next line

Asserted FAIL fixture for rule D6 (render). This reproduces the line in
construction-equivalence.md §4 that left the rest of that file as raw text in
Obsidian's editor (review thread 7rlhya):

The naqsh side is `bikar render --piece Coaster --format stl
--check` of the same file.

Expected: exactly one finding, `D6 (render)`, on the line the span opens — not
a second one on the line that closes it.
