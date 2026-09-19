"""Generates the two new visual assets for the "Odin's Designs" tab
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
  an owner-supplied Odin-style character render. Original silhouette,
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


def shade_tuple(color, factor):
    r, g, b = (max(0, min(255, int(c * factor))) for c in color[:3])
    return (r, g, b, color[3] if len(color) > 3 else 255)


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
    per the owner's reference photo (a vertical relic with a dense red
    circuit/vein pattern etched across nearly the whole dark chamber face),
    rather than a flat black fill. Drawn once, low-cost (a handful of
    random-walk line segments), sits *underneath* the dashboard's live
    percentage-fill DOM element (see .relic-gauge-fill in
    ultron-dashboard.html), which fully covers whatever's here below its
    own fill line -- so this only shows through the unfilled portion, same
    as the reference's resting glow.

    Quality pass (2026-09-15, owner-supplied relic photo): the reference's
    veins cover most of the chamber's height, not just a small band near
    the bottom -- more seed points, spread across the full height, longer
    reach, deeper branching, and a brighter core line under the soft glow
    line so thin veins don't just read as blur."""
    import math
    random.seed(seed)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def branch(x, y, angle, length, depth):
        if depth <= 0 or length < 3:
            return
        dx = math.sin(angle) * length
        dy = math.cos(angle) * length
        nx, ny = x + dx, y + dy
        d.line([(x, y), (nx, ny)], fill=(255, 70, 55, random.randint(120, 200)), width=1)
        if random.random() < 0.75:
            branch(nx, ny, angle + random.uniform(-0.7, 0.7), length * random.uniform(0.62, 0.85), depth - 1)
        if random.random() < 0.55:
            branch(nx, ny, angle + random.uniform(0.7, 1.6), length * random.uniform(0.45, 0.65), depth - 1)
        if random.random() < 0.3:
            branch(nx, ny, angle + random.uniform(-1.6, -0.7), length * random.uniform(0.4, 0.6), depth - 1)

    # Seed branches from points spread across the whole chamber height,
    # each growing both up and down, so the pattern fills the face instead
    # of clustering at one edge.
    for _ in range(11):
        sx, sy = w * random.uniform(0.15, 0.85), h * random.uniform(0.08, 0.92)
        branch(sx, sy, random.uniform(-0.5, 0.5), h * 0.16, 6)
        branch(sx, sy, math.pi + random.uniform(-0.5, 0.5), h * 0.14, 5)

    glow_layer = img.filter(ImageFilter.GaussianBlur(1.1))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(glow_layer)
    out.alpha_composite(img)  # crisp core vein on top of its own soft bloom
    return out


# The fillable interior rect -- exported so the JS side can hardcode the
# exact same numbers (see the "Odin's Designs" tab script in
# ultron-dashboard.html) and clip its real-percentage fill to line up
# precisely with this casing's chamber.
CANVAS_W, CANVAS_H = 200, 560
FILL_RECT = (70, 130, 130, 460)  # x0, y0, x1, y1 -- y1 is the chamber's bottom (0% fill line)


CHROME_DARK = (60, 64, 70, 255)
CHROME_MID = (150, 156, 166, 255)
CHROME_LIGHT = (222, 227, 234, 255)
CHROME_HOT = (255, 255, 255, 255)


def chrome_gradient(w, h, vertical=True):
    """A banded light/mid/dark/mid/light sweep -- cheap stand-in for a real
    specular reflection, the single biggest lever for flat Pillow rects to
    read as polished metal instead of solid gray (per the owner's relic
    photo, whose fittings are clearly brushed/polished chrome, not flat
    steel)."""
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    stops = [CHROME_DARK, CHROME_MID, CHROME_LIGHT, CHROME_HOT, CHROME_LIGHT, CHROME_MID, CHROME_DARK]
    n = len(stops) - 1
    span = h if vertical else w
    for i in range(span):
        t = i / max(1, span - 1)
        seg = min(n - 1, int(t * n))
        local_t = t * n - seg
        c0, c1 = stops[seg], stops[seg + 1]
        col = tuple(int(c0[k] + (c1[k] - c0[k]) * local_t) for k in range(3)) + (255,)
        if vertical:
            ImageDraw.Draw(grad).line([(0, i), (w, i)], fill=col)
        else:
            ImageDraw.Draw(grad).line([(i, 0), (i, h)], fill=col)
    return grad


def draw_relic_casing():
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = FILL_RECT
    cx = (x0 + x1) / 2

    # Base: a museum-plaque stand -- wide dark plinth, a bright chrome lip,
    # and a small engraved-look nameplate strip -- per the reference photo's
    # display-stand base rather than a bare rectangle.
    d.rectangle([30, 526, 170, 552], fill=(6, 6, 7, 255), outline=LINE, width=1)
    plinth_lip = chrome_gradient(140, 6, vertical=True)
    img.alpha_composite(plinth_lip, (30, 520))
    d.rectangle([70, 534, 130, 546], fill=(3, 3, 4, 255), outline=shade_tuple(STEEL, 0.6), width=1)
    for tx in range(74, 126, 7):
        d.rectangle([tx, 538, tx + 4, 540], fill=(90, 96, 104, 160))  # faint engraved ticks
    d.rectangle([60, 507, 140, 522], fill=BODY_DARK, outline=LINE, width=1)
    col_grad = chrome_gradient(int(x1 - x0 + 16), int(508 - y1), vertical=False)
    img.alpha_composite(col_grad, (int(x0 - 8), int(y1)))
    d.rectangle([x0 - 8, y1, x1 + 8, 508], outline=LINE, width=2)

    # Chamber (dark by default -- JS fills it live, see FILL_RECT/
    # .relic-gauge-fill). A dense glowing vein texture underneath, per the
    # owner's reference photo, instead of flat black.
    d.rectangle([x0, y0, x1, y1], fill=(4, 4, 5, 255))
    veins = draw_vein_texture(int(x1 - x0), int(y1 - y0))
    img.alpha_composite(veins, (int(x0), int(y0)))

    # Side fittings running the full chamber height -- dense stepped
    # chrome blades (reference: a continuous finned edge, not a few
    # isolated notches), each blade individually gradient-shaded.
    fin_h = 22
    for ny in range(int(y0), int(y1) - fin_h // 2, fin_h):
        for side, fx0, fx1 in ((-1, x0 - 16, x0), (1, x1, x1 + 16)):
            fin = chrome_gradient(int(fx1 - fx0), fin_h - 4, vertical=True)
            fin_shape = Image.new("RGBA", fin.size, (0, 0, 0, 0))
            pts = [(0, 2), (fin.size[0] if side < 0 else fin.size[0] * 0.35, 0),
                   (fin.size[0], fin.size[1] * 0.5), (fin.size[0] if side < 0 else fin.size[0] * 0.35, fin.size[1]),
                   (0, fin.size[1] - 2)]
            mask = Image.new("L", fin.size, 0)
            ImageDraw.Draw(mask).polygon(pts, fill=255)
            fin_shape.paste(fin, (0, 0), mask)
            img.alpha_composite(fin_shape, (int(fx0), ny + 1))

    # Top fitting block (chrome-shaded) + four spiky prongs, the
    # reference's most distinctive silhouette element.
    top_block = chrome_gradient(int(x1 - x0 + 20), 34, vertical=True)
    img.alpha_composite(top_block, (int(x0 - 10), int(y0 - 34)))
    d.rectangle([x0 - 10, y0 - 34, x1 + 10, y0], outline=LINE, width=2)
    prong_w = (x1 - x0 - 10) / 4
    for i in range(4):
        px = x0 + 5 + i * prong_w
        d.polygon([(px, y0 - 34), (px + prong_w * 0.6, y0 - 70), (px + prong_w, y0 - 34)], fill=CHROME_MID)
        d.polygon([(px, y0 - 34), (px + prong_w * 0.3, y0 - 55), (px + prong_w * 0.6, y0 - 70)], fill=CHROME_LIGHT)
    d.rectangle([x0 - 10, y0 - 40, x1 + 10, y0 - 34], fill=(10, 10, 11, 255))

    # A small always-on indicator light near the base, independent of
    # the fill level -- just a "power on" tell, not a data readout.
    d.ellipse([cx - 6, 480, cx + 6, 492], fill=RED_BRIGHT)
    d.ellipse([cx - 3, 483, cx - 1, 485], fill=(255, 220, 210, 230))  # hot-spot catch-light

    return glow(outline(img, size=3), RED_BRIGHT, blur=5)


GOLD = (255, 178, 56, 255)
GOLD_FILL = (255, 178, 56, 26)


def draw_body_design():
    """A holographic wireframe scan, not a solid-shaded figure -- per the
    owner's "design visual reference" (a Territory-Studio-style HUD
    showing a body as glowing gold wireframe/geometry under scan, not
    rendered in its real material colors). Gold/amber here specifically
    means "concept hologram," distinct from the red the pixel-companion
    and relic use for Odin's own real, physical glow (see
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

    # Chest core -- a bright scan hot-spot, the reference's brightest point,
    # with thin radiating spokes (per the owner's hologram-bay reference,
    # whose brightest point throws visible light rays, not just a glow).
    rect(cx - 32, 175, cx + 32, 260)
    node(cx, 221, 20)
    import math as _math
    for i in range(10):
        ang = i * (_math.pi * 2 / 10)
        r1, r2 = 22, random.uniform(34, 58)
        d.line([(cx + _math.cos(ang) * r1, 221 + _math.sin(ang) * r1),
                (cx + _math.cos(ang) * r2, 221 + _math.sin(ang) * r2)],
               fill=(255, 210, 140, 130), width=1)
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

    # Exploded fragment field -- small floating panel pieces just outside
    # the main silhouette, per the owner's hologram-bay reference (a body
    # assembled from many small suspended plates, not one solid outline).
    # Cheap: a scatter of tiny translucent trapezoids anchored along the
    # figure's own left/right edges at varying depth (size/opacity).
    random.seed(41)
    frag_anchors_y = list(range(20, H - 40, 14))
    for fy in frag_anchors_y:
        for side in (-1, 1):
            if random.random() < 0.4:
                continue
            depth = random.uniform(0.4, 1.0)  # 1.0 = near/bright, 0.4 = far/dim
            fx = cx + side * random.uniform(60, 150) * depth
            fw, fh = random.uniform(8, 20) * depth, random.uniform(10, 26) * depth
            skew = random.uniform(-4, 4)
            pts = [(fx, fy), (fx + fw, fy + skew), (fx + fw * 0.85, fy + fh), (fx - fw * 0.15, fy + fh - skew)]
            alpha_fill = int(18 * depth) + 6
            alpha_line = int(140 * depth) + 40
            d.polygon(pts, fill=(255, 178, 56, alpha_fill), outline=(255, 200, 110, alpha_line))

    # Two faint vertical scan-beam columns crossing the whole figure, per
    # the reference's hologram-bay lighting (thin bright verticals cutting
    # through the projection volume).
    beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beams)
    for bx in (cx - 70, cx + 55):
        bd.rectangle([bx, 0, bx + 3, H], fill=(255, 220, 160, 20))
    img.alpha_composite(beams)

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
    for _ in range(48):
        nx = cx + random.uniform(-150, 150)
        ny = random.uniform(0, H)
        r = random.uniform(0.6, 2.2)
        d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=(255, 200, 110, random.randint(70, 210)))

    return glow(img, GOLD, blur=6)


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print("wrote", path, img.size)


def main():
    save(draw_relic_casing(), "relic_gauge.png")
    save(draw_body_design(), "body_design.png")


if __name__ == "__main__":
    main()
