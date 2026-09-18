#!/usr/bin/env bash
# grid-plate.sh — slice N copies of ONE model on an EVEN, equi-spaced grid (a spread DISPLAY layout).
#
# WHY THIS EXISTS (provenance, 2026-09-18):
#   The sibling slice-copies.sh packs N copies TIGHT (libnest2d --arrange) — minimum bed use, the
#   right default for a production plate. But a *display* ask is the opposite: "spread N copies evenly
#   with room between them and a margin around the edge." A nester cannot express an even grid; it is
#   deterministic placement. grid_plate.py computes the grid FROM THE SHAPE'S FOOTPRINT and the bed,
#   bakes the positions into a .3mf, and this wrapper slices it with --arrange OFF so BambuStudio keeps
#   those authored positions. (print-model best-practices.md "Our examples"; rubric.md §Arrangement.)
#
# THE PRINCIPLE (default guidance for spacing multiple pieces): divide the bed into N equal cells per
#   axis and centre one piece per cell → equal inter-piece gaps AND an edge margin of gap/2. The grid
#   dimension is derived from shape size (N = floor(bed/(footprint+min_gap))), or pass rows x cols for a
#   target count. See grid_plate.py's header for the formula.
#
# THIS IS A FALLBACK. The proper home is a `bambu slice plate … --grid RxC` (or `--layout even`) flag
#   owned by the bambu CLI. When that lands, delete this pair and call the flag.
#
# GOTCHA — same by-design floating-regions caveat as slice-copies.sh: a decorative/organic model warns
#   once per copy; the gated CLI send BLOCKS, so send a fun print via `bambu slice open <plate>` → Print.
#
# Usage:
#   grid-plate.sh <model.stl> <rows> <cols> [extra bambu-slice args…]
#   grid-plate.sh <model.stl> --count <N>   [extra bambu-slice args…]
# Env overrides (defaults = the known-good X2D trio + 256 mm bed):
#   MACHINE, PROCESS, FILAMENT, TIMEOUT, BED, MIN_GAP, MARGIN, OUT, OUTDIR
set -euo pipefail

export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"   # repo rule: system Node is too old

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
BAMBU="$REPO_ROOT/tools/bambu/bin/bambu"
PLACER="$(dirname "${BASH_SOURCE[0]}")/grid_plate.py"

MODEL="${1:?usage: grid-plate.sh <model> <rows> <cols>  |  grid-plate.sh <model> --count <N>}"
shift
if [[ ! -f "$MODEL" ]]; then echo "model not found: $MODEL" >&2; exit 1; fi

# Grid spec: either "<rows> <cols>" or "--count <N>". Remaining args pass through to the slicer.
grid_args=()
if [[ "${1:-}" == "--count" ]]; then
  N="${2:?--count needs a number}"; shift 2
  grid_args=(--count "$N"); label="${N}"
else
  ROWS="${1:?need <rows>}"; COLS="${2:?need <cols>}"; shift 2
  grid_args=(--rows "$ROWS" --cols "$COLS"); label="${ROWS}x${COLS}"
fi

MACHINE="${MACHINE:-Bambu Lab X2D 0.4 nozzle}"
PROCESS="${PROCESS:-0.20mm Standard @BBL X2D}"
FILAMENT="${FILAMENT:-Bambu PLA Basic @BBL X2D 0.4 nozzle}"
TIMEOUT="${TIMEOUT:-1200}"
BED="${BED:-256}"
MIN_GAP="${MIN_GAP:-8}"
base="$(basename "${MODEL%.*}")"
OUT="${OUT:-${base}-grid-${label}.sliced.3mf}"
OUTDIR="${OUTDIR:-$(cd "$(dirname "$MODEL")" && pwd)}"

# Name the intermediate .3mf after the MODEL, not a throwaway token: BambuStudio names the plate's
# object from this filename, so a mktemp token (or a literal, un-expanded "XXXXXX" from `mktemp -t`)
# would leak into the GUI as the object name. A clean name inside a private temp dir gives both.
GRID_TMPDIR="$(mktemp -d -t grid-plate)"
trap 'rm -rf "$GRID_TMPDIR"' EXIT
GRID3MF="$GRID_TMPDIR/${base}.3mf"

# 1. Compute the even grid from the footprint and bake positions into a .3mf.
placer_extra=(--bed "$BED" --min-gap "$MIN_GAP")
[[ -n "${MARGIN:-}" ]] && placer_extra+=(--margin "$MARGIN")
python3 "$PLACER" "$MODEL" --out "$GRID3MF" "${grid_args[@]}" "${placer_extra[@]}"

# 2. Slice WITHOUT --arrange so the authored grid positions are kept (slice plate defaults arrange off).
echo "slicing the grid plate (arrange OFF — keeping authored positions) → $OUTDIR/$OUT"
set +e
"$BAMBU" slice plate "$GRID3MF" \
  -s "$MACHINE;$PROCESS" \
  -f "$FILAMENT" \
  -o "$OUT" \
  -d "$OUTDIR" \
  -t "$TIMEOUT" \
  "$@"
slice_rc=$?
set -e
if [[ ! -f "$OUTDIR/$OUT" ]]; then
  echo "slice failed (exit $slice_rc) — no plate written." >&2
  exit "$slice_rc"
fi
if [[ "$slice_rc" -ne 0 ]]; then
  echo "note: the slicer raised warnings (exit $slice_rc) — review them above." >&2
  echo "      a decorative model's 'floating regions' is usually by-design (supportless overhang);" >&2
  echo "      the CLI 'print send' gate will BLOCK on it — send via 'bambu slice open $OUT' → Print instead." >&2
fi

# 3. Verify the realized plate carries every copy (same rule as slice-copies.sh: a clean slice makes
#    validate authoritative; a warnings slice runs it for the displayed facts only — read them).
EXPECT="$(python3 -c "import sys; a=sys.argv[1:]; print(int(a[a.index('--count')+1]) if '--count' in a else int(a[a.index('--rows')+1])*int(a[a.index('--cols')+1]))" "${grid_args[@]}")"
echo "verifying the grid plate …"
set +e
"$BAMBU" validate sliced "$OUTDIR/$OUT" --expect-objects "$EXPECT" --machine X2D --nozzle 0.4
val_rc=$?
set -e
if [[ "$slice_rc" -eq 0 && "$val_rc" -ne 0 ]]; then
  echo "verify FAILED on a clean slice — a real problem, not a by-design warning." >&2
  exit "$val_rc"
fi
