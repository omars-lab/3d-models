// Passive LAN discovery of Bambu printers via their own SSDP broadcast.
//
// A Bambu printer periodically emits an unsolicited SSDP `NOTIFY * HTTP/1.1`
// (`NT: urn:bambulab-com:device:3dprinter:1`) to the LAN broadcast on UDP 2021.
// We BIND and LISTEN only — we transmit NOTHING to the printer — so discovery
// is safe to run during an active print: it cannot pause, reconfigure, or even
// touch the machine. Contrast `probeTcp` in setup.ts, which opens a TCP socket
// to the printer (still safe, but not zero-touch). This is zero-touch.
//
// The broadcast carries exactly what the setup flow needs before anyone types
// an access code: IP, serial (USN), model, firmware, and — load-bearing — the
// `DevConnect.bambu.com` field, which is `cloud` until LAN Mode + Developer Mode
// are enabled. griches MCP needs open LAN MQTT/FTPS, so a printer still in
// `cloud` mode will fail `bambu setup doctor`'s LAN-reach check no matter what
// host you configure. Discovery names that cause up front.

import { createSocket } from "node:dgram";
import { ev } from "../log.js";

/** The SSDP NT/USN Bambu printers advertise. */
const BAMBU_NT = "urn:bambulab-com:device:3dprinter:1";
/** UDP port the printer broadcasts its unsolicited alive NOTIFY to. */
export const DISCOVERY_PORT = 2021;

export interface DiscoveredPrinter {
  ip: string; // Location header (the printer's LAN IP)
  serial: string; // USN (device serial)
  model?: string; // DevModel.bambu.com (internal code, e.g. N6 for the X2D)
  name?: string; // DevName.bambu.com (user-set device name)
  connectMode?: string; // DevConnect.bambu.com — "cloud" until Developer/LAN Mode is on
  bind?: string; // DevBind.bambu.com — "occupied" / "free"
  secure?: string; // Devseclink.bambu.com
  firmware?: string; // DevVersion.bambu.com
  iface?: string; // DevInf.bambu.com (e.g. wlan0 / eth0)
  from: string; // source IP of the datagram (sanity vs Location)
}

/** Parse one SSDP NOTIFY payload into a printer record, or null if it isn't a Bambu alive. */
function parseNotify(text: string, from: string): DiscoveredPrinter | null {
  if (!text.includes(BAMBU_NT)) return null;
  const h: Record<string, string> = {};
  for (const line of text.split(/\r?\n/)) {
    const idx = line.indexOf(":");
    if (idx <= 0) continue;
    const key = line.slice(0, idx).trim();
    const val = line.slice(idx + 1).trim();
    if (key) h[key] = val;
  }
  // "ssdp:byebye" is a going-away notice, not a live printer — ignore it.
  if ((h["NTS"] ?? "").toLowerCase().includes("byebye")) return null;
  const serial = h["USN"];
  const ip = h["Location"];
  if (!serial || !ip) return null;
  return {
    ip,
    serial,
    model: h["DevModel.bambu.com"],
    name: h["DevName.bambu.com"],
    connectMode: h["DevConnect.bambu.com"],
    bind: h["DevBind.bambu.com"],
    secure: h["Devseclink.bambu.com"],
    firmware: h["DevVersion.bambu.com"],
    iface: h["DevInf.bambu.com"],
    from,
  };
}

/**
 * Listen for Bambu SSDP alive broadcasts for `timeoutMs`, returning one record
 * per distinct serial (the newest payload wins). Passive: binds a UDP socket and
 * receives; never sends. Brackets the listen with ev=discover_start / _done per
 * the observability tenet, and always resolves (a bind failure resolves empty
 * with ev=discover_error rather than throwing into a command).
 */
export function discoverPrinters(opts: { timeoutMs?: number; port?: number } = {}): Promise<DiscoveredPrinter[]> {
  const timeoutMs = opts.timeoutMs ?? 8000;
  const port = opts.port ?? DISCOVERY_PORT;
  return new Promise((resolve) => {
    const found = new Map<string, DiscoveredPrinter>();
    const sock = createSocket({ type: "udp4", reuseAddr: true });
    let settled = false;
    const finish = () => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      try {
        sock.close();
      } catch {
        /* already closed */
      }
      ev("discover_done", { port, count: found.size, timeout_ms: timeoutMs });
      resolve([...found.values()]);
    };
    const timer = setTimeout(finish, timeoutMs);
    sock.on("error", (err) => {
      ev("discover_error", { port, msg: `"${String(err.message).replace(/"/g, "'")}"` });
      finish();
    });
    sock.on("message", (buf, rinfo) => {
      const rec = parseNotify(buf.toString("utf8", 0, Math.min(buf.length, 65535)), rinfo.address);
      if (rec) found.set(rec.serial, rec);
    });
    ev("discover_start", { port, timeout_ms: timeoutMs });
    try {
      // Bind to all interfaces on the discovery port; receive-only.
      sock.bind(port);
    } catch (err) {
      ev("discover_error", { port, msg: `"${String((err as Error).message).replace(/"/g, "'")}"` });
      finish();
    }
  });
}

/** True when a discovered printer still routes through the cloud (Developer/LAN Mode not yet on). */
export function isCloudBound(p: DiscoveredPrinter): boolean {
  return (p.connectMode ?? "").toLowerCase() === "cloud";
}
