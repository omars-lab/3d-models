// Backend router — picks the cheapest capable backend for a capability, GUI last.
//
// Preference order (global CLAUDE.md "robust and simple beat cheap and easy"): the BambuStudio CLI
// owns headless slicing; AppleScript is the floor for GUI-only actions; the griches MCP is the
// fallback transport for control/camera. Status now rides our first-party MQTT backend directly
// (D-055) and does not go through this router. Slice-capable commands ask the router for a backend
// rather than hard-wiring one, so the fallback chain lives in one place.

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
 * list so callers can try in order. Slicing prefers the CLI then GUI; everything else prefers MCP.
 */
export function preferenceFor(cap: Capability, a: BackendAvailability): ("mcp" | "studio-cli" | "applescript")[] {
  if (cap === "slice") {
    const order: ("studio-cli" | "applescript")[] = [];
    if (a.studio.found) order.push("studio-cli");
    order.push("applescript"); // drive Studio's GUI as a last resort
    return order;
  }
  // control/status/upload/ams/camera all ride the MCP; no GUI equivalent worth scripting.
  return a.mcp ? ["mcp"] : [];
}
