# Orb Lab P2 — Custom Orbs + Studio Dials: Validation Plan & Design

Status: **DRAFT for review — P2 planning (P0/P1 shipped)**
Provenance: drafted by a planning subagent from the shipped P0/P1 code (2026-07-27); adopted as the P2 working plan.
Scope: `f=custom` code editing in the Lab with lz-string URLs and author-declared knobs; worker hardening against pathological scripts; the bikar studio **Dials** tab; the shared knob layer's new home; test plan and milestone slicing.
Companion: `docs/orb-lab-design.md` (§10 P2 line item; §6.3 custom URLs; §7 knobs⇄code; §8 studio tab). All file references verified against the working trees at `~/Workspace/git/bikar` and `~/Workspace/git/qiyas` (2026-07-27).

**Engine-change-free phase.** Everything P2 needs from the engine already exists and is public: `parse(source, options?)` (param extraction without evaluation, `packages/core/src/dsl/index.ts`), `compileToGeometry(source, { params })` (override entry point, `packages/core/src/index.ts:45`), `ParamSpec` on `EvaluationResult.params`, and the hard-error contract for out-of-range overrides (`parser.ts:528/658/665` — unknown name, non-finite, out-of-range are all `ParseError`s with author-facing messages; **the engine never clamps, by design**). P2 touches only `packages/lab`, `packages/web`, one new workspace package, and tests.

**Dependency check (constraint verification).** The design doc does list lz-string: §6.3 names "`lz-string compressToEncodedURIComponent` of the full `.bkr` source" and Appendix A cites the TypeScript-Playground precedent. It is **not yet installed** — `packages/lab/package.json` has only `@naqshcoffee/bikar-core`. P2 adds `lz-string` exactly once, in the shared knob package (§3), as the sole new runtime dependency.

---

## 1. Validation plan — custom scripts as untrusted input

### 1.1 Threat model, stated precisely

Everything runs client-side in the visitor's own browser. The `.bkr` DSL has no `eval`, no I/O, no recursion, and no unbounded loops (`for` ranges and `repeat` depths are literal constants after param substitution), so **every script terminates — but with unbounded cost**. The realistic threats are:

1. **Self-DoS** — CPU-hour evaluations and worker OOM from pathological geometry (assessed in §1.3).
2. **Broken shares** — truncated/corrupted `code=` payloads producing confusing failures (lz-string output is not checksummed).
3. **Markup injection** — the one real XSS surface: `main.ts:209` injects engine-rendered axis-view SVG via `axisViewEl.innerHTML = view.svg`, and with custom orbs that SVG derives from untrusted source. **Verified mitigated by construction**: every DSL-sourced string that can reach SVG attributes is an identifier lexed as `[a-zA-Z_][a-zA-Z0-9_]*` (`lexer.ts:30-31`), and colors are preprocessed hex literals. Residual action (cheap, do it in P2.2): a one-time audit of `render/svg-utils.ts` attribute escaping plus a unit test asserting `renderOrbViewSVG` output for a hostile-named pattern contains no unescaped `<`/`"` from user strings. Everything else user-controlled already goes through `textContent`/`.value` (verified in `lab/src/main.ts` and `knobs.ts`).

There is no server, no cookies of value, no cross-user state: the security bar is "the page cannot be made to execute injected markup, and cannot be wedged so badly the visitor blames us."

### 1.2 The validation layers

Order below is the order a payload traverses them. "User sees" is normative copy direction, not final strings.

| # | Layer | Checks | Runs | On failure, user sees |
|---|---|---|---|---|
| **L1** | **URL decode** (`code=`) | (a) `f=custom` present — `code=` is ignored with a toast if `f` names a preset; (b) `decompressFromEncodedURIComponent` returns non-null/non-empty; (c) decompressed text begins with the sentinel `bkr1\n` (§2.5) — detects truncation/corruption, which lz-string itself cannot; (d) decompressed length ≤ 64 KB (decompression-bomb cap: 1,800 URL chars can legally expand to megabytes of repetitive text) | main thread, boot (`url-state.ts` successor) | Toast: "This share link is damaged — it may have been truncated by a chat app. Ask the sender for the .bkr file instead." Lab loads the default preset; **no partial source is ever placed in the editor** (garbage that happens to decompress must not masquerade as the author's work) |
| **L2** | **Script size cap** | Source ≤ 64 KB. Enforced three times (defense in depth, all trivial): editor `maxlength`, L1(d) above, and a worker-side refusal before parse | editor (main), decode (main), worker | Inline editor notice: "Scripts are capped at 64 KB (yours: N KB)"; worker path returns a normal `error` response |
| **L3** | **Static budget sniff** | Regex over source text (no engine needed on main thread) for heavy constructs: `subdivide [34]`, `girih field`, `shells \d`, `repeat .* depth [3-9]`, `divide .* into \d{3,}`, `tile grid`. Selects the watchdog budget tier (§1.4): default 15 s → heavy 60 s. **Advisory, never a block** — presets legitimately use `subdivide` | main thread, before each evaluate | Nothing on the happy path; heavy tier shows "this design is large — computing may take up to a minute" beside the spinner |
| **L4** | **Parse / eval errors** | `LexerError` / `ParseError` / `EvalError` from `compileToGeometry` — includes the L5 engine cases and all §5-tier-2 geometry errors (inset degeneracy, manifold gate, weave contract) | worker (`worker.ts` catch already returns `e.message`, never a stack — keep exactly this) | The engine's message **verbatim** in the error panel; **last-good mesh, knob panel, and gate readout stay on screen** (P0's seq/`applyResult` machinery already guarantees this); STL disabled |
| **L5** | **Param-range enforcement** | Two halves. *Engine (unchanged, by design)*: default outside its own range, empty range, unknown/non-finite/out-of-range override → hard `ParseError` (`parser.ts:614/633/528/658/665`). *Lab reconcile (new)*: before evaluating custom source with overrides, the worker parses the header, then **drops unknown names and clamps out-of-range overrides against the freshly parsed specs, reporting every adjustment** (§1.5). This is the only way a code edit that shrinks a range can't strand a previously-touched knob into a guaranteed engine error | engine (in worker); reconcile in worker | Engine errors verbatim (an author who types `param inner = 90 range 16..58` gets the engine's own sentence). Reconcile adjustments surface as the existing "Adjusted N parameters" toast + knob sync — the Lab clamps, loudly; the engine never clamps |
| **L6** | **Cross-param UI clamps** | Existing tier-1 rules (`constraints.ts`): `inner ≤ shoulder − 8`, `amplitude ≥ (strut_depth + 0.4)/2`, applied by param **name convention** — they fire for custom scripts too iff the script declares those names (documented in the authoring help; a custom script using different names opts out and relies on L4/L7) | main thread knob layer (moves to shared package, §3) | Knob snaps + toast, as shipped in P0 |
| **L7** | **meshGate print-readiness** | Existing tier-3: watertight, min feature ≥ 1.2 mm floor, degenerate triangles; STL button gated on pass | worker, after every successful evaluate | The shipped gate panel; FAIL rows listed; STL disabled |
| **L8** | **Watchdog: timeout / OOM / crash** | Deadline per evaluate (tier from L3); worker `error`/`messageerror` events (worker-heap OOM in Chromium fires `error`); user **Stop** button | main thread (`WorkerHost`, §1.4) | "Evaluation exceeded 15 s and was stopped — reduce `subdivide`, `shells`, or repeat depth, or download the .bkr and render with the CLI." UI stays fully live; last-good preview retained |

Two invariants across all layers, restated because they are the project's stated conventions:

- **Engine hard errors surface verbatim, never stack traces.** The worker's existing `e instanceof Error ? e.message : String(e)` is the whole policy; no rewriting, no "friendly" paraphrase layered on top.
- **The engine never silently clamps.** All clamping is Lab-side (L5-reconcile, L6, URL `clampToSpecs`) and always announced via the adjustments toast.

### 1.3 CPU-bomb risk assessment (measured/derived)

`compileToGeometry` runs in the worker with **no yield points** — once evaluation starts, the worker cannot observe messages, so no cooperative cancellation is possible; `worker.terminate()` from the main thread is the only kill switch. Concrete bombs reachable from ~20 lines of legal DSL:

- **Subdivision × density.** Star×icosa `subdivide 2` measures 20,160 tris (design doc Appendix B); tris scale ×~4/level → `subdivide 4` ≈ 320k tris on the same pattern, before the author also densifies the face pattern (`rotate 10`, hankin, nested motifs). Tens of seconds to minutes.
- **Quadratic intersection.** `divide C0 into 5000` + `connect every k` feeds face extraction an O(E²)-flavored planar-subdivision problem — minutes, and the intersection graph's memory can OOM the worker heap.
- **`girih field … shells N`** — shell-BFS tile growth with per-tile decoration; large N is quadratic-ish tiles each carrying strapwork.
- **`repeat at C depth D`** — recursive circle placement, exponential in D.

Because the engine cannot self-police mid-flight, the design is: **L3 picks a budget before launch, L8 enforces it from outside, and the worker is disposable.** Worker isolation already keeps the main thread at 60 fps during any of this; the harms are a stuck spinner, a hot laptop, and (worst case, Safari) a tab-level memory kill — the last is accepted residual risk, noted in the risk register.

### 1.4 Worker watchdog design (`WorkerHost`)

New module `packages/lab/src/worker-host.ts`, a small class that owns the worker lifecycle so `main.ts` keeps calling `post()` and stays under the complexity gate:

- **State**: `worker`, `generation` (int), `deadlineTimer`, `lastGood: { source, params } | null`, `primed: boolean`.
- **Spawn**: `new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' })` exactly as today; tag all outgoing requests with `generation` alongside the existing `seq` (protocol change, §1.5). Replies from a stale generation are dropped before the `seq` logic even runs.
- **Evaluate**: start `deadlineTimer` at the L3-selected budget (15 s default / 60 s heavy). Clear it on any reply for the newest eval `seq` (the existing `latestEvalSeq` check).
- **Timeout / worker `error` / `messageerror` / user Stop** → one path: `worker.terminate()`; bump `generation`; respawn; synthesize a local `error` response with the L8 copy (Stop says "stopped" without the advice sentence); then **re-prime**: if `lastGood` exists and differs from the killed request, silently re-send it so the respawned worker rebuilds its `lastResult` cache — otherwise the STL and axis-view buttons would target a worker that answers "No mesh evaluated yet."
- **Priming gate**: `stl`/`views` requests are held (button disabled + spinner tooltip) until `primed` is true again after a respawn. On successful re-prime the stale-while-revalidate contract is fully restored.
- **Stop affordance**: the existing 300 ms spinner grows a "Stop" button after 2 s. One-click terminate+respawn; the Lab is never more than one click from responsive.
- **Budgets are constants** in `worker-host.ts` (`BUDGET_DEFAULT_MS = 15_000`, `BUDGET_HEAVY_MS = 60_000`) with the L3 sniff regexes beside them — one file to retune after real-world telemetry.

Cost of a kill: the respawned worker re-parses the engine bundle (already cached by the browser) and re-evaluates last-good once — a few hundred ms for preset-scale scripts. Acceptable.

### 1.5 Protocol changes (`protocol.ts`)

- `LabRequest['evaluate']` gains `generation: number` and changes `params` semantics to **reconcile mode**: the worker (custom and preset paths alike) parses first (`parse(source)` — cheap, no evaluation), drops unknown override names, clamps out-of-range values to the parsed spec, then calls `compileToGeometry(source, { params: reconciled })`.
- `LabResponse['result']` gains `adjustments: readonly KnobAdjustment[]` (the reconcile report; type moves to the shared package). Main thread toasts when non-empty and syncs knobs — the same UX as the P0 URL-load path.
- This **replaces the P0 two-pass boot** (evaluate-with-defaults → clamp → re-evaluate): one round trip for both preset-URL and `code=` boots, and it is the *only* correct mechanism for the mid-edit case where the author rewrites a `range` under a touched knob. `clampToSpecs` stays as the main-thread half for URL param keys (it produces the raw map the worker reconciles).
- All responses gain `generation` for the WorkerHost drop check.

---

## 2. Custom-orb editing UX

### 2.1 Layout — three surfaces, no modes on the Lab side

The Lab stays a single page; the code editor is a **resizable bottom drawer on the stage** (devtools-style), so knobs (left panel), code (drawer), and 3D/axis preview (stage) are visible simultaneously — §7's "the source is always visible" without sacrificing the preview:

```
┌───────────┬─────────────────────────────┐
│ chips     │ [3D][vertex-5][face-3]…     │
│ knobs     │        3D canvas            │
│ target    ├─────────────────────────────┤
│ actions   │ ▤ Code            [▲ hide]  │
│ gate      │ param radius = 60 range …   │
│           │ …textarea + line numbers…   │
└───────────┴─────────────────────────────┘
```

- **Editor widget: plain `<textarea>`** (monospace, line numbers in a gutter div, tab-key insertion). No CodeMirror/Monaco — the no-new-deps constraint decides this; the studio's textarea+highlight-layer pattern (`web/src/main.ts:4254`) can be ported later if syntax color proves worth it. Drawer is collapsed by default for preset browsing; a "Code" toggle in the stage header (and auto-open when arriving via `code=`) reveals it.
- **Preset chips stay exactly as shipped.** In custom mode no preset chip is active; a synthetic **"Custom orb"** chip renders at the end of the row (active style, non-dismissable) so the state is legible in the same visual vocabulary.
- **Knob panel is unchanged** — it renders whatever `ParamSpec[]` the last successful evaluation reported, which for custom source means **the author's own `param` lines become sliders**, the headline capability of P2.

### 2.2 When edited code re-derives knobs

One rule: **knobs re-derive on successful evaluate, and only then.** Editor input → 500 ms debounce (typing cadence; knobs keep their 200 ms) → `evaluate` with reconcile (§1.5) → on success, `applyResult` rebuilds/syncs the panel from `msg.specs` (add/remove/rename of `param` lines just works, per §7); on failure, last-good knobs + preview stay and the error panel shows the engine's sentence. There is no separate header-only re-parse path on the main thread — the engine bundle stays worker-only, and a dedicated `parseParams` round trip would add a protocol message for no observable UX gain over the 500 ms debounce.

### 2.3 Preset ⇄ custom state machine and dirty handling

- **Identity rule**: after each editor debounce, compare the buffer against every `SCRIPTS[i].source` by exact string equality. Match → the Lab is in preset mode for that id (URL `f=<id>` + override keys; chips re-highlight). No match → custom mode (`f=custom`). Exact match is correct, not just cheap: preset sources are canonical committed bytes, and "you are byte-identical to Rosette-Orb" is precisely what the preset badge may claim (§4.4).
- **Knob drags never edit the buffer.** In both modes, sliders write the `touched` override set (P0 machinery) — never the textarea. This keeps undo history intact, keeps derived defaults (`param inner = $outer - 22`) alive, and keeps drag-time work off the encoder. The §7 phrase "reflected in the visible source" is delivered by (a) the knob rows themselves, (b) a **"write values into code"** button in the drawer header that bakes overrides into the `param` defaults via `rewriteParamDefault` (§3.2) with one confirmation when it would overwrite a derived-default expression, and (c) **automatic bake on `.bkr` download** — a downloaded file must reproduce what's on screen with zero URL context. One rewrite helper, three call sites, all testable.
- **Dirty = custom mode with unsaved divergence.** Clicking a preset chip while dirty replaces the buffer, so: `confirm()` (native, no deps) — "Discard your custom orb and load <title>? Your code is also kept at this link / in this browser until you edit again." The claim is honest because of §2.4's draft persistence. Back-button behavior stays P0's reload-on-popstate, which round-trips through `code=` when it fits.

### 2.4 The `code=` round trip and the 1,800-char budget

**Codec** (shared package, §3.2): `encode(source) = compressToEncodedURIComponent('bkr1\n' + source)`; decode reverses and enforces L1's four checks. The `bkr1` sentinel is the codec-version tag (mermaid.live's `pako:` trick, folded inside the payload) and the truncation detector lz-string lacks.

**Write path** (custom mode, on the same 200/500 ms debounces): URL = `?v=1&f=custom&code=<enc>` **plus** touched param keys (the design doc's §6.3 contract: overrides ride next to `code=` and are applied after parse — reconciled by §1.5). `replaceState` for edits and drags; the preset→custom *transition* is a `pushState` (a navigation-sized jump, same rule as chip switches).

**Budget — measured.** Committed orb scripts are 1.1–2.2 KB raw. Gzip+base64 proxy (measured this session): Rosette-Orb 2,102 B → ~1,312 chars; Rosette-Weave 2,240 B → ~1,432; Hankin 1,663 B → ~1,184. lz-string lacks entropy coding and typically lands 10–25 % above gzip, so comment-heavy preset-scale sources sit at **~1,450–1,800 encoded chars — genuinely at the budget line**, and author scripts with generous comments will cross it. Behavior when `location.href` would exceed 1,800 chars:

- The URL is written as `?v=1&f=custom` **without** `code=` — never a truncated payload, never a silently-stale one.
- The actions section swaps "Copy link" into a warning state: "Too large to share as a link (N chars) — **Download .bkr** instead. Tip: trimming comments usually gets a script back under the line." Comment-stripping is a *suggestion to the author*, never automatic — the Lab does not rewrite user text.
- **Draft persistence backstop**: custom source (and touched overrides) mirror to `localStorage['orbLab.customDraft']` on the same debounce, restored on boot when the URL carries `f=custom` without a valid `code=`. This is what makes over-budget reloads, the Back button past an over-budget state, and the §2.3 confirm-copy honest. Single-slot, last-write-wins, cleared when the buffer re-matches a preset.

**Read path order at boot**: L1 decode → editor buffer + drawer open → evaluate with raw URL param keys (worker reconciles, one round trip) → toast adjustments. A parse-failing but well-formed payload **does** load into the editor with the verbatim error — that's an author mid-thought, not a damaged link.

**Open in Studio**: the Lab links to the studio as `/editor/#code/<same-encoded-payload>`. Hash transport is chosen over the dev pattern API because the deployed studio has no write API (`/api/patterns` is dev-only; prod falls back to starter files — verified `web/src/main.ts:3417-3449`). The studio's boot learns one new hash shape: `#code/…` decodes with the same shared codec into an in-memory file named "From Orb Lab" (dirty, unsaved), then the normal editor pipeline takes over.

---

## 3. Studio "Dials" tab

### 3.1 Where the knob layer lives — supersede §11 decision 6

P0 shipped the knob layer inside `packages/lab` because folding into `@naqshcoffee/ui` requires the external GitHub-Packages publish cycle and `GITHUB_PACKAGES_TOKEN` (recorded deviation, design doc §10). P2 is the moment both consumers exist, forcing the call:

- **Copy into `packages/web`** — rejected. The constraint table and machine table exist precisely so studio and Lab can never disagree (§8); two copies reintroduce the failure the design forbids.
- **Fold into `@naqshcoffee/ui` now** — rejected for P2. The token/publish friction is unchanged since P0, and these components will churn during P2 itself; publishing every iteration through an external package is the wrong loop.
- **New workspace package — chosen**: `packages/knobs` (`@naqshcoffee/bikar-knobs`), a sibling workspace member consumed by `packages/lab` and `packages/web` via the existing `"*"` workspace convention. Zero token friction, one source of truth, tree-shaking moot (it contains only knob code). **This supersedes resolved decision §11#6** on evidence discovered after it was made; record a decision doc noting that folding into `@naqshcoffee/ui` remains the end-state once the API stabilizes (post-P3), at which point the package moves wholesale.

### 3.2 Package contents

Moved verbatim (P2.1 is a pure move + import-path refactor, Lab behavior byte-identical): `knobs.ts` (`renderKnobPanel`/`syncKnobPanel`), `constraints.ts` (`applyConstraints`/`clampToSpecs`/`KnobAdjustment`), `machines.ts`. New modules:

- `code-codec.ts` — `encodeBkr`/`decodeBkr` with sentinel + size cap (§2.4); **the lz-string dependency lives here and only here**.
- `param-rewrite.ts` — `rewriteParamDefault(source, name, value): { source, replacedExpression: boolean }`. Line-anchored rewrite of the rigid `param <name> = <default> …` grammar (params must precede all other declarations — language ref — so the scan window is the header). Flags when it replaced a non-literal (derived) default so callers can confirm. Used by: Lab bake button, Lab `.bkr` download, studio Dials writes.

`packages/lab/src` keeps everything app-shaped: `main.ts`, `worker.ts`, `worker-host.ts`, `protocol.ts`, `scripts.ts`, `url-state.ts`, `viewer.ts`, new `editor.ts` (drawer) and `custom-state.ts` (identity rule, dirty flag, draft persistence) — the module split is also how `main.ts` stays under the complexity-10 gate as branches multiply.

### 3.3 Studio integration

The studio gets the §8 **input-mode toggle** — Dials / Code with inline-SVG glyphs (three-slider mixer; `</>` chevron), `aria-label`s, keyboard focus — orthogonal to the existing output tabs:

- **Dials is an alternate editing surface over the same buffer.** Slider change → `rewriteParamDefault` on the active file's content → set `input.value` → dispatch the `input` event. The studio's entire existing loop (highlight layer, debounce-compile at `main.ts:4933`, dirty marking, `/api/pattern` autosave in dev) runs untouched. No override plumbing, no second state store, no persistence questions — the file is the artifact, and dials edit the file. This deliberately differs from the Lab's override model, and the difference is principled: the Lab's identity/URL semantics need overrides; the studio's file semantics need writes.
- **Enablement**: Dials is clickable when the file's last successful evaluation reported `params` (all starter orbs qualify post-M5); otherwise disabled with the §8 tooltip ("declare `param` values to get dials"). Cross-param constraints and the adjustments toast come along from the shared package.
- **Known limitation, accepted**: the studio compiles on the **main thread**, so dial drags on heavy orbs will jank exactly as typing does today. Porting the studio to the Lab's worker+watchdog is real work with its own risks and is explicitly **out of P2 scope** — noted in the risk register as the likely first P3 item if it hurts.
- Machine/print-target UI stays Lab-only; the studio imports only the knob + constraint exports.

---

## 4. Test plan

Test infra facts: vitest globs `packages/*/tests/**/*.test.ts` (root `vitest.config.ts`); `packages/lab` currently has **no tests directory** — P2 creates `packages/lab/tests/` and `packages/knobs/tests/`; Playwright lives in `packages/e2e` (currently studio-only specs).

### 4.1 Unit coverage, keyed to the validation layers

| Layer | Tests (vitest) |
|---|---|
| L1/L2 codec | round-trip identity incl. unicode comments; sentinel-missing, null-decompress, empty, and truncated-at-every-10 % payloads all → damaged-link result, never partial source; decompression-bomb (repetitive 5 MB source) rejected by the 64 KB cap; `f=<preset>&code=` precedence |
| L3 sniff | each heavy regex hits its construct and nothing in the 11 committed preset sources except the intended `subdivide` cases |
| L4/L5 reconcile | worker `evaluate` (pure function extracted for testability) with: unknown override → dropped + adjustment; out-of-range vs freshly-shrunk range → clamped + adjustment; in-range → untouched; engine `ParseError` text passes through byte-identical (assert **no stack frames** in `message`) |
| L6 | existing `applyConstraints`/`clampToSpecs` behavior gets tests as it moves with the package; add name-convention opt-out case (custom script without `inner`/`shoulder`) |
| L8 | `WorkerHost` with an injected fake worker: deadline → terminate+respawn+generation bump; stale-generation replies dropped; re-prime sent with lastGood; stl/views gated until primed; Stop path; first-evaluate-times-out (no lastGood) leaves STL disabled with error shown |
| rewrite | `rewriteParamDefault`: literal default; derived default flagged; name-is-keyword (`param radius`); step/range/advanced tail preserved byte-for-byte; idempotence; bake-then-evaluate equals override-evaluate (golden equivalence — the property that makes download honest) |
| URL | budget math against a fixed origin; over-budget write omits `code=`; default elision unchanged for preset mode |

### 4.2 e2e (Playwright, `packages/e2e`)

Lab specs (new, against `vite preview` of `packages/lab`): edit code → new `param` line → slider appears; break the source → verbatim error + last-good canvas + STL disabled → fix → recovers; paste a bomb (`divide C0 into 4000` variant with a short test-only budget override via query flag) → watchdog copy appears, UI responsive, next evaluate succeeds; copy-link → open in fresh context → identical triangle count (exposed via a `data-tris` attribute on the gate panel); over-budget script → download affordance + draft restore after reload; damaged `code=` → toast + default preset. Studio specs: Dials toggle renders knobs for a param starter file; drag writes the param line into the visible code + dirty marker; param-less file → disabled tab tooltip; `#code/` hash boot creates "From Orb Lab" buffer.

Vendoring smoke (3d-models side): after `make lab`, `lab.html` + hashed assets exist and reference each other — a make-invoked shell check, not Playwright.

### 4.3 qiyas's role — and what "validated" means for custom orbs

`qiyas orb-validate` (M3, shipped) scores bikar's `--format views` output — per-symmetry-axis SVG renders — against the **engine's own declared `gt.json` ground truth**, gated at composite ≥ 0.95 (`qiyas/src/qiyas/cli.py:2992`, `orb_validate.py`). Three consequences for P2, stated explicitly:

1. **Custom orbs do not get qiyas runs in the Lab.** qiyas is Python and stays in CI (design doc §1 non-goal, reaffirmed). There is no in-browser path and P2 does not build one.
2. **Only presets carry recorded validation.** Strictly speaking, bikar can emit `gt.json` for *any* script — so a determined author can run `bikar render custom.bkr --format views` + `qiyas orb-validate` offline; the `.bkr` download help text mentions this as the power-user path. But the Lab's badge reflects only scores **we ran and recorded in CI at declared defaults** for committed scripts.
3. **Badge semantics — three trust levels, precise copy**: (a) **"qiyas-validated ✓ 1.000"** — preset chip, shown when the design is byte-identical to the committed script *at declared defaults* (the §2.3 identity rule makes this check exact). The illustration was **"✓ 0.954"** when this doc was drafted, because that was `rosette-dodeca`'s recorded composite; it reads 1.000 from qiyas v0.4.0 on, and the number here is re-typed rather than generated, so it is an illustration of the *format* — the badge's number comes from `packages/lab/src/scripts.ts`, which CI holds to a measured sweep ([orb-lab-design.md §3 footnote ²](orb-lab-design.md#v1-archetypes)); (b) **"calibrated range"** — preset with knobs moved: within the gate-swept envelope, but the qiyas score was measured at defaults, so the badge softens honestly; (c) **custom orbs show the mesh-gate PASS row only** — the existing "PASS — printable" is the entire claim, and the badge area explicitly reads "custom design — not qiyas-validated". The axis-view tabs (same `projectOrbView`/`renderOrbViewSVG` path qiyas consumes) remain available for custom orbs, honestly labeled "the view qiyas *would* validate."

Per-phase gate unchanged: bikar `npm test` + `npm run ci`; qiyas orb-validate ≥ 0.95 re-run on presets only (P2 changes no preset geometry — expect byte-identical, making this a regression tripwire).

---

## 5. Milestones, effort, risks

### 5.1 Slicing (dependency-ordered)

| Slice | Contents | Effort | Ships alone? |
|---|---|---|---|
| **P2.1 — knob-layer extraction** | `packages/knobs` created; `knobs/constraints/machines` moved verbatim; lab imports updated; Lab behavior byte-identical (manual smoke + existing URL-clamp behavior re-verified); decision doc superseding §11#6 | **S** | Yes — pure refactor |
| **P2.2 — worker hardening** | `WorkerHost` (timeout/terminate/respawn/re-prime/Stop), generation in protocol, L3 sniff, worker size guard, SVG-escaping audit + test (L0). Benefits presets immediately (subdivide sliders) and is a hard prerequisite for accepting untrusted code | **M** | Yes — user-visible resilience win |
| **P2.3 — custom mode core** | Editor drawer, `custom-state.ts` (identity rule, dirty, confirm), worker reconcile semantics + adjustments (replaces two-pass boot), verbatim-error loop, knob re-derive, bake button + bake-on-download, "Custom orb" chip | **L** (largest; splittable at "no URL persistence yet") | Yes — custom editing works, refresh loses work (draft lands in P2.4) |
| **P2.4 — share codec** | `code-codec.ts` + lz-string dep, L1 decode path, budget behavior + copy-link states, draft persistence, `f=custom` URL write discipline (push on transition) | **M** | Yes — completes the §6.3 contract |
| **P2.5 — studio Dials + handoff** | Dials/Code toggle + icons, shared-knob consumption, `rewriteParamDefault` write-through, disabled-state tooltip, `#code/` hash boot, Lab "Open in Studio" button | **M** | Yes |
| **P2.6 — test hardening + vendor + docs** | e2e suites (§4.2), vendoring smoke, orb-lab-design §10 status update, authoring-help copy (L6 name conventions, offline qiyas path), badge copy (§4.3) | **M**, partly continuous | Docs/tests trail each slice; final pass here |

Recommended order is as numbered: P2.1 unblocks P2.5 and shrinks every later diff; P2.2 before any untrusted input is accepted; P2.3/P2.4 are the core; P2.5 can proceed in parallel with P2.4 after P2.1+P2.3's rewrite helper exists.

### 5.2 Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| lz-string payloads exceed 1,800 chars for comment-heavy scripts (measured: presets already at ~1.4–1.8k) | High | Medium — share-by-link degrades to share-by-file | Budget behavior + draft persistence (§2.4); measure real lz-string numbers in P2.4's first commit and revisit the threshold copy if presets themselves cross it |
| Watchdog kills a *legitimate* long evaluation (subdivide 4 + dense pattern can exceed 60 s on slow hardware) | Medium | Medium — author frustration | Stop-vs-timeout copy differs; timeout message names the levers; budgets are one-file constants; consider a "keep waiting" extension button post-P2 if reports arrive |
| Worker OOM behavior varies by browser (Safari may kill the tab, not the worker) | Medium | Medium | Accepted residual; L3 sniff catches the predictable bombs pre-launch; document in help |
| `rewriteParamDefault` corrupts exotic-but-legal formatting | Low (grammar is line-rigid, params header-only) | High if it happens (silent code damage) | Golden equivalence property test (bake≡override); `replacedExpression` confirm path; rewrite refuses (error, not guess) on no-match |
| Preset-identity exact-match is too strict (whitespace edits flip to custom) | Medium | Low — cosmetic state change, knobs keep working | By design (byte-identity backs the qiyas badge, §4.3); revisit with normalization only if user reports arrive |
| Studio main-thread compile janks under dial drags on heavy orbs | High | Low–Medium | Accepted for P2 (parity with typing today); worker port is the flagged P3 candidate |
| Divergence pressure returns when `@naqshcoffee/ui` fold-in eventually happens | Low now | Low | Package moves wholesale later; decision doc records the end-state intent |
| `main.ts` complexity creep past the ≤10 gate as custom branches land | Medium | Low (CI catches it) | Module split (§3.2) planned up front, not retrofitted |
