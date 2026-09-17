// `bambu validate` — gate a mesh / plate / record / sliced-plate before it ships.
//   mesh <model.bkr>  : bikar's own min-strut/FDM --check (renders to a throwaway STL)
//   plate             : the 23-rung calibration expectation table (build/verify_machine_card.py)
//   record [dir]      : the prints gate over a records dir (.claude/gates/prints_gate.py)
//   sliced <3mf>      : gate the SLICED plate itself — realized brim/support/raft, object count,
//                       header (printer/nozzle) — and report time / length / derived grams.
//
// Every verb shells to the EXISTING authority rather than reimplementing it (robustness-over-ease:
// one code path, never two that can disagree). bikar is the geometry engine and producer of record;
// verify_machine_card.py owns the §7 table (D-014); prints_gate.py owns the record schema (§7). We
// only route to them with the right paths + BIKAR_DIR. `sliced` reads the .3mf (a zip) via `unzip`
// — same ethos, no bundled zip lib — and gates the REALIZED gcode, not just the settings, because a
// setting is an intent and the toolpath is the truth (a bare-plate expectation is only met if no
// Brim/Support/Raft feature was actually emitted).

import { Command } from "commander";
import { existsSync } from "node:fs";
import { basename, extname, join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { runWithTimeout, ev } from "../log.js";
import { locateBikarCli, bikarDir } from "../backends/bikar.js";
import { repoRoot, recordsDir } from "../paths.js";
import { readMember, listMembers } from "../threemf.js";
import { readSidecar, classifyWarnings, loadManifest, sidecarPath } from "../backends/warnings.js";

const PYTHON = process.env.PYTHON ?? "python3";

// Filament geometry for the grams derivation. The X2D PLA profile ships filament_density=['0'], so
// the headless slice leaves used_g=0.00 — grams must be DERIVED from a real density, and reported as
// derived/attributed, never as a slice output. 1.75 mm is the X2D filament; 1.24 g/cm³ is a common
// PLA density (attributed — a real spool's TDS is the grounded number; --density overrides).
const FILAMENT_DIAMETER_MM = 1.75;
const DEFAULT_PLA_DENSITY = 1.24;

async function runMesh(model: string): Promise<void> {
  const abs = resolve(model);
  if (!existsSync(abs)) {
    console.error(`no such file: ${model}`);
    process.exitCode = 1;
    return;
  }
  if (extname(abs).toLowerCase() !== ".bkr") {
    console.error(`mesh validation checks bikar source: expected a .bkr, got '${extname(abs)}'.`);
    console.error("An STL/3mf is already rendered geometry — check it at its .bkr source instead.");
    process.exitCode = 2;
    return;
  }
  const cli = locateBikarCli();
  if (!cli) {
    console.error(`bikar CLI not built at ${bikarDir()}/packages/cli/dist/index.js.`);
    console.error("Build bikar (npm run build there), or set BIKAR_DIR to your checkout.");
    process.exitCode = 1;
    return;
  }
  // Render to a throwaway STL with --check; bikar's exit code is the verdict (same as `make orbs`).
  const out = join(tmpdir(), `bambu-mesh-${Date.now()}.stl`);
  ev("mesh_check_start", { model: abs });
  const res = await runWithTimeout("node", [cli, "render", abs, "--format", "stl", "--check", "-o", out], {
    timeoutMs: 120_000,
    label: "bikar_check",
  });
  if (res.timedOut) {
    console.error("mesh check timed out.");
    process.exitCode = 1;
    return;
  }
  if (res.stdout.trim()) console.log(res.stdout.trim());
  if (res.stderr.trim()) console.error(res.stderr.trim());
  ev("mesh_check_done", { code: res.code ?? "null" });
  if (res.code !== 0) {
    console.error(`mesh check FAILED (exit ${res.code ?? "null"}).`);
    process.exitCode = 1;
  } else {
    console.log("mesh check PASSED.");
  }
}

async function runPlate(): Promise<void> {
  const root = repoRoot();
  if (!root) {
    console.error("could not find the repo root (.claude/gates). Run from inside the 3d-models repo.");
    process.exitCode = 1;
    return;
  }
  const verifier = join(root, "build", "verify_machine_card.py");
  if (!existsSync(verifier)) {
    console.error(`calibration verifier not found at ${verifier}.`);
    process.exitCode = 1;
    return;
  }
  // The single authority for the §7 expectation table (D-014). Same command `make coupons` runs.
  ev("plate_check_start", {});
  const res = await runWithTimeout(PYTHON, [verifier, "--bikar-dir", bikarDir()], {
    timeoutMs: 600_000,
    label: "verify_machine_card",
  });
  if (res.stdout.trim()) console.log(res.stdout.trim());
  if (res.stderr.trim()) console.error(res.stderr.trim());
  ev("plate_check_done", { code: res.code ?? "null" });
  process.exitCode = res.code === 0 ? 0 : 1;
}

async function runRecord(dir: string | undefined): Promise<void> {
  const root = repoRoot();
  if (!root) {
    console.error("could not find the repo root (.claude/gates). Run from inside the 3d-models repo.");
    process.exitCode = 1;
    return;
  }
  const gate = join(root, ".claude", "gates", "prints_gate.py");
  // Default to the gitignored staging area where `--record` scaffolds land; pass docs/prints to
  // check the shipped tree. The gate iterates record dirs under whatever prints dir it is given.
  const prints = dir ? resolve(dir) : recordsDir();
  if (!existsSync(prints)) {
    console.log(`no records dir at ${prints} — nothing scaffolded yet.`);
    console.log("`bambu print send --record` writes drafts there; the shipped tree is docs/prints/.");
    return;
  }
  ev("record_check_start", { prints });
  const res = await runWithTimeout(PYTHON, [gate, prints], {
    timeoutMs: 120_000,
    label: "prints_gate",
    env: { ...process.env, BIKAR_DIR: bikarDir() },
  });
  if (res.stdout.trim()) console.log(res.stdout.trim());
  if (res.stderr.trim()) console.error(res.stderr.trim());
  ev("record_check_done", { code: res.code ?? "null" });
  process.exitCode = res.code === 0 ? 0 : 1;
}

// ---- validate sliced ------------------------------------------------------------------------

interface SlicedOpts {
  expectObjects?: string;
  barePlate?: boolean;
  // commander maps `--no-brim`/`--no-supports`/`--no-raft` onto these (default true; false when the
  // flag is passed), NOT onto noBrim/noSupports/noRaft. `=== false` is "assert this is absent".
  brim?: boolean;
  supports?: boolean;
  raft?: boolean;
  machine?: string;
  nozzle?: string;
  density?: string;
}

/**
 * Realized-truth FEATURE histogram from the (14 MB) gcode without buffering it all: shell one
 * `unzip -p … | grep` so only the `; FEATURE:` lines cross into Node. grep -a treats the gcode as
 * text; the exit code is ignored (grep exits 1 on no match, which is a valid "no features" answer).
 */
async function featureHistogram(threemf: string, gcodeMember: string): Promise<Map<string, number>> {
  const res = await runWithTimeout(
    "sh",
    ["-c", `unzip -p ${JSON.stringify(threemf)} ${JSON.stringify(gcodeMember)} | grep -a -oE '^; FEATURE: .+'`],
    { timeoutMs: 120_000, label: "gcode_features" },
  );
  const hist = new Map<string, number>();
  for (const line of res.stdout.split("\n")) {
    const m = line.match(/^; FEATURE: (.+?)\s*$/);
    const name = m?.[1];
    if (!name) continue;
    hist.set(name, (hist.get(name) ?? 0) + 1);
  }
  return hist;
}

/** Sum realized feature occurrences whose name starts with any keyword (Brim/Support/Raft). */
function realizedCount(hist: Map<string, number>, keyword: string): number {
  let n = 0;
  for (const [name, count] of hist) if (name.startsWith(keyword)) n += count;
  return n;
}

function fmtDuration(seconds: number): string {
  const s = Math.round(seconds);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  return h > 0 ? `${h}h ${m}m` : `${m}m ${s % 60}s`;
}

/** Grams from filament length via a real density (the slice ships 0 — see the header constants). */
function deriveGrams(usedM: number, density: number): number {
  const area = Math.PI * (FILAMENT_DIAMETER_MM / 2) ** 2; // mm²
  const volMm3 = usedM * 1000 * area;
  return (volMm3 / 1000) * density; // cm³ × g/cm³
}

async function runSliced(threemf: string, opts: SlicedOpts): Promise<void> {
  const abs = resolve(threemf);
  if (!existsSync(abs)) {
    console.error(`no such file: ${threemf}`);
    process.exitCode = 2;
    return;
  }
  if (extname(abs).toLowerCase() !== ".3mf") {
    console.error(`validate sliced gates a sliced plate: expected a .3mf, got '${extname(abs)}'.`);
    process.exitCode = 2;
    return;
  }

  const members = await listMembers(abs);
  if (members.length === 0) {
    console.error(`could not read ${threemf} as a .3mf (unzip found no members). Is it sliced/valid?`);
    process.exitCode = 2;
    return;
  }
  const plateJsonName = members.find((m) => /Metadata\/plate_\d+\.json$/.test(m));
  const gcodeName = members.find((m) => /Metadata\/plate_\d+\.gcode$/.test(m));
  const hasGcode = Boolean(gcodeName);

  ev("sliced_check_start", { file: abs });

  // --- header (project_settings.config) ---
  let printerModel = "?";
  let nozzles: string[] = [];
  let brimType = "?";
  let enableSupport = "?";
  let raftLayers = "?";
  const settingsRaw = await readMember(abs, "Metadata/project_settings.config");
  if (settingsRaw) {
    try {
      const s = JSON.parse(settingsRaw);
      printerModel = String(s.printer_model ?? "?");
      nozzles = Array.isArray(s.nozzle_diameter) ? s.nozzle_diameter.map(String) : [];
      brimType = String(s.brim_type ?? "?");
      enableSupport = String(s.enable_support ?? "?");
      raftLayers = String(s.raft_layers ?? "?");
    } catch {
      console.error("warning: project_settings.config present but not parseable JSON.");
    }
  }

  // --- object count (plate_N.json bbox_objects) + skipped check (slice_info.config) ---
  let objectCount: number | null = null;
  if (plateJsonName) {
    const pj = await readMember(abs, plateJsonName);
    if (pj) {
      try {
        objectCount = (JSON.parse(pj).bbox_objects ?? []).length;
      } catch {
        /* leave null; reported below */
      }
    }
  }
  const sliceInfoRaw = (await readMember(abs, "Metadata/slice_info.config")) ?? "";
  const skippedObjects = [...sliceInfoRaw.matchAll(/<object[^>]*\bname="([^"]*)"[^>]*\bskipped="true"/g)].map(
    (m) => m[1],
  );

  // --- estimates (slice_info.config) ---
  const predMatch = sliceInfoRaw.match(/key="prediction"\s+value="(\d+(?:\.\d+)?)"/);
  const predictionS = predMatch ? Number(predMatch[1]) : null;
  const usedM = [...sliceInfoRaw.matchAll(/used_m="(\d+(?:\.\d+)?)"/g)].reduce((a, m) => a + Number(m[1]), 0);
  const density = opts.density ? Number(opts.density) : DEFAULT_PLA_DENSITY;
  const grams = usedM > 0 ? deriveGrams(usedM, density) : 0;

  // --- realized toolpath features (gcode) ---
  const hist = hasGcode ? await featureHistogram(abs, gcodeName!) : new Map<string, number>();
  const brimRealized = realizedCount(hist, "Brim");
  const supportRealized = realizedCount(hist, "Support");
  const raftRealized = realizedCount(hist, "Raft");

  // --- slicer warnings (from the sidecar `bambu slice` writes; classified vs the by-design manifest) ---
  const sidecar = readSidecar(abs);
  const warnClass = sidecar ? classifyWarnings(sidecar.warnings, loadManifest()) : null;

  // ---- report (always) ----
  console.log(`sliced plate: ${abs}`);
  console.log(`  printer   : ${printerModel}  nozzle ${nozzles.length ? nozzles.join(",") : "?"} mm`);
  console.log(`  objects   : ${objectCount ?? "?"}`);
  console.log(
    `  brim/supp/raft (setting): brim_type=${brimType} enable_support=${enableSupport} raft_layers=${raftLayers}`,
  );
  if (hasGcode) {
    console.log(`  brim/supp/raft (realized): Brim=${brimRealized} Support=${supportRealized} Raft=${raftRealized}`);
  } else {
    console.log(`  brim/supp/raft (realized): (no gcode member — settings only)`);
  }
  if (predictionS !== null) console.log(`  time      : ${fmtDuration(predictionS)} (${predictionS}s predicted)`);
  if (usedM > 0) {
    console.log(
      `  filament  : ${usedM.toFixed(2)} m → ~${grams.toFixed(0)} g PLA [derived @ ${density} g/cm³, Ø${FILAMENT_DIAMETER_MM} mm; slice ships 0 g]`,
    );
  }
  if (warnClass) {
    console.log(
      `  warnings  : ${sidecar!.warnings.length} captured — ${warnClass.expected.length} expected, ${warnClass.unexpected.length} unexpected` +
        (sidecar!.studio_version ? ` (Studio ${sidecar!.studio_version})` : ""),
    );
  } else {
    console.log(`  warnings  : (no sidecar — re-slice with \`bambu slice\` to capture; see ${basename(sidecarPath(abs))})`);
  }

  // ---- assertions ----
  const failures: string[] = [];

  // Always-on: a silently dropped/skipped object is never acceptable (the c2-assembly K1 footgun).
  if (skippedObjects.length > 0) {
    failures.push(`slicer SKIPPED ${skippedObjects.length} object(s): ${skippedObjects.join(", ")}`);
  }

  // Always-on: an UNEXPECTED slicer warning (one no by-design manifest rule covers) is never
  // acceptable to ship — it is exactly what Studio would warn about before a print (#52).
  if (warnClass) {
    for (const w of warnClass.unexpected) {
      failures.push(`UNEXPECTED slicer warning [${w.severity}] ${w.object ?? "(plate)"}: ${w.message}`);
    }
  }

  if (opts.expectObjects !== undefined) {
    const want = Number(opts.expectObjects);
    if (objectCount === null) failures.push(`--expect-objects ${want}: could not read object count`);
    else if (objectCount !== want) failures.push(`--expect-objects ${want}: got ${objectCount}`);
  }

  const wantNoBrim = opts.brim === false || Boolean(opts.barePlate);
  const wantNoSupports = opts.supports === false || Boolean(opts.barePlate);
  const wantNoRaft = opts.raft === false || Boolean(opts.barePlate);
  // Realized-truth is the fail condition; the setting corroborates but the toolpath is what prints.
  if (wantNoBrim) {
    if (!hasGcode) failures.push("--no-brim: no gcode member to check realized toolpath");
    else if (brimRealized > 0) failures.push(`--no-brim: ${brimRealized} Brim feature(s) in the gcode`);
    else if (brimType !== "no_brim") failures.push(`--no-brim: no brim toolpath, but brim_type=${brimType} (setting)`);
  }
  if (wantNoSupports) {
    if (!hasGcode) failures.push("--no-supports: no gcode member to check realized toolpath");
    else if (supportRealized > 0) failures.push(`--no-supports: ${supportRealized} Support feature(s) in the gcode`);
    else if (enableSupport !== "0")
      failures.push(`--no-supports: no support toolpath, but enable_support=${enableSupport} (setting)`);
  }
  if (wantNoRaft) {
    if (!hasGcode) failures.push("--no-raft: no gcode member to check realized toolpath");
    else if (raftRealized > 0) failures.push(`--no-raft: ${raftRealized} Raft feature(s) in the gcode`);
    else if (raftLayers !== "0") failures.push(`--no-raft: no raft toolpath, but raft_layers=${raftLayers} (setting)`);
  }

  if (opts.machine !== undefined && !printerModel.toLowerCase().includes(opts.machine.toLowerCase())) {
    failures.push(`--machine ${opts.machine}: printer_model is '${printerModel}'`);
  }
  if (opts.nozzle !== undefined) {
    const bad = nozzles.filter((d) => Number(d) !== Number(opts.nozzle));
    if (nozzles.length === 0) failures.push(`--nozzle ${opts.nozzle}: could not read nozzle_diameter`);
    else if (bad.length > 0) failures.push(`--nozzle ${opts.nozzle}: nozzle_diameter=[${nozzles.join(",")}]`);
  }

  const asserted =
    opts.expectObjects !== undefined ||
    wantNoBrim ||
    wantNoSupports ||
    wantNoRaft ||
    opts.machine !== undefined ||
    opts.nozzle !== undefined;

  ev("sliced_check_done", { failures: failures.length, asserted });

  if (failures.length > 0) {
    console.error("");
    for (const f of failures) console.error(`FAIL: ${f}`);
    process.exitCode = 1;
    return;
  }
  if (asserted) console.log("\nPASS: sliced plate meets the stated expectations.");
  else if (skippedObjects.length === 0) console.log("\n(informational — pass expectation flags to gate; no objects skipped)");
}

export function registerValidate(program: Command): void {
  const validate = program.command("validate").description("gate a mesh / plate / record before it ships");

  validate
    .command("mesh <model>")
    .description("bikar min-strut/FDM --check on a .bkr source")
    .action(runMesh);

  validate
    .command("plate")
    .description("the 23-rung calibration expectation table (calibration-design §7, D-014)")
    .action(runPlate);

  validate
    .command("record [dir]")
    .description("run the prints gate over a records dir (default: .bambu/records/)")
    .action((dir?: string) => runRecord(dir));

  validate
    .command("sliced <3mf>")
    .description("gate a sliced .3mf: realized brim/support/raft, object count, header; report time/length/grams")
    .option("--expect-objects <n>", "fail unless the plate holds exactly N objects")
    .option("--bare-plate", "shorthand for --no-brim --no-supports --no-raft (the Plate-1 expectation)")
    .option("--no-brim", "fail if any Brim feature is in the realized gcode")
    .option("--no-supports", "fail if any Support feature is in the realized gcode")
    .option("--no-raft", "fail if any Raft feature is in the realized gcode")
    .option("--machine <substr>", "fail unless printer_model contains this (e.g. X2D)")
    .option("--nozzle <d>", "fail unless every nozzle_diameter equals this (e.g. 0.4)")
    .option("--density <g/cm3>", `PLA density for the grams estimate (default ${DEFAULT_PLA_DENSITY})`)
    .action((threemf: string, opts: SlicedOpts) => runSliced(threemf, opts));
}
