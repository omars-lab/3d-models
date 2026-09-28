---
title: "Floating regions" slicer warning
kind: slicer-warning
---
# Fixture: D8 must fire on frontmatter that is not valid YAML

Asserted FAIL fixture for rule D8 (render). The title opens with a quoted phrase
and carries on after the closing quote, which YAML cannot parse; Obsidian then
shows none of the note's properties. Wrapped in single quotes, the whole
title parses.

Expected: exactly one finding, `D8 (render)`.
