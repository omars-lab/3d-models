// The color is named at the send (call 18, Omar 2026-10-08: "Always at the send";
// print-time-color-map-design §8). A one-color plate's recipe carries no color, so a send that names
// none would print in whatever the slice's preset says, Studio's default green, which nobody chose.
// The send refuses that before anything reaches the network, dry run or not: the operator names the
// color with `--color`, or picks the tray with `--ams-mapping`.
//
// Two cases still go out without either flag:
//   - a plate that feeds more than one filament (phones-01): its colors are a list in its recipe and
//     the slice, matched tray by tray, and `--color` is refused for it anyway (chooseColor);
//   - a recipe that still fixes one color: only a frozen production plate may (phones-02, D-095, open
//     call 3), and the plates gate (P11) refuses one anywhere else.

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { parse as parseYaml } from "yaml";

/** The recipe a plate is sliced from: docs/design/plates/<name>.yaml, the page's sibling. */
export function plateRecipePath(name: string, root: string): string {
  return join(root, "docs", "design", "plates", `${name}.yaml`);
}

/** The color a recipe fixes in `profile.color`, or null when it fixes none (or there is no recipe). */
export function recipeColor(recipe: string): string | string[] | null {
  if (!existsSync(recipe)) return null;
  const doc = parseYaml(readFileSync(recipe, "utf8")) as { profile?: { color?: unknown } } | null;
  const c = doc?.profile?.color;
  if (typeof c === "string" && c.trim() !== "") return c;
  if (Array.isArray(c) && c.length > 0) return c.map(String);
  return null;
}

export interface ColorAtSendInput {
  used: number[] | null; // the filament slots the slice feeds (readUsedFilaments), null when unread
  fixed: string | string[] | null; // what the recipe fixes in profile.color
  color?: string; // --color
  amsMapping?: string; // --ams-mapping
}

export interface ColorAtSend {
  ok: boolean;
  line: string;
}

/** Does the send's color match the one the yes covers (print-time-color-map §5)? A yes that names a
 * color covers that color only, so the send must name the same one with `--color`; a tray picked
 * with `--ams-mapping` alone says no color, so it is refused too. A new color is a new yes (D-103).
 * A yes that names none covers whatever the send names (null line: nothing to report). PURE. */
export function colorMatchesYes(yesColor: string | null, color?: string): ColorAtSend | null {
  if (yesColor === null) return null;
  if (color !== undefined && color.toUpperCase() === yesColor.toUpperCase()) {
    return { ok: true, line: `color: ${yesColor}, the color the yes covers` };
  }
  const named = color === undefined ? "names no color" : `names ${color}`;
  return {
    ok: false,
    line:
      `color: the yes covers this plate in ${yesColor} and the send ${named}; pass --color ${yesColor}, ` +
      "or a new color needs a new yes (D-103)",
  };
}

/** May this send go out with the color it names? PURE. */
export function colorAtSend(input: ColorAtSendInput): ColorAtSend {
  if (input.color !== undefined) return { ok: true, line: `color: ${input.color}, named at the send (--color)` };
  if (input.amsMapping !== undefined) return { ok: true, line: "color: the tray picked at the send (--ams-mapping)" };
  if (input.used === null) return { ok: true, line: "color: the slice names no filaments; the filament match decides" };
  if (input.used.length > 1) {
    return { ok: true, line: `color: ${input.used.length} filaments, matched tray by tray to the slice's colors` };
  }
  if (input.fixed !== null) {
    const fixed = Array.isArray(input.fixed) ? input.fixed.join(", ") : input.fixed;
    return { ok: true, line: `color: ${fixed}, fixed in a frozen recipe (production, D-095)` };
  }
  return {
    ok: false,
    line:
      "color: a one-color plate's color is named at the send, and this one names none; " +
      "pass --color <#RRGGBB> (or pick the tray with --ams-mapping)",
  };
}
