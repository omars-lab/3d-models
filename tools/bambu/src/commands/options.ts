// `bambu options` — the printer's print options (the checks it runs before and during a print).
//   show                       : each switch on or off, from the status report (read-only, MQTT)
//   set <option> <on|off> [-y] : switch one, the way Bambu Studio does; asks first, then reads it back
//
// Added 2026-10-07 so the glacier plate's two switches (Foreign Object Detection, Type Detection)
// can be turned off and back on from the CLI. Omar: "yes command that changes settings". The bits,
// the command and why each switch matters: print-options.ts and
// docs/research/2026-10-07-third-party-plates.md. A switch is printer-wide and stays as set for every
// print after it, so `set` changes the printer only on the owner's go, like `print send --yes`.

import { Command } from "commander";
import { MqttBackend, type PrinterStatus } from "../backends/mqtt.js";
import { loadConfig, type PrinterConfig } from "../config.js";
import { ev } from "../log.js";
import { confirm } from "../prompt.js";
import { buildOptionCommand, optionByKey, parseOnOff, PRINT_OPTIONS, readBack, renderOptions, setRefusal } from "../print-options.js";

/** Only these switch from the CLI; the AI checks are shown, not set (they carry a level). */
export const SETTABLE = ["foreign-object", "plate-type", "plate-alignment", "displacement"] as const;

/** Bambu Studio holds its own value for 3 s after a switch before it trusts the report again. */
const READ_BACK_AFTER_MS = 4000;

function requireConfigured(cfg: PrinterConfig): void {
  if (!cfg.host || !cfg.serial || !cfg.token) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (env, .mcp.json, or the repo .env with its .env.keys).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

export function registerOptions(program: Command): void {
  const options = program.command("options").description("the printer's print options: foreign objects, plate type and alignment, displacement, AI checks");

  options
    .command("show")
    .description("each print option on or off, and what a non-Bambu plate wants (read-only)")
    .option("--json", "print the switches as JSON", false)
    .action(async (opts: { json?: boolean }) => {
      const cfg = loadConfig();
      requireConfigured(cfg);
      const mqtt = new MqttBackend(cfg);
      try {
        await mqtt.connect();
        const frame = await mqtt.requestStatus();
        if (opts.json) {
          const out = PRINT_OPTIONS.map((o) => ({ option: o.key, label: o.label, on: o.read(frame), level: o.level?.(frame) ?? null, supported: o.supported(frame), non_bambu_plate: o.nonBambu }));
          console.log(JSON.stringify(out, null, 2));
        } else {
          console.log(renderOptions(frame));
        }
      } catch (err) {
        console.error(`options show failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mqtt.close();
      }
    });

  options
    .command("set")
    .description(`switch one print option on or off (${SETTABLE.join(", ")}); asks first, then reads it back`)
    .argument("<option>", SETTABLE.join(" | "))
    .argument("<state>", "on | off")
    .option("-y, --yes", "switch without asking", false)
    .action(async (key: string, state: string, opts: { yes?: boolean }) => {
      let option, on: boolean;
      try {
        option = optionByKey(key);
        on = parseOnOff(state);
      } catch (err) {
        console.error(`✗ ${(err as Error).message}`);
        process.exitCode = 2;
        return;
      }
      if (!(SETTABLE as readonly string[]).includes(option.key)) {
        console.error(`✗ ${option.key} is shown, not set, here. Switch it at the printer (Settings > Print Options).`);
        process.exitCode = 2;
        return;
      }
      const cfg = loadConfig();
      requireConfigured(cfg);
      const mqtt = new MqttBackend(cfg);
      try {
        await mqtt.connect();
        const before: PrinterStatus = await mqtt.requestStatus();
        const refused = setRefusal(option, on, before);
        if (refused) {
          console.error(`✗ ${refused}.`);
          process.exitCode = 2;
          return;
        }
        if (option.read(before) === on) {
          console.log(`${option.key} is already ${state}; nothing sent.`);
          return;
        }
        const word = on ? "on" : "off";
        if (!(await confirm(`Switch ${option.label} ${word} on the printer? It stays ${word} for every print after this.`, Boolean(opts.yes)))) {
          console.error("not switched. Pass --yes (or confirm at a TTY).");
          process.exitCode = 2;
          return;
        }
        const cmd = buildOptionCommand(option, on);
        ev("options_set", { option: option.key, on: String(on) });
        await mqtt.setPrintOption(cmd);
        await new Promise((r) => setTimeout(r, READ_BACK_AFTER_MS));
        const after = await mqtt.requestStatus();
        const result = readBack(option, on, after);
        ev("options_read_back", { option: option.key, mark: result.mark });
        console.log(`${result.mark} ${result.line}`);
        if (result.mark === "✗") process.exitCode = 1;
      } catch (err) {
        console.error(`options set failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mqtt.close();
      }
    });
}
