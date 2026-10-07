---
name: manage-approvals
description: Record Omar's yes or hold on a plate, and record a change to a plate's recipe, which resets the yes. Use when a plate recipe (docs/design/plates/<plate>.yaml) is edited, when the commit hook says "P9 the recipe changed since iteration N", when Omar ticks Approve or Hold on a plate page or says yes in chat, when a plate is sent, and for "is this plate approved", "what did Omar approve", "which version did he say yes to", "reset the approval". Owns approvals.yaml (each plate's recipe iterations) and plate_approve.py. Not for which plate to print next (prioritize-prints), the send itself (send-plate), or a plate's maturity (grade-plate).
---

# manage-approvals — a yes covers one version of a recipe

A plate's recipe changes in place: there is no new plate per version. Each version whose content
differs from the last is an **iteration**, numbered from 1 per plate. The iterations live in
[`approvals.yaml`](approvals.yaml) beside this file, and the plate page's frontmatter says which
one it is at (`iteration: 2`). Why this shape and not a new plate per change:
[D-097](../../../docs/working-model/decisions-log.md).

A yes is a row in the page's `## Approvals` table ([D-096](../../../docs/working-model/decisions-log.md)),
and its Covers cell names the iteration and the master commit that holds it:
`iteration 2 @ 1a2b3c4d5e`. So `git show 1a2b3c4d5e:docs/design/plates/<plate>.yaml` is exactly
what Omar said yes to, and `git diff 1a2b3c4d5e -- docs/design/plates/<plate>.yaml` is what changed
since. The commit is on master because a squash merge drops branch commits.

## When a recipe changes

1. Edit the recipe.
2. Run `python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --iterate`. It
   adds the next iteration to `approvals.yaml`, sets `iteration:` on the page, marks an open yes
   `reset <date>`, and puts an approved plate back to `waiting`.
   Add a timeline row saying what changed and why:
   `| <date> | changed (iteration N): <what, and whose ask> | <where it is written> |`, then a
   `sliced` row once it is sliced again.
3. Stage the recipe, the page and `approvals.yaml` by name, and ship the PR.
4. The plate needs a new yes from Omar. It cannot be given until the change is on master, since the
   yes names the master commit.

Hook 39 (the plates gate's rule P9) refuses a commit with a recipe change that is not recorded,
and names the command. It does not run the command itself: in a shared checkout a hook that edits
and stages files would sweep up another session's work.

**Not a change:** a comment, or the same keys in another order. The hash is taken over the
parsed recipe, so a reprint as-is keeps its iteration and its yes, and `--iterate` refuses.

**A production plate** does not change in place (D-095): `--iterate` refuses it once it has an
iteration, and P8 sends the change to a new plate (`python3 tools/plate_grade.py --derive`).

**Not covered:** a change to a bikar `.bkr` file the recipe names. Only the recipe file is hashed,
so a geometry change in bikar makes no iteration. Look at the render before asking for a yes.

## Recording a decision

- A yes: `… plate_approve.py <plate> --approved --by "Omar, tick on this page"` (or
  `'Omar, in chat: "<his words>"'`). It refuses when the recipe is not a recorded iteration, or
  that iteration is not on master yet.
- A hold: `… --held --by "Omar, tick: <his note>"`.
- Never write a yes Omar did not give (D-093).

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/plate_approve.py` | Writes the Approvals table and the iterations file; reads them back for a send | A recipe changed (`--iterate`); a tick or a chat yes (`--approved`, `--held`); promotion (`--standing`); a send (`--sent`); "may it go out" (`--status`) | `python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --iterate` |
| `scripts/iterations.py` | Reads and writes `approvals.yaml`, hashes a recipe, and asks git what a commit holds and whether it is on master | Imported by the plates gate, `plate_approve.py` and `tools/plate_grade.py`; not run by hand | — |

Both self-test: `python3 .claude/skills/manage-approvals/scripts/plate_approve.py --self-test`,
and the plates gate's `python3 .claude/gates/plates_gate.py --self-test` covers P9.
