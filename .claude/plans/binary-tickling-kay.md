# Plan: `setup-bambu-x2d` skill + `tools/bambu` CLI + blog post

## Context

A new **Bambu Lab X2D AMS Combo** (dual-nozzle, enclosed, AMS 2 Pro) has arrived and needs to
be driven from Claude Code — not just monitored, but sliced-and-dispatched as part of the
existing bikar → print-record workflow this repo already runs. Today none of that is wired: no
`.mcp.json`, no printer CLI, no setup procedure. This plan builds three layered artifacts so the
next session can go from a `.bkr`/STL to a logged plate with one allow-listable command, and
publishes a companion blog post explaining what each piece is and *why* it exists.

Printing itself stays **owner-gated** (no CAL bet settled; see memory *owner-gated-and-on-hold*).
This work builds the *capability* and the setup path; the first physical dispatch remains Omar's
call, and the CLI's dispatch verbs default to confirm-before-send.

## Decisions settled (via Q&A this session)

| Decision | Choice | Why |
|---|---|---|
| Control mode | **Full control via Developer Mode** (open MQTT/FTPS on LAN) | Community MCPs need open transport; Bambu Connect only routes slicer prints |
| Build strategy | **Skill + CLI companion over a community MCP** | Reuse the moving-target transport; own only our bikar/docs-prints glue |
| Transport MCP | **griches/bambu-mcp** (Node, MIT, 45★, `claude mcp add`, X.509 handled, multi-printer) | Best-maintained; slicing lives in *our* CLI, not the MCP |
| Bambu Studio | **Stable 2.7.x, fall back to 2.8.x beta** if X2D/dual-nozzle profiles missing | X2D is brand-new; betas install side-by-side |
| Home | **3d-models repo** — skill in `.claude/skills/`, CLI in `tools/bambu/` | Next to prototype/calibrate; feeds `docs/prints/` directly |
| CLI shape | **Command groups + multi-backend router** | Groups: print/validate/slice/status/setup. Router picks backend per verb |

## Architecture — three layers

```
SKILL.md (setup-bambu-x2d)  → when/why, setup tasks, decisions; reads rubric.md at runtime   (judgment)
tools/bambu  (our CLI)      → command groups, rich --help, bikar→slice→dispatch→record        (mechanics, allow-listable)
   ├─ backend: griches MCP  → control, upload, AMS, camera, status   (JSON-RPC via @modelcontextprotocol/sdk client)
   ├─ backend: BambuStudio CLI → headless slice (.3mf/.stl → sliced .3mf/gcode)
   └─ backend: AppleScript/osascript → last-resort GUI automation of Bambu Studio.app / Bambu Connect.app
community griches MCP + Bambu firmware  → MQTT 8883 / FTPS 990 / X.509 transport   (delegated, never reimplemented)
```

**Backend router rule (cheapest capable backend wins, GUI last):** MCP → BambuStudio CLI →
AppleScript. AppleScript only where no headless path exists (e.g. Bambu Connect is closed-source
GUI-only). Per global observability tenet, every `osascript`/BambuStudio-CLI shell-out gets a
**timeout that logs `ev=*_timeout` and recovers**, and each long op logs one line before and one
after to a greppable file.

## Deliverables

### A. Skill — `.claude/skills/setup-bambu-x2d/`
- `SKILL.md` — frontmatter `description` is the dispatch prompt, so write it strong (triggers on
  "set up the Bambu / X2D printer", "connect the printer to Claude", "wire up printing"). Body =
  the ordered **setup task checklist** (below) with all links, plus the layering explanation and a
  Troubleshooting table.
- `rubric.md` — the per-print decision rubric the CLI/skill reads at runtime (which nozzle profile,
  when a plate is a real prototype vs decoration — mirrors `prototype` skill's "restate the
  questions" rule).
- Cross-links to `prototype`, `validate-render`, `calibrate` skills and `docs/prints-tab-design.md`.

### B. CLI — `tools/bambu/` (self-contained TS package, run via `tsx`; no root package.json exists)
- `package.json` + `tsconfig.json` (deps: `commander` for groups, `@modelcontextprotocol/sdk`
  client, `execa`/`node:child_process` for BambuStudio CLI + `osascript`). Node **v22.22.3** via the
  repo's pinned PATH prefix.
- **Command groups** (`bambu <group> <verb> --help` everywhere; help *is* the docs):
  - `bambu setup` — `doctor` (LAN mode? dev mode? token reachable? X2D model supported? Studio +
    ffmpeg installed?), `mcp` (write/verify `.mcp.json`), `studio` (detect stable/beta, guide install).
  - `bambu slice` — `plate <model.bkr|stl>` → BambuStudio CLI headless slice with the X2D dual-nozzle
    profile → sliced `.3mf`. Wraps the Bambu CLI; falls back to AppleScript-driving Studio if headless
    slice unsupported for a needed option.
  - `bambu print` — `send <plate.3mf> [--record]` (dispatch via griches MCP, **confirm-before-send**),
    `pause`/`resume`/`stop`, `ams` (slots/RFID). `--record` writes the `docs/prints/<date>-<slug>/`
    record so it passes `.claude/gates/prints_gate.py` / `make validate-prints`.
  - `bambu validate` — `mesh` (bikar min-strut/FDM `--check`), `plate` (against calibration
    expectation table, `docs/calibration-design.md` §7, 23 rows; D-014), `record` (record satisfies
    the prints gate before commit).
  - `bambu status` — `show`/`monitor` (temps/progress/AMS via MCP), `camera` (snapshot; needs ffmpeg).
- **Backend router module** + a `backends/` dir (`mcp.ts`, `studio-cli.ts`, `applescript.ts`) with the
  timeout+logging wrapper.

### C. Config — `.mcp.json` (repo root, gitignored-secret-aware)
griches entry with `PRINTER_HOST`, `BAMBU_SERIAL`, `BAMBU_TOKEN` (LAN access code/token), model.
**Secret handling:** token never committed — document sourcing it via env/`.env` (repo tenet:
fail-closed on secrets). Provide `.mcp.json.example`; real one gitignored.

### D. Makefile — new targets appended at **END** (per repo convention)
`bambu-doctor` (→ `tools/bambu setup doctor`), `bambu-validate` (mesh+plate+record). Keep each a
single allow-listable command.

### E. Blog post — `../omars-lab.github.io/bytesofpurpose-blog/blog/2026-09-13-driving-a-bambu-x2d-from-claude-code.md`
Separate repo → its own branch→PR (draft: true, authors [oeid], kind: framework/walkthrough).
Structure (bytesofpurpose framework voice, like `2026-08-04-deciding-what-to-buy.md`):
1. The goal: a `.bkr` to a logged plate with one command, no GUI babysitting.
2. Why each component exists — Studio (slice), **Bambu Connect vs Developer Mode** (the
   authorization system, why open control needs Dev Mode), the **MCP** (transport), **our CLI**
   (contextualized verbs), the **skill** (judgment layer).
3. **The MCP comparison table + build-vs-buy** (griches vs rowbotik vs schwarztim vs Shockedrope vs
   the mcpmarket BambuStudio-CLI skill) and why we wrap, not rebuild, transport.
4. The setup tasks, with links.
5. Security note: what Developer Mode opens and who owns that risk.

## The setup task checklist (goes in SKILL.md **and** the blog)

1. **Unbox / network** — put X2D on the LAN, note its IP.
2. **Install Bambu Studio** — stable first: <https://bambulab.com/en/download/studio>. If X2D/dual-nozzle
   profiles absent, install the 2.8.x beta alongside. X2D support ref:
   <https://bambulab.com/en/support/804923811139526656>.
3. **Printer: enable LAN Mode**, then **toggle Developer Mode** (opens MQTT/FTP/live-stream). Record
   **access code + serial**. (Context: Bambu Connect authorization system —
   <https://wiki.bambulab.com/en/software/bambu-connect>,
   <https://blog.bambulab.com/updates-and-third-party-integration-with-bambu-connect/>.)
4. **Install Bambu Connect** (kept for the GUI/AppleScript fallback path even though control goes via
   Dev Mode): <https://wiki.bambulab.com/en/software/bambu-connect>.
5. **Install the MCP** — griches/bambu-mcp (<https://github.com/griches/bambu-mcp>): `claude mcp add`
   or `.mcp.json`; verify with `bambu setup doctor`.
6. **Build the CLI** — `tools/bambu` deps + `bambu setup doctor` green.
7. **First read-only check** — `bambu status show` returns live temps/AMS (proves transport before any
   dispatch).
8. **Slice a test plate** — `bambu slice plate <model>` headless.
9. **(Owner-gated) first dispatch** — `bambu print send --record`; stays Omar's call.

Reference — the alternative packaged skill considered:
<https://mcpmarket.com/tools/skills/bambu-lab-3d-print-automation> (wraps BambuStudio CLI; its
slice/search idea is folded into our `slice` group). MCP SDK for the CLI client:
<https://github.com/modelcontextprotocol/typescript-sdk>.

## Gates & tenets to honor while implementing
- **docs_gate**: any `**Default:**` (e.g. slice profile values) needs a citation or `CAL-*` id (K4/D3);
  a `**Validator:**` needs PASS:/FAIL: (K6/D2); all relative links resolve (D1). SKILL.md + blog obey.
- **Anchored pointers**: cite bikar/sibling files at a **git ref**, not a bare path (repo pointer gate).
- **PR flow**: branch → PR → merge in *both* repos; never direct-to-master; delete branch after merge.
- **No `git add -A`** — stage by name; shared working tree.
- Consider a **decisions-log** entry for the build-vs-buy call (grab the next free D-0xx carefully —
  see memory *decision-id-collision*); a `docs/issues/` file only if implementation forces a pivot.

## Verification (end-to-end)
1. `tools/bambu setup doctor` → all preflight checks pass (or name the missing one).
2. `bambu status show` → live printer status via the griches MCP (read-only proof of transport).
3. `bambu slice plate <fixture>` → produces a sliced `.3mf` headless.
4. `bambu validate record <dir>` and `make validate-prints` → a `--record` output passes the prints gate.
5. `make validate` (local.ci) stays green with the new skill/docs/Makefile targets.
6. Blog post builds/serves in the omars-lab repo (`make serve-locally` there); links resolve; draft: true.

## Sequencing
Phase 1 — CLI skeleton + `setup doctor` + `.mcp.json.example` + griches wired + `status show` (read-only,
provable without printing). Phase 2 — `slice` group (BambuStudio CLI). Phase 3 — `print`/`validate`
groups + `--record` + gates + Makefile. Phase 4 — SKILL.md + rubric. Phase 5 — blog post (separate PR).
Each phase is its own branch→PR.
