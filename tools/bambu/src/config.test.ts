import { describe, expect, it } from "vitest";
import { mkdirSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import dotenvx from "@dotenvx/dotenvx";
import { fromDotenv } from "./config.js";

// The printer config sat encrypted in the repo .env while every printer command said "Not
// configured", because bambu read only the environment and .mcp.json (2026-09-26).
async function encryptedRepo(): Promise<string> {
  const dir = mkdtempSync(join(tmpdir(), "bambu-config-test-"));
  const opts = { path: join(dir, ".env"), envKeysFile: join(dir, ".env.keys"), noNative: true, noArmor: true, no1Password: true, noBitwarden: true };
  await dotenvx.set("PRINTER_HOST", "10.0.0.9", opts);
  await dotenvx.set("BAMBU_SERIAL", "SERIAL123", opts);
  await dotenvx.set("BAMBU_TOKEN", "tok-5678", opts);
  return dir;
}

describe("fromDotenv", () => {
  it("decrypts the printer keys with the .env.keys beside the .env", async () => {
    const dir = await encryptedRepo();
    expect(readFileSync(join(dir, ".env"), "utf8")).toContain("encrypted:");
    expect(fromDotenv(dir, {})).toEqual({ host: "10.0.0.9", serial: "SERIAL123", token: "tok-5678" });
  });

  it("finds the .env from a subdirectory, as bambu runs from tools/bambu", async () => {
    const dir = await encryptedRepo();
    const sub = join(dir, "tools", "bambu");
    mkdirSync(sub, { recursive: true });
    expect(fromDotenv(sub, {}).host).toBe("10.0.0.9");
  });

  it("leaves a key out rather than pass on a value it could not decrypt", async () => {
    const dir = await encryptedRepo();
    rmSync(join(dir, ".env.keys"));
    expect(fromDotenv(dir, {})).toEqual({});
  });
});
