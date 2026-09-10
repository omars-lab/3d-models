# Kickoff — make the orb breakdown pages teach construction (task #81)

> **SHIPPED — do not paste this into a new session to build.** The construction the
> kickoff below hands off is merged and deployed. The teaching fixes it calls for
> (shaded depth-cued spheres, the flat pattern shown, the spin reading as a turning
> ball) landed and were verified on the live gallery across the cell, cell+strand and
> strand-only families. Merges: the restyle + five-beat arc, the flat→sphere wrap morph
> (bikar #149, 3d-models #148, gate T8), round-pattern orb breakdowns (bikar #158,
> 3d-models #159, index 16), and base-face honesty (bikar #170 `c2fa085`, 3d-models #170
> `19e885d`, gate T9, D-052). This file's `task #81` is a fresh-snapshot id, unrelated to
> `done.md`'s #81. Kept as the historical brief — see plan.md §3 for the shipped record.

Paste the block below into a **clean new session** (fresh, not a fork — the cascade
context that produced this doc is irrelevant to the build, and this is a multi-day
effort across two repos). It frames the goal and hands off the non-obvious
constraints, then points at the detailed plan as the source of truth. Kept lean on
purpose: a new session auto-loads `CLAUDE.md` and `MEMORY.md`, so only what those
don't make immediately actionable is spelled out here.

---

**Goal:** Make the orb breakdown pages actually *teach construction* — a newcomer
should be able to watch a flat overhead drawing become a 3D orb. The page shipped
(bikar #110, 3d-models #84) but fails this core job today: every frame is a flat
gray blob, the flat pattern is never shown, and the spin doesn't read as a turning
sphere.

**Source of truth — read this first, in full:** `.claude/plans/sunny-booping-crescent.md`
in the 3d-models repo. It has the measured audit (A1–A7, frames rendered to PNG and
inspected), the user-locked scope decisions, the full renderer/geometry/gate design
with verified `file:line` anchors, the execution order, and the verification plan.
Treat it as the spec. This is tracked as **task #81**.

**Shape of the work — two repos, in order, never stacked:**

1. **bikar PR 1** (the producer — kernel `meanDot` + `baseSolidCells`, renderer
   `OrbViewStyle`/highlight behind a **byte-stability snapshot test written first**,
   CLI frames + transitions + ribbon turntable, `breakdown-main.ts` page, e2e
   fixtures). bikar **has CI** → poll to green, **never `--auto` or `--admin`**
   (`gh` `--auto` merges immediately on NaqshCoffee repos). Read main's last CI run
   before starting — it has merged past red before.
2. **3d-models PR 2** (after PR 1 merges; bump `build/bikar-ref.txt`) —
   `orb_previews.py` restyle, `make orbs` regen, the `timelapse_gate.py` (§9,
   task #17), doc amendments, close tasks #14/#17/#35. 3d-models has **no CI** —
   `make validate` is the only run; a billing-blocked run is not a red build.

**Hard constraints (won't be obvious fast enough):**

- **The qiyas byte-stability shield is load-bearing.** Scope decision 1: style every
  *human* surface, but the qiyas-scored SVG/PNG/gt.json instrument set stays
  byte-identical (`style` absent ⇒ character-identical output, pinned by the snapshot
  test). Do not restyle the `build/orb-views` top level.
- **Generality is a hard requirement** (scope decision 2): every mechanism is
  parameterised by what the manifest/scene declares — orb family, stage axis, view
  kind — **never per-orb code**. Family is *measured* from the frame-kind set, not
  assumed.
- **Node:** prefix every git/npm/tsx/vitest with
  `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`.
- **Shared checkout:** multiple sessions run in this tree. `git branch --show-current`
  before every commit; stage only files you changed; never `git add -A` /
  `git restore .`; take your own `git worktree` per session. Every change goes
  branch→PR→merge; delete merged branches.

**Already done — don't redo:** the T9 outline↔solid gate (#49), the D-052
base-face-honesty cascade across all four repos, and the two mirror gates (schema
hook 41, prose hook 42). #81 is "the full plan *beyond* the T9 gate."

Start by reading the plan file end to end, then confirm the bikar PR 1 breakdown
against the current bikar `file:line` anchors before writing code.
