include <../BasicShapes.scad>
include <../ComplexShapes.scad>
include <Common.scad>



module kaabah_top(size) {
    translate([0,size*8,0]) scale([10,1.5,1]) equilateral_triangle(size);
}

module kaabah_bottom(size) {
    mirror([0,1,0]) kaabah_top(size);    
}

module kaabah_body(size) {
    square([size*8*2.15, size*8*1.815], center=true);
}

module kaabah(size) {
    union() {
        kaabah_body(size);
        kaabah_top(size);
        kaabah_bottom(size);    
    }
}

//kaabah(10);

cookie_cutter(7,2.5,15) {
    kaabah(10);
}
