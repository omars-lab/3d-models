// Cable spiral: a thin disc with an open spiral groove on top. Fold a cable at its middle, lay the
// fold in the S-bend at the centre, and press the two halves down into the two side-by-side
// spirals. Both plugs leave at the rim. The flat underside of the next disc closes the grooves of
// the disc below, and a stacking ring on the top edge keeps the pile lined up.
//
// Design: docs/design/pieces/cable-spiral-design.md. Numbers: the checked research note on PR #1022
// (docs/research/2026-11-11-cable-spiral-consolidated.md). Every size below is a starting value
// for the first test print unless the design doc says otherwise.
//
// Render:  openscad -D 'part="disc"'   -D d=4.0 -o disc.stl   cable-spiral.scad
//          openscad -D 'part="coupon"' -D d=4.0 -o coupon.stl cable-spiral.scad
// The one setting that matters is d, the cable's diameter measured with calipers.
// Three sizes cover 3.0-4.7 mm USB-C cables with no gap, just to the edges, and the wall stretch
// under 4% where both walls can bend: d = 3.2, 3.7 and 4.3 (design doc, "One disc per cable size").
// In the S-bend, and beside the centre and the rim, a wall has solid behind it and cannot bend;
// the design doc's open question 1.

part = "disc";          // "disc" or "coupon" (the first test piece)
d = 4.0;                // cable diameter, mm
cable_length = 1000;    // how much cable one disc holds, mm (the disc grows to fit)
only = "";              // with part="coupon": render just the piece with this id, for checking

// ---- The groove, all in terms of d (design doc §"How the cable is held") ----
gap      = 0.4;         // groove is d + 0.4 wide: 0.2 mm a side
floor_t  = 0.8;         // four 0.2 mm layers under the cable
wall_t   = 0.8;         // wall between turns: two lines
mouth_k  = 0.80;        // mouth = 0.80 x d
lead_ang = 30;          // lead-in slope above the lip tip, degrees from upright
rim      = 2.0;         // solid rim outside the last turn
ring_h   = 0.4;         // stacking ring on the top edge
chamfer  = 0.6;         // 45 degree chamfer on the bottom edge; the ring tucks into it
bend_k   = 2.5;         // S-bend half-loop radius = 2.5 x d
slab     = 0.1;         // height step for the sloped faces (half a 0.2 mm layer)
$fn      = 96;

function groove_w(d)       = d + gap;
function lip_reach(d, mk)  = (groove_w(d) - mk * d) / 2;
// "tip high": the lip underside starts at height d, so a cable on the floor never touches it.
// "tip low":  the lowest the tip can sit and still clear a cable on the floor by 0.2 mm, measured
//             straight up at the tip (the shortest distance to the round cable is about 0.13 mm).
function tip_h(d, mk, low) = low ? 0.8 * d + 0.2 : d + lip_reach(d, mk);
function lead_h(d)         = 0.2 * d;
function disc_t(d, mk, low)= floor_t + tip_h(d, mk, low) + lead_h(d);

// Half the groove's width at height z above the floor, for the stepped slabs.
function half_w(z, d, mk, low, lip) =
    let(w2 = groove_w(d) / 2, m2 = mk * d / 2,
        th = tip_h(d, mk, low), under = th - lip_reach(d, mk))
    !lip           ? w2 :
    z <= under     ? w2 :
    z <= th        ? w2 - (z - under) :                                  // 45 degree underside
                     min(w2, m2 + (z - th) * tan(lead_ang));             // lead-in opens upward

// ---- Paths ----
// A stroke: the 2D band of half-width h around a polyline (no self-overlap for gentle curves).
function _unit(v) = v / norm(v);
function _tan(p, i) = let(n = len(p))
    _unit(i == 0 ? p[1] - p[0] : i == n - 1 ? p[n-1] - p[n-2] : p[i+1] - p[i-1]);
function _nrm(p, i) = let(t = _tan(p, i)) [-t[1], t[0]];
module stroke(p, h) {
    polygon(concat([for (i = [0:len(p)-1]) p[i] + h * _nrm(p, i)],
                   [for (i = [len(p)-1:-1:0]) p[i] - h * _nrm(p, i)]));
}

// The folded-cable path: arm 2 in, the S-bend through the centre, arm 1 out, each arm ending in a
// straight run out through the rim.
rho    = bend_k * d;                         // S-bend half-loop radius
r0     = 2 * rho;                            // where the spirals start
pitch2 = 2 * (groove_w(d) + wall_t);         // one arm's radius gain per turn (two arms interleave)
s_len  = 2 * PI * rho;                       // cable held in the S-bend
// Two interleaved spirals from r0 out to R hold pi (R^2 - r0^2) / (w + t) of cable.
R_out  = sqrt(max(0, cable_length - s_len) * (groove_w(d) + wall_t) / PI + r0 * r0);
th_max = (R_out - r0) * 2 * PI / pitch2;     // radians along an arm
R_disc = R_out + groove_w(d) / 2 + rim;

function arm(th) = let(r = r0 + pitch2 * th / (2 * PI)) [r * cos(th * 180 / PI), r * sin(th * 180 / PI)];
arm_pts = [for (i = [0:ceil(th_max * 24)]) if (i == 0 || (i - 1) / 24 < th_max - 1e-9) arm(min(i / 24, th_max))];
// The exit: from the arm's end, bend outward by exit_turn degrees round radius exit_r, then run
// straight off the disc. Leaving along the spiral would cross the rim almost flat and leave a thin
// blade of wall; turning out first makes the notch cross the rim more steeply.
exit_turn = 60;
exit_r    = 2 * rho;                         // never tighter than the S-bend
arm_end   = arm_pts[len(arm_pts) - 1];
arm_t     = _unit(arm_end - arm_pts[len(arm_pts) - 2]);
arm_n     = [arm_t[1], -arm_t[0]];           // points away from the centre (the arm runs anticlockwise)
exit_c    = arm_end + exit_r * arm_n;
exit_arc  = [for (a = [5:5:exit_turn]) exit_c + exit_r * (-cos(a) * arm_n + sin(a) * arm_t)];
exit_dir  = sin(exit_turn) * arm_n + cos(exit_turn) * arm_t;
exit_pts  = concat(exit_arc, [exit_arc[len(exit_arc) - 1] + R_disc * exit_dir]);
arm_full  = concat(arm_pts, exit_pts);
exit_full = concat([arm_end], exit_pts);
// S-bend half: from the centre to (r0, 0), round a half-loop centred at (rho, 0), dipping below y = 0.
s_half = [for (a = [180:5:360]) [rho + rho * cos(a), rho * sin(a)]];
function neg(p) = [for (q = p) -q];
function rev(p) = [for (i = [len(p)-1:-1:0]) p[i]];
// Joining pieces repeats their shared end points; a repeated point has no direction and breaks the
// groove outline, so drop them.
function dedupe(p) = [for (i = [0:len(p)-1]) if (i == 0 || norm(p[i] - p[i-1]) > 1e-6) p[i]];
fold_path = dedupe(concat(rev(neg(arm_full)), rev(neg(s_half)), s_half, arm_full));

function path_len(p) = len(p) < 2 ? 0 : [for (i = [1:len(p)-1]) norm(p[i] - p[i-1])] * [for (i = [1:len(p)-1]) 1];
cable_on_disc = 2 * path_len(arm_pts) + s_len;

// One exit notch, flat. Filling in the bend (hull) also takes away the rim on the outside of the
// bend, which would otherwise narrow to a fragile point. Everything it removes lies outside the
// line the groove runs along at the arm's end, so no wall between turns is touched.
// The point straight out from the arm's end, past the edge, ends the rim with a square cut.
module exit_notch() {
    hull() {
        stroke(exit_full, groove_w(d) / 2);
        translate(arm_end * (R_disc + 2) / norm(arm_end)) square(0.1, center = true);
    }
}

// ---- Solids ----
// A grooved block: the child is the 2D outer shape, `paths` a list of groove centrelines. Built as
// stacked slabs so the sloped lip and lead-in come out in 0.1 mm steps.
module grooved(paths, d, mk = mouth_k, low = false, lip = true) {
    T  = disc_t(d, mk, low);
    // heights above the groove floor, from where the lip's underside starts to the top face
    zs = [for (z = [tip_h(d, mk, low) - lip_reach(d, mk) : slab : T - floor_t - slab / 2]) z];
    // solid floor, then the straight-walled part of the groove
    linear_extrude(height = floor_t) children();
    translate([0, 0, floor_t]) linear_extrude(height = zs[0]) difference() {
        children(); for (p = paths) stroke(p, half_w(0, d, mk, low, lip));
    }
    for (z = zs) translate([0, 0, floor_t + z])
        // 0.01 overlap: 4.0 + n*0.1 is not exact in floating point, and a hair-thin gap between
        // two slabs splits the part into separate solids (seen on test bar A, mouth 0.75)
        linear_extrude(height = min(slab + 0.01, T - floor_t - z)) difference() {
            children(); for (p = paths) stroke(p, half_w(z + slab / 2, d, mk, low, lip));
        }
}

module disc() {
    T = disc_t(d, mouth_k, false);
    echo(str("CABLE-SPIRAL disc: d=", d, " mm, ", round(2 * R_disc * 10) / 10, " mm across, ",
             round(T * 10) / 10, " mm thick, holds ", round(cable_on_disc), " mm of cable"));
    difference() {
        union() {
            grooved([fold_path], d) circle(R_disc);
            // stacking ring: 45 degree inner face, vertical outer face, on the top edge
            translate([0, 0, T]) rotate_extrude() polygon([[R_disc - ring_h, 0], [R_disc, 0], [R_disc, ring_h]]);
        }
        // bottom chamfer
        rotate_extrude() polygon([[R_disc - chamfer, -0.01], [R_disc + 1, -0.01], [R_disc + 1, chamfer + 1]]);
        // the two exits cut through the ring too
        // the exits are cut full width (no lip) so the plugs' cable lifts out freely at the rim
        translate([0, 0, floor_t]) linear_extrude(height = T + ring_h) { exit_notch(); rotate(180) exit_notch(); }
    }
}

// ---- The first test piece: straight runs, each a separate bar with a carved id ----
// Ids skip B, D, I, M, N and O, which read alike at this size (I reads as 1).
bar_len = 40;
tag_w   = 7;            // the id tab beside each bar
function bar_w(wall, twin) = twin ? 2 * groove_w(d) + 3 * wall : groove_w(d) + 2 * wall;
module bar(id, mk = mouth_k, low = false, lip = true, wall = wall_t, twin = false) {
    // The groove is open at both ends, so a cable with a plug on each end lies flat through it.
    // It runs 1 mm past each end: ending it flush with the outer edge leaves faces of zero
    // thickness that OpenSCAD 2021.01 cannot close. The id sits on a tab beside the bar.
    w  = groove_w(d);
    W  = bar_w(wall, twin);
    T  = disc_t(d, mk, low);
    centres = twin ? [-(w + wall) / 2, (w + wall) / 2] : [0];
    difference() {
        union() {
            grooved([for (c = centres) [[-1, c], [bar_len + 1, c]]], d, mk, low, lip)
                translate([0, -W / 2]) square([bar_len, W]);
            translate([bar_len - 10, W / 2 - 0.01, 0]) cube([10, tag_w, T]);
        }
        translate([bar_len - 5, W / 2 + tag_w / 2, T - 0.6]) linear_extrude(1)
            text(id, size = 4.5, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}
module curved_run(id) {
    // one half-loop at the S-bend radius, the tightest curve on the disc, open at both ends; the
    // inside of the loop is solid and carries the id
    w = groove_w(d); T = disc_t(d, mouth_k, false);
    path   = [for (a = [180:5:360]) [rho * cos(a), rho * sin(a)]];
    groove = concat([[-rho, 1]], path, [[rho, 1]]);
    difference() {
        grooved([groove], d) union() {
            stroke(path, w / 2 + wall_t);
            intersection() { circle(rho); translate([-rho, -rho]) square([2 * rho, rho]); }
        }
        translate([0, -rho / 2 + 0.5, T - 0.6]) linear_extrude(1)
            text(id, size = 4, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}
module stack_coupon(id) {
    // a small disc with the stacking ring, the bottom chamfer and one straight groove across, so a
    // length of cable can lie in the lower coupon while the upper one is set on it
    r = 15; w = groove_w(d); T = disc_t(d, mouth_k, false);
    difference() {
        union() {
            grooved([[[-r - 1, 0], [r + 1, 0]]], d) circle(r);
            translate([0, 0, T]) rotate_extrude() polygon([[r - ring_h, 0], [r, 0], [r, ring_h]]);
        }
        rotate_extrude() polygon([[r - chamfer, -0.01], [r + 1, -0.01], [r + 1, chamfer + 1]]);
        // the groove cuts through the ring at both ends too, as the disc's exits do, so the ring
        // never spans the groove in mid-air
        translate([-r - 1, -w / 2, T - 0.01]) cube([2 * r + 2, w, ring_h + 0.02]);
        translate([0, w / 2 + 4.5, T - 0.6]) linear_extrude(1)
            text(id, size = 4, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

function _ys(rows, i) = i == 0 ? 0 :
    _ys(rows, i - 1) + bar_w(rows[i - 1][4], rows[i - 1][5]) / 2 + tag_w + 3 + bar_w(rows[i][4], rows[i][5]) / 2;
module coupon() {
    rows = [
        ["A", 0.75, false, true, wall_t, false],   // mouth 0.75 d
        ["C", 0.80, false, true, wall_t, false],   // mouth 0.80 d (the suggested one)
        ["E", 0.85, false, true, wall_t, false],   // mouth 0.85 d
        ["F", 0.80, false, false, wall_t, false],  // no lip: the control
        ["G", 0.80, true,  true, wall_t, false],   // thin: tip low, 0.8 wall
        ["H", 0.80, true,  true, 0.45, false],     // thin: tip low, one-line wall
        ["J", 0.80, false, true, wall_t, true],    // two grooves sharing one wall, as on the disc
    ];
    for (i = [0:len(rows) - 1]) let(r = rows[i]) if (only == "" || only == r[0])
        translate([0, _ys(rows, i), 0]) bar(r[0], r[1], r[2], r[3], r[4], r[5]);
    y0 = _ys(rows, len(rows) - 1) + bar_w(wall_t, true) / 2 + tag_w + 5 + rho + groove_w(d) / 2 + wall_t;
    if (only == "" || only == "K") translate([rho + 3, y0, 0]) curved_run("K");
    if (only == "" || only == "L") translate([2 * rho + 26, y0 - 4, 0]) stack_coupon("L");
    if (only == "" || only == "P") translate([2 * rho + 60, y0 - 4, 0]) stack_coupon("P");
}

// "plan": the groove layout at floor level, flat, for checking the S-bend and the exits by eye.
module plan() {
    difference() { circle(R_disc); stroke(fold_path, groove_w(d) / 2); exit_notch(); rotate(180) exit_notch(); }
}

// "section": a cut across the middle of each test bar, side by side, ids in order, with a circle of
// diameter d on each groove floor standing in for the cable. Flat, for the design doc's picture.
module section() {
    rows = [["A", 0.75, false, true, wall_t, false], ["C", 0.80, false, true, wall_t, false],
            ["E", 0.85, false, true, wall_t, false], ["F", 0.80, false, false, wall_t, false],
            ["G", 0.80, true,  true, wall_t, false], ["H", 0.80, true,  true, 0.45, false],
            ["J", 0.80, false, true, wall_t, true]];
    w = groove_w(d);
    for (i = [0:len(rows) - 1]) let(r = rows[i], x0 = i * (w + 2 * wall_t + 4) + (i == 6 ? 4 : 0))
        translate([x0, 0]) {
            // turn the bar so its length points down, cut level with the middle, lay the cut flat
            rotate(90) projection(cut = true) rotate([0, 90, 0]) translate([-bar_len / 2, 0, 0])
                bar(r[0], r[1], r[2], r[3], r[4], r[5]);
            centres = r[5] ? [-(w + r[4]) / 2, (w + r[4]) / 2] : [0];
            for (c = centres) translate([c, floor_t + d / 2]) color("orange") circle(d / 2);
            translate([0, disc_t(d, r[1], r[2]) + 1.5]) text(r[0], size = 2.5, halign = "center");
        }
}

// "grip": one full-height groove cut three times, with a round cable of 0.94 d, d and d + 0.4 in
// each. The filled circle lies on the floor; the outline is the same cable lifted until it meets
// the lip tips. The label gives the cable's size, its side play and how far it can lift.
module grip() {
    w = groove_w(d); m2 = mouth_k * d / 2; tip = floor_t + tip_h(d, mouth_k, false);
    sizes = [0.94 * d, d, d + gap];
    for (i = [0:2]) let(D = sizes[i], r = D / 2, x0 = i * (w + 2 * wall_t + 7),
                        c_up = tip - sqrt(r * r - m2 * m2), lift = c_up - (floor_t + r))
        translate([x0, 0]) {
            rotate(90) projection(cut = true) rotate([0, 90, 0]) translate([-bar_len / 2, 0, 0])
                bar("C", mouth_k, false, true, wall_t, false);
            translate([0, floor_t + r]) color("orange") circle(r);
            translate([0, c_up]) color("orange") difference() { circle(r); circle(r - 0.12); }
            echo(str("CABLE-SPIRAL grip: D=", D, " side play ", w - D, " lift ", lift,
                     " top above disc ", c_up + r - disc_t(d, mouth_k, false)));
            translate([0, disc_t(d, mouth_k, false) + 3.2]) text(str(round(D * 100) / 100, " mm"), size = 1.3, halign = "center");
            translate([0, disc_t(d, mouth_k, false) + 1.4]) text(str("side ", round((w - D) * 100) / 100, ", lift ", round(lift * 10) / 10), size = 1.0, halign = "center");
        }
}

if (part == "disc") disc();
else if (part == "coupon") coupon();
else if (part == "plan") plan();
else if (part == "section") section();
else if (part == "grip") grip();
