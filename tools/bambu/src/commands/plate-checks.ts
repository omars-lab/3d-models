// `bambu plate-checks run <plate.3mf>` runs the plate checks list on one plate, the same lines the
// send prints; `bambu plate-checks verify` is the list's own check (make validate-plate-checks).

import { Command } from "commander";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { plateRecipePath } from "../color-at-send.js";
import { repoRoot } from "../paths.js";
import { PLATE_CHECKS_FILE, loadPlateChecks, runPlateChecks, verifyPlateChecks } from "../plate-checks.js";
import { plateNameOf } from "../send-gate.js";

/** Run every check that applies to the plate at `abs` and print one line each (to stderr, beside
 * the send's other checks). True when all passed. A list that cannot be read is one ✗ line. */
export function reportPlateChecks(abs: string, root: string): boolean {
  let checks;
  try {
    checks = loadPlateChecks(root);
  } catch (err) {
    console.error(`✗ plate checks: ${PLATE_CHECKS_FILE} could not be read (${(err as Error).message}).`);
    return false;
  }
  const results = runPlateChecks(checks, abs, plateRecipePath(plateNameOf(abs), root), root);
  for (const r of results) {
    console.error(`${r.mark} ${r.line}.`);
    for (const d of r.detail) console.error(`    ${d}`);
  }
  return results.every((r) => r.ok);
}

export function registerPlateChecks(program: Command): void {
  const pc = program
    .command("plate-checks")
    .description(`the checks every plate must pass before a send (${PLATE_CHECKS_FILE})`);

  pc.command("run <plate3mf>")
    .description("run every check that applies to one sliced plate, as the send does")
    .action((plate3mf: string) => {
      const abs = resolve(plate3mf);
      if (!existsSync(abs)) {
        console.error(`no such file: ${plate3mf}`);
        process.exitCode = 2;
        return;
      }
      if (!reportPlateChecks(abs, repoRoot() ?? process.cwd())) process.exitCode = 1;
    });

  pc.command("verify")
    .description("check the list itself: every entry reads, every file it names is in the repo")
    .action(() => {
      const root = repoRoot() ?? process.cwd();
      const problems = verifyPlateChecks(root);
      if (problems.length > 0) {
        for (const p of problems) console.error(`FAIL: ${p}`);
        process.exitCode = 1;
        return;
      }
      console.log(`PASS: ${loadPlateChecks(root).length} plate checks read, every file they name is there.`);
    });
}
