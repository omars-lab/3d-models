include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

// The Kaaba is an iconic cube. As a cookie cutter the faithful silhouette
// is a clean square with very slightly softened corners (so the print and
// the dough release cleanly). Earlier versions added wide, flat triangular
// "peaks" that made the outline read as a hexagon / house rather than a cube.

module kaabah(size) {
    corner = size * 0.06;          // subtle corner rounding
    side   = size * 8 * 1.9;       // overall edge length (kept close to old footprint)
    offset(r = corner) offset(r = -corner)
        square([side, side], center = true);
}

//kaabah(10);

cookie_cutter(7,2.5,15) {
    kaabah(10);
}
