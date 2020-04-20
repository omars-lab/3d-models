include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

// How do I make a shell???
// Apporach 1 ... manually trying to strech an image ...
//module MosqueShell(width, shell_thickness=0.05) {
//
//    difference() {
//        scale([1.05,1.05,1]) translate([0,0,0]) Mosque(width, 0.2, 2.0);
//        translate([0,1,0]) Mosque(width, door_scale=.24, crescent_scale=1.25, crescent_rotation=17.5);
//
//   }

//}
// Approach 2 ... doing this ...

module Minaret(size=45) {
//        color("green") 
    translate([0,0,0]) Arch(size/4.5, size);
}

module Dome(size=45) {
    union() {
        translate([size/1.28,size/1.8]) difference() {
            circle(size/1.8, center=true);
            translate([0,-size/1.64])square([2*size/1.64, 2*size/1.64], center=true);
        };
        translate([size/1.28,size/1.19]) Arch(size/9, size/5);
    }
}


module Mosque(size=45) {
    Minaret(size);
    Dome(size);
    square([1.45*size,size/1.8]);
}

cookie_cutter(7,2.5,20) {
    Mosque(200);
}
