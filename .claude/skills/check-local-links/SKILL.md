---
name: check-local-links
description: Count the broken links on the local pages Omar opens on this Mac — the Studio app (127.0.0.1:7136), the Print Hub (4717) and the judging pages (8768). Use when Omar says links "can't be reached", asks how many links are broken, or after changing bikar's Studio pages or the hub's pages. Runs on its own at session start and, after a session that edited page files, at the end.
---

# Check the local links

Omar, 2026-11-13: "lots of the links on pressing cant be reached (example
http://127.0.0.1:7136/judge) do we have a hook to go through and see how many broken links we have
at session end". This skill opens every page it can reach from each site's front page and counts
what is broken.

## What it counts

- **Does not load:** the page answers 4xx or 5xx, or the connection fails.
- **Loads but its data can't be reached:** the page shows bikar's sentence "The print data can't be
  reached from here" (`UNREACHABLE_TEXT` in bikar `packages/web/src/print/api.ts`). This is the
  2026-11-13 case: `/judge` loaded, `/api/print/...` did not answer.
- **Points at a site that is not running:** a link on a running site into one of the three sites
  that is down. The down site itself is reported once as "not running", not as one broken link per
  page.

## How it reads a page

The Studio and the Print Hub draw their pages in the browser, so a plain fetch sees an empty shell.
Their pages are loaded in headless Chrome and read after the scripts ran (about 5 seconds each).
The judging pages on 8768 are read with plain GETs only, never in a browser: the comment bar there
writes each thread's found-or-lost state back when a page loads, and a check must not write.

Only GETs are sent and nothing is clicked. Every write on these pages sits behind a button
(the files judge.ts and main.ts in 3d-model-hub's web/src folder, checked 2026-11-13).

## What it misses

- Links that only appear after a click, a typed value or a signed-in state.
- Pictures, scripts and data calls a page makes (only `<a href>` links are followed; a data call
  shows up only when the page turns it into the "can't be reached" sentence).
- Any other error a page shows in its own words.
- The judging pages' own drawn content, since they are not run in a browser.
- Pages past the limit of 300 a site (the report says when it stopped there).

## When it runs

| When | What it does | Silent when |
|---|---|---|
| Session start (hook) | Checks all three sites. A site that is only not running gets one quiet line naming it, with no question. A broken page on a running site prints the count and tells Claude to ask Omar whether to fix it this session | every site runs and is clean |
| Session end (Stop hook) | Only when this session edited a page file (bikar `packages/web` or `packages/lab`, the hub's `web/`) since it last ran. Blocks the stop once with the count when a running site has a broken page; a down site only gets a one-line note | no page file was edited, or nothing is broken |
| By hand | The full list | — |

When none of the three sites is running, the session-start check says it could not check rather
than staying quiet.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `.claude/skills/check-local-links/scripts/local_links.py` | Opens every page linked from the three sites' front pages and lists what is broken; `ev=` lines go to `$TMPDIR/local-links/run.log` | Omar says links are broken, or after changing Studio or hub pages; `--sites studio` for one site, `--json` for a machine-readable list | `make local-links` or `python3 .claude/skills/check-local-links/scripts/local_links.py [--sites studio,hub,judging]` |
| same, `--session-start` / `--stop` | The two hook modes above | Wired in `.claude/settings.json`; run by hand only to test a hook | `python3 .claude/skills/check-local-links/scripts/local_links.py --session-start` |
| same, `--self-test` | Checks the link reader and the "did this session edit a page" reader against fixtures | After changing the script | `python3 .claude/skills/check-local-links/scripts/local_links.py --self-test` |

Exit codes for the plain run: 0 nothing broken, 1 something broken, 2 no site running.
