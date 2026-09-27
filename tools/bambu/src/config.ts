// Printer + tooling configuration resolution.
//
// Config precedence (first wins): process env  →  .mcp.json (griches "bambu" server env block)
//   →  the repo's encrypted .env  →  built-in defaults. The real .mcp.json is gitignored (carries
//   the LAN token); a committed .mcp.json.example documents the shape. We read the SAME env block
//   the MCP itself reads, so the CLI and the MCP never disagree about which printer they're talking
//   to. The .env is checked in with dotenvx-encrypted values and decrypted with the private key in
//   the gitignored .env.keys beside it: the printer config sat there while every command said "Not
//   configured", because nothing read it (2026-09-26).

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
// A CommonJS package: node's ESM loader cannot see its named exports (`bin/bambu` failed on
// `{ parse }` while vitest passed), so take the default export.
import dotenvx from "@dotenvx/dotenvx";

const parseDotenv = dotenvx.parse;

export interface PrinterConfig {
  host?: string; // PRINTER_HOST — LAN IP
  serial?: string; // BAMBU_SERIAL — from the device info screen
  token?: string; // BAMBU_TOKEN — LAN access code / token (secret; never printed in full)
  model?: string; // BAMBU_MODEL — e.g. x2d
  slicerPath?: string; // SLICER_PATH — BambuStudio.app binary
  source: "env" | ".mcp.json" | ".env" | "none";
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

/** The printer keys from the nearest `.env` (cwd upward), decrypted with the `DOTENV_PRIVATE_KEY`
 *  in the `.env.keys` beside it or in the environment. A value that stays encrypted (no key, or the
 *  wrong one) is left out rather than passed on as a host or token. */
export function fromDotenv(startDir: string, env: NodeJS.ProcessEnv = process.env): Partial<PrinterConfig> {
  let dir = startDir;
  for (let i = 0; i < 6; i++) {
    const file = join(dir, ".env");
    if (existsSync(file)) {
      let privateKey = env.DOTENV_PRIVATE_KEY;
      const keysFile = join(dir, ".env.keys");
      if (!privateKey && existsSync(keysFile)) {
        privateKey = parseDotenv(readFileSync(keysFile, "utf8"), { processEnv: {} }).DOTENV_PRIVATE_KEY;
      }
      let parsed: Record<string, string>;
      try {
        parsed = parseDotenv(readFileSync(file, "utf8"), { processEnv: {}, privateKey });
      } catch {
        return {};
      }
      const out: Partial<PrinterConfig> = {};
      for (const [field, key] of Object.entries(ENV_KEYS) as [keyof typeof ENV_KEYS, string][]) {
        const v = parsed[key];
        if (v && !v.startsWith("encrypted:")) (out as Record<string, string>)[field] = v;
      }
      return out;
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
  const dot = fromDotenv(cwd);
  if (Object.keys(dot).length > 0) return { ...dot, source: ".env" };
  return { source: "none" };
}

/** Mask a secret for display: keep the last 4 chars, star the rest. */
export function mask(secret: string | undefined): string {
  if (!secret) return "(unset)";
  if (secret.length <= 4) return "****";
  return "*".repeat(secret.length - 4) + secret.slice(-4);
}
