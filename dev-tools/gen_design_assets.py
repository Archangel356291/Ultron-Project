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
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os
import random

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


def outline(img, color=(5, 6, 8, 255), size=3):
    """Same crisp-rim trick as gen_pixel_assets.py's outline() -- pulled in
    here too so this casing gets the same pixel-art-adjacent polish pass."""
    alpha = img.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(size))
    ring = ImageChops.subtract(dilated, alpha)
    ring_layer = Image.new("RGBA", img.size, color)
    ring_layer.putalpha(ring)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(ring_layer)
    out.alpha_composite(img)
    return out


def draw_vein_texture(w, h, seed=3):
    """Branching glowing-vein pattern for the relic chamber's interior --
    per the owner's reference photo (a vertical relic with a red circuit/
    vein pattern etched into its dark chamber), rather than a flat black
    fill. Drawn once, low-cost (a handful of random-walk line segments),
    sits *underneath* the dashboard's live percentage-fill DOM element
    (see .relic-gauge-fill in ultron-dashboard.html), which fully covers
    whatever's here below its own fill line -- so this only shows through
    the unfilled portion, same as the reference's resting glow."""
    random.seed(seed)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def branch(x, y, angle, length, depth):
        if depth <= 0 or length < 4:
            return
        # random-walk segment biased upward (angle measured from vertical)
        import math
        dx = math.sin(angle) * length
        dy = -math.cos(angle) * length
        nx, ny = x + dx, y + dy
        d.line([(x, y), (nx, ny)], fill=(255, 90, 70, random.randint(90, 160)), width=1)
        if random.random() < 0.7:
            branch(nx, ny, angle + random.uniform(-0.6, 0.6), length * random.uniform(0.6, 0.85), depth - 1)
        if random.random() < 0.45:
            branch(nx, ny, angle + random.uniform(0.6, 1.4), length * random.uniform(0.4, 0.6), depth - 1)

    for _ in range(5):
        branch(w * random.uniform(0.3, 0.7), h * random.uniform(0.85, 1.0), random.uniform(-0.3, 0.3), h * 0.16, 5)
    return img.filter(ImageFilter.GaussianBlur(0.4))


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

    # Chamber (dark by default -- JS fills it live, see FILL_RECT/
    # .relic-gauge-fill). A faint glowing vein texture underneath, per the
    # owner's reference photo, instead of flat black.
    d.rectangle([x0, y0, x1, y1], fill=(4, 4, 5, 255))
    veins = draw_vein_texture(int(x1 - x0), int(y1 - y0))
    img.alpha_composite(veins, (int(x0), int(y0)))

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

    return glow(outline(img, size=3), RED_BRIGHT, blur=4)


GOLD = (255, 178, 56, 255)
GOLD_FILL = (255, 178, 56, 26)


def draw_body_design():
    """A holographic wireframe scan, not a solid-shaded figure -- per the
    owner's "design visual reference" (a Territory-Studio-style HUD
    showing a body as glowing gold wireframe/geometry under scan, not
    rendered in its real material colors). Gold/amber here specifically
    means "concept hologram," distinct from the red the pixel-companion
    and relic use for Ultron's own real, physical glow (see
    ULTRON-COLOR-SYSTEM.md's gold-vs-red split) -- this panel is
    explicitly labeled "in progress," so it reads as a blueprint being
    scanned into existence, not a finished thing.

    Same silhouette/proportions as before (shoulder pauldrons, segmented
    leg plating, crested head) -- only the rendering technique changed:
    structural armor is faint-fill + bright wireframe edges, and joints/
    core are solid bright nodes, like the reference's scan hot-spots."""
    W, H = 340, 620
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = W / 2

    def poly(pts):
        d.polygon(pts, fill=GOLD_FILL, outline=GOLD)

    def rect(x0, y0, x1, y1):
        d.rectangle([x0, y0, x1, y1], fill=GOLD_FILL, outline=GOLD)

    def node(cx_, cy_, r):
        d.ellipse([cx_ - r, cy_ - r, cx_ + r, cy_ + r], fill=GOLD)

    # Head -- crested, angular, wireframe visor band.
    poly([(cx - 40, 70), (cx - 15, 20), (cx + 15, 20), (cx + 40, 70), (cx + 36, 120), (cx - 36, 120)])
    rect(cx - 34, 118, cx + 34, 148)
    rect(cx - 28, 128, cx + 28, 140)
    poly([(cx - 26, 20), (cx - 20, -30), (cx - 6, 15)])
    poly([(cx + 6, 15), (cx + 20, -34), (cx + 26, 20)])

    # Neck + shoulder pauldrons.
    rect(cx - 14, 148, cx + 14, 168)
    poly([(cx - 90, 175), (cx - 35, 165), (cx - 35, 220), (cx - 100, 235), (cx - 115, 200)])
    poly([(cx + 90, 175), (cx + 35, 165), (cx + 35, 220), (cx + 100, 235), (cx + 115, 200)])
    node(cx - 100, 203, 8)
    node(cx + 100, 203, 8)

    # Chest core -- a bright scan hot-spot, the reference's brightest point.
    rect(cx - 32, 175, cx + 32, 260)
    node(cx, 221, 20)
    d.ellipse([cx - 10, 211, cx + 10, 231], fill=(255, 245, 220, 240))

    # Torso, with a couple of horizontal "scan ring" bands (per the
    # reference's ellipse HUD rings crossing the scanned figure).
    poly([(cx - 45, 175), (cx + 45, 175), (cx + 55, 300), (cx - 55, 300)])
    for gy in (210, 235, 270):
        d.ellipse([cx - 60, gy - 4, cx + 60, gy + 4], outline=GOLD, width=1)
    rect(cx - 55, 260, cx - 30, 320)
    rect(cx + 30, 260, cx + 55, 320)

    # Arms.
    rect(cx - 118, 220, cx - 90, 340)
    rect(cx + 90, 220, cx + 118, 340)
    poly([(cx - 122, 270), (cx - 86, 270), (cx - 86, 306), (cx - 122, 306)])
    poly([(cx + 86, 270), (cx + 122, 270), (cx + 122, 306), (cx + 86, 306)])
    node(cx - 104, 288, 6)
    node(cx + 104, 288, 6)
    rect(cx - 116, 340, cx - 92, 400)
    rect(cx + 92, 340, cx + 116, 400)

    # Hips + legs, wireframe plates with bright knee-joint nodes.
    poly([(cx - 60, 300), (cx + 60, 300), (cx + 50, 340), (cx - 50, 340)])
    for side in (-1, 1):
        lx = cx + side * 32
        rect(lx - 22, 340, lx + 22, 430)
        rect(lx - 24, 430, lx + 24, 448)
        node(lx, 441, 8)
        rect(lx - 20, 452, lx + 20, 540)
        rect(lx - 24, 540, lx + 24, 566)

    # Scanline texture across the whole figure -- the "being read out by
    # a scanner" cue, cheap (one line per 3px row, low alpha).
    scan = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scan)
    for ly in range(0, H, 3):
        sd.line([(0, ly), (W, ly)], fill=(255, 210, 130, 14), width=1)
    img.alpha_composite(scan)

    # Scattered scan-node dots along the silhouette -- matches the
    # reference's field of small bright points around the main geometry,
    # not just on it.
    random.seed(9)
    for _ in range(22):
        nx = cx + random.uniform(-130, 130)
        ny = random.uniform(0, H)
        d.ellipse([nx - 1, ny - 1, nx + 1, ny + 1], fill=(255, 200, 110, random.randint(90, 200)))

    return glow(img, GOLD, blur=5)


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print("wrote", path, img.size)


def main():
    save(draw_relic_casing(), "relic_gauge.png")
    save(draw_body_design(), "body_design.png")


if __name__ == "__main__":
    main()
