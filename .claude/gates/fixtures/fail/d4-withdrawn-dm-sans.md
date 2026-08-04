# Fixture: D4 must fire on the withdrawn DM Sans crossing count

Asserted FAIL fixture for rule D4 (K1)'s second registered withdrawal, taken
from the line as it stood in `outline-font-emit.md` §2 before 2026-08-04. The
survey's own script reported `6 of 37` DM Sans glyphs with crossing contours;
writing the bake forced the failing glyphs to be named one at a time, and `Y`
turned out to be a single 9-point straight-line contour that cannot cross.

| **DM Sans Bold (wght 700)** | 6 of 37 | crossing contours |

The row names the number and says nothing about its status. Expected: exactly
one finding, `D4 (K1)`.

## Why this withdrawal is registered at all

The number is cheap to re-type and expensive to disbelieve: it appears in a
table, in prose, and in a bake script's docstring copied from that prose, and
every one of those sites reads as measured. The literal `4 self-intersections`
is registered with it for the same reason — it is the other half of the same
sentence. Neither literal survives the correction, so a live match is always a
rebuild, never the original.

What D4 still cannot see here is the glyph list itself. `A B H Q R Y` is written
as code at every site in this corpus, and `strip_code` blanks inline code spans
before the withdrawal patterns run — the same exemption every marker gets. So
the count is gated and the membership claim behind it is not, which is the D4
reach limit the first fixture already records, in a second shape.
