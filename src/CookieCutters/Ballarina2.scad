include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

cookie_cutter(15,7.5,25) {
    mirror([1,0,0]) scale([1, 1, 0.1]) import("Ballarina2.svg", invert=True);
}
