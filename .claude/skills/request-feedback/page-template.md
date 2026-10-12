# The page — shape and writing rules

The [`request-feedback`](SKILL.md) skill reads this every run. Copy the shape of
[2026-10-12-bottom-slits](../../../docs/working-model/feedback-requests/2026-10-12-bottom-slits.md):
it opens on a marked-up photo, and each option has its own picture.

Why the shape changed: the first version of that page followed the older shape here (summary
table first, a paragraph of "In short", one picture per call). Omar opened it and said "im not
seeing any pcitrues, explantions, etc that are simple to follow along". The pictures were there,
below a screen of text. So the picture now comes first, and the words shrink to captions.

## Shape

```markdown
---
date: <yyyy-mm-dd>
---

# <The question in plain words>

<One line: what to do on this page (tick one box per call) and what happens after.>

![<what it shows>](<page>-media/<the problem>.jpg)

*<One line saying what to look at in the picture.>*

## What we learned

- <Three bullets at most, one short sentence each.>

## Pick one

### 1. <Option in plain words> (my pick)

![<what it shows>](<page>-media/option-1.png)

<Two or three short sentences: what we would do, what it would show.>

### 2. <Option>

...

| | Pros | Cons | What it leads to |
|---|---|---|---|
| **1. <option>** | ... | ... | ... |

**Your answer:**

- [ ] 1. <option>
- [ ] 2. <option>
- Notes:

## Things only you can do (not decisions)
```

A page with more than one call repeats `## Pick one` per call (`## Call 2: <question>`), and adds a
summary table of the calls under the first picture: `| # | Call | My pick | Why, in one line |`.

## Rules

- **Open on a picture.** The first thing under the title is the picture of the problem. Use a
  close-up, mark the spot with a circle or an arrow, and put a word label on each half
  ("S: normal settings", not "S"). A screen of text before the first picture is the failure this
  rule is for.
- **Every option gets its own picture** of what it changes. With no photo to hand, draw it, and
  say in the picture that it is a drawing, not to scale. A picture of "stop" is the thing as it
  stays.
- **Pictures before tables.** A caption says what the picture cannot say itself: the scale, what
  each color means, and whether it shows the value being decided or a stand-in (for example,
  "the strip shows 1 and 2 mm; the proposal is 0.6").
- **Short.** Sentences under about 20 words. No paragraph over three sentences. Background goes in
  a link to the record or the issue, not on the page.
- **Plain words.** Write it so Omar could read it cold, on a phone. No house shorthand, no ticket
  numbers standing in for names, no ids without a word saying what they are.
- **Every option has pros, cons and what it leads to.** "What it leads to" is the next piece
  of work it starts, or the door it closes. A bare label with a cost is not an option. The table
  goes under the option pictures, not above them.
- **Mark one pick** and give its reason in one line. Leaving things as they are is an option
  only if its cost is written out like the others.
- **Keep the source's hedges.** "Worked out from the layer count, not measured" stays in the
  sentence. An untested claim is not written as a fact.
- **One tick-box list per call, with a Notes line.** Where one call has two parts, split it
  (4a, 4b) so each part gets its own list.
- **Owner actions are not calls.** They go in the closing list, one line each.
- **Look at it the way Omar will, before telling him.** Open the page in Obsidian, screenshot it
  top to bottom, and check that every picture shows and that the first screen has a picture on
  it. Look at each picture at full size before it goes in.
- **Links must resolve** (the docs gate checks them). Put no backticks round a path that is not
  in this repo, and never link the FAQ proposal, which is Omar's untracked file.
