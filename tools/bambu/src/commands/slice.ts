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
import { existsSync, statSync } from "node:fs";
import { basename, dirname, extname, join, resolve } from "node:path";
import { runWithTimeout, ev } from "../log.js";
import { surveyBackends, preferenceFor } from "../backends/router.js";
import { locateStudio } from "../backends/studio-cli.js";
import { appInstalled, activateApp } from "../backends/applescript.js";

const SLICEABLE = new Set([".stl", ".3mf", ".step", ".stp", ".obj"]);

interface SliceOpts {
  out?: string;
  outputdir?: string;
  settings?: string;
  filament?: string;
  plate: string;
  arrange: boolean;
  timeout: string;
  dryRun?: boolean;
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
    ev("slice_done", { out: basename(outPath), kb });
    console.log(`sliced → ${outPath} (${kb} KB)`);
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
      "-s, --settings <paths>",
      'machine + process settings, semicolon-joined (BambuStudio --load-settings)',
    )
    .option("-f, --filament <paths>", "filament settings, semicolon-joined (BambuStudio --load-filaments)")
    .option("-p, --plate <n>", "plate index to slice, 0 = all", "0")
    .option("--arrange", "arrange objects before slicing", false)
    .option("-t, --timeout <seconds>", "slice timeout in seconds", "300")
    .option("--dry-run", "print the exact BambuStudio invocation and exit", false)
    .allowUnknownOption(false)
    .action(async (model: string, opts: SliceOpts, cmd: Command) => {
      // Anything after `--` is forwarded verbatim to the BambuStudio CLI.
      const raw = cmd.args.slice(1);
      await runSlice(model, opts, raw);
    });
}
