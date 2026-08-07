---
name: validate-render
description: Turn an LDraw model (.mpd/.ldr) into a set of camera-angle PNGs and validate it against a committed expectation. Use when checking that a brick/assembly export still renders and reads back correctly, when regenerating a model's thumbnails, or before putting a render in a PR or the gallery — the tool renders several angles because one view of stacked bricks cannot show how many there are, and gates them by exact counts plus tolerant golden pixels.
---

# Validate a render — a `.mpd` to a *set* of PNGs, gated two ways

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
- **Golden pixels are the soft gate.** A render is GPU/driver dependent, so the differing-pixel
  fraction is compared against a small `--tolerance` (default 0.02), not against zero. A one-pixel
  wobble passes; a materially different frame fails. A size mismatch is a hard fail (not a
  swallowable ratio).

Exit 0 means both passed; nonzero prints which gate fired.

**The load-bearing case — read it, don't skip it.** If `--check` reports `counts` failing while
every angle's pixels still pass, that is the tool working, not a flake: an emitter change added or
dropped a part in a way no camera angle shows. Trust the counts. The inverse — pixels fail,
counts pass — is usually the backend, not the model (see K10 below).

**Update goldens (`--update-goldens`).** Only after a render legitimately changed (an intended
emitter change, verified by reading the new counts), and **only on the same backend that will
validate against them** (see K10). Writes `<name>.expected.json` + the angle PNGs as the new
goldens. Commit them with the change that caused them.

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
- The fixture `bikar:scripts/fixtures/ldraw-thumbnails/Brick-Stack.mpd` and its three goldens are
  the one exercised model; §10.6's "one of twelve viewers" caveat still stands for everything else.
