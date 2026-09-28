// POC 1 + 3 — colour control and flush-vs-lowered, by hand. Straps = the plain
// openwork coaster; each filled orbit = bikar's own orbit-N-filled mesh in its own
// colour. Straps are lifted 0.02 mm so their top wins the preview where the two
// meshes coincide. `drop` lowers the fills: the mesh is shifted down and clipped at
// the bed, so a lowered fill is (height - drop) tall and still stands on the bed.
orbits = [1, 3, 5, 7];
colours = ["#9b1b30", "#1f7a7a", "#d4af37", "#2e4a9e", "#9b1b30", "#1f7a7a", "#d4af37", "#2e4a9e"];
drop = 0;
strap = "#3a2a1a";
color(strap) translate([0, 0, 0.02]) import("plain.stl");
for (o = orbits) color(colours[o]) intersection() {
  translate([0, 0, -drop]) import(str("orbit", o, "-filled.stl"));
  translate([-500, -500, 0]) cube([1000, 1000, 100]);
}
