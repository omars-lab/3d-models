#!/usr/bin/env -S npx tsx
// `bambu` — contextualized CLI companion to the setup-bambu-x2d skill.
//
// Command groups (the help IS the docs): setup, status, slice, print, validate. Status rides our
// own first-party MQTT backend (D-055); slicing shells to the BambuStudio CLI; the remaining
// control/camera verbs still route through the griches MCP until they are ported. See
// .claude/skills/setup-bambu-x2d/SKILL.md for when/why and .claude/plans/binary-tickling-kay.md
// for the build sequencing.

import { Command } from "commander";
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { registerSetup } from "./commands/setup.js";
import { registerStatus } from "./commands/status.js";
import { registerFilament } from "./commands/filament.js";
import { registerHeader } from "./commands/header.js";
import { registerSlice } from "./commands/slice.js";
import { registerPrint } from "./commands/print.js";
import { registerValidate } from "./commands/validate.js";
import { dumpFlags } from "./flags.js";

const program = new Command();

program
  .name("bambu")
  .description(
    [
      "Drive the Bambu Lab X2D from Claude Code.",
      "",
      "Layers: this CLI (our verbs) → first-party MQTT (status) / griches MCP (control) → printer.",
      "Slicing shells to the BambuStudio CLI; GUI-only actions fall back to AppleScript.",
      "Full control needs Developer Mode ON on the printer (opens MQTT/FTP on the LAN).",
    ].join("\n"),
  )
  .version("0.1.0");

registerSetup(program);
registerStatus(program);
registerFilament(program);
registerHeader(program);
registerSlice(program);
registerPrint(program);
registerValidate(program);

// The CLI describes its own flag surface (see src/flags.ts). Hidden: it is a maintenance verb for the
// gate/make target, not a user-facing one, so it stays out of --help. `--write` regenerates the
// checked-in FLAGS.md next to this module; without it the reference prints to stdout for inspection.
program
  .command("dump-flags", { hidden: true })
  .description("Emit the generated flag reference (maintenance verb for `make bambu-flags`).")
  .option("--write", "write FLAGS.md next to the CLI instead of printing to stdout")
  .action((opts: { write?: boolean }) => {
    const body = dumpFlags(program);
    if (opts.write) {
      const out = fileURLToPath(new URL("../FLAGS.md", import.meta.url));
      writeFileSync(out, body);
      console.error(`wrote ${out}`);
    } else {
      process.stdout.write(body);
    }
  });

program.parseAsync(process.argv).catch((err) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
