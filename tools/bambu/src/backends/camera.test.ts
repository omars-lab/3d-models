import { describe, expect, it } from "vitest";
import { createHash } from "node:crypto";
import {
  cameraUrl,
  RtspRewriter,
  scrub,
  signDigest,
  snapshotArgs,
  urlSwaps,
} from "./camera.js";

// The pinned TLS hop the camera rides is tested with the other connections in tls-pin.test.ts.

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
