---
name: design-note
description: Turn a design decision into a published note whose figures are compiled from the parts the repo builds today. Use when a decision has real alternatives and a drawing would settle it, when a design doc's Open Questions entry needs an argument before it can close, or when a decision was taken and the reasoning is about to be lost. Starts with /artifact-design for the visual treatment, then componentizes the artifact into a DesignNote module on the studio's design.html.
---

# Design note — the argument, with the geometry compiled beside it

A design doc argues in prose. When the argument is *about a shape* — a socket
that is declared and never cut, three ways to decompose a part, a clearance you
cannot picture — prose loses, and the usual fix is to draw a picture. A drawn
picture is a lie in waiting: it is correct on the day it is drawn and nothing
notices when it stops being.

This skill's whole claim is that a figure should be a **compile**, not a
drawing. `design.html` loads notes as modules and calls `render()` in the
browser with the real kernel in scope, so every section is cut from the part the
repo builds right now. A note whose argument has expired throws on the page and
turns `packages/lab/tests/design-notes.test.ts` red, instead of ageing well.

Where each skill stops:

```
ground-design-doc  — what sources can settle
calibrate          — what only a printer can settle    (../calibrate/SKILL.md)
design-note        — what a section drawing can settle, and what was chosen
```

## When this is the wrong tool

- **The decision has one option.** That is a design-doc paragraph.
- **The argument has no geometry in it.** Process, tooling, repo-layout calls
  go straight to [`docs/decisions-log.md`](../../../docs/decisions-log.md).
- **The unknown is a measurement.** That is `calibrate`, and a note that draws
  a number nobody measured launders a guess into a picture.
- **It is a defect.** Per the graduation rule in
  [`CLAUDE.md`](../../../CLAUDE.md) a defect ships a test, not a note.

## Workflow

### 1. Frame it

Name the decision, the doc section it argues about, and **the alternatives that
are actually on the table** — with the one that gets rejected still written
down, because a note with one option is an announcement. Write the eyebrow
first (`3d-models · docs/lego-lab-design.md · §10 P1`): if you cannot name the
section this argues about, the note has no home and probably no reader.

Set `status: 'open'` and leave `decision` unset. A note that opens already
knowing its answer is a defence, not an argument, and it reads like one.

### 2. `/artifact-design` for the treatment

Invoke `artifact-design` and produce its design plan — palette, the type pairing,
the layout concept — for *this* note's subject. It is a utilitarian treatment:
a technical argument read by one designer, not a landing page.

Then apply its own first rule against the studio. **The design system already
exists** in `packages/lab/src/design/tokens.css`, and precedence runs the user's
words, then the project's system, then your choices. So the plan's job is to
fill gaps and to decide this note's *one* distinguishing move — a figure layout,
a comparison table, an accent restricted to the option being argued for. When
the plan proposes a colour or a face the tokens already answer, drop that part
of the plan; do not fork the palette for one page.

A section drawing takes its colour from `tokens.css` class names, never from
inline fills. A note that wants its own accent restyles the classes — it does
not re-render the geometry.

### 3. Componentize

One file: `packages/lab/src/design/notes/<id>.ts`, exporting a `DesignNote`.
The id is a URL slug (`design.html?n=<id>`) and is **stable forever** once
published, because `docs/decisions-log.md` cites it.

- Compile, don't draw: `compileToGeometry(script.source).brick3d`, then
  `brickSection(brick, opts, scale)` from `../draw`. Source the script through
  `brickScriptById` and **throw** when the preset is missing — a renamed preset
  must break the page, not silently draw a different brick.
- Hand-authored marks go in `overlays` and nowhere else. That list is dashed and
  warn-coloured on purpose: a reader has to be able to tell a claim from a
  measurement without reading the caption. A `phantom` says *declared and not
  cut*; a `rod` says *arrives from off-drawing*.
- Every figure goes through `figure({ svg, caption, from })`. `from` names the
  script it compiled. When the note added marks of its own, `overlaid` says what
  they were.
- Compare like with like: sections that argue against each other share a scale.

Register it in `src/design/notes/index.ts`, newest first — the list is dated in
descending order and the suite checks that.

### 4. Land it in the catalogue

`design.html` is already a catalogued page, so an added note needs no catalogue
edit. A *new* page does: `src/catalog.ts` `PAGES` entry (file, entry module,
`status`, and each actor's `does` in that actor's own words), then the
`LAB_PAGES` list in this repo's `Makefile`, `.gitignore`, and a UC row in
[`use-cases.md`](../maintain-use-cases/use-cases.md) — the `page_catalogs` rule
fails the commit if the catalogue claims a use-case id the map does not carry.

### 5. Close it

When the decision is taken: flip `status` to `decided`, fill `decision`, and add
the entry to [`docs/decisions-log.md`](../../../docs/decisions-log.md) with its
reversal condition, citing the note by id. Superseding a note sets
`superseded` and points at what replaced it.

**Notes are never deleted.** The reason an option was rejected is worth as much
as the reason one was taken, and the log's link has to keep resolving.

## The parity rule

**Validator:** a note's `<figure>` count equals its `Compiled from` count, and
`tests/design-notes.test.ts` fails when they are not equal.

- PASS: the `multi-piece-export` note renders 3 figures and 3 provenance lines —
  every drawing on the page names the script it was cut from.
- FAIL: a fourth `<figure>` built with hand-written `<svg>` instead of
  `figure({...})` — 4 figures, 3 provenance lines, suite red. This is the
  failure the rule exists for: an undocumented drawing is indistinguishable from
  a compiled one on screen, which is exactly the lie the page claims not to tell.

## Verify

```sh
export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"
cd ~/Workspace/git/bikar-lego-lab && npm run ci     # renders every note against the kernel
cd ~/Workspace/git/3d-models && make lab && make validate-use-cases
```

`npm run ci` is the real gate: it calls `render()` on every note, so a figure
that no longer compiles fails there rather than on a page nobody reloaded.

## Rules

- Never hand-author geometry the kernel can compile. If it cannot be compiled,
  it is an overlay and it is dashed.
- Never delete or renumber a note id.
- A note argues; it does not decide alone. The decision lands in
  `docs/decisions-log.md` with what would reverse it.
- `preview` status on the page means *reachable and not somewhere to send
  anyone*. Do not promote it to `live` to make an index look finished.
- The bikar working checkout `~/Workspace/git/bikar` may belong to another
  session — do this work in the `bikar-lego-lab` worktree, and read the other
  checkout only through `git show`/`git log`/`git diff`.
