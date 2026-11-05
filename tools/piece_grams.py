"""Grams of filament each piece on a sliced plate costs, read off the slice's G-code.

Kept apart from print_review.py so it needs nothing outside the standard library: the hub calls
after_print.py with a python3 that has no PIL, and after_print adds up these grams per question.
print_review.py's `grams` command and its bed.json use the same function.
"""

import re


def piece_grams(zf):
    """{3MF object id: grams} for a sliced plate open as a ZipFile, plus "between" for what falls
    outside every object's marks.

    The X2D's G-code marks each object with `; start printing object, unique label id: N` and
    `; stop printing object, ...`; N is the `identify_id` that `Metadata/model_settings.config`
    ties to an `object_id`. Extrusion is relative (M83): the E of every G0-G3 move inside a mark
    goes to that object, retractions included, so they cancel. Millimetres of filament become
    grams at the slice's own rate (its `used_g` over all the E), so the parts add up to the
    plate's grams as `bambu validate sliced` reads them.

    The slice's grams leave out the prime line and the color flush: the start G-code lays them
    with its own commands (G130, M620), not G0-G3 E moves. On star-3 the E inside its two pieces
    came to 169.1 mm against the slice's 170 mm, and between them only -0.4 mm of pull-back, so
    "between" is floored at zero. Returns {} when the slice has no G-code, no object marks or no
    grams; refuses absolute extrusion (M82)."""
    names = zf.namelist()
    gcode = next((n for n in names if n.endswith(".gcode")), None)
    if not gcode or "Metadata/slice_info.config" not in names:
        return {}
    info = zf.read("Metadata/slice_info.config").decode("utf-8", "replace")
    used_g = sum(float(x) for x in re.findall(r'used_g="([\d.]+)"', info))
    settings = (zf.read("Metadata/model_settings.config").decode("utf-8", "replace")
                if "Metadata/model_settings.config" in names else "")
    ident = {}
    for inst in re.findall(r"<model_instance>(.*?)</model_instance>", settings, flags=re.S):
        oid = re.search(r'key="object_id" value="(\d+)"', inst)
        iid = re.search(r'key="identify_id" value="(\d+)"', inst)
        if oid and iid:
            ident[iid.group(1)] = oid.group(1)
    mm, now = {}, "between"
    for line in zf.read(gcode).decode("utf-8", "replace").splitlines():
        if line.startswith("; start printing object, unique label id:"):
            now = ident.get(line.rsplit(":", 1)[1].strip(), "between")
        elif line.startswith("; stop printing object"):
            now = "between"
        elif line.startswith("M82"):
            raise ValueError(f"{gcode}: absolute extrusion (M82); piece grams read relative E only")
        elif line[:3] in ("G0 ", "G1 ", "G2 ", "G3 "):
            e = re.search(r"\sE(-?[\d.]+)", line.split(";", 1)[0])
            if e:
                mm[now] = mm.get(now, 0.0) + float(e.group(1))
    total = sum(mm.values())
    if used_g <= 0 or total <= 0 or set(mm) <= {"between"}:
        return {}
    out = {k: round(v * used_g / total, 2) for k, v in mm.items()}
    out["between"] = max(0.0, out.get("between", 0.0))
    return out
