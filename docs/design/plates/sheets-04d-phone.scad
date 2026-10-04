// The phone alone (first for sheets-04d, a plate removed since; now phones-01 and phones-02), cut out of the iPhone 16 Pro model.
//
// The model is two bodies 2 mm apart at x = 81.2: the phone (x < 81.2, screen down, lenses and
// logo up) and a case (x > 81.2). Sliced on their own on 2026-10-03, the phone as modeled was the
// only one of four tries with no warning: the case is "floating cantilever" open side down (its
// back hangs over the hollow) and open side up (it stands on its raised camera ring), and the
// phone turned over is "floating regions" (it stands on its lenses). So the plate carries the
// phone and leaves the case off.
//
// Neither file is in git (the model's license, see phones-02.yaml). From the repo root:
//   OpenSCAD -o .bambu/imports/iphone-16-pro-phone.stl docs/design/plates/sheets-04d-phone.scad
// then put the output's sha256 in the recipe that uses it.

intersection() {
  import("../../../.bambu/imports/iphone-16-pro.stl");
  translate([0, 0, -1]) cube([81.2, 200, 10]);
}
