#!/usr/bin/env python3
"""Post-process OpenSCAD renders for the web gallery.

OpenSCAD's Cornfield preview renders the model in gold on a flat cream
background (#FFFFE5). For the gallery we want the object to float on the
page, so we key that cream out to transparency and autocrop to the object's
bounding box. Originals in build/images/ are left untouched; results land in
build/images/web/.

Usage:  python3 build/process_images.py
Deps:   pillow   (pip install pillow)
"""
import glob
import os

from PIL import Image

SRC_DIR = "build/images"
OUT_DIR = "build/images/web"
BG = (255, 255, 229)   # OpenSCAD Cornfield background
TOL = 14               # match near-background pixels within this tolerance
PAD = 12               # padding kept around the autocrop bbox
SKIP = {"Common.png"}  # not a model


def near_bg(r, g, b):
    return (abs(r - BG[0]) <= TOL
            and abs(g - BG[1]) <= TOL
            and abs(b - BG[2]) <= TOL)


def process(path):
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if near_bg(r, g, b):
                px[x, y] = (r, g, b, 0)
    bbox = im.getbbox()
    if bbox:
        l, t, rr, bb = bbox
        l, t = max(0, l - PAD), max(0, t - PAD)
        rr, bb = min(w, rr + PAD), min(h, bb + PAD)
        im = im.crop((l, t, rr, bb))
    return im


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    count = 0
    for path in sorted(glob.glob(f"{SRC_DIR}/*.png")):
        name = os.path.basename(path)
        if name in SKIP:
            continue
        process(path).save(f"{OUT_DIR}/{name}")
        count += 1
    print(f"processed {count} images -> {OUT_DIR}")


if __name__ == "__main__":
    main()
