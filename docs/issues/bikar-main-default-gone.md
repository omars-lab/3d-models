---
date: 2026-10-29
---

# The default bikar folder disappeared, and the prints check kept saying OK

**Found:** 2026-10-29, writing split-06's print record.

## What happened

Every tool here that reads bikar defaulted to `~/Workspace/git/bikar-main`. That folder was bikar's
only work tree while bikar itself was a bare repo. Some time before 2026-10-28 bikar became an
ordinary checkout at `~/Workspace/git/bikar`, and `bikar-main` was removed.

Nothing failed. The prints check could not read any bikar file, so it counted all 245 of its bikar
hash checks as skipped and still printed `OK`. The skip line said "bikar not checked out", which
reads as an expected state on a machine without bikar, not as "the folder you rely on is gone".
The commit hook for split-06's record showed the same line. Only running the check by hand with
`BIKAR_DIR` set showed what was being skipped.

## What changed

- Each default now names `~/Workspace/git/bikar`: the Makefile, the prints and site-graph checks,
  the `bambu` tool (and its test), the color-themes and cookbook scripts, and the machine-card
  check. The two skill pages that named `bikar-main` were updated too.
- The prints check's skip line now gives the cause that applies. With no bikar it names the folder
  it looked in and says to set `BIKAR_DIR`, so the next move of the folder shows in the first run
  after it. With bikar present, the 6 that still skip are meshes kept out of git (the third-party
  imports), pinned by their recipes, and the line says so instead of blaming bikar.
- With the default fixed, 239 of the 245 pins verify again.

Old research and done-list lines that name `bikar-main` were left alone. They record what was
read at the time.

## What did not change

A skip is still not a failure. The check is meant to run on a machine with no bikar at all, and
its self-test covers that case on purpose. Turning a missing folder into a failure would block
every commit in such a session, so the fix makes the skip say where it looked instead.
