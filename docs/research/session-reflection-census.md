<!-- provenance: date=2026-09-17; produced-by=claude-opus-4-8 (session_reflect.py --census prototype, run by hand); feeds=docs/session-reflection-design.md; scope=measured census of the local Claude Code transcripts for 3d-models, with a glance at the bikar and youtube sibling slugs -->

# Session-reflection census — what actually gets re-derived

A **measured** census of the Claude Code transcripts on this machine, produced
to feed `docs/session-reflection-design.md`. Every number here is a count from
`tools/session_reflect.py --census`, not an impression. Where a signal was
hand-sampled for precision, the sample size and the hits/real verdict are stated
inline, the way this repo's counts gate was calibrated ("9 hits, 9 real").

**Evidence-pointer convention.** A pointer is written `session <uuid8> line <n>`
in plain prose (never a backticked path — a transcript path ends in `.jsonl` and
the pointer gate would try to resolve it). Line numbers are **0-based**, the same
index bikar's `scripts/transcript.py show`/`entry` take, so a pointer is directly
openable. Full 32-char session/agent ids and every sample line live in the JSON
sidecar the run wrote (not checked in; regenerate with the command below).

## How this was run

The miner streams each transcript line by line (files reach ~292 MB; none is ever
read whole) and classifies assistant `message.content[]` blocks into
thinking / text / tool_use. Exact command, from the repo root with the pinned
Node on PATH:

```
python3 tools/session_reflect.py --census \
  --project=-Users-omareid-Workspace-git-3d-models \
  --min-reads 20 --json <scratch>/census_3dm.json
```

The sibling slugs `-Users-omareid-Workspace-git-bikar` and
`-Users-omareid-Workspace-git-youtube` were run the same way (`--min-reads 25`).
Authorship vs read-back follows bikar's reader (`scripts/transcript.py`) and its
`transcript-archaeology` skill: a hit in a **tool_use input** is
authorship; a hit in a **tool_result/attachment** is a read-back. This prototype
does **not** yet import that reader — see the design doc's "shared reader" section
and social-presence-hub technique #19 ("two repos carry independent JSONL
readers").

## The corpus (3d-models slug)

- **17 main-session transcripts + 176 subagent transcripts = 193 files**, 241,226
  lines, **0 parse errors**, 80,203 assistant turns. (An 18th top-level file is a
  250-byte `orphaned` stub, skipped. The brief's "18 sessions / 887 MB" counts the
  stub and the subagent subtree; the main files are ~0.7 GB, the subagent subtree
  ~190 MB.)
- tool_use totals: Bash 27,385 · Edit 5,505 · Read 4,456 · WebFetch 1,286 · Write
  942 · WebSearch 688 · ToolSearch 585 · Agent 180.

### Structural correction — subagents are a separate file tree, not `isSidechain`

The brief (and bikar's reader) assume subagents appear inline in the main file as
`isSidechain:true` with an `agentId`. **In this corpus that is false: `isSidechain`
appears zero times.** The current Claude Code layout writes each subagent to its
own file at `<slug>/<session-uuid>/subagents/agent-<agentId>.jsonl`. A top-level
`*.jsonl` glob (bikar's `transcripts()`, and this miner's first cut) silently drops
all 176 subagent files — **which is exactly where the one real loop lives.** The
miner was corrected to recurse into `*/subagents/agent-*.jsonl` and to key reads by
`(session, agent, file)` so a subagent's behaviour is not merged into its parent's.
This is a transfer-condition finding for the design (K10): the shared reader must
walk the subagent subtree, or every subagent signal reads as zero.

---

## Signal (a) — same file read many times by one agent

23 `(session, agent, file)` pairs cross 20 reads. **Only one is a re-read with no
matching write by that agent** — the loop the brief predicted:

| reads | writes by agent | kind | session · agent | file | span |
|---|---|---|---|---|---|
| **129** | **0** | subagent | session 82a84811 · agent afe38a5fa616 | bikar-constructions parser.ts | 06:18→14:48Z (8.5 h) |
| 85 | >0 | main | session 27e89d38 · main | bikar parser.ts | 3.8 h |
| 78 | >0 | main | session 27e89d38 · main | bikar evaluator.ts | — |
| 77 | >0 | main | session 27e89d38 · main | 3d-models lego-lab-design.md | — |

Pointer to the loop: **session 82a84811 line 266** is its first Read of
`parser.ts`; it wrote nothing in 6,199 lines.

**The distinction the brief asked for holds cleanly.** The other 22 pairs are all
`wrote=True`: an agent re-reading a file it is actively editing across a long
design/build session. That is normal work, **not** a re-derivation and **not** a
loop. Split by the wrote-by-that-agent flag, the corpus separates 1 loop from 22
edit-driven re-reads.

**Cross-repo confirmation of rarity.** bikar (6 sessions, 54 subagent files, 8
pairs ≥25 reads) and youtube (2 sessions, 26 subagent files, 8 pairs ≥25 reads)
each show **zero** no-write loops — every high-read file there was also written.
So across 3 repos / 25 main sessions / 256 subagent files the no-write loop occurs
**once**.

**Precision: 1 hit, 1 real (the wrote=False + high-count filter).** The signal is
precise but rare, and a pure read-count threshold cannot separate the loop (129,
no write) from productive editing (youtube `ggb_build.py` 101 reads *with* writes;
bikar evaluator 66 with writes) — **the no-write filter is load-bearing, the count
alone is not.** With a single positive, the threshold is under-determined by data
(see the design doc's calibration note).

---

## Signal (b) — repeated command shapes across sessions

Command shapes were normalised to `verb + first-non-flag-arg` (digits → N). The
head of the ranking is git plumbing, repeated in nearly every session:

| sessions | occ | shape |
|---|---|---|
| 7 | 504 | git status |
| 7 | 449 | git commit |
| 7 | 262 | git diff |
| 6 | 2891 | sed N,Np (range print) |
| 5 | 201 | grep export |
| 5 | 80 | grep function |
| 5 | 73 | grep interface |

**Precision, hand-read: git/sed plumbing is ~0/10 as a re-derivation** — it is
workflow, not a repeated *question*. The re-derivation-bearing rows are the
**symbol greps**: `grep -rn "export interface Face"` (session 27e89d38 line 1121),
`grep -n "function countGeometricVertices\|function resolveFaceClass"` (session
27e89d38 line 1134), `grep -n "interface Face" src/graph/` (session 27e89d38 line
171) — the same engine symbols searched again in 4–5 sessions. Sampling 10 of the
"grep <identifier>" hits, **~7/10 are a genuine re-lookup of a code location** a
FAQ entry with a code pointer would answer; the other 3 are one-offs. **So (b)
works only when filtered to a search verb (grep/rg/find) carrying a code
identifier, and is near-useless across git plumbing.** Note the counts are
dominated by session 27e89d38 (the 292 MB session); session *breadth* is the
trustworthy column, raw occ is not.

---

## Signal (c) — question-shaped thinking/text blocks

| sessions | occ | shape |
|---|---|---|
| 11 | 2087 | "let me check …" |
| 8 | 219 | "let me find …" |
| 7 | 27 | "need to check/verify …" |
| 5 | 15 | "where is/are/does …" |
| 4 | 15 | "how does/do …" |
| 4 | 6 | "what is the …" |
| 0 | 0 | "which file …" |

**Precision, hand-sampled 10 each:**
- **"let me check" — ~1/10 as a recurring repo re-derivation.** It is a procedural
  narration tic ("let me check the working tree state" session 27e89d38 line 513;
  "let me check for orphaned test processes" line 392). High volume, low precision —
  the textbook "cries wolf" signal. **Must not drive clustering.**
- **"where is" / "how does" — 10/10 are grammatical questions, but only ~4–6/10 are
  the kind a repo FAQ answers.** The rest are design rhetoric ("where does authoring
  help live?" session 27e89d38 line 8072) or user-directed ("How do you want these
  handled?" session 332d42c3 line 33100).
- **Unexpected, and the strongest (c) finding:** several hits are *already
  FAQ-shaped blocks the session wrote by hand* — `**Q-HOME — Where does the shared
  drawing code live?**` (session 792c03e6 line 10545) and `**Q-DATA — How does
  qiyas score data reach the picture?**` (session 792c03e6 line 10545). Sessions
  spontaneously mint `**Q-XXX — <question>**` blocks with answers, which is direct
  evidence the FAQ format proposed in the design is a natural shape, not an imposed
  one.

**Verdict:** (c) is a *candidate-surfacing* signal for a human, never an
auto-answer signal, and only the low-volume "where is/how does" shapes with an
"authored + immediately followed by a Read/Grep" filter are worth clustering.

---

## Signal (d) — known recurring repo facts (literal probes)

Probes drawn from `.claude/memory/MEMORY.md`. **The robust metric is session-count**
(how many distinct sessions touch the fact); raw occurrence is inflated by read-backs
and by single-session deep-dives, and the authored/read-back split matters.

| sessions | occ | authored | first→last (UTC) | fact |
|---|---|---|---|---|
| 13 | 14557 | 12980 | 07-29 → 09-17 | v22.22.3 Node PATH prefix |
| 13 | 5259 | 1258 | 07-23 → 09-17 | `make validate` is the only CI |
| 13 | 4175 | 408 | 07-23 → 09-17 | gh-pages is a diverged branch |
| 13 | 1626 | 254 | 07-28 → 09-17 | use-cases hook / USE_CASES_OK |
| 12 | 1810 | 522 | 07-31 → 09-17 | dotenvx version on PATH |
| 12 | 1190 | 112 | 07-30 → 09-17 | D-id collision (next decision id) |
| 12 | 960 | 180 | 07-23 → 09-17 | sibling worktree add |
| 11 | 1585 | 215 | 07-25 → 09-17 | npm ci/install in a fresh worktree |
| 10 | 5609 | 838 | 07-23 → 09-17 | ci/e2e/gitleaks required on bikar main |
| 2 | 98 | 34 | 09-17 → 09-17 | THREED_MODELS_DIR on bikar commits (emerging) |

**Precision / interpretation, hand-read:**
- The **v22.22.3 Node prefix** tops the list (12,980 authored) but is a special case:
  it is *typed into almost every Bash command* because it must prefix each one. That
  is a re-*application* cost, not a re-*discovery* — a FAQ answer will not remove it
  (a shell profile or an allow-listed wrapper would). Flagged so the design does not
  miscount it as a re-derivation win.
- **D-id collision** occurrences are almost all read-backs of `decisions-log.md`
  (sampled 12/12 at session 27e89d38 lines 25932–40410 are read-backs), so its raw
  occ overstates re-derivation; its **12-session breadth** is the real signal.
- **use-cases hook** occ is inflated by one deep-dive (session 27e89d38 lines
  10979–11007 in a single investigation); again the 13-session breadth is what
  matters.

### Before / after the memory file existed

Memory files carry an `originSessionId`; the file's own creation date bounds "after".
Example: the **D-id collision** memory file entered the repo 2026-09-07, yet the
fact still appears in sessions dated 09-09, 09-10, 09-13 and 09-17. **Literal
recurrence does not drop to zero once the memory exists.** Honest caveat, and the
central measurement limit of this census: *a transcript occurrence after the memory
exists cannot be cleanly separated into "re-derived from scratch" vs "recalled by
reading the memory".* The authored-in-tool_use count is a better proxy than raw occ
but still imperfect (writing `decisions-log.md` counts as authored). What the data
*does* support, and no more: **memory existing did not zero the recurrence** —
consistent with `docs/issue-register-evaluation.md` §1.3 ("written ≠ re-read"). This
is the finding the design's success metric has to be built to actually test.

---

## Top re-derivations, ranked (feeds the FAQ seed list)

Ranked by session-breadth (robust) then interpreted into a question shape:

1. **What Node / PATH does this repo need?** — v22.22.3 prefix, 13 sessions (re-application, not re-discovery).
2. **What checks gate a commit / what is "CI" here?** — `make validate` only; ci/e2e/gitleaks on bikar main — 13 / 10 sessions.
3. **What is gh-pages and can I merge it?** — diverged branch, never merge — 13 sessions.
4. **Why was my commit blocked (use-cases hook)?** — USE_CASES_OK override — 13 sessions.
5. **How do I handle secrets / dotenvx here?** — 12 sessions.
6. **What's the next decision id / how do I avoid a D-id collision?** — 12 sessions.
7. **How do I make a sibling worktree without disturbing the shared checkout?** — 12 sessions.
8. **What must I run in a fresh worktree?** — npm ci/install — 11 sessions.
9. **Where does the shared render/drawing code live, and how does qiyas data reach it?** — spontaneously written as `**Q-HOME**`/`**Q-DATA**`, session 792c03e6.
10. **THREED_MODELS_DIR on bikar commits (registry hook)** — 2 sessions, emerging.

Plus the flagship signal-(a) instance: the afe38a5 subagent's 129-read, zero-write
loop on `parser.ts` (session 82a84811 line 266).

## Which signals held up, and at what precision

| signal | keep? | filter that makes it work | measured precision |
|---|---|---|---|
| (a) same-file reads | **yes** | per-agent, `wrote=False` by that agent | 1 hit / 1 real; rare (1 in 3 repos) |
| (b) command shapes | partial | search verb + code identifier only | ~7/10 for `grep <ident>`; ~0/10 for git plumbing |
| (c) question shapes | candidate-surface only | "where is"/"how does" + authored + followed-by-tool | ~4–6/10; "let me check" ~1/10, drop it |
| (d) literal probes | **yes, by session-breadth** | authored count + distinct-session count, not raw occ | breadth robust; raw occ inflated 3–10× by read-backs |

## Limitations

- **One dominant session.** 27e89d38 (292 MB) supplies most raw occurrences; session
  breadth is used instead of occ wherever possible, but the corpus is not balanced.
- **occ ≠ re-derivation.** Read-backs and single-session deep-dives inflate raw occ;
  the authored/read-back split mitigates but does not remove this.
- **memory-recall vs fresh-derivation is not separable** from literal counts (above).
- **The fact probes are a hand-picked list**, so signal (d) measures *known* recurring
  facts, not an exhaustive discovery of all of them — an exhaustiveness claim would be
  a K2 defect. Discovery of *unknown* recurring questions rests on (b)/(c), which are
  candidate-surfacing at the precisions stated, not exhaustive.
- **Prototype reader.** The miner does not yet share bikar's authorship classifier;
  the authored/read-back flag here is a per-line approximation (does the line carry any
  tool_use/thinking/text block), not the per-hit block attribution bikar's reader does.
