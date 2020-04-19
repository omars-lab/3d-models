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

module Minaret() {
//        color("green") 
    translate([ 0,0,0]) Arch(10, 45);
}

module Dome() {
    union() {
        translate([35,25]) difference() {
            circle(27.5, center=true);
            translate([0,-27.5])square([27.5*2, 27.5*2], center=true);
        };
        translate([35,42]) Arch(5, 9);
    }
}


module Mosque(width, door_scale=0.25, door_stretch=0, crescent_scale=1, crescent_rotation=0) {
    Minaret();
    Dome();
    square([65,25]);
}

cookie_cutter() {
    Mosque();
}
