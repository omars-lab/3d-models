// The bed photo and what someone saw in it.
//
// `print send --dry-run` saves one camera frame of the bed under `.bambu/bed/`, and the send-plate
// skill says to open it and look. Nothing proved anyone did. sheets-04b's photo showed a Textured
// PEI Plate while the slice was for a Cool Plate (docs/issues/sliced-for-wrong-plate.md): the photo
// held the answer, and the send went out without anyone comparing it to the slice. Omar asked for a
// check on "recently pulled screenshots, screenshot verdicts" (2026-10-03).
//
// So a look is written down. `bambu bed verdict` records, beside the photo, what it shows: the bed
// clear or not, the plate seated or not, which plate type, and who looked. The record names the
// photo's bytes (sha256), so it cannot be moved to another photo. A real send then refuses unless
// the newest photo of this plate is recent, has a record, and the record says clear, seated, and the
// plate type the slice was made for.
//
// The checks are PURE (`bedCheck`); the IO (`newestBedPhoto`, `readVerdict`, `writeVerdict`) is kept
// apart so the tests need no camera.

import { createHash } from "node:crypto";
import { existsSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";
import { plateTypeFromToken } from "./plate-type.js";

/** How old the photo a send rests on may be. A bed can change in half an hour; a dry run is cheap. */
export const BED_PHOTO_MAX_AGE_MIN = 30;

export interface BedPhoto {
  path: string;
  mtimeMs: number;
  sha256: string;
}

export interface BedVerdict {
  photo: string; // the photo's file name
  sha256: string; // of the photo's bytes
  plate: string; // the plate name, e.g. "sheets-04b"
  bed_clear: boolean; // nothing left on the bed
  plate_seated: boolean; // the build plate is in and flat
  plate_type: string; // the start command's token for the plate seen, e.g. "textured_plate"
  non_bambu?: boolean; // true: not Bambu's own plate (the glacier); absent: a Bambu plate. Sets the print options (D-108)
  by: string; // who looked
  note?: string;
  at: string; // ISO time the verdict was written
}

export interface BedCheck {
  ok: boolean; // false: refuse the send
  line: string; // the send's ✓ / ✗ line, without the mark
}

export function bedDir(root: string): string {
  return join(root, ".bambu", "bed");
}

export function verdictPath(photoPath: string): string {
  return `${photoPath}.verdict.json`;
}

/** The photo name `print send` writes: `<plate>-<ISO stamp with : and . as ->.jpg`. */
export function bedPhotoName(plate: string, now: Date = new Date()): string {
  return `${plate}-${now.toISOString().replace(/[:.]/g, "-")}.jpg`;
}

/** True when `file` is one of this plate's photos, and not another plate whose name starts the same. */
export function isPhotoOf(plate: string, file: string): boolean {
  const esc = plate.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`^${esc}-\\d{4}-\\d{2}-\\d{2}T[\\d-]+Z\\.jpg$`).test(file);
}

export function sha256File(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

/** This plate's newest bed photo by file time, or null. */
export function newestBedPhoto(root: string, plate: string): BedPhoto | null {
  const dir = bedDir(root);
  if (!existsSync(dir)) return null;
  const photos = readdirSync(dir)
    .filter((f) => isPhotoOf(plate, f))
    .map((f) => ({ path: join(dir, f), mtimeMs: statSync(join(dir, f)).mtimeMs }))
    .sort((a, b) => b.mtimeMs - a.mtimeMs);
  const top = photos[0];
  return top ? { ...top, sha256: sha256File(top.path) } : null;
}

export function readVerdict(photoPath: string): BedVerdict | null {
  const p = verdictPath(photoPath);
  if (!existsSync(p)) return null;
  try {
    return JSON.parse(readFileSync(p, "utf8")) as BedVerdict;
  } catch {
    return null;
  }
}

export function writeVerdict(photo: BedPhoto, v: Omit<BedVerdict, "photo" | "sha256">): BedVerdict {
  const verdict: BedVerdict = { photo: basename(photo.path), sha256: photo.sha256, ...v };
  writeFileSync(verdictPath(photo.path), `${JSON.stringify(verdict, null, 2)}\n`);
  return verdict;
}

const plateName = (token: string): string => plateTypeFromToken(token)?.name ?? token;

/**
 * May a send go out on this bed? PURE. `sliceToken` is the plate type the slice was made for. The
 * refusal names the command that fixes it, so the line is the next step.
 */
export function bedCheck(
  plate: string,
  photo: BedPhoto | null,
  verdict: BedVerdict | null,
  sliceToken: string,
  nowMs: number,
  maxAgeMin = BED_PHOTO_MAX_AGE_MIN,
): BedCheck {
  const record = `bambu bed verdict ${plate} --plate-type <seen> --by <who>`;
  if (!photo) {
    return { ok: false, line: `bed: no photo of the bed for ${plate}. Take one with \`bambu bed photo ${plate}\` (or the dry run), look at it, then \`${record}\`` };
  }
  const name = basename(photo.path);
  const ageMin = Math.floor((nowMs - photo.mtimeMs) / 60000);
  if (ageMin > maxAgeMin) {
    return { ok: false, line: `bed: the newest photo (${name}) is ${ageMin} min old, over ${maxAgeMin}. Take a new one with \`bambu bed photo ${plate}\` and look again` };
  }
  if (!verdict) {
    return { ok: false, line: `bed: nobody has written down what ${name} shows. Open it, then \`${record}\`` };
  }
  if (verdict.sha256 !== photo.sha256) {
    return { ok: false, line: `bed: the verdict beside ${name} is for other photo bytes. Look again and write a new one` };
  }
  if (!verdict.bed_clear) {
    return { ok: false, line: `bed: ${verdict.by} saw something on the bed in ${name}${verdict.note ? ` (${verdict.note})` : ""}. Clear it, take a new photo, look again` };
  }
  if (!verdict.plate_seated) {
    return { ok: false, line: `bed: ${verdict.by} saw the build plate not seated in ${name}. Seat it, take a new photo, look again` };
  }
  if (verdict.plate_type !== sliceToken) {
    return {
      ok: false,
      line: `bed: ${verdict.by} saw a ${plateName(verdict.plate_type)} in ${name}; the slice is for a ${plateName(sliceToken)}. Re-slice with --plate-type ${verdict.plate_type}, or put the right plate in`,
    };
  }
  return { ok: true, line: `bed: ${name}, ${ageMin} min old, looked at by ${verdict.by}: clear, plate seated, ${plateName(verdict.plate_type)}` };
}
