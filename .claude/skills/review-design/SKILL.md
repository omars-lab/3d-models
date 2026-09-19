---
name: review-design
description: Audit a design doc for newcomer-friendliness — is the premise, the problem, and why-it-matters up front in plain language; is every domain term and product name defined in a footnote glossary; is the jargon (file:line anchors, grammar, kernel internals) deferred to an appendix. Use before publishing or merging a design doc, when a doc reads like a diff or a wall of jargon instead of an explanation, or when someone new could not follow it cold. Scores against the shared design-craft rubric and reports one fix per failing criterion.
argument-hint: <path/to/design-doc.md> [more docs...]
---

# Review a design doc for the engineer who reads it cold

Take the design doc(s) in `$ARGUMENTS` (ask which doc if none given) and answer one
question: **could an engineer who joined the team this week understand what this is,
what problem it solves, and why it matters — from the top of the doc, without knowing
our product names or following a link?**

This is not a grounding review ([`ground-design-doc`](../ground-design-doc/SKILL.md)
checks whether the claims are *true*) and not a figure review
([`design-note`](../design-note/SKILL.md) checks whether a *drawing* settles an
argument). This checks whether the doc is **readable**. A doc can pass both other
bars and still fail this one.

## The standard is shared, not built in

The rubric lives in [`../design-craft.md`](../design-craft.md) — the arc a good doc
follows, the twelve clarity rules (C1–C12), the glossary-via-footnotes pattern, the
diagram-with-legend pattern, and a worked good/bad example. **Read it first, every run.** It is the authority; this file
is only the process for applying it. When you find a failure the rubric doesn't name,
add it *there*, not here.

## Process

### 1. Read design-craft.md, then the doc — as a newcomer

Read the rubric. Then read the target doc **once, top to bottom, pretending you know
nothing about the codebase.** The moment you hit a word you'd have to already know —
a product name, an acronym, a file path, a decision id — mark it. That first-read
confusion is the data; you cannot recover it on a second read once you've decoded the
doc, so capture it now.

### 2. Score each criterion C1–C12

For each rule in the rubric, decide PASS or FAIL against *this* doc, and for a FAIL
pin the exact line where a newcomer first falls off. Be concrete about the failure —
"C3 fail: `AMS` used at line 14, never defined" — not "could use more definitions."

The most common and most damaging failures, in order:

- **C1/C2 at the very top.** The doc opens on "the finding that shapes this doc," on
  the mechanism, or on a region/grammar name — no premise, no problem. A newcomer is
  lost at sentence one. This is the failure that makes a doc "a wall of jargon."
- **C3 unglossed terms.** List *every* domain term used before it's defined. A
  first-paragraph proper noun with no footnote is the single worst offender.
- **C4 jargon in the body.** `file:line` anchors and grammar productions in the prose
  instead of an appendix.
- **C8 walls of text.** A pipeline or data flow explained in paragraphs with no
  diagram. If you find yourself re-reading a paragraph to trace "A → B → C," that
  paragraph wanted a Mermaid diagram — say so and sketch the nodes.
- **C9 no component or data-model view.** The doc spans repos/packages but never
  shows the boundaries (which side owns what) or the classes it touches. Flag it if
  you cannot tell, from the doc, which component a change lands in, or if the touched
  types are named in prose but never drawn and reasoned. Watch the level too: a
  data-model diagram that draws the whole model instead of the impacted slice fails
  C9 as surely as one that is missing.
- **C10 no context diagram, or internals first.** The doc drops the reader into
  packages and classes without ever drawing the outside world — the actors and
  neighbouring systems it sits among, with the interactions labeled. Flag it if the
  first structural picture is a component/class diagram rather than a context one.
- **C11 use cases missing or actor-less.** No list of the use cases the design
  enables or impacts, or a list with no named actor, or one that is never drawn as a
  use-case diagram. "Who does what, and what's new versus changed" should be legible
  at a glance.
- **C12 user-facing surface left to guess.** The reader cannot tell which app, page,
  tab, button, or command the change surfaces in — and the doc never says "no
  user-facing surface" for an internal/CLI/format change. Silence here is a fail; an
  explicit "none, this is a CLI-only change" is a pass.

### 3. Report — one fix per failing criterion

Output a findings list, most-damaging first. Each finding:

```
[C_] <criterion> — <file>:<line>
  Fails because: <the specific thing a newcomer trips on>
  Fix: <a concrete rewrite or move — an actual sentence, or "move lines X–Y to an
        appendix", or "footnote `bikar` as: ...". Never "make it clearer.">
```

End with a one-line **verdict**: `PASS` only if all twelve criteria pass, else
`FAIL (n/12)` naming which failed. A doc that fails is not ready to merge.

### 4. Offer the rewrite, don't sneak it

If the doc is being *iterated* (the caller wants it fixed, not just scored), hand the
findings to [`write-design`](../write-design/SKILL.md) — that skill owns authoring to the
standard. Reviewing and rewriting are separate steps so the score stays honest: a
reviewer who also rewrites grades their own work.

## When this is the wrong tool

- **The doc's claims might be wrong**, not just hard to read → [`ground-design-doc`](../ground-design-doc/SKILL.md).
- **The argument needs a picture** → [`design-note`](../design-note/SKILL.md).
- **It's a decision record, not a design** — `docs/decisions-log.md` entries are
  terse by design and don't owe a newcomer the full arc.
- **It's not a design doc at all** (a runbook, a research file under `docs/research/`,
  a README). Those have their own audiences; don't force the design arc on them.
