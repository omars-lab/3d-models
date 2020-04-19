include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

use <dotSCAD/src/shape_arc.scad>;

//module top_curve(size=40, outline_width=4) {
//    t_step = 0.05;
//    p0 = [0, 0, 0];
//    p1 = [size/16, size/1.2, 0];
//    % translate(p1) circle(4);
//    p2 = [size/1.5, size, 0];
//    points = bezier_curve(t_step,
//        [p0, p1, p2]
//    );
//    polyline2d(points, outline_width);
//}

module top_curve(size=40, outline_width=4) {
    shape_pts = shape_arc(radius = size/4, angle = [90, 180], width = size/2);
    translate([size/1.5, 0, 0]) scale([1.5,2]) polygon(shape_pts);
}

module top_bar(size=40, outline_width=4) {
    translate([size/1.6, (5/8)*size, 0]) square([size/6, 3/2*size], center=true);
}

module dome(size=40, outline_width=4) {
    union() {
        top_curve(size);
        translate([(5/4)*size,0]) mirror([1,0,0]) top_curve(size);
        top_bar(size);
    }
}

module Minaret(size=40){
    translate([size/6, 4*size]) dome(size);
    square([1.575*size, size/3+4*size]);
}

cookie_cutter() {
    Minaret(100);
}

