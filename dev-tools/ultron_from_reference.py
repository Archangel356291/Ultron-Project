#!/usr/bin/env python3
"""Rebuild Odin's in-game sprites so he looks exactly like the pixel reference
art (pixel ultron referance.png). Pink background -> transparent, crisp NEAREST
upscale, anchored to match the existing sprite canvases so the draw code keeps
placing him correctly behind his desk / on the floor.

  ultron_work.png   424x494  head+chest bust (desk hides the rest)
  ultron_walk_a.png 424x614  full body
  ultron_walk_b.png 424x614  full body, bobbed for a 2-frame step
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "pixel-assets"))
SRC = r"C:\Ultron Project\pixel ultron referance.png"
PINK = (254, 165, 161)

def load_figure():
    im = Image.open(SRC).convert("RGBA")
    w, h = im.size
    px = im.load()

    def pinkish(p):
        r, g, b = p[0], p[1], p[2]
        # pink field (incl. its darker shaded salmon) is warm with g,b both fairly
        # high; the red accents are r-high but g,b LOW (~40), so they're excluded.
        return r > 195 and g > 100 and b > 95 and abs(r - g) < 115 and (r - b) < 135

    # flood fill the connected background from every border pixel -> transparent.
    # interior reds aren't border-connected through pink, so they're preserved.
    from collections import deque
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            q.append((x, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y][x]:
            continue
        seen[y][x] = True
        p = px[x, y]
        if p[3] == 0 or pinkish(p):
            px[x, y] = (0, 0, 0, 0)
            q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    # second pass: kill any pink pockets trapped in the LOWER body (e.g. between
    # the legs) that the border fill couldn't reach. Restricted below the head so
    # the red under-eye glow up top is never touched.
    for y in range(int(h * 0.5), h):
        for x in range(w):
            if pinkish(px[x, y]):
                px[x, y] = (0, 0, 0, 0)
    return im.crop(im.getbbox())   # tight crop to the figure

def fit(fig, cw, ch, frac_h, anchor_bottom_pad):
    """Scale fig (NEAREST) so its height = ch*frac_h, center horizontally,
    sit its feet anchor_bottom_pad px above the canvas bottom."""
    fw, fh = fig.size
    target_h = int(ch * frac_h)
    scale = max(1, round(target_h / fh))
    # prefer integer scale for crisp pixels; fall back to exact if too big/small
    sc = fig.resize((fw * scale, fh * scale), Image.NEAREST)
    if sc.size[1] > ch - 4 or sc.size[1] < target_h * 0.7:
        sc = fig.resize((max(1, int(fw * target_h / fh)), target_h), Image.NEAREST)
    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    x = (cw - sc.size[0]) // 2
    y = ch - sc.size[1] - anchor_bottom_pad
    canvas.alpha_composite(sc, (max(0, x), max(0, y)))
    return canvas

def main():
    fig = load_figure()
    fw, fh = fig.size
    # bust = top ~62% of the figure (head + chest), for the seated 'work' sprite
    bust = fig.crop((0, 0, fw, int(fh * 0.62)))
    work = fit(bust, 424, 494, 0.98, 6)
    work.save(os.path.join(ASSETS, "ultron_work.png"))
    walk_a = fit(fig, 424, 614, 0.97, 6)
    walk_a.save(os.path.join(ASSETS, "ultron_walk_a.png"))
    # walk_b: same figure lifted a few px for a simple 2-frame bob-step
    wb = Image.new("RGBA", (424, 614), (0, 0, 0, 0))
    wb.alpha_composite(walk_a, (0, -7))
    wb.save(os.path.join(ASSETS, "ultron_walk_b.png"))
    print("wrote ultron_work.png, ultron_walk_a.png, ultron_walk_b.png from reference (figure %dx%d)" % (fw, fh))

if __name__ == "__main__":
    main()
