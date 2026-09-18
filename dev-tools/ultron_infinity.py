#!/usr/bin/env python3
"""Upgrade Ultron's sprites to his Infinity-Stone form (ref: infinity ultron.jpg):
the same recognizable Ultron, but chromed to bright silver/titanium, a red gem on
the brow, the six Infinity Stones set across his chest, gold trim and a red cape.

Starts from the pixel reference figure, recolors, paints the stones/cape, then fits
the result into the existing sprite canvases (same anchoring as the base sprites so
the draw code still places him behind his desk / on the floor).

  ultron_work.png   424x494  head+chest bust
  ultron_walk_a.png 424x614  full body + cape
  ultron_walk_b.png 424x614  full body, bobbed
"""
import os
from collections import deque
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "pixel-assets"))
SRC = r"C:\Ultron Project\pixel ultron referance.png"
STONES = [(155, 89, 232), (60, 140, 245), (232, 60, 60), (245, 150, 40), (70, 210, 110), (245, 214, 70)]  # mind,space,reality,soul,time,power


def clean_figure():
    im = Image.open(SRC).convert("RGBA")
    w, h = im.size
    px = im.load()

    def pinkish(p):
        r, g, b = p[0], p[1], p[2]
        return r > 195 and g > 100 and b > 95 and abs(r - g) < 115 and (r - b) < 135

    seen = [[False] * w for _ in range(h)]
    q = deque([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] +
              [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y][x]:
            continue
        seen[y][x] = True
        p = px[x, y]
        if p[3] == 0 or pinkish(p):
            px[x, y] = (0, 0, 0, 0)
            q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    for y in range(int(h * 0.5), h):
        for x in range(w):
            if pinkish(px[x, y]):
                px[x, y] = (0, 0, 0, 0)
    return im.crop(im.getbbox())


def chrome(im):
    """Brighten neutral greys toward bright titanium; keep the reds (eyes/mouth)."""
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            mx, mn = max(r, g, b), min(r, g, b)
            is_red = r > 120 and r - g > 55 and r - b > 55
            if is_red or (mx - mn) > 60:   # keep reds and any already-saturated pixel
                continue
            # neutral grey -> chrome: lift luminance, add a faint cool highlight
            lum = (r + g + b) / 3
            nl = min(255, int(40 + lum * 1.18))
            px[x, y] = (min(255, nl + 6), min(255, nl + 10), min(255, nl + 18), a)
    return im


def upgrade(fig):
    fig = chrome(fig)
    px = fig.load()
    w, h = fig.size

    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] > 0

    def dot(x, y, c, rad=0):
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                if 0 <= x + dx < w and 0 <= y + dy < h:
                    px[x + dx, y + dy] = (c[0], c[1], c[2], 255)

    def gem(x, y, c, rad):   # like dot() but only paints OVER the body, so a bigger gem never spills onto transparency
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                X, Y = x + dx, y + dy
                if opaque(X, Y):
                    px[X, Y] = (c[0], c[1], c[2], 255)

    # brow gem (mind stone) at head center, ~18% down
    cx = w // 2
    dot(cx, int(h * 0.16), (245, 60, 60), 1)
    dot(cx, int(h * 0.16) - 1, (255, 180, 180), 0)

    # six Infinity Stones set in a row across the chest (~46% down) -- the signature.
    # Bigger + brighter so they read clearly: 5x5 gem, 3x3 bright core, white glint,
    # and a wider colour glow ring around each (kept on the body via gem()/opaque()).
    cy = int(h * 0.46)
    span = int(w * 0.56)
    x0 = cx - span // 2
    for i, col in enumerate(STONES):
        gx = x0 + int(i * span / 5)
        if opaque(gx, cy) or opaque(gx, cy + 1) or opaque(gx, cy - 1):
            bright = (min(255, col[0] + 80), min(255, col[1] + 80), min(255, col[2] + 80))
            gem(gx, cy, col, 2)              # 5x5 gem
            gem(gx, cy, bright, 1)           # 3x3 bright core
            dot(gx, cy - 1, (255, 255, 255), 0)  # white top glint
            for ox, oy in ((3, 0), (-3, 0), (0, 3), (0, -3), (2, 2), (-2, 2), (2, -2), (-2, -2)):
                if opaque(gx + ox, cy + oy):
                    p = px[gx + ox, cy + oy]
                    px[gx + ox, cy + oy] = (min(255, (p[0] + col[0]) // 2 + 40),
                                            min(255, (p[1] + col[1]) // 2 + 40),
                                            min(255, (p[2] + col[2]) // 2 + 40), 255)

    # gold trim on the shoulders (top corners of the torso band)
    gold = (232, 184, 40)
    sy = int(h * 0.4)
    for gx in (int(w * 0.2), int(w * 0.8)):
        for dy in range(0, 3):
            for dx in range(-2, 3):
                if opaque(gx + dx, sy + dy):
                    px[gx + dx, sy + dy] = (gold[0], gold[1], gold[2], 255)
    return fig


def add_cape(fig):
    """Compose the figure over a modest red cape behind the shoulders->feet.
    Kept only a little wider than the figure so the sprite stays roughly square."""
    w, h = fig.size
    pad = int(w * 0.16)
    cw = w + pad * 2
    canvas = Image.new("RGBA", (cw, h), (0, 0, 0, 0))
    cape = Image.new("RGBA", (cw, h), (0, 0, 0, 0))
    cp = cape.load()
    cx = cw // 2
    top = int(h * 0.36)   # shoulder line
    for y in range(top, h - 2):
        f = (y - top) / max(1, (h - top))
        half = int(w * 0.26 + f * (pad + w * 0.06))   # widens gently toward the floor
        shade = int(150 - 60 * f)                     # brighter at the shoulders
        for x in range(cx - half, cx + half):
            if 0 <= x < cw:
                cp[x, y] = (max(70, shade), 22, 28, 255)
    canvas.alpha_composite(cape, (0, 0))
    canvas.alpha_composite(fig, (pad, 0))
    return canvas.crop(canvas.getbbox())


def fit(fig, cw, ch, frac_h, pad):
    """Scale (NEAREST) to fit within cw x (ch*frac_h), whichever bound binds, then
    bottom-center it so nothing is ever clipped by the canvas width."""
    fw, fh = fig.size
    target_h = int(ch * frac_h)
    sc_by_h = target_h / fh
    sc_by_w = (cw - 8) / fw
    scale = min(sc_by_h, sc_by_w)
    nw, nh = max(1, int(fw * scale)), max(1, int(fh * scale))
    sc = fig.resize((nw, nh), Image.NEAREST)
    out = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    out.alpha_composite(sc, ((cw - nw) // 2, ch - nh - pad))
    return out


def main():
    base = upgrade(clean_figure())
    fw, fh = base.size
    bust = base.crop((0, 0, fw, int(fh * 0.62)))
    fit(bust, 424, 494, 0.98, 6).save(os.path.join(ASSETS, "ultron_work.png"))
    caped = add_cape(base)
    wa = fit(caped, 424, 614, 0.97, 6)
    wa.save(os.path.join(ASSETS, "ultron_walk_a.png"))
    wb = Image.new("RGBA", (424, 614), (0, 0, 0, 0))
    wb.alpha_composite(wa, (0, -7))
    wb.save(os.path.join(ASSETS, "ultron_walk_b.png"))
    # big preview
    prev = base.resize((fw * 4, fh * 4), Image.NEAREST)
    prev.save(os.path.join(HERE, "_infinity_preview.png"))
    print("wrote infinity ultron sprites; figure %dx%d" % (fw, fh))


if __name__ == "__main__":
    main()
