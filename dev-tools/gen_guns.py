#!/usr/bin/env python3
"""Original pixel-gun arsenal for Ultron's Corner. Procedurally draws a set of
weapons across the same categories as the reference sheets (signature energy
weapons; a plasma / sci-fi set; a ballistic set: pistol -> SMG -> rifle ->
shotgun -> sniper -> heavy) in the game's own palette -- original art, not traced
from any sheet. Each gun is a transparent PNG in pixel-assets/gun_<id>.png plus a
manifest (guns_manifest.json) the dashboard reads to build the Arsenal.
"""
import os, json
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "pixel-assets"))
U = 4  # pixel scale

DARK = (26, 28, 33)
STEEL = (92, 100, 112)
STEEL_D = (58, 64, 74)
STEEL_L = (150, 160, 174)
WOOD = (120, 78, 44)
WOOD_D = (86, 54, 30)


def new(w, h):
    return Image.new("RGBA", (w * U, h * U), (0, 0, 0, 0))


def rect(d, x, y, w, h, c):
    d.rectangle([x * U, y * U, (x + w) * U - 1, (y + h) * U - 1], fill=c)


def px(d, x, y, c):
    rect(d, x, y, 1, 1, c)


def energy(d, x, y, w, h, c):
    """a glowing energy cell: core + lighter rim."""
    rect(d, x, y, w, h, c)
    lc = tuple(min(255, v + 90) for v in c[:3]) + (255,)
    rect(d, x, y, w, 1, lc)
    rect(d, x + w - 1, y, 1, h, lc)


def outline(img):
    """add a 1px dark edge around opaque pixels for a crisp read."""
    base = img.load()
    W, Hh = img.size
    edge = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ep = edge.load()
    for yy in range(0, Hh, U):
        for xx in range(0, W, U):
            if base[xx, yy][3] == 0:
                for ox, oy in ((U, 0), (-U, 0), (0, U), (0, -U)):
                    nx, ny = xx + ox, yy + oy
                    if 0 <= nx < W and 0 <= ny < Hh and base[nx, ny][3] > 0:
                        for iy in range(U):
                            for ix in range(U):
                                ep[xx + ix, yy + iy] = (10, 11, 14, 255)
                        break
    edge.alpha_composite(img)
    return edge


# ---------- ballistic guns (accent = magazine / furniture tint) ----------
def pistol(accent):
    img = new(20, 14); d = ImageDraw.Draw(img)
    rect(d, 3, 3, 11, 4, STEEL)          # slide
    rect(d, 3, 3, 11, 1, STEEL_L)
    rect(d, 13, 4, 4, 2, STEEL_D)        # muzzle
    rect(d, 5, 7, 5, 6, STEEL_D)         # grip
    rect(d, 6, 7, 3, 5, accent)          # magazine
    px(d, 4, 7, DARK)
    return img


def smg(accent):
    img = new(28, 14); d = ImageDraw.Draw(img)
    rect(d, 4, 4, 15, 4, STEEL)
    rect(d, 4, 4, 15, 1, STEEL_L)
    rect(d, 18, 5, 6, 2, STEEL_D)        # barrel
    rect(d, 1, 4, 3, 3, STEEL_D)         # stock
    rect(d, 7, 8, 4, 5, accent)          # mag
    rect(d, 12, 8, 3, 4, STEEL_D)        # grip
    return img


def rifle(accent, wood=False):
    img = new(34, 14); d = ImageDraw.Draw(img)
    body = WOOD if wood else STEEL
    rect(d, 2, 4, 20, 4, body)
    rect(d, 2, 4, 20, 1, WOOD_D if wood else STEEL_L)
    rect(d, 21, 5, 10, 2, STEEL_D)       # long barrel
    rect(d, 0, 4, 3, 4, WOOD_D if wood else STEEL_D)  # stock
    rect(d, 9, 8, 4, 5, accent)          # mag
    rect(d, 14, 8, 3, 4, STEEL_D)        # grip
    rect(d, 6, 2, 4, 2, STEEL_D)         # sight
    return img


def shotgun(accent):
    img = new(34, 14); d = ImageDraw.Draw(img)
    rect(d, 2, 5, 18, 3, WOOD)
    rect(d, 2, 5, 18, 1, WOOD_D)
    rect(d, 19, 4, 13, 2, STEEL_D)       # barrel top
    rect(d, 19, 6, 13, 2, STEEL)         # barrel bottom (double)
    rect(d, 0, 5, 3, 5, WOOD_D)          # stock
    rect(d, 8, 8, 6, 3, accent)          # pump
    return img


def sniper(accent):
    img = new(38, 14); d = ImageDraw.Draw(img)
    rect(d, 2, 6, 22, 3, STEEL)
    rect(d, 2, 6, 22, 1, STEEL_L)
    rect(d, 23, 7, 13, 2, STEEL_D)       # very long barrel
    rect(d, 0, 6, 3, 4, STEEL_D)         # stock
    rect(d, 9, 3, 8, 2, DARK)            # scope tube
    rect(d, 10, 2, 6, 1, accent)
    rect(d, 11, 9, 4, 4, accent)         # mag
    return img


def heavy(accent):
    img = new(34, 18); d = ImageDraw.Draw(img)
    rect(d, 4, 5, 18, 6, STEEL_D)        # bulky receiver
    rect(d, 4, 5, 18, 1, STEEL_L)
    rect(d, 21, 6, 11, 4, STEEL)         # thick barrel
    for i in range(5):                   # barrel shroud vents
        px(d, 23 + i * 2, 6, DARK)
    rect(d, 1, 5, 3, 5, STEEL_D)
    rect(d, 8, 11, 6, 5, accent)         # box mag
    rect(d, 15, 11, 3, 4, STEEL_D)
    return img


# ---------- plasma / sci-fi guns (accent = energy colour) ----------
def plasma_pistol(accent):
    img = new(22, 15); d = ImageDraw.Draw(img)
    rect(d, 3, 4, 11, 5, STEEL)
    rect(d, 3, 4, 11, 1, STEEL_L)
    rect(d, 13, 5, 5, 3, DARK)
    energy(d, 15, 5, 3, 3, accent)       # muzzle cell
    rect(d, 5, 9, 5, 5, STEEL_D)
    energy(d, 6, 4, 3, 2, accent)        # top cell
    return img


def plasma_rifle(accent):
    img = new(34, 16); d = ImageDraw.Draw(img)
    rect(d, 3, 5, 20, 5, STEEL)
    rect(d, 3, 5, 20, 1, STEEL_L)
    rect(d, 22, 6, 9, 3, DARK)
    energy(d, 29, 6, 3, 3, accent)       # muzzle
    energy(d, 8, 3, 8, 2, accent)        # top rail cells
    rect(d, 1, 5, 3, 4, STEEL_D)
    energy(d, 10, 10, 4, 3, accent)      # battery mag
    rect(d, 15, 10, 3, 4, STEEL_D)
    return img


def plasma_cannon(accent):
    img = new(38, 20); d = ImageDraw.Draw(img)
    rect(d, 4, 6, 20, 8, STEEL_D)
    rect(d, 4, 6, 20, 1, STEEL_L)
    energy(d, 8, 8, 12, 4, accent)       # big energy core
    rect(d, 23, 8, 11, 5, STEEL)         # muzzle housing
    energy(d, 31, 9, 3, 3, accent)
    rect(d, 1, 7, 3, 5, STEEL_D)
    rect(d, 12, 14, 6, 5, STEEL_D)
    energy(d, 20, 4, 4, 2, accent)
    return img


# ---------- signature hero weapons ----------
def signature(kind, accent):
    if kind == "lance":                  # long energy rifle
        img = new(44, 18); d = ImageDraw.Draw(img)
        rect(d, 4, 6, 26, 6, STEEL); rect(d, 4, 6, 26, 1, STEEL_L)
        energy(d, 30, 7, 10, 4, accent)  # long energy emitter
        energy(d, 8, 3, 16, 2, accent)   # top charge rail
        rect(d, 1, 6, 3, 6, (232, 184, 40, 255))  # gold stock
        energy(d, 6, 12, 5, 4, accent)
        rect(d, 14, 12, 4, 5, (232, 184, 40, 255))
        return img
    if kind == "blaster":                # plasma blaster
        img = new(38, 18); d = ImageDraw.Draw(img)
        rect(d, 5, 6, 18, 6, STEEL_D); rect(d, 5, 6, 18, 1, STEEL_L)
        energy(d, 9, 8, 10, 3, accent)
        rect(d, 22, 7, 10, 4, (232, 184, 40, 255))  # gold barrel
        energy(d, 30, 8, 3, 3, accent)
        rect(d, 2, 7, 3, 5, (232, 184, 40, 255))
        rect(d, 12, 12, 6, 5, STEEL_D)
        energy(d, 6, 4, 4, 2, accent)
        return img
    # scepter / staff cannon (vertical-ish)
    img = new(20, 36); d = ImageDraw.Draw(img)
    rect(d, 8, 2, 4, 30, (232, 184, 40, 255))     # gold shaft
    rect(d, 8, 2, 1, 30, (255, 220, 120, 255))
    energy(d, 6, 4, 8, 5, accent)                  # top emitter
    energy(d, 5, 26, 10, 6, accent)                # base cannon
    rect(d, 4, 32, 12, 3, (232, 184, 40, 255))
    for yy in (12, 18, 24):
        energy(d, 7, yy, 6, 2, accent)
    return img


# rarity accent palette (matches the game's ladder)
RAR = {
    "Common": (150, 160, 174), "Uncommon": (51, 209, 122), "Rare": (61, 155, 255),
    "Epic": (176, 132, 240), "Legendary": (255, 157, 60), "Mythic": (255, 90, 122),
}

# ---- the arsenal: (id, display name, class, builder, rarity) ----
ARSENAL = [
    # signature energy weapons
    ("sig_lance", "Oxide Lance", "Signature", ("sig", "lance"), "Mythic"),
    ("sig_blaster", "Vibranium Blaster", "Signature", ("sig", "blaster"), "Legendary"),
    ("sig_scepter", "Genesis Scepter", "Signature", ("sig", "scepter"), "Mythic"),
    # ballistic set
    ("bal_pistol", "Sidewinder", "Pistol", ("pistol", None), "Common"),
    ("bal_pistol2", "Vandal", "Pistol", ("pistol", None), "Uncommon"),
    ("bal_smg", "Ripsaw SMG", "SMG", ("smg", None), "Uncommon"),
    ("bal_smg2", "Static SMG", "SMG", ("smg", None), "Rare"),
    ("bal_rifle", "Marauder", "Assault", ("rifle", False), "Rare"),
    ("bal_rifle_w", "Woodland AR", "Assault", ("rifle", True), "Uncommon"),
    ("bal_shotgun", "Breaker", "Shotgun", ("shotgun", None), "Rare"),
    ("bal_shotgun2", "Thunderclap", "Shotgun", ("shotgun", None), "Epic"),
    ("bal_sniper", "Longshot", "Sniper", ("sniper", None), "Epic"),
    ("bal_sniper2", "Reaper's Eye", "Sniper", ("sniper", None), "Legendary"),
    ("bal_heavy", "Juggernaut", "Heavy", ("heavy", None), "Epic"),
    ("bal_heavy2", "Devastator", "Heavy", ("heavy", None), "Legendary"),
    # plasma / sci-fi set
    ("plz_pistol", "Ion Sidearm", "Plasma Pistol", ("pp", None), "Uncommon"),
    ("plz_pistol2", "Volt Sidearm", "Plasma Pistol", ("pp", None), "Rare"),
    ("plz_rifle", "Pulse Rifle", "Plasma Rifle", ("pr", None), "Rare"),
    ("plz_rifle2", "Neon Rifle", "Plasma Rifle", ("pr", None), "Epic"),
    ("plz_rifle3", "Venom Rifle", "Plasma Rifle", ("pr", None), "Legendary"),
    ("plz_cannon", "Arc Cannon", "Plasma Cannon", ("pc", None), "Epic"),
    ("plz_cannon2", "Singularity Cannon", "Plasma Cannon", ("pc", None), "Mythic"),
]

BUILDERS = {
    "pistol": lambda arg, ac: pistol(ac), "smg": lambda arg, ac: smg(ac),
    "rifle": lambda arg, ac: rifle(ac, arg), "shotgun": lambda arg, ac: shotgun(ac),
    "sniper": lambda arg, ac: sniper(ac), "heavy": lambda arg, ac: heavy(ac),
    "pp": lambda arg, ac: plasma_pistol(ac), "pr": lambda arg, ac: plasma_rifle(ac),
    "pc": lambda arg, ac: plasma_cannon(ac), "sig": lambda arg, ac: signature(arg, ac),
}


def main():
    manifest = []
    # plasma/sig accents cycle through vivid energy colours
    energy_cols = {
        "plz_pistol": (90, 220, 255), "plz_pistol2": (120, 150, 255),
        "plz_rifle": (90, 220, 255), "plz_rifle2": (255, 120, 230), "plz_rifle3": (120, 240, 120),
        "plz_cannon": (255, 170, 60), "plz_cannon2": (180, 120, 255),
        "sig_lance": (90, 220, 255), "sig_blaster": (60, 230, 200), "sig_scepter": (120, 220, 255),
    }
    for gid, name, cls, (b, arg), rar in ARSENAL:
        accent = energy_cols.get(gid, RAR[rar]) + (255,) if gid in energy_cols else RAR[rar] + (255,)
        img = BUILDERS[b](arg, accent)
        img = outline(img)
        img.save(os.path.join(ASSETS, "gun_%s.png" % gid))
        manifest.append({"id": gid, "name": name, "cls": cls, "rarity": rar})
    with open(os.path.join(ASSETS, "guns_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    # contact sheet for review
    cols = 5
    cw = max(i["id"] and 200 for i in manifest) or 200
    rows = (len(ARSENAL) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 200, rows * 120), (44, 46, 54, 255))
    for idx, (gid, name, *_ ) in enumerate(ARSENAL):
        g = Image.open(os.path.join(ASSETS, "gun_%s.png" % gid))
        gx = (idx % cols) * 200 + (200 - g.width) // 2
        gy = (idx // cols) * 120 + (110 - g.height)
        sheet.alpha_composite(g, (gx, max(0, gy)))
    sheet.save(os.path.join(HERE, "_guns_preview.png"))
    print("wrote %d guns + manifest" % len(ARSENAL))


if __name__ == "__main__":
    main()
