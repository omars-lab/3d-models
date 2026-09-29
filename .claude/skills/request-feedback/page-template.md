# The page — shape and writing rules

The [`request-feedback`](SKILL.md) skill reads this every run. The first page written this way is
[2026-09-29-open-calls](../../../docs/working-model/feedback-requests/2026-09-29-open-calls.md).
Copy its shape.

## Shape

```markdown
---
date: <yyyy-mm-dd>
---

# Open calls — <yyyy-mm-dd>

<Two or three sentences: how many calls; how to answer (tick one box per call, or comment
on a line); what happens next (the next session records each answer and moves the task).>

| # | Call | My pick | Why, in one line |
|---|---|---|---|

## 1. <The call in plain words>

**In short.** <Three to six sentences: what the thing is, what is already built, what the
choice changes. Link the design doc for the full argument.>

![<what the picture shows>](<page>-media/<file>.png)

| Option | Pros | Cons | What it leads to |
|---|---|---|---|
| **<pick>** (my pick) | ... | ... | ... |

**Your answer:**

- [ ] <option>
- [ ] <option>
- Notes:

## Things only you can do (not decisions)
```

## Rules

- **Plain words.** Write it so Omar could read it cold, on a phone. No house shorthand, no
  ticket numbers standing in for names, no ids without a word saying what they are.
- **Every option has pros, cons and what it leads to.** "What it leads to" is the next piece
  of work it starts, or the door it closes. A bare label with a cost is not an option.
- **Mark one pick** and give its reason in one line. Leaving things as they are is an option
  only if its cost is written out like the others.
- **Pictures before tables.** A call about a shape gets the shape. Caption what the picture
  cannot say itself: the scale, what each color means, and whether it shows the value being
  decided or a stand-in (for example, "the strip shows 1 and 2 mm; the proposal is 0.6").
- **Keep the source's hedges.** "Worked out from the layer count, not measured" stays in the
  sentence. An untested claim is not written as a fact.
- **One tick-box list per call, with a Notes line.** Where one call has two parts, split it
  (4a, 4b) so each part gets its own list.
- **Owner actions are not calls.** They go in the closing list, one line each.
- **Links must resolve** (the docs gate checks them). Put no backticks round a path that is not
  in this repo, and never link the FAQ proposal, which is Omar's untracked file.
