#!/bin/sh
# A gate must reach the same verdict when git runs it as when a person does.
#
# git exports `GIT_DIR` to the hooks it launches from a **linked worktree** (not
# from a primary clone — measured 2026-08-03, and the difference is why this went
# unnoticed for so long). `GIT_DIR` outranks `-C`: it names the repository, and
# `-C` is left naming only a directory. Two consequences, both silent:
#
#   1. `maintain-use-cases/validate.py` resolved its root with
#      `git -C <skills dir> rev-parse --show-toplevel`, which under `GIT_DIR`
#      answers with the skills directory. `repo_dir()` then looked for
#      `.claude/skills/bikar`, missed, and emitted "not checked out locally" —
#      a **warning**. The commit validated its 52 self-repo pointers, skipped all
#      67 pinned sibling ones, and exited 0.
#   2. `git -C ../bikar show <ref>:<path>` is served from *this* repo's object
#      store, so a read spelled as bikar's tree is not one.
#
# The gap survived because the hook and the hand-run disagreed and only the
# hand-run was read: `make validate-use-cases` has no `GIT_DIR`, checks all 119
# pointers, and prints "all valid".
#
# So this test does not check any gate's verdict. It checks that the verdict does
# not depend on `GIT_DIR`, which is a property no individual gate can assert
# about itself.
#
# Usage: .githooks/tests/hook-env-git-dir.sh [repo-root]
set -eu

ROOT=${1:-$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)}

if [ ! -d "$ROOT/.claude" ]; then
  echo "hook-env: no .claude/ here — nothing to check (this is the gh-pages shape)"
  exit 0
fi

# What git would export. In a primary clone this is `<root>/.git`; in a linked
# worktree, that worktree's admin dir. Either reproduces the hazard.
GIT_DIR_VALUE=$(git -C "$ROOT" rev-parse --absolute-git-dir)

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# ---------------------------------------------------------------------------
# Positive control: does `GIT_DIR` still outrank `-C` on this git?
#
# Without this the whole file degrades into "two identical runs agree", which is
# true of a gate that checks nothing at all. If a future git stops honouring
# `GIT_DIR` over `-C`, the hazard is gone and so is this test's meaning — that
# should be reported, not silently passed.
# ---------------------------------------------------------------------------
git init --quiet "$TMP/other"
# --no-verify: this clone may carry a global hooksPath, and the control has no
# opinion about the caller's hooks — only about which repo git picks.
git -C "$TMP/other" -c user.email=t@e.invalid -c user.name=t \
  commit -q --no-verify --allow-empty -m "a commit that is not this repo's"

here=$(git -C "$ROOT" rev-parse HEAD)
there=$(git -C "$TMP/other" rev-parse HEAD)
hijacked=$(GIT_DIR="$GIT_DIR_VALUE" git -C "$TMP/other" rev-parse HEAD)

if [ "$hijacked" = "$there" ]; then
  echo "FAIL control — GIT_DIR no longer outranks -C on this git."
  echo "       The hazard this test guards cannot be reproduced, so every"
  echo "       assertion below would pass vacuously. Re-derive the test."
  exit 1
fi
[ "$hijacked" = "$here" ] || { echo "FAIL control — GIT_DIR redirected somewhere unexpected: $hijacked"; exit 1; }
echo "ok   control — GIT_DIR outranks -C, so the hazard is live and testable"

# ---------------------------------------------------------------------------
# Every gate that reads a git repository, run both ways.
# ---------------------------------------------------------------------------
fail=0
check() {
  name=$1
  shift
  clean_rc=0
  ( cd "$ROOT" && "$@" ) >"$TMP/clean.out" 2>&1 || clean_rc=$?
  hook_rc=0
  ( cd "$ROOT" && GIT_DIR="$GIT_DIR_VALUE" "$@" ) >"$TMP/hook.out" 2>&1 || hook_rc=$?

  if [ "$clean_rc" != "$hook_rc" ]; then
    echo "FAIL $name — exit $clean_rc by hand, $hook_rc under GIT_DIR"
    sed 's/^/       /' "$TMP/hook.out" | tail -12
    fail=1
    return
  fi
  if ! diff -q "$TMP/clean.out" "$TMP/hook.out" >/dev/null 2>&1; then
    echo "FAIL $name — same input, different report under GIT_DIR:"
    diff "$TMP/clean.out" "$TMP/hook.out" | sed 's/^/       /' | head -12
    fail=1
    return
  fi
  # The skip warnings are the specific shape the defect took: a sibling repo that
  # is checked out, reported as absent because the root resolved into .claude/.
  if grep -q "not checked out locally" "$TMP/hook.out" \
     && ! grep -q "not checked out locally" "$TMP/clean.out"; then
    echo "FAIL $name — GIT_DIR turned a checked-out sibling into a skipped one"
    fail=1
    return
  fi
  echo "ok   $name — same verdict with and without GIT_DIR"
}

check "validate.py"        python3 .claude/skills/maintain-use-cases/validate.py
check "doc_pointers.py"    python3 .claude/gates/doc_pointers.py
check "catalog_models.py"  python3 .claude/gates/catalog_models.py

[ "$fail" -eq 0 ] || { echo "hook-env: a gate's verdict depends on how it was launched"; exit 1; }
echo "hook-env: every repo-reading gate agrees with itself under git's hook environment"
