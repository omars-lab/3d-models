# find-model sources — where to search, how to get the file, what the licence lets you do

A run-time rubric for [`SKILL.md`](SKILL.md) step 2. Ranked by usefulness for **"find a printable
model for X, for the Bambu X2D"**. Search URLs are the current patterns — the skill drives a real
browser, so verify the live form and adapt rather than trusting a stale query string. Always read the
model page's own licence line; the summaries below are the *shape* of each site's licensing, not a
per-model ruling.

## The ranked list

### 1. Thangs — the meta-search (start here)
- **Why first:** indexes 14M+ files across MakerWorld, Printables, Thingiverse, Cults3D and dozens of
  smaller sites, plus geometric similarity search. Best single query to learn whether the thing exists
  and where the good versions live.
- **Search:** `https://thangs.com/search/<query>` (spaces → `%20`).
- **Acquire:** Thangs links out to the host (or mirrors a download). Follow the link to the source and
  acquire there, so the licence + provenance come from the real origin.
- **Licence:** inherited from the host — record the *host's* licence, not Thangs'.

### 2. MakerWorld — Bambu-native, one-click into Studio
- **Why:** 2M+ free models tuned for Bambu machines, each with ready **print profiles**; the catalogue
  **Bambu Handy** prints from. The cleanest path to a plate.
- **Search:** `https://makerworld.com/en/search/models?keyword=<query>`.
- **Acquire (preferred):** on the model page pick a **print profile** (right side), then **"Open in
  Bambu Studio"** (green button, or the dropdown). Studio launches with the plate loaded — profiles
  are not printer-specific, so pick X2D / filament / plate in Studio. No file to manage.
- **Acquire (fallback):** **Download** → `.3mf` (carries the profile) or `.stl`. Login required.
- **Licence:** Creative Commons variants, declared per model; many CC-BY, some **NC** (non-commercial)
  / **ND** (no-derivatives). MakerWorld also has a points/boost economy — points are not a licence,
  the CC line is. Respect NC/ND.

### 3. Printables — large, free, print-ready, clean licences
- **Why:** modern browsable library, fast search, active creators, clearly-labelled CC licences,
  print-ready files. The best general free source after MakerWorld.
- **Search:** `https://www.printables.com/search/models?q=<query>`.
- **Acquire:** **Download** the `.3mf` (preferred, may carry a Prusa/Bambu profile) or `.stl`; files
  arrive in `~/Downloads`, sometimes zipped. Login usually required. Move the file into the gitignored
  `.bambu/` staging area, then `bambu slice open` it.
- **Licence:** Creative Commons, labelled on each model page.

### 4. Thingiverse — the legacy giant
- **Why:** 15+ years of designs, millions of them, many never re-uploaded anywhere else. Reach here for
  older or niche things the newer sites don't have.
- **Search:** `https://www.thingiverse.com/search?q=<query>&type=things`.
- **Acquire:** **Download All Files** (zip) or a single `.stl`. Quality varies — eyeball the mesh in
  Studio (`bambu slice open`) before trusting it; older files may be non-manifold.
- **Licence:** Creative Commons + GPL + occasional custom. Read the page.

### 5. Cults3D / MyMiniFactory — curated + premium
- **Why:** designed objects, often higher craft; a mix of free and paid. Good when quality matters
  more than free.
- **Search:** `https://cults3d.com/en/search?q=<query>` · `https://www.myminifactory.com/search?query=<query>`.
- **Acquire:** free models download after login; paid models must be **purchased** — surface the price
  and stop for Omar's call before any purchase (spend is a one-way door). Files land in `~/Downloads`.
- **Licence:** per-model, frequently a **Standard / personal-use** licence with a separate commercial
  licence for sale; check before any commercial use.

## Choosing between candidates

Prefer, in order: **a Bambu-tuned `.3mf` on MakerWorld** (one-click, profile included) → **a well-liked
`.3mf` on Printables** → **an `.stl` with a permissive licence and a real popularity signal**. Break ties
on: licence fit for the intended use, printability for FDM on the X2D (no unsupported thin overhangs the
part can't afford), size vs the 256 mm bed, and colour count vs the loaded AMS.

## What always gets recorded (provenance)

For every staged model, write next to the file: **source URL · author · licence (verbatim) · date ·
the search query that found it**. This is the design-side twin of the profile header `guide-print`
requires before any measurement — a printed part whose origin isn't recorded is an anecdote.

## Hard rules

- **Licence before download**, and again before any commercial use. Refuse or ask on NC/ND when intent
  might cross the line.
- **Never purchase** a paid model without Omar's explicit go — surface the price and stop.
- **Staged files are gitignored** (`.bambu/`), never committed.
- **Drive the signed-in browser**, don't scrape or handle credentials; never stand up an MCP server.
