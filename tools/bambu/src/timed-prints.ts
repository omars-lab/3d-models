// How long prints really took, next to what the slicer said: the ratio that corrects a plan's minutes.
//
// The slicer's minutes are a floor. phones-01 took 62 minutes against 22 sliced (color swaps the
// slicer does not count), and the one-color plates took about an eighth longer than sliced. The order
// design (§9.1 step 4) corrects sliced minutes by the ratio of watched to sliced minutes over past
// prints with the same printer, process and filament, and says how many prints it rests on.
//
// A run counts only when the monitor watched all of it: a `watching` row at layer 0 and 0%, then a
// `finished` row, with nothing paused, stalled, stopped, failed, errored or lost between. A watch that
// started mid-print (sheets-04b's second run began at 38%) has no start time, so it is not counted.
// Watched minutes run from the `watching` row to the `finished` one. Sliced minutes are the plate
// page's `minutes:`, and the profile is the recipe's, matched exactly: a two-filament plate's
// "Basic;Basic" is not a one-filament Basic plate, and is not pooled with one.

import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { parse as parseYaml } from "yaml";

export interface TimedRun {
  plate: string;
  started: string; // "2026-10-04 18:37", UTC, as the log writes it
  watched: number; // minutes
  sliced: number; // minutes, the page's
  settings: string;
  filament: string;
}

export interface LogRow {
  time: string;
  event: string;
  layer: string;
  done: string;
  said: string; // the last column, "What the printer said" (a `sent` row's trays)
}

const BREAKS = new Set(["paused", "stalled", "stopped", "failed", "error", "lost", "resumed"]);

/** The rows of a print log's table. */
export function logRows(text: string): LogRow[] {
  const rows: LogRow[] = [];
  for (const line of text.split("\n")) {
    const m = /^\|\s*(\d{4}-\d\d-\d\d \d\d:\d\d)\s*\|\s*([a-z]+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|(?:\s*([^|]*?)\s*\|)?/.exec(line);
    if (m) rows.push({ time: m[1]!, event: m[2]!, layer: m[3]!, done: m[4]!, said: m[5] ?? "" });
  }
  return rows;
}

/** Each fully watched run in a log: [start time, watched minutes]. */
export function watchedRuns(rows: LogRow[]): Array<{ started: string; watched: number }> {
  const runs: Array<{ started: string; watched: number }> = [];
  let start: LogRow | null = null;
  for (const r of rows) {
    if (r.event === "watching") {
      start = /^0\//.test(r.layer) && r.done === "0%" ? r : null;
    } else if (BREAKS.has(r.event)) {
      start = null;
    } else if (r.event === "finished" && start) {
      runs.push({ started: start.time, watched: minutesBetween(start.time, r.time) });
      start = null;
    }
  }
  return runs;
}

function minutesBetween(a: string, b: string): number {
  const t = (s: string) => Date.parse(`${s.replace(" ", "T")}:00Z`);
  return Math.round((t(b) - t(a)) / 60000);
}

/** Every counted run under a plates folder (`<dir>/print-logs/<plate>.md`, `<dir>/<plate>.md|yaml`),
 *  and why each skipped log was skipped. */
export function readTimedRuns(platesDir: string): { runs: TimedRun[]; skipped: string[] } {
  const logs = join(platesDir, "print-logs");
  const runs: TimedRun[] = [];
  const skipped: string[] = [];
  if (!existsSync(logs)) return { runs, skipped };
  for (const file of readdirSync(logs).filter((f) => f.endsWith(".md")).sort()) {
    const plate = file.replace(/\.md$/, "");
    const watched = watchedRuns(logRows(readFileSync(join(logs, file), "utf8")));
    if (watched.length === 0) {
      skipped.push(`${plate}: no run watched from layer 0 to finished`);
      continue;
    }
    const sliced = pageMinutes(join(platesDir, `${plate}.md`));
    const profile = recipeProfile(join(platesDir, `${plate}.yaml`));
    if (sliced === null || !profile) {
      skipped.push(`${plate}: ${sliced === null ? "its page has no minutes" : "its recipe has no profile"}`);
      continue;
    }
    for (const w of watched) runs.push({ plate, started: w.started, watched: w.watched, sliced, ...profile });
  }
  return { runs, skipped };
}

function pageMinutes(page: string): number | null {
  if (!existsSync(page)) return null;
  const fm = /^---\n([\s\S]*?)\n---/.exec(readFileSync(page, "utf8"));
  const m = fm ? /^minutes:\s*(\d+(?:\.\d+)?)\s*$/m.exec(fm[1]!) : null;
  return m ? Number(m[1]) : null;
}

function recipeProfile(recipe: string): { settings: string; filament: string } | null {
  if (!existsSync(recipe)) return null;
  const doc = parseYaml(readFileSync(recipe, "utf8")) as { profile?: { settings?: unknown; filament?: unknown } } | null;
  const p = doc?.profile;
  return typeof p?.settings === "string" && typeof p?.filament === "string" ? { settings: p.settings, filament: p.filament } : null;
}

export interface Ratio {
  value: number; // watched ÷ sliced, pooled, to two places
  watched: number;
  sliced: number;
  prints: string[]; // "<plate> <started>"
}

function pool(runs: TimedRun[]): Ratio | null {
  if (runs.length === 0) return null;
  const watched = runs.reduce((a, r) => a + r.watched, 0);
  const sliced = runs.reduce((a, r) => a + r.sliced, 0);
  return { value: Math.round((watched / sliced) * 100) / 100, watched, sliced, prints: runs.map((r) => `${r.plate} ${r.started}`) };
}

/** The pooled ratio of runs printed with exactly this profile, or null when none was. */
export function ratioFor(runs: TimedRun[], settings: string, filament: string): Ratio | null {
  return pool(runs.filter((r) => r.settings === settings && r.filament === filament));
}

export interface NearestRatio extends Ratio {
  filament: string;
  why: string;
}

/** With no ratio for a profile: the nearest one not used, the same settings with another filament
 *  (the one resting on the most prints), and why it is not used. Null when there is none. */
export function nearestUnused(runs: TimedRun[], settings: string, filament: string): NearestRatio | null {
  const others = [...new Set(runs.filter((r) => r.settings === settings && r.filament !== filament).map((r) => r.filament))];
  const pooled = others
    .map((f) => ({ filament: f, ratio: ratioFor(runs, settings, f)! }))
    .sort((a, b) => b.ratio.prints.length - a.ratio.prints.length || a.filament.localeCompare(b.filament));
  const top = pooled[0];
  if (!top) return null;
  return { ...top.ratio, filament: top.filament, why: `printed with ${top.filament}, not ${filament}: another filament prints at its own speeds` };
}
