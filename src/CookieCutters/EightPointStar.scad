include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>


module InnerFold(size=20) {
    translate([-size/2, -size/2])
        union() {
            translate([0, 0])rotate([0,0,0])square(size,size);
            translate([size/2, -size/5])rotate([0,0,45])square(size,size);
        }
}

cookie_cutter() {
    InnerFold(150);
}
