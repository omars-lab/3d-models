---
name: use-case-map-mechanics
description: How the 3d-models use-case map and pointer gates behave in practice — what --refresh does and does not do, fetch/pull the sibling first, cite bikar by PR not relative link, Makefile targets go at the end
metadata:
  type: feedback
---

- `validate.py --refresh` re-pins `as_of` for ALL repos (siblings at origin/HEAD, self at the merge-base) and REPORTS anchor drift; it never moves a line number — apply each reported new line by hand, then `validate.py --full`.
- Before `--refresh`, `git -C ~/Workspace/git/bikar fetch origin` (a stale ref pins to a commit lacking the new file); the pointer gate resolves `bikar:` paths at a git ref, so a new bikar file is unresolvable until its PR merges and the fetch runs. Merge bikar BEFORE the 3d-models commit that cites it.
- A `../../bikar/...` markdown link is checked by D1 against the primary checkout on disk, which is usually parked stale — cite bikar via PR URL + bare backticked path instead. bikar's own pointer gate rejects a bare `docs/...` for a 3d-models doc: write `3d-models/docs/<file>.md`.
- Inserting a Makefile target above existing ones moves every pinned `Makefile:L<n>` anchor (five moved once): **new targets go at the END of the Makefile**.
- Merge commit with a conflicted map: resolve with HEAD's map + `USE_CASES_OK=1`, land the refreshed map next commit. Catalog edits trip the hook for UC8; `USE_CASES_OK=1` is correct there.
- The site-graph gate (hook 40, `docs/site-graph.json`) pins `index.html` line anchors — a gallery insertion moves them; re-pin by hand.
- Bumping a sibling pin drags in unrelated anchor drift; pinning deliberately behind is legitimate when the drift is another task's, and the map may pin self only to a master-reachable commit.

**Why:** the map's pins are claims; auto-moving them would rewrite a claim silently.

**How to apply:** fetch → merge sibling → `--refresh` → hand-repair → `--full`. Gates must agree from any checkout: [[gate-verdict-checkout-independent]]. Hook behaviour: [[3d-models-use-case-hook]].
