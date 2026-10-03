---
status: draft
---

# Print review: one page per plate, and a queue that says why

**Status:** draft, 2026-09-30. The pages, the gate and the skill are built. Omar has not
reviewed the design, and §9 lists the calls that are theirs.

## 1. What Omar asked for

On 2026-09-30 Omar asked for "a skill to help us prioritize the highest roi prints and why", and
for a "doc driven print review system": prints captured "as a sub dir", "a file per print",
"where prints are plates", with "documentation on what we can print, why to print it",
"frontmatter on whether or not I approved the print", "screenshots of models we will print", "an
updated timeline of event snapshots on when i approved, when i printed", and "how many times i
printed".

Before this there was no single place to see a plate before it printed. A plate was a recipe
(such as `docs/design/plates/minis-05.yaml`) whose header comment explained it, a review sheet in a scratch
folder, and a line in a backlog saying it was waiting. Whether Omar had said yes lived in chat.
After it printed, a record appeared in `docs/prints/`, but nothing linked the record back to a
plate or counted runs.

## 2. The layout

- `docs/design/plates/<plate>.yaml` — the recipe, unchanged. `bambu slice compose` reads it.
- `docs/design/plates/<plate>.md` — the review page, new, one per recipe. The gate fails on a recipe
  with no page.
- `docs/design/plates/<plate>-media/` — the page's pictures.
- `docs/design/plates/README.md` — what a plate is, how it moves, what we can print, and **the queue**.
- `docs/prints/<run>/index.md` — the print records, unchanged. One per time a plate came off the
  bed.

The pages sit beside the recipes and not under `docs/prints/`. That folder holds only records,
and the prints gate treats every directory in it as one. A plate is a thing that can print; a
record is one time it did.

## 3. A plate page

The frontmatter holds the facts the queue and the gate need. It is flat, as the vault rules ask.

| Property | Holds |
|---|---|
| `plate`, `recipe` | the page's own name, and `<plate>.yaml` beside it; the recipe may be empty only at `planned` |
| `stage` | `planned`, `proposed`, `waiting`, `approved`, `sent`, `printed` or `retired` (§4) |
| `times_printed`, `runs` | how many records name this plate, and which |
| `answers` | the question the plate answers, in one sentence |
| `kind` | `new` question, `taste` (a look at something known), or `repeat` |
| `maturity` | `experiment`, `repeatable` or `production`: what the prints have shown, set by the grade-plate skill ([plate maturity](plate-maturity-design.md)) |
| `bed_fill` | the share of the first bed the pieces cover, from a slice; required only at `production` |
| `bets` | the calibration bets a reading from this plate can move |
| `unblocks` | the open decisions the print lets Omar make, in words |
| `minutes`, `grams`, `bed_plates` | from a local slice; empty at `planned` |
| `risk` | `ok`, `watch` or `hold` — risk to the machine, not to the print |
| `pictures` | the files the page shows |
| `after` | optional: a plate this one waits behind |
| `needs` | at `planned` only, and required there: the builds the plate waits on, in words |

It is `stage`, not `status`, because in this vault `status` means a design doc's state and every
note with one is listed in the design-docs view.

Approval is not in the frontmatter. One design is approved many times: once per send, again after
a fix, held between. A pair of properties holds only the last of those, so each yes is a row in the
page's **Approvals** table instead ([D-096](../../working-model/decisions-log.md)):

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|
| 2026-10-02 | approved | Omar, tick on this page | recipe 1a2b3c4d5e6f | sent 2026-10-02 |

`Decision` is `approved`, `held`, or `standing` (a production plate's, D-095). `By` is who said it
and how: a tick, or his words in chat. `Covers` is the recipe the yes was given on, as the gate's
`recipe_hash`; rows moved in from before the table say `—`. `Spent by` is empty while a yes is
open, then `sent <date>` or `replaced <date>`; a hold or a standing row has `—`. Only
`tools/plate_approve.py` writes rows, and `bambu print send` reads them through the same tool, so
the gate and the CLI cannot read a page two ways.

The body, in order: **In short**; **What it is** (the pieces, linked to the recipe); **Why print
it** (the question, the bet, the decision it unblocks, what to read off the print); **Pictures**
(the review sheet and the bed); **Cost and risk**; **Your call** (tick boxes); **Approvals**;
**Timeline**.
[minis-05](../plates/minis-05.md) is the full example, with a fix to choose before approval.

**Why print it** is the part a backlog line never held: which question it answers and what Omar
can decide once it has printed. The queue's "why" comes from the same fields, so the reason on
the page and the reason in the ranking cannot say different things.

## 4. How a plate moves, and the timeline

| Stage | Means |
|---|---|
| `planned` | designed, but a build it needs does not exist yet, so there is no recipe or slice |
| `proposed` | the recipe exists, the page is not complete |
| `waiting` | pictures and cost are on the page; waiting for Omar |
| `approved` | Omar said yes, and it is an open row in the Approvals table |
| `sent` | it went to the printer; no record yet |
| `printed` | at least one record exists |
| `retired` | not printing it again |

The **Timeline** is a table at the foot of the page, one row per event, oldest first. Each row
starts with an event word — `proposed`, `reviewed`, `sliced`, `sent`, `printed`, `judged`,
`retired`, and the grade's `promoted` and `demoted` — then says what happened and where it is written (a PR, the
record, the page). A plate can print more than once: each run is its own record, with its own
`printed` row, and `times_printed` counts them. The count is never typed from memory; it is the
number of records whose `plate:` starts with the plate's name. A yes or a hold is not a timeline
event: it is a row in the Approvals table, and the `sent` row that spends it names its date.

## 5. Approval, the request-feedback way

Omar answers on the page, not in chat. **Your call** is a short list of tick boxes, each an
option with what it leads to, and a Notes line, the shape the
[request-feedback skill](../../../.claude/skills/request-feedback/SKILL.md) uses. The
prioritize-prints skill reads the ticks back with
`python3 tools/plate_approve.py <page> --approved --by "Omar, tick on this page"` (or `--held`),
which adds the dated row and clears the box, so the next tick is a new answer.

Nothing but a tick or Omar's words writes an `approved` row. The gate prints a notice for a ticked
Approve box with no open row behind it, so an unread answer shows up on the next commit. And a
ticked box is never an approval by itself: a box left ticked after a send from Bambu Studio looks
exactly like a fresh one, which is how sheets-04 looked approved again after it printed. An empty
table is its own state: the plates that went out before this system existed were never asked
about, and a row on them would claim an answer nobody gave.

## 6. The rules the gate holds

`.claude/gates/plates_gate.py`, run by hook 39 after the prints gate and by
`make validate-prints`:

- **P1, shape.** The page is named for its recipe, which exists; only a `planned` page may have
  no recipe yet, and a `planned` page lists what it waits on in `needs`, which no other stage
  may carry. Stage, kind and risk use the words above. Each bet is in `bets.md`. A plate in the
  queue has a positive cost.
- **P2, approval.** Every page has the Approvals table, each row in its shape and in date order,
  and no `approved` or `approved_on` left in the frontmatter. At most one yes is open, and none
  with a hold after it. A plate at `approved` has an open yes, and a plate with an open yes is at
  `approved`. Each `sent` row since the table began spends a yes, and each `sent <date>` names a
  `sent` row. A yes given since the table began names the recipe it covers.
- **P3, count.** `runs` and `times_printed` match the records in `docs/prints/`.
- **P4, pictures.** Each picture exists; a plate waiting on Omar has at least one.
- **P5, coverage.** Every recipe has a page.
- **P6, timeline.** Rows are dated, in order, and use the event words; an `approved` or `held`
  row is refused there, because it belongs in the table. Each run has a `printed` row naming it,
  and there are as many `printed` rows as runs.
- **P7, the queue.** The block on `docs/design/plates/README.md` is the one the pages compute.
- **P8, maturity.** The page's `maturity` is no higher than its prints show, with a dated
  `promoted` row behind any level above experiment. Its rules, and its own validator, are in
  [plate maturity §7](plate-maturity-design.md#7-the-gate-and-why-a-skill-as-well).

**Validator:** `python3 .claude/gates/plates_gate.py --self-test` builds a clean set of plate
pages and records, requires it clean, then breaks it once per rule and requires that rule to
fire.

PASS: the real tree today — eleven pages (five of them sampler sheets at `planned`), two records,
minis-03 and minis-04 at one run each, and the queue current.

FAIL: a second record for minis-09 while its page still says `times_printed: 1` with one run
listed. The page agrees with itself; only a count taken from `docs/prints/` catches it. For
approval, the hard case is a `sent` row with no yes spent on it: the page is otherwise clean, the
box unticked, the stage right, and only reading the table against the timeline catches the send
nobody approved. Also a page moved to `stage: approved` with no open row, and a queue block edited
by hand.

## 7. The queue, and why it is computed

The skill's [scoring.md](../../../.claude/skills/prioritize-prints/scoring.md) holds the sum and
its weights. In short: **value** is each bet the plate can move plus each decision it unblocks,
plus a bonus for a new question; **cost** is hours on the machine, with filament counted as time.
The queue lists plates highest value per hour first, drops any plate at `risk: hold` into a
"held" line, and keeps a plate with `after:` below the one it waits for. A `planned` plate has no
hours to divide by, so it is not ranked; it is listed on a "waiting on a build" line by value
alone, so a design that is worth building shows up before its recipe exists.

The weights are a first guess, not measured. That is why the scoring lives in a file the skill
reads at run time, with a round log: a ranking Omar disagrees with becomes a change of weight
with its reason written down.

The rank itself is never stored on a page. The prints-tab design already settled this
([§6, "Priority is presented, never stored"](prints-tab-design.md#6-priority-is-presented-never-stored)):
a stored rank goes stale the moment a weight or a cost changes. The pages hold the inputs, and
`plates_gate.py --write` computes the table; the gate fails when the table and the pages
disagree.

The first run put [minis-06](../plates/minis-06.md) first (value 8 over 3.8 hours) and
[minis-05](../plates/minis-05.md) second (10 over 5.8). minis-05 is slower because as written
it spills onto a second bed. Its page offers dropping the plain pair, which would make it one bed
in about 3.8 hours and put it first.

## 8. Reuses and replaces

**Reuses:** the recipes and `bambu slice compose`; the print records and the prints gate (the
count is read from them); the review-print skill's sheet (`tools/print_review.py`); the
request-feedback page shape for the tick boxes; the calibration bets; the vault's Bases for the
"by stage" view (`docs/bases/plates.base`).

**Replaces:** the "waiting on Omar" lines about plates in the
[coaster-pipeline backlog](../../tasks/coaster-pipeline/backlog.md), which now point at the
pages; the stale "Nothing yet" and hand-kept queue on [prints.md](../../prints.md), which now
list the records and point at the queue.

**Does not replace:** the print register's §2 order for the calibration plates (the machine
card, the LEGO ladder, the wall joint, the first orb). Those have no recipe yet, so they have no
page and are not in the queue. Until they do, two orders exist: one computed for the coaster
plates, one argued by hand for the calibration plates. Call 1 below is about that.

## 9. Omar's calls

Each of these is Omar's. The plate-level calls (2, 3, 5) are also tick boxes on their pages;
answer them there.

**1. One queue for every plate?**

| | Calibration plates get pages when they get recipes (my pick) | Keep the register §2 order for them |
|---|---|---|
| **Pros** | One order, computed the same way for everything; Plate 1's "defines the profile every later plate reuses" becomes `after: plate-1` on the pages that need it | No work now; the register's hand-argued order stays exactly as written |
| **Cons** | Each calibration plate needs a recipe before it can be ranked, which is work the register has not started | Two orders that can disagree, which is what the prints-tab design warned against |
| **What it leads to** | The register §2 argument shrinks to the `after:` lines and the pages' "why print it" | The register and the plates page both need reading to know what is next |

- [ ] Pages when they get recipes
- [ ] Keep the register order

**2. minis-05's second bed.** As written, one key coaster spills onto a second bed. Drop the
plain pair (my pick: one bed, about 3.8 hours, and it moves to first), move the plain pair to
minis-06, or print both beds. The pictures and the trade-offs are on
[minis-05's page](../plates/minis-05.md#fix-before-approval-the-second-bed).

**3. Did minis-01 and minis-02 print?** Both went out from Bambu Studio on 2026-09-25 and
neither has a record, so both pages sit at `sent`. A yes on either means writing its record.
Tick boxes on [minis-01](../plates/minis-01.md) and [minis-02](../plates/minis-02.md).

**4. The weights.** A bet and an unblocked decision are worth the same (2 each), a new question
adds 2, and 100 g of filament counts as an hour.

| | Keep them and change on a case (my pick) | Weight bets above decisions |
|---|---|---|
| **Pros** | Nothing to decide in the abstract; the first ranking that looks wrong says which way to move | Bets feed every later design, a decision only the one that asked |
| **Cons** | Two plates in the queue is too few to test the weights on | Guessing a ratio with nothing to measure it against |
| **What it leads to** | A line in the round log the first time a ranking is wrong | minis-05 (one bet, three decisions) drops against a bet-heavy calibration plate, once one has a page |

- [ ] Keep them
- [ ] Bets count more (say how much in the notes)

**5. minis-06's control pair.** minis-06 repeats minis-04's dovetail pair to test bikar's slot
fix. Keeping it (my pick) checks the fix against the "pegs too tight" minis-04 found; dropping
it saves about half the plate and leaves room for minis-05's plain pair. On
[minis-06's page](../plates/minis-06.md#your-call).

**6. Should an approval lapse when the recipe changes?** Today an approved plate whose recipe is
edited afterwards stays approved.

| | Lapse by hand for now (my pick) | Gate it: record the recipe's hash at approval |
|---|---|---|
| **Pros** | No new field; an approval option that changes the recipe names the change, so that yes already covers it | A changed recipe can never go out on an old yes |
| **Cons** | Someone could edit a recipe and forget | One more field, and every approval option that edits the recipe needs a second tick |
| **What it leads to** | A gate later if it ever happens once | Approval means "this exact recipe" |

- [ ] Lapse by hand
- [ ] Gate it

Since the Approvals table (D-096, 2026-10-03), each yes records the recipe it covers, so "Gate it"
needs no new field and no second tick: it is one switch, `LAPSE_ON_RECIPE_CHANGE` in the plates
gate. Until this is answered the switch is off: a recipe changed after a yes is a notice on the
next commit and a warning on the send, and the yes stands, as before.

Notes:
