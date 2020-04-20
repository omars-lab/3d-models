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

module Door() {
    difference(){
        translate([ 0,0,0])color("green")Arch(13, 13);
        translate([ 0,0.5,0])Arch(12, 12);
    }
}

module Mosque(width, door_scale=0.25, door_stretch=0, crescent_scale=1, crescent_rotation=0) {
    crescent_size = width/10;
    arc_factor = width/2;

    square_height =  width+(width/10);
    crescent_height = crescent_size;
    arc_height = 1.5*width/5 ;
    total_height = square_height + arc_height + crescent_height;
//    echo(total_height, width, total_height/width);

    union() {
        translate([0,square_height+arc_height+crescent_height,0])
            Crescent(crescent_size, crescent_scale, rotate=crescent_rotation);
        difference() {
            translate([-width/2,0,0])square([width, width+(width/10)]);
            scale([2,1,1]) Arch(width*door_scale,2*width*door_scale, door_stretch);
        }
        translate([0,square_height,0]) scale([1.5,1.5,1]) HalfCircle(width/5);
    }
}

cookie_cutter(9,3.5,25) {
    Mosque(200, crescent_scale=0.9, crescent_rotation=30);
}


////Mosque(20);
