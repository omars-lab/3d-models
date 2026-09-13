// Placeholder command groups for later phases, registered now so `bambu --help` shows the whole
// intended surface (the help IS the documentation). Each stub prints what it WILL do and which
// phase lands it, and exits non-zero so nothing silently no-ops.

import { Command } from "commander";

function notYet(phase: string, what: string): () => void {
  return () => {
    console.error(`not implemented yet — ${what} lands in ${phase}.`);
    console.error("See .claude/plans/binary-tickling-kay.md for sequencing.");
    process.exitCode = 2;
  };
}

export function registerStubs(program: Command): void {
  // `slice` is implemented in commands/slice.ts (phase 2). print/validate remain phase-3 stubs,
  // registered so `bambu --help` shows the whole intended surface (the help IS the documentation).
  const print = program.command("print").description("[phase 3] dispatch + print control (owner-gated)");
  print
    .command("send <plate>")
    .description("[phase 3] dispatch a sliced .3mf via the MCP (confirm-before-send); --record logs it")
    .option("--record", "write a docs/prints/<date>-<slug>/ record")
    .action(notYet("phase 3", "dispatch"));
  print.command("pause").description("[phase 3] pause the running print").action(notYet("phase 3", "print control"));
  print.command("resume").description("[phase 3] resume the running print").action(notYet("phase 3", "print control"));
  print.command("stop").description("[phase 3] stop the running print").action(notYet("phase 3", "print control"));

  const validate = program.command("validate").description("[phase 3] gate a plate/record before it ships");
  validate.command("mesh <model>").description("[phase 3] bikar min-strut/FDM --check").action(notYet("phase 3", "mesh validation"));
  validate
    .command("plate <plate>")
    .description("[phase 3] check against the calibration expectation table (calibration-design §7)")
    .action(notYet("phase 3", "plate validation"));
  validate
    .command("record <dir>")
    .description("[phase 3] confirm a print record passes the prints gate")
    .action(notYet("phase 3", "record validation"));
}
