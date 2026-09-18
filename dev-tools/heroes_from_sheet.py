#!/usr/bin/env python3
"""Slice the 7 in-game heroes out of the pixel Marvel sheet (pixel mcu.jpg) so the
office cameos look exactly like those sprites. White background -> transparent via
a border flood fill (interior whites like eyes/stars are preserved), tight-cropped.

Saved to pixel-assets/hero_<kind>.png at their native pixel resolution; the game
upscales them with NEAREST so they stay crisp.
"""
import os
from collections import deque
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "pixel-assets"))
SRC = r"C:\Ultron Project\pixel mcu.jpg"
COLS, ROWS = 6, 8

# kind -> (row, col) in the sheet
CELLS = {
    "cap":     (0, 0),
    "ironman": (0, 1),
    "thor":    (0, 2),
    "hulk":    (0, 5),
    "panther": (1, 2),
    "widow":   (1, 4),
    "vision":  (1, 5),
}

def is_white(p):
    return p[0] > 232 and p[1] > 232 and p[2] > 232

def cut(im, r, c, cw, ch):
    # crop the cell with a tiny inset to avoid a neighbour bleeding in
    x0, y0 = int(c * cw), int(r * ch)
    x1, y1 = int((c + 1) * cw), int((r + 1) * ch)
    cell = im.crop((x0, y0, x1, y1)).convert("RGBA")
    w, h = cell.size
    px = cell.load()
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y][x]:
            continue
        seen[y][x] = True
        if is_white(px[x, y]):
            px[x, y] = (0, 0, 0, 0)
            q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    # keep only the largest connected blob of opaque pixels -- drops stray bits of
    # a neighbouring character that overlapped this cell's top/bottom edge.
    comp = [[0] * w for _ in range(h)]
    blobs = []
    cid = 0
    for sy in range(h):
        for sx in range(w):
            if px[sx, sy][3] > 0 and comp[sy][sx] == 0:
                cid += 1
                cells = []
                dq = deque([(sx, sy)])
                comp[sy][sx] = cid
                while dq:
                    x, y = dq.popleft()
                    cells.append((x, y))
                    for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                        if 0 <= nx < w and 0 <= ny < h and comp[ny][nx] == 0 and px[nx, ny][3] > 0:
                            comp[ny][nx] = cid
                            dq.append((nx, ny))
                blobs.append((len(cells), cid))
    if blobs:
        keep = max(blobs)[1]
        for y in range(h):
            for x in range(w):
                if comp[y][x] != keep:
                    px[x, y] = (0, 0, 0, 0)
    bbox = cell.getbbox()
    return cell.crop(bbox) if bbox else cell

def main():
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    cw, ch = W / COLS, H / ROWS
    for kind, (r, c) in CELLS.items():
        sprite = cut(im, r, c, cw, ch)
        sprite.save(os.path.join(ASSETS, "hero_%s.png" % kind))
        print("  hero_%s.png %s" % (kind, sprite.size))
    print("done")

if __name__ == "__main__":
    main()
