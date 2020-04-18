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

module cookie_cutter(handle_thickness=2.5, cutter_tickness=1, total_height=10) {
    union() {
        linear_extrude(height = total_height*(0.25), slices = 60) { 
            scale([.2,.2,1]) {
              offset_shell(handle_thickness) {
                children();

              }
            }
        };
        linear_extrude(height = total_height*(0.75), slices = 60)
            translate([0,0,2]) 
            scale([.2,.2,1]) {
              offset_shell(cutter_tickness) {
                children();
            }
        };
    }
}


//module cookie_press(handle_thickness=2.5, cutter_tickness=1, total_height=10) {
//    union() {
//        cookie_cutter(handle_thickness, cutter_tickness, total_height);
//        translate([0,0,10]) children();
//    }
//}
//
//
