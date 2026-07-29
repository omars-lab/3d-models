# `.bkr` grammar formalization — design/audit doc

Status: **DRAFT v1 — grounded in a first-party audit of the bikar parser
(measurements in §2–§3, run against the built `packages/core/dist` and the 327-file `.bkr`
corpus) and in a survey of parser-generator and grammar-notation practice (Appendix A).
Contested bets in Appendix B.**
Question asked: *is the `.bkr` DSL being parsed "properly", and should it have a formal grammar
(BNF/EBNF) and/or a generated parser instead of the hand-rolled one?*
Scope: the syntactic front end only — `lexer.ts` → `parser.ts` → `ast.ts`. Nothing about the
evaluator, the renderer, or the kernel3d pipeline.
Rides: nothing. This document proposes no engine change in Phase 0–1.

**Nothing in this doc is implemented. No code has been written. Every measurement comes from
throwaway scripts run against `packages/core/dist/index.js`, not from anything checked in. No
file in `bikar/` was modified.**

---

## 1. Premise check

The premise handed to this work was: *the `.bkr` parser is hand-rolled recursive descent with no
formal grammar, therefore parsing may not be "proper", therefore we should consider a grammar
and/or a generated parser.*

**The premise does not survive contact with the code, and the reason it fails is specific.**
"Hand-rolled" is not the defect, and the industry evidence usually cited for that claim points the
other way. But the audit found five real defects, none of which a parser generator would
have prevented, and three of which are cheap to fix without one.

| Premise component | Verdict | Evidence |
|---|---|---|
| "No formal grammar exists" | **True** | `*.ebnf`/`*.bnf`/`*.grammar`/`*.pegjs`/`*.ne` — zero files in any of the four repos. Spec is prose: `bikar/docs/language-reference.md`, 841 lines, 11 signature-style headings. |
| "Hand-rolled recursive descent" | **True** | `bikar/packages/core/src/dsl/parser.ts`, 3,993 lines, 115 `private parse*` methods. |
| "…therefore parsing may be improper" | **False as stated** | 326 of 327 corpus files parse. The one failure is a bad file, not a parser bug (§3.6). Clang, GCC (since 4.1), and Zoo's KCL all hand-roll *by choice* (§4.1). |
| "A generated parser would be safer" | **False for the defects that exist** | All five defects (§3) live in `preprocessSource`, in layout sensitivity, in the keyword table, or in error strategy. A generator changes none of them; two of them it makes *worse* (§5.3). |
| "A grammar would be useful" | **True, for different reasons than assumed** | Not as a parser source. As a **written spec** and as a **fuzzer seed** (§5.2, §5.5). |

**Measured, so the premise can be argued with rather than asserted at:**

| Metric | Value | How obtained |
|---|---|---|
| `.bkr` corpus | **327 files** (bikar 93, sacred-patterns 112, qiyas 111, 3d-models 11) | `find` across all four repos, `node_modules` excluded |
| Corpus size | 53,693 lines · 2,400,427 bytes · **211,325 tokens** | `lex()` over the corpus |
| Parse failures | **1** (`sacred-patterns/…/girih-star4.bkr`) | `parse()` over the corpus |
| Reserved keywords | **123** | `KEYWORDS` map, `bikar/packages/core/src/dsl/tokens.ts:197`+ |
| Contextual (soft) keywords matched by string value | **25** + 8 math functions + 7 orb solids = **40** | `grep -oE "\.value (===\|!==) '[a-z_]+'" parser.ts` |
| Maximum lookahead | **2** | one `peek(1)` at `parser.ts:815`; no other multi-token lookahead |
| Backtracking sites | **0** | `this.pos` is mutated only in `advance()` (`parser.ts:525-528`) |
| Located diagnostics | **99** `throw new ParseError` | `parser.ts` |
| Assignment-LHS names in corpus that collide with a keyword | **0 of 1,300** | corpus scan |

---

## 2. What the parser actually is

### 2.1 It is LL(2), deterministic, and backtracking-free

The entire cursor mechanism is nine lines (`bikar/packages/core/src/dsl/parser.ts:521-528`):

```ts
private peek(ahead = 0): Token {
  const i = this.pos + ahead;
  return this.tokens[i] ?? this.tokens[this.tokens.length - 1];
}
private advance(): Token {
  const t = this.tokens[this.pos++];
  return t;
}
```

`this.pos` is assigned in exactly one place in 3,993 lines. There is no save/restore, no
speculative parse, no `try { … } catch { pos = mark }`. The 7 `catch` clauses in the file all
wrap numeric evaluation, not parsing. Dispatch is by leading token through 7
`Partial<Record<TokenType, …>>` tables (`declarationHandlers` at `parser.ts:590`,
`statementHandlers` at `parser.ts:2126`+, `connectModeHandlers`, and four others).

**This matters more than anything else in the doc.** The strongest published defence of
hand-rolling — that real languages (C++, Rust) are not in a tractable grammar class and the
generator fights you — **does not apply to bikar**. bikar is squarely inside what any LL/LR
generator handles. The honest position is therefore not "we hand-rolled because we had to"; it is
"we hand-rolled, and the cost of switching now exceeds the benefit" (§5.3).

### 2.2 It already practises soft-keyword discipline, deliberately and in writing

`tokens.ts` carries the policy in comments at five declaration keywords
(`tokens.ts:130-156`). Verbatim, at `Orb` (`tokens.ts:130-134`):

> Its body words — base, inscribe, project, struts, pierce — stay plain identifiers, matched
> contextually by the parser, so existing sources that use them as pattern/shape names
> (e.g. `pattern base`) keep parsing unchanged.

The same note is repeated for `Piece`, `Param`, `Wall`, and `Assembly`. And `expectName()`
(`parser.ts:2811-2818`) accepts *any* keyword where a name is expected:

```ts
// Accept identifiers and any keyword token (keywords can be used as names in some contexts)
if (t.type === TokenType.Identifier || KEYWORDS.has(t.value)) {
```

This is a real, maintained discipline adopted in response to a real incident
(`bikar/docs/engine-issues.md:62-65`, "Keyword Collision with Palette Names", commit `0ff7848`;
`bikar/docs/lessons.md:387-402`). **It is also invisible to anyone who has not read the
comments** — which is one of the two strongest arguments for a written grammar (§5.2).

### 2.3 It is layout-sensitive in seven places

Seven parse decisions read `Token.column`:

| Site | `parser.ts` | Rule | Corpus files affected |
|---|---|---|---|
| `style` / `animate` top-level vs statement | `806` | top-level iff `column === 1` | 119 / 14 |
| `clip` declaration vs `clip pattern` statement | `815` | `column === 1` **and** `peek(1) !== Pattern` | 2 |
| `for` body extent | `3113` | body = tokens with `column > forCol` | 2 |
| `repeat` body extent | `3155` | `column <= repeatCol` ends body | 49 |
| `rotate` body extent | `3182` | `column <= rotateCol` ends body | 88 |
| `mirror` body extent | `3209` | `column <= mirrorCol` ends body | 3 |
| `face` body extent | `3453` | `column <= faceCol` ends body | 3 |

The source itself names the first as ambiguous (`parser.ts:797-803`):

> Blueprint/pattern are always top-level. Style/animate are ambiguous: they can be top-level
> declarations or statement references. We treat style/animate as top-level only at column 1
> (unindented).

**A context-free grammar cannot express any of these seven rules.** The standard remedy is a
lexer that emits INDENT/DEDENT tokens; `lexer.ts` emits nothing of the kind — `consumeWhitespace`
discards horizontal space outright. This is the single biggest obstacle to any grammar-derived
parser (§5.3) and the single biggest caveat on any EBNF that gets written (§6).

### 2.4 It preprocesses the source text before lexing

`preprocessSource` (`bikar/packages/core/src/dsl/lexer.ts:314-331`) rewrites the source *string*
line by line, replacing `#RRGGBB` with a `__hex_RRGGBB` identifier so that the `#` comment
character does not eat colour literals. `lex()` then converts those identifiers back into
`HexColor` tokens. The trigger set is four tokens — `=`, `color`, `stroke`, `fill`:

```ts
/(?:=|color|stroke|fill)\s*#([0-9a-fA-F]{3,8})/g
```

This is context-sensitivity smuggled into a nominally context-free pipeline, and it is the source
of three of the five defects in §3. There is also a second, divergent implementation of the same
idea — `resolveHexColors`, exported, using a *different* regex (`/=\s*#([0-9a-fA-F]{3,8})\b/g`,
note the `\b`), documented in its own comment as not on the active `lex` path.

### 2.5 Test coverage of the grammar surface

| Artifact | Size | What it covers |
|---|---|---|
| `bikar/packages/core/tests/dsl/parser.test.ts` | 2,681 lines · 156 tests · 18 `toThrow` | positive constructs, mostly |
| lexer tests | **none** — `tests/dsl/` contains no lexer test file | nothing |
| `tests/canonical/starter-compile.test.ts` | globs `bikar/patterns/**/*.bkr` | **93 of 327 corpus files (28%)** |

That last test exists *because of* the keyword-collision incident; its header says so:

> Why this test exists: keyword additions to the DSL have silently broken shipped starter recipes
> before (Radiant, Rosette-Radar)…

**It is the right idea aimed at 28% of the available corpus.** Enlarging its aim is the cheapest
single improvement available anywhere in this document (§8, gate G1).

---

## 3. The five real defects

None of these is "the parser is hand-rolled". All five are independently fixable, and four of
them are *not* fixed by any option in §5.

### 3.1 D1 — `preprocessSource` corrupts every column number to its right

`__hex_` is 6 characters; `#` is 1. Every token after a rewritten hex on the same line reports a
column **5 too far right**, per hex literal on that line.

Measured, source `  fg = #000000 extra`:

```
Identifier("fg")@3:3  =@3:6  HexColor("#000000")@3:8  Identifier("extra")@3:21
actual column of "extra": 16
```

And in a real diagnostic, source line 5 = `  bg = #ffffff ???`:

```
Lexer error at 5:21: Unexpected character: ?      (the `?` is at column 16)
```

**Blast radius:** 298 of 327 corpus files contain a preprocessed hex literal; 1,564 lines are
rewritten; **186 of those lines have further content after the hex**, i.e. are lines where a
diagnostic would point to the wrong column today.

This is a five-line fix (pad the replacement to the original width, or record a per-line column
map) and it is a **precondition for click-to-source** — see §10.

### 3.2 D2 — the hex rewrite has no validation, in either direction

Three demonstrated leaks, all reproduced against `dist`:

| Input | Result | Why |
|---|---|---|
| `a = #abcg` | `HexColor("#abcg")` — a non-hex char inside a hex token | regex matches `abc`, emits `__hex_abc`; the identifier scanner (`IDENT_CONT_RE = /[a-zA-Z0-9_]/`, `lexer.ts:31`) then swallows the trailing `g` |
| `a = #abcdef0123` | `HexColor("#abcdef0123")` — 10 digits, defeating the `{3,8}` cap | same mechanism |
| `__hex_abc = red` | lexes as `HexColor("#abc")` — the identifier is hijacked | `lex()` converts *any* identifier starting `__hex_`, with no guard |
| `a = #ab` | clean `Expected HexColor, got Newline` | 2 digits fails the regex, so `#ab` stays a comment |

`grep` finds **no hex validation anywhere in `packages/core/src/`**. The one case that errors
cleanly errors *by accident*. Both malformed literals above compile end-to-end without a
diagnostic.

### 3.3 D3 — the trigger set is complete by maintenance, not by construction, and nothing asserts it

`TokenType.HexColor` is accepted in five places (`parser.ts:2670, 2837, 3612, 3627, 3780`). The
four preprocessor triggers happen to cover all five. Two demonstrated failure modes when they do
not line up:

- **Line-scoped rewriting.** `a =` / newline / `    #ffffff` silently drops the colour — the hex
  becomes a comment, and the `=` is left dangling.
- **A position the triggers do not cover.** `values [#ff0000, #00ff00]` inside an `animate`
  keyframe swallows the rest of the line and reports
  `Parse error at 9:1: Expected name, got EOF ('')` — **six lines past the actual mistake.**
  (`parseAnimValue`, `parser.ts:3926`, uses `expectName()` and does not accept `HexColor`.)

**I could not construct an input where a genuine trailing comment is eaten as a hex literal.** A
comment's `#` is either line-leading (nothing precedes it to trigger the regex) or preceded by
real code, which would have to end in a bare `=`/`color`/`stroke`/`fill` — itself already a syntax
error. Four probe families (B1/B2/F1/H-series) all came back safe. **This defect is a latent
correctness hazard, not a live exploit**, and the honest way to state it is: the attack surface is
empty because **0 of 327 corpus files use a trailing inline comment**, obeying a rule
`language-reference.md:838` documents (`# inline comments not supported`) that
`consumeComment` (`lexer.ts:86`) does **not** actually enforce.

### 3.4 D4 — keyword collision is live, reproducible today, and produces a maximally misleading error

The documented incident (`lessons.md:387-402`: `edge = #5C3D1A` in `Radiant.bkr`,
`void = #0A0A1A` in `Rosette-Radar.bkr`) is not historical. Reproduced against `dist`, a palette
entry named with any current keyword:

```
edge   -> Parse error at 3:5: Expected 'param', 'blueprint', 'pattern', 'style', 'animate',
          'orb', 'piece', 'tile', 'clip', 'wall', or 'assembly', got edge ('edge')
```

Six of eight probed names (`edge`, `void`, `face`, `color`, `radius`, `line`) fail this way;
`safe_name` and `star` pass. The mechanism: `parsePalette` (`parser.ts:2820`+) loops only
`while (this.peek().type === TokenType.Identifier)`, so a keyword-named entry silently terminates
the palette, and the failure surfaces later as a **top-level structure error pointing at the
colour's own line**. The message tells the author their file's top level is wrong when one colour
name is wrong.

The exposure today is zero (0 of 1,300 assignment-LHS names collide) — but the exposure is
recomputed on **every keyword addition**, and `KEYWORDS` is at 123 and growing (`orb`, `piece`,
`param`, `wall`, `assembly` are all recent). This is precisely the risk `starter-compile.test.ts`
was built to catch, aimed at 28% of the corpus.

### 3.5 D5 — one error per file, and the lexer preempts the parser

`parse()` (`parser.ts:423`) runs `lex()` to completion, then parses. So a lexical error
*anywhere* in the file masks every parse error *before* it. Demonstrated with a file containing
three independent errors (missing radius on line 2, missing divide count on line 3, `?` on line 5):

```
Lexer error at 5:11: Unexpected character: ?
```

One diagnostic; the two earlier, more actionable ones never surface. There is no synchronization
set, no error production, no `Bad*` node. Compare `go/parser`, whose documentation states it
*"accepts a larger language than is syntactically permitted by the Go spec, for simplicity, and
for improved robustness in the presence of syntax errors"* and returns *"a partial AST (with
`ast.Bad*` nodes representing the fragments of erroneous source code)"*.

For a single-author CLI compiler, one-error-then-stop is a defensible choice. For an editor
integration it is not, and §10 is where that bill arrives.

### 3.6 The one corpus failure is a bad file, not a parser bug

`sacred-patterns/sessions/bikar-medallion-10/girih-network/girih-star4.bkr`,
`Parse error at 17:37: Unexpected token: Identifier ('star')`. Line 17 is
`  girih field decagonal 30 shells 1 star 4`; column 37 is `star`.

The file's own header comment says *"The fix is the new `star <k>` keyword: `star 4` = {10/4} chord
skip"* — i.e. it was committed (`fa12d1b`, 2026-06-21) as a **witness for a feature that was never
implemented**. `star` exists in `parser.ts` only as a contextual identifier inside
`tryParsePocketsVariant` (`parser.ts:3401-3410`), never in the `girih field` production
(`parseGirihField`, `parser.ts:3361`+). The parser is correct to reject it.

**Consequence for every option below:** the corpus's true baseline is **326 must-parse + 1
must-fail**, and any conformance harness must encode the `must-fail` as an expectation, not as a
tolerated failure.

---

## 4. Prior art — who hand-rolls, who generates, and why

### 4.1 Production language front ends

| Project | Front end | Stated reason (verbatim where fetched) |
|---|---|---|
| Clang | hand-built recursive descent | *"Because it is plain C++ code, recursive descent makes it very easy for new developers to understand the code, it easily supports ad-hoc rules and other strange hacks required by C/C++, and makes it straight-forward to implement excellent diagnostics and error recovery."* |
| GCC | hand-written recursive descent since 4.1 | *"The old Bison-based C and Objective-C parser has been replaced by a new, faster hand-written recursive-descent parser."* |
| rustc | hand-written lexer (`rustc_lexer`) | *"Although it is popular to implement lexers as generated finite state machines, the lexer in `rustc_lexer` is hand-written."* The dev guide does **not** state a rationale for the parser itself — marked **unverified** for the parser. |
| Go | `go/parser`, recovery-oriented | accepts a larger language than the spec *"for improved robustness in the presence of syntax errors"*; returns partial ASTs with `ast.Bad*` nodes |
| Zoo / KittyCAD **KCL** | hand-written, `winnow` combinators (`rust/kcl-lib/src/parsing/{parser.rs,token/,ast/}`, `winnow = "1.0"` and no `nom`/`pest`/`lalrpop`/`chumsky` in `Cargo.toml`) | none published |
| **OpenSCAD** | **Bison** (`src/core/parser.y`, with `%union`/`%token`/`%expect 0`) + Flex | none published |
| TypeScript, V8 | widely reported as hand-written recursive descent, but the pages fetched (`TypeScript-Compiler-Notes/GLOSSARY.md`, `v8.dev/blog/scanner`) do **not** state it | **unverified** |

**Synthesis, three points.**

1. **"Hand-rolled" is the majority position among the front ends that care most about
   diagnostics**, and every stated reason is about *error quality and hackability*, not speed.
   Clang's sentence is the one that transfers to bikar directly.
2. **The nearest neighbour in the problem domain is split.** OpenSCAD — the closest analogue to
   bikar, a small declarative geometry DSL — uses Bison. KCL, the newest well-funded CAD DSL,
   hand-rolls with combinators. There is no domain consensus to defer to.
3. **Nobody in the list treats "no formal grammar" as a defect to be fixed by generating the
   parser.** The projects that publish grammars (SVG path data, Graphviz DOT, XML) publish them as
   *specifications*, decoupled from any implementation. That is the split this document adopts
   in §5.

### 4.2 Notation, if a grammar is written

| Notation | Fit for `.bkr` | Note |
|---|---|---|
| **W3C XML EBNF** | **chosen** | `*`/`+`/`?`/`()`/`|` plus the exclusion operator: *"A - B means any string that matches A but does not match B"* — needed for `identifier - keyword`, which is exactly the soft-keyword situation in §2.2 |
| ABNF (RFC 5234) | poor | designed for byte-oriented internet protocols; *"balances compactness and simplicity with reasonable representational power"* — its strengths (value ranges, case rules) are irrelevant here |
| ISO 14977 EBNF | rejected | the terminator-heavy syntax is unpleasant to read and is not what the neighbouring specs use |
| PEG | rejected **as the spec notation** | Ford's ordered choice *"solve[s] the ambiguity problem by not introducing ambiguity in the first place"* — which means a PEG **cannot report** that the grammar is ambiguous. §2.3's genuine ambiguity would be silently papered over, which is the opposite of what a spec is for. |
| Graphviz-style prose grammar | close second | *"Terminals are shown in bold font and nonterminals in italics. Literal characters are given in single quotes."* Readable, but has no exclusion operator |
| Railroad diagrams | supplementary only | generated *from* the EBNF, never authored |

**Decision: if a grammar is written, it is W3C XML EBNF, in one fenced block per production
group, with a coverage table stating exactly what is and is not covered.** Rejected: ABNF (wrong
domain), ISO 14977 (unreadable, unused by neighbours), PEG-as-spec (structurally unable to
express the thing §2.3 needs expressed).

---

## 5. Options

Five options were considered. Each is stated with what it buys, what it costs, and — for the
rejected ones — the specific fact that killed it.

| | Option | Grammar is the spec? | Fixes D1–D5? | Migration risk | Gives spans/trivia? | Verdict |
|---|---|---|---|---|---|---|
| (a) | Status quo | no | no | none | no | **partially adopted** — as the baseline for (b) and (e) |
| (b) | EBNF **as documentation**, conformance-tested against the real parser | yes, as prose | D3, D4 (by making them visible + testable) | none | no | **adopted** |
| (c) | Generate the parser from a grammar | yes, as source | no; makes D2/D5 harder | **very high** | no | **rejected** |
| (d) | tree-sitter / Lezer **alongside** the hand-rolled parser, for tooling | second grammar | no | medium | **yes** | **deferred, not rejected** — §10 |
| (e) | Grammar as **test oracle** — differential + round-trip fuzzer over 327 files | no | D2, D4, D5 (detection) | none | no | **adopted** |

### 5.1 (a) Status quo

**What it buys:** zero cost, and it is not as bad as the premise assumed — 326/327, 99 located
diagnostics, no backtracking, a documented soft-keyword discipline.
**What it costs:** the discipline of §2.2 lives only in comments; the layout rules of §2.3 are
undocumented anywhere a DSL author would look; D1–D5 stay.

**Decision: the status quo is the *implementation* baseline, not the *documentation* baseline.**
The parser stays. The prose spec does not stay as-is (§7).

### 5.2 (b) EBNF as documentation, conformance-tested

Write a grammar that describes what `parser.ts` actually accepts, keep it in
`bikar/docs/`, and make its *worked examples* executable — every example in the grammar file is a
`.bkr` snippet that a test parses (or asserts fails).

**What it buys, concretely:**

- The seven layout rules (§2.3) and the 40 contextual keywords (§2.2) become **stated**, not
  archaeology. Today the only way to learn that `style` at column 2 means something different is
  to read `parser.ts:806`.
- It makes D3 checkable: the grammar names the five `HexColor` positions, and a test asserts the
  preprocessor's trigger set covers exactly those.
- It makes D4 a review artifact: adding a keyword becomes a visible diff against a stated
  reserved-word list.
- It is the seed the fuzzer in (e) needs.

**What it costs:** the grammar can drift from `parser.ts`. This is the one serious objection and
it is answered in Appendix B.1.

**Decision: adopt (b), with the standing rule that a grammar which does not match `parser.ts` is
worse than no grammar.** Therefore the grammar ships *with* the conformance test in the same
change, never before it, and the coverage table in §6 is mandatory — a partial grammar that
claims completeness is the failure mode being guarded against.

### 5.3 (c) Generate the parser from a grammar — rejected

Candidates surveyed: Peggy (*"a simple parser generator for JavaScript that produces fast parsers
with excellent error reporting"*, PEG), Nearley (Earley; *"effectively linear-time for LL(k)
grammars"*, handles ambiguity by returning all parses), Chevrotain (*"an internal JavaScript
DSL"*, not a generator; *"implements error recovery heuristics to parse even partially invalid
inputs"*), ANTLR4 (*"a powerful parser generator for reading, processing, executing, or
translating structured text"*), Langium (*"first-class support for the Language Server Protocol,
written in TypeScript"*; generates parser + AST + LSP server from a grammar).

**Decision: reject (c).** Four reasons, in descending weight:

1. **The layout rules are not context-free.** All seven sites in §2.3 read `Token.column`. Every
   generator listed requires either a token stream with INDENT/DEDENT (which `lexer.ts` does not
   produce) or a semantic-predicate escape hatch (ANTLR, Chevrotain) — at which point the grammar
   contains embedded imperative code and has stopped being a spec. **The generator would not
   remove the hand-written layout logic; it would relocate it into the grammar file.**
2. **Diagnostics would regress.** 99 hand-placed `ParseError`s carry domain-specific text —
   `"Statement '%s' is not allowed in blueprint block. Only circle, divide, polygon, …"`,
   `"subdivide expects an integer 1..4, got '%s'"`. Generated parsers produce
   `expected one of {…}`. Clang's stated rationale is exactly this, and Chevrotain's own pitch
   is that it *"can compete with the performance of hand-crafted parsers"* — performance, not
   diagnostics, is what it claims parity on.
3. **The one thing generators are uniquely good at, bikar does not need.** Generators earn their
   keep on grammars a human cannot keep straight. bikar is LL(2) with zero backtracking (§2.1).
   The complexity that would justify the switch is absent.
4. **A new runtime dependency.** `bikar-core` ships **zero** runtime dependencies
   (`bikar/docs/decisions/2026-05-07-polygon-clipping-dep.md`). Peggy/Nearley/ANTLR-generated
   parsers can be built to a dependency-free artifact, but Chevrotain and Langium cannot; and
   even the dependency-free ones add a build step and a generated file to review.

**What would reverse this:** a `.bkr` construct that needs unbounded lookahead or genuine
ambiguity resolution. None exists today; §12 Q3 names the trigger.

### 5.4 (d) tree-sitter or Lezer alongside — deferred, and reported to the parallel work

This is the strongest secondary candidate, and it is the only option that pays for itself in a
currency the hand-rolled parser cannot mint.

- **tree-sitter**: *"General enough to parse any programming language… Fast enough to parse on
  every keystroke in a text editor… Robust enough to provide useful results even in the presence
  of syntax errors… Dependency-free so that the runtime library (which is written in pure C11) can
  be embedded in any application."* Grammar is a JavaScript `grammar.js`; conflicts resolve by
  precedence, and *"for genuine ambiguities… Tree-sitter will use the GLR algorithm to explore all
  the possible interpretations."*
- **Lezer**: *"uses the LR parsing algorithm"*, is *"Incremental"* and *"Error-Insensitive"* with
  *"strategies for recovering from syntax errors"*, and was *"designed for the code editor use
  case"* — it is CodeMirror 6's parser system, which matters because the Orb Lab is a browser
  surface.

**What it buys that nothing else does:** a concrete syntax tree with **source spans on every
node** and **retained trivia**, incrementally, error-tolerantly. `ast.ts` has **zero** position
fields today (`grep -cE "readonly (line|column|span|start|end|loc|pos)\b" ast.ts` → `0`, across
1,190 lines and 64 `kind:` literals), and `consumeComment` (`lexer.ts:86`) discards comments
entirely. Both gaps close as a side effect.

**What it costs:** a **second grammar that can disagree with `parser.ts`**. The divergence risk
here is categorically worse than in (b): in (b) the grammar is prose and a test can compare it to
one parser; in (d) there are two executable parsers, each authoritative for different consumers
(the editor vs the compiler), and *nothing in either tool detects the disagreement*. Every
tree-sitter grammar in the wild accepts programs the real compiler rejects — that is by design,
because an editor must keep highlighting broken code. It is also exactly the property that makes
the second grammar unusable as a specification.

**Decision: defer (d) — do not reject it — and hand the decision to whoever owns editor tooling.**
It is not a grammar-formalization decision; it is an editor-integration decision that happens to
involve a grammar. §10 states the interaction explicitly.

### 5.5 (e) Grammar as test oracle — adopted

Three mechanisms, in increasing cost:

1. **Differential corpus sweep (cheap, immediate).** Parse all 327 files on every commit; assert
   326 pass and `girih-star4.bkr` fails with its exact message. This is `starter-compile.test.ts`
   pointed at 3.5× more input. McKeeman's differential-testing framing applies loosely — bikar
   has only one parser, so there is no second implementation to diff against; the diff is
   **against the recorded baseline of the corpus itself**. (McKeeman's 1998 paper was
   **not retrievable**: `cs.cmu.edu` and `cs.dartmouth.edu` copies both returned **HTTP 403**.
   The concept is standard; the citation is **unverified**.)
2. **Round-trip / print-parse idempotence (medium).** There is no `.bkr` printer today, so this
   is only available if one is written. Deferred to §11 Phase 3.
3. **Grammar-driven generation (the real prize).** Nearley advertises *"inverting parsers into
   generators for fuzzing and test case creation"*; Grammarinator is *"a random test generator /
   fuzzer that creates test cases according to an input ANTLR v4 grammar"*; the Fuzzing Book's
   position is that grammar-based fuzzing *"take[s] a grammar to produce syntactically valid input
   strings"* so testers can *"focus on semantic vulnerabilities rather than parser failures"*.
   In-repo, `fast-check` lists `letrec` among its combiners, which is the mechanism for
   recursive/mutually-recursive generators — the natural fit for a small declarative grammar.

**Decision: adopt (e), starting with mechanism 1 only.** Mechanism 3 is Phase 2 and depends on
(b) existing. Rejected: writing a fuzzer *before* the grammar — a generator whose distribution is
invented rather than derived tests the generator, not the parser.

---

## 6. The partial EBNF — derived and checked

This is a **partial** grammar, derived by reading `parser.ts` and verified by round-tripping each
production against `parse()`. **It covers 6 of 64 AST node kinds and 4 of 11 top-level
declaration forms.** Publishing it as complete would be a lie; the coverage table below is part
of the artifact, not commentary on it.

Notation: W3C XML EBNF. `A - B` is exclusion.

```ebnf
/* ---- file structure  (parser.ts:549-584) ---- */
File          ::= NL* Param* Declaration+
                  /* `Param` before any `Declaration` is enforced imperatively at
                     parser.ts:556-564; the CFG above states it, the parser's error
                     message states it better. At least one Declaration is required
                     (parser.ts:571-573). */

Declaration   ::= Blueprint | Pattern | Style | Animate | Orb
                | Piece | Tile | Clip | Wall | Assembly
                  /* dispatch table, parser.ts:590-601 */

/* ---- param  (parser.ts:630-700, signature quoted at parser.ts:618) ---- */
Param         ::= 'param' Name '=' ConstExpr ParamRange? 'advanced'? NL
ParamRange    ::= 'range' ConstExpr '..' ConstExpr ParamStep?
ParamStep     ::= 'step' ConstExpr
                  /* 'range', 'step', 'advanced' are CONTEXTUAL: matched by
                     Token.value at parser.ts:662, not by TokenType.  Policy stated
                     at tokens.ts:141-143. */

/* ---- blueprint  (parser.ts:851-875) ---- */
Blueprint     ::= 'blueprint' Identifier NL BlueprintStmt*
                  /* body terminates at isTopLevel() — parser.ts:797-818 — which is
                     NOT context-free.  See the LAYOUT note below. */
BlueprintStmt ::= Circle | Divide | Polygon | Line | Segment | Intersect
                | Repeat | Rotate | Mirror | Bisector | Tangent | Offset
                | Fillet | Boundary
                  /* BLUEPRINT_STARTERS, parser.ts:840-848.  Note the error message
                     at parser.ts:864 lists only 12 of these 14 — 'offset' and
                     'fillet' are accepted but unlisted.  Grammar follows the code,
                     not the message. */

/* ---- circle  (parser.ts:2174-2216) ---- */
Circle        ::= 'circle' Identifier? 'center' '(' CircleCenter ')' 'radius' NumExpr
CircleCenter  ::= Variable                              /* center($p)        */
                | Number ',' Number                     /* center(x, y)      */
                | RepeatAddr '.' Identifier             /* center(@0.3.p0)   */
                | Identifier '.' Identifier             /* center(C0.p0)     */

/* ---- divide  (parser.ts:2326-2351) ---- */
Divide        ::= 'divide' DivideTarget? 'into' Number DivideOffset?
DivideTarget  ::= Identifier | RepeatAddr
DivideOffset  ::= 'offset' '-'? Number

/* ---- polygon  (parser.ts:2353-2372) ---- */
Polygon       ::= 'polygon' Identifier NL? '[' ( NL* PointPair )* NL* ']'
PointPair     ::= Identifier '.' Identifier
                  /* no separator between points — the loop at parser.ts:2359 reads
                     until ']' with no comma handling.  A comma is a parse error. */

/* ---- point references  (parser.ts:2543-2575) ---- */
PointRef      ::= RepeatAddr '.' Identifier
                | RelChain '.' Identifier
                | Identifier RepeatAddr '.' Identifier   /* iff Identifier ends '_' */
                | Identifier '.' Identifier
RelChain      ::= RelPart ( '.' RelPart )*
RelPart       ::= '$self' | '$parent' | '$sibling' '(' Number ')'

/* ---- names and the soft-keyword rule  (parser.ts:2811-2818) ---- */
Name          ::= Identifier | Keyword          /* expectName(): keywords ARE names */
Identifier    ::= IdentStart IdentCont*  -  Keyword   /* lexer.ts IDENT_START_RE/IDENT_CONT_RE
                                                         + the KEYWORDS map, tokens.ts:197 */
IdentStart    ::= [a-zA-Z_]
IdentCont     ::= [a-zA-Z0-9_]
Keyword       ::= /* one of the 123 entries in KEYWORDS, tokens.ts:197+ */
```

### 6.1 What this grammar does **not** cover, stated exactly

| Not covered | Why |
|---|---|
| `pattern`, `style`, `animate`, `orb`, `piece`, `tile`, `clip`, `wall`, `assembly` bodies | 9 of 11 declaration forms; ~2,500 lines of `parser.ts` unread for this purpose |
| 58 of 64 AST node kinds | only `file`, `blueprintDeclaration`, `circle`, `divide`, `polygon`, `repeat` (head only) are covered |
| `NumExpr` / `ConstExpr` precedence | `parseNumericExpr` → `parseAddSub` chain, `parser.ts:2243`+; needs its own production group |
| The 40 contextual keywords | 25 value-matched + 8 `MATH_FUNCTIONS` (`parser.ts:2231`) + 7 orb solids. Only `range`/`step`/`advanced` appear above |
| `for` / `repeat` / `rotate` / `mirror` / `face` bodies | **structurally inexpressible** — see LAYOUT below |
| Hex colours | **structurally inexpressible** — `#RRGGBB` is not produced by the lexer; it is produced by a source rewrite before lexing (§2.4) |
| Comments | `consumeComment` discards them; they never reach the parser, so no production can mention them |

**LAYOUT — the note that must accompany any `.bkr` grammar.** Seven productions above and below
are gated on `Token.column` (§2.3). The EBNF above **silently omits** those gates, which means:

- `Blueprint ::= 'blueprint' Identifier NL BlueprintStmt*` is **wrong in one direction** — it does
  not say that the body ends when a `style`/`animate`/`clip` appears **at column 1**.
- `Repeat`, `Rotate`, `Mirror`, `Face`, and `For` bodies cannot be written at all without
  INDENT/DEDENT terminals, which `lexer.ts` does not emit.

Any future completion of this grammar must either (i) introduce `INDENT`/`DEDENT` as *declared
pseudo-terminals with a prose definition*, or (ii) mark those productions
**`{layout-sensitive}`** and describe the rule in prose beside them. Option (ii) is what
Graphviz and SVG do with their own out-of-band rules, and is the recommendation.

### 6.2 One divergence found while deriving it

`parseBlueprintDeclaration`'s error message (`parser.ts:864`) enumerates 12 allowed
statements; `BLUEPRINT_STARTERS` (`parser.ts:840-848`) contains 14. `offset` and `fillet` parse
fine inside a blueprint but are absent from the message a user sees when they get it wrong. **This
is the class of bug a written grammar catches and a test suite does not**, because no test asserts
the message enumerates the set. It is a one-line fix in `parser.ts` and is deliberately **not**
made here (this doc modifies no bikar file); logged as §12 Q1.

---

## 7. Interaction with `docs/language-reference.md`

The prose reference (841 lines) is not replaced. It is **not** the same artifact as a grammar: it
is a tutorial-flavoured reference with worked examples, and it is already quasi-formal — 11 of its
headings are signatures, e.g.

> ### `param <name> = <default> [range <min>..<max> [step <s>]] [advanced]`

**Decision: the EBNF is a new sibling file (`bikar/docs/grammar.md`), and
`language-reference.md` links to it from each signature heading. The reference stays
authoritative for semantics; the grammar becomes authoritative for syntax.** Rejected: folding the
EBNF into `language-reference.md` (it would double the file and bury the examples), and replacing
the prose reference with the grammar (a grammar teaches nobody the language).

Two divergences in the reference were found and must be fixed in the same change that adds the
grammar — both in the Comments section, `language-reference.md:833-841`:

| Reference says | Implementation does | Fix |
|---|---|---|
| `# inline comments not supported` (shown in an example) | `consumeComment` (`lexer.ts:86`) consumes `#`-to-EOL **anywhere on the line**, so inline comments *are* lexically supported — just not safe near a hex trigger (§3.3) | state the real rule: inline comments work, **except** after `=`/`color`/`stroke`/`fill`, where the text is captured as a hex literal |
| "hex colors are handled via preprocessor (palette definitions and `color` keywords)" | the trigger set is **four** tokens: `=`, `color`, `stroke`, `fill` (`lexer.ts:321`) | enumerate all four |

---

## 8. Enforcement — what is a gate, what is a warning, what cannot be enforced

This section follows the pattern of `derivation-worksheet-design.md` §5.1 and is deliberately
consistent with it: **three gates, and no second Stop hook.**

`derivation-worksheet-design.md` §5.1 already defines E1 (prefix sweep at `fail=0`), E2 (closed
gloss vocabulary), E3 (suppressed-diagnostic count vs baseline). The gates below are numbered
**G1–G3** so the two sets do not collide, and G1 is explicitly designed to *subsume* the corpus
half of E1 rather than duplicate it.

**G1 — the corpus sweep becomes a standing assertion at `326 pass / 1 known-fail`.** A vitest
case that parses all 327 `.bkr` files across the four repos and asserts the exact partition,
including `girih-star4.bkr`'s exact message. This is `starter-compile.test.ts` (93 files, 28%)
generalized to 327. It rides the existing `npm test` → pre-commit → CI chain. **No new hook.**
This is the gate that would have caught the Radiant/Rosette-Radar incident, and the one that will
catch the next keyword addition (D4).

*Caveat that must be written down:* three of the four repos are outside `bikar`. A test inside
`bikar/packages/core` cannot reach them. G1 therefore has to live where the corpus does — the
realistic form is a script in `bikar` that takes corpus roots from config, run by `bikar`'s CI over
`bikar/` alone (93 files) and by the `3d-models` Stop hook over the rest. §12 Q2.

**G2 — the reserved-word list is a fixture, and changing it is a reviewable diff.** Export
`KEYWORDS`' key set to a checked-in snapshot; a test asserts the map matches. Adding a keyword
then *cannot* be a silent one-line change — it is a diff against a fixture plus a G1 run over the
corpus. This converts D4 from "an incident class we remember" into "a lint". It is the direct
analogue of E2's closed gloss vocabulary and should copy E2's stale-entry reporting: a snapshot
entry for a keyword that no longer exists is reported, not ignored.

**G3 — the grammar's examples are executable.** Every `.bkr` snippet in `bikar/docs/grammar.md` is
extracted and parsed by a test; snippets marked `{invalid}` must fail. This is the entire
anti-drift mechanism for option (b), and it is why §5.2 says the grammar ships *with* the test or
not at all. It does not prove the grammar is complete — nothing can — but it proves every claim
the grammar makes is a claim `parser.ts` agrees with.

### 8.1 Triaged

| | Failure | Enforcement class |
|---|---|---|
| D1 column corruption | **not a gate** — it is a bug with a five-line fix; gate it only via a regression test on the fix |
| D2 hex validation leaks | **warning** initially — tightening the regex may reject files in the corpus; run G1 first to find out |
| D3 trigger/position mismatch | **gate (G3)** — the grammar names the five `HexColor` positions and the test asserts the trigger set covers them |
| D4 keyword collision | **gate (G2 + G1)** |
| D5 one error per file | **not enforceable** — it is a design choice, not a defect, until an editor consumes the parser (§10) |
| grammar drift | **gate (G3)** |

Three gates, three non-gates. As in `derivation-worksheet-design.md` §5.1, that ratio is
intentional: a documentation artifact that refuses to build is worse than one that builds with a
stated gap.

### 8.2 If a hook is wanted, extend the one that exists

The repo already runs `.claude/hooks/check-bkr-mesh.py` as a Stop hook, and there is already a
second dispatcher enforcing the use-case map on pointer-file commits. **The right move is to
extend the existing Stop hook to run G1 over changed `.bkr` files, not to add a third hook.** The
cost of that gate is already paid and its conventions are already understood.

### 8.3 What cannot be enforced

**No gate can establish that the grammar is complete.** G3 proves soundness (everything the
grammar claims, the parser agrees with); it says nothing about coverage. §6.1's coverage table is
a human-maintained honesty artifact, and it will rot unless someone updates it when a declaration
form is added. That obligation belongs to whoever adds the form, and no test can self-detect it —
the same asymmetry `derivation-worksheet-design.md` §5.1 records for E1's corpus floor.

Second: **no gate catches a grammar that is correct and useless.** A grammar that describes 6 of
64 node kinds passes G3 forever. Whether §6 grows is an editorial decision reviewed by a human or
not at all.

---

## 9. Migration risk

Only option (c) has migration risk, and it is worth pricing precisely rather than gesturing at.

**The oracle exists and is unusually good.** 327 files, 211,325 tokens, 53,693 lines, spanning
four repos and every declaration form the language has. A regenerated parser could be validated
by: parse all 327 with old and new, deep-compare the ASTs, require byte-identical JSON. That is a
genuinely strong differential test — far stronger than the 156 unit tests.

**But it is strong on acceptance and blind on rejection.** The corpus contains **one** invalid
file. A new parser that accepts a strictly larger language would pass a 326-file AST-equality
check perfectly. Every one of D2's three leaks (`#abcg`, `#abcdef0123`, `__hex_abc`) is invisible
to a corpus of valid files, because none of them appears in one. **A corpus of working programs
cannot validate a parser's rejection behaviour**, and rejection behaviour is where the five
defects live.

**And the diagnostics are not covered at all.** 99 `ParseError` messages, 18 `toThrow` assertions
in `parser.test.ts`. Even a perfect AST-equality result would leave ~81 messages unverified, and
§5.3's second reason says those messages are the main thing being risked.

**Decision: the 327-file corpus is adopted as the oracle for G1 and for any future parser change,
with the explicit caveat that it validates acceptance only.** Any option-(c) revival must first
build a *negative* corpus — invalid files with expected messages — and that work is a prerequisite,
not a follow-up.

---

## 10. Interaction with the parallel click-to-source design

*Flagged, not resolved. `docs/click-to-source-design.md` is owned by other work and is not
modified here.*

Two findings from this audit **raise** that proposal's cost, and one **lowers** it.

**Raises it — D1 means the position data is already wrong.** Click-to-source needs source spans
on AST nodes; `ast.ts` has zero position fields, so the spans would be built from
`Token.line`/`Token.column`. Those columns are **corrupted by +5 per hex literal on the line**
(§3.1) on **186 corpus lines across 298 files**. Any span mechanism built on today's tokens
inherits the bug. **`preprocessSource` must be fixed before, not after, spans are added** —
otherwise clicking a shape jumps five columns right of the truth on every styled line, and the
regression will be attributed to the span work rather than to the lexer.

**Raises it — token splicing destroys the source→node mapping for loops.** `expandFor`
(`parser.ts:3085-3129`) captures the body by indentation and splices the unrolled tokens into the
stream (`this.tokens.splice(this.pos, 0, ...expanded)`, `parser.ts:3129`), with positions copied
verbatim from the original body tokens. All *N* iterations therefore carry **identical
line/column**, and are indistinguishable by position. The same is true of `param` substitution,
which rewrites tokens in place preserving `line`/`column` (`parser.ts:793`). Exposure is small —
**2 of 327 files use `for`** — but the mechanism is silent, so it will present as "click-to-source
sometimes highlights the wrong iteration" rather than as an error.

**Lowers it — option (d) supplies spans *and* trivia as a side effect.** Both tree-sitter and
Lezer produce concrete syntax trees with positions on every node, retain whitespace and comments,
and recover from errors — which simultaneously closes the `ast.ts`-has-no-positions gap
(§5.4), the `consumeComment`-discards-everything gap (`lexer.ts:86`), and D5. **If
click-to-source concludes it needs a CST anyway, option (d) stops being a deferred nice-to-have
and becomes the cheaper path**, and this document's §5.4 deferral should be revisited jointly
rather than separately.

**Not resolved here.** Whether the right answer is "fix D1 and add spans to the hand-rolled
parser" (small, targeted, keeps one parser) or "adopt Lezer for the editor surface" (larger, gives
incremental + error-tolerant parsing, introduces a second grammar) is a decision that needs both
designs on the table at once.

---

## 11. Phasing

**Phase 0 — free, no grammar required.** Fix D1 (pad `__hex_` to preserve columns, or carry a
per-line column map). Add the regression test. Fix the two `language-reference.md` divergences
(§7) and the blueprint error-message enumeration (§6.2). *Nothing in this phase depends on any
decision in §5.*

**Phase 1 — option (b) + G1/G2.** Write `bikar/docs/grammar.md` covering §6's subset, with the
coverage table. Land G3 (executable examples) in the same change. Land G1 (327-file sweep) and G2
(keyword snapshot). *Trigger: none — this is the recommended next step.*

**Phase 2 — extend the grammar and add option (e) mechanism 3.** Grow §6 to cover `pattern` and
`style` bodies (the two most-used declaration forms after `blueprint`), then seed a `fast-check`
`letrec` generator from the grammar and fuzz for parser crashes and for accepted-but-invalid
inputs. *Trigger: Phase 1 landed and the grammar has survived one keyword addition.*

**Phase 3 — printer and round-trip.** A `.bkr` printer, then print∘parse idempotence over the
corpus. *Trigger: someone wants formatting, codegen, or a `.bkr` writer. Not before.*

**Phase 4 — option (d).** Only if click-to-source or an editor extension needs a CST. *Trigger:
§10's joint decision.*

### 11.1 Explicit scope-outs

- **No parser regeneration.** Not in any phase.
- **No new runtime dependency in `bikar-core`.** The zero-dependency property is preserved.
- **No changes to `parser.ts` semantics.** Phase 0 touches `lexer.ts` (D1) and one error message;
  nothing else. The language accepted by bikar does not change in any phase of this doc.
- **No error recovery.** D5 stays until §10 forces the question. Introducing synchronization sets
  into 115 parse methods is a larger change than anything else proposed here, and CPCT+-style
  minimum-cost repair (§Appendix A) is an LR technique that does not transfer to recursive descent.
- **No grammar for the 3D layer.** `orb`, `piece`, `wall`, `assembly`, `clip` bodies are the
  newest and most volatile syntax in the language; formalizing them now would document a moving
  target. Phase 2 stops at `pattern` and `style`.
- **No qiyas-side grammar.** qiyas has **no `.bkr` parser** — it generates files from `.bkr.tmpl`
  templates and shells out to the bikar CLI, and `validate_dsl_contract.py` validates the SVG
  `data-*` contract, not the DSL. There is exactly one parser, which removes the usual strongest
  argument for a shared formal spec.

---

## 12. Open questions

1. **The blueprint error message enumerates 12 of 14 allowed statements (§6.2).** Are `offset`
   and `fillet` intentionally undocumented-in-the-message, or is this an omission? The fix differs:
   add them to the message, or remove them from `BLUEPRINT_STARTERS`.
2. **Where does G1 live (§8)?** Three of the four corpus repos are outside `bikar`. Options:
   (i) a `bikar` script taking corpus roots from config, (ii) split — `bikar` CI covers its 93
   files, the `3d-models` Stop hook covers the rest, (iii) a corpus manifest checked into
   `3d-models`. (ii) is cheapest and matches how the repos already relate.
3. **What is the reversal trigger for §5.3 (do not generate)?** Proposed: any `.bkr` construct
   requiring lookahead > 2 or genuine backtracking. Should that be asserted mechanically — e.g. a
   test that fails if `peek(n)` with `n > 1` appears more than once in `parser.ts`?
4. **Should D2's regex be tightened (`#[0-9a-fA-F]{3,8}\b` plus a `__hex_` guard), given it may
   reject corpus files?** G1 answers this empirically; the question is whether a rejection is a
   bug fix or a breaking change.
5. **Does `girih-star4.bkr` stay in the corpus as a `must-fail` fixture, or does `star <k>` get
   implemented?** The file was committed as a witness for an unimplemented feature; leaving it
   permanently failing is defensible only if G1 pins its exact message.
6. **Should the 25 contextual keywords be enumerated in `tokens.ts` as a named set**, the way
   `KEYWORDS`, `MATH_FUNCTIONS`, and `ORB_SOLIDS` are? They are currently scattered across ~25
   inline `t.value === '…'` comparisons, which is the least greppable form and the hardest thing
   in the parser to keep a grammar synchronized with.
7. **Does §10's joint decision belong in this doc, in `click-to-source-design.md`, or in a third
   reconciliation note?** This doc deliberately does not resolve it.

---

## Appendix A — sources

All URLs below were fetched during this work unless marked otherwise. Quotations in §4 and §5 are
verbatim from these fetches.

**Hand-rolled front ends, with stated rationale**
- Clang, "Features and Goals" — https://clang.llvm.org/features.html *(quoted in §4.1)*
- GCC 4.1 release notes — https://gcc.gnu.org/gcc-4.1/changes.html *(quoted in §4.1)*
- rustc dev guide, "Lexing and Parsing" — https://rustc-dev-guide.rust-lang.org/the-parser.html
  *(states the lexer is hand-written; states no rationale for the parser — §4.1 marks this
  **unverified** for the parser)*
- `go/parser` package docs — https://pkg.go.dev/go/parser *(error recovery, `ast.Bad*`, positions)*
- V8, "Blazingly fast parsing, part 1: optimizing the scanner" — https://v8.dev/blog/scanner
  *(does **not** state hand-written vs generated; §4.1 marks V8 **unverified**)*
- TypeScript Compiler Notes glossary —
  https://github.com/microsoft/TypeScript-Compiler-Notes/blob/main/GLOSSARY.md *(does **not**
  state recursive descent; §4.1 marks TypeScript **unverified**)*
- TypeScript Architectural Overview wiki —
  https://github.com/microsoft/TypeScript/wiki/Architectural-Overview *(content moved to the
  Compiler Notes repo; no parser detail)*

**Geometry / CAD DSL front ends**
- OpenSCAD `src/core/parser.y` —
  https://github.com/openscad/openscad/blob/master/src/core/parser.y *(Bison: `%union`, `%token`,
  `%expect 0`)*
- Zoo / KittyCAD KCL parser —
  https://github.com/KittyCAD/modeling-app/tree/main/rust/kcl-lib/src/parsing *(`parser.rs`,
  `token/`, `ast/`, `math.rs`)* · dependencies —
  https://raw.githubusercontent.com/KittyCAD/modeling-app/main/rust/kcl-lib/Cargo.toml
  *(`winnow = "1.0"`; no `nom`/`pest`/`lalrpop`/`chumsky`)*
- Zoo KCL docs index — https://zoo.dev/docs/kcl-lang *(no grammar or parser statement)*

**Parser generators and parsing toolkits (JS/TS)**
- Peggy — https://peggyjs.org/ *("a simple parser generator for JavaScript that produces fast
  parsers with excellent error reporting"; PEG-based)*
- Nearley — https://nearley.js.org/ *(Earley; "effectively linear-time for LL(k) grammars";
  ambiguity returns all parses; "inverting parsers into generators for fuzzing")*
- Chevrotain — https://chevrotain.io/docs/ *("an internal JavaScript DSL", not a generator;
  "implements error recovery heuristics to parse even partially invalid inputs")*
- ANTLR — https://www.antlr.org/ *(parser generator; the page does **not** mention ALL(\*) —
  that attribution is **unverified**)*
- Langium — https://langium.org/docs/introduction/ *(grammar → AST + parser + LSP server)*

**Incremental / error-tolerant parsers for editors**
- tree-sitter — https://tree-sitter.github.io/tree-sitter/ *(four stated goals, quoted in §5.4)* ·
  grammar DSL —
  https://tree-sitter.github.io/tree-sitter/creating-parsers/2-the-grammar-dsl.html *(JavaScript
  `grammar.js`; precedence; GLR for genuine ambiguity)* · *(the ERROR/MISSING node documentation
  was **not found** at `using-parsers/1-getting-started.html` or `using-parsers/3-advanced-parsing.html`;
  that behaviour is **unverified** here)*
- Lezer — https://lezer.codemirror.net/ *(LR, incremental, error-insensitive, built for CodeMirror)*

**Grammar notations**
- W3C XML 1.0, "Notation" — https://www.w3.org/TR/xml/#sec-notation *("A - B means any string that
  matches A but does not match B")*
- RFC 5234, ABNF — https://datatracker.ietf.org/doc/html/rfc5234
- Ford, "Parsing Expression Grammars: A Recognition-Based Syntactic Foundation" —
  https://bford.info/pub/lang/peg/ *("solve the ambiguity problem by not introducing ambiguity in
  the first place")*
- Graphviz DOT language — https://graphviz.org/doc/info/lang.html *("Terminals are shown in bold
  font and nonterminals in italics.")*
- SVG 1.1 path data BNF — https://www.w3.org/TR/SVG11/paths.html#PathDataBNF *(BNF plus an
  out-of-band longest-match processing rule)*
- Zaytsev, "BNF WAS HERE: What Have We Done About the Unnecessary Diversity of Notation for
  Syntactic Definitions" — https://dl.acm.org/doi/10.1145/2034654.2034657 *(**HTTP 403**;
  `grammarware.github.io` index carries no listing either — cited from memory,
  **unverified**)*

**Grammars as test oracles**
- The Fuzzing Book, "Fuzzing with Grammars" — https://www.fuzzingbook.org/html/GrammarFuzzer.html
- Grammarinator — https://github.com/renatahodovan/grammarinator *("a random test generator /
  fuzzer that creates test cases according to an input ANTLR v4 grammar")*
- fast-check arbitraries index — https://fast-check.dev/docs/core-blocks/arbitraries/ *(lists
  `letrec` under Combiners; the dedicated `letrec` page 404'd at three URL variants, so the API
  detail is **unverified**)*
- McKeeman, "Differential Testing for Software," *Digital Technical Journal* 10(1), 1998 —
  **HTTP 403** at both `cs.cmu.edu/~jch/publications/mckeeman98differential.pdf` and
  `cs.dartmouth.edu/~mckeeman/references/DifferentialTesting.pdf`. Cited from memory,
  **unverified**.

**Error recovery**
- Diekmann & Tratt, "Don't Panic! Better, Fewer, Syntax Errors for LR Parsers," ECOOP 2020 —
  https://soft-dev.org/pubs/html/diekmann_tratt__dont_panic/ *(CPCT+; panic mode "often leads to a
  cascading chain of errors that drown out the original"; 98.37% of 200,000 Java files repaired
  within 0.5 s; error locations reduced from 981,628 to ~435,812)*

**In-tree primary sources** (paths relative to `/Users/omareid/Workspace/git/`)
- `bikar/packages/core/src/dsl/parser.ts` (3,993 lines) · `lexer.ts` (343) · `tokens.ts` (321) ·
  `ast.ts` (1,190)
- `bikar/packages/core/tests/dsl/parser.test.ts` (2,681 lines, 156 tests, 18 `toThrow`) ·
  `tests/canonical/starter-compile.test.ts`
- `bikar/docs/language-reference.md` (841) · `bikar/docs/engine-issues.md:62-65` ·
  `bikar/docs/lessons.md:387-402` ·
  `bikar/docs/decisions/2026-05-07-polygon-clipping-dep.md`
- `sacred-patterns/sessions/bikar-medallion-10/girih-network/girih-star4.bkr` (commit `fa12d1b`)
- `3d-models/docs/derivation-worksheet-design.md` §5.1, §8.5 (house style; gates E1–E3)

---

## Appendix B — contested bets and why they stand

**B.1 A prose EBNF that can drift from `parser.ts`.**
*Counter-evidence:* this is the strongest objection in the document, and it is the brief's own
warning — *a grammar that does not match `parser.ts` is worse than no grammar*. Documentation
drift is the default outcome, and §6 already found one divergence between `parser.ts` and its own
error message before the grammar even existed (§6.2). A generated parser (option c) makes drift
*structurally impossible*, which is a real advantage that §5.3 does not have a rebuttal for.
*Why the bet stands:* G3 makes every claim the grammar makes executable, so drift becomes a test
failure rather than a discovery. And the alternative that eliminates drift eliminates it by
**relocating** the layout logic into the grammar file (§5.3 reason 1) — at which point the grammar
contains imperative predicates and is no longer readable as a spec. **But the bet is real: if G3
is ever skipped, or the grammar grows faster than the test, this decision inverts and the honest
move is to delete the grammar rather than let it lie.**

**B.2 Keeping a hand-rolled parser for a language that is comfortably LL(2).**
*Counter-evidence:* §2.1 is the most inconvenient measurement in this document. The usual defence
of hand-rolling — "the language is not in a tractable grammar class" — is exactly what does *not*
apply here. bikar could be generated. 3,993 hand-written lines is a lot of code to maintain for a
grammar a generator would handle in a few hundred lines of declaration.
*Why the bet stands:* the 99 domain-specific diagnostics (§5.3 reason 2), the seven layout rules a
generator cannot express without escape hatches (reason 1), and the zero-dependency constraint
(reason 4). None of the five real defects is caused by hand-rolling, and two are made worse by
generating. **But "we could have generated this" is true, and anyone proposing a rewrite is not
being unreasonable — they are trading diagnostics for declarativeness, which is a legitimate
trade this project declines.**

**B.3 Calling the hex/comment preprocessor a latent hazard rather than a live bug.**
*Counter-evidence:* it rewrites source text before lexing, it corrupts 186 lines' worth of column
data (D1), it admits `#abcg` and `#abcdef0123` as valid colours (D2), and it hijacks the
`__hex_*` identifier namespace with no guard. That is four demonstrated failures, not a
theoretical concern, and calling it "latent" understates it.
*Why the bet stands:* the specific catastrophe — a genuine comment silently eaten as a colour —
could not be constructed after four probe families, because a comment `#` is either line-leading
(no trigger precedes it) or preceded by code that would have to end in a bare
`=`/`color`/`stroke`/`fill`. **But the reason the surface is empty is a convention, not a
mechanism: 0 of 327 files use a trailing inline comment, obeying a rule
`language-reference.md:838` states and `lexer.ts:86` does not enforce.** The first author who
writes `circle C0 center(0,0) radius 100  # outer ring` after a colour assignment on the same
line finds the edge. D1 and D2 should be fixed in Phase 0 regardless of anything else in this doc.

**B.4 Adopting the 327-file corpus as the oracle when 326 of them are valid.**
*Counter-evidence:* §9 says it outright — a corpus of working programs validates acceptance and is
blind to rejection, and all five defects live in rejection behaviour. G1 would pass with a parser
that accepts a strictly larger language. The corpus's headline number (327) is more reassuring
than the corpus deserves.
*Why the bet stands:* it is the only oracle that exists, it is free, it is 3.5× what
`starter-compile.test.ts` already uses, and it is precisely calibrated to the failure mode that
has actually bitten this project twice (keyword additions breaking shipped recipes). **The
mitigation is named and not deferred: §9 makes a negative corpus a prerequisite for any parser
change, and §12 Q4 routes D2's regex tightening through G1 to find out empirically what a
stricter parser would break.**

**B.5 Deferring tree-sitter/Lezer rather than deciding.**
*Counter-evidence:* deferral is the weakest kind of answer, and §10 shows option (d) would close
four gaps at once — spans, trivia, error recovery, incrementality — several of which other work is
about to pay for separately. Deciding "no" now and "yes" in six months means paying twice.
*Why the bet stands:* the decision is not this document's to make. A second executable grammar is
justified by editor requirements that neither this doc nor the parallel click-to-source doc has
established yet, and the divergence risk (§5.4) is categorically worse than prose drift because
*nothing detects it*. **This is recorded as an interaction to reconcile, not as a rejection —
and if click-to-source concludes it needs a CST, §5.4 should be reopened immediately rather than
waiting for Phase 4.**

**B.6 A grammar covering 6 of 64 node kinds, published as a real artifact.**
*Counter-evidence:* 9% coverage is not a language specification, and a `grammar.md` in
`bikar/docs/` will be read as one. A reader who checks their `pattern` body against it and finds
nothing has been misled by the file's existence.
*Why the bet stands:* §6.1's coverage table is mandatory and adversarial — it lists what is
missing before it lists what is present — and the alternative (wait for 100% coverage) means the
grammar never ships, which is how prose specs stay prose. Partial-but-honest beats
complete-but-imagined; the brief's rule was that a grammar not derived from `parser.ts` is worse
than none, and every production in §6 was derived by reading a cited line range and checked
against `parse()`. **But the failure mode is real and §8.3 names it: no gate can detect that the
coverage table has gone stale.**
