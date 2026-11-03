// Lebanon flag cedar stencil, for a pre-K class drawing the flag on one sheet of printer paper
// turned sideways (landscape).
//
// The red stripes are each a quarter of the flag's height and the white band between them half.
// The cedar's tips touch both red stripes, and it keeps its own shape (about as wide as tall). The cedar outline is the outer edge of the
// green path in Wikimedia's Flag_of_Lebanon.svg (public domain, 2880 x 1920 px, kept here), with
// the white details inside it left out so the stencil hole is one opening. It comes in as a
// polygon from lebanon-cedar-outline.scad (the make-stencil skill's svg_outline.py writes it): Bambu Studio would
// not slice the card with the SVG imported directly.
//
// flag = "page" (Omar, 2026-10-30: "a flag that is 8.5 in tall by 11 wide"): the whole sheet is the
// flag. On Letter the stripes are 54 mm, the white band and the cedar 108 mm tall. This is not
// the official 2:3; the stripes keep their quarter-half-quarter split and the cedar its shape.
// flag = "official": a 2:3 flag across the paper's width, centered, with a strip above and below
// to trim. Letter: 279.4 x 186.3 mm, the cedar 93 mm. A4: 297 x 198 mm.
//
// The plate prints the card only (Omar, 2026-10-30: "i want the bigger piece, not the smaller
// one"). The loose cedar stays in the source as a part, not printed:
//   sheet  - a card as tall as the paper. Lay it flush with the paper's top and bottom edges and
//            line its middle notches up with a fold down the paper's middle. Trace inside the
//            cedar hole. The notches on its sides mark the stripe lines, for the grown-up's
//            pencil and ruler. With flag = "official", two slots also mark the trim lines.
//   cedar  - the cedar on its own, to trace around.
//
// For crayons the cedar is grown all round: a crayon is 8 to 11 mm across and never gets into the
// 2 to 3 mm frond tips of the exact outline, and on the loose piece those tips would snap. The
// cedar is scaled so the opening, the line a child traces, spans the white band tip to base.
//
//   openscad -D 'part="sheet"' -o src/Stencils/lebanon-cedar-sheet-letter.stl src/Stencils/LebanonCedar.scad

paper = "letter";      // "letter" or "a4"
flag = "page";         // "page" (the whole sheet is the flag) or "official" (2:3 inside it)
part = "sheet";        // "sheet" (the card), "cedar" (the loose cedar), or "paper" (the flag)

thick = 0.6;           // three 0.2 mm layers: thin and bendable (Omar, 2026-10-30)
sheet_w = 140;         // the 108 mm opening plus a 16 mm border each side
slot_w = 1.6;          // a pencil tip fits; a crayon marks along it
slot_end = 4;          // solid border left at the sheet's edge at each end of a slot
notch = 6;             // the fold-line and stripe-line notches
corner = 6;
grow = 1.5;            // mm added round the cedar, for crayons and sturdier fronds

paper_w = paper == "a4" ? 297 : 279.4;
paper_h = paper == "a4" ? 210 : 215.9;
flag_w = paper_w;
flag_h = flag == "page" ? paper_h : flag_w * 2 / 3;
stripe_line = flag_h / 4;   // stripe edge, from the flag's middle

// The opening spans the white band, which is 960 of the source SVG's 1920 px height.
k = (flag_h / 2 - 2 * grow) / 960;  // mm per SVG px

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
        if (flag_h < paper_h)
            for (y = [-flag_h / 2, flag_h / 2])
                translate([0, y]) square([sheet_w - 2 * slot_end, slot_w], center = true);
        for (s = [-1, 1]) {
            translate([0, s * paper_h / 2]) rotate(45) square(notch * sqrt(2), center = true);
            for (y = [-stripe_line, stripe_line])
                translate([s * sheet_w / 2, y]) rotate(45) square(notch * sqrt(2), center = true);
        }
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
else sheet();
