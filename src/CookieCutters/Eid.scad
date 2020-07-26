include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

cookie_cutter(7,2.5,15) {
    scale([20,25,1]) text("Eid", font = "Tingler Script");
//    scale([20,25,1]) text("Adha", font = "Tingler Script");
}