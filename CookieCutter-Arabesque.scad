include <BasicShapes.scad>
include <ComplexShapes.scad>
include <CookieCutter.scad>

module OuterStars(count, star_points, star_size, distance_factor=1) {
    union() {
        for (p = [1 : count]) {
            // inplace_rotation = (p % 4 == 1) ? -18 : ( (p % 4 == 2) ? -18 : ( (p % 4 == 3) ? -18: -18));
            inplace_rotation = - 90 / star_points;
            rotate([0,0, (60 + p*360/count)+count])
                translate([0, -3.225*count*distance_factor])
                    rotate([0,0, inplace_rotation])
                        Star(star_points, star_size/2.1, star_size);
        }
    }
}

module EightFold(distance_factor=1) {
    difference() {
        rotate([0,0,90])Octagon(24.7);
        OuterStars(8, 5, 10.0, distance_factor=distance_factor);
    }
}

cookie_cutter(2, 1) {
    scale([5,5,1]) EightFold();
}



// Attempt 1: Trying to manually outline ... 

//module InnerFoldShell(shell_thickness) {
//   scale_factor = 1 + shell_thickness;
//   difference() {
//        scale([scale_factor,scale_factor,scale_factor])InnerFold();
//        InnerFold();
//   }
//} 

//module EightFoldShell(shell_thickness) {
//   scale_factor = 1 + shell_thickness;
//   difference() {
//        scale([scale_factor,scale_factor,1])EightFold();
//        EightFold();
//   }
//} 
//
//module EightFoldCookieCutter() {
//    union() {
//          linear_extrude(height = 75, slices = 60) {
//          scale([5, 5, 1]) 
//            intersection() {
//                EightFoldShell(0.3);
//                translate([0,0,0]) rotate([0,0,90]) Octagon(26.7);
//            }
//        }
//    }
//}
//EightFoldCookieCutter();