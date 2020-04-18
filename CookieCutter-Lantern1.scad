include <BasicShapes.scad>
include <ComplexShapes.scad>
include <CookieCutter.scad>

pi = 21/7;

//https://www.google.com/search?q=lantern+svg+arab+cookie+cutter&tbm=isch&ved=2ahUKEwijy_z_kOfoAhUV_6wKHYdRDEsQ2-cCegQIABAA&oq=lantern+svg+arab+cookie+cutter&gs_lcp=CgNpbWcQA1DZzwFYi90BYIneAWgAcAB4AIABQIgBiAaSAQIxNJgBAKABAaoBC2d3cy13aXotaW1n&sclient=img&ei=KEOVXqOXGJX-swWHo7HYBA&bih=899&biw=1680&rlz=1C5CHFA_enUS815US815#imgrc=zVpryMX5PRFfeM&imgdii=zC5WgQe_cj3uLM

//https://www.google.com/search?q=lantern+svg+arab+cookie+cutter&tbm=isch&ved=2ahUKEwijy_z_kOfoAhUV_6wKHYdRDEsQ2-cCegQIABAA&oq=lantern+svg+arab+cookie+cutter&gs_lcp=CgNpbWcQA1DZzwFYi90BYIneAWgAcAB4AIABQIgBiAaSAQIxNJgBAKABAaoBC2d3cy13aXotaW1n&sclient=img&ei=KEOVXqOXGJX-swWHo7HYBA&bih=899&biw=1680&rlz=1C5CHFA_enUS815US815#imgrc=NUgwm3IHPtpIDM

//https://www.google.com/search?q=lantern+svg+arab+cookie+cutter&tbm=isch&ved=2ahUKEwijy_z_kOfoAhUV_6wKHYdRDEsQ2-cCegQIABAA&oq=lantern+svg+arab+cookie+cutter&gs_lcp=CgNpbWcQA1DZzwFYi90BYIneAWgAcAB4AIABQIgBiAaSAQIxNJgBAKABAaoBC2d3cy13aXotaW1n&sclient=img&ei=KEOVXqOXGJX-swWHo7HYBA&bih=899&biw=1680&rlz=1C5CHFA_enUS815US815#imgrc=zVpryMX5PRFfeM


//https://www.etsy.com/listing/687654882/ramadan-cookie-cutters-set-of-9?gpla=1&gao=1&&utm_source=google&utm_medium=cpc&utm_campaign=shopping_us_housewarming_Craft_Supplies_and_Tools&utm_custom1=e12205a9-1426-4d66-9c46-fd49f0a70718&utm_content=go_1707294187_63430325701_331635217662_pla-295462056867_c__687654882&utm_custom2=1707294187&gclid=EAIaIQobChMIt8rz3Yrn6AIVRNbACh0UDAPnEAQYBCABEgLFWfD_BwE

//http://forum.openscad.org/Rounded-Polygon-td21897.html

module rod_with_clipped_circle(square_d, circle_d, circle_placement) {
    difference() {
        square(square_d, center=true);
        translate(circle_placement) circle(circle_d, center=true);
    }
}


module TopOfLantern2(size=100) {
   difference() {
       translate([size,0]) square([size, size/1.2], center=true); 
       translate([size,size/3]) circle(1.25*size/pi);
       translate([size,-size/3]) circle(1.25*size/pi);
       translate([1.5*size,0]) square([size, size/1.2], center=true); 
    };
}

module Lantern2(size=100) {
     union() {
        square([size*1.2, size/1.2], center=true);
        translate([0,size/7]) circle(size/2);
        translate([0,-size/7]) circle(size/2);
        TopOfLantern2(size);
        rotate([0, 0, 180])TopOfLantern2(size);
    }
}


module bottom_lantern_1(arch_height = 40) {
    size = arch_height/10;
    translate([0, -arch_height]) difference() {
        union() {
            Arch(arch_height, (2/3)*arch_height);
            translate([0, arch_height + arch_height/3.95]) scale([5,5,1]) polygon([[-1/2,0], [0,1], [1/2,0]]);
        }
        translate([arch_height*0.725, arch_height*1.125]) rotate([0,0,90]) 
            rod_with_clipped_circle([size*1.5,size*10], size, [-size/1.25,size*5]);
        mirror([1,0,0]) {
            translate([arch_height*0.725, arch_height*1.125]) rotate([0,0,90]) 
                rod_with_clipped_circle([size*1.5,size*10], size, [-size/1.25,size*5]);
        }
        square([arch_height*2,arch_height*2], center=true);
    }
}

module TopOfLantern1(size=10) {
    difference() {
        translate([size,0]) square([size,size], center=true);
        rod_with_clipped_circle([size,size], 5, [size-5]);
    }
}

module Lantern1(size=40) {
    union() {
        rotate([0, 0, 90]) difference() {
            square([size,size*2], center=true);
            translate([0,size*1.5]) circle(size);
            translate([0,-size*1.5]) circle(size);
        }
        translate([0,size/2]) round_edges(0.9) bottom_lantern_1(size*5/4);
        mirror([0,1,0]) translate([0,size/2]) round_edges(0.9) bottom_lantern_1(size*5/4);
    }
}

module Lantern3() {
    round_edges(0.4 ) difference() {
        union() {
            scale([5,5,1]) polygon([[-1/2,0], [0,1], [1/2,0]]);
            translate([0,5,0]) rotate([0,0,180]) scale([3,3,1]) polygon([[-1/2,0], [0,1], [1/2,0]]);

        }
        translate([0.7, 5.5,0]) rotate([0,0,180]) polygon([[-1/2,0], [0,1], [1/2,0]]);
        translate([-0.8,5.5,0]) rotate([0,0,180]) polygon([[-1/2,0], [0,1], [1/2,0]]);
        translate([0,   5.5,0]) rotate([0,0,180]) polygon([[-1/2,0], [0,1], [1/2,0]]);
    }
}

//Lantern3();

//cookie_cutter() {
//    Lantern1(50);
//    Lantern2();
//}

