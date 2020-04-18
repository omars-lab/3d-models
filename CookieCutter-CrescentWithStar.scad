include <BasicShapes.scad>
include <ComplexShapes.scad>
include <CookieCutter.scad>


module CrescentWithStar() {
    union() {
        CrescentV2(10, 7.5, [3.5,3.5,0], edge_rounding=0.25);
        translate([2.75,3.75]) rotate([0,0,22.5]) scale([0.875,0.875]) Star(5,4);
    }
}

// Turned out weird because of the floating piece in the middle ...
//cookie_cutter() {
//    CrescentWithStar();
//};

cookie_cutter() {
    scale([10,10]) CrescentV2(10, 7.5, [3.5,3.5,0], edge_rounding=0.25);
}