import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { createHash, X509Certificate } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { connect, createServer, type Server } from "node:tls";
import {
  cameraUrl,
  firstPem,
  pinnedTlsOptions,
  pinRefusal,
  RtspRewriter,
  scrub,
  signDigest,
  snapshotArgs,
  urlSwaps,
} from "./camera.js";

// The camera reaches the printer through a pinned TLS hop (backends/camera.ts). The load-bearing
// case is the refusal: a server showing any certificate but the pinned one, even one naming the same
// serial, must not get a connection. The certificates are made here with openssl, shaped like the
// X2D's: a leaf naming the serial, signed by a CA the server never sends.

const SERIAL = "TESTSERIAL0001";
let dir: string;
const pem: Record<string, string> = {};
const key: Record<string, string> = {};

function ssl(...args: string[]): void {
  execFileSync("openssl", args, { cwd: dir, stdio: "ignore" });
}

/** A CA, and a leaf it signs naming `cn`; returns the leaf's PEM and key. */
function leaf(name: string, cn: string): void {
  ssl("req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", `${name}-ca.key`, "-out", `${name}-ca.pem`,
    "-days", "2", "-subj", `/CN=Test Device CA ${name}`);
  ssl("req", "-newkey", "rsa:2048", "-nodes", "-keyout", `${name}.key`, "-out", `${name}.csr`, "-subj", `/CN=${cn}`);
  ssl("x509", "-req", "-in", `${name}.csr`, "-CA", `${name}-ca.pem`, "-CAkey", `${name}-ca.key`,
    "-CAcreateserial", "-out", `${name}.pem`, "-days", "2");
  pem[name] = readFileSync(join(dir, `${name}.pem`), "utf8");
  key[name] = readFileSync(join(dir, `${name}.key`), "utf8");
}

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), "camera-pin-"));
  leaf("printer", SERIAL);
  leaf("impostor", SERIAL); // same serial, different key and CA
  leaf("other", "SOMEOTHERSERIAL");
});

afterAll(() => rmSync(dir, { recursive: true, force: true }));

/** Serve `name`'s leaf (no chain) and try a pinned connection; resolve to "ok" or the error. */
async function handshake(served: string, pinned: string): Promise<string> {
  const server: Server = createServer({ cert: pem[served], key: key[served] }, (s) => s.end());
  await new Promise<void>((ok) => server.listen(0, "127.0.0.1", ok));
  const port = (server.address() as { port: number }).port;
  try {
    return await new Promise<string>((resolve) => {
      const opts = { ...pinnedTlsOptions("127.0.0.1", SERIAL, pem[pinned]!), port };
      const sock = connect(opts, () => {
        sock.destroy();
        resolve("ok");
      });
      sock.on("error", (err) => resolve(err.message));
    });
  } finally {
    server.close();
  }
}

describe("pinnedTlsOptions", () => {
  it("connects to the pinned certificate although its CA is never sent", async () => {
    expect(await handshake("printer", "printer")).toBe("ok");
  });

  it("refuses a certificate naming the same serial that is not the pinned one", async () => {
    expect(await handshake("impostor", "printer")).not.toBe("ok");
  });

  it("refuses the pinned certificate's twin naming another serial", async () => {
    expect(await handshake("other", "other")).toMatch(/names SOMEOTHERSERIAL, not TESTSERIAL0001/);
  });
});

describe("pinRefusal", () => {
  it("accepts a certificate naming the serial, in date", () => {
    expect(pinRefusal(new X509Certificate(pem.printer!), SERIAL)).toBeNull();
  });
  it("refuses one naming another serial", () => {
    expect(pinRefusal(new X509Certificate(pem.other!), SERIAL)).toMatch(/names SOMEOTHERSERIAL/);
  });
  it("refuses one out of date", () => {
    expect(pinRefusal(new X509Certificate(pem.printer!), SERIAL, new Date("2001-01-01"))).toMatch(/out of date/);
  });
});

describe("firstPem", () => {
  it("takes the first certificate out of s_client output", () => {
    const out = `CONNECTED\n${pem.printer}${pem.other}---\n`;
    expect(firstPem(out)).toBe(`${pem.printer!.trim()}\n`);
  });
  it("is null when there is none", () => {
    expect(firstPem("connect:errno=61")).toBeNull();
  });
});

describe("cameraUrl and snapshotArgs", () => {
  it("opens the loopback relay with the stand-in password, never the access code", () => {
    expect(cameraUrl(5544)).toBe("rtsp://bblp:relay@127.0.0.1:5544/streaming/live/1");
  });
  it("asks ffmpeg for one JPEG frame over TCP", () => {
    const args = snapshotArgs("rtsp://x", "out.jpg");
    expect(args).toEqual(expect.arrayContaining(["-rtsp_transport", "tcp", "-frames:v", "1"]));
    expect(args.at(-1)).toBe("out.jpg");
  });
});

describe("scrub", () => {
  it("hides the code raw and URL-encoded", () => {
    expect(scrub("a 12/34 b 12%2F34", "12/34")).toBe("a **** b ****");
  });
});

const md5 = (s: string) => createHash("md5").update(s).digest("hex");

describe("signDigest", () => {
  const head =
    "DESCRIBE rtsps://10.0.0.5:322/streaming/live/1 RTSP/1.0\r\nCSeq: 3\r\n" +
    'Authorization: Digest username="bblp", realm="LIVE555 Streaming Media", nonce="abc123", ' +
    'uri="rtsps://10.0.0.5:322/streaming/live/1", response="00000000000000000000000000000000"';

  it("replaces the response with one over the real password, method and written uri", () => {
    const ha1 = md5("bblp:LIVE555 Streaming Media:secret");
    const ha2 = md5("DESCRIBE:rtsps://10.0.0.5:322/streaming/live/1");
    const signed = signDigest(head, "secret");
    expect(signed).toContain(`response="${md5(`${ha1}:abc123:${ha2}`)}"`);
    expect(signed).toContain('nonce="abc123"');
    expect(signed).not.toContain("00000000000000000000000000000000");
  });

  it("leaves a message without Digest auth alone", () => {
    const plain = "OPTIONS rtsps://10.0.0.5:322/streaming/live/1 RTSP/1.0\r\nCSeq: 1";
    expect(signDigest(plain, "secret")).toBe(plain);
  });
});

describe("RtspRewriter with urlSwaps", () => {
  const swaps = urlSwaps("10.0.0.5", 5544, "secret");

  it("swaps the loopback URL for the printer's on the way out", () => {
    const out = new RtspRewriter(swaps.outbound).push(
      Buffer.from("OPTIONS rtsp://127.0.0.1:5544/streaming/live/1 RTSP/1.0\r\nCSeq: 1\r\n\r\n"),
    );
    expect(out.toString()).toBe("OPTIONS rtsps://10.0.0.5:322/streaming/live/1 RTSP/1.0\r\nCSeq: 1\r\n\r\n");
  });

  it("swaps the printer's URL back, with or without the port, and recomputes Content-Length", () => {
    const sdp = "a=control:rtsps://10.0.0.5/streaming/live/1/track1\r\n";
    const msg = `RTSP/1.0 200 OK\r\nContent-Base: rtsps://10.0.0.5:322/streaming/live/1/\r\nContent-Length: ${sdp.length}\r\n\r\n${sdp}`;
    const text = new RtspRewriter(swaps.inbound).push(Buffer.from(msg)).toString();
    const body = "a=control:rtsp://127.0.0.1:5544/streaming/live/1/track1\r\n";
    expect(text).toContain("Content-Base: rtsp://127.0.0.1:5544/streaming/live/1/");
    expect(text).toContain(`Content-Length: ${body.length}\r\n\r\n${body}`);
  });

  it("passes media frames through byte for byte, even when one holds the URL", () => {
    const payload = Buffer.from("rtsps://10.0.0.5:322 inside video");
    const frame = Buffer.concat([Buffer.from([0x24, 0, 0, payload.length]), payload]);
    expect(new RtspRewriter(swaps.inbound).push(frame).equals(frame)).toBe(true);
  });

  it("holds a message or frame split across chunks until it is whole", () => {
    const rw = new RtspRewriter(swaps.inbound);
    const frame = Buffer.from([0x24, 1, 0, 3, 7, 8, 9]);
    const msg = Buffer.from("RTSP/1.0 200 OK\r\nCSeq: 4\r\n\r\n");
    const all = Buffer.concat([frame, msg]);
    const parts = [all.subarray(0, 2), all.subarray(2, 9), all.subarray(9)];
    const out = Buffer.concat(parts.map((p) => rw.push(p)));
    expect(out.equals(all)).toBe(true);
    expect(rw.push(Buffer.alloc(0)).length).toBe(0);
  });
});
