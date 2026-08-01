<!--
  Research produced 2026-08-01 by Claude (Opus 5) under the 3d-models
  design-doc rules, for the LDraw half of Lego Lab phase P3.
  Sources: WebFetch and `curl` against tcobbs.github.io, raw.githubusercontent.com,
  leocad.org, trevorsandy.github.io, melkert.net, bricksmith.sourceforge.io,
  ldglite.sourceforge.io, hassings.dk and library.ldraw.org; the GitHub REST API
  via `gh`; read-only inspection of this machine (`uname`, `sw_vers`, `which`,
  `ls /Applications`, `brew search`, `brew info`); and first-hand reading of the
  sample MPD our exporter produced. Full fetch record in §7.
  Feeds: docs/lego-lab-design.md §14.3 — specifically the four unknowns that
  section says "are answered by opening one file in three viewers".
  NOTHING WAS INSTALLED AND NOTHING WAS RUN. Every claim about runtime
  behaviour in this file is derived from documentation or from source code,
  never from observation. §0 states this again and §6 lists it per item.
-->

# LDraw viewers you can drive from a shell on macOS — what exists, what is free, and what would actually open our file

*Research date: 2026-08-01. Scope: how to get a rendered picture, or a
machine-checkable parse, of the MPD that bikar's `--format ldraw` emitter
produces, from a shell on this machine (Apple Silicon, macOS 26.5.1). The
format questions are settled in
[`lego-ldraw-export.md`](lego-ldraw-export.md) and are not re-derived here.*

---

## 0. The standing disclaimer, and the limits on this survey

Three limits apply to **every** sentence below and are not repeated at each claim.

1. **I installed nothing and ran nothing.** No viewer was downloaded, no
   `brew install` was executed, no image was rendered. Every statement about
   what a tool *does* is either (a) quoted from its documentation, (b) read out
   of its source code, or (c) an inference I label as an inference. Where the
   distinction matters — and it usually does — the text says **documented**,
   **source-read**, or **inferred**.
2. **WebSearch was unavailable.** The session's search budget was already
   exhausted (200 of 200) before this research began, exactly as it was for
   [`lego-ldraw-export.md`](lego-ldraw-export.md) §0. So there was **no
   exploratory search at all**. The candidate set below is the list the brief
   named, plus what I could reach by following links and by querying the GitHub
   search API. **K2 — this is a survey of twelve named candidates, not of the
   space of LDraw software.** §3 enumerates the twelve. Nothing here should be
   read as "no LDraw viewer does X".
3. **Documentation written for Windows or Linux does not transfer to macOS by
   itself.** LDView's own help text is written from a Windows point of view
   (*"since LDView is a normal Windows program, and not a console program…"*),
   and its Linux release assets include a dedicated OSMesa (software,
   off-screen) build that the macOS release does not have. Where I claim a flag
   works on macOS, §4.1 gives the macOS-specific source file that implements it.
   Where I cannot, the row says so.

The machine, read directly: `uname -m` → `arm64`; `sw_vers` → macOS 26.5.1
(build 25F80); Homebrew present at `/opt/homebrew/bin/brew`; **no LDraw software
of any kind installed** (`which ldview leocad l3p ldglite blender povray` all
empty, `/Applications` contains none of them); `python3` present via Homebrew;
Node available at `~/.nvm/versions/node/v22.22.3/bin`; **no `cargo`/`rustc`**.

---

## 1. The recommendation, up front

**Install LDView 4.7 and run it as a command-line snapshot tool. It is the only
candidate of the twelve for which I could read, in macOS-specific source code,
a code path that renders to an off-screen buffer and exits without ever
creating a window — and it is also the only one whose search order I could
confirm resolves a type-1 reference against a `0 FILE` block in the same file
*before* touching the disk or the network.**

### 1.1 Install (a human must run this; I did not)

There is **no Homebrew formula or cask for LDView**. `brew search ldview` on
this machine returned only `urlview`, `djview` and `hdfview`. The macOS build
is a disk image from the project's own download page:

```
open https://tcobbs.github.io/ldview/Downloads.html
# download LDView_4.7.dmg  (3,399,129 bytes, published 2026-02-23)
# mount it and drag LDView.app into /Applications
```

### 1.2 The command

```sh
/Applications/LDView.app/Contents/MacOS/LDView \
  "$PWD/Brick-Stack.mpd" \
  -SaveSnapshot="$PWD/Brick-Stack.png" \
  -SaveWidth=1600 -SaveHeight=1200 \
  -SaveZoomToFit=1 -DefaultZoom=0.95 \
  -VerifyLDrawDir=0 \
  -CheckPartTracker=0 \
  -IniFile="$PWD/ldview-run.ini" \
  -v
```

Why each flag, all from LDView's shipped `Help.html`:

| Flag | Documented meaning |
|---|---|
| `-SaveSnapshot=<file>` | *"LDView automatically takes a snapshot of the specified model and outputs to this file."* Extension must be `.png`, `.bmp` or `.jpg`. LDView *"will immediately exit"* afterwards. |
| `-SaveWidth` / `-SaveHeight` | Integers 1–9999, the Save Snapshot dialog's width/height. |
| `-SaveZoomToFit=1` | *"if you use the SaveSnapshot setting and set this setting to 1 on the command line, the resulting image will be zoomed to fit."* |
| `-DefaultZoom=0.95` | *"Setting DefaultZoom to 0.95, for instance, will provide a small margin all the way around the model."* |
| `-VerifyLDrawDir=0` | *"Allows you to run LDView without having LDraw installed, if you want to use it to view LDraw-format models that don't use the LDraw parts library."* **This is the flag that matters most for us**: our MPD references nothing but its own inline block (§2), so the ~80 MB LDraw library is not needed at all. |
| `-CheckPartTracker=0` | Turns off *"Automatically check LDraw.org for missing parts"*, which is on by default. Keeps the run offline and deterministic. Flip it to `1` deliberately when running the §5 experiment for unknown ③. |
| `-IniFile=<path>` | *"have LDView use the specified INI file for its settings … This only works when specified on the command line."* Keeps the run hermetic; on macOS the settings otherwise live in User Defaults. |
| `-v` | *"To show warnings as well as errors, use the -v option."* Errors print by default; `-q` / `-qq` suppress. |

The same binary also exports geometry rather than pixels —
`-ExportFile=out.pov`, `-ExportFile=out.stl`, `-ExportFile=out.3ds` are
documented, and `.pov` feeds Homebrew's `povray` formula (3.7.0.10, AGPL-3.0,
with an `arm64_tahoe` bottle, i.e. a native Apple Silicon binary) if a
publication-quality render is ever wanted.

### 1.3 Verified versus assumed, itemised

**Read out of LDView's own source tree (strongest evidence available without running it):**

- `MacOSX/LDView/main.m` calls `[CommandLineSnapshot takeSnapshot]` **before**
  `NSApplicationMain`, and `return 0`s if it succeeded. The Cocoa application
  object is therefore never started on the snapshot path — no window, no dock
  icon, no run loop.
- `MacOSX/LDView/SnapshotTaker.mm` renders into a **CGL PBuffer**
  (`CGLCreatePBuffer`, pixel format `kCGLPFAPBuffer`) at 1024×1024, or into a
  framebuffer object when `TREGLExtensions::haveFramebufferObjectExtension()`
  is true. On the command-line path `-init` forwards to
  `initWithModelViewer:nil sharedContext:nil`, and the pixel-format chooser is
  called with `remote: sharedContext == nil` — i.e. **true** — which sets
  `kCGLPFARemotePBuffer`. That is Apple's attribute for a renderer with no
  attached display.
- `MacOSX/LDView/Info.plist` sets `CFBundleExecutable` to `LDView`, so the path
  in §1.2 is the right one.
- `LDLoader/LDLModel.cpp::readComment` registers every `0 FILE <name>` block
  into the loaded-models dictionary, and `LDLModel::subModelNamed` looks that
  dictionary up **first**, before `openSubModelNamed` ever touches the disk.
- The change history dates the platform support: **"Mac: Added support for
  Apple Silicon Macs"** in 4.4; **"Mac: Now requires macOS 10.13 (High Sierra)
  or later"** in 4.5; 4.7 (21 Feb 2026) carries *"macOS: Fixed the rendering of
  toolbar buttons to not look weird in macOS 26"*, so the current release is at
  least aware of this OS version.

**Assumed, inferred or untested — and any of these could sink it:**

- **That the CGL pbuffer path still works on macOS 26.5 on Apple Silicon.** CGL
  and OpenGL are long-deprecated Apple APIs. The code exists; whether it
  executes is untested. This is the single biggest risk in the recommendation.
- **That it works with no logged-in GUI session** (e.g. over SSH, or in CI).
  `kCGLPFARemotePBuffer` is the flag for that case, but LDView's own help hedges
  the whole idea: *"if your video card allows this to run without displaying a
  window, you won't have a good way of knowing when LDView has finished
  executing."* **K1 — that hedge is the authors', and it is carried here
  unmodified: LDView does not promise windowless operation, it says it may
  happen.** Assume an interactive desktop session until someone tests otherwise.
- **That `LDView_4.7.dmg` contains an arm64 or universal binary.** The change
  history says Apple Silicon is supported; the download page states no
  architecture; I did not inspect the binary. Check with
  `lipo -archs /Applications/LDView.app/Contents/MacOS/LDView` after installing.
- **Gatekeeper.** A manually downloaded dmg is quarantined. I make no claim
  about LDView's signing or notarisation status. (For contrast, Homebrew has
  *deprecated* both the `leocad` and `bricksmith` casks with the note *"does not
  pass the macOS Gatekeeper check! It will be disabled on 2026-09-01"* — so
  Gatekeeper trouble in this corner of the ecosystem is real and current.)
- Every rendering-quality flag (`-AutoCrop`, `-SaveAlpha`, `-EdgeThickness`,
  `-BFC`) is documented but unexercised.

### 1.4 The second recommendation, which is complementary rather than an alternative

**Also wire up three.js `LDrawLoader` in Node.** It answers a different and
sharper question than a picture does: *did the type-1 line resolve, and how many
triangles came back?* It needs no GUI app, no LDraw parts library, no download
from a third party, and no App Store. It is the route to put in CI.

```sh
export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"
mkdir -p /tmp/ldraw-check && cd /tmp/ldraw-check
npm init -y >/dev/null && npm i three
cat > check.mjs <<'EOF'
import fs from 'node:fs';
import { LDrawLoader } from 'three/examples/jsm/loaders/LDrawLoader.js';

const text = fs.readFileSync(process.argv[2], 'utf8');
const loader = new LDrawLoader();
loader.addDefaultMaterials();          // parse() does NOT do this; load() does
loader.parse(text, (group) => {
  let meshes = 0, tris = 0;
  group.traverse((o) => {
    if (o.isMesh) { meshes++; tris += o.geometry.attributes.position.count / 3; }
  });
  console.log(JSON.stringify({ meshes, triangles: tris }));
}, (e) => { console.error('FAILED', e); process.exit(1); });
EOF
node check.mjs /path/to/Brick-Stack.mpd
```

Expected, if the export is correct: two placements of one 3,764-triangle block.
**That expectation is arithmetic, not an observation** — I have not run this.

The `addDefaultMaterials()` line is not decoration. Reading `LDrawLoader.js`:
`load()` calls it before parsing, but `parse()` does not. Without it the
material library is empty and every face falls back to
`missingColorMaterial` — `0xFF00FF`, magenta. Source-read, untested.

If a **picture** is wanted from this route rather than a count, drive the same
loader inside Chromium through **Playwright, which is already a devDependency of
bikar** (`packages/e2e/package.json`, `"@playwright/test": "^1.44.0"`), and
screenshot the canvas. Headless Chromium supplies WebGL via SwiftShader without
a window server. I did not build or run that harness; it is a described route,
not a tested one.

---

## 2. The file we are actually trying to open

Read first-hand from the emitter's output at
`…/scratchpad/ldraw/Brick-Stack.mpd`, 218,264 bytes:

| Property | Value |
|---|---|
| Line-type histogram | 3,764 × type 3; 20 × type 0; **2 × type 1**; 1 blank |
| Blocks | `0 FILE Stack.ldr` (lines 1–13) and `0 FILE bikar-2x4-3p-76a063bd.dat` (line 15 onward); each closed by `0 NOFILE` |
| The two placements | `1 7 0 -24 0 1 0 0 0 1 0 0 0 1 bikar-2x4-3p-76a063bd.dat` and the same at `y = -48` |
| Header of the part block | `0 !LDRAW_ORG Unofficial_Part` — the S2 form, **not** the `0 UNOFFICIAL PART` form |
| Geometry colour | all 3,764 triangles in colour 16, so the referencing line's `7` wins |
| Absent | any type-2 edge line, any type-4 quad, any `0 BFC` statement, any reference to a library part |

Four consequences that shape everything below.

1. **The file references no LDraw library part at all.** So a viewer that can
   be told not to demand the parts library (LDView's `-VerifyLDrawDir=0`) needs
   no library, and a loader that resolves from an in-memory cache (three.js,
   weldr) never issues a fetch.
2. **The whole payload is type-3 triangles.** A tool that models an LDraw file
   as *a list of placed parts* rather than *a mesh* has nowhere to put them.
   §4.2 shows this is exactly LeoCAD's data model, and it is the reason LeoCAD
   is predicted to render our file as empty.
3. **The reference target is defined in the same file, below the reference.**
   Resolution order is the single behaviour the export depends on.
4. **There are no edge lines**, so any viewer's "edges" rendering will show
   none; a flat-shaded blob is the expected result, not a bug.

---

## 3. Evidence table — the twelve candidates checked

**K2 — this is the enumerated set.** LDView, LeoCAD, LPub3D, LDGLite, L3P
(+ POV-Ray), LDCad, Bricksmith, BrickLink Studio, three.js `LDrawLoader`,
weldr, `ldr_tools_blender` (Blender), and LDraw.org's hosted model-viewer.
Twelve. Found by GitHub search but **not investigated**, and therefore claimed
nothing about: `segfault87/ldraw.rs`, `michaelgale/pyldraw`,
`hbmartin/pyldraw3-tui`.

| # | Tool | Licence / cost | macOS + Apple Silicon | Install route | Runs without a window? | Output | Same-file `0 FILE` resolution? |
|---|---|---|---|---|---|---|---|
| 1 | **LDView 4.7** | Free; source on GitHub (licence file present, text not read) | Apple Silicon support added in **4.4**; 4.5+ needs macOS 10.13+; 4.7 has a macOS 26 fix | **No brew formula/cask.** `LDView_4.7.dmg`, 3,399,129 B, from the project's Downloads page | **Yes on the snapshot path — source-read.** `main.m` returns before `NSApplicationMain`; render is a CGL pbuffer / FBO with `kCGLPFARemotePBuffer`. Help hedges: *"if your video card allows this…"* | PNG / BMP / JPG; also POV / STL / 3DS export; `.ldvz` depth map | **Yes — source-read.** `readComment` registers each `0 FILE` block; `subModelNamed` checks that dictionary before any disk search |
| 2 | **LeoCAD 25.09** | Free, open source | Homebrew cask is **deprecated** (*"does not pass the macOS Gatekeeper check! It will be disabled on 2026-09-01"*) **and Intel-only**: *"leocad is built for Intel macOS and so requires Rosetta 2"*. Official `LeoCAD-macOS-25.09.dmg` (158 MB) exists; its architecture is **not established** — the CI workflow builds macOS with Qt 6.11 on `macos-latest` but has no publish step | `brew install --cask leocad` (deprecated, Intel) or the 158 MB dmg | **No window is shown**, but it is a full `QApplication` even in save-and-exit mode, rendering through `QOpenGLContext` + `QOffscreenSurface`. **Whether it starts with no window server is untested and I doubt it** | GIF/BMP/PNG/JPG via `-i`; OBJ/3DS/DAE/HTML export | **Yes for the *name* — source-read.** Every `0 FILE` block becomes an `lcModel` registered by `CreatePieceInfo`, and `FindPiece` checks that map first. **But see §4.2: the block's contents will be discarded** |
| 3 | **LPub3D** | *"available for free under the GNU Public License version 3.0 (GPLv3)"* | **Yes, explicitly**: downloads listed for *"Ventura 13 (x86_64)"* and *"macOS 14 (arm64)"* | Project download page | Claims *"'Headless' mode on Linux, macOS and Windows platforms"* and *"Console commands - enabling 'Batch' mode"*. **The exact flags for headless were not obtained from any doc page I could fetch** | Instruction-manual images; embeds LeoCAD's visual editor (its arg list carries LeoCAD's `-i -w -h --viewpoint --shading` verbatim) plus `-pf/--process-file`, `-pe/--process-export` | **Not established.** It delegates rendering to LDView / LDGLite / POV-Ray / a native renderer; which one it would use is unexamined |
| 4 | **LDGLite** | Not stated on the page I fetched | Page documents *"Windows, Mac OS X, Linux, DOS, and Mac OS 8-9"* builds; latest macOS is 1.3.1, *"Universal disk image"*, **no date, no architecture given**. Apple Silicon **not established** | SourceForge | Its own page says *"Several internet sites use ldglite as a scripted offscreen renderer, generating many pictures"* — so offscreen scripted use is real, **on unnamed platforms** | Images (flags not documented on that page) | **Not established** |
| 5 | **L3P 1.4 BETA** + POV-Ray | Not stated for L3P; POV-Ray via Homebrew is AGPL-3.0 | **Effectively no.** The only macOS build offered is *"L3P (MacOSX ppc/i386) v1.4 BETA 20080930"* — a 2008 **ppc/i386** binary. This machine is `arm64`. No arm64 or x86_64 macOS build is offered | — | *"A neat little console program"* — genuinely a console tool, on platforms where a binary exists | `.pov` for POV-Ray | **Not established** |
| 6 | **LDCad** | Free ( *"free LDraw editing software"* ) | **No macOS build.** The download page lists Windows (32/64-bit) and *"Linux … only available in the archive variant"*. macOS appears nowhere on it | — | — | — | — |
| 7 | **Bricksmith 3.1** | *"an open-source venture"*; specific licence not stated on the page | **Yes**: *"requires Mac OS X 10.11 or later. Universal binary for Intel and Apple Silicon."* But the Homebrew cask is **deprecated for the same Gatekeeper reason**, disabled 2026-09-01 | `brew install --cask bricksmith` (deprecated) or SourceForge | **No CLI is mentioned anywhere on its site.** GUI editor | — | **Not established** |
| 8 | **BrickLink Studio** | Free (proprietary) | Not re-checked here | GUI installer | No CLI known to this survey | — | **Not established** — unchanged from [`lego-ldraw-export.md`](lego-ldraw-export.md) §3.3 |
| 9 | **three.js `LDrawLoader`** | MIT (three.js) | Pure JS — runs anywhere Node runs, so arm64 is a non-issue | `npm i three` | **Yes, completely** for parsing: no GL context needed by `parse()`. For pixels, Chromium via Playwright (already a bikar devDependency) | A `THREE.Group`; PNG only if you render it | **Yes — source-read, and commented as such.** The loader's own comment: *"This also allows to handle the embedded text files ("0 FILE" lines)"*. `setData()` puts each embedded block in `_cache`; `ensureDataLoaded()` fetches **only** `if ( ! ( key in this._cache ) )` |
| 10 | **weldr** | *"dual licensed … Apache License 2.0 OR MIT"* | Rust; **no `cargo` or `rustc` on this machine**, so a toolchain install comes first | `cargo install` (Rust ≥ 1.61) | **Yes** — a console converter, no GL at all | **glTF 2.0 only.** Not a picture | **Yes — source-read.** `SourceMap::insert` calls `split_mpd_file` with the comment *"The MPD extension allows .ldr or .mpd files to contain multiple files. Add each of these so that they can be resolved by subfile commands later."* |
| 11 | **`ldr_tools_blender`** (Blender) | MIT (repo licence field) | Blender ships arm64 macOS builds; the addon is installed through Blender's UI (*"Do not extract the zip file!"*) | Blender + addon zip | Blender itself has `--background --python`; **the addon documents no command-line usage**, so scripting it is inference | Whatever Blender renders | **Not established.** README says *"LDR and MPD files"* and says nothing about embedded parts |
| 12 | **library.ldraw.org/model-viewer** | Free, hosted by LDraw.org | Browser — any machine | None | n/a — it is a web form | Interactive view in the page | **Yes, and stated as a requirement**: *"All parts used in the file submitted to the model viewer must be embedded in the MPD, be present in the Official Library, or listed on the Parts Tracker."* **But: *"The model submitted here is uploaded to LDraw.org for processing"*** — server-side, third-party upload |

---

## 4. The three candidates worth reading closely

### 4.1 LDView — why the macOS command line is real, and where it stops being certain

The prior research could quote LDView's search order but had to record *"what I
could not learn about LDView: what it does after the parts-tracker download
fails"* ([`lego-ldraw-export.md`](lego-ldraw-export.md) §3.3). Reading the
source moves several of those from unknown to known — and moves one of them out
of relevance entirely.

**Resolution order, from `LDLoader/LDLModel.cpp`.** `readComment` handles
`0 FILE`: when the main model has already been loaded, it creates a new
`LDLModel` for the block and calls `initializeNewSubModel(subModel, filename)`,
keyed by that filename. `subModelNamed` then begins:

```
TCDictionary* subModelDict = getLoadedModels();
…
subModel = (LDLModel*)(subModelDict->objectForKey(dictName));
if (subModel == NULL) { …openSubModelNamed(…)… }
```

The disk search runs **only if the dictionary misses**. So for our file, the
documented four-step search path (model directory, then `P`, `PARTS`, `MODELS`,
then extra dirs) and the parts-tracker download are never reached — the name is
already in memory. **The parts-tracker question is not a question for our
file.** It only becomes one for a *malformed* export whose type-1 name has no
matching block, which is precisely the negative test in §5.

**And when it genuinely cannot find a file**, the Help documents a named error
class rather than a refusal: *"File not found — The model referenced another
model which could not be found in any of the standard search locations (the
current directory; the LDraw model, parts, and p directories; entries in the
extra search directories list)."* It is `LDLError03`, one entry in the Errors &
Warnings window. **That the *rest* of the model still renders is an inference
from the error being per-line and per-file rather than fatal — the Help does not
say so.**

**`0 UNOFFICIAL PART` vs `0 !LDRAW_ORG Unofficial_Part`, from
`LDLoader/LDLCommentLine.cpp`.** `isPartMeta()` returns true for *either* form:
the `!ldraw_org` branch accepts `part`, `unofficial_part`, `shortcut`,
`unofficial_shortcut`; a separate branch accepts a first word of `unofficial`,
`un-official`, `ldraw_org` or `custom` followed by `part` or `element`. A
companion predicate `isOfficialPartMeta()` then separates the two: it accepts
`!ldraw_org part` and bare `ldraw_org`/`official`/`original`, and therefore
classifies **both** of our candidate forms as *unofficial*. **In LDView the two
forms are interchangeable for part recognition.** That is one viewer's answer to
unknown ④, read from its parser — it is emphatically not a statement about the
LDraw standard, which §6 keeps open.

**Where certainty stops.** Everything above is about parsing, which is
platform-independent C++. The *rendering* claim rests on
`MacOSX/LDView/SnapshotTaker.mm`, and that file uses CGL pbuffers — an API Apple
deprecated years ago along with OpenGL itself. **The code is there; whether it
runs on macOS 26.5 is untested and is the recommendation's main risk.**

### 4.2 LeoCAD — it will resolve the name and then throw the geometry away

This is the finding most worth acting on, and it is a prediction, not an
observation.

LeoCAD models an LDraw file as *a list of placed pieces*, not as a mesh. In
`common/lc_model.cpp::LoadLDraw`, the token dispatch has a branch for `0`, a
branch for `1`, and then:

```cpp
else
{
    ReadingHeader = false;
    mFileLines.append(OriginalLine);
}
```

**Type 2, 3, 4 and 5 lines all land in that `else`.** `mFileLines` is used in
exactly one place — the *save* path, which writes the stored lines back out
verbatim. No geometry is constructed from them anywhere in `lcModel`.

Meanwhile the name resolves perfectly well. `Project::Load` runs
`Model->SplitMPD(Buffer)` in a loop, creating one `lcModel` per `0 FILE` block
and calling `Model->CreatePieceInfo(this)`, which registers each block in the
piece library under its upper-cased filename. `lcPiecesLibrary::FindPiece` then
checks that map first, the project's own directory second, and only then
manufactures a placeholder.

So the predicted behaviour on our file is: **the two type-1 lines resolve to a
submodel that contains zero pieces, and LeoCAD shows an empty model** — no
error, no placeholder, no warning, because from LeoCAD's point of view the
reference resolved fine. **This is the "export that succeeds and produces the
wrong thing" failure class the design doc names, arriving from a direction the
doc did not anticipate.** If it holds, it is a much more important finding than
any command line in this file, and §14.3's sentence *"all four are answered by
opening one file in three viewers"* would need a fifth line: *a viewer may
accept the file and render nothing.*

**Confidence, stated honestly.** The `else`-branch reading is unambiguous and I
am confident about it. What I have *not* checked is whether some other code path
(a preview renderer, the POV-Ray export path, `lcSynthInfo`, or the `IsPrimitive`
branch just above) reconstitutes those lines. Only running it settles it, and
that is §5's experiment ①.

Two further LeoCAD facts, both bearing on whether it is even installable here:

- The Homebrew cask says *"leocad is built for Intel macOS and so requires
  Rosetta 2 to be installed"*, is **deprecated for failing the Gatekeeper
  check**, and **will be disabled on 2026-09-01** — a month from this file's
  date.
- The official `LeoCAD-macOS-25.09.dmg` (158 MB, 2025-09-02) and a `continuous`
  build dated 2026-08-01 both exist. The repo's only workflow builds macOS with
  Qt 6.11 on `macos-latest` but contains no upload step, so **I could not
  establish the released dmg's architecture from CI configuration.**
- The bundle's executable name *is* established: `leocad.pro` reads
  `unix:!macx { TARGET = leocad } else { TARGET = LeoCAD }`, so the path is
  `/Applications/LeoCAD.app/Contents/MacOS/LeoCAD`.

The invocation, from LeoCAD's man page (`docs/leocad.1`, dated 1 September 2025):

```sh
/Applications/LeoCAD.app/Contents/MacOS/LeoCAD "$PWD/Brick-Stack.mpd" \
  -i "$PWD/Brick-Stack-leocad.png" -w 1600 -h 1200 \
  --viewpoint home --shading full
```

`-i`/`--image` is documented as *"Saves a picture to outfile.ext … and exits"*,
formats `gif, bmp, png or jpg`. `-l`/`--libpath` and `LEOCAD_LIB` set the parts
library. **The man page says nothing about whether rendering needs a display**;
`common/lc_application.cpp` constructs a `QApplication` (not a
`QCoreApplication`) on every path and `lc_context.cpp` builds a
`QOpenGLContext` + `QOffscreenSurface`, so *no window is shown* but a Qt GUI
platform plugin is still initialised. **Inference: on macOS that means the
`cocoa` plugin and a window server. Untested.**

### 4.3 three.js `LDrawLoader` — the route with no app to install

`LDrawLoader.js` carries the behaviour our export needs, and says so in a
comment on the field that implements it: `this.partsCache = new
LDrawPartsGeometryCache(this); // This also allows to handle the embedded text
files ("0 FILE" lines)`.

The mechanism, source-read:

- During `parse()`, a `0 FILE` line at any index past the first flips
  `parsingEmbeddedFiles = true`; subsequent lines accumulate into
  `currentEmbeddedText` and are committed with
  `this.setData( currentEmbeddedFileName, currentEmbeddedText )` at the next
  `0 FILE` or at end of input.
- `setData` writes `this._cache[ fileName.toLowerCase() ]`.
- `ensureDataLoaded` fetches **only** when `! ( key in this._cache )`.

Hence: **the inline block is in the cache before any subobject is resolved, so
no network access happens and no parts library is required.** Matching is
case-insensitive. `0 NOFILE` is not handled specially; it would be swept into
the embedded text and parsed as a comment there — **inferred from the parser's
shape, not stated anywhere.**

On unknown ④, three.js gives the *opposite* answer to LDView, which is why the
question stays open in §6. `isPartType( type )` is
`type === 'Part' || type === 'Unofficial_Part'`, and `type` is only ever set
from a `!LDRAW_ORG` meta. **`0 UNOFFICIAL PART` would not be recognised at all
by this loader.** Our file writes `0 !LDRAW_ORG Unofficial_Part`, which is the
form three.js accepts — so the emitter's existing choice is the safer one across
these two readers. That is a two-implementation observation, not a rule.

---

## 5. Which of §14.3's four unknowns each candidate could answer

§14.3 lists four unknowns and asserts *"All four are answered by opening one
file in three viewers … no coupon, no calipers, one afternoon."* Against the
evidence above, that is **nearly right, with two corrections**: reading source
code has already answered parts of ①, ③ and ④ without opening anything, and no
single viewer answers ②.

| Unknown (§14.3) | Answerable by | Status after this research |
|---|---|---|
| ① What LeoCAD does with an unresolvable type-1 reference, and whether it resolves names against same-file `0 FILE` blocks | **LeoCAD only.** No substitute | **Half-answered by source.** It *does* resolve against same-file blocks (`CreatePieceInfo` → `FindPiece`), and an unresolvable name yields a **placeholder** piece (`CreatePlaceholder`), not an error. The *new* and more urgent question is §4.2's prediction that the resolved block renders as **nothing**. Still needs the run |
| ② What BrickLink Studio does with an inline-defined part, on import and on round-trip | **Studio only.** No substitute — it maps LDraw parts onto its own catalogue, so no other tool's behaviour predicts it | **Unchanged. Fully open.** Nothing in this survey touches it |
| ③ What LDView does after its parts-tracker download attempt fails | **LDView** — but see right | **Largely dissolved for our file.** Source shows the same-file dictionary is consulted before any disk or network lookup, so for a *well-formed* export the tracker is never reached. The question survives only for a malformed export, and there the documented outcome is the `File not found` error class (`LDLError03`), with "does the rest still render" an untested inference |
| ④ Whether `0 UNOFFICIAL PART` and `0 !LDRAW_ORG Unofficial_Part` are interchangeable | **Any parser** — and different parsers disagree | **Answered per-implementation, still open as a standards question.** LDView's `isPartMeta()` accepts **both**; three.js's `isPartType()` accepts **only** the `!LDRAW_ORG` form. So they are *not* interchangeable across readers. No specification reconciling them was found — see [`lego-ldraw-export.md`](lego-ldraw-export.md) §8 item 4, which remains correct |

**The experiment set, minimal version.** Two files, three commands:

```sh
# A: the real export, as shipped
/Applications/LDView.app/Contents/MacOS/LDView "$PWD/Brick-Stack.mpd" \
  -SaveSnapshot="$PWD/A-ldview.png" -SaveWidth=1600 -SaveHeight=1200 \
  -SaveZoomToFit=1 -VerifyLDrawDir=0 -CheckPartTracker=0 -v

# B: a variant whose type-1 line names bikar-nonexistent.dat, with the
#    inline block left in place under its real name — tracker ON, then OFF
/Applications/LDView.app/Contents/MacOS/LDView "$PWD/Broken.mpd" \
  -SaveSnapshot="$PWD/B-tracker-on.png" -VerifyLDrawDir=0 -CheckPartTracker=1 -v
/Applications/LDView.app/Contents/MacOS/LDView "$PWD/Broken.mpd" \
  -SaveSnapshot="$PWD/B-tracker-off.png" -VerifyLDrawDir=0 -CheckPartTracker=0 -v

# and the same file A through LeoCAD, which is where the interesting failure is
/Applications/LeoCAD.app/Contents/MacOS/LeoCAD "$PWD/Brick-Stack.mpd" \
  -i "$PWD/A-leocad.png" -w 1600 -h 1200 --viewpoint home --shading full
```

Record for each: exit status, everything on stdout/stderr, whether a PNG
appeared, and **whether the PNG contains two bricks, one brick, or nothing**.
The last column is the one that matters and it is the one no amount of reading
can supply.

---

## 6. What could not be grounded

Each item names the experiment that would settle it. All of these are *open*;
none is a hedge on something I actually know.

1. **UNGROUNDED — untested. Whether LDView's macOS command-line snapshot path
   executes at all on macOS 26.5 / Apple Silicon.** The code path is read and
   understood (`main.m` → `CommandLineSnapshot` → CGL pbuffer / FBO), but CGL
   and OpenGL are deprecated Apple APIs and this machine has never run LDView.
   *Experiment:* install `LDView_4.7.dmg`, run §1.2, and record exit status,
   whether a PNG appeared, and whether anything flashed on screen. Also run
   `lipo -archs` on the binary to settle the architecture question, and try it
   once over SSH with no GUI session to settle the headless question. **Until
   this is done the recommendation in §1 is a reading, not a result.**

2. **UNGROUNDED — untested, and the highest-value item here. Whether LeoCAD
   renders our file as empty.** §4.2 predicts it does, from the `else` branch
   that routes type-3 lines into a save-only buffer. Not checked: whether any
   other LeoCAD code path consumes `mFileLines`. *Experiment:* the LeoCAD
   command in §5 against the real export. A blank or near-blank PNG with exit
   status 0 confirms the prediction — and would mean the export is silently
   useless in LeoCAD specifically.

3. **UNGROUNDED — not established. The architecture of the released
   `LeoCAD-macOS-25.09.dmg`.** Homebrew's cask is Intel-only and deprecated with
   a hard disable date of 2026-09-01; the official dmg's architecture is not
   stated anywhere I fetched, and the repo's only CI workflow has no publish
   step. *Experiment:* download the dmg and run `lipo -archs` on the bundle
   executable. If it is Intel-only, LeoCAD on this machine needs Rosetta 2 and
   experiment ② needs that installed first.

4. **UNGROUNDED — not fetched. LPub3D's actual headless flags.** Its home page
   claims *"'Headless' mode on Linux, macOS and Windows platforms"* and its
   argument list (read from `mainApp/commandline.cpp`) contains `-pf`,
   `-pe`, and LeoCAD's whole rendering flag set — but **no documentation page I
   could reach states the headless invocation**, and the SourceForge wiki
   returned only the same marketing sentence. *Experiment:* install the macOS 14
   arm64 build and run `lpub3d --help`, or read `mainApp/application.cpp`'s
   console-redirect logic. Worth doing only if LDView fails, since LPub3D is an
   instruction-manual generator and would be delegating to a renderer anyway.

5. **UNGROUNDED — not established. LDGLite's macOS architecture, release date
   and command-line flags.** Its own page says *"Several internet sites use
   ldglite as a scripted offscreen renderer"* — which is the most promising
   sentence in this whole survey for a genuinely headless tool — but names no
   platform for that use, gives no date for the 1.3.1 macOS *"Universal disk
   image"*, and documents no flags. *Experiment:* fetch the SourceForge file
   listing for dates and the source tree for the argument parser. **This one
   deserves a look before the next viewer is chosen**; I could not reach it
   because WebSearch was exhausted.

6. **UNGROUNDED — untested. Whether the three.js snippet in §1.4 runs.** The
   `parse()` / `addDefaultMaterials()` asymmetry, the embedded-file cache, and
   the `key in this._cache` short-circuit are all read directly from
   `LDrawLoader.js`, but the script has never been executed and `three` is not
   installed here. *Experiment:* run it. If it prints
   `{"meshes":…,"triangles":3764}` against a two-placement file, the exporter's
   central assumption is confirmed by an independent implementation, in CI, with
   no GUI.

7. **UNGROUNDED — untested. Whether Playwright can screenshot the loaded
   model.** Chromium's software WebGL is real, and `@playwright/test` is already
   a bikar devDependency, but no harness was written. *Experiment:* build the
   smallest page that imports three.js from `node_modules`, loads the MPD text,
   and screenshots the canvas.

8. **UNGROUNDED — no source found. Whether `0 UNOFFICIAL PART` and
   `0 !LDRAW_ORG Unofficial_Part` are interchangeable *as a matter of the LDraw
   standard*.** Two implementations now disagree (§4.3), which strengthens the
   case that the question is real, and settles nothing about the spec.
   [`lego-ldraw-export.md`](lego-ldraw-export.md) §8 item 4 names the source
   that would settle it — the LDraw Standards Board's revision history for the
   header specification — and it was not fetched here either.

9. **UNGROUNDED — not attempted. BrickLink Studio.** Unknown ② is untouched by
   this survey and no other tool substitutes for it.

10. **Bounded, not exhaustive: the candidate set.** Twelve tools, enumerated at
    the head of §3, chosen from the brief plus link-following plus GitHub search,
    with **no exploratory web search performed at all**. Three further LDraw
    libraries were found by repository search and not investigated
    (`segfault87/ldraw.rs`, `michaelgale/pyldraw`, `hbmartin/pyldraw3-tui`).
    **No sentence in this file supports a claim of the form "no LDraw viewer
    does X".**

11. **Bounded: what "documented" means per tool.** Of the twelve, I read
    *source code* for four (LDView, LeoCAD, three.js, weldr), a *man page* for
    one (LeoCAD), a shipped *help file* for one (LDView), an *argument list in
    source* for one (LPub3D), and **only a marketing or download page** for the
    rest. The evidence in the §3 table is not of uniform strength and the
    "Same-file `0 FILE` resolution?" column says which kind each row is.

12. **Not verified: the third-party upload path.** LDraw.org's hosted
    model-viewer is the only candidate that explicitly documents the
    embedded-in-MPD case as supported — *"All parts used in the file submitted
    to the model viewer must be embedded in the MPD…"* — and it is also the only
    one that requires **sending our geometry to someone else's server**
    (*"uploaded to LDraw.org for processing but is not permanently stored"*).
    It should not be used as the routine check. It is, however, a legitimate
    one-off tiebreaker if every local route fails, **provided a human decides
    the upload is acceptable.**

---

## 7. Fetch record — every URL retrieved, and every retrieval that failed

Retrieved by WebFetch unless marked. `curl` was used only to pull a
documentation file into the scratchpad so it could be read in full locally;
nothing was installed and nothing was executed.

| # | Source | URL | How |
|---|---|---|---|
| V1 | LDView home page | https://tcobbs.github.io/ldview/ | WebFetch (returned no download or CLI detail) |
| V2 | LDView Downloads | https://tcobbs.github.io/ldview/Downloads.html | WebFetch |
| V3 | LDView `Help.html` (shipped help, read in full) | https://raw.githubusercontent.com/tcobbs/ldview/master/Help.html | `curl` → scratchpad, parsed locally |
| V4 | LDView `ChangeHistory.html` | https://raw.githubusercontent.com/tcobbs/ldview/master/ChangeHistory.html | `curl` → scratchpad |
| V5 | LDView `MacOSX/LDView/main.m` | https://raw.githubusercontent.com/tcobbs/ldview/master/MacOSX/LDView/main.m | `curl` |
| V6 | LDView `MacOSX/LDView/CommandLineSnapshot.mm` | https://raw.githubusercontent.com/tcobbs/ldview/master/MacOSX/LDView/CommandLineSnapshot.mm | `curl` |
| V7 | LDView `MacOSX/LDView/SnapshotTaker.mm` | https://raw.githubusercontent.com/tcobbs/ldview/master/MacOSX/LDView/SnapshotTaker.mm | `curl` |
| V8 | LDView `MacOSX/LDView/Info.plist` | https://raw.githubusercontent.com/tcobbs/ldview/master/MacOSX/LDView/Info.plist | `curl` |
| V9 | LDView `LDLoader/LDLModel.cpp` | https://raw.githubusercontent.com/tcobbs/ldview/master/LDLoader/LDLModel.cpp | `curl` |
| V10 | LDView `LDLoader/LDLCommentLine.cpp` | https://raw.githubusercontent.com/tcobbs/ldview/master/LDLoader/LDLCommentLine.cpp | `curl` |
| V11 | LDView `LDLib/LDSnapshotTaker.cpp` | https://raw.githubusercontent.com/tcobbs/ldview/master/LDLib/LDSnapshotTaker.cpp | `curl` |
| V12 | LDView releases + repo tree (asset names, sizes, dates) | `gh api repos/tcobbs/ldview/releases`, `gh api repos/tcobbs/ldview/contents[/MacOSX…]` | GitHub REST via `gh` |
| V13 | LeoCAD man page `docs/leocad.1` | https://raw.githubusercontent.com/leozide/leocad/master/docs/leocad.1 | `curl` |
| V14 | LeoCAD `common/lc_model.cpp` | https://raw.githubusercontent.com/leozide/leocad/master/common/lc_model.cpp | `curl` |
| V15 | LeoCAD `common/project.cpp` | https://raw.githubusercontent.com/leozide/leocad/master/common/project.cpp | `curl` |
| V16 | LeoCAD `common/lc_library.cpp` | https://raw.githubusercontent.com/leozide/leocad/master/common/lc_library.cpp | `curl` |
| V17 | LeoCAD `common/lc_library.h`, `common/pieceinf.h` | https://raw.githubusercontent.com/leozide/leocad/master/common/lc_library.h | `curl` |
| V18 | LeoCAD `common/lc_context.cpp` | https://raw.githubusercontent.com/leozide/leocad/master/common/lc_context.cpp | `curl` |
| V19 | LeoCAD `common/lc_application.cpp`, `qt/qtmain.cpp` | https://raw.githubusercontent.com/leozide/leocad/master/common/lc_application.cpp | `curl` |
| V20 | LeoCAD `leocad.pro` (bundle target name) | https://raw.githubusercontent.com/leozide/leocad/master/leocad.pro | `curl` |
| V21 | LeoCAD CI workflow | https://raw.githubusercontent.com/leozide/leocad/master/.github/workflows/continuous.yml | `curl` |
| V22 | LeoCAD releases + repo tree | `gh api repos/leozide/leocad/releases`, `…/contents/docs` | GitHub REST via `gh` |
| V23 | LPub3D project site | https://trevorsandy.github.io/lpub3d/ | WebFetch |
| V24 | LPub3D `mainApp/commandline.cpp` | https://raw.githubusercontent.com/trevorsandy/lpub3d/master/mainApp/commandline.cpp | `curl` |
| V25 | LPub3D `mainApp/lpub.cpp` | https://raw.githubusercontent.com/trevorsandy/lpub3d/master/mainApp/lpub.cpp | `curl` |
| V26 | LDCad downloads | http://www.melkert.net/LDCad/Download | WebFetch |
| V27 | Bricksmith home | https://bricksmith.sourceforge.io/ | WebFetch |
| V28 | LDGLite home | https://ldglite.sourceforge.io/ | WebFetch (after a 301 from `.net`) |
| V29 | L3P home | http://www.hassings.dk/l3/l3p.html | WebFetch |
| V30 | three.js `LDrawLoader.js` | https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/jsm/loaders/LDrawLoader.js | `curl` → scratchpad, read in full |
| V31 | weldr README | https://raw.githubusercontent.com/djeedai/weldr/main/README.md | WebFetch |
| V32 | weldr `lib/src/lib.rs` | https://raw.githubusercontent.com/djeedai/weldr/main/lib/src/lib.rs | `curl` |
| V33 | weldr `lib/src/parse.rs` | https://raw.githubusercontent.com/djeedai/weldr/main/lib/src/parse.rs | `curl` |
| V34 | `ldr_tools_blender` README | https://raw.githubusercontent.com/ScanMountGoat/ldr_tools_blender/main/README.md | WebFetch |
| V35 | LDraw.org hosted model viewer | https://library.ldraw.org/model-viewer | WebFetch |
| V36 | GitHub repository search (ldglite, weldr, ldr-tools, pyldraw, ldraw-rs) | `gh api search/repositories?q=…` | GitHub REST via `gh` |
| V37 | This machine | `uname -m`, `sw_vers`, `ls /Applications`, `which …`, `brew search …`, `brew info leocad/bricksmith/povray`, `brew info --json=v2 povray` | local, read-only |
| V38 | The sample export itself | `…/scratchpad/ldraw/Brick-Stack.mpd` | read on disk |
| V39 | bikar worktree (Playwright devDependency) | `bikar-lego-lab/packages/e2e/package.json` | read on disk |
| V40 | Prior LDraw research in this repo | [`lego-ldraw-export.md`](lego-ldraw-export.md) | read on disk |

**Retrieval failures, disclosed:**

- **WebSearch: budget exhausted (200/200) before this research started.** No
  exploratory search was performed. This is the binding constraint on §3's
  completeness and item 10 of §6 records it.
- `https://www.leocad.org/docs/commandline.html` — **404**.
  `https://www.leocad.org/docs/` — **404**. LeoCAD's command line is documented
  here from `docs/leocad.1` in the source repo instead, which is the man page
  the project ships.
- `https://github.com/leozide/leocad/blob/master/docs/CHANGELOG.md` — **404**
  (no such file; the repo's `docs/` holds `COPYING.txt`, `CREDITS.txt`,
  `README.md`, `leocad.1`).
- `https://www.ldraw.org/help/tools-and-software.html` and
  `https://www.ldraw.org/help/tools-and-software/os-x.html` — both **404**. I
  could not obtain LDraw.org's own catalogue of macOS tools, which would have
  been the natural way to widen the candidate set. This is a real gap.
- `https://api.github.com/repos/tcobbs/ldview/releases/latest` via WebFetch —
  **403**. Re-run through `gh`, which succeeded.
- `http://www.melkert.net/LDCad` and `http://www.melkert.net/LDCad/requirements`
  — fetched but returned no platform or requirements detail; the platform claim
  in §3 comes from `/Download`, which did.
- `https://raw.githubusercontent.com/trevorsandy/lpub3d/master/README.md` and
  `https://sourceforge.net/p/lpub3d/wiki/Home/` — both fetched, **neither
  contains the command-line reference**; only the two marketing sentences quoted
  in §3.
- `https://ldglite.sourceforge.io/` — fetched, but documents **no command-line
  flags and no dates**.
- The first pass at `Help.html` through WebFetch returned a **truncated**
  document that cut off before the Command Line section entirely. Every LDView
  quotation in this file comes from the `curl`-retrieved copy read locally, not
  from that truncated pass.
