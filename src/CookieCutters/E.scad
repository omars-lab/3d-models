include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

cookie_cutter(7,2.5,20) {
    scale([20,25,1]) text("E", font = "Tre:style=Bold");
}
