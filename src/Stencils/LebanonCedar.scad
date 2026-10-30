// Lebanon flag cedar stencil, for a pre-K class drawing the flag on one sheet of printer paper
// turned sideways (landscape).
//
// The flag is 2:3. The red stripes are each a quarter of its height and the white band between
// them half. The cedar's tips touch both red stripes. The cedar outline is the outer edge of the
// green path in Wikimedia's Flag_of_Lebanon.svg (public domain, 2880 x 1920 px, kept here), with
// the white details inside it left out so the stencil hole is one opening. It comes in as a
// polygon from lebanon-cedar-outline.scad (make_cedar_outline.py writes it): Bambu Studio would
// not slice the card with the SVG imported directly.
//
// The flag fills the paper's width; its height is width x 2/3, centered, leaving a strip above and
// below to trim. Letter: 279.4 x 186.3 mm on 279.4 x 215.9. A4: 297 x 198 mm on 297 x 210.
//
// Two pieces:
//   sheet  - a card as tall as the paper. Lay it flush with the paper's top and bottom edges and
//            line its middle notches up with a fold down the paper's middle. Trace inside the
//            cedar hole. The slots are for the grown-up's pencil: the outer pair marks the trim
//            lines where the flag ends, the inner pair (stopping short of the cedar so a crayon
//            in the hole does not run into them) marks the stripe lines; join them with a ruler.
//   cedar  - the cedar on its own, to trace around.
//
// For crayons the cedar is grown by `grow` all round: a crayon is 8 to 11 mm across and never
// gets into the 2 to 3 mm frond tips of the exact outline, and on the loose piece those tips
// would snap. grow = 0 gives the exact outline.
//
//   openscad -D 'part="sheet"' -o src/Stencils/lebanon-cedar-sheet-letter.stl src/Stencils/LebanonCedar.scad
//   openscad -D 'part="cedar"' -o src/Stencils/lebanon-cedar-piece-letter.stl src/Stencils/LebanonCedar.scad

paper = "letter";      // "letter" or "a4"
part = "both";         // "sheet", "cedar", "both", or "paper" (a picture of the flag on the page)

thick = 3;             // stiff enough for small hands
sheet_w = 140;         // cedar plus a 23 mm border each side
slot_w = 1.6;          // a pencil tip fits; a crayon marks along it
slot_end = 4;          // solid border left at the sheet's edge at each end of a slot
slot_clear = 5;        // gap between an inner slot and the cedar
notch = 6;             // the fold-line notches, top and bottom middle
corner = 6;
grow = 1.5;            // mm added round the cedar, for crayons and sturdier fronds

paper_w = paper == "a4" ? 297 : 279.4;
paper_h = paper == "a4" ? 210 : 215.9;
flag_w = paper_w;
flag_h = flag_w * 2 / 3;
stripe_line = flag_h / 4;   // stripe edge, from the flag's middle

svg_px = 2880;              // flag width in the source SVG
k = flag_w / svg_px;        // mm per SVG px

include <lebanon-cedar-outline.scad>

module cedar() {
    offset(r = grow) scale(k) polygon(cedar_outline);
}

module rounded_rect(w, h, r) {
    offset(r) square([w - 2 * r, h - 2 * r], center = true);
}

module sheet() {
    linear_extrude(thick) difference() {
        rounded_rect(sheet_w, paper_h, corner);
        cedar();
        for (y = [-flag_h / 2, flag_h / 2])
            translate([0, y]) square([sheet_w - 2 * slot_end, slot_w], center = true);
        // The cedar is flag_w / 3 wide; the inner slots stop slot_clear short of it.
        inner_from = flag_w / 6 + grow + slot_clear;
        for (y = [-stripe_line, stripe_line], sx = [-1, 1])
            translate([sx * (inner_from + sheet_w / 2 - slot_end) / 2, y])
                square([sheet_w / 2 - slot_end - inner_from, slot_w], center = true);
        for (s = [-1, 1])
            translate([0, s * paper_h / 2])
                rotate(45) square(notch * sqrt(2), center = true);
    }
}

module cedar_piece() {
    linear_extrude(thick) cedar();
}

// The finished flag on the page, with the card's outline where it sits: for the plate page.
module on_paper() {
    color("white") translate([0, 0, -0.2]) square([paper_w, paper_h], center = true);
    color("#d31624") for (s = [-1, 1])
        translate([0, s * 3 * flag_h / 8]) square([flag_w, flag_h / 4], center = true);
    color("#008c3e") cedar();
    color("black") translate([0, 0, 0.1]) difference() {
        rounded_rect(sheet_w, paper_h, corner);
        offset(-0.8) rounded_rect(sheet_w, paper_h, corner);
    }
}

if (part == "sheet") sheet();
else if (part == "paper") on_paper();
else if (part == "cedar") cedar_piece();
else {
    sheet();
    translate([sheet_w / 2 + 10 + flag_h / 4 + grow, 0]) cedar_piece();
}
