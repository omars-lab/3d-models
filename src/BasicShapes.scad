module Star(points, outer, inner_defaulted=0) {
    inner = inner_defaulted == 0 ? 2 * outer  : inner_defaulted;
	// polar to cartesian: radius/angle to x/y
	function x(r, a) = r * cos(a);
	function y(r, a) = r * sin(a);
	
	// angular width of each pie slice of the star
	increment = 360/points;
	
	union() {
		for (p = [0 : points-1]) {
			
			// outer is outer point p
			// inner is inner point following p
			// next is next outer point following p

			assign(	
                x_outer = x(outer, increment * p),
                y_outer = y(outer, increment * p),
                x_inner = x(inner, (increment * p) + (increment/2)),
                y_inner = y(inner, (increment * p) + (increment/2)),
                x_next  = x(outer, increment * (p+1)),
                y_next  = y(outer, increment * (p+1))
            ) {
				polygon(
                    points = [
                        [x_outer, y_outer], 
                        [x_inner, y_inner],
                        [x_next, y_next], 
                        [0, 0]
                    ], 
                    paths  = [[0, 1, 2, 3]]
                );
			}
		}
	}
}

//https://github.com/openscad/MCAD/blob/master/shapes.scad
module Hexagon(size) {
  Star(3, size, size);
}

module Octagon(size) {
  Star(4, size, size);
}

module Decagon(size) {
  Star(5, size, size);
}

module Decagon(size) {
  Star(5, size, size);
}

module Dodecagon(size) {
  Star(6, size, size);
}
