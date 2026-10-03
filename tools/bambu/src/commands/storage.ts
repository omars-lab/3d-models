// `bambu storage` — what is on the printer's storage card, and clearing old plates off it.
//   show       : card in or not, free space, from the status report (read-only, MQTT)
//   list [dir] : the files in one folder on the card, the top by default (read-only, FTPS)
//   rm <name…> : delete plate files from the card's top (asks first, or --yes)
//
// Added 2026-10-03 after the sheets-04b send failed at the upload with no card in the printer
// (docs/issues/first-party-dispatch.md). Which names `rm` may delete is storage.ts `rmRefusal`: only
// .3mf plates at the top, where `print send` puts them, never the printer's own folders, never the
// file it is printing from.

import { Command } from "commander";
import { FtpsBackend } from "../backends/ftps.js";
import { MqttBackend, type PrinterStatus } from "../backends/mqtt.js";
import { loadConfig, type PrinterConfig } from "../config.js";
import { confirm } from "../prompt.js";
import { fmtKb, readStorage, renderStorage, rmRefusal } from "../storage.js";

function requireConfigured(cfg: PrinterConfig): void {
  if (!cfg.host || !cfg.serial || !cfg.token) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (env, .mcp.json, or the repo .env with its .env.keys).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

async function readFrame(cfg: PrinterConfig): Promise<PrinterStatus> {
  const mqtt = new MqttBackend(cfg);
  try {
    await mqtt.connect();
    return await mqtt.requestStatus();
  } finally {
    await mqtt.close();
  }
}

export function registerStorage(program: Command): void {
  const storage = program.command("storage").description("the printer's storage card: space, files, clearing old plates");

  storage
    .command("show")
    .description("is a storage card in, and how much room it has (read-only, from the status report)")
    .action(async () => {
      const cfg = loadConfig();
      requireConfigured(cfg);
      try {
        console.log(renderStorage(readStorage(await readFrame(cfg))));
      } catch (err) {
        console.error(`storage show failed: ${(err as Error).message}`);
        process.exitCode = 1;
      }
    });

  storage
    .command("list")
    .description("the files in one folder on the storage card (read-only)")
    .argument("[dir]", "folder on the card", "/")
    .action(async (dir: string) => {
      const cfg = loadConfig();
      requireConfigured(cfg);
      try {
        const entries = await new FtpsBackend(cfg).list(dir);
        if (entries.length === 0) console.log(`(${dir} is empty)`);
        for (const e of entries.sort((a, b) => a.name.localeCompare(b.name))) {
          const when = e.modifiedAt ? e.modifiedAt.toISOString().slice(0, 16).replace("T", " ") : e.rawModifiedAt;
          const size = e.isDirectory ? "folder" : fmtKb(Math.ceil(e.size / 1024));
          console.log(`${size.padStart(9)}  ${when.padEnd(16)}  ${e.name}${e.isDirectory ? "/" : ""}`);
        }
      } catch (err) {
        console.error(`storage list failed: ${(err as Error).message}`);
        process.exitCode = 1;
      }
    });

  storage
    .command("rm")
    .description("delete plate files (.3mf) from the top of the storage card; asks first")
    .argument("<names...>", "file names at the card's top, as `storage list` shows them")
    .option("-y, --yes", "delete without asking", false)
    .action(async (names: string[], opts: { yes?: boolean }) => {
      const cfg = loadConfig();
      requireConfigured(cfg);
      let frame: PrinterStatus | null = null;
      try {
        frame = await readFrame(cfg);
      } catch (err) {
        console.error(`could not read the printer, so cannot tell which file it prints from: ${(err as Error).message}`);
        process.exitCode = 1;
        return;
      }
      const refused = names.map((n) => rmRefusal(n, frame)).filter((r): r is string => r !== null);
      if (refused.length) {
        for (const r of refused) console.error(`✗ ${r}.`);
        process.exitCode = 2;
        return;
      }
      if (!(await confirm(`Delete ${names.join(", ")} from the printer's storage card?`, Boolean(opts.yes)))) {
        console.error("not deleted. Pass --yes (or confirm at a TTY).");
        process.exitCode = 2;
        return;
      }
      const ftps = new FtpsBackend(cfg);
      for (const name of names) {
        try {
          await ftps.remove(name);
          console.log(`deleted ${name}`);
        } catch (err) {
          console.error(`could not delete ${name}: ${(err as Error).message}`);
          process.exitCode = 1;
        }
      }
    });
}
