---
produced: 2026-09-16
produced-by: web research (Claude subagent), real WebSearch/WebFetch
feeds: docs/bambu-cli-design.md (the tools/bambu CLI transport design)
scope: survey of ways to drive a Bambu X2D + slice headless, to ground the CLI backend choice
---

# Bambu X2D control-transport & headless-slicing survey

## What was surveyed (and what was not)

This surveys **the concrete options I could find and verify by real web search/fetch on
2026-09-16** for two jobs: (a) driving a Bambu Lab printer over the LAN — status, control,
file upload, camera; and (b) slicing models headless. **16 options are covered here**, grouped
into Control/transport (5 MCP servers + 1 Go CLI), Slicing (4), and Library layer (5, some
overlapping). This is **not** an exhaustive census of the Bambu tooling ecosystem — new MCP
servers and forks appear weekly (the search surfaced at least four near-identical forks of one
`bambu-printer-mcp` alone). Where a fact could not be confirmed from a fetched primary source
it is marked **unconfirmed**, with what would settle it.

Target machine context that shapes every "does it support this?" answer below: the printer is a
**Bambu X2D** — a *dual-nozzle* H2-series machine (Bambu's dual-nozzle line: H2D / H2D Pro / X2D),
firmware `01.02.00.00`, currently cloud-bound with **LAN Mode + Developer Mode not yet toggled**.
The X2D is new (2025-2026) and shares its firmware track and MQTT/camera shape with the H2D, but
is **rarely named explicitly** by any third-party tool — this is the survey's central risk (see
Gaps & risks).

---

## 1. Official API situation

**What it is.** Bambu Lab publishes **no public, documented, stable local or cloud API** for
third-party control. The only *officially sanctioned* third-party path is **Bambu Connect**, a
closed desktop app that brokers "cloud account login, printer management, LAN mode connectivity,
file import and printing" — third parties are meant to integrate *through* Bambu Connect, not
against a documented protocol
(https://blog.bambulab.com/updates-and-third-party-integration-with-bambu-connect/ ,
https://wiki.bambulab.com/en/software/third-party-integration).

**The LAN protocol (community-reverse-engineered).** Bambu printers speak, on the LAN:
- **MQTT over TLS on port 8883** — status telemetry and control (start/pause/stop, temps, speed,
  AMS, movement, raw G-code). Brokers for cloud are `us.mqtt.bambulab.com` / `cn.mqtt.bambulab.com`;
  LAN uses the printer itself as broker.
- **FTPS on port 990** (implicit TLS) — upload/list/delete `.3mf` / `.gcode` files.
- **Camera stream** — model-dependent: raw TCP on port 6000 for A1/P1, RTSP (X1/H2 series).

None of this is officially documented. The de-facto references are community projects:
**Doridian/OpenBambuAPI** (https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md),
**coelacant1/Bambu-Lab-Cloud-API** (https://github.com/coelacant1/Bambu-Lab-Cloud-API/blob/main/API_MQTT.md),
and the **greghesp/ha-bambulab** Home Assistant integration (https://github.com/greghesp/ha-bambulab).

**What LAN Mode / Developer Mode unlock.** "LAN-only Mode" disconnects the printer from Bambu
cloud (local devices only). "Developer Mode" opens the **MQTT channel, live video stream, and
FTP** for local apps to actually drive the printer. Bambu states plainly that these protocols are
**"not officially supported" and carry no customer support**, and that Developer Mode works
**only in LAN Mode** (no cloud while enabled)
(https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode ,
https://help.simplyprint.io/en/article/bambu-lab-lan-only-mode-and-developer-mode-how-to-enable-xa0hch/).
Bambu's own docs historically listed Developer Mode for **X1, P1, A1, A1 Mini**; the H2/X2 series
now have LAN/Developer-Mode-capable firmware on the same download track
(https://bambulab.com/en-us/support/firmware-download/x2d — "The Dual-Nozzle 3D Printer for
Everyone", firmware V01.02.00.00 dated 2026/08/06, matching the target printer). Whether the X2D's
Developer Mode exposes exactly the same MQTT/FTP surface as X1/P1 is **unconfirmed** until toggled.

**The January 2025 auth wall (carry this hedge).** A Jan-2025 firmware update added an
authentication requirement: certain "critical" MQTT messages must be **signed with an X.509
certificate/private key** shipped inside Bambu Connect, which broke OctoPrint, Home Assistant and
custom scripts. The community extracted that cert/key from the Bambu Connect binary to restore
access (https://hackaday.com/2025/01/19/bambu-connects-authentication-x-509-certificate-and-private-key-extracted/).
Bambu's sanctioned escape hatch is exactly **Developer Mode**, which removes the signing
requirement — *at the cost of cloud and of official support*. So on this X2D, Developer Mode is
both the enabler and the thing that keeps us off the fragile cert path.

**Official developer program (2025-2026).** I found **no** announced public developer API/program
beyond Bambu Connect integration. **Unconfirmed** that one exists; to settle it I'd want a Bambu
blog/wiki page announcing a documented API — none surfaced.

**X2D / dual-nozzle support:** Protocol exists and is reachable in principle once Developer Mode is
on; the *dual-nozzle-specific* MQTT payload shape (e.g. `ams_mapping2` parallel arrays seen in H2
tooling) is handled by some tools but **unverified against a real X2D**.

---

## Control / transport options

### 2a. griches/bambu-mcp  (the repo the current transport references)
- **What it is.** MCP server to control Bambu printers / a fleet from any MCP client.
- **Transport/protocol.** MQTT (8883, TLS) + FTP (990, implicit FTPS). TypeScript/Node.js;
  **no Python SDK** underneath — self-contained.
- **Capabilities.** status ✅ · control ✅ (start/pause/resume/stop, skip objects, lights, temps,
  speed, nozzle config) · upload ✅ (list/upload/download/delete) · camera ✅ · slice ❌ · AMS ✅ ·
  raw G-code ✅.
- **Maintenance & license.** README (fetched) states **MIT**, ~45 stars / 14 forks / 16 commits,
  recent activity; requires **LAN Only + Developer Mode**. Star/commit counts are point-in-time and
  **may have drifted** — treat as approximate.
- **X2D / dual-nozzle.** README's tested list (as fetched) names **P1S, H2D, A1 Mini** and says it
  "should work with any Bambu printer supporting MQTT over LAN." **H2D is the X2D's dual-nozzle
  sibling**, so this is the strongest single signal that the dual-nozzle MQTT shape is handled —
  but **X2D itself is not named**; treat as *likely, unconfirmed*.
- **Source.** https://github.com/griches/bambu-mcp (also listed https://lobehub.com/mcp/griches-bambu-mcp)

### 2b. synman/bambu-mcp
- **What it is.** Fully self-contained LAN-mode MCP server, **85 tools**.
- **Transport/protocol.** MQTT + FTPS; persistent MQTT sessions; encrypted (AES-256-GCM)
  credential store; write-protected state-changing tools.
- **Capabilities.** status ✅ · control ✅ · upload ✅ · camera ✅ · slice ❌ · raw commands ✅ ·
  discovery/climate/filament/detectors ✅.
- **Maintenance & license.** Version 0.9.0, ~253 commits (active). **License not stated in the
  excerpt fetched — unconfirmed** (would need the LICENSE file / README badge).
- **X2D / dual-nozzle.** Camera module branches on **`X1/H2D` vs `A1/P1`**, and the README text
  references **"X2" and "dual-nozzle"** — the most explicit X2-adjacent mention found. Still
  **unconfirmed against a real X2D**.
- **Source.** https://github.com/synman/bambu-mcp

### 2c. schwarztim/bambu-mcp
- **What it is.** MCP server, local MQTT real-time control + monitoring.
- **Transport/protocol.** MQTT (local) + FTPS upload + **X.509 certificate signing** (handles the
  Jan-2025 auth path explicitly).
- **Capabilities.** status ✅ · control ✅ · upload ✅ · camera ✅ · slice ❌ · AMS ✅.
- **Maintenance & license.** Listed on Glama/LobeHub/MCPWorld. Version/stars/license **unconfirmed**
  from search snippets.
- **X2D / dual-nozzle.** README names **P1P, P1S, X1C, A1, A1 Mini** — all *single-nozzle*.
  **No H2D/X2 mention → dual-nozzle unconfirmed, likely unsupported without changes.**
- **Source.** https://github.com/schwarztim/bambu-mcp , https://glama.ai/mcp/servers/schwarztim/bambu-mcp

### 2d. DMontgomery40/bambu-printer-mcp  (control **and** slice — notable)
- **What it is.** MCP server that both drives the printer **and wraps a slicer**, plus STL editing.
  (Several near-identical forks exist: pixeldublu, rowbotik, offthehook-*… — one codebase, many
  copies.)
- **Transport/protocol.** stdio + Streamable HTTP to the MCP client; **FTPS** for upload; camera
  via TCP-6000 (A1/P1) or **RTSP via ffmpeg (X1/H2 series)**; slicing by shelling out to
  **BambuStudio CLI** (also OrcaSlicer/PrusaSlicer/Cura/Slic3r).
- **Capabilities.** status ✅ · control ✅ (pause/resume/cancel, speed, fan, light) · upload ✅ ·
  camera ✅ (JPEG snapshots) · **slice ✅ (STL→3MF via BambuStudio CLI, with profile-flattening
  workarounds)** · STL tools ✅ (scale/rotate/base/merge/center/lay-flat).
- **Maintenance & license.** **GPL-2.0**, ~140 stars / 27 forks / 69 commits, active (open issues/PRs).
- **X2D / dual-nozzle.** **Explicitly lists H2, H2S, H2D, H2C** and implements H2-specific MQTT
  formatting (`ams_mapping2` parallel array). **No X2 by name** — but the H2-series handling is the
  right family. *Dual-nozzle path present; X2D unconfirmed.*
- **Source.** https://github.com/DMontgomery40/bambu-printer-mcp

### 2e. Shockedrope/bambu-mcp-server
- **What it is.** Minimal MCP server to **monitor** a Bambu printer from Claude Desktop.
- **Transport/protocol.** MQTT.
- **Capabilities.** status ✅ · control ~ (some) · upload ❌ · camera ❌ · slice ❌ — monitoring-first.
- **Maintenance & license.** README built around **P1P**; details **unconfirmed**.
- **X2D / dual-nozzle.** Not addressed → **unconfirmed / likely no**.
- **Source.** https://github.com/Shockedrope/bambu-mcp-server

### 2f. tobiasbischoff/bambu-cli  (a plain CLI, not MCP)
- **What it is.** A command-line tool to drive a Bambu printer over the LAN — the closest match in
  spirit to a scriptable `tools/bambu`.
- **Transport/protocol.** **Go** binary. MQTT (8883) + FTPS (990) + camera stream (port 6000).
  Profiles/config; recommends storing the access code in a file, not on the command line.
- **Capabilities.** status ✅ (`bambu-cli status`) · control ✅ (`bambu-cli print start`, stop) ·
  upload ✅ (FTPS) · camera ✅ · slice ❌.
- **Maintenance & license.** ~27 stars / 4 forks, **8 commits** on master — **small and early**;
  **license not stated in the excerpt fetched → unconfirmed**; last-commit date not shown.
- **X2D / dual-nozzle.** **No X2/dual-nozzle mention → unconfirmed**.
- **Source.** https://github.com/tobiasbischoff/bambu-cli

---

## Slicing options (headless)

### 3a. BambuStudio CLI (`bambu-studio --slice …`)
- **What it is.** Headless slicing built into Bambu's own (open-source) slicer. Lineage:
  BambuStudio is a **fork of PrusaSlicer** (which forks Slic3r), open-sourced by Bambu in late 2022;
  **OrcaSlicer is in turn a fork of BambuStudio** — the three share the libslic3r core and the CLI
  flag set.
- **Transport/protocol.** N/A (local process). Flags: `--slice`, `--load-settings`,
  `--load-filaments`, `--export-3mf`, `--pipe` (live progress), `--allow-newer-file`.
- **Capabilities.** slice ✅ (STL/3MF → G-code/3MF). No printer control/upload/camera.
- **Maintenance & license.** Actively developed by Bambu; slicer core **AGPLv3**. The **network
  plugin** that talks to printers is *proprietary/closed* (hence the open-bamboo-networking
  replacements) — but the *slice-only* path does not need it.
- **X2D / dual-nozzle.** BambuStudio is Bambu's own tool and the natural home for X2D/H2D profiles,
  so it is the **most likely** slicer to carry correct dual-nozzle process/filament presets — but
  I did **not** confirm an X2D preset ships in a specific version; **unconfirmed pending a real
  slice**. Community reference: https://printago.io/blog/bambu-studio-cli-reference ;
  primary: https://github.com/bambulab/BambuStudio
- **Source (CLI flags):** https://printago.io/slicer-cli/bambu

### 3b. OrcaSlicer CLI
- **What it is.** Community slicer (fork of BambuStudio) with the same headless CLI.
- **Transport/protocol.** N/A. Flags mirror BambuStudio: `--slice`, `--load-settings`,
  `--load-filaments`, `--export-3mf`, `--pipe`, plus transforms (arrange/orient/rotate/scale).
  43 keys are deliberately CLI-excluded (credentials, network, indexing).
- **Capabilities.** slice ✅ (G-code + 3MF). No control/upload/camera.
- **Maintenance & license.** Very active OSS, **AGPLv3**.
- **X2D / dual-nozzle.** **Weak and buggy today.** Open issue #11711: new Bambu profiles carry
  *two* value sets (standard + high-flow nozzle); **Orca only shows/edits/saves the standard set**,
  yet slices with the high-flow set when the printer reports a high-flow nozzle → "wrong and/or
  uneditable filament settings." A model *re-slices* onto H2D cleanly, but H2D/dual-nozzle profiles
  may need importing. **Dual-nozzle via Orca CLI: unconfirmed / known-rough.** Carry this hedge —
  it is not "works."
- **Source.** https://www.orcaslicer.com/wiki/cli/cli_mode ,
  https://github.com/OrcaSlicer/OrcaSlicer/discussions/8593 ,
  https://github.com/OrcaSlicer/OrcaSlicer/issues/11711

### 3c. Helio-Additive/slicer-cli  (standalone, packageable)
- **What it is.** A **standalone FDM slicer CLI** derived from BambuStudio *and* OrcaSlicer
  libslic3r forks — ships **separate engine binaries** (`slicer_cli` = BambuStudio,
  `slicer_cli-orcaslicer` = Orca). Aims for **byte-identical G-code** to the desktop apps.
- **Transport/protocol.** N/A. Reads STL/3MF, accepts BambuStudio's printer/filament/process
  profile schema.
- **Capabilities.** slice ✅. No control/upload/camera.
- **Maintenance & license.** **AGPLv3**; CI-built releases for Linux/macOS/Windows (active).
- **X2D / dual-nozzle.** Ships an **`example_benchy_h2d.sh`** — an explicit H2D (dual-nozzle) example,
  the best dual-nozzle-slicing signal among slicers. **X2D not named → likely-via-H2D, unconfirmed.**
- **Source.** https://github.com/Helio-Additive/slicer-cli

### 3d. printago.io  (commercial, hosted)
- **What it is.** A **commercial SaaS "commerce OS for print farms"** that includes cloud slicing
  and farm management. Its `/slicer-cli` pages are **reference docs for the OrcaSlicer (54 flags,
  v2.4.0) and BambuStudio (55 flags, v2.8.0) CLIs** — i.e. documentation of the same open engines
  above, not a separate downloadable CLI product.
- **Transport/protocol.** Hosted service (cloud) wrapping those two CLIs.
- **Capabilities.** slice ✅ (hosted) + farm management. Not a local, allow-listable binary.
- **Maintenance & license.** **Commercial SaaS, free tier ("no credit card")**, engines are the
  underlying OSS/proprietary slicers. Using the *service* means routing models through a vendor cloud.
- **X2D / dual-nozzle.** "Bambu Lab Farms" is a named category; **dual-nozzle not explicitly stated
  → unconfirmed**.
- **Source.** https://printago.io/slicer-cli , https://printago.io/blog/orca-slicer-cli-reference

---

## Library layer (what the MCPs/integrations sit on)

### 4a. greghesp/pybambu
- **What/transport.** Python library, **MQTT**; the engine behind the Home Assistant integration.
- **Capabilities.** status ✅ · control ✅ (subset) · upload ~ · camera ~.
- **Maintenance & license.** Origin project; one snapshot (an older PyPI 0.0.3 note) says it is
  **"currently not up-to-date"** as a *standalone* package — carry that hedge; the *integration*
  it powers is active.
- **X2D / dual-nozzle.** X1C-centric; **dual-nozzle unconfirmed**.
- **Source.** https://github.com/greghesp/pybambu , https://pypi.org/project/pybambu/0.0.3/

### 4b. BambuTools/bambulabs_api  (the de-facto standalone Python lib)
- **What/transport.** Unofficial Python API, **MQTT** + FTP upload + (partial) camera. Python 3.10+.
- **Capabilities.** status ✅ · control ✅ (jobs, light, etc.) · upload ✅ · camera ~ (incomplete on
  some models) · slice ❌.
- **Maintenance & license.** **MIT**, ~326 stars / 61 forks / 318 commits, **actively maintained**,
  passing CI/docs.
- **X2D / dual-nozzle.** README states **X1 "not fully supported yet — camera not implemented"** and
  **H2D "have not been tested yet"**, **no X2 mention**. So the closest dual-nozzle model (H2D) is
  explicitly **untested**. Carry this hedge: *not supported-and-verified for X2D.*
- **Source.** https://github.com/BambuTools/bambulabs_api , https://pypi.org/project/bambulabs-api/

### 4c. greghesp/ha-bambulab (Home Assistant integration)
- **What it proves.** That **local MQTT control works** on real Bambu hardware at scale, and that
  the Jan-2025 auth change **broke** local integrations until Developer Mode / cert workarounds —
  the clearest evidence for what Developer Mode buys us. Bug #1584 documents LAN-Mode install
  friction (carry: LAN-mode setup is fiddly, not turnkey).
- **X2D / dual-nozzle.** Broad model support; **H2D/X2D dual-nozzle status unconfirmed** from the
  material fetched — would need the integration's supported-devices doc/issue tracker.
- **Source.** https://github.com/greghesp/ha-bambulab , https://github.com/greghesp/ha-bambulab/issues/1584

### 4d. Protocol references (not libraries, but the ground truth)
- **Doridian/OpenBambuAPI** — the canonical community MQTT/protocol write-up.
  https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md
- **coelacant1/Bambu-Lab-Cloud-API** — MQTT + cloud analysis; aims to restore local API "without
  developer mode" (compatibility-layer research; **early / in-flux**, README notes a big commit in
  progress). https://github.com/coelacant1/Bambu-Lab-Cloud-API
- **open-bamboo-networking** (ClusterM/carterjones/pallaswept forks) — open replacement for
  BambuStudio's proprietary `bambu_networking` plugin.
  https://github.com/ClusterM/open-bambu-networking/blob/master/NETWORK_PLUGIN.md

### 4e. zhaobenny/bambulab-cloud-py  (cloud, not LAN)
- Unofficial Python client for the **Bambu Cloud** backend (the app's REST API) — relevant only if
  driving *through* the cloud rather than the LAN. Reverse-engineered, auth via Bambu account.
  https://github.com/zhaobenny/bambulab-cloud-py

---

## 5. AppleScript-driven Bambu Studio / Bambu Connect (macOS GUI automation — fallback of last resort)

- **What it is.** Instead of a protocol or a headless CLI, **automate the macOS GUI app**
  (Bambu Studio, and/or Bambu Connect) with **AppleScript / `osascript`** to click through slice
  → dispatch when no headless/API path is good enough. The repo's CLI already carries an
  `applescript.ts` backend for exactly the GUI-only cases, so this is a real, wired-up fallback,
  not a hypothetical.
- **Transport/protocol.** macOS Apple Events. **Crucially — which flavor matters:** an app that
  ships an AppleScript **dictionary (`.sdef`)** can be driven semantically (`tell app … slice`);
  an app that does **not** can only be driven by **UI scripting via System Events / accessibility**
  (clicking coordinates and named UI elements). I found **no evidence that Bambu Studio ships an
  AppleScript dictionary**, and Bambu Studio is a **wxWidgets C++ app of PrusaSlicer lineage**,
  which as a class **do not** ship `.sdef` dictionaries — so this is almost certainly the brittle
  **UI-scripting** flavor. **Unconfirmed** without opening the installed app in Script Editor
  (`View → Application Dictionary`); that check is the one-command way to settle it
  (https://support.apple.com/guide/script-editor/view-an-apps-scripting-dictionary-scpedt1126/mac ,
  https://www.macosxautomation.com/applescript/uiscripting/index.html).
- **Capabilities.** slice ✅ (by driving the GUI) · dispatch/print ✅ · upload ✅ (through the app) ·
  status ~ (only what the GUI shows) · camera ❌ · **structured output ❌** (you read pixels/UI
  state, not JSON).
- **Brittleness (be honest).** Breaks on **app updates and any UI/layout/locale change**; requires
  the app **foregrounded and focused** (steals focus, fights other GUI work); **non-headless**
  (needs a real display / logged-in GUI session — poor fit for CI/servers/`ssh`); **macOS-only**;
  timing-fragile (needs waits/retries around dialogs); accessibility permissions must be granted.
  This is the *least* deterministic and *least* AI-friendly option in the survey.
- **When it is nonetheless the ONLY option.** Where a step is **genuinely GUI-only with no headless
  or protocol equivalent** — most concretely the **Bambu Connect** login/auth and cloud-account
  handshake, and any dispatch/upload that Bambu funnels exclusively through Bambu Connect's UI
  (recall the Jan-2025 auth model puts cert-signed "critical operations" behind Bambu Connect).
  If a firmware/auth change closes the Developer-Mode LAN path on the X2D, GUI automation of Bambu
  Connect may be the *only* remaining way to get a file onto the machine.
- **Load-bearing vs. avoidable (the key call).** For **slicing, AppleScript is avoidable** —
  BambuStudio ships a real headless `--slice` CLI (§3a), so never drive the slicer GUI when the CLI
  will do. AppleScript is **load-bearing only for the Bambu-Connect-GUI-gated auth/dispatch steps**
  that have no headless path. Keep the `applescript.ts` backend scoped to exactly those; do not let
  it creep into slicing or status, which have deterministic alternatives.
- **Maintenance & license.** N/A (it's our own glue over Apple Events); depends on macOS
  `osascript` (stable) but on **each app's UI staying put** (unstable).
- **X2D / dual-nozzle.** Inherits whatever Bambu Studio/Connect themselves support for the X2D —
  so if the GUI can slice/dispatch an X2D dual-nozzle job, this can too. **Unconfirmed**, same as §3a.
- **Source.** https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/AboutScriptingTerminology.html
  , https://www.macosxautomation.com/applescript/uiscripting/index.html (Bambu-specific AppleScript
  support: **none found** — verify locally with Script Editor).

---

## Comparison table

| Option | Kind | Transport | Status | Control | Upload | Camera | Slice | X2D/dual-nozzle | License |
|---|---|---|---|---|---|---|---|---|---|
| griches/bambu-mcp | MCP (TS) | MQTT+FTPS | ✅ | ✅ | ✅ | ✅ | ❌ | H2D tested; X2D unconf. | MIT* |
| synman/bambu-mcp | MCP | MQTT+FTPS | ✅ | ✅ | ✅ | ✅ | ❌ | "X2"/dual mentioned; unconf. | unconf. |
| schwarztim/bambu-mcp | MCP | MQTT+FTPS+X509 | ✅ | ✅ | ✅ | ✅ | ❌ | single-nozzle only listed | unconf. |
| DMontgomery40/bambu-printer-mcp | MCP (TS) | FTPS + BambuStudio CLI | ✅ | ✅ | ✅ | ✅ | ✅ | H2 family listed; X2D unconf. | GPL-2.0 |
| Shockedrope/bambu-mcp-server | MCP | MQTT | ✅ | ~ | ❌ | ❌ | ❌ | unconf. (P1P) | unconf. |
| tobiasbischoff/bambu-cli | CLI (Go) | MQTT+FTPS+cam | ✅ | ✅ | ✅ | ✅ | ❌ | unconf. | unconf. |
| BambuStudio CLI | Slicer | local | ❌ | ❌ | ❌ | ❌ | ✅ | most-likely home for X2D presets; unconf. | AGPLv3 |
| OrcaSlicer CLI | Slicer | local | ❌ | ❌ | ❌ | ❌ | ✅ | dual-nozzle buggy (#11711) | AGPLv3 |
| Helio-Additive/slicer-cli | Slicer | local | ❌ | ❌ | ❌ | ❌ | ✅ | H2D example ships; X2D unconf. | AGPLv3 |
| printago.io | Slicer (SaaS) | cloud | ~ | ~ | ~ | ❌ | ✅ | unconf. | Commercial |
| greghesp/pybambu | Py lib | MQTT | ✅ | ✅ | ~ | ~ | ❌ | unconf. | (repo) |
| BambuTools/bambulabs_api | Py lib | MQTT+FTP | ✅ | ✅ | ✅ | ~ | ❌ | H2D "not tested"; no X2 | MIT |
| ha-bambulab | HA integ. | MQTT | ✅ | ✅ | ~ | ✅ | ❌ | unconf. | (repo) |
| AppleScript GUI automation | GUI glue | Apple Events (UI scripting) | ~ | ✅ | ✅ | ❌ | ✅ (via GUI) | inherits Bambu Studio; unconf. | N/A (our glue) |

`*` griches license/stars read from the fetched README on 2026-09-16; may drift. `~` = partial/model-dependent.

---

## Option rubric (carry this verbatim into the design doc)

Each criterion is stated as a **guiding question**; every option is scored against all of them.
Scores are **Hi / Med / Lo** (or confirmed/unconfirmed/unsupported for X2D). The rubric is the
scoring instrument — the ranking that follows the table is the reading of it.

**Criteria (the questions):**
- **R — Robustness:** *Which is least likely to break on a firmware, app, or cloud change?*
  Ordering principle: **a documented/stable local protocol > a reverse-engineered LAN protocol >
  a reverse-engineered cloud API > GUI-scripting.** (Bambu's LAN protocol is community-RE'd, not
  documented — so nothing here reaches the top tier; Developer-Mode MQTT/FTP is the most stable
  *available* surface because Bambu sanctions the *mode* even while not supporting the *protocol*.)
- **AI — AI/agent-friendliness:** *How cleanly can an agent drive it?* Deterministic text I/O, one
  allow-listable command per action, structured/JSON output, **no GUI focus-stealing, no interactive
  dialogs, headless & scriptable.**
- **OSS — Open-source & self-hostable** (vs. paid/hosted/closed).
- **Local — Local-only vs. cloud-dependent** (privacy, offline, no vendor lock).
- **Headless — CI/server-runnable with no display** (vs. GUI-bound).
- **Maint — Maintenance health & license.**
- **X2D — X2 dual-nozzle support:** confirmed / unconfirmed / unsupported (**the biggest risk**).
- **Slice — Slicing capability** vs. control-only.

| Option | R (robust) | AI-friendly | OSS/self-host | Local vs cloud | Headless | Maint & license | X2D dual-nozzle | Slice |
|---|---|---|---|---|---|---|---|---|
| **BambuStudio CLI** | **Hi** (Bambu's own engine) | **Hi** (one command, files in/out) | Hi (AGPLv3, slice core) | Local | **Hi** | Hi, active | **most-likely / unconf.** | ✅ |
| Helio slicer-cli | Hi | Hi | Hi (AGPLv3) | Local | Hi | Med (small, CI-built) | H2D example / unconf. | ✅ |
| OrcaSlicer CLI | Med-Hi | Hi | Hi (AGPLv3) | Local | Hi | Hi, active | **buggy (#11711) / unconf.** | ✅ |
| griches/bambu-mcp | Med (RE'd LAN MQTT) | Med-Hi (MCP, structured; needs Dev Mode) | Hi (MIT*) | Local (LAN) | Hi | Med, active | H2D tested / unconf. | ❌ |
| synman/bambu-mcp | Med | Med-Hi | Hi? (license unconf.) | Local (LAN) | Hi | Med, active | "X2" mentioned / unconf. | ❌ |
| DMontgomery40/bambu-printer-mcp | Med | Med-Hi (control+slice in one) | Hi (GPL-2.0) | Local (LAN) | Hi | Hi, active | H2 family / unconf. | ✅ |
| schwarztim/bambu-mcp | Med (rides X.509 path) | Med-Hi | Hi? (unconf.) | Local (LAN) | Hi | Med | single-nozzle only | ❌ |
| tobiasbischoff/bambu-cli | Med | **Hi** (plain CLI, allow-listable) | Hi? (license unconf.) | Local (LAN) | Hi | Lo (8 commits, early) | unconf. | ❌ |
| BambuTools/bambulabs_api | Med | Med (Python lib, you write glue) | Hi (MIT) | Local (LAN) | Hi | Hi, active | H2D "not tested" | ❌ |
| ha-bambulab / pybambu | Med | Lo (HA-shaped, not a CLI) | Hi | Local (LAN) | Med | Hi, active | unconf. | ❌ |
| printago.io | Med (vendor cloud) | Med (API, but hosted) | **Lo (commercial)** | **Cloud** | Hi (hosted) | Commercial | unconf. | ✅ |
| bambulab-cloud-py | **Lo** (RE'd cloud API) | Med | Hi | **Cloud** | Hi | Med | unconf. | ❌ |
| **AppleScript GUI automation** | **Lo** (UI-scripting) | **Lo** (focus-stealing, dialogs, pixels) | N/A (our glue) | Local | **Lo (GUI-bound, macOS-only)** | our glue | inherits Studio / unconf. | ✅ (via GUI) |

`*` point-in-time read on 2026-09-16.

**Reading of the rubric:**
- **Most robust:** **BambuStudio CLI** for the *slice* job — it is Bambu's own maintained engine,
  a stable local process, and the natural home for X2D presets; no reverse-engineering, no cloud,
  no GUI. For the *control/upload* job there is **no top-tier-robust option** (all LAN control is
  community-RE'd); the **most robust available control surface is Developer-Mode MQTT+FTPS**, and
  among wrappers **griches/bambu-mcp** (MIT, H2D-tested) is the steadiest.
- **Most AI-friendly:** the **headless slicer CLIs** (BambuStudio / Orca / Helio) — one
  allow-listable command, files in/out, no GUI, no dialogs — tied with **tobiasbischoff/bambu-cli**
  for control (a plain deterministic CLI), ahead of the MCP servers (structured but need an MCP
  client + Developer Mode) and far ahead of **AppleScript (lowest: focus-stealing, dialog-driven,
  non-headless, no structured output).**
- **Least robust / least AI-friendly:** **AppleScript GUI automation** and **cloud-API** paths —
  reserved for what nothing else can do.

**Rubric-scored recommendation:**
- **Most robust AND most AI-friendly path = a two-layer local split:**
  **BambuStudio CLI for slicing** (Hi/Hi/local/headless/OSS) + **Developer-Mode MQTT+FTPS for
  drive/upload**, wrapped by **griches/bambu-mcp** (or a thin direct client / `bambulabs_api`).
  This scores highest on Robustness, AI-friendliness, OSS, Local and Headless simultaneously; its
  only weak cell is the X2D-dual-nozzle *unconfirmed*, which is a validation task, not a design flaw.
- **Strongest alternative = DMontgomery40/bambu-printer-mcp** — one integrated MCP that both drives
  the H2-family printer and wraps BambuStudio to slice. **It wins if** the repo prefers a single
  backend over composing two, and accepts GPL-2.0.
- **AppleScript fallback becomes necessary only when** a step is **GUI-only with no headless or
  protocol equivalent** — concretely, Bambu-Connect-gated auth/dispatch, or if a firmware/auth
  change closes the Developer-Mode LAN path on the X2D. Keep `applescript.ts` scoped to exactly
  those steps; never use it for slicing or status, which have deterministic alternatives.

---

## Gaps & risks

- **X2D dual-nozzle is unconfirmed everywhere.** *No* surveyed tool names the **X2D** explicitly.
  The strongest proxies are tools that name the **H2 series / H2D** (the X2D's dual-nozzle sibling
  sharing firmware `01.02.00.00`): **griches** (H2D tested), **DMontgomery40** (H2, H2S, H2D, H2C
  + `ams_mapping2` handling), and **Helio slicer-cli** (`example_benchy_h2d.sh`). Everything else is
  single-nozzle-verified only. Treat X2D support as *plausible-by-family, not proven* until we
  toggle Developer Mode and actually see MQTT/FTP/camera and a correct dual-nozzle slice.
- **Everything LAN-side depends on toggling LAN Mode + Developer Mode on the X2D touchscreen**,
  which also **severs cloud** while enabled and is **explicitly unsupported by Bambu** (no help if
  it breaks). This matches the current blocker in memory (bambu-x2d-bringup).
- **The Jan-2025 X.509 auth wall** means any path that is *not* Developer Mode (i.e. authenticated
  LAN or cloud) rides on a **community-extracted certificate** that Bambu could rotate/revoke — a
  fragility to design *away* from by using Developer Mode.
- **Dual-nozzle slicing correctness is a live bug in OrcaSlicer** (#11711: standard vs high-flow
  nozzle value sets). BambuStudio (Bambu's own) is the safer bet for X2D presets, but *no version
  was confirmed to ship an X2D profile* — verify by slicing.
- **printago.io is commercial + cloud** — it routes models off-machine and is not an
  allow-listable local binary; it fails the repo's locally-runnable/open-source preference even
  though its free tier works.
- **Unconfirmed specifics** (would need a direct LICENSE/README/API fetch or the printer itself):
  synman & schwarztim & tobiasbischoff licenses and last-commit dates; exact BambuStudio version
  carrying an X2D preset; whether the X2D's Developer-Mode MQTT surface is byte-identical to X1/P1.

---

## Recommendation input (not the decision)

For a repo that wants a **scriptable, allow-listable, locally-runnable, open-source-preferred CLI
with headless slicing**, the shape that fits best is a **two-layer split**, because *no single
option both drives the X2D and slices well while staying open and local*:

- **Drive/transport layer — prefer a thin dependency on the community LAN protocol (MQTT 8883 +
  FTPS 990 + camera), reached either directly or via a small open library.** Among surveyed options,
  **griches/bambu-mcp** (MIT, H2D-tested, the repo the current transport already references) and
  **synman/bambu-mcp** (85 tools, most complete, but license unconfirmed) are the leading MCP
  transports; **tobiasbischoff/bambu-cli** (Go) is the closest to a plain allow-listable binary but
  is small/early with an unconfirmed license. If `tools/bambu` wants a library rather than an MCP,
  **BambuTools/bambulabs_api** (MIT, actively maintained) is the de-facto Python layer — with the
  explicit caveat that **H2D is "not tested"** there, so dual-nozzle must be validated.
- **Slice layer — prefer BambuStudio CLI (AGPLv3), shelled out as one allow-listable command**
  (`bambu-studio --slice --load-settings … --export-3mf …`). It is Bambu's own engine, the most
  likely to carry correct **X2D dual-nozzle** presets, and needs none of the proprietary network
  plugin for slice-only use. **Helio-Additive/slicer-cli** is the strongest *packaging* alternative
  (standalone, byte-identical, ships an H2D example) if a self-contained binary is wanted over a
  full BambuStudio install.

**Why this shape:** it keeps every call a single, allow-listable command against local/open tools;
it avoids printago's cloud/commercial lock-in; and it isolates the one genuinely unproven thing —
X2D dual-nozzle behaviour — into a **validation step** (toggle Developer Mode; confirm MQTT/FTP/
camera on the real X2D; slice a dual-nozzle test and diff the G-code) rather than a design
assumption.

**Strongest alternative, and when it wins:** **DMontgomery40/bambu-printer-mcp** collapses both
layers into one MCP (it drives the printer *and* wraps BambuStudio for slicing, explicitly handles
the H2 family, GPL-2.0). It **wins if** the repo prefers one integrated MCP backend over composing
a transport + a slice shell-out — at the cost of GPL-2.0 (vs MIT/AGPL slice-only) and of inheriting
its opinionated stack. **printago wins only if** hosted, zero-local-install slicing at farm scale is
wanted and cloud routing + a commercial dependency are acceptable — neither of which matches this
repo's stated preferences.

*Final backend choice is the main agent's call; this section only ranks the inputs.*
