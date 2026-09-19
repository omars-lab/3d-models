#!/usr/bin/env sh
# bambu_flags_gate.sh — the checked-in flag reference must match the CLI that generates it.
#
# tools/bambu/FLAGS.md is emitted by `bambu dump-flags` from the live commander tree, so it can never
# be wrong about a flag the way hand-written prose (the README table, the bambu skill) drifts the
# moment a `.option()` is added. This gate re-runs the generator and diffs: add or change a flag,
# regenerate (`make bambu-flags`) or the commit is blocked with the exact diff. Same shape as the
# count gate — the tool prints the reference, the gate diffs it — so there is no second copy to keep
# in sync by hand.
#
# Usage:
#   bambu_flags_gate.sh              # regenerate and diff against the checked-in FLAGS.md (make/hook)
#   bambu_flags_gate.sh --self-test  # the by-design failure (a mutated reference) must be caught
#
# Exit 0 clean / 1 drift or a generator failure / 2 misuse or missing deps.
# The generator needs the pinned Node toolchain (tsx); hook 45 declares `wholesale-requires: node` so
# a machine without Node reads NOT VERIFIED rather than a false pass.

set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "bambu-flags: not inside a git worktree" >&2
  exit 2
}
BAMBU="$ROOT/tools/bambu"
FLAGS="$BAMBU/FLAGS.md"
BIN="$BAMBU/bin/bambu"

# A commit that does not touch the CLI must not be forced to have the bambu deps installed. If the
# toolchain is not runnable, say so and stop honestly — never pass silently.
if [ ! -x "$BIN" ]; then
  echo "bambu-flags: no CLI at $BIN — nothing to check" >&2
  exit 2
fi
if [ ! -d "$BAMBU/node_modules" ]; then
  echo "bambu-flags: tools/bambu deps not installed (run: cd tools/bambu && npm install)" >&2
  exit 2
fi

# Regenerate to a temp so the real file is never touched by the check itself.
gen="$(mktemp)" || exit 2
trap 'rm -f "$gen"' EXIT
if ! "$BIN" dump-flags >"$gen" 2>/dev/null; then
  echo "bambu-flags: the generator (\`bambu dump-flags\`) failed to run" >&2
  exit 1
fi

# The one comparison, reused by the real run and the self-test: current generated output vs a
# reference file. Prints the unified diff and the fix on drift.
compare() {
  ref="$1"
  if [ ! -f "$ref" ]; then
    echo "bambu-flags: no reference at $ref — generate it with \`make bambu-flags\`" >&2
    return 1
  fi
  if diff -u "$ref" "$gen" >/tmp/bambu-flags-diff.$$ 2>/dev/null; then
    rm -f /tmp/bambu-flags-diff.$$
    return 0
  fi
  echo "bambu-flags: FLAGS.md is out of date with the CLI — a flag changed but the reference did not." >&2
  echo "  Fix: make bambu-flags   (regenerates tools/bambu/FLAGS.md, then stage it)" >&2
  echo "  Drift (reference → generated):" >&2
  sed 's/^/    /' /tmp/bambu-flags-diff.$$ >&2
  rm -f /tmp/bambu-flags-diff.$$
  return 1
}

if [ "${1:-}" = "--self-test" ]; then
  # By-design failure: a reference with one flag description mangled MUST be reported as drift. A gate
  # that cannot catch a deliberate break is not testing anything (repo robustness tenet).
  bad="$(mktemp)" || exit 2
  # Take the real generated output and drift it by one line, so the fixture no longer matches what
  # the CLI produces. A trailing marker line is portable across seds and is exactly the kind of stale
  # edit the gate must catch (the reference says something the generator does not).
  cat "$gen" >"$bad"
  printf '| `--drift-marker` | self-test drift, not a real flag |\n' >>"$bad"
  if [ ! -s "$bad" ] || cmp -s "$bad" "$gen"; then
    echo "bambu-flags: self-test could not construct a drifted fixture" >&2
    rm -f "$bad"
    exit 1
  fi
  if compare "$bad" >/dev/null 2>&1; then
    echo "bambu-flags: SELF-TEST FAILED — a mutated reference was NOT caught as drift" >&2
    rm -f "$bad"
    exit 1
  fi
  rm -f "$bad"
  echo "bambu-flags: self-test OK — drift is caught"
  exit 0
fi

if compare "$FLAGS"; then
  echo "bambu-flags: OK — FLAGS.md matches the CLI"
  exit 0
fi
exit 1
