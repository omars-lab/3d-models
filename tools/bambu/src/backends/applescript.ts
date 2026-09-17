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

/** The .app bundle names Bambu Studio ships under (stable + beta coexist). */
export const STUDIO_APPS = ["Bambu Studio.app", "BambuStudio.app", "BambuStudio-beta.app"] as const;

/** First installed Bambu Studio .app bundle name, or null. (The GUI app, not the CLI binary.) */
export function locateStudioApp(): string | null {
  return STUDIO_APPS.find(appInstalled) ?? null;
}

/**
 * Open a file in a macOS app and bring it to the front. `open -a` is timeout-bounded
 * (a GUI can hang) and does NOT trigger a blocking dialog by itself. Throws on a
 * non-zero `open` exit so callers can report honestly instead of pretending it worked.
 */
export async function openFileInApp(appName: string, filePath: string): Promise<void> {
  const bundle = appName.endsWith(".app") ? appName : `${appName}.app`;
  await activateApp(bundle.replace(/\.app$/, ""));
  const res = await runWithTimeout("open", ["-a", bundle, filePath], {
    timeoutMs: 15_000,
    label: "app_open",
  });
  if (res.timedOut) throw new Error(`open -a ${bundle} timed out`);
  if (res.code !== 0) throw new Error(`open -a ${bundle} failed: ${res.stderr.trim() || res.stdout.trim()}`);
}
