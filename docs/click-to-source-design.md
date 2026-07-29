# Click-to-source — implementation design doc

Status: **DRAFT v1 — grounded in first-party experiments against the bikar tree (a working
prototype; measurements in §2, §3 and §5.3) and in fetched external sources (Appendix A).
Contested bets in Appendix B.**
Scope: given a rendered artifact — an SVG face, a derivation-worksheet panel, or something in the
Lab — take the reader to the `.bkr` source that produced it.
Builds on: `lex` → `parse` → `evaluateFile` → `renderSVG`, the `Segment.tags` → `Face.sources`
provenance channel, and the `data-*` contract in `bikar/docs/dsl-metadata-contract.md`.
Rides: nothing. **Breaks** the derivation-worksheet doc's no-engine-file rule — deliberately, and
§5.2 says so out loud.

This document answers **Q11** of
[`derivation-worksheet-design.md`](derivation-worksheet-design.md) §8.9 ("Does click-to-source
require source spans in the AST, and does that change the IR calculus?"). It does not modify that
document.

**Nothing in this doc is implemented in the bikar tree. No engine file has been changed.** The
measurements in §2, §3 and §5.3 come from a throwaway prototype built in a scratchpad: a copy of
`packages/core/src` with a 12-line patch, bundled with esbuild and run against the corpus. The
patch is described verbatim in §2.3 so it can be reproduced or disputed.

---

## 1. Goals

1. **Answer honestly or decline.** A reader who clicks a shape must get either the statements that
   demonstrably contributed to it, or an explicit "cannot be resolved" — never a confident wrong
   line. §3 shows this is not a hypothetical worry: a *majority* of faces have more than one
   contributing statement.
2. **Statement granularity, not expression granularity.** The unit of the answer is the `.bkr`
   line, because that is the unit a person edits. Sub-expression spans are §5.7 scope-out.
3. **Do not damage the existing contract.** `data-shape-id`, `data-authored-region` and gt.json
   `source_primitives` are live cross-repo surfaces with witness tests. §5.3 records a measured
   way this feature corrupts them, and the decision that avoids it.
4. **Separate the cheap half from the expensive half, and be willing to ship only the cheap half.**
   §9 concludes that is exactly what should happen.

**Non-goals for v1:**

- **No bidirectional editing.** Nothing drags a vertex and rewrites the source. Zoo does this
  (§4.5) and it is a different product.
- **No expression-level spans.** §2.2 prices them at 101 construction sites; §5.2 declines.
- **No language server.** §4.7 examines whether LSP is the endgame and concludes it is the
  *eventual* right frame but not the v1 shape.
- **No new DSL syntax.** Nothing here adds a keyword to `.bkr`.
- **No `.bkr` file modified**, ever, by this feature.

---

## 2. Premise check

**The premise, as stated in the brief that commissioned this work** (and inherited from
`derivation-worksheet-design.md` §6, which listed click-to-source among deferred items and called
it "cheap"): source positions exist at the token level and are thrown away at node construction, so
click-to-source means threading positions through a 3,993-line hand-rolled parser — expensive, and
Q11 was right to flag it as blocked rather than deferred.

**Q11 is half right, and the half it gets wrong is the important half.**

Q11 is right that §6's "both cheap" citation was wrong, and the reading of the sources is worse for
§6 than Q11 assumed. `derivation-visualization-survey.md` §12.7 is itself accurate — it describes
**step→source**, a timeline dot mapped to the line of the stdlib call that produced it. §6
compressed that into **shape→source**, which is a different and much harder problem, and which
CascadeStudio does not implement at all: its viewport has no click listener and its face index is
never joined to its line numbers (§4.4). Zoo does implement it, and its own design doc states §3's
problem in almost the same words (§4.5). Q11 is **wrong that the span work is the expensive part.**
The parser has two dispatch chokepoints, and a 12-line patch at those two sites produces correct
spans on 99.6% of statement and declaration nodes across the corpus. The expensive part is
somewhere Q11 did not look: **getting from a statement to a rendered face**, which §3 shows is
irreducibly many-to-many and §5.3 shows cannot ride the provenance channel that already exists.

### 2.1 The starting facts, re-verified

Each of these was independently re-measured; all four hold.

| Claim | Verdict | Evidence |
|---|---|---|
| `Token` carries `line` and `column` | **holds** | `bikar/packages/core/src/dsl/tokens.ts:190-195` — `readonly line: number; readonly column: number`, documented as 1-based |
| `ParseError` carries `line`/`column`; CLI pretty-prints `<file>:<line>:<column>` | **holds** | `bikar/packages/core/src/dsl/parser.ts:90-99`. `LexerError` does the same at `lexer.ts:4-13` |
| `ast.ts` has **zero** source-position fields | **holds** | grep for `^\s+(readonly )?(line\|column\|loc\|span\|start\|end\|pos\|range\|offset\|comments\|trivia)\??:` over all 1,190 lines returns **0** |
| Comments are destroyed in the lexer | **holds** | `bikar/packages/core/src/dsl/lexer.ts:85-90` — *"`#` to end-of-line; whole comment discarded"*; `consumeComment` advances the cursor and emits no token |
| 31 of 92 pattern files carry `# Construction:` blocks | **holds exactly** | 92 `.bkr` under `bikar/patterns/`; 31 match `# *Construction:` |

`ast.ts` inventory, since §5.2 turns on it: **67 interfaces, 12 type aliases, 59 interfaces named
`*Node`.**

### 2.2 What expression-level spans would cost — 101 sites

Measured by parsing `parser.ts` with the TypeScript compiler API and counting object literals
carrying a string-literal `kind:` or `type:` discriminant:

```
object literals in parser.ts:                 166
tagged node-construction sites:               101   (71 `kind:`, 30 `type:`)
distinct tags:                                 76   (59 `kind:`, 17 `type:`)
object literals returned directly:            102   (26 of them untagged)
```

**101 is the honest price of putting a span on every node**, and it is the number the brief asked
for. It is also the wrong number to design against, because §2.3 shows a much smaller one buys
everything the feature actually needs.

### 2.3 The chokepoint finding — 2 sites, not 101

`parser.ts` routes **every** statement through one function and **every** top-level declaration
through one other:

- `parseStatement()` — `parser.ts:2167-2172` — a single `this.statementHandlers[t.type]` lookup
  over a **39-entry** table (`parser.ts:2126-2165`).
- `parseDeclaration()` — `parser.ts:604-615` — a single `this.declarationHandlers[…]` lookup.

Both already read `this.peek()` — the token whose `line`/`column` we want — before dispatching.
So the span can be attached *around* the handler rather than inside each of the 101 constructors.

**The prototype patch, verbatim and complete** (`+9 / −2` lines, 2 hunks, one file):

```ts
// parser.ts, parseDeclaration()
-    return handler();
+    const startTok = this.peek();
+    const node = handler();
+    const prev = this.tokens[Math.max(0, this.pos - 1)];
+    return { ...node, loc: { line: startTok.line, column: startTok.column,
+             endLine: prev.line, endColumn: prev.column + String(prev.value).length } } as Declaration;

// parser.ts, parseStatement()
-    if (handler) return handler();
+    if (handler) {
+      const node = handler();
+      if (!node) return node;
+      const prev = this.tokens[Math.max(0, this.pos - 1)];
+      return { ...node, loc: { line: t.line, column: t.column,
+               endLine: prev.line, endColumn: prev.column + String(prev.value).length } } as ASTNode;
+    }
```

plus one interface in `ast.ts` (`SourceLoc`) and one optional `loc?: SourceLoc` on the node types.

**Measured against all 92 corpus files:**

```
files parsed ok/fail:                          92 / 0
statement + declaration nodes:               1,405
       …carrying a loc:                      1,400   (99.6%)
loc pointing at a blank or comment-only line:     0
evaluateFile still succeeds:                  92 / 92
```

The 5 misses are named: `rod` ×3 and `extrude` ×2, in `Pinned-Tiles.bkr`, `Fit-Coupon.bkr` and
`Nail-Tile.bkr`. They are `PieceConstructorNode`s built by `setBody(...)` inside
`parsePieceDeclaration` (`parser.ts:1181-1220`), which does not route through `parseStatement`.
Covering them is a third hunk; it is not covered here so the 99.6% number stays honest about what
two hunks buy.

**Coverage of the wider node graph.** Of 2,136 AST node objects across the corpus, **1,405 (65.8%)
are direct members of a `declarations` / `statements` / `body` array** and therefore reachable from
the two chokepoints. The 731 (34.2%) that are not are almost entirely sub-statement payloads —
`expr:literal` (224), `expr:where` (212), `file` (92), `styleRule` (35), `expr:var` (32),
`expr:attribute` (26). **That is exactly the population Goal 2 declines to address.** The
chokepoint covers 100% of the granularity the feature promises and 0% of the granularity it
disclaims, which is a suspiciously clean result and is why it is stated as a measurement rather
than an argument.

### 2.4 Two hazards found while measuring, neither previously recorded

**(a) Token columns are computed against a rewritten source.** `lex` is a three-stage pipeline
(`lexer.ts:333-341`): `preprocessSource` rewrites color-context `#RRGGBB` into a `__hex_RRGGBB`
identifier (`lexer.ts:314-330`) so `#` can still mean "comment", *then* `tokenize` runs, *then* a
post-pass converts the markers back. The rewrite is **length-changing** — `#` (1 char) becomes
`__hex_` (6 chars), +5 per literal — and `tokenize` counts columns on the rewritten string.

Measured, with a deliberate syntax error placed after a hex literal on the same line:

```
source line:  `      lapis = #1A3A6E %%%`
true 1-based column of `%`:                23
column reported by ParseError:             28      (+5)
control line with `XXXXXXX` in place:      matches the true column
```

Line numbers are unaffected (the rewrite never spans a newline in practice), so **statement-level
spans are safe and column-level spans are not.** 283 lines across 75 of 92 corpus files carry a
hex literal. This is a pre-existing defect in `ParseError`/`LexerError` reporting, found here and
not fixed here.

A related latent hazard: `preprocessSource`'s regex is `(?:=|color|stroke|fill)\s*#([0-9a-fA-F]{3,8})`
and `\s*` matches newlines, so a comment line beginning `#deadbeef` immediately after a line ending
in `=` would be silently eaten. No corpus file trips it. **Unverified beyond inspection** — not
reproduced.

**(b) `for` is a token-level macro, so one line legitimately becomes N statements.**
`expandFor` (`parser.ts:3085-3129`) captures body tokens by indentation, calls `substituteLoopVar`
once per iteration, and **splices the copies back into `this.tokens`** (`parser.ts:3129` — the only
token-stream mutation site in the parser). `substituteLoopVar` (`parser.ts:311-336`) copies tokens
through unchanged unless a rewrite fires, so every unrolled iteration keeps the *original* body
line numbers. Synthesized separator newlines get a fabricated `{ line: forTok.line, column: 1 }`.

Consequence: **`for` makes the source→shape direction one-to-many by construction**, and no span
scheme can change that. `for` is used in **0 of 92** bikar pattern files and **2** `.bkr` files
under `qiyas/`, so it is latent rather than active — but it is in the language.

---

## 3. The many-to-many problem — measured end to end

This is the section the feature lives or dies on, so it is answered with a working prototype rather
than an argument.

### 3.1 The mechanism under test

The prototype extends §2.3 with three more hunks so a face can be asked which lines built it:

- `environment.ts` — one field `currentStmtLine`, and one line in `tagSegments`
  (`environment.ts:303-328`) pushing `src:<line>` alongside the existing `layer:N` / `wave:N` tags.
- `evaluator.ts` — one wrapper around `evaluateStatement` (`evaluator.ts:3373`) that sets
  `env.currentStmtLine` from `node.loc` and restores it in a `finally`. Like the parser, the
  evaluator has a **single dispatch chokepoint**: `STATEMENT_DISPATCHERS`, a 33-entry table at
  `evaluator.ts:3346-3379`.
- Nothing else. Tags already flow `Segment.tags` → `face-extractor.ts:29` (`sourcesSet.add(tag)`)
  → `Face.sources` (`graph/half-edge.ts:46`).

Total: **5 hunks across 3 files.** It builds and the whole corpus still evaluates.

### 3.2 The answer, in one table

**Distinct source lines per rendered face, all 92 files, 5,394 faces:**

| lines resolved | faces | share |
|---|---|---|
| 0 | 131 | 2.4% |
| **1** | **2,097** | **38.9%** |
| 2 | 2,724 | 50.5% |
| 3 | 438 | 8.1% |
| 4 | 4 | 0.1% |

**38.9% of faces resolve to exactly one source line. 58.7% resolve to two, three or four. 2.4%
resolve to none.** The worst case is 4 (`Tangent-Sq-Oct.bkr`, lines 26–29). There is no long tail:
the answer is small and plural, not large and plural.

**The other direction is far worse.** Grouping faces by statement-ish source (the `:#<counter>`
invocation suffix stripped, which is a *lower* bound on distinct statements because two identical
statements collide):

```
186 statement-ish sources across the corpus
faces produced per source:   median 17   p90 129   max 417
sources producing exactly one face:  1 of 186
```

**One statement produces a median of 17 faces. Exactly one statement in the entire corpus produces
exactly one face.** Any UI framed as "this line ↔ this shape" is describing a relationship that
occurs once in 186.

Independent corroboration from the raw tag sets, before any statement-ish collapsing: median 3
distinct source tags per face, p90 4, max 14 (`Petal-2-Ring.bkr`, `Petal-Outer-Glow.bkr`);
**53.1% of faces carry two or more distinct `connect`-invocation tags** (`:#N`), and 54.3% have two
or more *distinct edge-source-sets* around their own boundary — i.e. the face's edges genuinely come
from different statements, which is what "the arrangement walk emerges from many contributors"
means concretely.

### 3.3 Where the 2.4% with no answer come from — arcs are a second, un-chokepointed channel

The 131 untagged faces are not spread evenly. They concentrate in the Petal Tutorial family:
`Petal-Full.bkr` **37 of 37 faces**, `Petal-2-Ring.bkr` 19, `Petal-Outer-Glow.bkr` 19,
`Petal-1-Ring.bkr` 13, `Petal-Spin.bkr` 13, `Petal-Strapwork.bkr` 13.

Cause: `connect arc` **bypasses `tagSegments` entirely** — stated in-source at
`evaluator.ts:3841-3843` (*"arc is handled separately because it bypasses tagSegments /
auto-intersect entirely"*). Arc edges go to `env.arcEdges`, a parallel array with **6 push sites**
(`evaluator.ts:3774, 4554, 4679, 4716, 4849, 4878`). So the emission side has **two** channels and
only one of them is a chokepoint.

This matters out of proportion to 2.4%, because **the arc-built lens is the signature shape of the
corpus** — the petal. A click-to-source feature that silently has no answer for petals is answering
for the wrong half of the collection. Closing it is a sixth hunk across 6 sites, not a redesign, but
it must be costed rather than assumed.

### 3.4 Three more sources of plurality, each irreducible

- **`rotate` / `mirror` replay.** `evalRotate` (`evaluator.ts:4605-4625`) emits replicas and *then*
  stamps `rotate:N` over everything emitted since a watermark, via `appendTag`. Bodies do route
  through `evaluateStatement`, so `src:` tags survive replay — but N instances all carry the same
  line, which is correct and one-to-many.
- **`for` unrolling** — §2.4(b).
- **Face extraction itself.** Faces are *found* by an arrangement walk, not constructed
  (`bikar/docs/architecture.md`, and `derivation-worksheet-design.md` §2.1). A face's boundary is
  whatever edges bound it; nothing in the pipeline ever decides that a face "belongs to" a
  statement. The 54.3% two-or-more-edge-source-sets figure is this fact in numeric form.

### 3.5 Decision: what the feature promises

**Decision: the answer is a *set* of statements, ordered by line, always rendered as a set even
when it has one element. When the set is empty the feature says so. It never picks a winner.**

Rejected options, and why:

| Option | Why rejected |
|---|---|
| **Single "best" line** — e.g. the minimum, or the most-frequent contributor | The only faces this is correct for are the 38.9%. On the other 58.7% it would be a confident lie, which Goal 1 forbids. There is also no principled tiebreak: `data-wave` and `data-layer` use a **min** rule (contract table, `data-wave` row) but that rule is defensible only because wave/layer are *ordinal construction passes*, and a line number is not one. |
| **Omit the attribute when ambiguous** — the existing house rule | This is the established discipline for `data-shape-id` and `data-authored-region` (*"omitted (attribute absent / `authored_region: null`) when a face's bounding edges carry >1 distinct region id … never guessed"*, `dsl-metadata-contract.md`). It is right for *identity* attributes, where a wrong id poisons a downstream classifier. It is wrong here: it would answer on 38.9% of faces and stay silent on 58.7%, which is the *inverse* of useful. A set of two lines is a good answer; no lines is not. |
| **Rank and show a primary + "also"** | Same tiebreak problem, dressed up. Deferred to Q6, not adopted. |
| **Highlight the enclosing block instead** (the `pattern`/`blueprint` declaration) | Always correct and almost never useful — the median file has 15 statements+declarations, so the block is most of the file. |

**Both shipping implementations independently reached the same answer** (§4.5, §4.6): Zoo
highlights the `line(...)` *and* the `extrude(...)` for a single picked wall face; OpenSCAD offers
the whole ancestor chain as a menu and labels the ones without a span `" (no source reference)"`.
Neither picks a winner. That is corroboration, not proof — Zoo also carries a
`codeRefLookup?: 'first' | 'last'` tiebreak knob (`selections.ts:387`), so "always a set" may be
the honest first answer rather than the final one (Q3).

The house precedent is being **deliberately departed from**, and Appendix B.2 records that as a
contested bet. The difference in kind: `data-shape-id` answers *"what is this?"*, where a wrong
answer is worse than none; click-to-source answers *"where do I look?"*, where two candidate places
still beats zero.

**The measured shape of the promise:** 38.9% one line, 58.7% two-to-four lines, 2.4% "not
resolvable" — and 2.4% falls to near zero if the arc channel is threaded (§3.3).

---

## 4. What the research establishes

Load-bearing external findings, with the design consequence stated. Full URLs in Appendix A. Every
quotation below is from a page that was fetched; failures are recorded in Appendix A.

### 4.1 Source maps are the wrong model, and the analogy should be dropped

ECMA-426 defines every positional field as a position **in text**: a segment's fields are *"The
zero-based starting column of the line in the generated code that the segment represents"*, *"the
zero-based index into the sources list"*, *"the zero-based starting line in the original source"*,
*"the zero-based starting column of the line in the original source."* Even the composition
mechanism assumes text — an index map section's `offset` is *"an object with two fields, `line` and
`column`, that represent the offset into generated code."*

Two structural mismatches, both fatal:

1. **The generated side must be text with line/column positions.** bikar's generated side is a set
   of faces found by an arrangement walk. There is no generated line to key on. (An SVG *is* text,
   but the face's position in the SVG file is an artifact of emission order, not of geometry.)
2. **A segment maps one generated position to at most one source position** — 1, 4 or 5 fields,
   where the 4/5 forms carry exactly one `(sourceIndex, line, column)` triple. §3 measured the real
   relationship at one-to-many in both directions. *(The "at most one" phrasing is inference from
   the field grammar; no spec sentence states it. Marked as such.)*

The field's own precedent agrees: when output stopped being text, the industry left source maps
rather than extending them. Chrome's WebAssembly debugging post is explicit — *"source maps were
designed for text formats with clear mappings to JavaScript concepts and values, not for binary
formats like WebAssembly with arbitrary source languages, type systems, and a linear memory"* — and
the replacement was DWARF, an address-based format.

**Consequence: no VLQ, no `mappings` string, no `.map` sidecar shaped like a source map. The word
"source map" should not appear in the implementation.** A face→lines map is a plain
`number[][]` indexed by face ordinal; §5.5 sizes it at a mean 385 bytes per file.

### 4.2 Two integers, not a `loc` object — every high-performance implementation agrees

| System | Stored per node | Line/column |
|---|---|---|
| **ESTree** | `loc: {source, start:{line,column}, end:{line,column}}` — 3 heap objects | stored eagerly |
| **Babel** | ESTree `loc` **plus** flat `start`/`end`; `range` is opt-in | stored eagerly |
| **TypeScript** | 2 ints (`pos`, `end`) | derived on demand |
| **SWC** | 2 ints — `pub struct Span { pub lo: BytePos, pub hi: BytePos }` | derived via `SourceMap` |
| **Roslyn** | `TextSpan` = start + length, both 32-bit | derived |
| **rowan / rust-analyzer** | green node stores only `text_len`; absolute offset lives on the red facade | derived |
| **tree-sitter** | 2 byte offsets **+** 2 `TSPoint` (row, column) = 4×u32 | both stored |

ESTree's shape is normative for JS ASTs — *"Each `Position` object consists of a `line` number
(1-indexed) and a `column` number (0-indexed)"* — and **`range` is not in the ESTree spec at all**;
it is a parser add-on, confirmed absent from `es5.md`. Roslyn: *"A text position is represented as a
32-bit integer, which is a zero-based `char` index. A `TextSpan` object is the beginning position
and a count of characters, both represented as integers."* tree-sitter's columns are **bytes**, not
characters: *"`column` represents the number of bytes between the position and beginning of the
line."*

Roslyn and rowan store *lengths* rather than absolute offsets specifically so subtrees survive
edits; absolute-offset trees do not. ts-morph states the consequence bluntly: after a text edit
*"all previously navigated descendants of the node will be forgotten and not be available for
use—an error will be thrown if you try to use them."*

**Consequence for bikar, and it cuts against the mainstream:** bikar has no incremental reparse, no
editor integration that survives keystrokes, and — decisively — **no byte offsets anywhere in the
pipeline.** `Token` carries `line`/`column` and nothing else (`tokens.ts:190-195`); there is no
`SourceMap`-equivalent line-start table to derive line/column *from* an offset. Adopting
offsets would mean building that table, i.e. paying for the mainstream design's prerequisite
without its payoff. §5.2 therefore stores line/column and records the departure as a bet
(Appendix B.1).

### 4.3 Full-fidelity trees cost about 2×, and bikar does not need one

Roslyn is the reference implementation of the maximal position: *"Syntax trees hold all the source
information in full fidelity … every piece of information found in the source text, every
grammatical construct, every lexical token, and everything else in between including whitespace,
comments, and preprocessor directives"*, and *"A syntax tree obtained from the parser is completely
round-trippable back to the text it was parsed from."* rust-analyzer states the same property:
*"Syntax trees are lossless, or full fidelity. All comments and whitespace get preserved."*

The price is stated by the designer. Eric Lippert on red-green trees: *"The cost is that this system
is complex and can consume a lot of memory if the 'red' façades get large"*, and in the 2020
addendum, *"This scheme ends up creating up to twice as many small objects as a normal parse tree
would, and therefore a lot of collection pressure."* rust-analyzer's mitigation is interning:
*"To avoid allocating EVERY SINGLE TOKEN on the heap, syntax trees use interning."*

Roslyn's *trivia* design is the more transferable part, and it is cheaper than a CST: trivia are not
tree children, they hang off tokens. *"Because trivia are not part of the normal language syntax and
can appear anywhere between any two tokens, they are not included in the syntax tree as a child of a
node."* … *"In general, a token owns any trivia after it on the same line up to the next token. Any
trivia after that line is associated with the following token."* TypeScript copied the rule verbatim
(*"all trivia naturally precedes some non-trivia token, and resides between that token's 'full
start' and the 'token start'"*), and explicitly declines to store it — trivia is *"not stored in the
AST (to keep it lightweight)."*

The alternative — attach comments after the fact by heuristic — is Prettier's, and Prettier says it
does not work well: *"Turns out this is a really difficult problem. Prettier tries its best to keep
your comments roughly where they were, but it's no easy task because comments can be placed almost
anywhere."* Its `attach.js` classifies each comment as **ownLine** / **endOfLine** / **remaining**
and routes it to `addLeadingComment` / `addTrailingComment` / `addDanglingComment`, disambiguating
with a `breakTies` pass.

Two ecosystem data points on cost: Babel's `attachComment: false` *"can provide up to 30%
performance improvement when the input code has many comments"*; and `proc-macro2` gates byte
ranges behind an opt-in `span-locations` cargo feature, i.e. even *positions* are treated as a cost
to pay only on demand. tree-sitter takes the opposite line and makes comments grammar members:
extras are *"tokens that can appear anywhere in the grammar, without being explicitly mentioned in a
rule … useful for things like whitespace and comments."*

**Consequence: §5.4 takes Roslyn's cheap half (a comment list with positions, produced by the lexer
which already knows exactly where each comment is) and neither Roslyn's full-fidelity tree nor
Prettier's heuristic reattachment.** The corpus makes this unusually easy — see §5.4.

### 4.4 CascadeStudio — the mechanism is real, the feature is not the one being cited

`derivation-visualization-survey.md` §12.7 is accurate: *"CascadeStudio recovers the line from the
JS stack and drives Monaco `deltaDecorations`."* What compressed badly is the step from there to
`derivation-worksheet-design.md` §6's *"click-to-source … cheap"*. Reading the source shows the
survey is describing **step→source**, not **shape→source**, and CascadeStudio does not have the
latter.

The stack trick exists and its author's own comment prices it:

```js
/** Mega Brittle Line Number Finding algorithm for Handle Backpropagation;
 * only works in Chrome and FF. */
static getCallingLocation() {
  let errorStack = (new Error).stack;
  let matchingString = ", <anonymous>:";
  if (navigator.userAgent.includes("Chrom")) { … }
  else if (navigator.userAgent.includes("Moz")) { matchingString = "eval:"; }
  else { lineAndColumn[0] = "-1"; … }
```

(`packages/cascade-core/src/worker/StandardUtils.js:169-195`.) It works only because user code is
run through `eval()` in a worker, so the eval'd frame's line number *is* the editor line. On Safari
it returns `-1`.

It feeds exactly two things, and neither is picking a shape:

1. **The timeline scrubber.** `CacheOp` stamps every stdlib call
   (`StandardUtils.js:54`, `this.currentLineNumber = CascadeStudioUtils.getCallingLocation()[0]`)
   into `modelHistory`. The UI is a **strip of dots**, scrubbed with `mousedown`/`mousemove` on
   `this._timelineTrack` (`CascadeView.js:405-414`). Selecting a step calls
   `_onHistoryStepChange(lineNumber)` → `editor.deltaDecorations(…, [{ range: new
   monaco.Range(lineNumber,1,lineNumber,1), options: { isWholeLine: true, … } }])` +
   `revealLineInCenter` (`CascadeMain.js:370-386`). **The thing you click is a dot on a timeline,
   not a face.**
2. **Gizmo write-back.** `postMessage({type:"createTransformHandle", payload:{…, lineAndColumn}})`
   (`StandardLibrary.js:361`); `CascadeViewHandles.js:39-75` takes `lineAndColumn[0] - 1`,
   regex-replaces the `Transform(…)` call on that one line, and calls
   `window.monacoEditor.setValue(newCode)`. Line-oriented string surgery, not an AST edit.

**And picking is deliberately cosmetic.** `CascadeView.js:101,634-656` has a raycaster, but the only
mouse listener on the viewport is `mousemove` (`CascadeView.js:142`) — there is **no `click`
listener on `mainObject`** — and its payload is a white highlight plus a tooltip reading
`"Face Index: N"`. That face index is **never joined** to `modelHistory`'s line numbers.

**Consequence: the strongest-sounding precedent for "cheap click-to-source" does not implement
click-to-source.** It implements timeline-step→line, which is a fundamentally easier problem because
a step *is* a call and a call *has* one line. Editor is Monaco (`EditorManager.js:64`).

### 4.5 Zoo / KCL — the real precedent, and it says faces have no source

This is the one product that ships pick-a-face→highlight-source, and its own design doc states the
central problem of §3 in almost the same words. From `src/lang/std/artifactGraph-README.md`,
verbatim:

> "The artifact graph's primary role is to map geometry artifacts in the 3d-scene/engine, to the
> code/AST such that when the engine sends the FE an id of some piece of geometry (say because the
> user clicked on something) then we know both what it is, and how it relates to the user's code."

> "The extrude created a bunch of faces, edges etc, each of these relates back to the extrude
> command and the segment call expression, **but there's no direct bit of kcl to refer to.**"

> "the user hovers over a extrude wall-face, the engine sends us this id, we look it up in the
> graph, but **there's no pointer to the code in this node**. We can then traverse to both the
> segment and the extrude nodes to get source ranges for `line(...)` and `extrude(...)` and
> **highlight them both**."

Confirmed in the types — `Wall` carries no `code_ref`, only a differently-scoped `face_code_ref`
(`rust/kcl-api/src/artifact.rs:372-383`): *"This is for the sketch-on-face plane, not for the wall
itself. Traverse to the extrude and/or segment to get the wall's code_ref."*

Three transferable design facts:

- **The unit is a byte range plus a structural path, carried side by side.**
  `SourceRange([usize; 3])` — *"the start and end points (byte offsets from the start of the file).
  The third item is whether the source range belongs to the 'main' file"*
  (`rust/kcl-error/src/source_range.rs`) — and `CodeRef { range, node_path, path_to_node }`
  (`artifact.rs:29-36`). The flat range drives editor highlighting; the AST path drives code
  mutation. bikar needs only the first half in v1.
- **A pick returns a *set*, and they highlight all of it.** Same conclusion as §3.5, reached
  independently by a shipping product.
- **They needed an explicit tiebreak knob anyway.** `selections.ts:387` carries
  `codeRefLookup?: 'first' | 'last'`. §3.5 declined to pick a winner; Zoo's experience says a
  policy parameter eventually shows up regardless. Recorded as Q3.

Editor is **CodeMirror 6** (`selections.ts:2`, `import { EditorSelection } from
'@codemirror/state'`), with a first-party Lezer grammar package. Selection flows both ways
(`handleSelectionBatch` → `EditorSelection.create`, `selections.ts:1385-1397`; `codeToIdSelections`
at :1932 pushes highlights back to the engine), and drag→edit does a real AST mod plus `recast`
(`sceneEntities.ts:1395`) rather than CascadeStudio's regex.

**Could not verify:** `zoo.dev/docs/kcl-lang/index` returned 404, so there is no user-facing doc
quote — everything above is repo source, which is the stronger evidence anyway.

### 4.6 OpenSCAD ships this, and the way it ships it is the finding

**A premise carried into this work — that OpenSCAD has no jump-to-source — is wrong.** The
`OpenSCAD_User_Manual/The_OpenSCAD_User_Interface` wikibooks page describes only camera controls and
supports that impression; the page is out of date. The source says otherwise.

**Every AST node carries a mandatory span.** `src/core/AST.h`:

```cpp
class Location {
  Location(int firstLine, int firstCol, int lastLine, int lastCol, std::shared_ptr<fs::path> path)
};
class ASTNode {
  ASTNode(Location loc) : loc(std::move(loc)) {}
  const Location& location() const { return loc; }
protected: Location loc;
};
```

`ASTNode` has **no default constructor** — a `Location` is required, with `Location::NONE`
(`AST.cc:11`) as the explicit sentinel. Every console message is stamped with it via
`Location::toRelativeString` (`AST.cc`), which returns the literal string `"location unknown"` when
absent, appended by `printutils.h:96`.

**Picking is a GPU colour-ID buffer, not a raycast.** `MouseSelector.h`: *"Grab the of the Tree
element that was rendered at a specific location"* [sic]. `MouseSelector.cc:95-153` renders to an
offscreen FBO with an ID shader, then
`glReadPixels(…, GL_RGB, …); const int index = color[0] | (color[1]<<8) | (color[2]<<16);` — a
24-bit node index encoded as RGB. Exact, O(1), no CPU-side geometry.

**And the interaction is explicitly plural.** `MainWindow.cc:3745` binds `doRightClick` (left click
is the measurement tool). `rightClick` (:2126+) resolves the picked index to an **ancestor path**:

```cpp
const int index = this->qglview->pickObject(position);
std::deque<std::shared_ptr<const AbstractNode>> path;
const auto result = this->rootNode->getNodeByID(index, path);
```

and builds a context menu with **one entry per ancestor**, labelled `name (file.scad:LINE)` — or
`" (no source reference)"` (`:2165`) when the node has none. *Hovering* an entry calls `setSelection`
(`:2337-2345`), which opens the owning file, calls `setCursorPosition(line-1, column-1)` (`:2331`),
and marks **two tiers** of highlight: `SELECTED` for the picked node's own span, `IMPACTED` for
every node sharing its module (`findNodesWithSameMod`, `:2316-2323`), with a nesting `level`
assigned up the ancestor stack (`:2244-2267`).

**Consequence, and it is the sharpest one in this document.** OpenSCAD can do this because its
render tree is *isomorphic to its AST* — every `AbstractNode` both renders geometry and owns a
`Location`, so picking a pixel picks a node. Zoo cannot rely on that isomorphism, which is why it
needs an artifact graph with **ancestry edges** to traverse. **bikar has neither.** Faces are found
by an arrangement walk (§3.4); there is no node to pick and no ancestry to traverse — only a flat
`Set<string>` of tags on a `Face`. Both shipping implementations depend on a structure bikar does
not have, and §3's 38.9% is the numeric shadow of that absence. OpenSCAD's `SELECTED`/`IMPACTED`
two-tier answer to "this line ran 40 times" is the best UI idea found, and bikar **cannot implement
it** without inventing the ancestry OpenSCAD gets for free.

**CadQuery ecosystem — a claim examined and found false.** jupyter-cadquery's `replay.py` (676
lines) is often described as recovering source position via `inspect.stack()`. It does not:
**`inspect` is never imported.** The full import set is `traceback, dataclasses, typing, cadquery,
IPython, ipywidgets, ocp_tessellate, ocp_vscode, cad_viewer_widget`, and `traceback` appears only in
an exception handler. It monkeypatches `__getattribute__` on `cq.Workplane`/`cq.Sketch` to record
`{func, args, kwargs, obj, children}`, and the UI is a `SelectMultiple` of **synthesized** call
strings (`"%s%s%s" % ("| "*level, func, args)` → `box(10, 20) => _v1`). **No filename, no line
number, no source text** — this corroborates `derivation-visualization-survey.md` §12.8's ranking of
the monkey-patch as the most invasive and least informative mechanism. `ocp_vscode`'s "visual
debugging" shows CAD objects found in `locals()`, i.e. it names the *variable*. The Python CAD
ecosystem has no shape→source story at all; best-in-class there is a naming convention.

**Blender geometry nodes — no reverse mapping, as expected.** The manual's own source
(`manual/modeling/geometry_nodes/output/viewer.rst`): *"The Viewer node allows viewing data from
inside a geometry node group in both the Spreadsheet Editor and the 3D Viewport"*, driven by
*"`Shift-Ctrl-LMB` on any node or socket to connect it to the active viewer."* Strictly
node→viewport. Blender's answer to "which node made this?" is manual bisection — move the viewer
until the picture changes. (`docs.blender.org` itself returned 403; the manual source repo was used
instead.)

### 4.7 Editors, and whether LSP is the endgame

**Both editors can do the job; the gap is cost and model.**

| | CodeMirror 6 | Monaco |
|---|---|---|
| Range highlight | `Decoration.mark({class})` — *"influences the styling of the content in its range. Nested mark decorations will cause nested DOM elements to be created"* (`view/src/decoration.ts:224-231`); nesting order by facet precedence | `createDecorationsCollection(…)` (`monaco.d.ts:2807-2812`). **`editor.deltaDecorations` is deprecated** (`:6012-6017`, *"@deprecated Use `createDecorationsCollection`"*) — the call CascadeStudio still uses |
| Whole line | `Decoration.line` (`decoration.ts:260-262`) | `isWholeLine: true` |
| Reveal | `EditorView.scrollIntoView(pos)` — a transaction **effect** (`editorview.ts:889-892`) | `revealLineInCenter(lineNumber)` (`monaco.d.ts:2674-2678`) |
| Model | decorations are **derived state** recomputed from a `StateField` | decorations are **imperative handles you mutate** |
| Size (measured) | `codemirror@6.0.2` meta-package **373 kB raw / 119 kB gzip**, 7 deps | `min/vs/editor/editor.main.js` **3.77 MB raw / 950 kB gzip**, plus `loader.js` (30 kB) and `workerMain.js` (377 kB) |

The size numbers are ~8× gzip in CodeMirror's favour. Caveat stated: the Monaco figure is the
prebuilt AMD bundle with all languages; a tree-shaken ESM build with one custom language would be
materially smaller and **was not measured**. (CodeMirror figure from the bundlephobia API; Monaco
measured directly from unpkg with `wc -c` + `gzip -9`, because bundlephobia returned 429.)

For bikar the derived-state model is the better fit — a plural, per-render mapping is rebuilt
wholesale rather than diffed — and it is what Zoo, the only product shipping this feature, chose.
**None of which changes §5.5's finding that there is nothing to click.**

**LSP: the right frame for a different feature.** `Position` is `{line: uinteger, character:
uinteger}`, both zero-based, `Range` is two Positions, `Location` is `{uri, range}` (LSP 3.17). The
`character` offset is in **UTF-16 code units** by default — 3.17 added `PositionEncodingKind`
negotiation — with the spec's own example: *"in a string of the form `a𐐀b` the character offset of
`a` is 0, the character offset of `𐐀` is 1 and the character offset of b is 3."* Zoo sidesteps this
by using byte offsets internally and converting only at the editor boundary.

Two findings that settle the question:

1. **Direction.** `textDocument/definition`, `hover` and `documentSymbol` are all client-initiated;
   the spec states *"the lifecycle of a server is managed by the client."* There is no LSP concept
   of "a rendered mesh asks the editor to reveal a range." The one server→client primitive that
   fits is **`window/showDocument`**, whose `ShowDocumentParams` carries `uri`, `external`,
   `takeFocus` and an optional `selection` range (since 3.16). *(Direction, existence and field
   names verified; the per-field prose was truncated in the fetch, so it is not quoted.)*
2. **Precedent.** CAD-DSL language servers exist — `Leathong/openscad-LSP` (Rust; *"jump to
   definition"*, completion, hover signatures, document symbols, rename, topiary formatter) and
   KCL's own `rust/kcl-language-server` (*"a thin wrapper around the KCL language tooling
   library"*, shipped as a VS Code extension). **And Zoo ships both an LSP *and* an artifact graph —
   the artifact graph is not part of the LSP.**

**Consequence: LSP is not the endgame for click-to-source; it is an orthogonal, later concern that
happens to want the same `loc` field.** That is an argument for §7 Phase 1 and *not* an argument
for Phases 4–5.

---

## 5. The design

### 5.1 What is being built

Three separable artifacts, in dependency order:

1. **`loc` on statement and declaration nodes** (§5.2) — an `ast.ts` + `parser.ts` change.
2. **A face → source-lines map** (§5.3) — an `evaluator.ts` + `environment.ts` change plus a
   *new* carrier, deliberately not the existing tag channel.
3. **A surface that consumes it** (§5.5).

§9 concludes that (1) should be built, (2) should be built only as far as the worksheet needs, and
(3) should not be built yet.

### 5.2 Where spans live — `loc` on the node, attached at the two chokepoints

**Decision: an optional `loc?: SourceLoc` field on statement and declaration node types,
`{ line, column, endLine, endColumn }`, all 1-based, assigned in `parseStatement` and
`parseDeclaration`.**

| Option | Cost | Verdict |
|---|---|---|
| **`loc` on nodes, at the 2 chokepoints** | +9/−2 lines, 1 file; 1 interface in `ast.ts`; 99.6% coverage measured | **chosen** |
| `loc` on nodes, at all 101 construction sites | 101 edits in a 3,993-line file; buys sub-statement spans Goal 2 disclaims | rejected — pays 50× for granularity nobody asked for |
| **Side table keyed by node identity** (`WeakMap<ASTNode, SourceLoc>`) | ~0 edits to `ast.ts` | **rejected, and the reason is specific to this repo.** The worksheet's whole mechanism is `{ ...ast, declarations: prefix }` (`derivation-worksheet-design.md` §4.2), and this doc's own prototype does `{ ...node, loc }`. Object identity does not survive a spread. The worksheet doc's proposed **E4** gate asserts the AST is plain, cloneable data (§8.8) — a side table is exactly the thing E4 exists to protect, and it would break silently rather than loudly. |
| **Token-index ranges** (`{ startTok, endTok }`) | 2 sites, 2 ints — cheapest | rejected: resolving an index to a line requires shipping the `Token[]` alongside the AST, and the token array is mutated in place by `expandFor` (`parser.ts:3129`), so an index is not stable across parse. |
| **Byte offsets** (the TypeScript/SWC/Roslyn shape, §4.2) | 2 ints, mainstream | rejected: bikar has no byte offsets anywhere and no line-start table to derive line/column from one. All existing diagnostics are already line/column. Recorded as a bet — Appendix B.1. |

**Storage shape.** §4.2 says every performance-motivated implementation stores two integers.
bikar stores four numbers in one object. That is ESTree's shape, which §4.2 shows is the expensive
one — and it is chosen anyway, because the counts make the argument moot: **1,405 statement nodes
across 92 files.** ESTree's cost model is written for parsing multi-megabyte bundles; the entire
bikar corpus is 3,241 lines of `.bkr`.

**This breaks a scope-out and the break is deliberate.** `derivation-worksheet-design.md` §4.7
says *"No engine file is modified"* and §8.9 extends it: *"No `ast.ts` modification. Not source
spans…"*. This design requires both. The worksheet doc was right to scope them out — it did not
need them. **This doc needs them and says so rather than working around them**, because every
workaround examined (side table, token indices, re-lexing at query time) is worse than the 12-line
edit. Q11 is hereby answered: spans do require engine files, they are cheap, and the IR calculus of
§8.9 is unchanged because §8.2's consumer census is unchanged — nothing new crosses a process
boundary.

**One prerequisite.** §2.4(a) shows `column` is wrong on any line carrying a hex literal (283 lines,
75 files). `line`, `endLine` and statement-level use are unaffected. **`column`/`endColumn` must not
be consumed by anything until `preprocessSource` is made position-preserving** (pad the replacement
to equal length, or record a per-line delta). Recorded as V3 in §6 and Q1 in §8.

### 5.3 How face → statement provenance travels — a new channel, not `Segment.tags`

The obvious implementation is the one §3.1's prototype used: push `src:<line>` into the existing
tag list, since it already flows `Segment.tags` → `Face.sources` → `svg-renderer` for free, exactly
as `layer:N` and `wave:N` do.

**It was measured, and it silently corrupts an ACCEPTED cross-repo contract attribute.**

`resolveShapeId` (`svg-renderer.ts:280-290`) resolves `data-shape-id` from the face's source tags
after filtering through `isNamedShapeTag` (`svg-renderer.ts:308-326`), which is an **exclusion
list**: a tag is a "named shape" unless it starts with `layer:` / `rotate:` / `boundary:` / `line:`
/ `.`, or matches `/:#\d/`, or is one of the girih role constants. A `src:` tag matches none of
those, so it is treated as the author's chosen shape name.

Measured across the corpus, stock `packages/core/dist` versus the prototype bundle, identical
inputs:

```
STOCK   92 files   5,286 faces   data-shape-id emitted on   734 faces
PROTO   92 files   5,286 faces   data-shape-id emitted on 1,788 faces      (+1,054, +143.6%)
```

and on `Flower-of-Life.bkr` the emitted values are, verbatim:

```
{"src:15": 7}
```

**`data-shape-id="src:15"` — a source line number shipped as a shape identity, into an attribute
qiyas reads as ground truth.** The failure is not a crash; it is 1,054 faces gaining a plausible-
looking wrong value.

Fixing it by extending `isNamedShapeTag` costs **three mirrored edits, not one**:
`svg-renderer.ts:308`, its explicit mirror `gt-emitter.ts:1219` (*"Mirrors `isNamedShapeTag` in
svg-renderer.ts (bikar#664)"*), and the `uncovered_shapes` computation at `gt-emitter.ts:816`,
which uses the same predicate to decide which authored shapes left no trace. Miss any one and the
gt.json contract shifts under qiyas.

**Decision: face→statement provenance does not ride `Segment.tags`. It travels on a dedicated
parallel field.**

| Option | Verdict |
|---|---|
| `src:<line>` in `Segment.tags` | **rejected — measured to corrupt `data-shape-id` on 1,054 faces (+143.6%)**, and even correctly filtered it puts a rendering concern inside a contract-governed identity channel that three call sites already have to agree about. It also inflates gt.json `source_primitives`, a published multiset. |
| A new `Segment.srcLines?: readonly number[]` + `Face.srcLines?` | **chosen.** Parallel to the existing `sources` / `edgeSources` pair (`half-edge.ts:46,59`), invisible to `isNamedShapeTag`, invisible to gt.json unless deliberately added. Cost: one field on `primitives/types.ts:25` `Segment`, one on `Face`, one merge line in `face-extractor.ts` beside the existing `sourcesSet.add(tag)` at `:29`. |
| Recompute at query time from the AST | rejected: face identity is not recoverable from the AST — that is the whole finding of `derivation-worksheet-design.md` §3.1. |

**The arc channel must be threaded too**, or petals have no answer (§3.3): 6 sites at
`evaluator.ts:3774, 4554, 4679, 4716, 4849, 4878`. Costed here, not hidden.

**Running total for the full feature:** 2 hunks (parser) + 1 interface (ast) + 1 field + 1 wrapper
(evaluator/environment) + 2 fields + 1 merge (primitives/graph) + 6 arc sites + 1 emit site
(renderer) ≈ **14 edit sites across 7 engine files.** Not enormous; not the "cheap" of the
worksheet doc's §6 either.

### 5.4 Comment retention — a separate decision, and the cheaper one

This is orthogonal to spans and must be decided separately, because it has its own cost and its own
payoff.

**The corpus fact that decides it:** across all 92 files, **812 comment lines** out of **3,241 total
lines — 25.1% of the corpus is comments** — and

```
own-line comments:   812   (100%)
trailing comments:     0   (0%)
```

**Zero trailing comments.** Prettier's three-way classification (§4.3) collapses to its first case,
which Prettier itself resolves without ambiguity — an own-line comment *"prefer[s] a leading
comment."* The hard part of comment attachment, which Prettier calls *"a really difficult problem,"*
is **absent from this corpus by construction**. Roslyn's same-line ownership rule
(*"a token owns any trivia after it on the same line up to the next token"*) has no work to do
either.

269 of the 812 lines sit inside a `# Construction:` block, across the 31 files that have one.

**Decision: the lexer emits comments into a side list on `FileNode` — `comments?: readonly
{ line: number; column: number; text: string }[]` — ordered by position. Comments are *not* attached
to nodes, and `Token[]` is *not* changed.**

| Option | Verdict |
|---|---|
| **Side list on `FileNode`** | **chosen.** `consumeComment` (`lexer.ts:86-90`) already computes the exact start position and consumes to end-of-line; it discards instead of pushing. The change is ~4 lines. Nothing downstream sees a new token type, so the 39-entry statement table, `parseStatement`, and every existing test are untouched. Attachment ("which statement does this comment introduce?") becomes a pure function over `comments` + statement `loc`, computable by any consumer, testable in isolation, and **not baked into the AST** where a wrong guess would be permanent. |
| **Comment tokens in the stream** (tree-sitter's `extras` shape) | rejected: every `peek()`/`expect()` path in a 3,993-line hand-rolled parser would have to skip them, including the **column-sensitive** body terminators — `parseRepeat` reads `this.peek().column` to detect dedent (`parser.ts:3132-3160`), and `expandFor` captures body tokens by comparing `t.column <= forCol`. A comment token at column 1 inside an indented body would terminate the block. This is the change most likely to break parsing in a way tests would not obviously localize. |
| **Comments attached to nodes at parse time** (Roslyn/TypeScript trivia) | rejected: it is the right design for a compiler that must round-trip source, and bikar has no printer at all — a grep for `unparse` / `printAST` / `toSource` / `astToSource` / `formatBkr` across `packages/*/src` returns one false positive (`render/svg-utils.ts:202`, the word "unparseable"). Paying for full fidelity with no consumer for it repeats the mistake `derivation-worksheet-design.md` §8 declined. |
| **Do nothing; keep discarding** | rejected — see the payoff below. |

**The payoff, and it is the strongest single argument in this document.** The worksheet doc's
**B.4** is its most honestly unresolved bet: a mechanical prefix walk *"recovers the sequence the
file literally specifies, which is not necessarily the sequence a teacher would choose,"* and *"no
validator in §5 catches it."* Its §3.6b finding is that **node labelling is the universal weak point
across every tool surveyed** — CQ-editor labels a step with plane-origin coordinates, jupyter-cadquery
with `func(args) => _v1`, OpenSCAD with `cube1`.

The corpus already contains hand-written editorial labels for exactly these steps. From
`bikar/patterns/Petal Tutorial/Petal-Full.bkr:14-19`, verbatim:

```
# Construction:
# 1. Central circle C0 divided into 6 (depth-2 repeat builds ring-1 + ring-2)
# 2. Intersect C0 with each ring-1 circle -> X-points (6 pairs)
# 3. Intersect adjacent ring-1 circles -> Y-points (6 pairs)
# 4. layer 0: X-petal arcs (inner arc on C0 + outer arc on ring-1 circle)
```

**That is a worksheet caption track, written by hand, sitting in the file, thrown away at
`lexer.ts:88`.** Retrieving it costs four lines in the lexer and answers the labelling problem that
§3.6b says nobody solved. This is independent of click-to-source and would be worth doing if
click-to-source were abandoned entirely — which §9 is close to recommending.

**Two costs, stated:** (a) the hex-preprocessing interaction — `preprocessSource` runs *before*
`tokenize`, so a retained comment's `column` inherits §2.4(a)'s drift and its `text` is read from the
rewritten string; comments must be captured from the **original** source or the preprocessing made
position-preserving. (b) `FileNode` gains a field, so the worksheet doc's §8.1 round-trip and §8.8
E4 fixtures both grow — additively, and both are already written to compare serialized forms.

### 5.5 Delivery surface — and the finding that there is no v1 surface

Three candidates were checked in the tree rather than assumed.

| Surface | State today | Verdict |
|---|---|---|
| **Static SVG `data-*`** | `renderSVG` emits 20+ `data-*` attributes (`svg-renderer.ts:395-451`). The 40 SVGs in `3d-models/` are inert markup; **no click handler exists anywhere in either repo.** | Possible but inert. Adding `data-src-lines` to an SVG nobody has wired a listener to ships a payload with no reader — the exact failure `data-shape-id` already recorded (producer-side ACCEPTED, use-case FALSIFIED). |
| **The derivation worksheet** | Not implemented. Its §4.4 item 5 requires *"a text label naming the operation, derived from the source statement node kind plus its salient arguments."* | **The one real consumer.** With `loc`, the label can be the author's own line instead of a synthesized paraphrase; with §5.4, the section header can be the author's own `# Construction:` step. Neither requires a click. |
| **The Lab** (`packages/lab`) | Editor is a **plain `<textarea>` with a line-number gutter** — `editor.ts:2-4`, verbatim: *"a plain `<textarea>` with a line-number gutter — no CodeMirror/Monaco, per the no-new-deps constraint."* Wired at `main.ts:242` (`#code-editor`). **The Lab does not render the 2D pattern SVG at all** — its stage is a 3D orb mesh plus orb *axis-view* SVGs (`main.ts:469`, `axisViewEl.innerHTML = view.svg`), and per-view gt deliberately emits null identity (contract, orb-view rows). Evaluation runs in a Web Worker (`worker.ts`) that receives **source text** and returns meshes and SVG strings (`protocol.ts`). | **There is nothing in the Lab to click.** The faces with provenance are not on screen. |

**Decision: v1 has no interactive click surface, because none exists to build on. The v1 consumer
is the derivation worksheet's labels, and it consumes `loc` and comments — not a face→line map.**

Two secondary notes for whoever revisits this:

- **A `<textarea>` can do the editor half.** `setSelectionRange` + `scrollTop` will select and
  reveal a line range natively — no decoration API, no dependency. What a textarea cannot do is
  *multiple* simultaneous ranges, which §3.5's plural answer requires. **That is a real argument
  for an editor swap, and it is the only one this design found.**
- **Sizing, if a map is ever emitted.** Measured over the corpus: a face→lines sidecar is
  **35,398 bytes total, mean 385 bytes/file**; inline `data-src-lines` attributes are
  **113,852 bytes total, mean 1,238 bytes/file, +3.46% on SVG size**. Cost is not the obstacle.

### 5.6 Interaction with the `data-*` contract

**Decision: this design proposes no new `data-*` attribute in v1.**

If §7 Phase 4 ever fires, `data-src-lines` would enter `bikar/docs/dsl-metadata-contract.md` as
**PROPOSED**, per that document's governance, with the use case stated so it can be falsified the
way `data-shape-id`'s was. It would carry three unusual properties that the row must state:

1. **Plural by design** (§3.5) — unlike every existing row, which is scalar-or-omitted.
2. **Not an identity.** It is a navigation hint. It must be excluded from `isNamedShapeTag` on both
   sides (`svg-renderer.ts:308`, `gt-emitter.ts:1219`) and from `uncovered_shapes`
   (`gt-emitter.ts:816`) — §5.3 measured what happens otherwise.
3. **Deliberately absent from gt.json.** qiyas validates *geometry*; a line number is not evidence
   about a pattern. Adding it would bump `GT_SCHEMA_VERSION` for a field with no consumer.

**No canonical amendment is sought.** The canonical contract lives in
`sacred-patterns/docs/dsl-metadata-contract.md` and the bikar copy is a mirror; nothing here reaches
that far.

### 5.7 Scope-outs, stated explicitly

- **No expression-level spans** (§2.2: 101 sites). `where` predicates, numeric expressions, palette
  entries and style rules — the 34.2% of nodes outside the chokepoints — get the enclosing
  statement's span or nothing.
- **No `column` consumers** until §2.4(a) is fixed. Line-granular only.
- **No AST → `.bkr` printer.** None exists; none is added.
- **No incremental reparse, no red/green tree, no CST.** §4.3 prices full fidelity at ~2× object
  count for properties (persistence, cheap parent access) nothing here needs.
- **No editor dependency.** CodeMirror and Monaco are both out under the Lab's stated no-new-deps
  constraint (`editor.ts:3`); revisiting that is a Lab decision, not this one.
- **No bidirectional edit.**
- **No 3D.** `piece` / `wall` / `orb` provenance is a result descriptor, not a trace
  (`derivation-worksheet-design.md` §2.3), and per-view orb gt deliberately emits null identity.
- **No claim on the parser's architecture.** See §8 Q7 — this design is neutral on the
  grammar-formalization question, but not independent of it.

---

## 6. Validators and failure modes

Nothing is fabricated here, so there is no manifold gate — but spans can be wrong in checkable ways,
and a wrong span is worse than no span (Goal 1).

| # | Failure | Detection | Response |
|---|---|---|---|
| V1 | A statement node has no `loc` | walk the corpus AST | **Gate.** Measured floor is 1,400/1,405; assert it, and assert the 5 known misses by name so a *sixth* is a diff. |
| V2 | A `loc` points at a blank or comment-only line | resolve `loc.line` against the source text | **Gate.** Measured 0/1,400; any nonzero is a parser bug. This is the cheapest real correctness check available and it caught nothing, which is the point. |
| V3 | `column` consumed anywhere | grep / type-level | **Gate until Q1 closes.** §2.4(a) — 283 lines in 75 files carry the drift. |
| V4 | `data-shape-id` count changes | corpus diff vs the 734 baseline | **Gate.** §5.3 measured a naive implementation at 1,788 (+143.6%). Any drift means the provenance channel leaked. |
| V5 | gt.json `source_primitives` multiset changes | existing witness tests | Already gated by the contract's witness convention; named here so the interaction is not discovered late. |
| V6 | A face resolves to zero lines | count during emit | Report the count against the §3.2 baseline of **131 (2.4%)**. Not a failure — an inventory. Should fall toward 0 when the arc channel is threaded (§3.3). |
| V7 | A face resolves to >4 lines | count during emit | Warn. Measured max is 4; a jump means a new construction shape the §3.5 promise was not sized for. |
| V8 | `loc` survives the worksheet's prefix spread | E4-style plain-data assertion | `{ ...ast, declarations: prefix }` copies `loc` by value. Asserting it keeps §5.2's rejection of the side-table option honest. |

**Enforcement classes**, following `derivation-worksheet-design.md` §5.1's discipline: **V1–V4 are
gates**, V5 rides an existing gate, V6–V8 are counts and warnings. All ride the existing
`npm test` → pre-commit → CI chain. **No new hook.** If a hook is ever wanted, extend
bikar's `.claude/hooks/check-bkr-mesh.py` as §5.1 argues, rather than adding a second convention.

**What cannot be enforced.** No gate can check that the line a face points at is the line a *reader*
would have expected. §3 establishes the relationship is many-to-many; the feature can be provably
faithful to the evaluator's tagging and still surprise. That is a documentation problem, not a test
problem, and §3.5's "always a set" framing is the only mitigation on offer.

---

## 7. Phasing

Commit-sized, and **trigger-gated after Phase 2** — later phases are unlocked by a named event, not
scheduled. Nothing below is implemented.

| Phase | Trigger | What it is |
|---|---|---|
| **1 — spans** | unconditional | The §2.3 patch: `SourceLoc` in `ast.ts`, 2 hunks in `parser.ts`, plus the third hunk for the 5 `PieceConstructorNode` misses. Tests: V1, V2, V8 as corpus fixtures. **No consumer yet — this phase is worth landing on the strength of better diagnostics alone.** |
| **1b — column fix** | with or before any `column` consumer | Make `preprocessSource` position-preserving (pad `__hex_` to the original width, or track a per-line delta). Test: the §2.4(a) reproduction, asserting the reported column equals the true column on a hex-bearing line. |
| **2 — comments** | unconditional; independent of 1 | `FileNode.comments` from `lexer.ts` (~4 lines), captured against the original source. Test: 812 comments across the corpus, 100% own-line, 269 inside `# Construction:` blocks. |
| **3 — worksheet consumption** | when the worksheet reaches its Phase 3 | Panel labels use the author's own source line; section headers use `# Construction:` steps. **This is where phases 1 and 2 pay off, and it involves no click.** |
| **4 — face→line map** | when a surface exists that can *display* a plural answer | The §5.3 dedicated channel, the 6 arc sites, `data-src-lines` PROPOSED in the contract mirror. Gates V4–V7. |
| **5 — interaction** | when the Lab renders 2D pattern SVG **and** has a multi-range-capable editor | Click handler; multi-line highlight; "3 statements contributed to this face" affordance. |
| **never unless separately justified** | — | Expression-level spans; a CST; an AST printer; bidirectional edit. |

Phases 4 and 5 have **not fired and there is no evidence they will soon** — §5.5 found no surface.
That is the finding, not a scheduling accident.

---

## 8. Open questions

**Q1. Can `preprocessSource` be made position-preserving without breaking the hex round-trip?**
The rewrite is `#RRGGBB` → `__hex_RRGGBB` (+5 chars) and the reverse post-pass keys on the
`__hex_` prefix (`lexer.ts:336-341`). A same-length marker needs a 1-char sentinel the lexer can
scan as an identifier start, which `IDENT_START_RE = /[a-zA-Z_]/` (`lexer.ts:30`) constrains.
*Resolved by:* attempting the substitution and re-running the §2.4(a) reproduction. **Until this
closes, `column` is unusable and V3 stands.**

**Q2. Does threading the 6 arc sites actually take the 131 zero-answer faces to zero?**
§3.3 assumes it does; the arc path also carries its own tagging (`evaluator.ts:1077` emits
`<circle>:arc:#<n>`), so some arc faces may already be reachable by a different route.
*Resolved by:* extending the prototype to the 6 sites and re-running §3.2's histogram.

**Q3. Is "always a set" right, or is 38.9% unique enough to justify a primary line?**
§3.5 decided against ranking, but that decision was made on distribution shape alone, with no user
sitting in front of it. *Resolved by:* rendering the same face's answer both ways once a surface
exists. **Not resolvable in the abstract, and deliberately not resolved here.**

**Q4. Do statement spans change the IR calculus of `derivation-worksheet-design.md` §8?**
The answer this doc reaches is **no**: §8.2's consumer census is unchanged, because `loc` and
`comments` are consumed in-process by a worksheet builder that already holds a typed `FileNode`.
Q11 speculated that *"spans are the first AST content a second process would want"* — plausible, but
§5.5 found the second process (the Lab worker) receives **source text**, not an AST
(`lab/src/evaluate.ts:230`, `protocol.ts`), so it can parse spans itself. §8.9's Phase 1 trigger
does not fire. *Resolved by:* re-checking if anything ever ships an AST across a boundary.

**Q5. Does `loc` on nodes break the AST's plain-data property?**
It should not — four numbers in a plain object. But the worksheet's E4 asserts *"no classes, Maps,
Sets, Dates, RegExps, functions or cycles"* and *"`JSON.stringify` is a fixpoint after one pass"*
over 55,701 nodes, and the prototype adds ~1,405 objects per corpus pass. *Resolved by:* running
E4's assertion against a span-carrying AST. **Cheap and not yet done.**

**Q6. What is the right answer for `tileBlock` and `rotate`/`mirror` bodies?**
`tileBlock` appears 10 times in the corpus and is **outside** the chokepoint coverage (§2.3), which
is the same limitation `derivation-worksheet-design.md` §2.6.3 calls *"the single largest honest
limitation"* of its own mechanism. Two designs hit the same wall from opposite sides, which is
evidence the wall is structural. *Resolved by:* whichever design touches it first.

**Q7. Does this design depend on the parser-architecture question?**
**Yes, and the dependency is asymmetric — see §8.1 below.**

**Q8. Does the worksheet's `--format worksheet` want the source line, the statement text, or both?**
§5.4's payoff assumes "the author's own line" reads better than a synthesized label, which is
Kurlander & Feiner's requirement met the cheap way. It might read worse — source lines contain
syntax, not prose. *Resolved by:* rendering a sample sheet both ways. Same shape as the worksheet
doc's own Q8.

**Q9. Does a new doc plus a new engine field need a use-case map entry?**
This repo's `.githooks/pre-commit.d/20-use-cases` blocks pointer-file commits without a map update.
*Resolved by:* reading `.claude/skills/maintain-use-cases` before the first commit that touches the
map. **Not resolved here, because this doc is not being committed.**

### 8.1 Dependency on the grammar-formalization question — flagged, not resolved

A parallel design pass owns the question of whether bikar's DSL should have a formal grammar
(BNF/EBNF) and whether the hand-rolled recursive-descent parser should be replaced or merely
specified. That work owns `dsl-grammar-formalization.md`. This document does not attempt to resolve
it, and states the dependency in both directions:

**What this design assumes about the parser, and would lose if it changed:**

- The two chokepoints (`parseStatement`, `parseDeclaration`) exist *because* the parser is
  hand-rolled with handler tables. §2.3's 12-line result is a property of that architecture, not of
  parsers in general.
- `expandFor`'s token-splice macro (§2.4b) is a hand-rolled-parser artifact. A grammar-generated
  parser would have to express `for` some other way, which would change what a span on an unrolled
  statement means.
- §5.4's rejection of comment-tokens-in-stream rests on the parser's **column-sensitive** block
  termination (`parser.ts:3132-3160`, `:3105-3115`). Indentation-sensitivity is exactly the feature
  that is hard to express in BNF, so it is likely to be contested by the parallel work.

**What a parser change would offer this design:**

- **tree-sitter would supply spans and comments for free** — byte offsets plus `TSPoint` row/column
  on every node (§4.2), comments as grammar `extras` (§4.3), plus error tolerance and incremental
  reparse. If bikar adopted tree-sitter, Phases 1, 1b and 2 of §7 would be **subsumed**, not merely
  helped.
- Conversely, **if the parser stays as it is, §2.3's measurement stands and this design is cheap.**

**The honest statement of the dependency: this design is cheap if the parser stays, and redundant if
the parser is replaced by a CST-producing generator.** It is *not* a reason to delay either — Phase
1 is 12 lines and Phase 2 is 4, and both are throwaway-cheap if a grammar rewrite later subsumes
them. **Reconciling the two documents is a job for whoever reads both; this doc does not claim the
answer.**

---

## 9. Verdict

**Click-to-source, as commissioned — click a shape, land on the line that made it — should not be
built.** Not because it is expensive, and not because it is impossible. Because:

1. **It cannot honestly promise what its name promises.** 38.9% of faces resolve to one line;
   58.7% to two-to-four; 2.4% to none. One statement produces a median of 17 faces, and exactly one
   statement in the whole corpus produces exactly one face. "The line that made this shape" describes
   a relationship that occurs 1 time in 186.
2. **There is nothing to click.** No click handler exists in either repo. The Lab's stage is a 3D
   orb mesh and orb axis views — the 2D pattern faces that carry provenance are **not on screen**,
   and its editor is a `<textarea>` that cannot show more than one highlighted range, which is
   precisely what an honest plural answer requires.
3. **The naive implementation silently corrupts a live cross-repo contract** — measured, 1,054 faces
   gaining `data-shape-id="src:15"`.

**What should be built is the part underneath it, and it is small:**

- **`loc` on statement and declaration nodes** — `+9/−2` lines at 2 sites, measured at 99.6%
  coverage with 0 mispointings and 92/92 files still evaluating. It pays for itself in diagnostics
  alone, and it makes every later question (worksheet labels, an eventual language server, a
  face→line map if a surface ever appears) a small change instead of a large one.
- **Comment retention** — ~4 lines in `lexer.ts`, recovering **25.1% of the corpus** that is
  currently discarded at `lexer.ts:88`, including 269 lines of hand-written `# Construction:` steps
  across 31 files. This is the highest value-per-line change identified anywhere in this
  investigation, and it has **nothing to do with click-to-source.** It answers the worksheet doc's
  §3.6b ("node labelling is the universal weak point") and softens its B.4 (the mechanical walk
  cannot reproduce editorial judgment) — because the editorial judgment is *already written down in
  the file* and the compiler is throwing it away.

**Q11 is answered:** click-to-source does require source spans in the AST; the spans are cheap and
the *feature* is not; and the IR calculus of §8 is unchanged, because nothing new crosses a process
boundary (§8.1 / Q4).

**The structural reason, stated once.** Both products that ship this feature depend on a structure
bikar does not have. OpenSCAD picks a *node* because its render tree is isomorphic to its AST —
every `AbstractNode` renders geometry and carries a mandatory `Location` (§4.6). Zoo, whose
geometry is derived and therefore *not* isomorphic, needs an artifact graph with ancestry edges to
traverse, and says outright that a wall face has *"no direct bit of kcl to refer to"* (§4.5).
bikar's faces are derived like Zoo's, but bikar has no ancestry to traverse — a `Face` carries a
flat `Set<string>` (`half-edge.ts:46`) and nothing else. **§3's 38.9% is that missing structure
expressed as a number.** Building click-to-source properly does not mean adding spans; it means
building the artifact graph, and that is a different project than the one this doc was asked to
scope.

**One reframing, correctly bounded.** It is tempting to say the endgame is a language server. §4.7
says no, on the evidence: LSP requests are client-initiated, there is no "the render asks the editor
to reveal a range" (only `window/showDocument` comes close), and **Zoo ships an LSP *and* an
artifact graph as separate things — the shape→source map is not part of the LSP.** So an eventual
`.bkr` language server is a genuine, independently valuable use of §5.2's `loc` and §5.4's
comments — and it is *another* reason to build Phase 1, not a reason to build Phases 4–5. The two
features share a field and nothing else.

---

## Appendix A — sources

All URLs below were fetched during this work (some by a delegated research pass, whose fetched
copies were re-checked locally against the quotations used here). Quotations are verbatim from the
fetched text. Fetch failures are listed at the end so the gaps are visible rather than papered over.

**Specs**

- Source Map format (ECMA-426 / Source Map Revision 3) — https://tc39.es/ecma426/ · https://sourcemaps.info/spec.html
- Language Server Protocol Specification 3.17 — https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/
- ESTree spec, `Position` / `SourceLocation` — https://github.com/estree/estree/blob/master/es5.md
- Debugging WebAssembly with modern tools (why source maps were left behind) — https://developer.chrome.com/blog/wasm-debugging-2020

**AST positions and CST/trivia**

- Babel parser options (`ranges`, `attachComment`, `startLine`) — https://babeljs.io/docs/babel-parser
- SWC `Span` / `BytePos` — https://rustdoc.swc.rs/swc_common/struct.Span.html
- Roslyn "Work with syntax" / syntax API overview (full fidelity, `TextSpan`, trivia ownership) — https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/work-with-syntax
- Eric Lippert, "Persistence, Facades and Roslyn's Red-Green Trees" — https://learn.microsoft.com/en-us/archive/blogs/ericlippert/persistence-facades-and-roslyns-red-green-trees
- rust-analyzer syntax architecture (lossless trees, interning) — https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/syntax.md
- TypeScript compiler internals on trivia — https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API and https://basarat.gitbook.io/typescript/overview/ast/ast-trivia
- ts-morph on node invalidation after edits — https://ts-morph.com/manipulation/
- tree-sitter: `TSPoint`/byte offsets and `extras` — https://tree-sitter.github.io/tree-sitter/using-parsers · https://tree-sitter.github.io/tree-sitter/creating-parsers
- Prettier on comment attachment — https://prettier.io/docs/rationale · https://github.com/prettier/prettier/blob/main/src/main/comments/attach.js
- `proc-macro2` `span-locations` feature — https://docs.rs/proc-macro2/latest/proc_macro2/struct.Span.html

**CAD / geometry-DSL prior art**

- CascadeStudio — https://github.com/zalo/CascadeStudio
  - `getCallingLocation` — https://raw.githubusercontent.com/zalo/CascadeStudio/master/packages/cascade-core/src/worker/StandardUtils.js
  - timeline UI + raycaster — https://raw.githubusercontent.com/zalo/CascadeStudio/master/packages/cascade-studio/src/CascadeView.js
  - Monaco decorations — https://raw.githubusercontent.com/zalo/CascadeStudio/master/packages/cascade-studio/src/CascadeMain.js
  - gizmo write-back — .../CascadeViewHandles.js · stdlib `createTransformHandle` — .../StandardLibrary.js · editor — .../EditorManager.js
- Zoo / KittyCAD modeling-app
  - artifact graph design doc — https://raw.githubusercontent.com/KittyCAD/modeling-app/main/src/lang/std/artifactGraph-README.md
  - `SourceRange` — https://raw.githubusercontent.com/KittyCAD/modeling-app/main/rust/kcl-error/src/source_range.rs
  - `CodeRef` / `Wall` — https://raw.githubusercontent.com/KittyCAD/modeling-app/main/rust/kcl-api/src/artifact.rs
  - selection plumbing — .../src/lib/selections.ts · drag→AST-mod — .../src/clientSideScene/sceneEntities.ts
  - KCL language server — https://github.com/KittyCAD/modeling-app/tree/main/rust/kcl-language-server
- OpenSCAD
  - `Location` / `ASTNode` — https://raw.githubusercontent.com/openscad/openscad/master/src/core/AST.h · .../src/core/AST.cc
  - colour-ID picking — https://raw.githubusercontent.com/openscad/openscad/master/src/gui/MouseSelector.h · .../MouseSelector.cc
  - right-click → ancestor menu → `SELECTED`/`IMPACTED` — https://raw.githubusercontent.com/openscad/openscad/master/src/gui/MainWindow.cc
  - message stamping — .../src/utils/printutils.h
  - GUI manual (out of date re: source navigation) — https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_User_Interface
  - openscad-LSP — https://github.com/Leathong/openscad-LSP
- jupyter-cadquery `replay.py` — https://raw.githubusercontent.com/bernhard-42/jupyter-cadquery/master/jupyter_cadquery/replay.py
- ocp-cad-viewer — https://github.com/bernhard-42/vscode-ocp-cad-viewer
- Blender Viewer node (manual source) — https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/modeling/geometry_nodes/output/viewer.rst

**Editors**

- CodeMirror 6 decorations — https://raw.githubusercontent.com/codemirror/view/main/src/decoration.ts · https://raw.githubusercontent.com/codemirror/view/main/src/editorview.ts · https://codemirror.net/examples/decoration/
- Monaco type definitions — https://unpkg.com/monaco-editor@0.52.2/monaco.d.ts
- Bundle sizes — https://bundlephobia.com/api/size?package=codemirror@6.0.2 ; Monaco measured directly from https://unpkg.com/monaco-editor@0.52.2/min/vs/editor/editor.main.js

**In-repo**

- `bikar/docs/dsl-metadata-contract.md` · `bikar/docs/architecture.md`
- `docs/derivation-worksheet-design.md` · `docs/research/derivation-visualization-survey.md`

**Fetches that failed, and what was used instead**

| Target | Result | Substitute |
|---|---|---|
| `zoo.dev/docs/kcl-lang/index` | 404 | repo source (`artifactGraph-README.md`, Rust types) |
| Monaco typedoc HTML pages | 404 (both) | shipped `monaco.d.ts` for the pinned version |
| `docs.blender.org` (`/latest/`, `/4.2/`) | 403 ×2 | `blender-manual` repo `.rst` source |
| `codemirror.net/docs/ref/` | fetched but truncated before the `view` section | upstream `.ts` source |
| bundlephobia for `monaco-editor` | 429 | measured the artifacts directly |
| `kcl-lib/src/source_range.rs` | 404 (moved) | `rust/kcl-error/src/source_range.rs` |
| GitHub issue search for an OpenSCAD jump-to-source request | nothing relevant; WebSearch budget exhausted | moot — the feature is implemented |

**Explicitly unverified claims, flagged in place**

- §4.1's "a source-map segment maps one generated position to at most one source position" is
  *inference from the field grammar*; no spec sentence states it.
- §2.4(a)'s newline-spanning `preprocessSource` regex hazard is inspection-only; not reproduced.
- §4.7's `window/showDocument` field prose was truncated in the fetch; direction, existence and
  field names are verified, the wording is not quoted.
- §4.7's Monaco size is the all-languages AMD bundle; a tree-shaken ESM build was not measured.
- The measured `mAP` figures and E1–E4 gate definitions referenced from
  `derivation-worksheet-design.md` are that document's, not re-measured here.

---

## Appendix B — contested bets and why they stand

**B.1 — Storing `{line, column}` when every serious implementation stores byte offsets.**
§4.2 is unanimous: TypeScript, SWC, Roslyn and rowan all store two integers and derive line/column
on demand, and Zoo uses byte offsets internally, converting only at the editor boundary (§4.5).
This design stores four numbers per node instead. **The bet:** bikar has no byte offsets anywhere,
no line-start table to derive from, and every existing diagnostic (`ParseError`, `LexerError`) is
already line/column — so adopting offsets means building the mainstream design's prerequisite
without its payoff (incremental reparse, which bikar has no use for). **What would falsify it:** an
incremental-reparse requirement, a UTF-16-vs-bytes correctness bug (LSP's `a𐐀b` case, §4.7), or a
corpus large enough for 1,405 objects to matter. None is close.

**B.2 — Answering with a set, where the house rule is to omit when ambiguous.**
`dsl-metadata-contract.md` establishes that a face's attribute is *"omitted … never guessed"* when
its bounding edges disagree, and §3.5 deliberately departs from it. **The bet:** omission is right
for *identity* claims, where a wrong id poisons a downstream classifier — which is exactly how
`data-shape-id`'s use case got FALSIFIED. Navigation is not identity; two candidate places to look
beats zero. **Corroboration arrived from outside:** both shipping implementations return sets —
Zoo highlights `line(...)` **and** `extrude(...)` together, OpenSCAD offers the whole ancestor chain
as a menu. **What would falsify it:** a user study, or Q3's side-by-side. **What weakens it:** Zoo
still needed a `'first' | 'last'` tiebreak knob (`selections.ts:387`), which suggests "always a set"
is not the final answer, only the honest first one.

**B.3 — Concluding "do not build it" while two products demonstrably ship it.**
The strongest counter-evidence in this document is §4.6: OpenSCAD has had pick→source since before
this question was asked. **The bet:** the two shipping implementations rest on structures bikar
lacks — an AST-isomorphic render tree (OpenSCAD) or an artifact graph with ancestry edges (Zoo) —
and bikar's `Face` carries a flat tag set with no ancestry. The honest local answer is therefore
plural and 2.4% empty, and there is no surface to display it on (§5.5). **What would falsify it:**
someone building the ancestry — which is a real, coherent project, and §7 Phase 4/5 is where it
would land. This doc does not argue that project is wrong, only that it is not what "add source
spans" buys.

**B.4 — Claiming the chokepoint result is a property of *this* parser, not a general one.**
§2.3's 12 lines work because `parseStatement`/`parseDeclaration` are handler-table dispatchers.
**The bet:** that architecture survives. §8.1 flags the parallel grammar-formalization question as
the thing that could invalidate it — and notes that a tree-sitter-style replacement would make
Phases 1, 1b and 2 redundant rather than harder. **Why it still stands:** 12 lines and 4 lines are
cheap enough to throw away.

**B.5 — Treating comment retention as the headline result of a click-to-source investigation.**
§9 recommends a change that has nothing to do with the feature that was commissioned. **The bet:**
25.1% of the corpus is comments; 269 lines across 31 files are hand-written `# Construction:` steps;
`derivation-visualization-survey.md` §12.6 found that **node labelling is the universal weak point
across every tool surveyed** (CascadeStudio: `fnName` + line number; jupyter-cadquery:
`box(10, 20) => _v1`, §4.6; Zoo: the only human-meaningful names, and it cannot expand user-defined
functions). bikar's authors already wrote the good labels and the lexer discards them at
`lexer.ts:88`. **What would falsify it:** Q8 — source-line and comment text may read worse than a
synthesized label, since one is syntax and the other is prose. **What makes it worth the risk:** it
is four lines.

**B.6 — Asserting there is no click surface, when adding one is not hard.**
A `<script>` in an SVG, or a Lab tab that renders the 2D pattern, would each create a surface.
**The bet:** the absence is a signal, not an accident. The Lab explicitly refuses editor
dependencies (`editor.ts:3`) and is aimed at orbs; the 40 SVGs in this repo are static assets in a
static gallery; and `data-shape-id` already demonstrated what shipping a producer-side payload
before its consumer exists gets you — an ACCEPTED attribute with a FALSIFIED use case. **What would
falsify it:** a Lab 2D-pattern tab landing for unrelated reasons, at which point §7 Phase 5's
trigger fires legitimately.
