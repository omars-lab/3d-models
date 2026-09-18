---
name: find-model
description: Find a printable 3D model from the maker repositories, bring it into Bambu Studio, and hand it straight into the print walkthrough. Use for "find a 3D model for X", "find me a print for X", "I want to print something that …", "search MakerWorld/Printables/Thingiverse for X", "download this model and queue it in Studio". It discovers candidates across a curated set of sources, lets you pick, acquires the file (MakerWorld one-click into Studio, or a download), records provenance + license, opens it in Bambu Studio, then routes into print-model and guide-print. It never dispatches — the physical send stays Omar's at the owner gate.
---

# find-model — discover a print, queue it in Studio, hand off to the walkthrough

You say **"find a 3D model for a …"** and this skill does the front half of a print job that today
happens by hand in a browser: it **searches the maker repositories**, shows you the best candidates,
**acquires** the one you pick, **opens it in Bambu Studio**, and then **routes into the existing print
pipeline** — [`print-model`](../print-model/SKILL.md) for the how (nozzle / orientation / supports /
filament / arrangement) and [`guide-print`](../guide-print/SKILL.md) for the operator runbook up to
the owner gate.

It owns discovery and acquisition. It owns **no** print mechanics of its own and it **never
dispatches**: slicing, the plan, and the physical send all belong to the skills it hands off to.

## The boundary (read first)

- **It advises and stages; it does not print.** The last thing this skill does is open the model in
  Studio and invoke `print-model`. The send stays Omar's `bambu print send` at the owner gate.
- **It respects licenses.** Every model carries a license. The skill surfaces it before download and
  records it with the file — and it will *not* quietly stage a No-Derivatives or Non-Commercial model
  for a use that violates it. When intent is unclear, it asks (see step 5).
- **It drives the browser you are already signed into.** MakerWorld / Printables / Thingiverse
  downloads generally want a logged-in session; the skill uses the `claude-in-chrome` tools against
  your own browser rather than scraping or handling credentials. It never configures an MCP server.

## How one run flows

1. **Pin the ask down** — turn "find a model for X" into search terms + the constraints that matter:
   what it is *for* (display / functional / mechanical), rough size vs the X2D bed
   (256 × 256 × 256 mm), whether it must be **free / commercial-use**, single- vs multi-colour, and
   any must-have features. State the assumptions you make; don't interrogate.
2. **Search the sources, in order** — work the ranked list in [`sources.md`](sources.md). Start with
   **Thangs** (it indexes across MakerWorld, Printables, Thingiverse, Cults3D — best for "is this out
   there at all"), then go native to **MakerWorld** (Bambu-first, one-click into Studio, tuned print
   profiles) and **Printables** (large, free, print-ready). Use `claude-in-chrome` to open each
   source's search URL (patterns in `sources.md`), read the results, and collect 3–6 real candidates
   with: title, source, author, licence, a popularity signal (downloads / likes / boosts), and the
   direct model URL. Record a GIF of the browse when it helps you show your work.
3. **Present the shortlist** — use `AskUserQuestion` with the candidates as options (put the
   distinguishing facts — source, licence, size, why-this-one — in each option so the choice is made
   from the comparison, not prose). Recommend one first, with the reason.
4. **Acquire the chosen model** — two clean paths, prefer the first:
   - **MakerWorld → one-click.** Use the model page's **"Open in Bambu Studio"** button (pick the
     print profile first; the profile is not printer-specific). Studio launches with the plate loaded
     — this is the same catalogue and the same one-step flow **Bambu Handy** prints from on your
     phone. No separate download step.
   - **Download → file.** For Printables / Thingiverse / Cults3D / a MakerWorld raw download, click
     download in your session and pick the file up from `~/Downloads`; move the `.3mf`/`.stl`/`.step`
     into the gitignored `.bambu/` staging area (see `.gitignore`) so it never lands in git.
5. **Record provenance + check the licence** — write a small sidecar next to the staged file (source
   URL, author, licence, date, the search that found it). If the licence is Non-Commercial or
   No-Derivatives and the intended use might cross it, surface that and let Omar decide before going
   further. Provenance is not optional here — a printed part with no record of where the design came
   from is an anecdote, the same way a reading with no profile header is (see `guide-print`).
6. **Queue it in Studio** — for the download path, `tools/bambu/bin/bambu slice open <staged file>`
   opens it in the Bambu Studio GUI for a first visual look. (The MakerWorld one-click already did
   this.) This is the same "open it in Studio" verb `guide-print` and `print-model` use, so there is
   one spelling of it.
7. **Hand off to the print walkthrough** — invoke [`print-model`](../print-model/SKILL.md) with the
   staged file as *"what to print"* (its step 1). print-model reasons nozzle / orientation / supports
   / filament / arrangement and composes the per-print plan + sliced plate + preview; then
   [`guide-print`](../guide-print/SKILL.md) runs the operator runbook and the pre-send go/no-go gate
   **up to the owner gate**. This skill stops here — it has found the model and put it in front of the
   pipeline; it does not slice, plan, or send.

## The sources (curated, ranked — full detail in `sources.md`)

| # | Source | Why it's here | Native format | Into Studio |
|---|--------|---------------|---------------|-------------|
| 1 | **Thangs** | Meta-search across 14M+ files (MakerWorld, Printables, Thingiverse, Cults3D, …) — start here to find *whether* the thing exists | links out | via its host |
| 2 | **MakerWorld** | Bambu-native; tuned print profiles; **one-click "Open in Bambu Studio"**; the catalogue Bambu Handy prints from | `.3mf` | one-click deep link |
| 3 | **Printables** | Large, free, actively maintained, print-ready; clean licences | `.3mf` / `.stl` | download → `slice open` |
| 4 | **Thingiverse** | Largest legacy library; things that never got re-uploaded | `.stl` | download → `slice open` |
| 5 | **Cults3D / MyMiniFactory** | Curated + premium (often paid); good for designed objects | `.stl` / `.3mf` | download → `slice open` |

`sources.md` carries the per-source search-URL patterns, licence models, download mechanics, and the
gotchas — it is a rubric read at run time, so the source list can sharpen without editing this skill.

## The Bambu Handy connection (why MakerWorld is #2, not lower)

The models on **Bambu Handy** *are* the MakerWorld catalogue. "Print the same model on Studio and on
Handy" is not a transfer between two libraries — it is one library (MakerWorld) reached two ways:
**Open in Bambu Studio** on the desktop, or **one-click print** from Handy on the phone when the
printer is bound to your Bambu cloud account.

**Caveat specific to this X2D:** it runs in **LAN Mode + Developer Mode** so we own the transport
(first-party FTPS + MQTT dispatch — see `docs/issues/first-party-dispatch.md`). That path is
deliberately cloud-decoupled, so Handy's *remote* one-click will not see a LAN-only job. The two ways
to print the same model therefore are: (a) **Studio → LAN dispatch** (our pipeline), or (b) rebind the
printer to the cloud to use Handy's remote print — a mode choice, not a limitation of this skill.

## Rules

- **The trigger is "find …", the exit is the owner gate.** This skill is the on-ramp; it always ends
  by handing a staged, provenance-recorded model to `print-model` → `guide-print`. It never slices,
  plans settings, or sends — those skills own that, and the send is Omar's.
- **Provenance travels with the file.** No staged model without a recorded source URL + author +
  licence. A print with no design provenance is not one we ship.
- **Licence before download.** Check it in step 5; refuse or ask when the intended use might cross it.
- **Downloads are gitignored.** Staged files live under `.bambu/`; they are never committed.
- **Prefer the one-click.** For a MakerWorld model, "Open in Bambu Studio" beats a raw download — it
  brings the tuned print profile and is the same flow Handy uses.
