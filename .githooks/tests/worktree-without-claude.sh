#!/bin/sh
# The pre-commit hooks must survive a worktree that carries `.githooks` but not
# `.claude`.
#
# `core.hooksPath` is a repo-wide setting, so every hook in `pre-commit.d/` runs
# in *every* worktree of this clone — including the `.gh-pages` one `make deploy`
# creates. `gh-pages` is a deliberately diverged branch (see CLAUDE.md) whose
# tree is built site output: it tracks `.githooks/` and does not track `.claude/`.
# Before this test existed, `20-use-cases` and `30-docs-gate` ran `python3` on a
# path that did not exist there and `make deploy` died on the gh-pages commit
# with `[Errno 2] No such file or directory`.
#
# Usage: .githooks/tests/worktree-without-claude.sh [hooks-dir]
# The default hooks-dir is the tracked one next to this script, so pointing it at
# a checkout of the old hooks reproduces the failure.
set -eu

HOOKS_DIR=${1:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}
FIXTURE=$(mktemp -d)
trap 'rm -rf "$FIXTURE"' EXIT

# A worktree shaped like gh-pages: hooks present, .claude absent, one staged
# file that is plainly site output rather than a design doc or a pointer file.
mkdir -p "$FIXTURE/.githooks"
cp -R "$HOOKS_DIR/." "$FIXTURE/.githooks/"
# On the branch it is shaped like: 00-branch refuses master and main, and
# init.defaultBranch is main on at least one machine this runs on.
git init --quiet --initial-branch=gh-pages "$FIXTURE"
git -C "$FIXTURE" config core.hooksPath .githooks
git -C "$FIXTURE" config user.email hooks-test@example.invalid
git -C "$FIXTURE" config user.name "hooks test"
printf '<!doctype html><title>built</title>\n' > "$FIXTURE/index.html"
git -C "$FIXTURE" add -A

fail=0
for hook in "$FIXTURE"/.githooks/pre-commit.d/*; do
  name=$(basename "$hook")
  # 10-gitleaks reads no `.claude` path; it is skipped because asserting on it
  # would only assert that gitleaks is installed on this machine.
  [ "$name" = "10-gitleaks" ] && continue
  status=0
  (cd "$FIXTURE" && "$hook" >/dev/null 2>"$FIXTURE/err") || status=$?
  if [ "$status" -eq 0 ]; then
    echo "ok   $name — skips cleanly with no .claude/ present"
  else
    echo "FAIL $name — exited $status in a worktree with no .claude/:"
    sed 's/^/       /' "$FIXTURE/err"
    fail=1
  fi
done

[ "$fail" -eq 0 ] || { echo "hooks: a pre-commit hook cannot run on gh-pages"; exit 1; }
echo "hooks: every .claude-dependent pre-commit hook survives a worktree without .claude/"
