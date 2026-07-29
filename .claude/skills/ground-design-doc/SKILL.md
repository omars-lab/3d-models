---
name: ground-design-doc
description: Enrich a design doc with source links via adversarial deep research — verify existing citations, hunt counter-evidence, and capture divergence justifications with links
argument-hint: <path/to/design-doc.md> [more docs...]
---

# Ground a design doc with sources — including the ones that disagree

Take the design doc(s) in `$ARGUMENTS` (ask which doc if none given) from
"claims things" to "every load-bearing claim traces to a link, and every contested
bet records the strongest counter-source plus why we diverge."

A doc is **grounded** when all four hold:

1. Every load-bearing claim (number, threshold, architecture bet, novelty claim) has a
   working link to a primary source that actually says what we claim it says.
2. The full research behind the doc is **checked into the repo** (`docs/research/*.md`),
   not living only in a conversation transcript.
3. Counter-evidence is captured: for each major bet, the strongest refuting source is
   linked with a fair one-line summary of its position.
4. Each divergence has due justification in the doc — or, if the counter-evidence wins,
   the design changed instead.

## Process

### 1. Identify the load-bearing claims

Read the doc. List the ~8–12 claims the design would not survive losing: specific
numbers/thresholds, "X is the standard approach" assertions, architecture bets
("we don't need Y"), and especially **novelty claims** ("no existing system does Z") —
those are the easiest to falsify and the most embarrassing when wrong.

### 2. Launch one adversarial research agent per doc

Use the Agent tool (general-purpose, background, parallel when auditing several docs).
The agent's mandate is two-sided — verify AND refute. Prompt template:

```
You are an adversarial research auditor for a design doc. Your job is NOT to confirm
the doc — it is to find where it is ungrounded, where its citations don't support its
claims, and where credible sources disagree with its approach. You have web access
(WebSearch, WebFetch) and file read access.

Repo: <absolute repo path>
Doc under audit: <path>
Supporting research on file: <paths to docs/research/*.md the doc cites, if any>
Context: <2-4 sentences: what the system is, what the doc proposes>

Steps:
1. Read the doc (and its research files) fully. Enumerate the ~8-12 most load-bearing
   claims and design bets.
2. Deep-search for COUNTER-EVIDENCE on each major bet. Attack hard:
   <per-doc steers: for each bet, name the strongest opposing position you can think
   of and tell the agent to steelman it — e.g. "find sources arguing <simpler
   alternative> is simply fine", "try HARD to refute the novelty claim: check
   <specific prior-art candidates>", "find credible sources giving DIFFERENT numbers
   and note the spread">
3. Spot-check the top 5 existing citations: fetch them and confirm they say what the
   doc claims (quotes, numbers, attributions).
4. For each major bet: GROUNDED (supporting link) / CONTESTED (credible refuting link
   found — include it) / UNGROUNDED (no evidence either way).
5. Where the approach still stands despite counter-evidence, DRAFT a 2-4 sentence
   divergence justification quoting the refuting source's position fairly. Where the
   counter-evidence should change the design, say so explicitly and flag it.

Deliverable — your final message is consumed as raw markdown data, not prose:
# Grounding audit: <doc>
## Claim-by-claim verdicts        (table: claim | verdict | supporting URLs | refuting URLs)
## Counter-evidence deep dives    (one subsection per bet; URLs + one-line summaries of
                                   what each source ACTUALLY says)
## Citation spot-check results
## Misgrounded or missing citations
## Recommended doc changes        (quotable divergence-justification paragraphs ready to
                                   paste, claim qualifications, new sources)

Rules: never fabricate a URL or a source's position; mark anything not fetched as
(unverified snippet). Prefer primary sources (standards bodies, official docs/source,
papers, manufacturer specs) over blog spam. Aim for 10-20 high-quality
refuting/complicating sources total.
```

### 3. Apply the results (after the agents report back)

- **Preserve the report verbatim** in `docs/research/<doc-slug>-grounding-audit.md` with
  a short HTML-comment provenance header (date, produced-by, which doc it feeds). Extract
  it from the agent transcript with jq rather than retyping it:
  `jq -rs '[.[] | select(.type=="assistant") | .message.content[]? | select(.type=="text") | .text] | last' <task output file>`
- **Fix misgrounded citations first** — a link that doesn't say what we claim is worse
  than no link.
- **Appendix A — survey sources**: linked source list; points at the research file(s)
  plus headline primary URLs. No prose-only source naming ("per the XYZ guide" with no
  URL is the failure mode this skill exists to prevent).
- **Appendix B — counter-evidence and divergences**: one entry per contested bet:
  the counter-position with its link and a fair summary, then either (a) our
  justification for diverging, or (b) the design change we made because the
  counter-evidence won. Never bury a lost argument — changing the design is a success
  outcome of this skill, not a failure.
- Deliberately-uncited defaults (calibration targets, placeholders pending physical
  evidence) are fine **only if labeled as such** with the mechanism that will firm
  them up.

### 4. Verify and ship

- Cross-references must be section-accurate: check that `research file §N` actually
  contains what you cite (`grep -n '^## ' docs/research/<file>.md`).
- Relative links must resolve from the doc's directory.
- Commit with a message that says what got grounded/qualified/changed; follow the
  repo's commit-trailer conventions.

### 5. Hand the empirical residue to `calibrate` — never let the trail stop

An UNGROUNDED verdict is not a finished verdict. Split every one of them:

- **ARGUED** — sources or reasoning could still decide it and the search was
  merely incomplete. It stays here: search harder, or record the gap in Appendix B
  as an open question with what was checked.
- **EMPIRICAL** — no literature *can* decide it, because a printer decides it (a
  fit gap, a wall floor, a bridge span, an overhang angle, warp, bed contact,
  hole compensation). It leaves this skill.

Every EMPIRICAL residue is registered as a **CAL bet** via the sibling `calibrate`
skill, and the doc's Appendix B entry cites the bet id in its heading —
`### B.3 The fit ladder — … [CAL-FIT-01]`. Registration is what makes the bet
enumerable; the citation is what lets a later reader of the doc find the coupon
instead of re-opening the argument. Both, or neither counts.

Two rules that decide the hard cases:

- **Misfiling an ARGUED claim as a bet is the failure mode of this handoff** — it
  buys a print to answer a question a citation would have answered for free.
  When a claim is genuinely ambiguous, leave it untagged and say so in the audit
  record. Fewer correct bets beat a full-looking table.
- **The same quantity open in two docs is one bet, not two.** Check the existing
  registry before minting an id: `FIT_GAP_MM` was independently unresolved as
  c2 Appendix B.3 *and* piece-composition B.2, with two coupons planned to
  measure one number. Cluster by *the measurement that settles it*, not by the
  doc it came from.

A bet with no coupon still gets registered, marked OPEN, with the apparatus it
needs named — an honest gap beats an invented coupon. Nothing here may mark a bet
settled: that needs the physical object, and it belongs to `prototype` and
`calibrate` (bikar Tenet 30).

## Rules

- Never fabricate a URL or a source's position. Unfetched search snippets are marked
  `(unverified snippet)` in research files and never promoted into a design doc.
- Quote counter-positions fairly — a strawmanned refutation is worthless as a record.
- Prefer primary sources; one standards document beats five blog posts.
- Novelty claims must be qualified with what WAS checked ("none of the N surveyed
  systems…"), never stated absolutely.
- Link rot happens: restate load-bearing numbers/claims in the research file itself so
  the doc survives dead links.
