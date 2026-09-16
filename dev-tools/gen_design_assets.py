"""Generates the two new visual assets for the "Ultron's Designs" tab
(owner-requested 2026-09-16):

- relic_gauge.png: the static casing (metal fittings, stand) for the
  memory-capacity gauge -- the red fill itself is drawn at runtime by
  the dashboard's own JS, clipped to FILL_RECT below, from a REAL
  percentage (memory_notes count vs its real cap), not baked into the
  image. Style inspired by an owner-supplied reference photo of a
  vertical glowing relic/artifact on a display stand -- an original
  casing design matching its general shape/material language (metal
  fittings top and bottom, a dark vertical chamber, a base plate), not
  a trace of that specific object.

- body_design.png: a bigger, more detailed standing figure for the
  "body design in progress" panel, in the same red/gunmetal language as
  the pixel-companion sprites but taller and more heroically
  proportioned, with shoulder pauldrons and leg plating -- inspired by
  an owner-supplied Ultron-style character render. Original silhouette,
  not a trace of that reference, for the same copyright reason
  documented in gen_pixel_assets.py (that reference is itself styled on
  Marvel's copyrighted design).

Run to (re)generate into ../pixel-assets/:
    python dev-tools/gen_design_assets.py
"""
from PIL import Image, ImageDraw, ImageFilter
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pixel-assets")
os.makedirs(OUT_DIR, exist_ok=True)

BODY_DARK = (27, 29, 32, 255)
BODY_MID = (44, 47, 51, 255)
BODY_LIGHT = (71, 76, 82, 255)
STEEL = (139, 147, 160, 255)
RED_BRIGHT = (255, 59, 59, 255)
RED_DIM = (150, 30, 30, 255)
PANEL = (15, 17, 19, 255)
LINE = (44, 47, 51, 255)


def glow(img, color, blur=6):
    alpha = img.split()[3].filter(ImageFilter.GaussianBlur(blur))
    tint = Image.new("RGBA", img.size, color)
    tint.putalpha(alpha.point(lambda a: int(a * 0.6)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(tint)
    out.alpha_composite(img)
    return out


# The fillable interior rect -- exported so the JS side can hardcode the
# exact same numbers (see the "Ultron's Designs" tab script in
# ultron-dashboard.html) and clip its real-percentage fill to line up
# precisely with this casing's chamber.
CANVAS_W, CANVAS_H = 200, 560
FILL_RECT = (70, 130, 130, 460)  # x0, y0, x1, y1 -- y1 is the chamber's bottom (0% fill line)


def draw_relic_casing():
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = FILL_RECT
    cx = (x0 + x1) / 2

    # Base plate + stand.
    d.rectangle([40, 520, 160, 550], fill=(5, 5, 6, 255), outline=STEEL, width=2)
    d.rectangle([60, 505, 140, 522], fill=BODY_DARK, outline=LINE, width=1)
    d.rectangle([x0 - 8, y1, x1 + 8, 508], fill=BODY_MID)
    d.rectangle([x0 - 8, y1, x1 + 8, 508], outline=LINE, width=2)

    # Chamber (dark, empty by default -- JS fills it live).
    d.rectangle([x0, y0, x1, y1], fill=(4, 4, 5, 255))

    # Side fittings along the chamber -- angular notches echoing the
    # reference's stepped metal side-plates.
    for ny in range(int(y0) + 10, int(y1) - 10, 34):
        d.polygon([(x0 - 14, ny), (x0, ny + 6), (x0, ny + 18), (x0 - 14, ny + 24)], fill=STEEL)
        d.polygon([(x1 + 14, ny), (x1, ny + 6), (x1, ny + 18), (x1 + 14, ny + 24)], fill=STEEL)

    # Top fitting block + four spiky prongs (the reference's most
    # distinctive silhouette element).
    d.rectangle([x0 - 10, y0 - 34, x1 + 10, y0], fill=BODY_LIGHT, outline=LINE, width=2)
    prong_w = (x1 - x0 - 10) / 4
    for i in range(4):
        px = x0 + 5 + i * prong_w
        d.polygon([(px, y0 - 34), (px + prong_w * 0.6, y0 - 70), (px + prong_w, y0 - 34)], fill=STEEL)
    d.rectangle([x0 - 10, y0 - 40, x1 + 10, y0 - 34], fill=(10, 10, 11, 255))

    # A small always-on indicator light near the base, independent of
    # the fill level -- just a "power on" tell, not a data readout.
    d.ellipse([cx - 6, 480, cx + 6, 492], fill=RED_BRIGHT)

    return glow(img, RED_BRIGHT, blur=4)


def draw_body_design():
    """Taller, more heroically proportioned than the pixel-companion
    sprite -- shoulder pauldrons, segmented leg plating, a bigger
    crested head -- for a "design concept" centerpiece rather than a
    small walking character."""
    W, H = 340, 620
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = W / 2

    def poly(pts, color):
        d.polygon(pts, fill=color)

    def rect(x0, y0, x1, y1, color):
        d.rectangle([x0, y0, x1, y1], fill=color)

    # Head -- crested, angular, red visor band.
    poly([(cx - 40, 70), (cx - 15, 20), (cx + 15, 20), (cx + 40, 70), (cx + 36, 120), (cx - 36, 120)], BODY_MID)
    rect(cx - 34, 118, cx + 34, 148, BODY_LIGHT)
    rect(cx - 28, 128, cx + 28, 140, RED_BRIGHT)
    poly([(cx - 26, 20), (cx - 20, -30), (cx - 6, 15)], RED_BRIGHT)
    poly([(cx + 6, 15), (cx + 20, -34), (cx + 26, 20)], RED_BRIGHT)

    # Neck + shoulder pauldrons -- big, layered, the reference's most
    # distinctive "battle-armor" silhouette element.
    rect(cx - 14, 148, cx + 14, 168, BODY_MID)
    poly([(cx - 90, 175), (cx - 35, 165), (cx - 35, 220), (cx - 100, 235), (cx - 115, 200)], BODY_LIGHT)
    poly([(cx + 90, 175), (cx + 35, 165), (cx + 35, 220), (cx + 100, 235), (cx + 115, 200)], BODY_LIGHT)
    d.ellipse([cx - 108, 195, cx - 92, 211], fill=RED_BRIGHT)
    d.ellipse([cx + 92, 195, cx + 108, 211], fill=RED_BRIGHT)

    # Chest core.
    rect(cx - 32, 175, cx + 32, 260, PANEL)
    d.ellipse([cx - 26, 195, cx + 26, 247], fill=RED_BRIGHT)
    d.ellipse([cx - 16, 205, cx + 16, 237], fill=(255, 255, 255, 235))

    # Torso.
    poly([(cx - 45, 175), (cx + 45, 175), (cx + 55, 300), (cx - 55, 300)], BODY_MID)
    for gy in (210, 235, 270):
        rect(cx - 40, gy, cx + 40, gy + 4, RED_DIM)
    rect(cx - 55, 260, cx - 30, 320, BODY_DARK)
    rect(cx + 30, 260, cx + 55, 320, BODY_DARK)

    # Arms.
    rect(cx - 118, 220, cx - 90, 340, BODY_MID)
    rect(cx + 90, 220, cx + 118, 340, BODY_MID)
    d.ellipse([cx - 122, 270, cx - 86, 306], fill=BODY_LIGHT)
    d.ellipse([cx + 86, 270, cx + 122, 306], fill=BODY_LIGHT)
    d.ellipse([cx - 110, 282, cx - 98, 294], fill=RED_BRIGHT)
    d.ellipse([cx + 98, 282, cx + 110, 294], fill=RED_BRIGHT)
    rect(cx - 116, 340, cx - 92, 400, BODY_DARK)
    rect(cx + 92, 340, cx + 116, 400, BODY_DARK)

    # Hips + legs, segmented armor plates with glowing knee joints.
    poly([(cx - 60, 300), (cx + 60, 300), (cx + 50, 340), (cx - 50, 340)], BODY_LIGHT)
    for side in (-1, 1):
        lx = cx + side * 32
        rect(lx - 22, 340, lx + 22, 430, BODY_MID)
        rect(lx - 24, 430, lx + 24, 448, BODY_LIGHT)
        d.ellipse([lx - 10, 434, lx + 10, 452], fill=RED_BRIGHT)
        rect(lx - 20, 452, lx + 20, 540, BODY_MID)
        rect(lx - 24, 540, lx + 24, 566, BODY_DARK)

    return glow(img, RED_BRIGHT, blur=5)


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print("wrote", path, img.size)


def main():
    save(draw_relic_casing(), "relic_gauge.png")
    save(draw_body_design(), "body_design.png")


if __name__ == "__main__":
    main()
