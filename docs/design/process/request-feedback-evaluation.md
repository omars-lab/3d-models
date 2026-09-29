---
status: built
---

# Do we need a request-feedback skill?

**Date:** 2026-09-29 · **Verdict:** yes. It is built as
[`request-feedback`](../../../.claude/skills/request-feedback/SKILL.md), with no hook.

## The request

> "this should be part of the typical way we document and gather feedback on decisions, see if
> we need a request-feedback skill for this" (Omar, 2026-09-29)

It came after he turned down a round of chat questions and asked instead for "a md in our docs
dir … with all context / screenshots for me to make decision". That page is
[2026-09-29-open-calls](../../working-model/feedback-requests/2026-09-29-open-calls.md).

## What was measured

The repo's rule is to measure how often a thing recurs before building a skill for it
([dsl-extension-skill-evaluation](dsl-extension-skill-evaluation.md),
[issue-register-evaluation](issue-register-evaluation.md)). Both of those ended with *no skill,
a gate instead*.

- **How often we ask.** In this repo's Claude Code session transcripts, counted on 2026-09-29:
  225 AskUserQuestion calls holding 325 questions. 35 of them were turned down or sent back for
  clarification.
- **How much is waiting.** 10 backlog lines were waiting on Omar when counted, and eight video
  records were stranded in open PRs that said "waiting for Omar".
- **What already exists.** `design-note` is the closest skill. It turns *one* decision into a
  note published on the studio site. It does not gather several calls, does not live in the
  vault, and does not read the answer back. `manage-tasks` moves the lines once a decision is
  made. No skill covers asking.

## Why a skill, and not a gate

The two earlier evaluations found a *check* that was missing, so a gate was the answer. What is
missing here is a way of *writing*: collect the calls, find the pictures, lay out the options,
then read the ticks back. A gate cannot write a page. The one part a gate could check, that
the page's links resolve, the docs gate already checks.

## What would reverse it

Drop the skill if Omar keeps answering in chat and not on the pages, or if two pages sit a week
with no box ticked. Either means the page is the wrong place to ask.
