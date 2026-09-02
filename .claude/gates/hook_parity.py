#!/usr/bin/env python3
"""`make validate` runs every pre-commit hook wholesale — and proves it does.

This repo has no CI. Its seven `.githooks/pre-commit.d/` hooks *are* the gate
set, and each of them checks only what a given commit stages. There was no way
to ask "would all of this pass over the whole tree right now?" without knowing
the seven target names by heart, which is the same as there being no way.

WHY THIS IS NOT JUST A `validate:` CHAIN IN THE MAKEFILE. A hand-listed chain
asserts a relationship — "these targets are the hooks" — that nothing checks,
and it drifts the first time a hook is added. That is not hypothetical here:
measured 2026-08-17, before this file existed, the two sets were **not
subset-related in either direction**. `10-gitleaks` had no wholesale target at
all, while `validate-hooks` and `validate-coupons` were targets with no hook.
A chain written that day would have been born wrong and printed success.

The sibling repo hit the identical failure the same week: qiyas' `make local.ci`
advertised "Full CI pipeline natively" while covering 3 of the 8 gating steps in
its `lint-test` job. And the repo has paid for this shape once before, in a
different costume — on 2026-08-02, 23 of 44 use-case pointers had drifted while
every run printed "all valid".

So the mapping is *declared by the hook itself*:

    # wholesale: make validate-docs
    # wholesale-requires: gitleaks        (optional)

One line, in the file it describes, which cannot be edited from a distance. A
hook with no declaration is a hard failure, and an entry naming a hook that no
longer exists cannot happen because the hooks are the enumeration.

`--check`  every hook declares its wholesale form. Instant, no side effects.
`--run`    run each declaration in hook order, then the extras below.
`--self-test`  the by-design failures fire (see `_self_test`).

WHAT `--run` PROMISES. A hook whose `wholesale-requires:` binary is absent is
reported NOT VERIFIED and named in the summary line, never skipped in silence:
a runner that omits what it cannot do is worse than no runner, because green
then means "green except the parts I skipped". It still exits 0 — a gate that
cries wolf gets switched off, which is worse than having no gate — so
`--strict` exists for when "I did not check" must not pass.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HOOK_DIR = ROOT / ".githooks" / "pre-commit.d"

_WHOLESALE = re.compile(r"^#\s*wholesale:\s*(.+?)\s*$", re.MULTILINE)
_REQUIRES = re.compile(r"^#\s*wholesale-requires:\s*(\S+)\s*$", re.MULTILINE)

# Targets with no hook behind them. Listed here rather than only in the
# Makefile so the answer to "why does `make validate` do more than the hooks?"
# lives beside the answer to "why does it do less?" — the question that made
# this file necessary.
EXTRA = [
    (
        "make validate-hooks",
        "Regression test for the hook *environment* (linked worktree without "
        ".claude/, GIT_DIR outranking -C). By construction it cannot be one of "
        "the hooks it tests.",
    ),
    (
        "make validate-coupons",
        "Checks the prototype coupon catalog. Not wired to a hook: coupons are "
        "edited rarely and the check shells out to bikar, which is a sibling "
        "checkout a commit here cannot assume is present.",
    ),
    (
        "make validate-status",
        "Self-tests build/status_manifest.py, the generator behind status.html. "
        "Not wired to a hook: its three inputs (build/bikar-ref.txt, the "
        "use-case map's as_of pins, the gh-pages tip) are files other gates "
        "already own, so a commit here has no staged trigger to hang one on.",
    ),
]


class Hook:
    """One `.githooks/pre-commit.d/` entry and the wholesale form it declares."""

    def __init__(self, path: Path, command: str, requires: str | None) -> None:
        self.path = path
        self.name = path.name
        self.command = command
        self.requires = requires


def load_hooks(hook_dir: Path = HOOK_DIR) -> tuple[list[Hook], list[str]]:
    """Read every executable hook. Returns (hooks, problems), in lexical order.

    Lexical order because that is the order the dispatcher runs them in, and a
    wholesale run that reordered them would be answering a different question
    than the one the commit path asks.
    """
    hooks: list[Hook] = []
    problems: list[str] = []
    if not hook_dir.is_dir():
        return hooks, [f"no hook directory at {hook_dir}"]

    for path in sorted(hook_dir.iterdir()):
        if not path.is_file() or not path.stat().st_mode & 0o111:
            continue
        text = path.read_text(encoding="utf-8")
        found = _WHOLESALE.findall(text)
        if not found:
            problems.append(
                f"{path.name}: no `# wholesale:` declaration.\n"
                f"    Add one line naming how to run this hook's check over the whole\n"
                f"    tree, e.g. `# wholesale: make validate-docs`. If the hook has no\n"
                f"    wholesale form, say so: `# wholesale: none — <reason>`."
            )
            continue
        if len(found) > 1:
            problems.append(f"{path.name}: {len(found)} `# wholesale:` declarations, expected 1")
            continue
        command = found[0]
        if command.startswith("none"):
            if not command[4:].strip(" —-:"):
                problems.append(f"{path.name}: `# wholesale: none` needs a reason after it")
            continue
        req = _REQUIRES.findall(text)
        hooks.append(Hook(path, command, req[0] if req else None))
    return hooks, problems


def check(hook_dir: Path = HOOK_DIR, quiet: bool = False) -> int:
    hooks, problems = load_hooks(hook_dir)
    if problems:
        if not quiet:
            print("hook-parity --check FAILED:\n", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
        return 1
    if not quiet:
        gated = sum(1 for h in hooks if h.requires)
        needs = "needs" if gated == 1 else "need"
        print(
            f"hook-parity: OK — {len(hooks)} pre-commit hooks, all declaring a "
            f"wholesale form ({gated} of them {needs} a tool on PATH), plus "
            f"{len(EXTRA)} check(s) with no hook behind them."
        )
    return 0


def run(strict: bool) -> int:
    rc = check(quiet=True)
    if rc:
        return check()  # re-run loudly, for the message

    hooks, _ = load_hooks()
    passed: list[str] = []
    failed: list[tuple[str, int]] = []
    unverified: list[tuple[str, str]] = []

    for hook in hooks:
        if hook.requires and not shutil.which(hook.requires):
            unverified.append((hook.name, f"`{hook.requires}` is not on PATH"))
            print(f"[NOT VERIFIED] {hook.name}  ({hook.requires} not installed)")
            continue
        print(f"\n==> {hook.name}\n    $ {hook.command}")
        started = time.monotonic()
        step = subprocess.run(hook.command, shell=True, cwd=ROOT)  # noqa: S602
        took = time.monotonic() - started
        if step.returncode == 0:
            passed.append(hook.name)
            print(f"    ok ({took:.1f}s)")
        else:
            failed.append((hook.name, step.returncode))
            print(f"    FAILED rc={step.returncode} ({took:.1f}s)")

    for command, _reason in EXTRA:
        print(f"\n==> [no hook behind this one] {command}")
        step = subprocess.run(command, shell=True, cwd=ROOT)  # noqa: S602
        if step.returncode == 0:
            passed.append(command)
            print("    ok")
        else:
            failed.append((command, step.returncode))
            print(f"    FAILED rc={step.returncode}")

    print("\n" + "=" * 72)
    if unverified:
        print("NOT VERIFIED — these gates did not run on this machine:")
        for name, why in unverified:
            print(f"  - {name}: {why}")
        print(
            "\n  These are real gates, and this repo has no CI to catch them later.\n"
            "  A green summary below means green on what ran."
        )
        print("=" * 72)
    for name, code in failed:
        print(f"FAILED: {name} (rc={code})")

    # The summary line is the whole contract: it can never read like a clean
    # bill of health when something went unrun.
    if failed:
        verdict = f"{len(failed)} FAILED"
    elif unverified:
        verdict = f"{len(passed)} verified, {len(unverified)} NOT VERIFIED"
    else:
        verdict = f"all {len(passed)} verified"
    print(f"hook-parity: {verdict}")

    if failed:
        return 1
    if unverified and strict:
        print("hook-parity: --strict — an unverified gate is a failure here.")
        return 2
    return 0


def _self_test() -> int:
    """Each by-design failure must fire. A gate that only sees green is untested.

    The load-bearing case is the first one: a hook added without a declaration
    is exactly how `make validate` would come to claim more coverage than it
    has, which is the whole reason this file exists.
    """
    cases: list[tuple[str, str, bool]] = [
        (
            "a hook with no `# wholesale:` line",
            "#!/bin/sh\necho hi\n",
            True,
        ),
        (
            "a hook declaring `none` with no reason",
            "#!/bin/sh\n# wholesale: none\n",
            True,
        ),
        (
            "a hook declaring `none` with a reason",
            "#!/bin/sh\n# wholesale: none — nothing to run over the whole tree\n",
            False,
        ),
        (
            "two `# wholesale:` lines in one hook",
            "#!/bin/sh\n# wholesale: make a\n# wholesale: make b\n",
            True,
        ),
        (
            "a well-formed hook",
            "#!/bin/sh\n# wholesale: make validate-docs\n",
            False,
        ),
    ]
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, body, must_fail in cases:
            case_dir = Path(tmp) / re.sub(r"\W+", "-", label)
            case_dir.mkdir()
            hook = case_dir / "50-fixture"
            hook.write_text(body, encoding="utf-8")
            hook.chmod(0o755)
            fired = check(case_dir, quiet=True) != 0
            ok = fired == must_fail
            print(f"  {'ok  ' if ok else 'FAIL'}  {label}: {'fires' if fired else 'passes'}")
            if not ok:
                failures += 1

        # A non-executable file is not a hook — the dispatcher skips it, so the
        # check must too, or a stray README in the directory blocks every commit.
        case_dir = Path(tmp) / "non-executable"
        case_dir.mkdir()
        (case_dir / "README.md").write_text("not a hook\n", encoding="utf-8")
        fired = check(case_dir, quiet=True) != 0
        print(f"  {'ok  ' if not fired else 'FAIL'}  a non-executable file is ignored")
        if fired:
            failures += 1

    if failures:
        print(f"hook-parity --self-test: {failures} case(s) behaved wrongly", file=sys.stderr)
        return 1
    print("hook-parity --self-test: all cases behaved as designed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="prove every hook declares one")
    group.add_argument("--run", action="store_true", help="run every wholesale form")
    group.add_argument("--self-test", action="store_true", help="the by-design failures fire")
    parser.add_argument(
        "--strict", action="store_true", help="with --run: exit 2 if a gate could not be verified"
    )
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    if args.run:
        return run(strict=args.strict)
    return check()


if __name__ == "__main__":
    sys.exit(main())
