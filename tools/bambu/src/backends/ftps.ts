// Backend: first-party FTPS upload to the Bambu printer (the upload half of dispatch, #50).
//
// Why this exists (extends D-055): the status read went first-party over MQTT because the griches
// MCP never ran end-to-end (`@griches/bambu-mcp` is unpublished, ships no build). Dispatch is the
// same story — it must not depend on a transport we cannot install — so the upload rides a direct
// implicit-FTPS client and the "start print" rides our existing MqttBackend (`print.project_file`).
//
// Bambu LAN FTPS facts this encodes (grounded 2026-09-17 against pybambu `bambu_client.py`
// `ImplicitFTP_TLS`, bambulabs_api `ftp_client.py`, and the basic-ftp AccessOptions docs):
//   - IMPLICIT TLS on port 990 (not explicit/AUTH-TLS on 21). basic-ftp: `secure: "implicit"`.
//   - username `bblp`, password = the 8-char LAN access code (BAMBU_TOKEN). Self-signed device cert
//     → `rejectUnauthorized: false` (trust boundary is the LAN, same as the MQTT path).
//   - Upload to the FTP ROOT as a BARE filename (`STOR <name>.3mf`); NOT /sdcard, NOT /model — the
//     reference clients STOR against the login working directory and subdir uploads are rejected.
//     The `print.project_file` command then references it as `ftp:///<name>.3mf` (three slashes:
//     empty host + /<name> at root). See mqtt.ts `buildProjectFileCommand`.
//   - Data-connection TLS session reuse is REQUIRED by Bambu firmware — basic-ftp reuses the control
//     TLS session on the data socket by default, so we must NOT force a fresh session. The single
//     most common cause of a hung Bambu FTPS transfer is breaking that reuse; we simply don't touch
//     it. Passive mode (basic-ftp default); active mode does not traverse the printer.

import { basename } from "node:path";
import { Client as FtpClient } from "basic-ftp";
import { ev } from "../log.js";
import { loadConfig, type PrinterConfig } from "../config.js";

const FTPS_PORT = 990;
const FTPS_USER = "bblp";

/**
 * The remote name a local plate is uploaded as: the bare basename at the FTP root. Pure so the
 * dispatch dry-run and the `print.project_file` url can be derived + tested without a printer.
 * (A path with directories collapses to its basename — the printer only accepts root uploads.)
 */
export function remoteUploadName(localPath: string): string {
  return basename(localPath);
}

export class FtpsBackend {
  readonly config: PrinterConfig;

  constructor(config: PrinterConfig = loadConfig()) {
    this.config = config;
  }

  /** True when we have enough config to even attempt a connection. */
  configured(): boolean {
    return Boolean(this.config.host && this.config.token);
  }

  /**
   * Upload a local file to the printer's FTP root under its bare basename and return that remote
   * name. Best-effort and self-closing: a wrong code / unreachable host / another-client conflict
   * throws an actionable Error, and the client is always closed. Never logs the token.
   */
  async uploadFile(localPath: string, timeoutMs = 120_000): Promise<string> {
    if (!this.configured()) {
      throw new Error("printer config missing (need PRINTER_HOST / BAMBU_TOKEN)");
    }
    const remote = remoteUploadName(localPath);
    const client = new FtpClient(timeoutMs);
    // basic-ftp's verbose logger would print the FTP dialogue (control commands) — keep it off so
    // credentials/paths never reach stdout. We emit our own structured, secret-free events instead.
    client.ftp.verbose = false;
    ev("ftps_upload_start", { host: this.config.host ?? "", port: FTPS_PORT, remote });
    try {
      await client.access({
        host: this.config.host,
        port: FTPS_PORT,
        user: FTPS_USER,
        password: this.config.token,
        secure: "implicit",
        secureOptions: { rejectUnauthorized: false }, // self-signed device cert; LAN trust boundary
      });
      await client.uploadFrom(localPath, remote);
      ev("ftps_upload_done", { remote });
      return remote;
    } catch (err) {
      throw this.enhance(err as Error);
    } finally {
      client.close();
    }
  }

  /** Turn the opaque FTPS failures into the actions that fix them (no secret in the message). */
  private enhance(err: Error): Error {
    const msg = err.message || String(err);
    if (/ECONNREFUSED|ETIMEDOUT|EHOSTUNREACH|timeout/i.test(msg)) {
      return new Error(
        `FTPS upload to ${this.config.host}:${FTPS_PORT} failed: ${msg}. Check the printer is on the ` +
          `LAN and Developer Mode / LAN-only is ON (surfaces FTP). Verify host with \`bambu setup doctor\`.`,
      );
    }
    if (/530|login|authentic/i.test(msg)) {
      return new Error(
        `FTPS login refused: ${msg}. The access code (BAMBU_TOKEN) is likely wrong or was rotated — ` +
          `re-read it from the printer screen and re-run \`bambu setup mcp\`.`,
      );
    }
    return err;
  }
}
