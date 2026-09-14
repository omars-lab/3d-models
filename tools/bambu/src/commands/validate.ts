// `bambu validate` — gate a mesh / plate / record before it ships.
//   mesh <model.bkr>  : bikar's own min-strut/FDM --check (renders to a throwaway STL)
//   plate             : the 23-rung calibration expectation table (build/verify_machine_card.py)
//   record [dir]      : the prints gate over a records dir (.claude/gates/prints_gate.py)
//
// Every verb shells to the EXISTING authority rather than reimplementing it (robustness-over-ease:
// one code path, never two that can disagree). bikar is the geometry engine and producer of record;
// verify_machine_card.py owns the §7 table (D-014); prints_gate.py owns the record schema (§7). We
// only route to them with the right paths + BIKAR_DIR.

import { Command } from "commander";
import { existsSync } from "node:fs";
import { extname, join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { runWithTimeout, ev } from "../log.js";
import { locateBikarCli, bikarDir } from "../backends/bikar.js";
import { repoRoot, recordsDir } from "../paths.js";

const PYTHON = process.env.PYTHON ?? "python3";

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
}
