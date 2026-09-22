---
name: write-design
description: Author or restructure a design doc so an engineer who joins next quarter can read it cold — premise and problem first in plain language, the idea before the mechanism, every domain term and product name defined in a footnote glossary, and the jargon (file:line anchors, grammar, kernel internals) moved to an appendix. Use when starting a new design doc, or when review-design has flagged one as a wall of jargon that reads like a diff. Writes to the shared design-craft standard and loops with review-design until it passes.
argument-hint: <path/to/design-doc.md> [findings from review-design]
---

# Write a design doc the next engineer can read cold

Author (or restructure) the doc in `$ARGUMENTS` so its first reader — an engineer who
joins the team next quarter and opens it knowing none of our names — gets the premise,
the problem, and the stakes from the top, in plain language, before any mechanism.

This is the authoring counterpart to [`review-design`](../review-design/SKILL.md).
That one scores; this one writes. They loop.

## The standard is shared

The arc, the thirteen clarity rules, the glossary-via-footnotes pattern, the
diagram-with-legend pattern, and a worked good/bad rewrite all live in
[`../design-craft.md`](../design-craft.md). **Read it first, every run.** Author to
it; do not reinvent the structure here.

## Process

### 1. Read design-craft.md and any review findings

If the caller passed findings from [`review-design`](../review-design/SKILL.md), those
are your work list — each failing criterion is a thing to fix. If this is a new doc,
the arc in design-craft.md (§"The arc every design doc follows") is your outline.

### 2. Preserve the content; change the order and the words

The most important rule of a restructure: **drop nothing technical.** A jargon-heavy
doc is usually *correct* — it fails the newcomer on order, translation, and deferral,
not on facts. So the move is:

- **Reorder** — why before how. Lift the premise and problem to the top; push
  `file:line` anchors, grammar productions, and edge-case rules to an appendix.
- **Translate** — put a plain sentence (or an analogy) ahead of each mechanism. "Our
  patterns are rings of tiles, like a dartboard" earns the right to then say
  "faces bucketed by centroid distance."
- **Gloss** — footnote every domain term at first use; collect them in `## Glossary`.
- **Draw** — every pipeline, data flow, before/after, or "which branch wins" decision
  gets a Mermaid diagram (C8), with node labels that reuse the glossary terms and a
  one-line footnote-linked legend beneath it. When a paragraph traces "A → B → C,"
  replace or accompany it with the picture; don't leave the reader to build it in their
  head. And when the design spans components or repos, add the two structural diagrams
  (C9): a component diagram grouped by repo/package (who owns what), and a class-level
  data-model diagram scoped to the *touched* types (new/changed/reused, each with a
  one-line why) plus its table. Draw the system at package level, the data model at
  class level for the impacted slice only. Before those, draw the two outside-in
  diagrams: a **context diagram** (C10) with the feature in the middle, its actors and
  neighbouring systems around it, and the interactions labeled on the arrows; and a
  **use-case diagram** (C11) linking each actor to the use cases this enables or
  impacts. And state the **user-facing surface** (C12) in prose — the app, the
  page(s), any new/changed tab/page/button/command, or an explicit "no user-facing
  surface." See design-craft.md §"Diagrams — show it, don't only tell it", §"The
  context diagram and the use-case diagram", and §"The two structural diagrams a
  cross-component design owes."

Keep the appendix rich. Deferring jargon is not deleting it — the specialist who needs
the `file:line` anchor still finds it, just not in the reader's way.

### 3. Write the arc

Follow design-craft.md §"The arc": title + premise → problem → why it matters → the
idea (mental model) → context and interactions (context diagram) → use cases
(use-case diagram) → the user-facing surface → the pieces and where they live
(component + data-model diagrams, for a cross-component design) → how it works →
alternatives + decision → glossary → appendix. Sections 1–4 carry no unglossed
jargon; that is the line.

For an *existing* doc, this usually means: write a fresh premise/problem/idea opening,
then keep the old technical sections but demote the deepest ones into `## Appendix`,
and add the glossary. Don't rewrite grounded technical prose that already passes — move
it, gloss its terms, and lead it with a plain sentence.

### 4. Loop with review-design until it passes

Run [`review-design`](../review-design/SKILL.md) on the result. Apply every finding.
Re-run. Repeat until the verdict is `PASS (13/13)`. Do not stop at "better" — the bar
is the full rubric green, because a newcomer needs all thirteen, not most.

Each pass should converge: if the same criterion fails twice, the fix wasn't concrete
enough — go back to the rubric's PASS wording for that rule and write to it literally.

### 5. Respect the other gates

A design doc here also answers to the grounding gates (`docs_gate.py`,
`doc_pointers.py`, `validate.py`) and, where claims need sources,
[`ground-design-doc`](../ground-design-doc/SKILL.md). Restructuring must not strip a
`**Default:**` marker, a `**Validator:**`/PASS/FAIL block, a CAL bet id, or a
`` `repo:path:Lnn "literal"` `` anchor — moving those to an appendix is fine, deleting
them is a gate failure. Readability is a new bar on top of the old ones, not a licence
to drop them.

## When this is the wrong tool

- **The doc reads fine and only its facts are in doubt** → [`ground-design-doc`](../ground-design-doc/SKILL.md).
- **The decision needs a drawing to settle** → [`design-note`](../design-note/SKILL.md).
- **It's a decisions-log entry, a runbook, or a research file** — those aren't design
  docs and don't take the arc.
