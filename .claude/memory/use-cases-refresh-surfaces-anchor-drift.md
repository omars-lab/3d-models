---
name: use-cases-refresh-surfaces-anchor-drift
description: "`validate.py --refresh` advances sibling pins and REPORTS every anchored line that moved; since 3d-models #418 (2026-09-29) `validate.py --repair` moves the unambiguous ones (one-line pointer, anchor on exactly one line); the schema-mirror hook needs a `youtube:` pin once bikar vendors ggb_construction.json"
metadata:
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-29T16:23:29.434Z
---

`.claude/skills/maintain-use-cases/validate.py --refresh` re-pins the sibling `as_of` to
origin/HEAD and re-hashes, but it never rewrites a `` `repo:path:L<n> "literal"` `` anchor.
Every anchor whose literal moved is reported. Advancing the pins moved 19 anchors on
2026-09-17 and 12 on 2026-09-29.

**Since #418 (2026-09-29): run `validate.py --repair` after `--refresh`.** It moves each
one-line anchored pointer whose anchor sits on exactly one line (at the sibling's pin, or
live for 3d-models) to that line, in the map and in any doc outside it, then re-validates.
Ranges and anchors found twice or nowhere stay errors, so fix those by grepping the literal
at the new pin. It also catches self pointers your own edit just shifted (CLAUDE.md,
validate.py). All 12 on 2026-09-29 were one-line, single-match cases.

Hook `41-schema-mirror`: once bikar vendors `packages/qiyas-schema/schemas/ggb_construction.json`,
use-cases.md frontmatter must pin `youtube:` in `as_of` and list `youtube: ../youtube` in
`repos`, or the commit is blocked with "pins no youtube commit".

**Why:** 2026-09-17, 3d-models #207: the refresh was needed for the bets.md regen and
surfaced the drift as a blocking side quest. It recurred on every pin advance, so the fix
went into the tool (#418) instead of being done by hand again.

**How to apply (the cheap path, used on #245, 2026-09-17):** when the PR only needs the
*3d-models* pin moved (hook `20-use-cases` demands `as_of.3d-models == merge-base(HEAD,
origin/HEAD)` whenever a pinned doc such as `decisions-log.md` is staged), run `--refresh`,
then `sed` the bikar/qiyas/youtube lines back to their committed shas and re-run `validate.py`
— it exits 0 and the anchor drift never enters the PR. Now that `--repair` exists, taking
the full advance is usually just as cheap.

**How to apply (the full path):** `--refresh`, then `--repair`, then hand-fix whatever is
still reported. Related: [[use-case-map-mechanics]], [[contract-and-schema-mirror]].
