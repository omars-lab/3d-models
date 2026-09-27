# Loop prompt — take a tutorial video apart and rebuild it

Paste the block below into a fresh session **in the youtube repo** (`~/Workspace/git/youtube`),
or run it there as `/loop` with no interval. Written 2026-09-25; queue and skills added
2026-09-27. It lives here, next to the
other loops, because its output is what the catalog loop turns into coasters
([`catalog-expansion.md`](catalog-expansion.md)).

---

## The goal

**One tutorial video at a time becomes a GeoGebra construction that is proved to match the
video.** Every scored step must pass, and a person must have looked at the render. Each video
also leaves the tooling better for the next one.

The youtube repo calls one video taken all the way a **rung**, and the sequence of videos the
**ladder**. A rung is done when:
- `scripts/yt-study.sh status <id>` is green,
- the notes say how the construction converged and what caught each mistake,
- every gap the rung exposed in the tooling is either fixed or filed.

## Where it stands (2026-09-27)

All ten rungs so far are Sarah Brewer videos. On 2026-09-27 two independent researchers and a
checker screened 29 videos and GeoGebra files from other creators. The
[consolidated screen](../../docs/research/candidate-screen-2026-09-27.md) is the one to act on,
and item 2 of the [catalog backlog](../../docs/tasks/catalog-expansion/backlog.md) is the live
copy of the queue. When a rung finishes or a verdict changes, update that backlog as well as this
table.

These are the next rungs, in rebuild order. Each is still judged only from its thumbnails and
preview frames, so screen it again with `youtube-screen` before spending a rung on it.

| # | Id | Creator | What it is | What to watch for |
|---|---|---|---|---|
| 1 | `0ke_GpoBa-s` | Samira Mian | 10-fold rosette, 43 min, chaptered | Its fivefold rectangle is the layout 3 and 5–7 reuse, so do it first |
| 2 | `88q-u2eWZqg` | Eman Zainab | 16-petal rosette | A new fold; the centre may crowd at 90 mm |
| 3 | `n_ICgwOr6qs` | Samira Mian | 5-fold arc motif | Rebuild the 1:20–8:06 construction only, not the freehand painting finish; needs the arc path `nmEjCTzMbDg` used |
| 4 | `Y6kS1MvnKoc` | Eric Broug | 10-fold star field from a Mamluk Qur'an page (1305, Cairo) | A field, not one rosette; crop to the centre star |
| 5 | `NtnlGMTElBk` | Samira Mian | 10-fold interlaced star | 82 s, no narration: evidence comes from frames only |
| 6 | `yZN_wn0uvTY` | Geogebra_Road to School | 10-fold rosette built on screen in GeoGebra | Narrated in Indonesian; the algebra list on screen is the evidence |
| 7 | `_U6G8QSfWnk` | Samira Mian | 5/10-fold girih tiling (part 1 of 4) | Conditional: faint tracing steps, may be near-solid, may need a one-cell crop |
| 8 | `fhGHzop7ULw` | Mohamad Aljanabi | 6-fold rectangle repeat unit | A new creator, but not a new fold |
| 9 | `jlTmt_279M4` | unravelling pattern | 7-point stars in a square (Bourgoin pl. 170) | Conditional: preview frames near-white; the 7-division may be approximate |
| 10 | `A9fefFurD_s` | Lex Wilson | 10-point star, Broug's method | Low priority |

Held: `LoCRh3SOhls` (a pentagon-framed variant of 1) and GeoGebra `hzyhmg9p` (the page says 9-
and 12-pointed stars, its preview shows 8/9/5; open the applet first). Cross-check only:
GeoGebra `cjAFU4ck`. No 9-fold video by anyone but Brewer turned up in the space searched.

**Licence:** no video in the queue showed a Creative Commons marker, so each is presumed to be
under the standard YouTube licence. Record that in the rung's provenance before any download.
GeoGebra files are probably CC BY-NC-SA (non-commercial); flag that if a coaster from one is
ever sold.

**Two fixes in this repo wait on Omar's OK.** They come from the
[oracle-FAILs note](../../docs/research/ledger-oracle-fails-2026-09-27.md). Make them only after
he says yes:
- `reconstructions/nmEjCTzMbDg/construction.ggb-commands` L84: `R = Intersect(t, m, 2)` →
  `R = Intersect(t, m, S)`. The second root is a different point in bikar, and this is what still
  fails nmEj's O1 and O2.
- `scripts/naqsh_score.py` `ssim_score`: `ggb_score.py` exits 2 on FAIL and 1 on an error, but
  the score treats 2 as a crash. Accept `(0, 2)`.

## Skills this loop runs on

The youtube repo's skills, by the step they serve. Use the skill, not a hand-rolled command.

| Step | Skill | What it does |
|---|---|---|
| Whole loop | `youtube-ladder` | Owns the loop: screen, study, close gaps, record |
| Find candidates | `youtube-discover`, `youtube-discovery` | Crawl for new videos; keep the discovery wiki (creators, concepts) |
| Screen | `youtube-screen` | Is this video worth a rung? GO or NO-GO |
| Gather evidence | `youtube-metadata`, `youtube-transcript`, `youtube-keyframes`, `youtube-download` | Title, chapters and licence; the narration; key frames and contact sheets; a local copy (after the licence step) |
| Rebuild | `youtube-study`, `youtube-reconstruct` | One rung end to end; the GeoGebra construction itself |
| When it goes sideways | `youtube-retro` | The same step failed twice: stop and look back |
| Record | `youtube-learnings`, `youtube-data`, `youtube-hub`, `youtube-feedback` | Write up what the video taught; keep the data and study hub current |

**Grow the skills as the queue exposes gaps.** This queue is the first set from outside one
creator's style, and it will push the skills in places the Brewer rungs never did. When the
same friction comes up in two rungs, fix it in the skill that owns that step, in the same
commit. Change a skill's `description` line first if the skill failed to fire. Add a new skill
only when no existing one owns the step. The places this queue is likely to push:
- **Screening without the video.** The 2026-09-27 screen judged fit from thumbnails and
  YouTube's storyboard preview sheets (yt-dlp metadata only). If that proves reliable, fold it
  into `youtube-screen` so screening never needs a download.
- **No narration, or narration not in English** (5, 6): frames and the on-screen algebra list
  are the only evidence. `youtube-keyframes` should say how to read a construction off frames
  alone.
- **Arc constructions** (3): the arc path from `nmEjCTzMbDg` belongs in `youtube-reconstruct`,
  not rediscovered.
- **A field, not one rosette** (4, 7, 8): record which cell the coaster crops to, so the
  catalog loop does not have to guess.
- **Licence check per video:** yt-dlp's licence field came back empty for all 12 videos
  re-read. Say in `youtube-metadata` how to confirm the licence by eye.
- **New creators in the discovery wiki:** it has a page only for Sarah Brewer. Add a creator
  page for each new creator as their first rung starts.

## Start here (in the youtube repo)

- The `youtube-ladder` skill owns the loop: screen, study, close gaps, record. Follow it.
  `youtube-study` does one rung. `youtube-reconstruct` does the construction.
  `youtube-retro` is for when a rung goes sideways.
- The next rungs are the table above, not `make ladder`'s older list, until the table is
  worked through.
- The ladder and its numbered gaps are in that repo's `.claude/plans/learning-from-youtube.md`.
  Finished rungs are in its `docs/tasks/done.md`.
- The worked example of a good iteration log is `reconstructions/bknVRSMcLj0/notes.md`: one
  entry per commit, what was wrong, and what caught it.
- `make ladder` lists the candidates; `yt-study.sh status <id>` shows a half-done rung.

## Each pass of the loop

1. **Finish before starting.** If any rung is half-done, finish it first.
2. **Screen, don't inherit.** Take the next row of the queue above (then `make ladder` once
   it is empty) and screen it again with `youtube-screen`. The queue's verdicts came from
   thumbnails. Prefer a GO with a short gap list over the next line of an old list. Write the
   verdict with its date, and if it turns NO-GO, remove it from the catalog backlog's queue too, with the reason in that screen's notes.
3. **Rebuild it.** Take evidence from the frames (keyframes, zoomed crops), never from a
   guess that happens to fit a crowded frame. Build, score, look at the render, fix, and
   commit each step that improves the score, with the reason in the commit message.
4. **Close the gaps.** Name every place the tooling made the rung harder. Fix the small ones
   with a test. File the big ones as numbered gaps in the plan.
5. **Hand it on.** When the rung is done, add a line to `done.md` saying what the tooling can
   now do. Hand the id to the catalog loop by adding it to 3d-models'
   [`docs/tasks/catalog-expansion/backlog.md`](../../docs/tasks/catalog-expansion/backlog.md)
   as a reconstruction ready to migrate.
6. **Stop** when: no candidate can be screened today; the next rung needs a gap bigger than
   one rung; the same step fails the same way twice (run `youtube-retro`); or Omar's own
   limit is reached. Say which one, then schedule the next wakeup 30 to 60 minutes out.

## Never

- Never mark a rung done on a best-effort score that no one has looked at.
- One rung per pass. Never fan out across videos.
- youtube has no remote. Commit on its main branch through its own checks, and keep
  generated renders out of git.
- Never download a video without the youtube skills' own licence and provenance steps.
