# Fixture: D3 must fire on a default with no provenance

Asserted FAIL fixture for rule D3 (K4). This reproduces the tile-wall defect:
a bow figure that appears in no source in either direction, with the capture
depth default then keyed to it.

**Default:** `captureDepthMm = 1.0`, sized against an FDM tile bow of 0.2-0.5 mm
over 100 mm.

Neither a citation nor a CAL-* bet id. Expected: exactly one finding, `D3 (K4)`.
