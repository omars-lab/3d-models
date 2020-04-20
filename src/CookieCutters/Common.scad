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

module cookie_cutter(handle_thickness=8, cutter_tickness=3, total_height=15) {
    union() {
        linear_extrude(height = total_height*(0.15), slices = 60) {
            scale([.2,.2,1]) {
              offset_shell(handle_thickness) {
                children();

              }
            }
        };
        linear_extrude(height = total_height*(0.9), slices = 60)
            translate([0,0,2])
            scale([.2,.2,1]) {
              offset_shell(cutter_tickness) {
                children();
            }
        };
    }
}

module rod_with_clipped_circle(square_d, circle_d, circle_placement) {
    difference() {
        square(square_d, center=true);
        translate(circle_placement) circle(circle_d, center=true);
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
