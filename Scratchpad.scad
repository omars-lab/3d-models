
module EightFoldCookieCutter() {
    union() {
//        translate([0,0,0])rotate([0,90,0])    HalfCylinder(r=1.25,h=75, center=true);
//        translate([0,0,0])rotate([0,90,45*3]) HalfCylinder(r=1.25,h=75, center=true);
//        translate([0,0,0])rotate([90,90,0])   HalfCylinder(r=1.25,h=75, center=true);
//        translate([0,0,0])rotate([90,90,45*3])HalfCylinder(r=1.25,h=75, center=true);

//        translate([0,0.4,0])linear_extrude(height=7.5, slices = 60) {
//            InnerFoldShell(0.05);
//        }
//        translate([0,0.4,0])linear_extrude(height=2.5, slices = 60) {
//            InnerFold();
//        }
          linear_extrude(height = 75, slices = 60) {
          scale([5, 5, 1]) 
            intersection() {
                EightFoldShell(0.3);
                translate([0,0,0]) rotate([0,0,90]) Octagon(26.7);
            }
        }
    }
}


//scale([5,5,1])Crescent(40, 0.9, 2);
//rotate([0, 0, 70]) Star(5, 50);

//Door();
//Mosque(20);
//linear_extrude(height = 12.5, slices = 60) {
//    MosqueShell(20);
//}
//Arch(5,5,7);



// Understanding how the arch works ...   
//             translate([ 0,0,1])color("green")Arch(2,20,7);
//             translate([ 2,20,0]) circle(7);
//color("blue")translate([-2,20,0]) circle(7);
//
//color("blue") Mosque(62.5);
//translate([0,0,1]) scale(1.2,1.,1) Mosque(62.5);
//MosqueShell(width=62.5);


//Shell(
//    difference() {
//        rotate([0,0,90])Octagon(24.5);
//        OuterStars(8, 5, 10);
//    },
//    0.1
//)
// difference() {
//     Star(12, 10, 20);
//     InnerFold(20)Star(12, 5, 10);
// }
//rotate([0,0,90])Hexagon(20);
//OuterStars(8, 5, 10);
//EightFold();

//rotate([0,90,0]) HalfCylinder(r=1.25, h=75, center=true);