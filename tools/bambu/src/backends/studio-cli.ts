// Backend: the BambuStudio headless CLI (slicing).
//
// BambuStudio ships a CLI inside the .app bundle. We locate it, and expose a version/probe used by
// `setup doctor` and (phase 2) `slice`. Slicing options are filled in when the slice group lands;
// this module owns *finding and probing* the slicer so doctor can report it today.

import { existsSync } from "node:fs";
import { runWithTimeout } from "../log.js";
import { loadConfig } from "../config.js";

// Common install locations on macOS for both the stable and beta apps (they coexist).
const CANDIDATES = [
  "/Applications/BambuStudio.app/Contents/MacOS/BambuStudio",
  "/Applications/Bambu Studio.app/Contents/MacOS/BambuStudio",
  "/Applications/BambuStudio-beta.app/Contents/MacOS/BambuStudio",
];

/** Resolve the BambuStudio binary: SLICER_PATH from config, else the first existing candidate. */
export function locateStudio(): string | null {
  const cfg = loadConfig();
  if (cfg.slicerPath && existsSync(cfg.slicerPath)) return cfg.slicerPath;
  return CANDIDATES.find((p) => existsSync(p)) ?? null;
}

export interface StudioProbe {
  found: boolean;
  path?: string;
  version?: string;
}

export async function probeStudio(): Promise<StudioProbe> {
  const path = locateStudio();
  if (!path) return { found: false };
  const res = await runWithTimeout(path, ["--version"], { timeoutMs: 15_000, label: "studio_version" });
  const version = (res.stdout + res.stderr).trim().split("\n")[0] || undefined;
  return { found: true, path, version };
}
