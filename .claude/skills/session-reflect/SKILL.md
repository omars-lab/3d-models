---
name: session-reflect
description: Find the repo facts that sessions keep working out from scratch, and keep the measured FAQ in docs/faq.md. Use when asked to reflect on past sessions, to find what keeps getting re-derived or re-looked-up, to add or audit an FAQ entry, to check whether an FAQ answer or a memory note actually stopped the repetition, to spot a subagent stuck re-reading one file, or when running tools/session_reflect.py. The tool measures and proposes; a person writes every answer.
---

# Session reflect

Sessions keep working out the same facts: which Node to use, where a gate lives,
what a hook blocks. Memory alone did not stop it; the census measured that. This
skill keeps a small FAQ of those facts, and it adds a question only when the
transcripts show it recurring. Every answer is then checked: after it ships, do
sessions stop re-deriving that fact?

The design and its reasons are in
[session-reflection-design.md](../../../docs/session-reflection-design.md). The
measurements behind it are in
[session-reflection-census.md](../../../docs/research/session-reflection-census.md).
The FAQ is [faq.md](../../../docs/faq.md).

## The one rule

**The tool never writes an answer, and neither do you on the tool's behalf.** The
tool finds candidate questions and counts them. A person decides which ones are
real, and a person writes the answer. An invented answer is worse than no
answer: it reads as settled while it is wrong. So when you reach the review step,
stop and hand the proposal over. Do not fill in answers so you can finish.

## The loop

All commands run from the repo root. By default they read this checkout's
transcripts under `~/.claude/projects/`, subagent files included. Add
`--also-project <repo path>` to count a sibling repo's sessions as well.

1. **Look.** `python3 tools/session_reflect.py census`
   It prints four signals. Only two of them turn into FAQ candidates:
   - *Known-fact probes* and *searches* (`grep`, `rg`) become candidates, but
     only in sessions that **re-derived** them. A session re-derives a fact
     when, at its first use, a failed tool result just before names the fact
     or it grepped for the fact's term. Typing a fact it already knew does
     not count. A grep counts only when it searches for one specific name
     (`BIKAR_DIR`, `patternSources`), not an outline scan like `grep ^##`.
     Section (d) shows each fact split three ways: after a failure, by
     searching, already knew it. The probes are a fixed list, `FACT_PROBES`
     in the tool, drawn from memory. To track a new fact, add one line there.
     Why the rule is this narrow: [the issue note](../../../docs/issues/faq-counted-use-not-rederivation.md).
   - *Question-shaped thinking* ("where is", "how does") is printed for you to
     read, but it is never proposed. The census found it right only 4 to 6 times
     in 10.
   - *Same-file re-reads* feed the loop detector. A session, agent and file
     read 40 or more times with **zero writes** from that agent is flagged as
     stuck. 40 is a placeholder: it rests on one real loop and waits on the
     calibration bet CAL-LOOP-01. Report a flag as "possibly stuck", never as
     proven.
2. **Propose.** `python3 tools/session_reflect.py update-faq`
   This writes docs/faq-proposal.md next to the FAQ. Each candidate has the
   number of sessions that re-derived it, how, and a ready evidence line. It also
   re-measures every question already answered. It never touches `docs/faq.md`.
   `--min-sessions N` (default 3) raises or lowers the bar for a candidate.
3. **Stop for review.** Tell the person the proposal is ready. Give them the
   candidate count and the top few, each with its session count. Then wait. The
   person merges, splits or throws away candidates and writes the answers. You
   can help them find where each fact lives. You can draft a pointer, but not
   the answer itself.
4. **Record what was accepted.** For each question the person keeps:
   - Add an entry to `docs/faq.md`, numbered with the next free three-digit id,
     in the shape the FAQ's "Entry shape" section describes. The answer names
     where the fact lives with an anchored pointer (repo, path, line and
     literal). The use-case validator then catches an answer that drifts away
     from the code.
   - Copy the candidate's evidence line into `docs/faq-evidence.jsonl`. Change
     `id` from `cand-NNN` to the entry's `Q-NNN`, and add
     `"answered": "YYYY-MM-DD"`, the day the answer ships.
   - Bump the `Questions tracked:` number. The count gate fails the commit if it
     disagrees with the entries.
   - Note how many candidates were kept and how many were thrown away. That
     ratio answers open question 4 in the design doc: does `update-faq` propose
     too much to be worth a person's time? Put it in the PR body.
5. **Check it.** `make validate-reflect` runs the tool's self-test, then
   `show --audit`. Ship the entries, the sidecar and the proposal in one PR, so
   the reviewer can compare what was proposed with what was kept.

## Reading `show`

`python3 tools/session_reflect.py show [Q-NNN]` compares, for each answered
question, the share of sessions that re-derived the fact before the answer date
with the share after it. It counts **re-derivations** only: a session that uses
the fact correctly with no failure and no search is the answer working, and is
not counted. A fact that merely came back in a tool result is not counted
either.

| Verdict | Meaning | What to do |
|---|---|---|
| taking | fewer sessions re-derive it since the answer | nothing |
| pending | no session has started since the answer | wait |
| no baseline | nothing re-derived it before the answer | question whether it belongs in the FAQ |
| ANSWER NOT TAKING | as many sessions or more still work it out | reopen: move the answer to where sessions look, or rewrite it |
| BROKEN | an entry has an answer but no evidence line with a cluster and a date | fix the sidecar |

`--audit` exits 1 on the last two. One caution remains: a session that greps
to *confirm* an answer it half-remembers looks the same as one that never knew
it. So "not taking" means "still being looked up". It is strong evidence, not
proof. Say so when you report it.

## Where this sits

- **Memory** is where answers live for recall. The FAQ measures whether an answer
  (in memory, CLAUDE.md or a doc) is working. When an answer is not taking, the
  usual fix is to move it somewhere sessions actually read.
- **bikar's transcript-archaeology** reads one session in depth. This skill counts
  what repeats across many. Pointers here are `<session-uuid> <line>`, which is
  the same form that skill's `show` takes, so you can open any sample it lists.
- `make validate-reflect` is not part of `make validate`. It reads this
  machine's transcripts, which a fresh clone does not have.
