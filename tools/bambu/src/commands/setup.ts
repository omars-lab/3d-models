// `bambu setup` — get the machine wired to Claude Code and prove it before any print.
//   doctor  : preflight every dependency and connection, name what's missing
//   mcp     : write/verify the .mcp.json griches entry
//   studio  : detect installed Bambu Studio (stable/beta) and guide install
//
// doctor is the read-only heart of Phase 1: it runs with no printer and reports honestly.

import { Command } from "commander";
import { connect as netConnect } from "node:net";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { loadConfig, mask } from "../config.js";
import { probeStudio } from "../backends/studio-cli.js";
import { appInstalled } from "../backends/applescript.js";
import { McpBackend } from "../backends/mcp.js";
import { runWithTimeout } from "../log.js";

type Status = "PASS" | "WARN" | "FAIL";
interface Check {
  name: string;
  status: Status;
  detail: string;
}

const MQTT_TLS_PORT = 8883;

/** TCP-connect to host:port within a timeout — proof the printer is on the LAN and listening. */
function probeTcp(host: string, port: number, timeoutMs = 4000): Promise<boolean> {
  return new Promise((resolve) => {
    const socket = netConnect({ host, port });
    let done = false;
    const finish = (ok: boolean) => {
      if (done) return;
      done = true;
      socket.destroy();
      resolve(ok);
    };
    socket.setTimeout(timeoutMs);
    socket.once("connect", () => finish(true));
    socket.once("timeout", () => finish(false));
    socket.once("error", () => finish(false));
  });
}

async function hasFfmpeg(): Promise<boolean> {
  const res = await runWithTimeout("ffmpeg", ["-version"], { timeoutMs: 5000, label: "ffmpeg_probe" });
  return res.code === 0;
}

/** Does the repo have a real .mcp.json wiring the bambu server? (searches cwd up to repo root) */
function mcpJsonPresent(cwd = process.cwd()): { present: boolean; path?: string } {
  let dir = cwd;
  for (let i = 0; i < 6; i++) {
    const p = join(dir, ".mcp.json");
    if (existsSync(p)) {
      try {
        const j = JSON.parse(readFileSync(p, "utf8")) as { mcpServers?: Record<string, unknown> };
        if (j.mcpServers && ("bambu" in j.mcpServers || Object.keys(j.mcpServers).length > 0)) {
          return { present: true, path: p };
        }
      } catch {
        /* malformed — treat as absent */
      }
    }
    const parent = join(dir, "..");
    if (parent === dir) break;
    dir = parent;
  }
  return { present: false };
}

async function runDoctor(opts: { probeMcp?: boolean }): Promise<Check[]> {
  const cfg = loadConfig();
  const checks: Check[] = [];

  // 1. Config
  const missing = (["host", "serial", "token"] as const).filter((k) => !cfg[k]);
  checks.push({
    name: "printer config",
    status: missing.length === 0 ? "PASS" : "FAIL",
    detail:
      missing.length === 0
        ? `source=${cfg.source} host=${cfg.host} serial=${cfg.serial} token=${mask(cfg.token)} model=${cfg.model ?? "(unset)"}`
        : `missing ${missing.join(", ")} — set env or .mcp.json (see .mcp.json.example)`,
  });

  // 2. Model = x2d
  checks.push({
    name: "model",
    status: cfg.model ? (cfg.model.toLowerCase() === "x2d" ? "PASS" : "WARN") : "WARN",
    detail: cfg.model
      ? cfg.model.toLowerCase() === "x2d"
        ? "x2d"
        : `set to '${cfg.model}', expected 'x2d' — verify the MCP recognizes this model`
      : "BAMBU_MODEL unset — set to x2d",
  });

  // 3. .mcp.json wiring
  const mcpj = mcpJsonPresent();
  checks.push({
    name: ".mcp.json",
    status: mcpj.present ? "PASS" : "WARN",
    detail: mcpj.present ? mcpj.path! : "no .mcp.json — run `bambu setup mcp` or copy .mcp.json.example",
  });

  // 4. Bambu Studio (slicing)
  const studio = await probeStudio();
  checks.push({
    name: "Bambu Studio",
    status: studio.found ? "PASS" : "WARN",
    detail: studio.found
      ? `${studio.path}${studio.version ? ` (${studio.version})` : ""}`
      : "not found — install stable, fall back to 2.8.x beta if X2D profiles missing",
  });

  // 5. ffmpeg (camera snapshots)
  const ff = await hasFfmpeg();
  checks.push({
    name: "ffmpeg",
    status: ff ? "PASS" : "WARN",
    detail: ff ? "present" : "absent — needed only for `bambu status camera` snapshots",
  });

  // 6. Bambu Connect (GUI fallback)
  const bc = appInstalled("Bambu Connect.app") || appInstalled("BambuConnect.app");
  checks.push({
    name: "Bambu Connect",
    status: bc ? "PASS" : "WARN",
    detail: bc ? "installed" : "absent — optional GUI/AppleScript fallback path",
  });

  // 7. LAN reachability (MQTT TLS port) — only if we have a host
  if (cfg.host) {
    const reachable = await probeTcp(cfg.host, MQTT_TLS_PORT);
    checks.push({
      name: `LAN reach ${cfg.host}:${MQTT_TLS_PORT}`,
      status: reachable ? "PASS" : "FAIL",
      detail: reachable
        ? "MQTT TLS port open — LAN Mode + Developer Mode look enabled"
        : "no connection — check the printer is on, on the LAN, and Developer Mode is ON",
    });
  }

  // 8. MCP handshake (optional; needs config + network)
  if (opts.probeMcp) {
    const mcp = new McpBackend(cfg);
    if (!mcp.configured()) {
      checks.push({ name: "MCP handshake", status: "WARN", detail: "skipped — config incomplete" });
    } else {
      try {
        await mcp.connect();
        const tools = await mcp.listTools();
        checks.push({
          name: "MCP handshake",
          status: tools.length > 0 ? "PASS" : "WARN",
          detail: `griches server up, ${tools.length} tools`,
        });
        await mcp.close();
      } catch (err) {
        checks.push({
          name: "MCP handshake",
          status: "FAIL",
          detail: `could not reach griches MCP: ${(err as Error).message}`,
        });
      }
    }
  }

  return checks;
}

function printChecks(checks: Check[]): number {
  const icon: Record<Status, string> = { PASS: "✓", WARN: "!", FAIL: "✗" };
  const width = Math.max(...checks.map((c) => c.name.length));
  for (const c of checks) {
    console.log(`  ${icon[c.status]} ${c.name.padEnd(width)}  ${c.detail}`);
  }
  const fails = checks.filter((c) => c.status === "FAIL").length;
  const warns = checks.filter((c) => c.status === "WARN").length;
  console.log("");
  console.log(`  ${fails === 0 ? "ready" : "not ready"}: ${fails} fail, ${warns} warn, ${checks.length} checks`);
  return fails;
}

export function registerSetup(program: Command): void {
  const setup = program.command("setup").description("wire the X2D to Claude Code and preflight it");

  setup
    .command("doctor")
    .description("preflight every dependency and connection; names what's missing")
    .option("--probe-mcp", "also attempt a live griches MCP handshake (needs config + network)", false)
    .action(async (opts: { probeMcp: boolean }) => {
      console.log("bambu setup doctor\n");
      const checks = await runDoctor({ probeMcp: opts.probeMcp });
      const fails = printChecks(checks);
      process.exitCode = fails === 0 ? 0 : 1;
    });

  setup
    .command("mcp")
    .description("show the .mcp.json griches entry to add (real file is gitignored — carries the token)")
    .action(() => {
      const cfg = loadConfig();
      const example = {
        mcpServers: {
          bambu: {
            command: "npx",
            args: ["-y", "@griches/bambu-mcp"],
            env: {
              PRINTER_HOST: cfg.host ?? "192.168.1.100",
              BAMBU_SERIAL: cfg.serial ?? "01P00A000000000",
              BAMBU_TOKEN: cfg.token ? mask(cfg.token) : "<lan-access-code>",
              BAMBU_MODEL: cfg.model ?? "x2d",
            },
          },
        },
      };
      console.log("Add this to .mcp.json at the repo root (keep the real file gitignored):\n");
      console.log(JSON.stringify(example, null, 2));
    });

  setup
    .command("studio")
    .description("detect installed Bambu Studio (stable/beta) and where to get it")
    .action(async () => {
      const studio = await probeStudio();
      if (studio.found) {
        console.log(`Bambu Studio: ${studio.path}${studio.version ? ` (${studio.version})` : ""}`);
      } else {
        console.log("Bambu Studio not found.");
        console.log("  Stable:  https://bambulab.com/en/download/studio");
        console.log("  If the X2D or dual-nozzle profiles are missing, install the 2.8.x beta alongside.");
      }
    });
}
