#!/usr/bin/env bash
# slice-smoke.sh — regression guard for the bambu slice path.
#
# Slices an STL with the known-good X2D trio passed *by preset display name* (not JSON paths) and
# asserts the sliced 3mf carries the X2D gcode header. This is the check that would have caught the
# 2026-09-16 break where `--load-settings` was fed preset names the BambuStudio CLI could not find
# ("can not find setting file"): the fix teaches `bambu slice` to resolve a name → its bundled JSON,
# and this script proves that resolution still works end-to-end.
#
# Usage:  slice-smoke.sh [path/to/model.stl]
#   default model: build/stls/ClassicBrick.stl (a simple LEGO brick — fast to slice)
# Requires: BambuStudio.app installed; Node pinned (v22.22.3). Exits non-zero on any failure.
set -euo pipefail

# Repo root is four levels up from .claude/skills/bambu/scripts/.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"

# Absolute STL path (the CLI resolves relative paths against tools/bambu when run via npm --prefix).
MODEL="${1:-$REPO_ROOT/build/stls/ClassicBrick.stl}"
case "$MODEL" in /*) : ;; *) MODEL="$REPO_ROOT/$MODEL" ;; esac
if [[ ! -f "$MODEL" ]]; then
  echo "slice-smoke: no such model: $MODEL" >&2
  echo "  (render one first, e.g. \`make orbs\`, or pass an STL path)" >&2
  exit 2
fi

# The CLI router imports every backend at load (mqtt among them, added with the first-party MQTT
# backend, #188). A node_modules predating that dep fails deep inside the router with an opaque
# ERR_MODULE_NOT_FOUND for 'mqtt' — not an obvious "install your deps". Preflight it here.
if [[ ! -d "$REPO_ROOT/tools/bambu/node_modules/mqtt" ]]; then
  echo "slice-smoke: bambu CLI deps missing (no tools/bambu/node_modules/mqtt)." >&2
  echo "  run: npm --prefix \"$REPO_ROOT/tools/bambu\" install" >&2
  exit 2
fi

OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT
OUT_3MF="smoke.sliced.3mf"

# The known-good X2D Plate-1 trio, BY NAME (the whole point: resolution must turn these into JSON).
MACHINE="Bambu Lab X2D 0.4 nozzle"
PROCESS="0.20mm Standard @BBL X2D"
FILAMENT="Bambu PLA Basic @BBL X2D 0.4 nozzle"

echo "slice-smoke: slicing $(basename "$MODEL") with the X2D trio by name…"
"$REPO_ROOT/tools/bambu/bin/bambu" slice plate "$MODEL" \
  --settings "$MACHINE;$PROCESS" \
  --filament "$FILAMENT" \
  --out "$OUT_3MF" --outputdir "$OUT" --timeout 180

GCODE="$(unzip -p "$OUT/$OUT_3MF" "Metadata/plate_1.gcode" 2>/dev/null || true)"
fail=0
if ! grep -q "printer_model = Bambu Lab X2D" <<<"$GCODE"; then
  echo "slice-smoke: FAIL — gcode is missing 'printer_model = Bambu Lab X2D'" >&2; fail=1
fi
if ! grep -q "nozzle_diameter = 0.4,0.4" <<<"$GCODE"; then
  echo "slice-smoke: FAIL — gcode is missing 'nozzle_diameter = 0.4,0.4' (dual nozzle)" >&2; fail=1
fi
if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

LAYERS="$(grep -c '^; CHANGE_LAYER' <<<"$GCODE" || true)"
echo "slice-smoke: PASS — X2D gcode header present, ${LAYERS} layer changes."
