include <BasicShapes.scad>
include <ComplexShapes.scad>

//https://www.etsy.com/listing/770065287/professional-quality-mosque-cookie?gpla=1&gao=1&&utm_source=google&utm_medium=cpc&utm_campaign=shopping_us_d-craft_supplies_and_tools-kitchen_supplies-kitchen_tools_and_utensils-cookie_cutters&utm_custom1=e12205a9-1426-4d66-9c46-fd49f0a70718&utm_content=go_1843970773_68900286679_346362959724_pla-295472669507_c__770065287&utm_custom2=1843970773&gclid=EAIaIQobChMI5bb_z6re6AIVGKSzCh3zTwPnEAQYBCABEgKdEPD_BwE


// How do I make a shell???
// Apporach 1 ... manually trying to strech an image ...
//module MosqueShell(width, shell_thickness=0.05) {
//
//    difference() {
//        scale([1.05,1.05,1]) translate([0,0,0]) Mosque(width, 0.2, 2.0);
//        translate([0,1,0]) Mosque(width, door_scale=.24, crescent_scale=1.25, crescent_rotation=17.5);
//
//   }
//} 
// Approach 2 ... doing this ...
// https://cubehero.com/2013/12/31/creating-cookie-cutters-using-offsets-in-openscad/

module Door() {    
    difference(){
        translate([ 0,0,0])color("green")Arch(13, 13);
        translate([ 0,0.5,0])Arch(12, 12);
    }
}

module Mosque(width, door_scale=0.25, door_stretch=0, crescent_scale=1, crescent_rotation=0) {
    crescent_size = width/10;
    arc_factor = width/2;

    square_height =  width+(width/10);
    crescent_height = crescent_size;
    arc_height = 1.5*width/5 ;
    total_height = square_height + arc_height + crescent_height;
    echo(total_height, width, total_height/width);
    
    union() {
        translate([0,square_height+arc_height+crescent_height,0]) 
            Crescent(crescent_size, crescent_scale, rotate=crescent_rotation);
        difference() {
            translate([-width/2,0,0])square([width, width+(width/10)]);
            scale([2,1,1]) Arch(width*door_scale,2*width*door_scale, door_stretch);
        }
        translate([0,square_height,0]) scale([1.5,1.5,1]) HalfCircle(width/5);
    }
}

module offset_shell(thickness = 0.1) {
  render() {
      difference() {
          minkowski() {
            children();
            circle(2* thickness, center=true);
          }
        children();
      }
   }
}

union() {
    linear_extrude(height = 2.5, slices = 60) { 
        scale([.2,.2,1]) {
            offset_shell(2.5) {
              Mosque(100, crescent_scale=0.9, crescent_rotation=30);
            }
        }
    };
    linear_extrude(height = 7.5, slices = 60) translate([0,0,2]) scale([.2,.2,1]) {
      offset_shell(0.5) {
          Mosque(100, crescent_scale=0.9, crescent_rotation=30);
        }
    };
}

//
//module test(thickness = 0.1) {
//     minkowski() {
//            children();
//            circle([2 * thickness, 2 * thickness], center=true);
//          }
//}
//    
////Mosque(20);