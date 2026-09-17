// Backend router — picks the cheapest capable backend for a capability, GUI last.
//
// Preference order (global CLAUDE.md "robust and simple beat cheap and easy"): the BambuStudio CLI
// owns headless slicing; AppleScript is the floor for GUI-only actions; the griches MCP is the
// last-ditch transport for anything still without a first-party path (camera/ams). The transports
// that matter have since gone first-party and do NOT ride this router: status over MQTT (D-055),
// and dispatch — FTPS upload + MQTT `print.project_file` control — over our own backends (#50),
// since the griches MCP was never installable (`@griches/bambu-mcp` unpublished, ships no build).
// So in practice this router only routes `slice`; the MCP branch survives for capabilities we have
// not yet brought first-party. Slice-capable commands ask the router rather than hard-wiring one.

import { McpBackend } from "./mcp.js";
import { probeStudio, type StudioProbe } from "./studio-cli.js";
import { appInstalled } from "./applescript.js";

export type Capability = "control" | "status" | "upload" | "ams" | "camera" | "slice";

export interface BackendAvailability {
  mcp: boolean; // configured + (assumed) reachable
  studio: StudioProbe;
  bambuConnect: boolean; // GUI fallback app present
}

export async function surveyBackends(): Promise<BackendAvailability> {
  const mcp = new McpBackend();
  return {
    mcp: mcp.configured(),
    studio: await probeStudio(),
    bambuConnect: appInstalled("Bambu Connect.app") || appInstalled("BambuConnect.app"),
  };
}

/**
 * Which backend should serve a capability, given what's available. Returns an ordered fallback
 * list so callers can try in order. Slicing prefers the CLI then GUI. status/control/upload have
 * first-party backends and never reach here; ams/camera have no first-party path yet, so they fall
 * back to the MCP (aspirational — it is not currently installable).
 */
export function preferenceFor(cap: Capability, a: BackendAvailability): ("mcp" | "studio-cli" | "applescript")[] {
  if (cap === "slice") {
    const order: ("studio-cli" | "applescript")[] = [];
    if (a.studio.found) order.push("studio-cli");
    order.push("applescript"); // drive Studio's GUI as a last resort
    return order;
  }
  // ams/camera have no first-party backend yet; status/control/upload never route here (first-party).
  return a.mcp ? ["mcp"] : [];
}
