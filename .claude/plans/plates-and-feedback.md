# Plates and feedback — the hand-off plan

Written 2026-11-10 by the plates-and-feedback session, for a new session picking this work up
cold. The task lists stay where they are, because hooks read them; this page points at them.

- Open work: [coaster-pipeline backlog](../../docs/tasks/coaster-pipeline/backlog.md) and
  [print-infrastructure backlog](../../docs/tasks/print-infrastructure/backlog.md).
- Finished work: each loop's `done.md` beside its backlog.
- Who runs what: [the loop table](../loop-prompts/README.md#which-session-runs-which-loop).

## The goal

Get Omar's prints from idea to judged record with as few prints as possible. This session owns
the print side of the coaster work: building plates, getting Omar's yes, sending, watching the
print, putting the questions on the hub's judging page, and writing the print record from his
answers. Split coasters and split pieces are the main line since 2026-10-06; small one-off plates
he asks for (toys, cable holders) go in between.

## How a plate moves

1. **Build.** A recipe `docs/design/plates/<name>.yaml` and its page `<name>.md`, sliced with
   `tools/bambu/bin/bambu slice compose docs/design/plates/<name>.yaml`. Skill: `prioritize-prints`.
2. **Yes.** Omar's yes must come in chat **in this session's own tab**, naming the plate and a
   color. A yes passed on by the manager or another session does not count; ask him here.
   Record it with `manage-approvals`. One yes covers one send.
3. **Send.** Skill `send-plate`. Run every `bambu` call from the main checkout with
   `env PATH=/Users/omareid/.nvm/versions/node/v22.22.3/bin:/opt/homebrew/bin:/usr/bin:/bin`.
4. **Watch.** Skill `monitor-print`: the script in the background, a watcher agent, then
   `--publish` puts the timelapse on the page.
5. **Judge.** Skill `judge-page`: Omar answers on the hub. Give him the link with comments on,
   `http://127.0.0.1:8768/judge.html#<plate>/1` (`open_questions.py <plate> --link` prints it). Never the bare `:4717` address: it has no
   comments, and he asked why on 2026-11-09. The hub opens an `After-print answers: <plate>` PR.
6. **Record.** Skill `review-print` writes `docs/prints/<date>-<plate>/` from the `## Judged`
   table.

Every change to a plate page or task file goes branch → PR → the manager merges → fast-forward
the main checkout (`git -C ~/Workspace/git/3d-models merge --ff-only origin/master`). Never edit
files in the main checkout by hand.

## Plate decisions waiting on Omar, from every session

Collected 2026-11-11 at Omar's ask: "move all the plate decisions we need to make across sessions
to the plan.md as well". This is the one list of calls that decide what gets printed. Each call
links to the page where Omar answers it, and that page holds the full options and pictures; this
list never replaces it. When a call is answered, delete its entry here in the same PR that
records the answer.

Swept from: the hub's "Waiting on you" box (`/api/plates`), `open_questions.py --list`, the plates
queue, every page in `docs/working-model/feedback-requests/` with an unticked box, and the plate
calls monitor-print-watcher sent from its plan. That session keeps the design side of the
spinner, orb and fidget-toy work; only the calls that pick a plate are here. Highest value first.

### A. cables-1: send it, and in which color

- **Question:** print the cable holder and the row of 13 clips now?
- **Options:** yes in green (#00AE42) sends it, about 19 minutes and 4.67 g; yes in another color
  sends it in that color; not now keeps it in the queue.
- **Where:** in this session's tab. A yes given to the manager does not count.
- **Unblocks:** the send, then the watch, then a desk cable holder in his hands.

### B. closeout-1 and toys-1: judge the prints in hand

- **Question:** closeout-1 rows 2 to 5 (4 questions, row 4 is the kite fit) and toys-1 rows 1
  to 3 (3 questions, row 1 is how the star's rings came out).
- **Options:** the answer buttons on each row; "not judged yet" is one of them.
- **Where:** `http://127.0.0.1:8768/judge.html#closeout-1/2` and
  `http://127.0.0.1:8768/judge.html#toys-1/1`.
- **Unblocks:** both print records. closeout-1 row 4 decides whether the three kite fits split-10
  dropped (KITE-G10, KITE-PIN20, KITE-PIN15) need a plate. toys-1 row 1 is also question 1 of the
  fidget toys (F below): its answer sets the smallest ring gap on the first toy plate.

### C. The 18 overtaken questions and the split-10 leftovers

- **Question:** seven calls on one page about old after-print questions: close the 18 overtaken
  ones; which star face is flattest; the kite gap; what "pins of 6" means; the lopsided bigger
  kites on split-07; star-3's two questions; and whether the leftovers get a plate.
- **Options:** each call's first option is the pick and needs no print: close, or answer from the
  pieces he has. Other options reprint four stars (0.94 g), four kites (0.44 g) or two middles
  (2.52 g), or build a small leftovers plate.
- **Where:** [2026-11-05-which-questions](../../docs/working-model/feedback-requests/2026-11-05-which-questions.md).
  Call 4 is the same question as the open hub comment t_1cc863 on split-10's MIDDLE-SUPPORT
  ("this was best but want pins of 6"); one answer settles both.
- **Unblocks:** the next middle-piece plate (pin count), the kites' gap, and whether any reprint
  plate is built at all.

### D. Round 3: which pattern becomes the next coaster

- **Question:** which of seven patterns to build next: the Alhambra door tile (the pick), Sultan
  Barsbay's tile, the seven-point rosette, the Ibn Tulun tile, the turned lattice, the nine-point
  rosette, or the star field. The page also asks about the scores behind the ranking.
- **Options:** each pick becomes the next coaster design, then its first plate; the page shows
  each one drawn.
- **Where:** [2026-11-05-next-coaster-round-3](../../docs/working-model/feedback-requests/2026-11-05-next-coaster-round-3.md).
- **Unblocks:** the next coaster's design and its first test plate.

### E. The spinner coaster: five choices

The watcher session's pick is option 1 on each. The design is
[spinner-coaster-design](../../docs/design/pieces/spinner-coaster-design.md).

- **Questions and options:**
  1. What spins: a button pressed into the straps coaster, printed face up; or a hub printed in
     the same job, inside a flat-faced coaster printed face down.
  2. How thick: 7.0 mm with the button inside the cap; or about 7.6 mm, with a 40 mm disc over
     the cap.
  3. Which bearing to buy: sealed chrome steel 6704 for the test pieces; sealed stainless 6704
     once a source turns up; open stainless 6704; or a 6705.
  4. How the pause gets into the file we send: teach our slicing to pass the pause to Bambu
     Studio's command line; or slice and send from the Bambu Studio window by hand.
  5. Order: the pause and cap first, through the two test pieces; or the split halves now.
- **Where:** [2026-11-08-spinner-coaster-choices](../../docs/working-model/feedback-requests/2026-11-08-spinner-coaster-choices.md).
- **Unblocks:** the first test piece, a small pocket coupon with no steel in it, which becomes a
  plate here. Buying the bearing is Omar's.

### F. Fidget toys from our patterns: three plate questions

The design is [fidget-toys-from-patterns](../../docs/design/pieces/fidget-toys-from-patterns.md),
§9. Its questions 3 and 5 are design calls and stay with the watcher session.

- **Questions and options:**
  1. How the toys-1 star came out (free, stiff or stuck), and whether the slicer put supports
     between its rings. Answered on the hub as toys-1 (B above). If the 1.0 mm gaps came out
     stiff, a 0.4 mm gap is likely too small.
  2. Toy size: keep the star's 78 mm across and 18 mm tall, or go bigger for more rings.
  4. Which pattern first: 0ke_GpoBa-s (cleanest rings, the watcher's pick) or one Omar names.
- **Where:** §9 of the design doc; question 1 on the hub.
- **Unblocks:** the first pattern toy plate. It also needs bikar work first (ring outlines and a
  ring-toy declaration), so it cannot be built the day he answers.

### G. Whole orbs with supports only outside: three plate questions

The design is [whole-orb-outside-supports-design](../../docs/design/orb/whole-orb-outside-supports-design.md),
§8. Its questions 4 and 5 are design calls and stay with the watcher session.

- **Questions and options:**
  1. How far PLA bridges on the X2D. The 10 mm limit is a guess (bet CAL-BRG-01). Print the
     bridge coupon MC-3 first, or keep 10 mm and go on.
  2. Whether the top half sags. Only a print shows it: the top-cap test piece in §7.
  3. Whether the 25 mm² bed-contact floor is too strict (bet CAL-BED-01). Coupon MC-6 settles it;
     the doc keeps 25 mm² until MC-6 prints.
- **Where:** §8 of the design doc.
- **Unblocks:** first a slice with no print, then the top-cap test piece as a plate.

### H. sheets-04g-fit3: the middle piece and the looser kite

- **Question:** print the fresh coaster with the middle piece at 0, 0.025 and 0.05 mm and kites
  at 0.05 and 0.075 mm (70 minutes, 19.4 g)?
- **Options:** approve as it stands; or hold it until closeout-1's kite answer (B), which may
  settle the kite gap without it.
- **Where:** the Approve box on [sheets-04g-fit3](../../docs/design/plates/sheets-04g-fit3.md),
  or a yes in this tab.
- **Unblocks:** the middle piece's gap and the kites' gap on the next sheets-04g coaster.

### I. The other 26 plates waiting for a yes

The hub lists 28 plates waiting for a yes; two are A and H. The rest, in
[the queue](../../docs/design/plates/README.md#the-queue): 15 theme plates (Night sky, Iznik
tile, Terracotta souk, Midnight blue), 4 color swatches, stud-1 and split-01 (held until the split
stud gap is settled), sheets-01 to 03 (edge steps, star points, crossing welds), minis-05 and 06
(thin joins), and split-09 (the two-of-each halves layout).

- **Question:** for each, print it, or mark it superseded. Most were built in late September and
  early October, and later plates have since moved several of their questions on. Never assume
  he still wants them as built.
- **Options:** a yes in this tab sends that one plate; "superseded by <plate>" retires it from
  the queue; no answer leaves it waiting.
- **Where:** each plate's page, or this tab.
- **Unblocks:** clears the queue down to the plates still worth their grams.

### Not in this list, and why

- **The star-1 comments t_d6d491 and t_db7bda** ask Omar to tap row 1's answer and point to
  star-2. star-2 has printed since, so both are likely overtaken. Closing them is his call.
- **The September and October feedback pages** (open calls of 09-29, 10-05 and 10-06, the
  bottom-slits pages, peaked pieces, the top-three renders, prioritize-design) still have unticked
  boxes, but read as decided (a Decided line) or overtaken by later plates. That was not checked
  call by call; the 10-13 bottom-slits page, for one, became bedface-5.

## Open, in order

### 1. Send cables-1 — waits on Omar's yes in this tab

[cables-1](../../docs/design/plates/cables-1.md): one 3-slot cable holder and one row of 13
cable clips from MakerWorld, for his desk. Built and merged (3d-models #1001), about 19 minutes
and 4.67 g, no supports. Omar said "Send in green" to the manager on 2026-11-10, which does not
count here; ask him in this tab. [Backlog line](../../docs/tasks/coaster-pipeline/backlog.md#open-in-roi-order).

Once he says yes, from a worktree branch off `origin/master`:

```
python3 .claude/skills/manage-approvals/scripts/plate_approve.py docs/design/plates/cables-1.md --approved --by 'Omar, in chat: "<his words>"' --color "#00AE42"
```

PR it, wait for the merge, fast-forward the main checkout, then from the main checkout:

```
tools/bambu/bin/bambu status show
tools/bambu/bin/bambu storage show
tools/bambu/bin/bambu filament-sync --plate build/plates/cables-1.plate.3mf
tools/bambu/bin/bambu print send build/plates/cables-1.plate.3mf --dry-run --color "#00AE42"
```

Open the bed photo the dry run saved and look at it. Only then:

```
tools/bambu/bin/bambu bed verdict cables-1 --plate-type textured_plate --bambu-plate --by "Claude, opened the photo" --clear --seated
tools/bambu/bin/bambu options for-bed cables-1 --yes
tools/bambu/bin/bambu print send build/plates/cables-1.plate.3mf --dry-run --no-bed-photo --color "#00AE42"
tools/bambu/bin/bambu print send build/plates/cables-1.plate.3mf --record --yes --color "#00AE42"
python3 .claude/skills/monitor-print/scripts/print_monitor.py cables-1 --snapshot-every 2
```

The last one runs in the background, with a watcher agent beside it. Ship the sent page, the
print log and the timelapse in one PR.

### 2. Write the closeout-1 and toys-1 records — waits on Omar judging

- [closeout-1](../../docs/design/plates/closeout-1.md) printed twice in green (the reprint on
  2026-11-09, #990). Four questions on the hub. Its row 4, the kite fit, decides item 3 below.
  Omar left a reprint note on row 1 that belongs in the "On the whole plate" box; he moves it.
- [toys-1](../../docs/design/plates/toys-1.md) printed in silk blue on 2026-11-07. Three
  questions. Its record carries his ball and star calls, already written in the
  [backlog entry](../../docs/tasks/coaster-pipeline/backlog.md#open-in-roi-order).

When his answers are sent, the hub writes `ev=answers_sent plate=<plate> pr=<n>` into
`~/Library/Application Support/3d-model-hub/answers/events.log`. Watch it with:

```
make -s -C ~/Workspace/git/3d-model-hub watch-answers
```

After the manager merges that PR, run `review-print` for the plate. Never edit the `## Judged`
or `## On the whole plate` tables by hand.

### 3. The kite fits split-10 dropped — waits on closeout-1's row 4

KITE-G10, KITE-PIN20 and KITE-PIN15. Whether they need a plate depends on Omar's answer to
closeout-1's kite question. [Backlog item 1](../../docs/tasks/coaster-pipeline/backlog.md#open-in-roi-order).

### 4. minis-01 — waits on a print

Keep [minis-01](../../docs/design/plates/minis-01.yaml) ready to send, and turn its print into
data when it happens (backlog items 2 to 4). The standard-size plate, P5.2, waits on the
numbers it measures (item 5).

### 5. Held

- **stud-1, pkt-2 and split-01** stay held until the split stud gap from spl-2 is settled
  ([owner-gated list](../../docs/tasks/coaster-pipeline/backlog.md#owner-gated)).
- **Print-infrastructure:** the plate-packing skill is open; bedface-5's judging and the hub's
  send button wait on Omar ([that backlog](../../docs/tasks/print-infrastructure/backlog.md#waiting-on-omar)).

## Omar's to do

Every plate call is in [Plate decisions waiting on Omar](#plate-decisions-waiting-on-omar-from-every-session)
above; the short version:

- Say yes and a color for cables-1, in this session's tab.
- Judge closeout-1 (4 questions) and toys-1 (3) on the hub.
- Move his row-1 reprint note on closeout-1 to the "On the whole plate" box.
- Page comment t_1cc863, and the two star-1 threads t_d6d491 and t_db7bda.

## Rules that bite

- Never send without Omar's yes in this tab, and never on a bed photo nobody opened.
- Resume, stop, pause and "ignore and resume" on the printer are Omar's. Never send them.
- Never print the printer's access code, tokens, or anything from `BambuStudio.conf`.
- The repo is public: no downloaded STLs, chamber pictures with people or QR codes, serials or
  addresses in git.
- Merging PRs is the manager session's job.
