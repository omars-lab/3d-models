---
date: 2026-11-16
repo: 3d-models
session: consolidate-design-print-app
branch: always-on-comments-notes, PR #1049; gallery-deploy-sidebar, PR #1050 (bikar #387)
folded: no
---

## Snags
- The always-on app on 7136 never had a Comment button; only the comment server on 7137 adds
  it, and nothing started 7137 at login. Fixed with a second launch agent (bikar #387). A page
  that "should have comments" is worth checking on the port Omar actually opens, not the one
  the setup names.
- bikar's pre-push hook (the full local checks, about 15 minutes) failed with 111 "connection
  refused" errors while 3d-models' `make validate` ran beside it: its test servers died under
  the load. Run it alone; the retry with nothing else running passed.
- A plugin hook from the earlbear marketplace (decision-tracking-manager) fires on every Edit
  here and fails because its script is gone from disk. The edits still apply. It is not ours
  to fix.

## Worth copying
- Before a gallery deploy, serve the built folder on a spare port and look at each Lab page at
  1280 and 390 px with the console open; after it, list the live page's requests. A failed
  request from the host's own visitor-counting script is not the gallery's.
