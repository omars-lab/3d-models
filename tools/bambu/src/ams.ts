// Palette name → AMS logical slot mapping for a composed colour plate (§6 of
// docs/coaster-colour-design.md; the D-074 dependency the composer owns, D-075).
//
// bikar's `--format parts` writes one STL per coaster region body plus a `<Coaster>.parts.json`
// sidecar tagging each body with the palette NAME the author chose (`color <region> <name>`) and
// its resolved hex. The region enum reaches the STL filename; the palette name only reaches the
// sidecar. This module is the composer's half of the §6 contract: it reads those sidecars and
// assigns each DISTINCT palette to a 1-based LOGICAL filament slot, deterministically, so the same
// plate always maps the same way and the slice's `--load-filaments` order is reproducible.
//
// Scope (part 4b-i): the pure mapping + the project_settings.config filament arrays it implies.
// Assembling the multi-part input 3MF (per-part `extruder` tags) and slicing it with
// `--load-filaments` is part 4b-ii, which needs the slicer to verify end-to-end. A LOGICAL slot is
// NOT a physical AMS slot — the physical mapping is resolved at print time by colour match (§6
// caveat); this module fixes only the logical filament index order.

/** One region body of a coaster, as bikar's `<Coaster>.parts.json` sidecar records it. */
export interface CoasterPartEntry {
  region: string; // "base" | "straps" | "border"
  stl: string; // "<Coaster>-<region>.stl", beside the sidecar
  triangles: number;
  paletteName: string | null; // null ⇒ untagged: prints in the plate's default filament
  hex: string | null;
}
/** The `<Coaster>.parts.json` sidecar `--format parts` writes beside the bodies (bikar #215). */
export interface CoasterPartsSidecar {
  coaster: string;
  pinch: string;
  parts: CoasterPartEntry[];
}

/** One logical filament slot on the plate. `paletteName === null` is the plate DEFAULT filament
 *  (always slot 1); its colour is the profile preset's, so `hex` is null there. */
export interface AmsSlot {
  slot: number; // 1-based logical slot (the `--load-filaments` list order)
  paletteName: string | null;
  hex: string | null;
}
export interface AmsSlotMap {
  slots: AmsSlot[];
  /** coaster name → (region → 1-based logical slot). Every region of every coaster resolves. */
  assignments: Map<string, Map<string, number>>;
}

// **Default:** one AMS unit carries 4 slots; multiple units expand this. A 3-region coaster needs
// at most 3 tagged slots + the default, so 4 covers the single-unit case — pass the real capacity
// when more units are installed. (docs/coaster-colour-design.md §6; D-075.)
export const DEFAULT_AMS_SLOTS = 4;

export interface SlotMapOpts {
  /** The plate's default filament (profile.filament) — slot 1. Untagged regions print in it. */
  defaultFilament: string;
  /** Physical AMS capacity to cap the logical slot count at (default one unit, 4 slots). */
  maxSlots?: number;
}

/**
 * Assign palette names to logical slots across a whole plate's coaster sidecars.
 *
 * Rule (D-075): slot 1 is the plate default filament; every DISTINCT tagged palette name takes the
 * next slot in FIRST-SEEN order (coaster order, then part order within each coaster). Two bodies
 * tagged with the same name share a slot. A name that resolves to two different hexes is an error —
 * a palette name must name one colour. The logical slot count may not exceed `maxSlots`.
 */
export function buildAmsSlotMap(sidecars: CoasterPartsSidecar[], opts: SlotMapOpts): AmsSlotMap {
  const maxSlots = opts.maxSlots ?? DEFAULT_AMS_SLOTS;
  const slots: AmsSlot[] = [{ slot: 1, paletteName: null, hex: null }];
  const slotOfName = new Map<string, number>(); // palette name → slot
  const hexOfName = new Map<string, string>(); // palette name → the hex it first resolved to
  const assignments = new Map<string, Map<string, number>>();

  for (const sc of sidecars) {
    const perRegion = new Map<string, number>();
    for (const part of sc.parts) {
      perRegion.set(part.region, slotForPart(part, sc.coaster, slots, slotOfName, hexOfName));
    }
    assignments.set(sc.coaster, perRegion);
  }

  if (slots.length > maxSlots) {
    const names = slots
      .slice(1)
      .map((s) => s.paletteName)
      .join(", ");
    throw new Error(
      `plate needs ${slots.length} logical filament slots (default + ${slots.length - 1} palettes: ` +
        `${names}) but the AMS has ${maxSlots}. Reduce distinct region colours, or pass the real ` +
        `AMS capacity (multiple units) as maxSlots.`,
    );
  }
  return { slots, assignments };
}

/** Resolve one region body to a slot, registering a newly-seen palette name (mutates the maps). */
function slotForPart(
  part: CoasterPartEntry,
  coaster: string,
  slots: AmsSlot[],
  slotOfName: Map<string, number>,
  hexOfName: Map<string, string>,
): number {
  if (part.paletteName === null) return 1; // untagged ⇒ the plate default filament
  const name = part.paletteName;
  const hex = part.hex ?? "";
  const seenHex = hexOfName.get(name);
  if (seenHex !== undefined && seenHex !== hex) {
    throw new Error(
      `palette "${name}" resolves to two colours (${seenHex} and ${hex}, on coaster ${coaster}) — ` +
        `a palette name must name one colour across the plate.`,
    );
  }
  const existing = slotOfName.get(name);
  if (existing !== undefined) return existing;
  const slot = slots.length + 1;
  slots.push({ slot, paletteName: name, hex });
  slotOfName.set(name, slot);
  hexOfName.set(name, hex);
  return slot;
}

/** The plate's default filament type + preset id, reused for every colour slot (same material,
 *  colour overridden per slot). filament_id MUST be non-empty or the slot silently routes to the
 *  external spool (§6). */
export interface FilamentDefaults {
  type: string; // e.g. "PLA"
  id: string; // a non-empty Bambu preset id
  hex: string; // the default filament's colour (slot 1)
}
/** Parallel arrays for `project_settings.config` (§6): one entry per logical slot, in slot order.
 *  Every colour slot reuses the default's type + id (same material) and overrides only the colour. */
export interface FilamentArrays {
  filament_type: string[];
  filament_colour: string[];
  filament_id: string[];
}
export function filamentArrays(map: AmsSlotMap, defaults: FilamentDefaults): FilamentArrays {
  const filament_type: string[] = [];
  const filament_colour: string[] = [];
  const filament_id: string[] = [];
  for (const s of map.slots) {
    filament_type.push(defaults.type);
    filament_id.push(defaults.id);
    filament_colour.push(s.paletteName === null ? defaults.hex : (s.hex ?? defaults.hex));
  }
  return { filament_type, filament_colour, filament_id };
}

/** The 1-based `extruder` slot for one coaster region — the value the 3MF assembler (4b-ii) writes
 *  as `<metadata key="extruder" value="K"/>` on that region's part. Throws if the region is unknown
 *  (a sidecar the map was not built from). */
export function extruderForRegion(map: AmsSlotMap, coaster: string, region: string): number {
  const slot = map.assignments.get(coaster)?.get(region);
  if (slot === undefined) {
    throw new Error(`no slot for coaster "${coaster}" region "${region}" — was its sidecar in the map?`);
  }
  return slot;
}
