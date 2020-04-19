include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>


module CrescentWithStar() {
    union() {
        CrescentV2(10, 6.5, [3.75,3.75,0], edge_rounding=0.35);
        translate([3.5,3.5]) rotate([0,0,35]) scale([0.825,0.825]) Star(5,4);
    }
}

// Turned out weird because of the floating piece in the middle ...
//cookie_cutter() {
//    CrescentWithStar();
//};

cookie_cutter() {
    scale([10,10]) CrescentV2(10, 7.5, [3.5,3.5,0], edge_rounding=0.25);
}
