---
date: 2026-09-28
---

# The use-case check skipped every bikar, qiyas and youtube pointer for 11 days

Found 2026-09-28 while reading the use-case validator's output from a clean run.

## What happened

The use-case map (`.claude/skills/maintain-use-cases/use-cases.md`) has two lists at the top:
`as_of`, the commit each repo is pinned at, and `repos`, where each sibling repo is checked out
(`../bikar`, `../qiyas`, `../youtube`). Commit d220bb6 (#246, 2026-09-17) wrote commit hashes
into `repos` instead of paths. From then on the validator looked for a folder named after a hash,
did not find one, printed "not checked out locally" as a warning, and moved on. Every pointer into
bikar, qiyas and youtube went unchecked, and `make validate` stayed green because a warning never
failed it. The summary line still said "all valid".

## What the fix turned up

Restoring the paths and pinning each sibling at its current default-branch tip showed:

- **28 pointers had drifted** in the 11 days: 26 in the map and 2 in `docs/guides/orb-pipeline-map.md`.
  Each one was moved to the line its quoted text is on now. None of the claims next to them had
  gone false.
- **Two pointers had never been checked at all**, even before #246, because the validator could
  not read them. One quoted text containing a backtick, which ends the code span early. The other
  used `\"` inside the quote. The validator saw neither as a pointer. The backtick one also named
  the wrong line even at its old pin (L519, when the text sat at L694). Both now quote plain text
  and point where the code actually is.
- **One pointer quoted text that is on the wrong line**: `"BrickFootprint"` matched a list that
  mentions the name, not the grammar rule that defines it. It now quotes `"BrickFootprint ="`.
- **The validator's own self-test never ran in `make validate`.** It exists (`--self-test`) but no
  target called it.

## What now stops it happening again

- **A hash in `repos` is refused**, with a message saying the hash belongs in `as_of` and `repos`
  holds the path. So is a pinned sibling with no `repos` entry.
- **An unreadable sibling is a failure, not a skip.** If a pinned sibling is not checked out, the
  validator fails and names the paths it tried. To run without a sibling on purpose, set
  `USE_CASES_SKIP_MISSING_SIBLINGS=1`: the run passes, but it prints "SKIPPED … NOT checked" for
  each repo, and the summary says "valid where checked … N NOT CHECKED" instead of "all valid".
- **A pointer the validator cannot read is an error**, in the map and in every other markdown file.
  Anything that starts like a pointer (`` `repo:path:L12 ``) but does not parse is reported with its
  file and line.
- **The self-test runs in `make validate`**, through a new `validate-use-cases-self-test` target.
  It builds a throwaway map and repo and checks each case above: the hash refusal, the missing
  entry, the missing checkout failing, the opt-out warning and honest summary, a missing page
  catalog failing, and the unreadable-pointer check.
- **Git must run this repo's hooks.** `core.hooksPath` must be exactly `.githooks`, the relative
  path, so each work tree runs the hooks on its own branch. Earlier in the same session the shared
  clone's setting had been found pointing somewhere else and reset by hand; nothing checked it.
  `hook_parity.py --check` now fails when it is unset, absolute, or any other folder, and says to
  run `make setup-hooks`. That check runs on every commit (hook `05-hook-parity`) and in
  `make validate`. Its self-test sets each bad value in a scratch repo and checks that it fires.

## The lesson

A check that prints a warning and carries on is a check that is off. When a check cannot look at
something, it has to fail, or say loudly and in its summary that it did not look.
