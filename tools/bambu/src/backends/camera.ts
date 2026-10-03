// Backend: first-party chamber camera snapshot (the camera capability, after status and dispatch).
//
// Why this exists (extends D-055): `bambu status camera` asked the griches MCP for a snapshot, and
// that MCP was never installable (`@griches/bambu-mcp` is unpublished), so the camera never worked.
// The snapshot is small and stable enough to own: one ffmpeg pull of one frame.
//
// Bambu LAN camera facts this encodes (the transport survey, docs/research/bambu-control-transport-
// survey.md: "raw TCP on port 6000 for A1/P1, RTSP (X1/H2 series)"):
//   - X1/H2-class printers serve RTSP over TLS on port 322, path /streaming/live/1, user `bblp`,
//     password = the LAN access code (BAMBU_TOKEN). The X2D answered on 322 on 2026-10-02.
//   - The printer's certificate names its serial (CN=<serial>) and is issued by a Bambu device CA
//     ("BBL Device CA N6-V2" on the X2D) that the printer does not send and Bambu Studio does not
//     ship, so no CA file can verify it. ffmpeg 8 verifies TLS by default and refuses it.
//   - So we pin: `bambu setup camera-pin` saves this printer's own certificate once, and every
//     connection must present exactly that certificate, naming the configured serial. Node does the
//     TLS hop (it can trust a single pinned certificate; ffmpeg cannot) and relays it to ffmpeg over
//     loopback. Why, and what was ruled out: docs/issues/camera-tls-pin.md.
//   - TCP interleaving (`-rtsp_transport tcp`), since the relay carries one TCP stream.
//
// The access code rides in the URL because ffmpeg takes RTSP credentials no other way. It only
// crosses loopback in the clear; the URL is never logged, and every line ffmpeg prints is scrubbed
// of the code before it reaches the operator.

import { createHash, X509Certificate } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { createServer, type AddressInfo, type Socket } from "node:net";
import { join } from "node:path";
import { connect as tlsConnect, type ConnectionOptions, type PeerCertificate } from "node:tls";
import { ev, runWithTimeout } from "../log.js";
import { loadConfig, type PrinterConfig } from "../config.js";
import { repoRoot } from "../paths.js";

export const RTSPS_PORT = 322;
const CAMERA_USER = "bblp";
const CAMERA_PATH = "/streaming/live/1";

/** A stand-in password ffmpeg sends to the relay; the relay re-signs each request with the real one. */
const RELAY_PASSWORD = "relay";

/** The camera URL ffmpeg opens: the loopback relay, plain RTSP, with the stand-in password. The
 *  access code is never in ffmpeg's arguments. */
export function cameraUrl(relayPort: number): string {
  return `rtsp://${CAMERA_USER}:${RELAY_PASSWORD}@127.0.0.1:${relayPort}${CAMERA_PATH}`;
}

const md5 = (s: string) => createHash("md5").update(s).digest("hex");

/**
 * Re-sign an outbound RTSP request's Digest Authorization with the real password. The printer runs
 * LIVE555, whose Digest has no qop: response = MD5(MD5(user:realm:pw):nonce:MD5(method:uri)), over
 * the `uri` as written in the header, which the URL swap has already turned into the printer's.
 * A message without Digest auth passes through unchanged.
 */
export function signDigest(head: string, password: string): string {
  const m = /\r\nAuthorization:\s*Digest ([^\r\n]+)/i.exec(head);
  if (!m) return head;
  const params: Record<string, string> = {};
  for (const p of m[1]!.matchAll(/(\w+)="([^"]*)"/g)) params[p[1]!] = p[2]!;
  const method = head.slice(0, head.indexOf(" "));
  const { username, realm, nonce, uri } = params;
  if (!username || realm === undefined || !nonce || !uri) return head;
  const response = md5(`${md5(`${username}:${realm}:${password}`)}:${nonce}:${md5(`${method}:${uri}`)}`);
  const signed = m[1]!.replace(/response="[^"]*"/, `response="${response}"`);
  return head.replace(m[1]!, signed);
}

/** ffmpeg arguments that write one JPEG frame from the stream to `out`. */
export function snapshotArgs(url: string, out: string): string[] {
  return [
    "-hide_banner",
    "-loglevel", "error",
    "-rtsp_transport", "tcp",
    "-y",
    "-i", url,
    "-frames:v", "1",
    "-q:v", "2",
    out,
  ];
}

/** Replace every occurrence of the access code (raw and URL-encoded) in text meant for a person. */
export function scrub(text: string, token: string | undefined): string {
  if (!token) return text;
  let out = text.split(token).join("****");
  const enc = encodeURIComponent(token);
  if (enc !== token) out = out.split(enc).join("****");
  return out;
}

/** Where this printer's pinned certificate lives: repo-root/.bambu (gitignored), else cwd. */
export function pinPath(serial: string, start = process.cwd()): string {
  return join(repoRoot(start) ?? start, ".bambu", `printer-${serial}.pem`);
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

/** TLS options that accept only the pinned certificate for this serial. `ca` holds the leaf itself
 *  and `allowPartialTrustChain` lets it stand as the trust anchor, so OpenSSL still checks the
 *  signature, dates and key; the identity check then requires the same serial and fingerprint. */
export function pinnedTlsOptions(host: string, serial: string, pem: string): ConnectionOptions {
  const pinned = new X509Certificate(pem).fingerprint256;
  return {
    host,
    port: RTSPS_PORT,
    ca: pem,
    allowPartialTrustChain: true,
    rejectUnauthorized: true,
    checkServerIdentity: (_host: string, cert: PeerCertificate) => {
      if (cert.subject?.CN !== serial) {
        return new Error(`the camera's certificate names ${cert.subject?.CN ?? "no CN"}, not ${serial}`);
      }
      if (cert.fingerprint256 !== pinned) {
        return new Error("the camera's certificate is not the pinned one");
      }
      return undefined;
    },
  };
}

/**
 * Rewrites the URLs in the RTSP messages of one direction of the relay, leaving the interleaved
 * media frames (`$`, channel, 16-bit length, payload) byte for byte. The printer answers any URL that
 * is not its own `rtsps://` one with a 301 to it (seen 2026-10-02), so ffmpeg's loopback URL is
 * swapped for the printer's on the way out and back on the way in. A rewritten body gets its
 * Content-Length recomputed. Bytes are held until a whole message or frame has arrived.
 */
export class RtspRewriter {
  private buf = Buffer.alloc(0);

  constructor(private readonly rewrite: (text: string) => string) {}

  push(chunk: Buffer): Buffer {
    this.buf = Buffer.concat([this.buf, chunk]);
    const out: Buffer[] = [];
    for (;;) {
      if (this.buf.length === 0) break;
      if (this.buf[0] === 0x24) {
        if (this.buf.length < 4) break;
        const end = 4 + this.buf.readUInt16BE(2);
        if (this.buf.length < end) break;
        out.push(this.buf.subarray(0, end));
        this.buf = this.buf.subarray(end);
        continue;
      }
      const headEnd = this.buf.indexOf("\r\n\r\n");
      if (headEnd < 0) break;
      const head = this.buf.subarray(0, headEnd).toString("latin1");
      const length = Number(/\r\ncontent-length:\s*(\d+)/i.exec(head)?.[1] ?? 0);
      const end = headEnd + 4 + length;
      if (this.buf.length < end) break;
      const body = this.rewrite(this.buf.subarray(headEnd + 4, end).toString("latin1"));
      let newHead = this.rewrite(head);
      if (length > 0) newHead = newHead.replace(/(\r\ncontent-length:\s*)\d+/i, `$1${Buffer.byteLength(body, "latin1")}`);
      out.push(Buffer.from(`${newHead}\r\n\r\n${body}`, "latin1"));
      this.buf = this.buf.subarray(end);
    }
    return Buffer.concat(out);
  }
}

/** The two rewrites: outbound, ffmpeg's loopback URL → the printer's and the request re-signed with
 *  the real password; inbound, the printer's URL (with or without its port) → loopback. */
export function urlSwaps(
  host: string,
  relayPort: number,
  password: string,
): { outbound(t: string): string; inbound(t: string): string } {
  const local = `rtsp://127.0.0.1:${relayPort}`;
  const remote = `rtsps://${host}:${RTSPS_PORT}`;
  const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const remoteRe = new RegExp(`rtsps://${esc(host)}(?::${RTSPS_PORT})?(?![\\d.])`, "g");
  return {
    outbound: (t) => signDigest(t.split(local).join(remote), password),
    inbound: (t) => t.replace(remoteRe, local),
  };
}

/** A loopback TCP relay that carries one ffmpeg connection to the printer over the pinned TLS
 *  session. `tlsError` holds the first TLS failure, so a refused pin is reported as that rather
 *  than as ffmpeg's generic "connection reset". */
async function openRelay(host: string, password: string, tlsOpts: ConnectionOptions): Promise<{ port: number; close(): void; tlsError(): Error | null }> {
  let failure: Error | null = null;
  const sockets: Socket[] = [];
  let relayPort = 0;
  const server = createServer((local) => {
    sockets.push(local);
    local.pause();
    const swaps = urlSwaps(host, relayPort, password);
    const out = new RtspRewriter(swaps.outbound);
    const back = new RtspRewriter(swaps.inbound);
    const remote = tlsConnect(tlsOpts, () => {
      ev("camera_tls_pinned", { authorized: remote.authorized });
      local.on("data", (d: Buffer) => remote.write(out.push(d)));
      remote.on("data", (d: Buffer) => local.write(back.push(d)));
      local.resume();
    });
    sockets.push(remote);
    remote.on("error", (err) => {
      failure ??= err;
      local.destroy();
    });
    local.on("error", () => remote.destroy());
    local.on("close", () => remote.destroy());
    remote.on("close", () => local.destroy());
  });
  await new Promise<void>((ok) => server.listen(0, "127.0.0.1", ok));
  relayPort = (server.address() as AddressInfo).port;
  return {
    port: relayPort,
    close: () => {
      for (const s of sockets) s.destroy();
      server.close();
    },
    tlsError: () => failure,
  };
}

export class CameraBackend {
  readonly config: PrinterConfig;

  constructor(config: PrinterConfig = loadConfig()) {
    this.config = config;
  }

  configured(): boolean {
    return Boolean(this.config.host && this.config.token && this.config.serial);
  }

  /**
   * Save the printer's camera certificate as this printer's pin. Fetching a certificate sends no
   * credentials. Returns the path and the certificate's facts for the operator to see.
   */
  async pin(timeoutMs = 10_000): Promise<{ path: string; fingerprint: string; issuer: string; validTo: string }> {
    const { host, serial } = this.config as { host: string; serial: string };
    const res = await runWithTimeout(
      "openssl",
      ["s_client", "-connect", `${host}:${RTSPS_PORT}`, "-showcerts"],
      { timeoutMs, label: "openssl_camera_cert", input: "" },
    );
    const pem = firstPem(res.stdout);
    if (!pem) {
      throw new Error(`no certificate from ${host}:${RTSPS_PORT}${res.timedOut ? " (timed out)" : ""}. Check LAN Mode Liveview is on.`);
    }
    const cert = new X509Certificate(pem);
    const refusal = pinRefusal(cert, serial);
    if (refusal) throw new Error(`not pinned: ${refusal}`);
    const path = pinPath(serial);
    mkdirSync(join(path, ".."), { recursive: true });
    writeFileSync(path, pem);
    ev("camera_pin_saved", { serial, fingerprint: cert.fingerprint256 });
    return { path, fingerprint: cert.fingerprint256, issuer: cert.issuer.replace(/\n/g, ", "), validTo: cert.validTo };
  }

  /**
   * Pull one frame to `out` (JPEG) and return its size in bytes. Read-only: it opens the video
   * stream and nothing else. Throws an actionable, code-free Error on failure.
   */
  async snapshot(out: string, timeoutMs = 20_000): Promise<number> {
    if (!this.configured()) throw new Error("printer config missing (need PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN)");
    const { host, token, serial } = this.config as { host: string; token: string; serial: string };
    const pinFile = pinPath(serial);
    if (!existsSync(pinFile)) {
      throw new Error(`no pinned camera certificate for ${serial} (${pinFile}). Run \`bambu setup camera-pin\` once.`);
    }
    const relay = await openRelay(host, token, pinnedTlsOptions(host, serial, readFileSync(pinFile, "utf8")));
    ev("camera_snapshot_start", { host, port: RTSPS_PORT });
    let res;
    try {
      res = await runWithTimeout("ffmpeg", snapshotArgs(cameraUrl(relay.port), out), {
        timeoutMs,
        label: "ffmpeg_camera",
      });
    } finally {
      relay.close();
    }
    const tlsError = relay.tlsError();
    if (tlsError) {
      throw new Error(
        `the camera's TLS check failed: ${tlsError.message}. If the printer was reset or its certificate ` +
          "renewed, run `bambu setup camera-pin` again; otherwise this is not the pinned printer.",
      );
    }
    const detail = scrub(res.stderr.trim(), token);
    if (res.timedOut) {
      throw new Error(
        `no frame from ${host}:${RTSPS_PORT} within ${timeoutMs / 1000} s. Check LAN Mode Liveview is on ` +
          "in the printer's settings, and that no other viewer holds the stream.",
      );
    }
    if (res.code === null && /ENOENT/.test(detail)) {
      throw new Error("ffmpeg is not on PATH (brew install ffmpeg)");
    }
    if (res.code !== 0 || !existsSync(out)) {
      const hint = /401|Unauthorized/i.test(detail)
        ? " The access code (BAMBU_TOKEN) was refused."
        : /refused|timed out|unreachable/i.test(detail)
          ? ` Check the printer is on the LAN and port ${RTSPS_PORT} is open (LAN Mode Liveview).`
          : "";
      throw new Error(`ffmpeg could not read the camera (exit ${res.code}): ${detail || "(no output)"}.${hint}`);
    }
    const bytes = statSync(out).size;
    ev("camera_snapshot_done", { bytes });
    return bytes;
  }
}
