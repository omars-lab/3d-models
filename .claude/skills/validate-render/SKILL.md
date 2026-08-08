---
name: validate-render
description: Turn an LDraw model (.mpd/.ldr) into a set of camera-angle PNGs and validate it against a committed expectation. Use when checking that a brick/assembly export still renders and reads back correctly, when regenerating a model's thumbnails, or before putting a render in a PR or the gallery — the tool renders several angles because one view of stacked bricks cannot show how many there are, and gates them by exact counts, a visible-colour set, and tolerant golden pixels.
---

# Validate a render — a `.mpd` to a *set* of PNGs, gated three ways

The tool is bikar's `bikar:scripts/render-ldraw-thumbnails.ts` (D-028,
[`docs/decisions-log.md`](../../../docs/decisions-log.md); spec in
[`docs/lego-lab-design.md`](../../../docs/lego-lab-design.md) §15). This skill is the
procedure for running it and reading its result — the CLI, the gate logic
(`bikar:scripts/thumbnail-gate.ts`), the witness (`bikar:scripts/thumbnail-gate.test.mjs`)
and the fixtures all live in bikar. It renders the *same* scene the studio read-back panel
shows (`bikar:packages/lab/src/ldraw-scene.ts` on `bikar:packages/lab/thumbnail.html`), so a
thumbnail is the same brick §14.4 reads back, not a second renderer that could disagree.

## The one idea this skill exists to enforce

[`docs/research/ldraw-cli-viewers.md`](../../../docs/research/ldraw-cli-viewers.md) §10.5:
**on a file with no edge lines, a render is evidence of shape and not of structure.** A
three-quarter view of two stacked 2×4 bricks is pixel-for-pixel a single six-plate block —
the seam is never drawn. So the honest output of a composition is a *set* of angles beside the
numbers, and the number is the real gate. Never certify "the model is right" from one picture.

## Prerequisites (once)

- Node via the pinned prefix: `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`
  before any `npm`/`tsx` — the system Node fails in ways that look like code bugs.
- The render backend is **Playwright's full Chromium**, not the default headless shell:
  §10.3 measured the shell failing to create a WebGL context on this machine class, while full
  Chromium reaches the GPU through ANGLE/Metal. Install it once in the bikar checkout:
  `npx playwright install chromium`.
- Run from a bikar checkout (`~/Workspace/git/bikar`), where the `thumbnail` npm script lives.

## Workflows

**Render (a fresh look).** `npm run thumbnail -- <model.mpd>` writes one PNG per default angle
(`iso`, `front`, `below`) beside the model, plus `<name>.counts.json` — the camera-independent
read-back. Pick angles with `--angles iso,front,below,top,back` when the defaults leave a model
ambiguous; each is there for a reason (§15.1: `iso` reads proportions, `front` puts the seam on
screen, `below` shows the underside tubes). This is a look, not a judgement — it asserts nothing.

**Validate (`--check`).** `npm run thumbnail -- <model.mpd> --check` holds the render to a
committed expectation, and the two halves are **deliberately unequal**:

- **Counts are the hard gate.** The whole read-back — placements, meshes, triangles, resolved
  part hashes, winding certification, edge pairing — is deep-compared against
  `<name>.expected.json` and fails on **any** drift. This is where §10.5's lesson bites: the
  thing a picture cannot establish (how many parts, placed where) is exactly what the counts pin,
  exactly. An aggregate cannot discharge this — a single changed field, a CCW→CW winding flip, or
  a changed part hash must fail, and the witness freezes that.
- **The colour set is the middle gate — and it ports.** Every foreground pixel is classified to the
  nearest colour in *the model's own palette plus the background* (not exact pixels, not the whole
  LDConfig set), each colour's best coverage is accumulated across the angle set, and the colours
  clearing a small area floor (`--colour-min-area`, default 0.01) are compared as a *set* against a
  committed `visibleColours`. Because it is nearest-of-palette, a shaded blue still reads blue, so
  this gate — unlike the pixels — **catches the D-026 grey blob on a backend whose goldens were never
  baked** (§16). The expectation is the *visible* set, deliberately a subset of the resolved colours:
  a colour can be wholly occluded in every angle (Brick-Stack's lower-brick yellow studs under the
  top brick) with nothing wrong, so `visibleColours` is baked by `--update-goldens`, never derived
  from the read-back. `colours: PASS (3 visible, set matches)` is the good line; a differing set names
  what is missing or unexpected.
- **Golden pixels are the soft gate.** A render is GPU/driver dependent, so the differing-pixel
  fraction is compared against a small `--tolerance` (default 0.02), not against zero. A one-pixel
  wobble passes; a materially different frame fails. A size mismatch is a hard fail (not a
  swallowable ratio).

Exit 0 means all three passed; nonzero prints which gate fired.

**The load-bearing case — read it, don't skip it.** If `--check` reports `counts` failing while
every angle's pixels still pass, that is the tool working, not a flake: an emitter change added or
dropped a part in a way no camera angle shows. Trust the counts. The inverse — pixels fail,
counts pass — is usually the backend, not the model (see K10 below).

**Update goldens (`--update-goldens`).** Only after a render legitimately changed (an intended
emitter change, verified by reading the new counts), and **only on the same backend that will
validate against them** (see K10). Writes `<name>.expected.json` (including the baked
`visibleColours` — the colour gate's expectation is *baked from a trusted backend*, exactly like
the golden PNGs, never auto-derived from the render, or occlusion would false-fail it) + the angle
PNGs as the new goldens. Commit them with the change that caused them, and update the model's
`.notes.md` in the same commit if the visible palette changed — the catalog gate (below) will
otherwise block the commit.

## The notes and the catalog they belong to

Each model carries a committed `<name>.notes.md` beside its `.mpd` and `.expected.json` — a plain
colour legend (every resolved hex named, with where it sits and whether it is visible or occluded)
and a per-angle description of what the picture should show. The notes are the human-readable half
of the expectation: `visibleColours` says *which* colours a correct render shows, the notes say
*why*, and the occlusion note is what stops the next person from "fixing" a deliberately-absent
colour. Brick-Stack's notes name all four resolved hexes and explain that the lower brick's yellow
studs are occluded under the top brick in every angle, so `visibleColours` is three, not four.

**The catalog is gated, the render is not.** `bikar:scripts/thumbnail-catalog.test.mjs` is the
GPU-free half — it reads the fixtures directory and holds it to three structural invariants that
need no pixels: every `.mpd` has both an `.expected.json` and a `.notes.md` (no uncatalogued
model, no orphaned metadata), every resolved colour is named in the notes (the same catalog↔model
coherence the W-F1 gate enforces), and the catalog is non-empty (a vacuous pass is not a pass).
Because it never renders, it runs in bikar CI (`test:scripts`) **and** in the pre-commit hook —
the only half of `--check` that graduates to a gate, because it is the only half with no GPU and
no backend fragility in the path. Adding a model without its notes, or growing a model's palette
without naming the new colour, fails the commit.

## K10 — the condition under which the goldens are valid

**The committed golden PNGs are valid only for the backend that produced them** — this machine's
Chromium-on-darwin through ANGLE/Metal (§10.6: nothing was run headless over SSH, in a container,
or in CI). A different GPU, driver, or OS may shift enough pixels to exceed the tolerance with
*nothing wrong*. The response is `--update-goldens` on that backend, not a loosened tolerance.

**The counts carry no such condition** — the read-back is pure geometry with no GPU in the path —
which is why the hard gate is the count gate and only the soft gate is the picture: only one of
the two ports across backends. When you must validate somewhere the goldens don't apply, run
`--check` for the counts and treat a pixel failure as "re-baseline needed here", not "model broke".

## Why this is a skill and not a pre-commit gate (D-028)

The render path has a GPU in it, so a gate that rendered on every commit would be both slow and
backend-fragile in exactly the way K10 describes. Graduating this to a hook waits until the defect
it would catch shows **measured recurrence** — the same *no skill/gate before the recurrence is
measured* discipline as [`docs/issue-register-evaluation.md`](../../../docs/issue-register-evaluation.md)
and [`docs/dsl-extension-skill-evaluation.md`](../../../docs/dsl-extension-skill-evaluation.md). If
you find yourself running `--check` by hand to catch the same regression a third time, that is the
recurrence — record it and propose the gate then, not before.

## Rules

- Never certify a model from a single angle. If you rendered one, say only what one view shows.
- A pixel diff over tolerance on an unfamiliar backend is a re-baseline signal, not a model defect
  — confirm with the counts before reporting the model wrong.
- `--update-goldens` changes committed truth: do it only for a verified, intended change, name the
  change in the commit, and never to make a red `--check` go green without understanding why it was
  red.
- The colour gate expects the *visible* set, not the resolved set — an occluded colour belonging
  in `.notes.md` but not `visibleColours` is correct, not a bug. Never add an occluded colour to
  `visibleColours` to "complete" it; that is what false-fails the next render.
- When a model's palette changes, update its `.notes.md` in the same commit — the catalog gate
  (CI + pre-commit) blocks a resolved colour the notes never name.
- The fixture `bikar:scripts/fixtures/ldraw-thumbnails/Brick-Stack.mpd` and its goldens, notes, and
  expectation are the one exercised model; §10.6's "one of twelve viewers" caveat still stands for
  everything else.
