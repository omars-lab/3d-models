include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

cookie_cutter(15,7.5,50) {
    scale([1, 1, 0.1]) import("CamelCookieCutter.svg", invert=True);
}

