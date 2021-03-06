include <BasicShapes.scad>

module HalfCylinder(r, h, e=1, center=false) {
    translate([0,0, center ? -h/2 : 0])difference(){
        cylinder(h,r,r);
        translate([0,-r,-e])cube([2*r,2*r,h+2*e]);
    }
}

module HalfCircle(r) {
    difference(){
        circle(r);
        translate([-r,-2*r,0]) square(2*r);
    }
}

// http://benjamin-engel.blogspot.com/2015/07/openscad-tips-and-tricks.html

module equilateral_triangle(h) {
    rotate([0,0,-30]) circle(r=h, $fn=3);
}

module Crescent(r, fatten_scale=1, curve_angle=0, rotate=0) {
    r_prime = r / fatten_scale;
    rotate([0,0,rotate]) difference() {
        circle(r_prime*1.1);
        translate([r_prime/4, curve_angle*r_prime/4, 0]) circle(r_prime*fatten_scale);
    }
}


module round_edges(r) {
    minkowski() {
        children();
        circle(r);
    };
}

module CrescentV2(outer_r, inner_r, r_shift, edge_rounding=2) {
    // Different way to construct ... rounded edges ...
   round_edges(edge_rounding) {
        difference() {
            circle(outer_r);
            translate(r_shift) circle(inner_r);
        };
    };
}


//module Arch(x,y,r) {
//    // http://kitwallace.co.uk/Blog/item/2013-01-28T17:59:00Z
//    union() {
//        intersection() {
//           translate([x,y,0]) circle(r);
//           translate([-x,y,0]) circle(r);
//        }
//        translate([0,y/2,0]) square(size=[2 * (r-x), y], center=true);
//    }
//}

module Arch(width, arc_height, strech_height=0) {
    // http://kitwallace.co.uk/Blog/item/2013-01-28T17:59:00Z
    r = arc_height;
    x = (width / 2) - r;
    y = arc_height + strech_height;
    union() {
        intersection() {
           translate([x,y,0]) circle(r);
           translate([-x,y,0]) circle(r);
        }
        translate([0,y/2,0]) square(size=[width, y], center=true);
    }
}
