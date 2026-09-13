// Backend: AppleScript / osascript GUI automation — the LAST-RESORT fallback.
//
// Used only where no headless path exists: Bambu Connect is closed-source and GUI-only, and a few
// Studio actions have no CLI. The router tries MCP and the BambuStudio CLI first; this is the floor.
// Every osascript call is timeout-bounded and logged (observability tenet) so a stuck GUI dialog
// cannot freeze the run.

import { runWithTimeout } from "../log.js";

/** Is a given macOS app currently installed? (by bundle name under /Applications) */
import { existsSync } from "node:fs";
export function appInstalled(appName: string): boolean {
  return existsSync(`/Applications/${appName}`);
}

/** Run an AppleScript snippet via osascript with a hard timeout. Returns trimmed stdout. */
export async function osascript(script: string, timeoutMs = 20_000): Promise<string> {
  const res = await runWithTimeout("osascript", ["-e", script], { timeoutMs, label: "osascript" });
  if (res.timedOut) throw new Error("osascript timed out (GUI likely showing a blocking dialog)");
  if (res.code !== 0) throw new Error(`osascript failed: ${res.stderr.trim() || res.stdout.trim()}`);
  return res.stdout.trim();
}

/** Bring an app to the front (used before scripted UI interaction). */
export async function activateApp(appName: string): Promise<void> {
  await osascript(`tell application "${appName}" to activate`);
}
