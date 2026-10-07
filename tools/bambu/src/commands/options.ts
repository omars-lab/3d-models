// `bambu options` — the printer's print options (the checks it runs before and during a print).
//   show                       : each switch on or off, from the status report (read-only, MQTT)
//   set <option> <on|off> [-y] : switch one, the way Bambu Studio does; asks first, then reads it back
//   for-bed <plate> [-y]       : set the two plate switches to fit the plate the bed verdict saw (D-108)
//
// Added 2026-10-07 so the glacier plate's two switches (Foreign Object Detection, Type Detection)
// can be turned off and back on from the CLI. Omar: "yes command that changes settings". The bits,
// the command and why each switch matters: print-options.ts and
// docs/research/2026-10-07-third-party-plates.md. A switch is printer-wide and stays as set for every
// print after it, so `set` changes the printer only on the owner's go, like `print send --yes`.
// `for-bed` is the exception Omar made standing on 2026-10-07 ("can you do this automatically per our
// skill? when you look at plates pre print", D-108): the two plate switches follow the bed verdict.

import { Command } from "commander";
import { MqttBackend, type PrinterStatus } from "../backends/mqtt.js";
import { newestBedPhoto, readVerdict } from "../bed-check.js";
import { loadConfig, type PrinterConfig } from "../config.js";
import { ev } from "../log.js";
import { repoRoot } from "../paths.js";
import { confirm } from "../prompt.js";
import { plateNameOf } from "../send-gate.js";
import {
  buildOptionCommand,
  optionByKey,
  parseOnOff,
  plateSwitchChanges,
  PRINT_OPTIONS,
  readBack,
  renderOptions,
  setRefusal,
  type PlateSwitchChange,
} from "../print-options.js";

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

/** Send each switch, wait out Studio's hold, then read them all back. Exit 1 on any ✗. */
async function applySwitches(mqtt: MqttBackend, changes: PlateSwitchChange[]): Promise<void> {
  for (const { option, on } of changes) {
    ev("options_set", { option: option.key, on: String(on) });
    await mqtt.setPrintOption(buildOptionCommand(option, on));
  }
  await new Promise((r) => setTimeout(r, READ_BACK_AFTER_MS));
  const after = await mqtt.requestStatus();
  for (const { option, on } of changes) {
    const result = readBack(option, on, after);
    ev("options_read_back", { option: option.key, mark: result.mark });
    console.log(`${result.mark} ${result.line}`);
    if (result.mark === "✗") process.exitCode = 1;
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
        await applySwitches(mqtt, [{ option, on }]);
      } catch (err) {
        console.error(`options set failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mqtt.close();
      }
    });

  options
    .command("for-bed")
    .description("set Foreign Object and Type Detection to fit the plate the newest bed verdict saw: off for a non-Bambu plate, on for Bambu's")
    .argument("<plate>", "plate name or its .3mf, as for `bed verdict`")
    .option("-y, --yes", "switch without asking (the send-plate skill's standing go, D-108)", false)
    .action(async (plate: string, opts: { yes?: boolean }) => {
      const name = plateNameOf(plate);
      const photo = newestBedPhoto(repoRoot() ?? process.cwd(), name);
      const verdict = photo ? readVerdict(photo.path) : null;
      if (!photo || !verdict || verdict.sha256 !== photo.sha256) {
        console.error(`✗ no verdict on the newest bed photo of ${name}. Look at the photo and write one first: bambu bed verdict ${name} …`);
        process.exitCode = 2;
        return;
      }
      const nonBambu = verdict.non_bambu === true;
      const which = nonBambu ? "a non-Bambu plate" : "a Bambu plate";
      const cfg = loadConfig();
      requireConfigured(cfg);
      const mqtt = new MqttBackend(cfg);
      try {
        await mqtt.connect();
        const before = await mqtt.requestStatus();
        const changes = plateSwitchChanges(before, nonBambu);
        if (changes.length === 0) {
          console.log(`✓ the bed verdict saw ${which}; Foreign Object and Type Detection already fit it. Nothing sent.`);
          return;
        }
        const refused = changes.map((c) => setRefusal(c.option, c.on, before)).find((r) => r !== null);
        if (refused) {
          console.error(`✗ ${refused}.`);
          process.exitCode = 2;
          return;
        }
        const list = changes.map((c) => `${c.option.label} ${c.on ? "on" : "off"}`).join(", ");
        if (!(await confirm(`The bed verdict saw ${which}. Switch ${list}?`, Boolean(opts.yes)))) {
          console.error("not switched. Pass --yes (or confirm at a TTY).");
          process.exitCode = 2;
          return;
        }
        await applySwitches(mqtt, changes);
      } catch (err) {
        console.error(`options for-bed failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mqtt.close();
      }
    });
}
