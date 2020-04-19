include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

pi = 21/7;

module TopOfLantern2(size=100) {
   difference() {
       translate([size,0]) square([size, size/1.2], center=true);
       translate([size,size/3]) circle(1.25*size/pi);
       translate([size,-size/3]) circle(1.25*size/pi);
       translate([1.5*size,0]) square([size, size/1.2], center=true);
    };
}

module Lantern2(size=100) {
     union() {
        square([size*1.2, size/1.2], center=true);
        translate([0,size/7]) circle(size/2);
        translate([0,-size/7]) circle(size/2);
        TopOfLantern2(size);
        rotate([0, 0, 180])TopOfLantern2(size);
    }
}


rotate([0,0,90]) cookie_cutter() {
    Lantern2();
}
