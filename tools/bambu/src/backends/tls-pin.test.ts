import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { X509Certificate } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { connect, createServer, type Server, type TLSSocket } from "node:tls";
import { Client as FtpClient } from "basic-ftp";
import mqtt from "mqtt";
import { firstPem, pinnedTlsOptions, pinRefusal, readPin } from "./tls-pin.js";

// Every connection that carries the access code (MQTT 8883, FTPS 990, camera 322) checks the
// printer's pinned certificate (backends/tls-pin.ts). The load-bearing case is the refusal: a server
// showing any certificate but the pinned one, even one naming the same serial, must not get a
// connection. The certificates are made here with openssl, shaped like the X2D's: a leaf naming the
// serial, signed by a CA no client has. Port 322 sends the leaf alone; 8883 and 990 send the leaf
// and its CA, so both shapes are served here.

const SERIAL = "TESTSERIAL0001";
let dir: string;
const pem: Record<string, string> = {};
const key: Record<string, string> = {};

function ssl(...args: string[]): void {
  execFileSync("openssl", args, { cwd: dir, stdio: "ignore" });
}

/** A CA, and a leaf it signs naming `cn`; keeps the leaf's PEM, its key and the CA's PEM. */
function leaf(name: string, cn: string): void {
  ssl("req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", `${name}-ca.key`, "-out", `${name}-ca.pem`,
    "-days", "2", "-subj", `/CN=Test Device CA ${name}`);
  ssl("req", "-newkey", "rsa:2048", "-nodes", "-keyout", `${name}.key`, "-out", `${name}.csr`, "-subj", `/CN=${cn}`);
  ssl("x509", "-req", "-in", `${name}.csr`, "-CA", `${name}-ca.pem`, "-CAkey", `${name}-ca.key`,
    "-CAcreateserial", "-out", `${name}.pem`, "-days", "2");
  pem[name] = readFileSync(join(dir, `${name}.pem`), "utf8");
  pem[`${name}-ca`] = readFileSync(join(dir, `${name}-ca.pem`), "utf8");
  key[name] = readFileSync(join(dir, `${name}.key`), "utf8");
}

beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), "printer-pin-"));
  leaf("printer", SERIAL);
  leaf("impostor", SERIAL); // same serial, different key and CA
  leaf("other", "SOMEOTHERSERIAL");
});

afterAll(() => rmSync(dir, { recursive: true, force: true }));

/** Serve `name`'s leaf (with its CA when `chain`), answer each connection with `greet`, and run
 *  `client` against the port. */
async function serving<T>(
  name: string,
  chain: boolean,
  greet: (s: TLSSocket) => void,
  client: (port: number) => Promise<T>,
): Promise<T> {
  const cert = chain ? `${pem[name]}${pem[`${name}-ca`]}` : pem[name];
  const server: Server = createServer({ cert, key: key[name] }, greet);
  await new Promise<void>((ok) => server.listen(0, "127.0.0.1", ok));
  try {
    return await client((server.address() as { port: number }).port);
  } finally {
    server.close();
  }
}

/** A plain pinned TLS connection: "ok" or the error. */
function handshake(served: string, pinned: string, chain = false): Promise<string> {
  return serving(served, chain, (s) => s.end(), (port) =>
    new Promise<string>((resolve) => {
      const sock = connect({ host: "127.0.0.1", port, ...pinnedTlsOptions(SERIAL, pem[pinned]!) }, () => {
        sock.destroy();
        resolve("ok");
      });
      sock.on("error", (err) => resolve(err.message));
    }));
}

describe("pinnedTlsOptions", () => {
  it("connects to the pinned certificate although its CA is never sent (the camera's 322)", async () => {
    expect(await handshake("printer", "printer")).toBe("ok");
  });

  it("connects to the pinned certificate sent with its CA (8883 and 990)", async () => {
    expect(await handshake("printer", "printer", true)).toBe("ok");
  });

  it("refuses a certificate naming the same serial that is not the pinned one", async () => {
    expect(await handshake("impostor", "printer")).not.toBe("ok");
  });

  it("refuses it sent with its own CA too", async () => {
    expect(await handshake("impostor", "printer", true)).not.toBe("ok");
  });

  it("refuses the pinned certificate's twin naming another serial", async () => {
    expect(await handshake("other", "other")).toMatch(/names SOMEOTHERSERIAL, not TESTSERIAL0001/);
  });
});

// The libraries the backends hand these options to: each must carry them into Node's TLS unchanged.

/** A pinned MQTT connect: "connected" on CONNACK, else the error. The server answers a CONNACK. */
function mqttConnect(served: string): Promise<string> {
  const connack = (s: TLSSocket) => s.once("data", () => s.write(Buffer.from([0x20, 0x02, 0x00, 0x00])));
  return serving(served, true, connack, (port) =>
    new Promise<string>((resolve) => {
      const client = mqtt.connect({
        host: "127.0.0.1", port, protocol: "mqtts", username: "bblp", password: "x",
        reconnectPeriod: 0, connectTimeout: 5000, ...pinnedTlsOptions(SERIAL, pem.printer!),
      });
      const done = (r: string) => {
        client.end(true);
        resolve(r);
      };
      client.on("connect", () => done("connected"));
      client.on("error", (err) => done(err.message));
    }));
}

/** A pinned implicit-FTPS connect: "connected" on the 220 greeting, else the error. */
function ftpsConnect(served: string): Promise<string> {
  return serving(served, true, (s) => s.write("220 ready\r\n"), async (port) => {
    const client = new FtpClient(5000);
    try {
      await client.connectImplicitTLS("127.0.0.1", port, pinnedTlsOptions(SERIAL, pem.printer!));
      return "connected";
    } catch (err) {
      return (err as Error).message;
    } finally {
      client.close();
    }
  });
}

describe("pinned options through mqtt and basic-ftp", () => {
  it("mqtt connects to the pinned printer", async () => {
    expect(await mqttConnect("printer")).toBe("connected");
  });
  it("mqtt refuses an impostor before the password goes out", async () => {
    expect(await mqttConnect("impostor")).not.toBe("connected");
  });
  it("basic-ftp connects to the pinned printer", async () => {
    expect(await ftpsConnect("printer")).toBe("connected");
  });
  it("basic-ftp refuses an impostor before the password goes out", async () => {
    expect(await ftpsConnect("impostor")).not.toBe("connected");
  });
});

describe("readPin", () => {
  it("names the command that makes the pin when there is none", () => {
    expect(() => readPin("NOPINSERIAL", dir)).toThrow(/bambu setup printer-pin/);
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
