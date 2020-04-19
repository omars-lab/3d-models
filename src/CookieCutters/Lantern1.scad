include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

module bottom_lantern_1(arch_height = 40) {
    size = arch_height/10;
    translate([0, -arch_height]) difference() {
        union() {
            Arch(arch_height, (2/3)*arch_height);
            translate([0, arch_height + arch_height/3.95]) scale([5,5,1]) polygon([[-1/2,0], [0,1], [1/2,0]]);
        }
        translate([arch_height*0.725, arch_height*1.125]) rotate([0,0,90])
            rod_with_clipped_circle([size*1.5,size*10], size, [-size/1.25,size*5]);
        mirror([1,0,0]) {
            translate([arch_height*0.725, arch_height*1.125]) rotate([0,0,90])
                rod_with_clipped_circle([size*1.5,size*10], size, [-size/1.25,size*5]);
        }
        square([arch_height*2,arch_height*2], center=true);
    }
}

module TopOfLantern1(size=10) {
    difference() {
        translate([size,0]) square([size,size], center=true);
        rod_with_clipped_circle([size,size], 5, [size-5]);
    }
}

module Lantern1(size=40) {
    union() {
        rotate([0, 0, 90]) difference() {
            square([size,size*2], center=true);
            translate([0,size*1.5]) circle(size);
            translate([0,-size*1.5]) circle(size);
        }
        translate([0,size/2]) round_edges(0.9) bottom_lantern_1(size*5/4);
        mirror([0,1,0]) translate([0,size/2]) round_edges(0.9) bottom_lantern_1(size*5/4);
    }
}

cookie_cutter() {
    Lantern1(50);
}
