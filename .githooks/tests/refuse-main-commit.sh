#!/bin/sh
# The branch guard (`pre-commit.d/00-branch`) must refuse a commit on the default
# branch and let every other commit through — and it must do so when *git* runs
# it through the dispatcher, not only when a person runs the file by hand. The
# by-design failure is the load-bearing case here (CLAUDE.md): a guard that lets
# the `master` commit land is exactly the defect it exists to end, and a guard
# that refuses `gh-pages` breaks `make deploy`.
#
# Six scratch repos, each with only the dispatcher and the guard copied in, so
# the verdict is the guard's alone — the sibling hooks each have their own test.
#
# Usage: .githooks/tests/refuse-main-commit.sh [hooks-dir]
set -eu

HOOKS_DIR=${1:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}
SCRATCH=$(mktemp -d)
trap 'rm -rf "$SCRATCH"' EXIT

# scratch <name> <initial-branch>: a repo with the guard wired the way this repo
# wires it (core.hooksPath -> .githooks), one staged file, on the given branch.
scratch() {
  dir="$SCRATCH/$1"
  mkdir -p "$dir/.githooks/pre-commit.d"
  cp "$HOOKS_DIR/pre-commit" "$dir/.githooks/pre-commit"
  cp "$HOOKS_DIR/pre-commit.d/00-branch" "$dir/.githooks/pre-commit.d/00-branch"
  git init --quiet --initial-branch="$2" "$dir"
  git -C "$dir" config core.hooksPath .githooks
  git -C "$dir" config user.email hooks@test
  git -C "$dir" config user.name hooks
  printf 'probe\n' > "$dir/probe.txt"
  git -C "$dir" add probe.txt
  printf '%s' "$dir"
}

fail=0

# expect_refused <name> <branch> [env]: the commit must fail AND the refusal must
# be the guard's, not some other error in the scratch setup.
expect_refused() {
  dir=$(scratch "$1" "$2")
  if git -C "$dir" commit -q -m probe 2>"$dir/err"; then
    echo "FAIL a commit on '$2' was ACCEPTED — the guard did not run or did not refuse"
    fail=1
  elif ! grep -q "refusing a direct commit on '$2'" "$dir/err"; then
    echo "FAIL a commit on '$2' failed, but not from the guard:"
    sed 's/^/       /' "$dir/err"
    fail=1
  else
    echo "ok   a commit on '$2' is refused, by the guard, through git"
  fi
}

# expect_accepted <name> <branch> <label>: the commit must land.
expect_accepted() {
  dir=$(scratch "$1" "$2")
  if git -C "$dir" commit -q -m probe 2>"$dir/err"; then
    echo "ok   $3"
  else
    echo "FAIL $3 — the commit was refused:"
    sed 's/^/       /' "$dir/err"
    fail=1
  fi
}

expect_refused master master
expect_refused main main
expect_accepted topic feat/topic "a commit on a topic branch lands"
expect_accepted pages gh-pages "a commit on gh-pages lands (make deploy commits there)"

# The named override lands the commit, on the default branch.
dir=$(scratch override master)
if BRANCH_OK=1 git -C "$dir" commit -q -m probe 2>"$dir/err"; then
  echo "ok   BRANCH_OK=1 lands a commit on master (the named override)"
else
  echo "FAIL BRANCH_OK=1 did not override the guard:"
  sed 's/^/       /' "$dir/err"
  fail=1
fi

# Detached HEAD: no branch, nothing to guard. Built from the accepted topic repo
# by detaching at its one commit and staging a second file.
dir="$SCRATCH/topic"
git -C "$dir" checkout -q --detach
printf 'again\n' > "$dir/again.txt"
git -C "$dir" add again.txt
if git -C "$dir" commit -q -m detached 2>"$dir/err"; then
  echo "ok   a commit on a detached HEAD lands (worktree fixtures build this way)"
else
  echo "FAIL a detached-HEAD commit was refused:"
  sed 's/^/       /' "$dir/err"
  fail=1
fi

[ "$fail" -eq 0 ] || { echo "hooks: the branch guard is wrong about a case it exists for"; exit 1; }
echo "hooks: the branch guard refuses master and main through git, and nothing else"
