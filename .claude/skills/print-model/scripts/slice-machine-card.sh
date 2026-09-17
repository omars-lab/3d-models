#!/usr/bin/env bash
# slice-machine-card.sh — slice the whole 23-rung machine card onto ONE X2D plate, brim OFF.
#
# WHY THIS EXISTS (provenance, 2026-09-17, PR #210):
#   Two facts surfaced slicing Plate 1 for task #9, and this script is the runnable form of both
#   (print-model best-practices.md "Our examples"; rubric.md §Self-healing, Track 2 + Reusable scripts):
#     1. The card is 23 separate STLs with no composite. They still slice onto one plate in one command:
#        one rung as the `slice plate <model>` positional, the other 22 after `--`, plus `--arrange`.
#     2. The shipped `0.20mm Standard @BBL X2D` process defaults `brim_type = auto_brim`, which SILENTLY
#        brims the MC-6 towers — invalidating CAL-BED-01 (and masking MC-5 warp). We must force
#        `brim_type = no_brim` plate-wide. Headless, an inheriting stub is rejected "process not
#        compatible with printer", so we materialize the FULL process JSON with only brim_type flipped.
#
# THIS IS A FALLBACK. The proper home is a `bambu slice plate … --no-brim` flag (owned by the bambu CLI
#   / the slice pre-flight branch, PR #185). When that flag lands, delete this script and call the flag.
#
# Slicer settings here are MEASUREMENTS fixed by the bench sheet, not preferences (calibration-design §4):
#   supports OFF (MC-4 fan), no brim / no raft (MC-6 towers, MC-5 warp). Do not "tidy" them.
#
# Usage:
#   .claude/skills/print-model/scripts/slice-machine-card.sh [COUPON_DIR] [OUT_3MF]
# Env overrides (defaults are the known-good X2D trio, memory: bambu-x2d-bringup):
#   MACHINE, PROCESS, FILAMENT, TIMEOUT
set -euo pipefail

export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"   # repo rule: system Node is too old

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
BAMBU="$REPO_ROOT/tools/bambu/bin/bambu"
COUPON_DIR="${1:-$REPO_ROOT/build/stls/coupons/machine-card}"
OUT_3MF="${2:-plate-1-machine-card.sliced.3mf}"

MACHINE="${MACHINE:-Bambu Lab X2D 0.4 nozzle}"
PROCESS="${PROCESS:-0.20mm Standard @BBL X2D}"
FILAMENT="${FILAMENT:-Bambu PLA Basic @BBL X2D 0.4 nozzle}"
TIMEOUT="${TIMEOUT:-420}"

STUDIO_PROFILES="/Applications/BambuStudio.app/Contents/Resources/profiles/BBL"
SRC_PROCESS="$STUDIO_PROFILES/process/$PROCESS.json"

# Collect the rungs. The card is exactly its STLs — do not filter or reorder.
shopt -s nullglob
RUNGS=("$COUPON_DIR"/*.stl)
shopt -u nullglob
if [[ ${#RUNGS[@]} -eq 0 ]]; then
  echo "no STLs in $COUPON_DIR — run 'make coupons' first (regenerates the 23 rungs)." >&2
  exit 1
fi
echo "coupons: ${#RUNGS[@]} rung(s) in $COUPON_DIR"

# Materialize the process with brim_type flipped to no_brim (the full JSON, so compatible_printers rides).
if [[ ! -f "$SRC_PROCESS" ]]; then
  echo "shipped process not found: $SRC_PROCESS" >&2
  echo "Check the BambuStudio version / process name (\`bambu setup studio\` lists X2D profiles)." >&2
  exit 1
fi
CARD_PROCESS="$(mktemp -t card-process.XXXXXX.json)"
trap 'rm -f "$CARD_PROCESS"' EXIT
python3 - "$SRC_PROCESS" "$CARD_PROCESS" "$PROCESS" <<'PY'
import json, sys
src, dst, name = sys.argv[1], sys.argv[2], sys.argv[3]
c = json.load(open(src))
c["name"] = f"{name} (card no-brim)"
c["brim_type"] = "no_brim"
json.dump(c, open(dst, "w"), indent=1)
PY

# One rung is the positional; the rest ride after `--` as raw model files; --arrange packs them.
"$BAMBU" slice plate "${RUNGS[0]}" \
  --arrange \
  -s "$MACHINE;$CARD_PROCESS" \
  -f "$FILAMENT" \
  -o "$OUT_3MF" \
  -d "$COUPON_DIR" \
  -t "$TIMEOUT" \
  -- "${RUNGS[@]:1}"

echo "sliced → $COUPON_DIR/$OUT_3MF   (brim OFF, supports OFF, raft OFF; verify with the .3mf config)"
