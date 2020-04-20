include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

use <dotSCAD/src/bezier_curve.scad>;
use <dotSCAD/src/polyline2d.scad>;
use <dotSCAD/src/arc.scad>;

// Attempt 1 ...
//module Lantern3() {
//    round_edges(0.4 ) difference() {
//        union() {
//            scale([5,5,1]) polygon([[-1/2,0], [0,1], [1/2,0]]);
//            translate([0,5,0]) rotate([0,0,180]) scale([3,3,1]) polygon([[-1/2,0], [0,1], [1/2,0]]);
//
//        }
//        translate([0.7, 5.5,0]) rotate([0,0,180]) polygon([[-1/2,0], [0,1], [1/2,0]]);
//        translate([-0.8,5.5,0]) rotate([0,0,180]) polygon([[-1/2,0], [0,1], [1/2,0]]);
//        translate([0,   5.5,0]) rotate([0,0,180]) polygon([[-1/2,0], [0,1], [1/2,0]]);
//    }
//}

module bottom_curve(size=40, outline_width=4) {
    t_step = 0.05;
    p0 = [0, 0, 0];
    p1 = [size/2, size/2, 0];
    p2 = [size, 0, 0];
    points = bezier_curve(t_step,
        [p0, p1, p2]
    );
    polyline2d(points, outline_width);
}

module latern_bottom(size=40, outline_width=4) {
    mirror([0,1,0]) union() {
        translate([size*0,0,0]) bottom_curve(size,outline_width);
        translate([size*1,0,0]) bottom_curve(size,outline_width);
        translate([size*2,0,0]) bottom_curve(size,outline_width);
    }
}

module latern_side(orientation="left", size=40, outline_width=4) {
    t_step = 0.05;
    side = size*3;
    h_plane = orientation == "left" ? size*3 : 0 ;
    v_plane = orientation == "left" ? -1 * size * 1.75 : size * 1.75 ;
    p0 = [h_plane, 0, 0];
    p1 = [h_plane + v_plane, size*1, 0];
    p2 = [h_plane, size*3, 0];
    points = bezier_curve(t_step, [p0, p1, p2]);
    polyline2d(points, outline_width);
}

module latern_top(orientation="left", size=40, outline_width=4) {
    t_step = 0.05;
    width = size/10;
    side = size*3;
    h_plane = orientation == "left" ? size*3 : 0 ;
    v_plane = orientation == "left" ? -1 * size : size ;
    p0 = [h_plane, size*3, 0];
    p1 = [h_plane+(v_plane/1.2), size*3+size/2.75, 0];
    p2 = [h_plane+v_plane*1.25, size*3+size/1.1, 0];
    points = bezier_curve(t_step, [p0, p1, p2]);
    polyline2d(points, outline_width);
//    %translate([h_plane+(v_plane/1.2), size*3+size/2, 0]) circle(2);
}

module latern_tip(size=40, outline_width=4) {
    translate([size*1.5, size*4.1]) arc(radius = size/3.25, angle = [-42.5, 222.5], width=outline_width, width_mode = "LINE_OUTWARD");
}

module _Lantern3(size=40, outline_width=4) {
    union() {
        latern_bottom(size, outline_width);
        latern_side("left", size, outline_width);
        latern_side("right", size, outline_width);
        latern_top("left", size, outline_width);
        latern_top("right", size, outline_width);
        latern_tip(size, outline_width);
    }
}

module Lantern3(size=40, outline_width=4) {
    union() {
        for ( i = [0 : 1 : size] ){
            translate([i*1.5,i*1.5]) _Lantern3(size=size-i, outline_width=outline_width);
        }
    }
}
//translate([0,0])         Lantern3(size=40,   outline_width=4);
//translate([3.75,3.75])   Lantern3(size=37.5, outline_width=4);
//translate([7.5,7.5])     Lantern3(size=35,   outline_width=4);
//translate([11.25,11.25]) Lantern3(size=32.5, outline_width=4);
//translate([15,15])       Lantern3(size=30,   outline_width=4);
//translate([18.75,18.75])   Lantern3(size=27.5, outline_width=4);
//translate([22.5,22.5])   Lantern3(size=25,   outline_width=4);
//translate([30,30])       Lantern3(size=20,   outline_width=4);
//translate([37.5,37.5])   Lantern3(size=15,   outline_width=4);

////cookie_cutter() {
//    difference() {
////        square([500,500], center=true);
//        minkowski(size=100) {
//            Lantern3(outline_width=0.01);
//            circle(1, center=true);
//        }
//        Lantern3(outline_width=0.01);
//    }
////}
//

 cookie_cutter(10, 4, total_height=30) {
//     _Lantern3(100);
     Lantern3(100);
 }




//
//module bottom_curve(size=40, outline_width=4, orient="left") {
//    t_step = 0.05;
//    p00 = orient=="left" ? [-size/2, 0, 0] : [size+size/2, 0, 0];
//    p0 = [0, 0, 0];
//    p1 = [size/2, size/2, 0];
//    p2 = [size, 0, 0];
//    _points = orient=="left" ? [p0, p1, p2] : [p0, p1, p2];
////    _points = orient=="left" ? [p00, p0, p1, p2] : [p0, p1, p2, p00];
//    points = bezier_curve(t_step, _points);
//    union() {
//        polyline2d(points, outline_width);
//        polyline2d(orient=="left" ? [p00, p0] : [p2, p00], outline_width);
//    }
//}
//
//module latern_bottom(size=40, outline_width=4) {
//    union() {
//        translate([size*0 + size/2,0,0]) bottom_curve(size,outline_width,"left");
//        translate([size*1.5,0,0]) bottom_curve(size,outline_width,"right");
//    }
//}
