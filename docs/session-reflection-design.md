# Session-reflection: a measured FAQ that answers what sessions re-derive

**Status:** built (2026-09-25). `tools/session_reflect.py` ships
the three verbs of §4 and the fixture self-test of §8. [faq.md](faq.md) and its
empty sidecar `docs/faq-evidence.jsonl` exist, with no entries yet. The
`faq-questions` count authority is registered, `make validate-reflect` is at
the end of the Makefile, and the skill (§5) is written. The first real
`update-faq` run proposed 79 candidates that were mostly outline greps and
facts sessions already knew, so the tool now counts a session only when it
**re-derives** a fact (after a failure naming it, or by searching for it), not
when it uses it — [issues/faq-counted-use-not-rederivation.md](issues/faq-counted-use-not-rederivation.md).
The rerun proposes 6, which a person has to review. The census this rests on is
[research/session-reflection-census.md](research/session-reflection-census.md),
run 2026-09-17 over 17 main sessions + 176 subagent transcripts (241,226 lines,
80,203 assistant turns) with the prototype that preceded the tool. The proposal
file (docs/faq-proposal.md) is written in plain prose here, not backticked,
because it exists only after a run and a backticked path is a claim this repo's
pointer gate resolves on disk.

The problem this addresses is narrow and measured: sessions re-derive the same
repo facts, and the fix has to survive the failure the two precedents here
already diagnosed — a record nobody re-reads.

## 1. What the census established, and its limits (carried forward, not hardened)

The census measured four candidate signals and reported the precision of each by
hand-sampling. The design must carry those hedges, not launder them into
certainties:

- **Same-file re-reads (signal a)** separate cleanly into *one* no-write loop
  (a subagent read `parser.ts` 129 times, wrote nothing) and 22 edit-driven
  re-reads that are normal work. The no-write filter is load-bearing; a raw read
  count is not. The loop is **rare** — one instance across 3 repos / 25 main
  sessions / 256 subagent files — so any threshold built on it rests on a single
  positive (see §7).
- **Command shapes (signal b)** are dominated by git plumbing (~0/10 as a
  re-derivation); only a search verb carrying a code identifier (`grep <symbol>`)
  reads as a real re-lookup, at ~7/10.
- **Question shapes (signal c)** are a candidate-surfacing signal for a human,
  never an auto-answer: "let me check" is ~1/10, "where is"/"how does" ~4–6/10.
  Notably, sessions already hand-write FAQ-shaped `**Q-XXX — …**` blocks
  spontaneously, so the format below is observed, not imposed.
- **Known-fact probes (signal d)** are robust **by distinct-session count**, not
  by raw occurrence (inflated 3–10× by read-backs). The single hardest limit,
  stated in the census and inherited whole: *a transcript occurrence cannot be
  cleanly split into "re-derived from scratch" vs "recalled by reading the
  memory".* Memory existing did **not** zero recurrence. That is the fact the
  success metric (§3) has to be built to actually test, and the reason this is
  not a gate (§2).

## 2. Why a skill + tool, and not a gate

This repo's default answer to "should this be a skill?" is *no, a gate instead* —
[issue-register-evaluation.md](issue-register-evaluation.md) and
[dsl-extension-skill-evaluation.md](dsl-extension-skill-evaluation.md) both
reached it on measurement, and CLAUDE.md's Precedent section makes reading them a
precondition. So the burden is on this doc to show why the answer differs here.

A gate blocks a commit on a checkable invariant of the **diff in front of it**.
The thing this addresses — a session re-deriving a fact — leaves no artefact in
any diff. It happens in a transcript, after the fact, across sessions. There is
nothing at commit time to check and nothing to block. A gate is therefore not a
weaker or a stronger option here; it is not applicable, the same way the
link-checker was rejected not for strictness but because "does this URL resolve"
was the wrong invariant.

What *is* checkable is the invariant those evaluations actually endorse: **is
every load-bearing number attributed to a source a research file records as
fetched** — local, no network. This design keeps a gate for exactly that (§6, the
count marker and the evidence sidecar) and puts the *human-judgement* part — is
this cluster really one recurring question, and what is the answer — in a skill,
because the census proved (signal c) that clustering at useful precision needs a
person. The tool proposes; it never invents an answer (§5).

## 3. What stops this becoming "the register nobody re-reads"

Both precedents name the same failure: capture was never the bottleneck,
retrieval and incentive were; a register's success condition is *being re-read*,
not *being written*. Four design commitments answer it, each traceable to a
measurement rather than a hope:

1. **The FAQ is generated from the census, not hand-curated.** An entry exists
   only because the miner clustered it from real recurrence. A register decays
   when entries are added faster than they are read; here an entry cannot be
   added without a recurrence count behind it.
2. **Every entry carries its own recurrence metrics and evidence pointers**
   (sessions, occurrences, first→last date, sample session+line pointers). The
   entry states why it earns its place, so a reader can audit the claim the way
   this repo audits every other number.
3. **The success metric is falling recurrence after an answer ships, not the
   count of answers.** The tool re-censuses and reports, per answered question,
   whether sessions started *after* the answer date still re-derive it. Zero
   post-answer recurrence is success; continued recurrence re-opens the entry.
   This is the metric a register never has, and it is why writing more entries
   cannot be mistaken for progress.
4. **The metric is honest about the census's confound.** Post-answer recurrence
   is measured on **authored** hits (tool_use inputs the session generated), not
   read-backs, because the census showed raw occurrence conflates re-derivation
   with recalling the answer. Authored is still not enough: a session that
   *uses* a fact it already knows authors it too, and the first real run found
   that is nearly every use. So a hit counts only when the session re-derived
   the fact — a failure naming it, or a search for it, just before its first
   use (§4). A residual confound remains and is stated in the entry, not hidden.

## 4. The tool: `tools/session_reflect.py`

One file, three verbs. It never writes docs/faq.md itself; it writes a
proposal a human accepts (§5).

- **`census`** — streams every transcript (main + the `subagents/` subtree; the
  census documents why the subtree is not optional), classifies assistant blocks,
  and emits the four signals with session/occurrence counts and sample pointers.
  Read-only. (The prototype spelled it as a `--census` flag; the research file
  keeps that spelling because it records the run as it happened.)
- **`update-faq`** — clusters census hits into candidate questions, each with its
  metrics and evidence, and writes a *proposal* beside docs/faq.md (never the FAQ
  directly). Clustering is coarse on purpose: it groups by fact-probe and by
  normalised command/question shape and leaves the merge/split judgement to the
  human, per the signal-c precision finding. It also re-measures already-answered
  entries so their metrics stay live.
- **`show`** — prints one `## Q-NNN` (or the whole FAQ) with its live recurrence:
  the pre-answer re-derivation rate against the latest, flagging "answer not taking"
  when a shipped answer has not reduced recurrence (§3.3). This is the view that
  makes the FAQ falsifiable.

Choices the build made that this section left open:

- **Authored** means the probe matches content the assistant generated on that
  line (a tool_use input, a thinking block, a text block). Matching the raw line
  would count a tool_result echo, which is a read-back.
- **Re-derived** is narrower than authored. At the first line where a
  transcript file authors a fact, the session re-derived it if, within the 12
  lines before or on that line, a failed tool result names the fact or a
  `grep`/`rg` searched for the fact's term. Otherwise it *knew it*, which does
  not count, and neither does a failure after the first use. A search-command
  cluster counts a session when it greps for one specific name (§4 Candidates).
- **Recurrence** is the share of sessions that re-derived the fact, split by
  whether the session *started* before the answer date or on/after it. A
  subagent counts toward its parent session. Sessions, not occurrences, because
  §1 found occurrence inflated 3–10× by read-backs.
- **Candidates** come from the fact probes and from `grep`/`rg` command shapes
  only, following §1's signal-b finding that git plumbing is never a
  re-derivation, and a cluster must be *re-derived* in the minimum number of
  sessions. A grep counts only when its term names one specific thing: an
  identifier with an underscore, camelCase, or all caps of four or more
  characters. `grep ^##`, `grep export` and `find .` are outline scans; they
  made up most of the first run's 79 candidates. Question shapes are printed by `census` for a human
  to read, but never proposed, following signal c.
- **The proposal** is written to docs/faq-proposal.md by default. Each candidate
  carries a ready evidence line, so accepting it means pasting that line into
  the sidecar and adding the `answered` date.
- **`show` verdicts**: *taking* (post-answer share below pre-answer), *ANSWER NOT
  TAKING* (equal or higher), *pending* (no session since the answer), *no
  baseline* (nothing re-derived it before), *BROKEN* (an answered entry with no
  sidecar record). `--audit` exits nonzero on *not taking* and *BROKEN*.

The tool shares bikar's transcript reader semantics (`bikar:scripts/transcript.py`
and its `transcript-archaeology` skill) for authorship vs read-back. **Transfer
condition (K10):** that reader assumes subagents appear inline as
`isSidechain:true`; the census measured that this is **false** in the current
Claude Code layout (subagents are separate files under `subagents/`). So the
shared reader transfers only once it walks that subtree. This tool always has,
and bikar's reader has too since bikar #246 (2026-09-25), so the condition now
holds on both sides.

## 5. How the skill updates the FAQ (tool proposes, human confirms)

The [`session-reflect` skill](../.claude/skills/session-reflect/SKILL.md) runs the loop: `census` → `update-faq` → the human reads the
proposal, merges or discards clusters, and **writes the answer prose**. The tool
supplies everything measurable (the question cluster, counts, evidence pointers,
the anchored code pointer where the answer lives) and nothing judgemental: it
never writes an answer, because an invented answer is worse than an absent one —
the same reason `docs_gate.py`'s D3 accepts a bet id but not a bare number.

The human's edit is the only path by which prose enters docs/faq.md. The tool's
proposal is staged beside it and diffed, so what the human accepted is reviewable.

## 6. Formats

### docs/faq.md — one entry per recurring question

```
## Q-014 — What Node/PATH does this repo need?

**Answer.** v22.22.3, prefixed on every git/npm/tsx call. Grounded at
`3d-models:CLAUDE.md:L<n>` "v22.22.3".

metrics: re-derived in 4 sessions (after a failure 1, by searching 3, already knew it 90) · used in 13 · occ 14557 (authored 12980) · first 2026-07-29 · last 2026-09-17
evidence: faq-evidence.jsonl#q-014
```

- **Heading `## Q-NNN`** — a stable id, so a pointer to an answer survives edits.
- **Anchored code pointer** — the answer names where the fact lives as
  `repo:path:L<n> "literal"`, the repo-wide anchored-pointer form `validate.py`
  re-checks against the diff, so an answer that drifts is caught. (Shown here with
  a `<n>` placeholder; a real entry carries the line and literal.)
- **metrics line** — the recurrence evidence, in the census's robust unit
  (distinct sessions): how many re-derived it and how, how many used it, the
  authored/raw split and the date span. (The example's numbers are illustrative;
  the real Node fact is re-derived in 0 sessions.)
- **A count marker** pins the question total to the tool that computes it, in
  this repo's counts-gate syntax: the number, then `<!--count:faq-questions-->`.
  The authority in `counts_gate.py` counts the FAQ's entries with the tool's own
  `read_faq`, the same parser `show` and `update-faq` use. This section first
  planned to take the count from `census`, but census reads this machine's
  transcripts, which a fresh clone does not have. A committed count has to be
  re-checkable from the repo alone, so the build reads the file instead.

### docs/faq-evidence.jsonl — the sidecar

One JSON object per line, keyed by question id: the full session-uuid + line
pointers (the FAQ shows a short id; the sidecar holds the list), the pre-answer
and latest recurrence measurements, and the census run that produced them. It is
the audit trail behind every metrics line — the "attributed to a source the
research file records as fetched" invariant, made a file. It is not backticked
anywhere it is claimed to already exist.

## 7. The loop detector

Signal (a) is worth a standing check because its one hit was a real 8.5-hour
stall. The detector flags a `(session, agent, file)` triple whose read count
crosses a threshold **with zero writes by that agent**.

The threshold is **under-determined by the data**: the census holds exactly one
positive (129 reads) and the highest no-write non-loop is far below it, so no
honest number can be fit from one point. I therefore route the threshold to a
proposed calibration bet **CAL-LOOP-01** rather than asserting it. This is
deliberately **not** written with the `**Default:**` marker, because that marker
must be discharged by a *registered* bet and CAL-LOOP-01 is not yet minted — the
divergence is called out here rather than smuggled past the gate. A provisional
working value of 40 no-write reads sits ~3× above every non-loop observed and
~3× below the one loop; it is a placeholder pending the bet, not a grounded
default. Minting CAL-LOOP-01 (and gathering more positives) is an open question.

## 8. Verification

**Validator:** an answered question must show falling post-answer recurrence, or
be re-opened — measured on re-derivations, per §3.4.

- PASS: `Q-014` ships an answer dated 2026-09-18; `show Q-014` finds sessions
  started after that date re-derive the fact at a lower per-session rate than
  before, or not at all. The entry stays answered.
- FAIL: `Q-014`'s answer ships, yet post-answer sessions re-derive it at the same
  or higher rate. `show` flags it "answer not taking" and re-opens the
  entry. The register-failure mode (an answer written but not working) is thus a
  **loud** result, not a silent one.

**By-design failure is the load-bearing case.** The tool ships two fixture
transcript sets, built in a temp directory by the self-test itself: one with a planted re-derivation `census` must surface as a cluster
(the PASS), and one where an answer exists but recurrence continues, which `show`
must flag rather than pass (the FAIL). A reflection tool that only ever reports
"everything is answered" has stopped testing the thing it exists for — the
corollary CLAUDE.md draws for every gate here. `census --self-test` runs both
fixtures with fixed expectations, the way `counts_gate.py --self-test` pins its
authorities so it cannot go green by reading nothing. The PASS set also plants a
read-back-only session that must not count as authored, a hit reachable only
through a subagent file, and an edited file read 45 times that the loop detector
must leave alone. It plants the three ways to re-derive a fact (a hook failure,
a grep, a failure inside a subagent), a session that knew the fact and only hit
the failure afterwards, a fact every session types and none re-derives, and an
outline grep beside a specific-name grep. A mutant that counts every first use
as re-derived fails 4 of the 12 checks; one that drops the subagent walk and
counts read-backs fails 7.

## 9. Makefile target

Appended at the **end** of the Makefile (this repo's rule for new targets), and
running the tool's own self-test then a census, matching the `validate-docs` /
`validate-counts` shape:

```
# ---- session reflection (docs/session-reflection-design.md) ----
validate-reflect:
	$(PYTHON) $(ROOT_DIR)/tools/session_reflect.py census --self-test
	$(PYTHON) $(ROOT_DIR)/tools/session_reflect.py show --audit
```

It runs the tool's own self-test, then an audit that every answered entry still
verifies (`show --audit` exits nonzero on an "answer not taking"). It is not wired
into `validate` (the aggregate) until the FAQ has answered entries to audit. The
fixtures and the shared-reader port have both landed, so that is the one thing
left to wait for. Even then, the audit reads this machine's transcripts, so it
can join the local run but never a check that runs on a fresh clone.

## 10. Relation to memory and transcript-archaeology

- **Memory** (`.claude/memory/MEMORY.md`) holds cross-session *facts* a session
  should recall. The census measured that memory existing does not stop a fact
  being re-derived, so the FAQ is not a competitor to memory — it is the
  instrument that measures *whether memory (or any answer) is working*, and points
  at the specific fact still being re-derived. Memory is the answer store; the FAQ
  is the recurrence meter.
- **transcript-archaeology** (bikar's skill) reads one session to reconstruct what
  happened. This tool reads *across* sessions to count what repeats. They share a
  reader and answer different questions; neither subsumes the other.

## 11. Options considered

Rubric, per column: **0** = does not do it, **1** = partial, **2** = does it.
Columns: *Captures recurrence* (is an entry backed by measured repetition),
*Gets re-read* (is there a mechanism forcing retrieval/verification, the failure
the precedents named), *Grounded* (each number attributed to a fetched source),
*Cost* (2 = cheap).

| Option | Captures | Re-read | Grounded | Cost | Total |
|---|---|---|---|---|---|
| **C. FAQ generated from census (recommended)** | 2 | 2 | 2 | 1 | **7** |
| A. Memory only | 1 | 0 | 1 | 2 | 4 |
| B. FAQ hand-written | 1 | 0 | 0 | 2 | 3 |
| D. A gate | 0 | 1 | 2 | 1 | 4 |

- **C (recommended)** is the only option that scores on *re-read*, because the
  `show --audit` recurrence check is the mechanism the precedents say every register lacks. Its
  cost is 1, not 2: it needs the tool, the sidecar, and a human in the loop.
- **A. Memory only** is the status quo; the census measured its ceiling directly
  (recurrence continues after the memory exists). Cheap, but scores 0 on re-read.
- **B. FAQ hand-written** is the classic register the two evaluations rejected: no
  measured backing, no retrieval mechanism, decays into "a defensible argument
  that management is occurring."
- **D. A gate** scores 0 on capture because, as §2 argues, there is no commit-time
  artefact to check; it is not applicable to the recurrence problem, only to the
  attribution sub-problem, which C already absorbs.

## 12. Open questions

1. **Mint CAL-LOOP-01** and gather more loop positives before fixing the §7
   threshold; one data point cannot set it.
2. ~~Register the `faq-…` count authority.~~ Done 2026-09-25 as `faq-questions`
   (§6).
3. ~~Port the subagent-subtree fix to bikar's reader.~~ Done 2026-09-25, bikar
   #246 (§4).
4. **Clustering precision.** Signal (c) is ~4–6/10 at best;
   does `update-faq` over-propose enough to waste the human's time? Measure the accept/discard ratio
   on the first real run and treat a low accept rate as the signal to narrow.
   The first run was narrowed before review: 79 candidates, nearly all outline
   greps and known facts, became 6 once only re-derivation counted
   ([issue](issues/faq-counted-use-not-rederivation.md)). The ratio is still to
   be measured on those 6.
5. **Does the confound bite?** If `show`'s recurrence check cannot distinguish recall from
   re-derivation even on authored hits, the success metric weakens to "the fact is
   still being typed", which is softer than "still being re-derived". Watch the
   first answered entry closely.
