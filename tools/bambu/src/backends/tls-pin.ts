// The printer's pinned TLS certificate, shared by every connection that carries the access code:
// MQTT (8883), FTPS (990) and the camera (322).
//
// The printer's certificate names its serial (CN=<serial>) and is issued by a Bambu device CA
// ("BBL Device CA N6-V2" on the X2D) that Bambu Studio does not ship, so no CA file can verify it.
// So we pin: `bambu setup printer-pin` saves this printer's own certificate once, and every
// connection must present exactly that certificate, naming the configured serial. All three ports
// present the same certificate (measured on the X2D 2026-10-04: same fingerprint; 8883 and 990
// also send the N6-V2 intermediate, 322 sends the certificate alone). Why, and what was ruled out:
// docs/issues/camera-tls-pin.md.

import { X509Certificate } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import type { PeerCertificate } from "node:tls";
import { ev, runWithTimeout } from "../log.js";
import { repoRoot } from "../paths.js";

/** The port the pin is fetched from: MQTT, which answers whenever LAN mode is on (the camera's 322
 *  needs LAN Mode Liveview as well). */
export const PIN_FETCH_PORT = 8883;

/** Where this printer's pinned certificate lives: repo-root/.bambu (gitignored), else cwd. */
export function pinPath(serial: string, start = process.cwd()): string {
  return join(repoRoot(start) ?? start, ".bambu", `printer-${serial}.pem`);
}

/** The pinned certificate for `serial`, or an Error saying how to make one. */
export function readPin(serial: string, start = process.cwd()): string {
  const file = pinPath(serial, start);
  if (!existsSync(file)) {
    throw new Error(`no pinned printer certificate for ${serial} (${file}). Run \`bambu setup printer-pin\` once.`);
  }
  return readFileSync(file, "utf8");
}

/** The first PEM certificate block in `text` (openssl s_client output), or null. */
export function firstPem(text: string): string | null {
  const m = /-----BEGIN CERTIFICATE-----[\s\S]+?-----END CERTIFICATE-----/.exec(text);
  return m ? `${m[0]}\n` : null;
}

/** Why `cert` may not be pinned for `serial`, or null when it may. The certificate must name the
 *  serial and be in date; anything else is a different device or a stale capture. */
export function pinRefusal(cert: X509Certificate, serial: string, now = new Date()): string | null {
  const cn = /(?:^|\n)CN=([^\n]+)/.exec(cert.subject)?.[1];
  if (cn !== serial) return `the certificate names ${cn ?? "no CN"}, not the configured serial ${serial}`;
  if (now < new Date(cert.validFrom) || now > new Date(cert.validTo)) {
    return `the certificate is out of date (valid ${cert.validFrom} to ${cert.validTo})`;
  }
  return null;
}

/** TLS options that accept only the pinned certificate for this serial; the caller adds host and
 *  port. `ca` holds the certificate itself and `allowPartialTrustChain` lets it stand as the trust
 *  anchor, so OpenSSL still checks the signature, dates and key, whatever intermediates the server
 *  sends; the identity check then requires the same serial and fingerprint. */
export interface PinnedTls {
  ca: string;
  allowPartialTrustChain: boolean;
  rejectUnauthorized: true;
  checkServerIdentity: (host: string, cert: PeerCertificate) => Error | undefined;
}

export function pinnedTlsOptions(serial: string, pem: string): PinnedTls {
  const pinned = new X509Certificate(pem).fingerprint256;
  return {
    ca: pem,
    allowPartialTrustChain: true,
    rejectUnauthorized: true,
    checkServerIdentity: (_host: string, cert: PeerCertificate) => {
      if (cert.subject?.CN !== serial) {
        return new Error(`the printer's certificate names ${cert.subject?.CN ?? "no CN"}, not ${serial}`);
      }
      if (cert.fingerprint256 !== pinned) {
        return new Error("the printer's certificate is not the pinned one");
      }
      return undefined;
    },
  };
}

/** The line to show when a pinned connection is refused. */
export function pinFailureHint(): string {
  return "If the printer was reset or its certificate renewed, run `bambu setup printer-pin` again; " +
    "otherwise this is not the pinned printer.";
}

/**
 * Fetch the printer's certificate and save it as this printer's pin. Fetching a certificate sends
 * no credentials. Returns the path and the certificate's facts for the operator to see.
 */
export async function savePin(
  host: string,
  serial: string,
  timeoutMs = 10_000,
): Promise<{ path: string; fingerprint: string; issuer: string; validTo: string }> {
  const res = await runWithTimeout(
    "openssl",
    ["s_client", "-connect", `${host}:${PIN_FETCH_PORT}`, "-showcerts"],
    { timeoutMs, label: "openssl_printer_cert", input: "" },
  );
  const pem = firstPem(res.stdout);
  if (!pem) {
    throw new Error(`no certificate from ${host}:${PIN_FETCH_PORT}${res.timedOut ? " (timed out)" : ""}. Check LAN mode is on.`);
  }
  const cert = new X509Certificate(pem);
  const refusal = pinRefusal(cert, serial);
  if (refusal) throw new Error(`not pinned: ${refusal}`);
  const path = pinPath(serial);
  mkdirSync(join(path, ".."), { recursive: true });
  writeFileSync(path, pem);
  ev("printer_pin_saved", { serial, fingerprint: cert.fingerprint256 });
  return { path, fingerprint: cert.fingerprint256, issuer: cert.issuer.replace(/\n/g, ", "), validTo: cert.validTo };
}
