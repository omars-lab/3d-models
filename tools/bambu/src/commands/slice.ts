// `bambu slice` — headless slicing via the BambuStudio CLI.
//   plate <model> : slice a .stl/.3mf/.step/.obj into a sliced .3mf
//
// This wraps the BambuStudio CLI that ships inside the .app bundle. The CLI's flags are
// version-dependent and the X2D is brand-new hardware, so this command does NOT hard-code a profile:
// it builds a transparent invocation you can inspect (`--dry-run`), lets you pass machine/process/
// filament settings explicitly, and forwards raw args after `--` for anything we don't model yet.
// When no headless binary is found it falls back to opening the model in Studio's GUI (AppleScript)
// and says so — it cannot produce a sliced .3mf that way, so it exits non-zero.
//
// A .bkr is bikar's source, not a slicer input: render it to STL first (see the 3d-models build,
// e.g. `make orbs`) and slice the STL. We reject .bkr here rather than silently doing nothing.

import { Command } from "commander";
import { existsSync, statSync, readdirSync, writeFileSync, readFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, extname, join, resolve } from "node:path";
import { runWithTimeout, ev } from "../log.js";
import { surveyBackends, preferenceFor } from "../backends/router.js";
import { locateStudio } from "../backends/studio-cli.js";
import { locateStudioApp, openFileInApp } from "../backends/applescript.js";
import {
  parseSlicerWarnings,
  classifyWarnings,
  loadManifest,
  studioVersionFrom,
  sidecarPath,
  hashFile,
  type WarningsSidecar,
} from "../backends/warnings.js";
import { registerCompose } from "./compose.js";

const SLICEABLE = new Set([".stl", ".3mf", ".step", ".stp", ".obj"]);

// BambuStudio's --load-settings/--load-filaments take JSON *file paths*, not preset display names —
// a bare name fails with "operator(): can not find setting file". But the human-facing docs (the
// bench sheet, calibration-design) name presets by their display name ("Bambu Lab X2D 0.4 nozzle").
// So we resolve a name → its bundled JSON here, keeping ONE spelling of a profile across CLI + docs.
// The presets ship inside the app: <app>/Contents/Resources/profiles/<Vendor>/{machine,process,
// filament}/<name>.json. An argument that already resolves to a file passes through untouched (the
// power-user escape hatch for a hand-edited profile).

/** <app>/Contents/MacOS/BambuStudio → <app>/Contents/Resources/profiles, or null if absent. */
function profilesRoot(studioBin: string): string | null {
  const root = join(dirname(dirname(studioBin)), "Resources", "profiles");
  return existsSync(root) ? root : null;
}

/** Find "<name>.json" under any vendor's given subdirs (BBL first, since the X2D is a Bambu Lab machine). */
function findPreset(root: string, subdirs: string[], name: string): string | null {
  const dirs = readdirSync(root, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name);
  const vendors = ["BBL", ...dirs.filter((d) => d !== "BBL")];
  for (const vendor of vendors) {
    for (const sub of subdirs) {
      const p = join(root, vendor, sub, `${name}.json`);
      if (existsSync(p)) return p;
    }
  }
  return null;
}

/** Resolve each ';'-joined token: an existing file passes through; a preset name → its bundled JSON.
 *  Throws with a clear, actionable message (listing where it looked) rather than deferring to the
 *  slicer's opaque "can not find setting file". */
export function resolvePresetList(value: string, kind: "settings" | "filament", studioBin: string): string {
  const subdirs = kind === "filament" ? ["filament"] : ["machine", "process"];
  const root = profilesRoot(studioBin);
  return value
    .split(";")
    .map((t) => t.trim())
    .filter(Boolean)
    .map((tok) => {
      const asPath = resolve(tok);
      if (existsSync(asPath)) return asPath; // already a JSON path
      const hit = root ? findPreset(root, subdirs, tok) : null;
      if (hit) return hit;
      throw new Error(
        root
          ? `could not resolve ${kind} preset "${tok}" — looked for "${tok}.json" under ` +
            `${subdirs.map((s) => `${root}/*/${s}/`).join(", ")}. ` +
            `Check the exact preset name (e.g. \`bambu setup studio\` lists X2D profiles), or pass an absolute JSON path.`
          : `cannot resolve preset "${tok}": BambuStudio profiles dir not found under the app bundle — pass an absolute JSON path.`,
      );
    })
    .join(";");
}

interface SliceOpts {
  out?: string;
  outputdir?: string;
  settings?: string;
  filament?: string;
  plate: string;
  arrange: boolean;
  timeout: string;
  dryRun?: boolean;
  strict?: boolean;
  filamentMapMode?: string;
}

// ── X2D dual-nozzle filament grouping ────────────────────────────────────────────────────────────
// The GUI's "Filament Grouping" selector maps to the process-config enum `filament_map_mode`
// (a ConfigOptionEnum<FilamentMapMode>). Verified 2026-09-17 (BambuStudio 02.08.02.61, X2D presets):
//   • The enum literals are "Auto For Flush" (Filament-Saving, the DEFAULT — minimise waste/flush),
//     "Auto For Match" (Quality — prioritise print quality over saving) and "Manual" (a hand-assigned
//     per-filament `filament_map` array).
//   • Studio does NOT validate the string — a typo (`Bogus`) slices exit 0 and silently falls back to
//     the default — so WE own the token→literal mapping and reject anything unknown, rather than letting
//     a silent no-op through.
//   • The key must be MERGED INTO the one process JSON: passing it as a second `--load-settings` process
//     file errors "duplicate process config file". The merged value lands in the sliced 3mf's
//     project_settings.config / model_settings.config.
//   • With a single filament the grouping collapses to one group (`filament_maps=1`) regardless of mode
//     — it is a definitional no-op. So this flag only DOES anything on a multi-filament plate.
// See docs/issues/x2d-filament-grouping-mode.md.

const FILAMENT_MAP_MODE_ENUM: Record<string, string> = {
  saving: "Auto For Flush", // Filament-Saving — the default
  quality: "Auto For Match", // Quality — prioritise print quality over filament saving
};

/** Map a validated grouping token to Studio's exact enum literal. `manual` is recognised but rejected
 *  (it needs an explicit per-filament `filament_map` array this command does not generate); anything
 *  else throws — Studio would silently accept a typo as the default, so we must not. */
export function filamentMapModeEnum(token: string): string {
  const t = token.trim().toLowerCase();
  if (t === "manual") {
    throw new Error(
      "--filament-map-mode manual needs an explicit per-filament `filament_map` array, which this " +
        "command does not generate. Hand-edit the process JSON (add `filament_map`) and pass it with " +
        "-s, or use `saving` (Filament-Saving, the default) or `quality`.",
    );
  }
  const hit = FILAMENT_MAP_MODE_ENUM[t];
  if (!hit) {
    throw new Error(
      `unknown --filament-map-mode "${token}". Use: saving (Filament-Saving, default), quality, or manual.`,
    );
  }
  return hit;
}

/** Number of loaded filaments in a ';'-joined --filament list. Grouping only means something with ≥2. */
export function filamentCount(filament?: string): number {
  if (!filament) return 0;
  return filament
    .split(";")
    .map((t) => t.trim())
    .filter(Boolean).length;
}

/** Merge `filament_map_mode` into the ONE process config among a resolved --settings list. Studio errors
 *  on a second process file, so the enum must live inside the process JSON itself. Writes the merged copy
 *  into `scratchDir` and returns the new ';'-joined settings string plus which preset it merged into.
 *  Throws if no process config is present (the enum has nowhere to go). */
export function injectFilamentMapMode(
  settings: string,
  enumValue: string,
  scratchDir: string,
): { settings: string; mergedInto: string } {
  const paths = settings
    .split(";")
    .map((t) => t.trim())
    .filter(Boolean);
  let mergedInto = "";
  const out = paths.map((p) => {
    let cfg: Record<string, unknown>;
    try {
      cfg = JSON.parse(readFileSync(p, "utf8")) as Record<string, unknown>;
    } catch {
      return p; // not JSON we can read — leave it (machine configs pass through untouched)
    }
    if (cfg.type !== "process") return p;
    cfg.filament_map_mode = enumValue;
    const tmp = join(scratchDir, `fmm.${basename(p)}`);
    writeFileSync(tmp, JSON.stringify(cfg, null, 2) + "\n");
    mergedInto = p;
    return tmp;
  });
  if (!mergedInto) {
    throw new Error(
      "--filament-map-mode needs a process preset in -s/--settings — the enum lives in the process " +
        "config. Pass the process preset name/path with -s.",
    );
  }
  return { settings: out.join(";"), mergedInto };
}

// Slicer warnings are captured from BambuStudio's OWN output, not guessed: at `--debug 2` (warning)
// the headless CLI emits the same per-object advisory the GUI shows, as a structured
// `plate N: found [NON_CRITICAL] slicing warnings: <msg>` line (measured 2026-09-17 — at the default
// log level it is silent, which is why the earlier "a clean slice is silent" conclusion was wrong).
// `parseSlicerWarnings` reads exactly those lines; everything else the slicer prints is ignored. The
// captured warnings are classified against the by-design manifest and written to a sidecar beside the
// .3mf so the dispatch gate (`bambu print send`) can refuse a plate carrying an UNEXPECTED warning
// without re-slicing. See backends/warnings.ts.

/** Build the BambuStudio CLI argument vector. Kept in one place so `--dry-run` shows the real thing,
 *  and so `slice plate` (one input) and `slice compose` (N inputs onto one plate) share ONE spelling
 *  of the invocation — the reuse boundary docs/plate-composer-design.md §2 draws. `--debug 2` raises
 *  the log level to `warning` so slicing warnings reach stdout (they are silent at the default level);
 *  it does not change the slice, only what is reported. Multiple trailing model paths are how the
 *  Bambu Studio CLI composes several objects onto one plate (compose research Topic 1). */
export function buildStudioArgs(
  inputs: string[],
  outDir: string,
  outFile: string,
  opts: { settings?: string; filament?: string; arrange: boolean; plate: string },
  raw: string[],
): string[] {
  const args: string[] = [];
  args.push("--debug", "2"); // surface slicing warnings (see note above)
  if (opts.settings) args.push("--load-settings", opts.settings);
  if (opts.filament) args.push("--load-filaments", opts.filament);
  if (opts.arrange) args.push("--arrange", "1");
  args.push("--slice", opts.plate); // "0" = every plate
  args.push("--outputdir", outDir);
  args.push("--export-3mf", outFile);
  args.push(...raw); // escape hatch for version-specific flags we don't model
  args.push(...inputs); // one input for `slice plate`; N for `slice compose`
  return args;
}

async function runSlice(input: string, opts: SliceOpts, raw: string[]): Promise<void> {
  const abs = resolve(input);
  if (!existsSync(abs)) {
    console.error(`no such file: ${input}`);
    process.exitCode = 1;
    return;
  }
  const ext = extname(abs).toLowerCase();
  if (ext === ".bkr") {
    console.error("a .bkr is bikar source, not a slicer input.");
    console.error("Render it to STL first (e.g. `make orbs` in 3d-models), then slice the STL.");
    process.exitCode = 2;
    return;
  }
  if (!SLICEABLE.has(ext)) {
    console.error(`unsupported input '${ext}'. Sliceable: ${[...SLICEABLE].join(", ")}`);
    process.exitCode = 2;
    return;
  }

  const outDir = opts.outputdir ? resolve(opts.outputdir) : dirname(abs);
  const outFile = opts.out ?? `${basename(abs, ext)}.sliced.3mf`;
  const outPath = join(outDir, outFile);

  // Router: prefer the headless CLI, GUI last.
  const avail = await surveyBackends();
  const order = preferenceFor("slice", avail);
  const studioBin = locateStudio();

  if (order[0] === "studio-cli" && studioBin) {
    // Resolve preset names → bundled JSON paths before building args, so --dry-run shows the real
    // (resolved) command and a bad name fails here with a clear message, not inside the slicer.
    try {
      if (opts.settings) opts.settings = resolvePresetList(opts.settings, "settings", studioBin);
      if (opts.filament) opts.filament = resolvePresetList(opts.filament, "filament", studioBin);
    } catch (err) {
      console.error((err as Error).message);
      process.exitCode = 2;
      return;
    }

    // Dual-nozzle filament grouping. Only meaningful with ≥2 filaments; a single filament collapses to
    // one group regardless of mode, so we say the no-op out loud rather than pretend to set it.
    if (opts.filamentMapMode) {
      let enumValue: string;
      try {
        enumValue = filamentMapModeEnum(opts.filamentMapMode);
      } catch (err) {
        console.error((err as Error).message);
        process.exitCode = 2;
        return;
      }
      if (filamentCount(opts.filament) <= 1) {
        console.log(
          `filament grouping: single filament → no-op (grouping needs ≥2 filaments). ` +
            `The default is Filament-Saving; nothing to set.`,
        );
      } else {
        try {
          const scratch = mkdtempSync(join(tmpdir(), "bambu-fmm-"));
          const injected = injectFilamentMapMode(opts.settings ?? "", enumValue, scratch);
          opts.settings = injected.settings;
          console.log(
            `filament grouping: ${opts.filamentMapMode} ("${enumValue}") merged into ${basename(injected.mergedInto)}.`,
          );
        } catch (err) {
          console.error((err as Error).message);
          process.exitCode = 2;
          return;
        }
      }
    }

    const args = buildStudioArgs([abs], outDir, outFile, opts, raw);
    if (opts.dryRun) {
      console.log("dry run — would execute:");
      console.log([studioBin, ...args].map((a) => (/\s/.test(a) ? `"${a}"` : a)).join(" "));
      return;
    }
    const timeoutMs = Math.max(30, Number(opts.timeout) || 300) * 1000;
    ev("slice_start", { input: basename(abs), plate: opts.plate });
    const res = await runWithTimeout(studioBin, args, { timeoutMs, label: "studio_slice" });
    if (res.timedOut) {
      console.error(`slice timed out after ${opts.timeout}s. Raise --timeout, or slice fewer plates.`);
      process.exitCode = 1;
      return;
    }
    if (res.code !== 0 || !existsSync(outPath)) {
      console.error(`slice failed (exit ${res.code ?? "null"}).`);
      const tail = (res.stderr || res.stdout).trim().split("\n").slice(-8).join("\n");
      if (tail) console.error(tail);
      console.error("BambuStudio CLI flags are version-dependent — check `" + studioBin + " --help`,");
      console.error("and pass machine/process/filament with --settings/--filament or raw args after `--`.");
      process.exitCode = 1;
      return;
    }
    const kb = Math.round(statSync(outPath).size / 1024);

    // Capture BambuStudio's own slicing warnings, classify against the by-design manifest, and write
    // a sidecar beside the .3mf so `bambu print send` can gate dispatch without re-slicing.
    const combined = `${res.stdout}\n${res.stderr}`;
    const warnings = parseSlicerWarnings(combined);
    const { expected, unexpected } = classifyWarnings(warnings, loadManifest());
    const sidecar: WarningsSidecar = {
      tool: "bambu slice",
      sliced_at: new Date().toISOString(),
      studio_version: studioVersionFrom(combined),
      source_sha256: hashFile(outPath) ?? undefined, // binds this capture to THESE .3mf bytes
      warnings,
    };
    try {
      writeFileSync(sidecarPath(outPath), JSON.stringify(sidecar, null, 2) + "\n");
    } catch (err) {
      console.error(`warning: could not write warnings sidecar: ${(err as Error).message}`);
    }
    ev("slice_done", {
      out: basename(outPath),
      kb,
      warnings: warnings.length,
      expected: expected.length,
      unexpected: unexpected.length,
    });
    console.log(`sliced → ${outPath} (${kb} KB)`);

    if (warnings.length === 0) {
      console.log("slicer warnings: none — clean.");
    } else {
      if (expected.length > 0) {
        console.log(`slicer warnings: ${expected.length} expected (by design):`);
        for (const { warning, rule } of expected) {
          const who = warning.object ?? "(plate)";
          console.log(`  ✓ ${who}: ${warning.message}`);
          console.log(`      expected — ${rule.reason}${rule.settles ? ` [${rule.settles}]` : ""}`);
        }
      }
      if (unexpected.length > 0) {
        console.error(`slicer warnings: ${unexpected.length} UNEXPECTED — dispatch will be blocked:`);
        for (const w of unexpected) {
          const who = w.object ?? "(plate)";
          console.error(`  ✗ [${w.severity}] ${who}: ${w.message}`);
        }
        console.error("Eyeball it (`bambu slice open " + basename(outPath) + "`), fix the model/settings and re-slice,");
        console.error("or add a rule to .claude/gates/expected-slicer-warnings.json if it is genuinely by-design.");
      }
    }
    // Fail non-zero when a warning would block dispatch, or under --strict for any warning at all.
    if (unexpected.length > 0 || (opts.strict && warnings.length > 0)) {
      process.exitCode = 1;
    }
    return;
  }

  // No headless binary. Fall back to the GUI if Studio.app is present — honest about the limit.
  const studioApp = locateStudioApp();
  if (studioApp) {
    console.error("No headless BambuStudio binary found — opening the model in Studio's GUI.");
    console.error("Slicing there is manual: arrange, pick the X2D profile, and export the sliced 3mf.");
    try {
      await openFileInApp(studioApp, abs);
    } catch (err) {
      console.error(`could not open Studio: ${(err as Error).message}`);
    }
    process.exitCode = 2; // no sliced .3mf was produced headlessly
    return;
  }

  console.error("BambuStudio not found. Install it, or set SLICER_PATH to the CLI binary.");
  console.error("Run `bambu setup doctor` / `bambu setup studio` for guidance.");
  process.exitCode = 1;
}

// `bambu slice open <plate>` — open a sliced plate (or any model) in the Bambu Studio GUI so the
// operator can eyeball it before dispatch. Read-only and local: it opens a file, changes nothing on
// the printer, and sits BEFORE the owner gate. This is the first-party replacement for a raw
// `open -a BambuStudio <file>` in the guide-print runbook — so there is one spelling of "open it in
// Studio" that reports honestly when Studio is missing.
async function runOpen(input: string): Promise<void> {
  const abs = resolve(input);
  if (!existsSync(abs)) {
    console.error(`no such file: ${input}`);
    process.exitCode = 1;
    return;
  }
  const studioApp = locateStudioApp();
  if (!studioApp) {
    console.error("BambuStudio not found under /Applications. Install it (`bambu setup studio`),");
    console.error("or open the file manually.");
    process.exitCode = 1;
    return;
  }
  try {
    ev("studio_open", { file: basename(abs), app: studioApp });
    await openFileInApp(studioApp, abs);
    console.log(`opened ${abs} in ${studioApp.replace(/\.app$/, "")}`);
  } catch (err) {
    console.error(`could not open Studio: ${(err as Error).message}`);
    process.exitCode = 1;
  }
}

export function registerSlice(program: Command): void {
  const slice = program.command("slice").description("headless slicing via the BambuStudio CLI");

  slice
    .command("plate <model>")
    .description("slice a .stl/.3mf/.step/.obj into a sliced .3mf")
    .option("-o, --out <file>", "output filename (default: <model>.sliced.3mf)")
    .option("-d, --outputdir <dir>", "output directory (default: alongside the input)")
    .option(
      "-s, --settings <names|paths>",
      'machine + process, semicolon-joined — preset display names (resolved to the bundled JSON) or JSON paths',
    )
    .option(
      "-f, --filament <names|paths>",
      "filament, semicolon-joined — preset display name (resolved to the bundled JSON) or JSON path",
    )
    .option("-p, --plate <n>", "plate index to slice, 0 = all", "0")
    .option(
      "--filament-map-mode <mode>",
      "X2D dual-nozzle filament grouping: saving (Filament-Saving, default) | quality | manual — only affects a plate with ≥2 filaments",
    )
    .option("--arrange", "arrange objects before slicing", false)
    .option("-t, --timeout <seconds>", "slice timeout in seconds", "300")
    .option("--strict", "exit non-zero if the slicer prints any warning/error-looking line", false)
    .option("--dry-run", "print the exact BambuStudio invocation and exit", false)
    .allowUnknownOption(false)
    .action(async (model: string, opts: SliceOpts, cmd: Command) => {
      // Anything after `--` is forwarded verbatim to the BambuStudio CLI.
      const raw = cmd.args.slice(1);
      await runSlice(model, opts, raw);
    });

  slice
    .command("open <plate>")
    .description("open a sliced plate (or model) in the Bambu Studio GUI to eyeball before dispatch")
    .action(async (plate: string) => {
      await runOpen(plate);
    });

  // `slice compose <plate.yaml>` — many rendered pieces onto one plate. Lives in compose.ts but is a
  // sibling subverb of this same `slice` group (docs/plate-composer-design.md §1), reusing the helpers
  // exported above (resolvePresetList, buildStudioArgs) rather than forking the invocation.
  registerCompose(slice);
}
