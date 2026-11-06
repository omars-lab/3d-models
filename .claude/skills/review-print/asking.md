# Asking the after-print questions: the SOP format

Omar picks the pieces up and does what the question says, with the pieces in one hand and the
screen in the other. A question he has to read twice is one he can get wrong, and a wrong answer
goes into the record as a measurement. So every question is a short procedure, like a
checklist on a bench: what we are checking, which pieces, numbered steps, what each result looks
like, then the answer. Read this file before asking each round.

Omar, 2026-10-09, on spl-1 row 4: "what kind of instructions are these ... not clear and
straighforward and in simple sop format ... easy to get a mistake".

## Before the steps: a plain paragraph and a picture

Omar, 2026-11-03, on the judging page at split-10 question 1: "These questions are unclear, i
don't know what to look for ... langague very cryptic. We should have narrative sytle writing on
what to look for and relevatn supplemtnatry figures to reference."

Steps alone tell him what to do, not why or what he is looking at. So every question on a plate
page's After-the-print table opens, before `**Do:**`, with:

- **A lead paragraph, 2 to 4 sentences, in words a newcomer knows.** What the question checks;
  why it matters for the coaster in the hand; what good looks like and what bad looks like. Name
  the earlier plate that raised it, if one did. A design word (brim, pin, flange) gets a few words
  of explanation the first time.
- **At least one picture.** The pieces themselves, cut from the bed picture or the pieces pictures
  with `tools/print_review.py compare`, labelled by the number or id he sees. Where good and bad
  are a shape (a curve, a gap, a lip), add a side-view sketch from the
  [draw-side-view](../draw-side-view/SKILL.md) skill, good on the left and bad on the right, and
  say in its caption it is a sketch. A real photo of the fault beats a sketch when one exists;
  never dress a sketch up as a photo.

The cell is written as pictures, then the lead, then the steps:

```
![<what the picture shows, by piece number>](<plate>-media/questions/q1-pieces.png) ![<what the sketch shows>](<plate>-media/questions/q1-look.png) <lead paragraph> **Do:** 1. … 2. … **Look for:** …
```

`after_print.py questions <plate>` reads the lead into `lead` and the pictures into `figures`, and
the hub's judging page shows them in a panel between the pieces and the steps. The alt text is the
caption, so write it as a sentence. The SOP rules below still hold for the steps.

### Don't: closeout-1 question 1 as first written

> **Do:** 1. Peel the supports off STAR-SUPPORT and STAR-GRID. 2. Close each cut star's two
> halves. 3. Lay the five stars face up side by side, STAR-GRID at one end. 4. Look at each from
> the side, along a point. **Look for:** a face that is flat out to its points, with no curve at
> the edges, and whether any of the four is flatter than STAR-GRID.

Clear steps, but nothing says why the curve matters, what a curve looks like next to a flat face,
or which star on the bed is which.

### Do: the same question now

> *(picture: the five stars cut from the bed picture, numbered 1, 3, 4, 2, 6)* *(sketch: a flat
> face on the left, one that dips toward its points on the right)*
>
> This checks whether a star's face stays flat right out to its points. On split-07 the stars
> came out with a curve, so a coaster made from them would rock and show light under the tips.
> Good is a top edge that runs straight from the centre to each tip when you look along a point;
> bad is an edge that dips toward the tip, like the right side of the sketch. STAR-GRID is the
> star we would print today, so the question is whether any of the other four beats it.
>
> **Do:** … (unchanged) **Look for:** … (unchanged)

All five of [closeout-1](../../../docs/design/plates/closeout-1.md)'s questions are written this
way; copy them.

## The format

```
<plate>, row <n>: <what we are checking, as a yes/no question in under ten words>

Pieces: <each carved id>, <what it is in plain words, and where its id is>

1. <one action>
2. <one action>
3. ...

<Result A>: <what you see or feel>
<Result B>: <what you see or feel>

<the question again, short>
```

- **One line on top saying what we are checking.** "Does the socket show through the top?",
  not a paragraph of context.
- **Pieces by the id cut into them**, and say where to find the id, since that is how he picks
  the right one off the pile.
- **Numbered steps, one action each.** Pick up, turn, hold, press, shake, pull. If a step has an
  "and" or a comma joining two actions, split it.
- **Name a face by something you can see on it**: "the face with the socket hole", "the flat
  face with the id". Never by what it lacks ("the face without the id"), and never by a word
  from the design ("the cut face", "the floor") unless the same step says what it looks like.
- **Say what each result looks like**, one line each, in what he will see or feel. That is how
  he knows which answer to pick.
- **No recap in the question.** Say what the last answer settled in one plain chat line before
  the question, or not at all. The question box holds the new procedure only.
- **No filler.** No "if it's mixed, type it under Other, for example …". Other is always
  there.
- **Options are what he found**, not decisions. The label is the result ("Only DT shows"), and
  the description is one line on what it changes ("the floor goes up to 0.8 mm"). Pros and cons
  are for choices between ways of doing something; an observation has none, so leave them out
  here.
- **Four options at most.** When the results he could find, plus "Not judged yet", come to more
  than four, keep the likeliest results and let "not looked yet" go through Other.
- **Name the pieces as they are now, not as they printed.** An earlier row may have closed a
  pair, and a letter on a cut face is then hidden inside it. spl-1 row 4 asked for KT, LT and DT
  after rows 1 to 3 had hammered them onto their lowers ("what lt and dt peices?", "i see nt and
  mt"). Ask instead for the closed pair, by the id still showing ("the pair with SL1 4K on its
  bottom"), and pick a check that works on it closed.
- **One check per question.** If a row asks two things (does it print clean, and does it hold),
  ask them as two questions, the one he does first first.

## Don't: spl-1 row 4 as first asked

> Noted for rows 2 and 3: 4G, 4H, 4K and 4I needed a hammer, … Also noted as a lesson: …
>
> spl-1, fourth row of "After the print" (open in Obsidian): the uppers KT (floor 0.8 mm over the
> socket), LT (1.0 mm) and DT (0.6 mm). Hold each one up to a window or lamp with its top face
> toward you, the face without the id. Can you see the socket as a darker or lighter dot through
> the top? If it's mixed, type it under Other, for example "DT shows faintly, KT and LT don't".

What is wrong with it:

- It opens with a recap of the last answer, so the new instruction starts halfway down.
- Three pieces, a material term ("floor") and a measurement are packed into one sentence.
- The face to look at is named by what it lacks, and "top face" means nothing on a loose part.
- The steps are one run-on sentence, so the order is unclear.
- It never says what "shows" looks like next to "doesn't show".
- It ends with filler about Other.

## Do: the same row, as an SOP, asked of the pieces as they are now

> spl-1, row 4: does the socket show through the top?
>
> Pieces: three closed pairs, found by the id on the bottom: SL1 4K (floor 0.8 mm), SL1 4L
> (1.0 mm) and SL1 4D (0.6 mm). Leave them closed.
>
> 1. Pick up the pair with SL1 4K on its bottom.
> 2. Turn it so SL1 4K faces down.
> 3. Hold it under a lamp, tilted so the light skims across the top face.
> 4. Look at the middle of the top face, right over the stud.
> 5. Do the same with SL1 4L, then SL1 4D.
>
> Shows: a round dent or spot in the middle, about 2 mm across.
> Doesn't show: the middle looks like the rest of the face.
>
> Which of 4K, 4L and 4D show a dent or spot?

Options: "None show" (the floor stays 0.6 mm), "Only 4D shows" (the floor goes up to 0.8 mm),
"4D and 4K show, 4L doesn't" (the floor goes up to 1.0 mm), "All three show" (no floor here
works; it gets its own coupon). Omar answered it in one pick.

## Do: a row with several checks, split

spl-1 row 5 asked four things of the trap pairs: does the hexagon drop in, does the pair close
flat, does it rattle, does the lip hold. Asked as four questions in one AskUserQuestion call, each
its own short procedure in the order he does them, all four came back answered.

## Do: a fit question

> spl-1, row 1: do the 2 mm studs press in by hand?
>
> Pieces: 4A to 4F (lowers, id on the bottom, a stud on top) and AT to FT (uppers, id next to
> the socket hole). Pair them by letter: 4A with AT, 4B with BT, and so on.
>
> 1. Put 4A's stud in AT's socket.
> 2. Press them together with your thumbs.
> 3. Shake the closed pair hard.
> 4. Pull them apart.
> 5. Do the same with B to F.
>
> By hand: it closes flat with thumb pressure.
> Tight: it needs a hammer, or does not sit flat.
> Loose: it closes, but falls apart when shaken.
>
> Which letters go in by hand, and of those, which stay closed when shaken?
