---
date: 2026-11-11
repo: 3d-models
session: monitor-print-watcher
branch: "one-app-design; earlier this session 3d-models #1017, Print Hub #36 and #37"
folded: no
---

## Snags
- `.claude/gates/docs_gate.py` D3: a `**Default:**` on an open call (a suggested answer, not a
  number) fails unless a link sits in the same paragraph. Writing "Suggested:" for proposals
  avoided it; the `write-design` skill could say so.
- `.claude/gates/docs_gate.py` D9: a research note needs `date` and `feeds` as front-matter
  properties; a bulleted "Date:" line in the body does not count. `ground-design-doc` should show
  the header shape.
- Headless Chrome at 390 px width drew the mockup wider than the screen; the chrome-devtools
  `emulate` call (390x844x2, mobile) gave the true phone picture. Its screenshot path must sit
  inside the workspace, then `mv` it.

## Worth copying
- Checking the four load-bearing facts by hand after the survey agents reported (editor with no
  pattern store, the tick-box patterns, the gallery's link to the Lab index, the launcher card)
  is what ruled out serving pages from the Print Hub. A survey line alone would not have.
- Handing the readability score to a fresh agent instead of grading my own rewrite, as
  `review-design` asks.
