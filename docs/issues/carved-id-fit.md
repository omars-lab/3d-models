---
date: 2026-10-08
---

# Carved ids: most pieces have no room for the full id

**2026-10-08.** D-109 says every experimental piece carries a carved id, the plate, the iteration
and the piece, cut into the face that sits on the bed. The plan was the full id on every piece of
every plate that waits for a yes. Measured, the full id fits 18 pieces of the five plates, and
every other piece is refused by bikar. So each of the others now says, in its recipe, why it has
no id and how it is told apart instead. This note is the record of what was measured, and of three
gaps the work turned up on the way.

## What bikar needs

bikar cuts the id in two lines, for example "SL1" over "3 A", mirrored so it reads the right way
round from below. It refuses a piece where the id does not fit, with this message (spl-1's first
pair as the example):

> bottom id 'SL1/3 A' fits nowhere on the bed face: at a 3.5 mm cap it is 10.2 × 7.9 mm, and
> needs that much flat bed face with 0.8 mm (CAL-CST-01) to every edge and 1.2 mm of solid over
> it (a 0.6 mm cut, CAL-TXT-01, and a 0.6 mm floor, CAL-CST-03). The cap cannot go under 3.5 mm,
> where the thinnest cut stroke is one 0.4 mm bead (BOTTOM_ID_CAP_MIN_MM).

So a piece needs a flat patch of about 10 by 8 mm on its bed face, clear of every edge and every
hole by 0.8 mm, with 1.2 mm of solid above it. Letters cannot get smaller than 3.5 mm, because
below that the thinnest stroke is narrower than one line of plastic.

## What was measured

Every distinct piece of the five plates was rendered by bikar with the id it would carry, and with
two shorter forms to see how much room there is: "3C" (the iteration and the piece) and "C" (the
piece alone). OK means bikar cut it; no means bikar refused.

| Plate | Piece | Full id | "3C" | "C" |
|---|---|---|---|---|
| spl-1 | the twelve Fit Lowers | OK | — | — |
| spl-1 | Fit Upper | no | OK | OK |
| spl-1 | Trap Lower, Trap Upper, trapped piece | no | OK | OK |
| pkt-1 | Pocket Lower, Pocket Upper | no | OK | OK |
| split-01 | Middle | OK | — | — |
| split-01 | Hex, Outer | no | OK | OK |
| split-01 | Lower, Upper | no | no | OK |
| split-01 | Kite | no | no | no |
| split-02 | Middle | OK | — | — |
| split-02 | Hex, Outer | no | OK | OK |
| split-02 | Lower, Upper, Star, Kite | no | no | no |
| sheets-04g-fit | the four Middles | OK | — | — |
| sheets-04g-fit | the coaster | no | no | OK |
| sheets-04g-fit | Kite | no | no | no |

The 18 that take the full id were rendered and looked at from below with
`python3 tools/print_review.py bottom <out.png> <a.stl> …`, the new view of the bed face as you
see it when you pick the piece up; each reads right. The pictures are on the plate pages.

One oddity, noted and not chased: the split coasters' Lower refuses even "A" when the coaster's
own id mark is off (`id=0`), but takes "C" with the mark on (`id=1`). Where bikar places the id
depends on more than the space left over, so a piece that refuses one text may take another of
the same size.

## What the recipes say now

Each recipe has an `id_code:` (SL1, PK1, SP1, SP2, 4GF), an `id:` on each piece that takes one,
and on every other piece a `no_id:` reason: bikar's refusal in a sentence, then how that piece is
told apart without it (its pair letter cut by the coupon, the only upper half on the plate, the
pile it comes off the bed in). The plates gate's rule P13 fails a recipe where a piece has
neither, so a new piece cannot slip through without one. pkt-1 has no piece that takes the full id.

Changing the recipes moved each of the five plates to iteration 3, which resets their yeses: each
needs Omar's yes again before it prints.

## The shorter id where the full one does not fit (D-114)

Omar's pick, 2026-10-08, of three ways on from here: "Shorter id where full won't fit". A piece
with no room for the full id carries a shorter one, set by `id_form:` on its recipe item: `short`
cuts the iteration and the piece, "4M", and `piece` cuts the piece alone, "Z". The plates gate
refuses `id_form:` without an `id:`, a form it does not know, and `short` on a piece whose id is a
digit, which would run into the iteration ("41" reads as iteration 41).

The pick came with a rule: an id is cut only on a face hidden in use. An upper half prints face
down, so its bed face is the top of the coaster, and it carries no id even where one fits; its
pair letter on its cut face tells it apart. No gate can check which face is hidden, so each upper
half's reason in its recipe says it.

Letters are kept apart within a plate and, where they can be, across the coupons on the shelf:
spl-1's trap lowers take their pair letters, M and N, and the trapped hexagons T and U; pkt-1's
lowers take P, Q and R, their pair letters, and S for P2a, because O is never cut as an id (it
reads as a zero).

Two pieces the table above shows taking a shorter id carry none, each for its own reason:

- **The split coasters' Hex and Outer rings.** bikar renders each ring as one model of ten
  pieces and cuts one id per render, so "4X" landed on one hexagon of ten (the picture made for
  this showed it). An id on one piece in ten tells nine pieces nothing, and the recipe would claim
  all ten carry it. They stay without one until bikar cuts an id into each piece of a ring; that is
  the next step, and when it lands they take `short`.
- **split-01's Lower.** It takes "L", but its bottom already carries the coaster's own id mark,
  1, and a letter beside it says nothing the 1 does not.

So, at iteration 4: spl-1 cuts 16 ids (12 full, 4 short), pkt-1 4 (short), split-01 and split-02
1 each (full, the middle piece), and sheets-04g-fit 5 (4 full, and Z on the coaster). Changing the
recipes again moved each plate to iteration 4, which resets their yeses once more.

## Three gaps found on the way

**The wrong iteration in the id.** `bambu slice compose` read the iteration from the approvals in
whatever checkout the shell stood in, not the one the recipe came from. Run from the main checkout
on a recipe in a work tree, it cut "SL1/2" into spl-1's iteration 3. The fix
(`idRecipeRoot` in `tools/bambu/src/commands/compose.ts`) reads the iteration from the repo the
recipe file sits in, and refuses a recipe with an `id_code:` that is not a plate's recipe beside
its page. Three tests in `tools/bambu/src/commands/compose-ids.test.ts` fail without it. The recipe
hash compose and slice write into their sidecars still come from the shell's checkout; that has
not misled anything yet and is left as it is.

**A recipe that does not parse passed every check.** Adding the reasons broke split-02's YAML: its
Star piece pointed to a reason that did not exist. Every rule in the plates gate skipped a recipe
it could not read, so the gate stayed green, and the first to notice would have been compose, at
the send. P13 now fails a recipe that does not parse, with a self-test that does.

**A derived plate failed the gate the moment it was made.** `plate_grade.py --derive` copies a
production recipe to a new experiment plate. Production recipes carry no ids, so the copy had
none, and P13 failed it before anyone could make the change it was derived for; the grader's own
self-test caught it. A derived plate now starts planned, with a `needs:` line for its ids, and is
proposed once its recipe has them.
