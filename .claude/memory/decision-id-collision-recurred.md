---
name: decision-id-collision-recurred
description: Second decision-id collision 2026-09-17 — master merged its own D-055 first, so the nine construction decisions became D-056…D-064 (renumbered corpus-wide in 3 docs + the log with one perl); check the log on origin/master for the next free id right before merging
metadata:
  type: project
---

The collision in [[decision-id-collision]] recurred: the constructions plan reserved
D-055…D-063 while master merged the X2D session's D-055 (first-party MQTT). Rule held —
first-merged owns the id; the open PR renumbered to D-056…D-064 across
`docs/decisions-log.md`, `docs/construction-equivalence.md`,
`docs/geogebra-construction-import-design.md` and
`docs/research/geogebra-construction-import-survey.md` with
`perl -pi -e 's/\bD-0(5[5-9]|6[0-3])\b/sprintf("D-%03d",$1+1)/ge'`.

**Why:** two sessions open on the same repo for a week each grabbed the same next id.

**How to apply:** Right before merging a PR that adds decisions, re-read the last id on
`origin/master`; if taken, shift the whole range with one regex over every doc that cites it,
and rebuild `decisions-log.md` from master + the branch's sections rather than resolving
the conflict line by line.
