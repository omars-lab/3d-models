include <../BasicShapes.scad>
include <../ComplexShapes.scad>


module hexinder(w = 10, l = 50) {
    // A hexogonal cylinder
    rotate([90, 0, 0]) translate([-w/2 + -w/sqrt(2),0,0]) union() {
        rotate([0,45,0]) square([w,l]);
        rotate([0,-45,0]) square([w,l]);

        translate([w+(2*w/sqrt(2)), 0, 0]) mirror([1,0,0]) rotate([0,-45,0]) square([w,l]);
        translate([w+(2*w/sqrt(2)), 0, 0]) mirror([1,0,0]) rotate([0,45,0]) square([w,l]);

        translate([w/sqrt(2), 0, -w/sqrt(2)]) square([w,l]);
        translate([w/sqrt(2), 0, w/sqrt(2)]) square([w,l]);
    };
}

module octinder(w = 10, l = 50) {
    // A octagonal cylinder
    rotate([90, 0, 0]) translate([-w/2 + -w/sqrt(2),0,0]) union() {
        // top half
        translate([0, 0, w/2]) rotate([0,-45,0]) square([w,l]);
        translate([0, 0, w/2]) translate([w/sqrt(2), 0, w/sqrt(2)]) square([w,l]);        
        translate([0, 0, w/2]) translate([w+(2*w/sqrt(2)), 0, 0]) mirror([1,0,0]) rotate([0,-45,0]) square([w,l]);

        translate([0, 0, -w/2]) rotate([0,-90,0]) square([w,l]);
        translate([(2*w/sqrt(2))+w, 0, -w/2]) rotate([0,-90,0]) square([w,l]);
        
        // bottom half
        translate([0, 0, -w/2]) rotate([0,45,0]) square([w,l]);
        translate([0, 0, -w/2]) translate([w/sqrt(2), 0, -w/sqrt(2)]) square([w,l]);
        translate([0, 0, -w/2]) translate([w+(2*w/sqrt(2)), 0, 0]) mirror([1,0,0]) rotate([0,45,0]) square([w,l]);

    };
}

 octinder(10,15);