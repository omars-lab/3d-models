---
name: use-cases-refresh-surfaces-anchor-drift
description: `validate.py --refresh` advances the bikar pin to origin/HEAD and REPORTS every anchored line that moved; the anchors must be hand-edited (19 in one refresh); the schema-mirror hook needs a `youtube:` pin once bikar vendors ggb_construction.json
metadata:
  type: project
---

`.claude/skills/maintain-use-cases/validate.py --refresh` re-pins the sibling `as_of` to
origin/HEAD and re-hashes, but it never rewrites a `` `repo:path:L<n> "literal"` `` anchor.
Every anchor whose literal moved is reported and must be edited by hand before the commit
passes hook `20-use-cases`. Advancing the bikar pin past several merged PRs moved 19 anchors
in one go (evaluator.ts, parser.ts, language-reference.md, grammar.md, calibration.ts).

Hook `41-schema-mirror`: once bikar vendors `packages/qiyas-schema/schemas/ggb_construction.json`,
use-cases.md frontmatter must pin `youtube:` in `as_of` and list `youtube: ../youtube` in
`repos`, or the commit is blocked with "pins no youtube commit".

**Why:** 2026-09-17, 3d-models #207: the refresh was needed for the bets.md regen and
surfaced the drift as a blocking side quest.

**How to apply (the cheap path, used on #245, 2026-09-17):** when the PR only needs the
*3d-models* pin moved (hook `20-use-cases` demands `as_of.3d-models == merge-base(HEAD,
origin/HEAD)` whenever a pinned doc such as `decisions-log.md` is staged), run `--refresh`,
then `sed` the bikar/qiyas/youtube lines back to their committed shas and re-run `validate.py`
— it exits 0 and the anchor drift never enters the PR. The refresh also moves the youtube pin
to a *local* HEAD (youtube has no origin), which is unpublished and must always be restored.

**How to apply (the full path):** Budget the anchor repair into any PR that refreshes pins; fix anchors by
grepping the literal at the new pin rather than guessing offsets. Related:
[[use-case-map-mechanics]], [[contract-and-schema-mirror]].
