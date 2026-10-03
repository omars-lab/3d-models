// Was this slice made from the plate's recipe as it is now?
//
// A plate's recipe (docs/design/plates/<plate>.yaml) can change after its .3mf was sliced: an item
// swapped, a count changed, a param moved. The old slice still sits in build/plates/ and nothing at
// the send said it was out of date; the send-plate skill asked a person to compare file times. Omar,
// 2026-10-03: "see if we need a hook to ensure we sliced right". So the slice verbs write the
// recipe's hash into the warnings sidecar beside the .3mf (warnings.ts), and the send compares it
// with the recipe's hash now. Both come from one implementation, iterations.py's `recipe_hash`, read
// through `plate_approve.py --status --json`: content, not text, so a comment edit is not a change,
// the same rule that resets an approval (D-097).
//
// What it does not cover: a change in the bikar sources the recipe names. The recipe hash is the
// recipe's own content; a .bkr edited under an unchanged recipe is not seen here.
// PURE: both hashes are passed in.

export interface SliceFresh {
  ok: boolean; // false: refuse the send
  mark: "✓" | "⚠" | "✗";
  line: string; // without the mark
}

/** May a slice that recorded `sliced` go out when the recipe hashes to `now`? */
export function checkSliceFresh(sliced: string | undefined | null, now: string | null): SliceFresh {
  if (!now) {
    return { ok: true, mark: "⚠", line: "slice: the plate has no recipe to compare it with" };
  }
  if (!sliced) {
    return {
      ok: false,
      mark: "✗",
      line: "slice: it does not say which recipe it was made from (sliced before slices recorded it). Slice it again",
    };
  }
  if (sliced !== now) {
    return {
      ok: false,
      mark: "✗",
      line: `slice: the recipe changed since this slice (sliced from ${sliced}, now ${now}). Slice it again`,
    };
  }
  return { ok: true, mark: "✓", line: `slice: made from the recipe as it is now (${now})` };
}

