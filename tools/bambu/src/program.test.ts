import { describe, expect, it } from "vitest";
import type { Command } from "commander";
import { buildProgram } from "./program.js";

// `bambu validate plate build/plates/minis-01.plate.3mf` ignored the file and printed the
// machine-card table's "all 23 rungs match", a pass for a plate it never read (minis-01 run,
// 2026-09-26). Every command now refuses a word it does not take.
function everyCommand(cmd: Command): Command[] {
  return [cmd, ...cmd.commands.flatMap(everyCommand)];
}

function quiet(cmd: Command): Command {
  for (const c of everyCommand(cmd)) {
    c.exitOverride();
    c.configureOutput({ writeErr: () => {}, writeOut: () => {} });
  }
  return cmd;
}

describe("the bambu command tree", () => {
  it("refuses the extra file `validate plate` used to ignore", async () => {
    const program = quiet(buildProgram());
    await expect(
      program.parseAsync(["validate", "plate", "build/plates/minis-01.plate.3mf"], { from: "user" }),
    ).rejects.toMatchObject({ code: "commander.excessArguments" });
  });

  it("refuses extra words on every command, not only that one", () => {
    const loose = everyCommand(buildProgram())
      .filter((c) => (c as unknown as { _allowExcessArguments: boolean })._allowExcessArguments)
      .map((c) => c.name());
    expect(loose).toEqual([]);
  });
});
