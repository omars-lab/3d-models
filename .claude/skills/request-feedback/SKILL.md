---
name: request-feedback
description: Gather Omar's decisions as a page in the docs/ Obsidian vault instead of questions in chat. Use when two or more calls are waiting on him, when a call needs pictures to decide, when an AskUserQuestion would need more than a line of context, or when he says "prepare a page / an md for me to decide", "gather my decisions", "what's waiting on me", "request feedback". Writes docs/working-model/feedback-requests/<date>-<slug>.md with pictures, options (pros, cons, what each leads to), a pick and tick boxes, ships it and opens it in Obsidian. When he has answered, reads the ticks back into the decisions log and the backlogs.
---

# request-feedback — decisions on a page, answered in Obsidian

A question in chat carries one line of context and no pictures, and it is gone when the session
ends. A page in the vault carries the pictures and the reasons, Omar answers it when he has time,
and the next session reads the answers back. Why this is a skill and not a habit:
[the evaluation](../../../docs/design/process/request-feedback-evaluation.md).

The page's shape and the writing rules are in [`page-template.md`](page-template.md). Read that
file every run; it is kept apart so it can improve without this file changing.

## Asking

1. **Collect the open calls.** Search the backlogs for work waiting on Omar
   (`grep -n -i "waiting on omar\|omar's call\|omar's pick" docs/tasks/*/backlog.md`), list the
   open PRs across the repos and read the task board. **Check each one still stands** before it
   goes on the page. A branch may already be gone, or a PR may be stranded (2026-09-29: a
   stacked PR merged into its parent, not master, and closed two others). Keep choices apart
   from things only he can do (a print, a secret, a send). The second kind goes in a short list
   at the end, not as a call.
2. **Find the pictures.** Use renders that already exist first: catalog media, research
   folders, the video loop's step-NN-diff pictures (frame, render, difference) in the youtube data
   folder. Draw a new one only when the call is about a shape nobody has drawn. Copy each into
   `<page>-media/` beside the page, shrunk
   (`magick in.png -resize 1400x -strip -colors 64 PNG8:out.png`). Look at every picture before
   it goes in.
3. **Write the page** from the template, at
   `docs/working-model/feedback-requests/<yyyy-mm-dd>-<slug>.md`. Run
   `python3 .claude/gates/docs_gate.py <page>` until it passes.
4. **Ship it.** Branch, PR, merge, like any doc. Then bring it into the vault. The vault is the
   main checkout's `docs/`, which other sessions share. Run `git merge --ff-only origin/master`
   there only if it goes through cleanly. Never discard another session's changes to make room.
   Then open it:
   `open "obsidian://open?vault=docs&file=working-model/feedback-requests/<name-without-.md>"`.
5. **Tell him** in two lines: how many calls there are, and the link.

## Reading the answers back

When Omar says he has answered, or a session finds ticked boxes:

1. Read the page and its review threads (`reviews list docs --open`).
2. For each call with a box ticked:
   - Write a [decisions log](../../../docs/working-model/decisions-log.md) entry with an id from
     `python3 tools/next_id.py next D`. It holds the options as the page gave them, his pick,
     his note, and what would reverse it.
   - Under the call on the page, add one line: `**Decided <date>:** <option> → D-0xx`.
   - Move the backlog item with the `manage-tasks` skill.
3. A call with no tick stays open. Say so in the reply. Do not decide it for him from the "my
   pick" column.
4. Ship all of it in one PR, then start the work each decision unblocked, highest value first.

## When not to use it

For a single yes/no that needs no picture, AskUserQuestion is fine. Put the options' pros, cons
and consequences in each option's text.
