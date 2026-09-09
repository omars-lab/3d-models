# The base-face honesty fix had two layers, and the gate branches on family

*Issue slug: `base-face-honesty-scaffold-pivot`. Written 2026-09-09, during the
#49 / D-052 cascade. Companion to
[`data-orb-base-face-honesty-cascade.md`](../data-orb-base-face-honesty-cascade.md).*

## What the defect was

`data-orb-base-face` is supposed to name a **true face of a base polyhedron**. Two orb
families exist:

- **Lifted / inscribed** (e.g. StarOrb): a real base solid, `base.faces > 0`. Its
  pattern is copied onto each face, so a scaffold outline and each drawn cell honestly
  name a base face.
- **Round-pattern / wheelfield** (e.g. DonutHexOrb, DonutHexWeld): **no base solid at
  all**, `base.faces == 0`. Wheels seat on disc-sites of a faceless sphere; a wheel
  touches three faces and names none. Its drawn `--format views` cells already carried
  `data-orb-unit`.

The breakdown page's scaffold underlay, however, stamped `data-orb-base-face` on **every**
orb — so a wheelfield breakdown said `base-face` on the same picture whose drawn cells
said `unit`. One name, two meanings, on one orb.

## What was first planned (and dropped)

The prepared plan (cascade doc §4, earlier form) took the simpler-looking route: make the
T9 gate check `data-orb-base-face` **universally**, reasoning that "`data-orb-base-face`
is always a true face, wheelfield cells carry none, so the subset check is trivially
satisfied." That routes *around* the defect instead of deleting it: it leaves the
wheelfield scaffold dishonestly stamping `base-face`, and makes the gate depend on that
dishonesty (a vacuous "carries none" pass). CLAUDE.md's rule — *a migration never buys a
fork; two code paths that disagree, or one name with two meanings, **are** the defect* —
says fix the producer, not the reader. So the scaffold was made honest instead.

## What the evidence showed — the fix has two layers, not one

Making the scaffold honest was **not** a single conditional. The renderer has two stamp
sites, and the breakdown base solid flows through the *second* one:

1. **The main polygon loop** (`buildViewFaceAttrs`) already read `scene.baseIndexKind`,
   so the drawn views were already correct.
2. **The scaffold underlay** (`scaffoldElements`) stamped `data-orb-base-face`
   **unconditionally** — and the breakdown's bare base solid renders as *this* underlay,
   not as drawn polygons.
3. Behind it, the CLI's `baseSolidScene` hardcoded `baseIndexKind: 'face'`, so even after
   `scaffoldElements` learned to branch, it was handed `'face'` for every family.

So the honest fix (bikar
[#170](https://github.com/NaqshCoffee/bikar/pull/170), merged `c2fa085`) had to flow
through **both** the plan and the render path: a new `OrbViewPlan.baseIndexKind` derived
per family in the CLI (`'face'` for orb3d, `'unit'` for sphere3d), `baseSolidScene` reading
that plan instead of a constant, and `scaffoldElements` branching on
`scene.baseIndexKind`. Fixing only one layer left the drawn cells saying `unit` while the
scaffold beneath them still said `base-face` — caught by reading the scaffold test, which
had asked for `base-face` without passing the kind.

## What replaced the universal gate

`.claude/gates/timelapse_gate.py`'s T9 now **branches on family**, and the manifest's own
`base` block is the discriminator — measured, not assumed: `base.faces == 0` ⟺ a faceless
wheelfield.

- **Lifted** (`base.faces > 0`): the base-face presence / range / subset check, against
  `data-orb-base-face`, unchanged.
- **Wheelfield** (`base.faces == 0`): the same three questions asked of `data-orb-unit`,
  **plus** any `data-orb-base-face` anywhere on the frame is itself a finding — a claim
  about a facet the orb does not have.

The `--self-test` grew a wheelfield fixture (`_make_wheelfield`, asserted clean) and three
by-design mutators that must each fire: a frame that claims a base face
(`_claim_a_face_on_a_wheelfield`), a scaffold that draws sites but stamps no units
(`_blank_the_wheelfield_units`), and a wheel placed on a site the scaffold never outlines
(`_orphan_a_wheelfield_unit`) — the round-pattern twin of the inscribed `_orphan_a_cell`.

## Verified

`make orbs` re-record against `c2fa085`: DonutHexOrb's breakdown carries `data-orb-unit`
and **zero** `data-orb-base-face` across all frames; StarOrb's base frame keeps its 10
`data-orb-base-face` scaffold labels. The gate passes on all 16 breakdowns and every
`--self-test` case fires. (`build/` is gitignored; the renders ship via `make deploy`, so
the check is the gate on the fresh build, not a git diff.)
