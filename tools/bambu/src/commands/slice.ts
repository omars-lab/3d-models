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
import { existsSync, statSync, readdirSync } from "node:fs";
import { basename, dirname, extname, join, resolve } from "node:path";
import { runWithTimeout, ev } from "../log.js";
import { surveyBackends, preferenceFor } from "../backends/router.js";
import { locateStudio } from "../backends/studio-cli.js";
import { appInstalled, activateApp } from "../backends/applescript.js";

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
function resolvePresetList(value: string, kind: "settings" | "filament", studioBin: string): string {
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
}

// A CLEAN BambuStudio slice is silent — it emits no warning/error lines to stdout/stderr (verified
// 2026-09-17 against the machine card). So this scan is BEST-EFFORT: there is no documented CLI
// warning vocabulary to match, and a warning-free slice looks exactly like a warning-suppressed one.
// It surfaces anything the slicer prints that reads like a warning so it is never swallowed; the
// AUTHORITATIVE, realized-truth gate is `bambu validate sliced` over the produced .3mf (it reads the
// gcode toolpath + the slice_info skipped-object flags, which cannot be silently absent).
const WARNING_RE = /\b(warn(?:ing)?|error|fail(?:ed|ure)?|cannot|could ?not|unable|invalid|not printable|outside\s+(?:the\s+)?print|exceed|collision|skipp?ed)\b/i;

/** Best-effort: lines from the slicer's own output that look like warnings/errors (deduped, capped). */
function scanSlicerWarnings(stdout: string, stderr: string): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const raw of `${stdout}\n${stderr}`.split("\n")) {
    const line = raw.trim();
    if (!line || !WARNING_RE.test(line)) continue;
    if (seen.has(line)) continue;
    seen.add(line);
    out.push(line);
    if (out.length >= 40) break; // never let a firehose bury the summary
  }
  return out;
}

/** Build the BambuStudio CLI argument vector. Kept in one place so `--dry-run` shows the real thing. */
function buildStudioArgs(input: string, outDir: string, outFile: string, opts: SliceOpts, raw: string[]): string[] {
  const args: string[] = [];
  if (opts.settings) args.push("--load-settings", opts.settings);
  if (opts.filament) args.push("--load-filaments", opts.filament);
  if (opts.arrange) args.push("--arrange", "1");
  args.push("--slice", opts.plate); // "0" = every plate
  args.push("--outputdir", outDir);
  args.push("--export-3mf", outFile);
  args.push(...raw); // escape hatch for version-specific flags we don't model
  args.push(input);
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
    const args = buildStudioArgs(abs, outDir, outFile, opts, raw);
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
    const warnings = scanSlicerWarnings(res.stdout, res.stderr);
    ev("slice_done", { out: basename(outPath), kb, warnings: warnings.length });
    console.log(`sliced → ${outPath} (${kb} KB)`);
    if (warnings.length > 0) {
      console.error(`slicer messages (best-effort scan — ${warnings.length}):`);
      for (const w of warnings) console.error(`  ${w}`);
      console.error("Gate the realized plate with `bambu validate sliced " + basename(outPath) + "`.");
      if (opts.strict) {
        console.error("--strict: treating slicer messages as fatal.");
        process.exitCode = 1;
      }
    }
    return;
  }

  // No headless binary. Fall back to the GUI if Studio.app is present — honest about the limit.
  const studioApp = ["Bambu Studio.app", "BambuStudio.app", "BambuStudio-beta.app"].find(appInstalled);
  if (studioApp) {
    console.error("No headless BambuStudio binary found — opening the model in Studio's GUI.");
    console.error("Slicing there is manual: arrange, pick the X2D profile, and export the sliced 3mf.");
    try {
      await activateApp(studioApp.replace(/\.app$/, ""));
      await runWithTimeout("open", ["-a", studioApp, abs], { timeoutMs: 15_000, label: "studio_open" });
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
}
