// What the printer can store, read off its status report, and which files on it we may delete.
// Kept apart from the network so it can be tested without a printer.
//
// Why this exists (2026-10-03): the first CLI send passed every check, then the upload came back
// `553 Could not create file`. The status report said `sdcard: false` the whole time: the upload
// writes to the storage card, and there was none. The send now reads that before uploading.
//
// What the report carries, as the X2D sent it on 2026-10-03 (`bambu status show --json`):
//   - `sdcard`: whether a storage card is in. The FTP root the upload writes to is that card.
//   - `ipcam.tl_external_free_kb` / `tl_external_total_kb`: free and total space on the card (both 0
//     with no card). The printer reports them for timelapse recording; reading them as the card's
//     space is our reading of the names, not confirmed with a card in.
//   - `ipcam.tl_internal_free_kb` / `tl_internal_total_kb`: the printer's built-in storage. The
//     upload cannot reach it; Bambu Studio's sends land there.

import { basename } from "node:path";
import type { PrinterStatus } from "./backends/mqtt.js";

export interface Storage {
  card: boolean | null; // null: the report did not say
  cardFreeKb: number | null;
  cardTotalKb: number | null;
  internalFreeKb: number | null;
  internalTotalKb: number | null;
}

function num(v: unknown): number | null {
  const n = typeof v === "string" ? Number(v) : v;
  return typeof n === "number" && Number.isFinite(n) ? n : null;
}

/** The storage fields of one status frame. Looks in `ipcam` first, then `device.cam`, which repeats them. */
export function readStorage(frame: PrinterStatus): Storage {
  const ipcam = (frame.ipcam ?? {}) as Record<string, unknown>;
  const cam = ((frame.device as Record<string, unknown> | undefined)?.cam ?? {}) as Record<string, unknown>;
  const field = (k: string) => num(ipcam[k]) ?? num(cam[k]);
  return {
    card: typeof frame.sdcard === "boolean" ? frame.sdcard : null,
    cardFreeKb: field("tl_external_free_kb"),
    cardTotalKb: field("tl_external_total_kb"),
    internalFreeKb: field("tl_internal_free_kb"),
    internalTotalKb: field("tl_internal_total_kb"),
  };
}

/**
 * Why the upload has nowhere to go, or null when it can try. Refuses when the report says there is no
 * card, or when the card's free space is reported and smaller than the file. A report that does not
 * mention the card is not a refusal: other models may leave the field out, and the upload's own error
 * still stops a send that cannot land.
 */
export function cardRefusal(frame: PrinterStatus, fileKb: number): string | null {
  const s = readStorage(frame);
  if (s.card === false) {
    return "the printer has no storage card in (it reports sdcard: false), and the upload writes to the card";
  }
  if (s.card === true && s.cardFreeKb !== null && s.cardTotalKb !== null && s.cardTotalKb > 0 && s.cardFreeKb < fileKb) {
    return `the storage card has ${fmtKb(s.cardFreeKb)} free and the plate is ${fmtKb(fileKb)}`;
  }
  return null;
}

export function fmtKb(kb: number): string {
  if (kb >= 1024 * 1024) return `${(kb / 1024 / 1024).toFixed(1)} GB`;
  if (kb >= 1024) return `${Math.round(kb / 1024)} MB`;
  return `${kb} KB`;
}

function space(free: number | null, total: number | null): string {
  return free === null || total === null ? "space not reported" : `${fmtKb(free)} free of ${fmtKb(total)}`;
}

/** The card in a few words: "in, 28.1 GB free of 29.7 GB", "none in the printer" or "not reported". */
export function cardSummary(s: Storage): string {
  if (s.card === null) return "not reported";
  return s.card ? `in, ${space(s.cardFreeKb, s.cardTotalKb)}` : "none in the printer";
}

/** Human lines for `bambu storage show`. */
export function renderStorage(s: Storage): string {
  return [
    `storage card:     ${cardSummary(s)}`,
    `built-in storage: ${space(s.internalFreeKb, s.internalTotalKb)} (the upload cannot reach it)`,
  ].join("\n");
}

/**
 * Why `bambu storage rm` will not delete this name, or null when it may. Only a plate file at the
 * card's top folder, which is where `print send` puts them: a bare name ending in .3mf. Anything in a
 * folder (timelapse videos, the printer's cache) is the printer's, not ours. The file the printer is
 * printing from is refused too.
 */
export function rmRefusal(name: string, frame: PrinterStatus | null): string | null {
  if (name !== basename(name) || name.includes("\\")) return `${name} is in a folder; only plate files at the top are ours to delete`;
  if (!/\.3mf$/i.test(name)) return `${name} is not a plate file (.3mf); only plates are ours to delete`;
  if (frame) {
    const state = String(frame.gcode_state ?? "").toUpperCase();
    const job = String(frame.subtask_name ?? "");
    const busy = !["IDLE", "FINISH", "FAILED", ""].includes(state);
    if (busy && job && name.replace(/\.3mf$/i, "") === job) return `the printer is printing from ${name} (${state})`;
  }
  return null;
}
