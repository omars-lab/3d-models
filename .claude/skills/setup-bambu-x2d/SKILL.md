---
name: setup-bambu-x2d
description: Set up the Bambu Lab X2D (AMS combo) so Claude Code can drive it — install Bambu Studio, enable LAN + Developer Mode, wire the griches MCP, and stand up the tools/bambu CLI. Use when connecting the new printer to Claude, wiring up printing, choosing Bambu Studio stable vs beta, deciding Bambu Connect vs Developer Mode, or when `bambu setup doctor` reports something missing.
---

# Set up the Bambu X2D for Claude Code

This skill takes a boxed **Bambu Lab X2D AMS Combo** to the point where Claude can go from a bikar
`.bkr`/STL to a logged plate with one allow-listable command. It is the *judgment* layer; the
*mechanics* live in the [`tools/bambu`](../../../tools/bambu/README.md) CLI, and the *transport*
is a community MCP. Read this before touching the printer, then let the CLI's `--help` carry you.

## The three layers (why it's split this way)

```
this skill        → when/why, the decisions, the setup order        (judgment)
tools/bambu CLI   → our verbs, --help; bikar→slice→dispatch→record   (mechanics, one command)
  → griches MCP   → control/status/upload/AMS/camera transport
  → BambuStudio CLI → headless slicing
  → AppleScript   → GUI-only actions (Bambu Connect, some Studio dialogs)
Bambu firmware    → MQTT 8883 / FTPS 990 / X.509 (Developer Mode opens these on the LAN)
```

We **do not** reimplement the transport. The MQTT/FTPS/X.509 layer is exactly what Bambu's
firmware keeps changing (the January-2025 Authorization Control System is the current example), and
the community MCP already tracks it. We own only our glue — the setup order below and the
bikar→slice→dispatch→record workflow — and delegate everything else. (Consume, don't reimplement:
the same rule this repo applies to bikar.)

## Decisions (settled — don't re-litigate)

| Decision | Choice | Why |
|---|---|---|
| Control mode | **Developer Mode** (open MQTT/FTP on the LAN) | An MCP can only drive the machine over open MQTT/FTP; Bambu Connect alone only *routes slicer prints* and won't accept MCP control. |
| Transport MCP | **griches/bambu-mcp** | Best-maintained (MIT, `claude mcp add`), multi-printer, already handles the X.509 auth. Slicing lives in our CLI, not the MCP. |
| Bambu Studio | **Stable first, 2.8.x beta only if the X2D or dual-nozzle profiles are missing** | The X2D is new hardware; betas install side-by-side, but a beta 3MF can't upload to MakerWorld. |
| Build strategy | **Skill + CLI over the community MCP** | Reuse the moving-target transport; own only what's ours. |

**Bambu Connect vs Developer Mode** — the distinction that trips people up: Bambu Connect is the
*default, closed-source* path that lets a third-party slicer hand a sliced file to the printer
through an authorization broker; it does **not** expose the machine to arbitrary control. Developer
Mode is the *opt-in* that leaves MQTT, live stream, and FTP open on your LAN — which is what an MCP
needs. Enabling it means **you own the LAN security and Bambu won't support that mode.** We still
install Bambu Connect: it's the GUI/AppleScript fallback for actions with no headless path.

## The setup tasks (do in order)

1. **Network the printer, then find it.** Put the X2D on the LAN. Rather than reading the IP off
   the touchscreen, run `bambu setup discover`: it passively listens for the printer's own SSDP
   broadcast (receive-only — safe to run during an active print) and reports IP, serial, model,
   firmware, and — the tell — `connect cloud`. A printer still `cloud`-bound has **not** had LAN +
   Developer Mode enabled (step 3), so no host you configure will pass `doctor`'s LAN-reach yet.
2. **Install Bambu Studio** — stable: <https://bambulab.com/en/download/studio>. Launch it, add the
   X2D. If the printer or its dual-nozzle/auxiliary profiles are missing, install the **2.8.x beta**
   alongside (they coexist). X2D support reference:
   <https://bambulab.com/en/support/804923811139526656>.
3. **Enable LAN Mode, then Developer Mode** on the printer (touchscreen). This opens MQTT/FTP/live
   stream. Record the **access code** and **serial number**. Background on the authorization system:
   [Bambu Connect wiki](https://wiki.bambulab.com/en/software/bambu-connect) ·
   [Bambu's announcement](https://blog.bambulab.com/updates-and-third-party-integration-with-bambu-connect/).
4. **Install Bambu Connect** (the GUI fallback path): <https://wiki.bambulab.com/en/software/bambu-connect>.
5. **Wire the MCP.** Copy [`.mcp.json.example`](../../../.mcp.json.example) to `.mcp.json` (gitignored
   — it carries the token) and fill in host/serial/token/model=`x2d`. `bambu setup mcp` prints the
   block. MCP repo: <https://github.com/griches/bambu-mcp>.
6. **Build the CLI.** `cd tools/bambu && npm install` (repo-pinned Node — see the README).
7. **Preflight:** `bambu setup doctor` (add `--probe-mcp` for a live handshake). Fix every `✗`
   before going further; a `!` is a warning you can proceed past.
8. **Prove transport, read-only:** `bambu status show` returns live temps/AMS. This reaches the
   printer *without sending anything* — trust the pipe before any dispatch.
9. **Slice a test plate:** `bambu slice plate <model.stl>` (headless via the BambuStudio CLI;
   `--dry-run` prints the exact invocation, `--settings`/`--filament` pass profiles, and raw
   BambuStudio flags go after `--`). A `.bkr` must be rendered to STL first — slicing is not bikar's job.
10. **First dispatch is owner-gated.** `bambu print send <plate.3mf> --record` stays a deliberate
    call — no CAL bet is settled and printing is on hold. It is fail-closed: it prints the owner-gate
    notice, then refuses unless you pass `--yes` or confirm at a TTY (`--dry-run` shows what it would
    send without connecting). `--record` scaffolds a draft under the gitignored `.bambu/records/`.

## After setup — how we actually print

The CLI groups map to the workflow: `slice` (BambuStudio CLI) → `print send --record` (dispatch via
the MCP + scaffold a draft record under the gitignored `.bambu/records/`) → fill it in → `validate
record .bambu/records` (the record passes [`docs/prints-tab-design.md`](../../../docs/prints-tab-design.md)
§4 and the prints gate) → move the finished dir into `docs/prints/<date>-<slug>/`. Drafts stage in
`.bambu/` because the prints gate is **whole-tree**: an incomplete record under `docs/prints/` would
block every commit. `validate mesh <model.bkr>` runs bikar's min-strut/FDM `--check`, and `validate
plate` runs the 23-rung calibration table (`calibration-design.md` §7, D-014). A plate is
only a *prototype* if it answers a question — restate the questions first, exactly as the
[`prototype`](../prototype/SKILL.md) skill requires; if none would be answered, it's decoration.
Coupons that measure the *(machine, material, nozzle, profile)* settle a `CAL-*` bet via
[`calibrate`](../calibrate/SKILL.md), against the expectation table in
[`docs/calibration-design.md`](../../../docs/calibration-design.md) §7. Render/thumbnail checks are
[`validate-render`](../validate-render/SKILL.md)'s job. The per-print rubric the CLI reads at runtime
is in [`rubric.md`](rubric.md).

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `discover` finds nothing | wrong subnet / guest VLAN, or long broadcast gap | same LAN as the printer; raise `--timeout` (it broadcasts every ~30s) |
| `discover` shows `connect cloud` | LAN + Developer Mode not enabled | enable both on the touchscreen (step 3); the field flips off `cloud` |
| `printer config missing` | env + `.mcp.json` both unset | copy `.mcp.json.example`; `bambu setup mcp` |
| `LAN reach …:8883 no connection` | Developer Mode off, or wrong IP | re-enable LAN + Developer Mode; recheck the IP with `bambu setup discover` |
| `MCP handshake FAIL` | token/serial wrong, or model unsupported | re-copy the access code; verify `x2d` is accepted (`--probe-mcp`) |
| `no status-like tool found` | griches renamed/omitted a tool | run `--probe-mcp` to list tools; update the CLI's hints |
| `Bambu Studio not found` | not installed, or non-standard path | install it, or set `SLICER_PATH` |
| `camera failed … needs ffmpeg` | ffmpeg absent | `brew install ffmpeg` (only for snapshots) |
| osascript timed out | a GUI dialog is blocking | dismiss the dialog in the app; GUI fallback can't proceed past a modal |

## Rules

- **Developer Mode is a security decision you own.** Say so out loud before enabling it; it's
  outward-facing and owner-gated.
- **The token is a secret.** It lives only in the gitignored `.mcp.json`; never commit it, never
  print it in full (the CLI masks it).
- **Read-only before write.** `status show` must succeed before any `print send`.
- **A dispatch is owner-gated** until a CAL bet justifies the print. The CLI confirms before sending.
- Full sequencing and the build-vs-buy reasoning: [`.claude/plans/binary-tickling-kay.md`](../../plans/binary-tickling-kay.md).
