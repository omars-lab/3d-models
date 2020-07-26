include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

//cookie_cutter(15,7.5,50) {
//    mirror([1,0,0]) scale([1, 1, 0.1]) surface(file="Ballarina.png", invert=True);
//}

// Used the following site to convert the png to svg!
//  https://www.vectorizer.io/images/upload.html

cookie_cutter(15,7.5,50) {
    mirror([1,0,0]) scale([5, 5, 0.1]) import("Ballarina.svg", invert=True);
}
