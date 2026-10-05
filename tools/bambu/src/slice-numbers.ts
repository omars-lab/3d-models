// The minutes, grams and beds a sliced plate carries, read one way for everyone: `bambu validate
// sliced` prints them and `bambu order plan` plans with them, so the two cannot disagree (order-driven
// design §9.5: "every plate's minutes and grams equal its own `bambu validate sliced` output").
//
// Grams: the slice writes its own (`used_g`, from the filament preset's density: PLA Basic 1.26,
// Matte 1.32), and every slice in build/plates since sheets-04 carries it (sheets-04g 27.15 g,
// phones-02 3.46 g, read 2026-10-05). An older headless slice left used_g=0.00 because the X2D PLA
// profile then shipped filament_density=['0']; for those, and when --density is given, grams are
// derived from the filament length and reported as derived, never as the slice's.

import { parseBeds, type SlicedBed } from "./threemf.js";

export const FILAMENT_DIAMETER_MM = 1.75;
export const DEFAULT_PLA_DENSITY = 1.24;

/** Grams from filament length via a density (g/cm³). */
export function deriveGrams(usedM: number, density: number): number {
  const area = Math.PI * (FILAMENT_DIAMETER_MM / 2) ** 2; // mm²
  return ((usedM * 1000 * area) / 1000) * density; // cm³ × g/cm³
}

export interface SliceNumbers {
  beds: SlicedBed[];
  /** Seconds the slicer predicts, all beds; null when no bed carries a prediction. */
  predictionS: number | null;
  usedM: number;
  grams: number;
  /** "slice": the slice's own used_g; "derived": from usedM and `density`. */
  gramsFrom: "slice" | "derived";
  density: number | null;
}

/** Read the numbers out of a slice's Metadata/slice_info.config. `density` forces derived grams. */
export function sliceNumbers(sliceInfoRaw: string, density?: number): SliceNumbers {
  const beds = parseBeds(sliceInfoRaw);
  const times = beds.map((b) => b.predictionS).filter((t): t is number => t !== null);
  const predictionS = times.length > 0 ? times.reduce((a, t) => a + t, 0) : null;
  const sum = (re: RegExp) => [...sliceInfoRaw.matchAll(re)].reduce((a, m) => a + Number(m[1]), 0);
  const usedM = sum(/used_m="(\d+(?:\.\d+)?)"/g);
  const usedG = sum(/used_g="(\d+(?:\.\d+)?)"/g);
  if (density === undefined && usedG > 0) {
    return { beds, predictionS, usedM, grams: round2(usedG), gramsFrom: "slice", density: null };
  }
  const d = density ?? DEFAULT_PLA_DENSITY;
  return { beds, predictionS, usedM, grams: usedM > 0 ? round2(deriveGrams(usedM, d)) : 0, gramsFrom: "derived", density: d };
}

/** Sliced minutes, to one decimal: the unit the plan and its goldens use. */
export function minutesOf(predictionS: number): number {
  return Math.round((predictionS / 60) * 10) / 10;
}

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}
