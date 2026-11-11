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
5. **Judge.** Skill `judge-page`: Omar answers on the hub at
   `http://127.0.0.1:4717/judge.html#<plate>/1`. The hub opens an `After-print answers: <plate>`
   PR.
6. **Record.** Skill `review-print` writes `docs/prints/<date>-<plate>/` from the `## Judged`
   table.

Every change to a plate page or task file goes branch → PR → the manager merges → fast-forward
the main checkout (`git -C ~/Workspace/git/3d-models merge --ff-only origin/master`). Never edit
files in the main checkout by hand.

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
