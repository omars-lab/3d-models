// `bambu header` — auto-pull the Plate-1 bench-sheet "Profile header" from the printer + a sliced
// `.3mf`, so the operator stops hand-transcribing it (docs/bambu-header-autopull-design.md).
//   header [--plate <file.3mf>] [--json]
//
// It is READ-ONLY and safe to run now — the same first-party MQTT path `status`/`filament` use (one
// `pushall` status request; moves nothing) plus, with --plate, an `unzip` read of the sliced file. It
// prints every machine-known field filled and every genuinely-manual field as the paper's exact blank,
// so the output IS the header. The token never reaches stdout or --json: the builder only ever sees
// the printer's report frame and the .3mf metadata — never the config that holds the secret.

import { Command } from "commander";
import { existsSync } from "node:fs";
import { extname, resolve } from "node:path";
import { MqttBackend } from "../backends/mqtt.js";
import { readPlateMeta } from "../threemf.js";
import { buildHeader, renderHeader } from "../header.js";

function requireConfigured(b: { configured(): boolean }): void {
  if (!b.configured()) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (or .mcp.json).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

interface HeaderOpts {
  plate?: string;
  json?: boolean;
}

async function runHeader(opts: HeaderOpts): Promise<void> {
  // Read the sliced plate first (no printer needed) so a bad path fails before we connect.
  let plate = null;
  if (opts.plate) {
    const abs = resolve(opts.plate);
    if (!existsSync(abs)) {
      console.error(`no such file: ${opts.plate}`);
      process.exitCode = 2;
      return;
    }
    if (extname(abs).toLowerCase() !== ".3mf") {
      console.error(`--plate expects a sliced .3mf, got '${extname(abs)}'. Slice first: bambu slice plate <model>`);
      process.exitCode = 2;
      return;
    }
    plate = await readPlateMeta(abs);
    if (!plate) {
      console.error(`could not read ${opts.plate} as a sliced .3mf (no Metadata/project_settings.config). Is it sliced?`);
      process.exitCode = 2;
      return;
    }
  }

  const mqtt = new MqttBackend();
  requireConfigured(mqtt);
  try {
    await mqtt.connect();
    const frame = await mqtt.requestStatus();
    const header = buildHeader(frame, plate);
    if (opts.json) {
      // The machine object `print send --record` consumes. Contains material/firmware/nozzle only —
      // never the token (the builder never sees config).
      console.log(JSON.stringify(header, null, 2));
    } else {
      console.log(renderHeader(header));
      if (!opts.plate) {
        console.error("\n(slice-side fields are `TODO — pass --plate <plate.3mf>` to fill machine/layer/profile/slicer)");
      }
    }
  } catch (err) {
    console.error(`header failed: ${(err as Error).message}`);
    process.exitCode = 1;
  } finally {
    await mqtt.close();
  }
}

export function registerHeader(program: Command): void {
  program
    .command("header")
    .description("auto-pull the bench-sheet profile header from the printer (+ a sliced --plate .3mf)")
    .option("--plate <file.3mf>", "a sliced plate — fills machine / layer height / profile / slicer version")
    .option("--json", "emit the header as a machine object (what `print send --record` consumes)")
    .action(runHeader);
}
