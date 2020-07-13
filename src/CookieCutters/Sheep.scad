include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>

cookie_cutter(7,2.5,20) {
    scale([1, 1, 0.1]) import("SheepCookieCutter.svg", invert=True);
}

