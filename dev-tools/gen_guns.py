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


# ---------- weapon PARTS (custom-build section) ----------
# accent brightens with the option index (more advanced = more energy)
PART_AC = [(150, 160, 174), (90, 220, 255), (90, 150, 255), (176, 132, 240), (255, 184, 60)]


def pac(oi):
    return PART_AC[min(oi, len(PART_AC) - 1)] + (255,)


def part_chassis(oi):
    ac = pac(oi); img = new(22, 15); d = ImageDraw.Draw(img)
    rect(d, 3, 4, 14, 7, STEEL); rect(d, 3, 4, 14, 1, STEEL_L)      # receiver body
    rect(d, 5, 11, 5, 3, STEEL_D)                                    # trigger housing
    rect(d, 15, 6, 4, 3, STEEL_D)                                    # ejection port
    if oi == 0: rect(d, 6, 6, 8, 1, STEEL_D)
    elif oi == 1:
        for x in (5, 8, 11, 14): rect(d, x, 5, 1, 5, STEEL_L)        # rail slots
    else:
        energy(d, 6, 6, 8, 3, ac)                                    # containment core
        if oi >= 3: energy(d, 8, 3, 4, 2, ac)                        # top vent glow
    return img


def part_barrel(oi):
    ac = pac(oi); img = new(26, 11); d = ImageDraw.Draw(img)
    if oi == 4:                                                      # gatling rotary cluster
        for yy in (2, 5, 8): rect(d, 3, yy, 18, 2, STEEL_D)
        rect(d, 1, 2, 3, 8, STEEL)
        return img
    rect(d, 2, 4, 20, 3, STEEL_D); rect(d, 2, 4, 20, 1, STEEL_L)     # base barrel
    if oi == 1: rect(d, 2, 3, 9, 5, STEEL); energy(d, 20, 4, 4, 3, ac)   # short + emitter cell
    elif oi == 2:
        for x in (5, 9, 13, 17): rect(d, x, 2, 2, 7, ac)            # EM coils
    elif oi == 3:
        energy(d, 20, 2, 5, 6, ac)                                  # focusing lens
    return img


def part_power(oi):
    ac = pac(max(1, oi)); img = new(15, 17); d = ImageDraw.Draw(img)
    if oi == 0:
        rect(d, 4, 3, 7, 12, STEEL); rect(d, 4, 3, 7, 1, STEEL_L)
        for yy in (6, 9, 12): rect(d, 4, yy, 7, 1, STEEL_D)         # slug clip ribs
    elif oi == 1:
        rect(d, 4, 2, 7, 13, STEEL_D); energy(d, 5, 4, 5, 9, ac)     # gas canister
        rect(d, 5, 1, 5, 2, STEEL)
    elif oi == 2:
        rect(d, 3, 4, 9, 10, STEEL); energy(d, 4, 6, 7, 4, ac); rect(d, 6, 2, 4, 2, STEEL_D)  # battery
    else:
        rect(d, 3, 3, 9, 11, DARK)
        energy(d, 5, 5, 6, 6, ac); px(d, 7, 7, (255, 255, 255))     # singularity cell
    return img


def part_stock(oi):
    ac = pac(oi); img = new(22, 13); d = ImageDraw.Draw(img)
    if oi == 0:
        rect(d, 6, 4, 6, 8, STEEL_D); rect(d, 6, 4, 6, 1, STEEL_L)  # pistol grip
    elif oi == 1:
        rect(d, 2, 5, 14, 3, STEEL); rect(d, 2, 5, 4, 3, STEEL_D)   # collapsible
        rect(d, 15, 4, 3, 5, STEEL_D)
    elif oi == 2:
        rect(d, 2, 4, 15, 6, STEEL_D); rect(d, 2, 4, 15, 1, STEEL_L)
        for x in (4, 6, 8): rect(d, x, 5, 1, 4, ac)                 # shock spring
    else:
        rect(d, 2, 4, 15, 6, STEEL)
        for x in (4, 7, 10, 13): rect(d, x, 5, 1, 4, ac)            # smart-link circuits
        energy(d, 14, 5, 2, 2, ac)
    return img


def part_optic(oi):
    ac = pac(oi + 1); img = new(20, 12); d = ImageDraw.Draw(img)
    if oi == 0:
        rect(d, 6, 4, 8, 4, STEEL_D); rect(d, 5, 8, 10, 1, STEEL_D)  # red-dot base
        energy(d, 9, 5, 2, 2, (255, 60, 60, 255))
    elif oi == 1:
        rect(d, 4, 4, 12, 4, STEEL); rect(d, 4, 8, 12, 1, STEEL_D)
        for x in (6, 9, 12): rect(d, x, 5, 1, 2, ac)                # HUD ticks
    else:
        rect(d, 3, 4, 13, 4, STEEL_D); rect(d, 3, 8, 13, 1, STEEL_D)
        energy(d, 14, 4, 4, 4, ac)                                  # thermal lens
    return img


def part_aux(oi):
    ac = pac(oi + 1); img = new(16, 15); d = ImageDraw.Draw(img)
    if oi == 0:                                                     # cooling loop (square ring)
        rect(d, 4, 3, 8, 8, ac); rect(d, 6, 5, 4, 4, (0, 0, 0, 0))
        rect(d, 6, 5, 4, 4, DARK)
    elif oi == 1:                                                   # vibro-bayonet
        d.polygon([(3 * U, 11 * U), (5 * U, 11 * U), (12 * U, 2 * U), (10 * U, 2 * U)], fill=STEEL_L)
        rect(d, 3, 10, 4, 3, STEEL_D)
    elif oi == 2:                                                   # micro-grapnel hook
        rect(d, 7, 3, 2, 8, STEEL); rect(d, 5, 10, 6, 2, STEEL)
        rect(d, 4, 8, 2, 3, ac); rect(d, 10, 8, 2, 3, ac)
    else:                                                           # EMP suppressor
        rect(d, 5, 4, 6, 8, STEEL_D); energy(d, 6, 5, 4, 6, ac)
        rect(d, 3, 7, 2, 2, ac); rect(d, 11, 7, 2, 2, ac)          # pulse rings
    return img


PART_BUILDERS = {"chassis": part_chassis, "barrel": part_barrel, "power": part_power,
                 "stock": part_stock, "optic": part_optic, "aux": part_aux}
PART_COUNTS = {"chassis": 4, "barrel": 5, "power": 4, "stock": 4, "optic": 3, "aux": 4}


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
    # second wave -- same rough designs, new names / rarities
    ("bal_pistol3", "Hornet", "Pistol", ("pistol", None), "Rare"),
    ("bal_smg3", "Wraith SMG", "SMG", ("smg", None), "Epic"),
    ("bal_rifle2", "Ravager", "Assault", ("rifle", False), "Epic"),
    ("bal_shotgun3", "Sawed-Off", "Shotgun", ("shotgun", None), "Uncommon"),
    ("bal_sniper3", "Void Lance", "Sniper", ("sniper", None), "Mythic"),
    ("bal_heavy3", "Annihilator", "Heavy", ("heavy", None), "Mythic"),
    ("plz_pistol3", "Nova Sidearm", "Plasma Pistol", ("pp", None), "Epic"),
    ("plz_cannon3", "Rift Cannon", "Plasma Cannon", ("pc", None), "Legendary"),
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
    # weapon PARTS for the custom-build section: one icon per group + option index
    for gid, n in PART_COUNTS.items():
        for oi in range(n):
            pimg = outline(PART_BUILDERS[gid](oi))
            pimg.save(os.path.join(ASSETS, "part_%s_%d.png" % (gid, oi)))
    print("wrote %d part icons" % sum(PART_COUNTS.values()))
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
