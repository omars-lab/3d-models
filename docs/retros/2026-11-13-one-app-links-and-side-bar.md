---
date: 2026-11-13
repo: 3d-models
session: monitor-print-watcher
branch: local-links-stop-text
folded: no
---

## Snags
- `.claude/gates/doc_pointers.py`: a backticked path to a file another repo's PR has not written
  yet (bikar's side bar design note) fails `make validate`. Name a not-yet-written file in words,
  and backtick it only once it exists on that repo's main.
- `.claude/skills/check-local-links/scripts/local_links.py`: the first quieting change (#1038)
  tested only the session-start half; the Stop hook's output lived inline and was never run.
  Each hook mode's output should be a text function the self-test calls.
- bikar Sessions browser test: it waited for the first `svg` on the page, which broke as soon as
  the side bar put icons ahead of the drawing. Wait for the element the page's own code reads
  (`#svg-container svg`), never "the first of a tag".

## Worth copying
- After a sub-agent rebuilds a site's links, run the local link check on its build before showing
  Omar. The sub-agent's own browser check measured layout, not links.
