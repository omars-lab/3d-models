# FAQ — the questions sessions keep re-deriving

Every entry here answers a question that the transcripts show sessions working
out from scratch, again and again. An entry is added only when that repetition
has been measured; nobody adds one on a hunch. Each answer is then held to a
test: once it ships, do later sessions stop re-deriving the fact? The design,
and why this is a measured FAQ and not a hand-kept register, is in
[session-reflection-design.md](session-reflection-design.md).

Questions tracked: 0 <!--count:faq-questions-->

## How an entry gets here

1. `python3 tools/session_reflect.py update-faq` reads the transcripts and
   writes a proposal next to this file: candidate questions, each with how many
   sessions worked it out and a ready evidence line. It never edits this file.
2. A person reads the proposal and merges, splits or throws away candidates.
   For each one kept, they write the answer themselves.
3. The accepted entry goes below, and its evidence line goes in the sidecar,
   `docs/faq-evidence.jsonl`, with `answered` set to the day the answer ships.
4. `python3 tools/session_reflect.py show --audit` (also `make validate-reflect`)
   re-measures every answered entry. If sessions after the answer still work the
   fact out as often as before, the entry is flagged "answer not taking" and
   reopened.

## Entry shape

Each entry is a level-two heading of the form "Q-NNN — the question", with a
stable three-digit id so links to it survive edits. Under it:

- **Answer.** Written by a person, never by the tool. It names where the fact
  lives with an anchored pointer (repo, path, line and literal), so an answer
  that drifts from the code is caught by the use-case validator.
- **metrics:** the line the proposal supplies: distinct sessions, occurrences
  (authored and total), and the first and last date seen.
- **evidence:** the entry's id in the sidecar, which keeps the full list of
  session and line pointers behind the metrics.

No questions have been accepted yet. The first `update-faq` run is waiting for a
person to review it.
