radius = 20;

//difference() {
//  
//    linear_extrude(height = 200*(0.15), slices = 60) {
//      circle(radius, $fn = 8);
//    }
//
//    translate([0,0,-10]) linear_extrude(height = 300*(0.15), slices = 60) {
//         circle(radius/2, spacing, levels);
//    }
// 
//}

radius = 5 ;
//union() {
//rotate_extrude(convexity = 10) 
//    translate([radius*radius*2.5, 0, 0]) 
//        scale([radius*2,radius*2,1]) 
//            circle(r = radius, $fn=12);
//
//    linear_extrude(100) square([3.14*radius*radius*2.5,radius*radius*2.5*3.14], center=true);
//}


    rotate_extrude(convexity = 10) 
        translate([radius*radius*3.25, 0, 0]) 
            scale([radius*2,radius*4,1]) 
                circle(r = radius, $fn=6);