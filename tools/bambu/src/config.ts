// Printer + tooling configuration resolution.
//
// Config precedence (first wins): process env  →  .mcp.json (griches "bambu" server env block)
//   →  built-in defaults. The real .mcp.json is gitignored (carries the LAN token); a committed
//   .mcp.json.example documents the shape. We read the SAME env block the MCP itself reads, so
//   the CLI and the MCP never disagree about which printer they're talking to.

import { readFileSync } from "node:fs";
import { join } from "node:path";

export interface PrinterConfig {
  host?: string; // PRINTER_HOST — LAN IP
  serial?: string; // BAMBU_SERIAL — from the device info screen
  token?: string; // BAMBU_TOKEN — LAN access code / token (secret; never printed in full)
  model?: string; // BAMBU_MODEL — e.g. x2d
  slicerPath?: string; // SLICER_PATH — BambuStudio.app binary
  source: "env" | ".mcp.json" | "none";
}

const ENV_KEYS = {
  host: "PRINTER_HOST",
  serial: "BAMBU_SERIAL",
  token: "BAMBU_TOKEN",
  model: "BAMBU_MODEL",
  slicerPath: "SLICER_PATH",
} as const;

function fromEnv(): Partial<PrinterConfig> {
  const out: Partial<PrinterConfig> = {};
  for (const [field, key] of Object.entries(ENV_KEYS) as [keyof typeof ENV_KEYS, string][]) {
    const v = process.env[key];
    if (v) (out as Record<string, string>)[field] = v;
  }
  return out;
}

/** The griches server's env block inside .mcp.json, if present. Search cwd upward to the repo root. */
function fromMcpJson(startDir: string): Partial<PrinterConfig> {
  let dir = startDir;
  for (let i = 0; i < 6; i++) {
    try {
      const raw = readFileSync(join(dir, ".mcp.json"), "utf8");
      const json = JSON.parse(raw) as {
        mcpServers?: Record<string, { env?: Record<string, string> }>;
      };
      const servers = json.mcpServers ?? {};
      // Prefer a server literally named "bambu"; otherwise the first one carrying PRINTER_HOST.
      const entry =
        servers["bambu"] ??
        Object.values(servers).find((s) => s.env && ENV_KEYS.host in s.env);
      const env = entry?.env;
      if (env) {
        const out: Partial<PrinterConfig> = {};
        for (const [field, key] of Object.entries(ENV_KEYS) as [keyof typeof ENV_KEYS, string][]) {
          if (env[key]) (out as Record<string, string>)[field] = env[key]!;
        }
        return out;
      }
    } catch {
      /* no .mcp.json here — keep walking up */
    }
    const parent = join(dir, "..");
    if (parent === dir) break;
    dir = parent;
  }
  return {};
}

export function loadConfig(cwd = process.cwd()): PrinterConfig {
  const env = fromEnv();
  if (Object.keys(env).length > 0) return { ...env, source: "env" };
  const mcp = fromMcpJson(cwd);
  if (Object.keys(mcp).length > 0) return { ...mcp, source: ".mcp.json" };
  return { source: "none" };
}

/** Mask a secret for display: keep the last 4 chars, star the rest. */
export function mask(secret: string | undefined): string {
  if (!secret) return "(unset)";
  if (secret.length <= 4) return "****";
  return "*".repeat(secret.length - 4) + secret.slice(-4);
}
