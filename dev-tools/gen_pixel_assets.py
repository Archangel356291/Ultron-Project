"""Generates original pixel-art PNG sprites/backdrop for the Ultron tab's
pixel-companion scene (dashboard, Ultron's Corner). Style/palette inspired
by two reference images the owner supplied (a red/gunmetal armored robot
portrait, and a teal-lit isometric sci-fi control room) -- NOT traced or
copied from either, since the character reference is itself modeled on
Marvel's copyrighted Ultron design. This draws an original silhouette
(angular gunmetal armor, glowing red core/joints, a crested head) built
from primitive shapes, matching the reference's palette and general
proportions rather than reproducing its actual artwork. Same principle
this project's own Module 13 already applied to the 3D hero head.

Run to (re)generate everything directly into ../pixel-assets/, which
ultron-backend/app.py serves at /pixel-assets/<file> (same pattern as
/three-pipeline/<file>):
    python dev-tools/gen_pixel_assets.py
"""
from PIL import Image, ImageDraw, ImageFilter
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pixel-assets")
os.makedirs(OUT_DIR, exist_ok=True)

# ---- palette (matches ultron-dashboard.html's own CSS custom properties) ----
BODY_DARK = (27, 29, 32, 255)
BODY_MID = (44, 47, 51, 255)
BODY_LIGHT = (71, 76, 82, 255)
STEEL = (139, 147, 160, 255)
RED_BRIGHT = (255, 59, 59, 255)
RED_CORE = (255, 130, 110, 255)
RED_DIM = (150, 30, 30, 255)
VOID = (8, 9, 10, 255)
PANEL = (15, 17, 19, 255)
PANEL_RAISED = (22, 25, 28, 255)
LINE = (44, 47, 51, 255)
CYAN = (61, 214, 255, 255)
GREEN = (51, 209, 122, 255)


def glow(img, color, blur=3):
    """Soft glow layer: a blurred copy of the opaque shapes, tinted,
    composited behind the original -- cheap way to fake emissive light
    without a real lighting engine."""
    alpha = img.split()[3].filter(ImageFilter.GaussianBlur(blur))
    tint = Image.new("RGBA", img.size, color)
    tint.putalpha(alpha.point(lambda a: int(a * 0.55)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(tint)
    out.alpha_composite(img)
    return out


def draw_ultron(scale, accent, pose):
    """pose: 'walk_a' | 'walk_b' | 'sit'. Bigger/more detailed than the
    old ASCII-grid sprite -- built from layered polygons for an angular
    armored silhouette instead of single-color grid cells."""
    W, H = 20 * scale, 28 * scale
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def px(x, y):
        return (x * scale, y * scale)

    def rect(x0, y0, x1, y1, color):
        d.rectangle([px(x0, y0), px(x1 - 0.01, y1 - 0.01)], fill=color)

    def poly(points, color):
        d.polygon([px(x, y) for x, y in points], fill=color)

    # Crested head -- an original angular silhouette (a peaked crown, a
    # single horizontal red visor band) rather than the reference's
    # actual horn/face design.
    poly([(6, 0), (10, -2), (14, 0), (15, 5), (5, 5)], BODY_MID)
    rect(5, 5, 15, 8, BODY_LIGHT)
    rect(6, 6.2, 14, 7.4, accent)  # visor
    poly([(7.5, 0), (8.5, -5.5), (10, -2.5)], accent)   # left crest spike
    poly([(10, -2.5), (11.5, -6), (12.5, 0)], accent)   # right crest spike, taller

    # Neck + shoulders -- wide, armored.
    rect(8, 8, 12, 9.5, BODY_MID)
    poly([(3, 9.5), (17, 9.5), (16, 13), (4, 13)], BODY_LIGHT)
    rect(4, 13, 16, 14, BODY_MID)

    # Chest core -- the glowing centerpiece, echoing the reference's lit
    # chest panel.
    rect(7.5, 10.5, 12.5, 16, PANEL)
    d.ellipse([px(8.3, 11.3), px(11.7, 14.7)], fill=accent)
    d.ellipse([px(9, 12), px(11, 14)], fill=(255, 255, 255, 230))

    # Torso.
    rect(4, 14, 16, 19, BODY_MID)
    rect(4, 14, 5.5, 19, BODY_DARK)
    rect(14.5, 14, 16, 19, BODY_DARK)
    for gy in (15, 17):
        rect(6, gy, 14, gy + 0.6, accent)  # armor seam glow lines

    if pose == "sit":
        # Bent forward slightly, arms toward a keyboard, legs folded
        # under -- drawn as one wide seated base rather than distinct legs.
        poly([(3, 19), (17, 19), (18, 20), (2, 20)], BODY_LIGHT)
        rect(2, 20, 18, 25, BODY_DARK)
        rect(2, 20, 18, 21, STEEL)
        # one arm forward
        rect(11, 15, 17, 17, BODY_MID)
        rect(15, 15.5, 18, 17.5, BODY_LIGHT)
        d.ellipse([px(16.5, 15.5), px(18.5, 17.5)], fill=accent)
    else:
        # Arms at sides.
        rect(2, 14.5, 4, 19.5, BODY_MID)
        rect(16, 14.5, 18, 19.5, BODY_MID)
        d.ellipse([px(2, 19), px(4, 21)], fill=RED_DIM if accent == RED_BRIGHT else BODY_DARK)
        d.ellipse([px(16, 19), px(18, 21)], fill=RED_DIM if accent == RED_BRIGHT else BODY_DARK)
        # Legs -- walk_a/walk_b alternate stance, clearly separated.
        lead = pose == "walk_b"
        left_x = 5.5 if lead else 6.5
        right_x = 11.5 if lead else 10.5
        rect(left_x, 19, left_x + 2.4, 24, BODY_MID)
        rect(right_x, 19, right_x + 2.4, 24, BODY_LIGHT)
        rect(left_x - 0.5, 24, left_x + 2.9, 25.5, BODY_DARK)
        rect(right_x - 0.5, 24, right_x + 2.9, 25.5, BODY_DARK)

    return glow(img, accent, blur=max(2, scale // 2))


def draw_desk_monitor(scale, w_units, h_units, mon_w, mon_h, accent, active, label_alpha):
    W, H = int(w_units * scale), int((h_units + mon_h + 10) * scale)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    top_desk = H - h_units * scale
    d.rectangle([0, top_desk, W, H], fill=PANEL_RAISED)
    d.rectangle([0, top_desk, W, top_desk + 2 * scale], fill=BODY_LIGHT)
    d.rectangle([0, top_desk, W, H], outline=LINE, width=max(1, scale // 3))
    mx0 = (W - mon_w * scale) / 2
    my0 = top_desk - mon_h * scale - 6 * scale
    d.rectangle([mx0 - scale, my0 + mon_h * scale, mx0 + scale, top_desk], fill=BODY_DARK)  # stand
    screen_color = accent if active else tuple(int(c * 0.35) for c in accent[:3]) + (255,)
    screen = Image.new("RGBA", (int(mon_w * scale), int(mon_h * scale)), screen_color)
    sd = ImageDraw.Draw(screen)
    for ly in range(2, int(mon_h * scale) - 2, max(3, scale)):
        sd.rectangle([2, ly, int(mon_w * scale) - 2, ly + 1], fill=(255, 255, 255, label_alpha))
    img.alpha_composite(glow(screen, screen_color, blur=scale), (int(mx0), int(my0)))
    d.rectangle([mx0 - 1, my0 - 1, mx0 + mon_w * scale + 1, my0 + mon_h * scale + 1], outline=BODY_LIGHT, width=1)
    return img


def draw_tube(scale, w_units, h_units, accent):
    W, H = int(w_units * scale), int(h_units * scale)
    img = Image.new("RGBA", (W, H + 6 * scale // 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cap = max(2, scale // 2)
    d.rectangle([0, cap, W, H + cap], fill=(255, 255, 255, 10))
    fill = Image.new("RGBA", (W - 2, H + cap - 2), accent[:3] + (70,))
    img.alpha_composite(glow(fill, accent, blur=scale), (1, cap + 1))
    for sy in range(cap + 6, H, max(6, H // 5)):
        d.line([(1, sy), (W - 1, sy)], fill=(255, 255, 255, 40), width=1)
    d.rectangle([0, cap, W, H + cap], outline=BODY_LIGHT, width=1)
    d.rectangle([-2, 0, W + 2, cap], fill=LINE)
    d.rectangle([-2, H + cap, W + 2, H + cap * 2], fill=LINE)
    return img


def draw_skyline(w, h):
    img = Image.new("RGBA", (w, h), VOID)
    d = ImageDraw.Draw(img)
    import random
    random.seed(7)
    x = 0
    while x < w:
        bw = random.randint(w // 14, w // 8)
        bh = random.randint(h // 3, h - 6)
        d.rectangle([x, h - bh, x + bw, h], fill=(18, 21, 26, 255))
        for wy in range(h - bh + 4, h - 3, 7):
            for wx in range(x + 3, x + bw - 3, 6):
                if random.random() < 0.35:
                    d.rectangle([wx, wy, wx + 2, wy + 2], fill=RED_BRIGHT)
        x += bw + random.randint(2, 6)
    d.rectangle([0, 0, w - 1, h - 1], outline=LINE, width=2)
    return img


def draw_room_background(w, h, floor_y):
    """Static backdrop: wall, floor, server rack, skyline window, cable
    clutter. Bigger and more detailed than the previous version, per the
    owner's reference (teal-lit control-room mood; kept as a straight-on
    2D scene rather than true isometric -- redoing the whole scene's
    perspective/movement math for an isometric camera was out of scope
    for this pass, flagged rather than silently attempted and half-done)."""
    img = Image.new("RGBA", (w, h), PANEL)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, floor_y], fill=PANEL)
    grid = Image.new("RGBA", (w, floor_y), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for gx in range(0, w, 28):
        gd.line([(gx, 0), (gx, floor_y)], fill=(61, 214, 255, 18))
    for gy in range(0, floor_y, 28):
        gd.line([(0, gy), (w, gy)], fill=(61, 214, 255, 18))
    img.alpha_composite(grid)

    sky_w, sky_h = int(w * 0.24), int(floor_y * 0.55)
    sky = draw_skyline(sky_w, sky_h)
    img.alpha_composite(sky, (int(w * 0.06), int(floor_y * 0.08)))

    d.rectangle([0, floor_y, w, h], fill=VOID)
    for gx in range(0, w, 18):
        d.line([(gx, floor_y), (gx, h)], fill=(20, 22, 25, 255))
    d.line([(0, floor_y), (w, floor_y)], fill=LINE, width=2)

    rack_x, rack_y, rack_w, rack_h = int(w * 0.02), int(floor_y * 0.35), int(w * 0.045), int(floor_y * 0.6)
    d.rectangle([rack_x, rack_y, rack_x + rack_w, rack_y + rack_h], fill=PANEL_RAISED, outline=LINE, width=2)
    lights = [CYAN, GREEN, CYAN, RED_BRIGHT, GREEN]
    for i, c in enumerate(lights):
        ly = rack_y + 10 + i * (rack_h - 20) // len(lights)
        d.rectangle([rack_x + 6, ly, rack_x + 6 + 8, ly + 8], fill=c)

    return img


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print("wrote", path, img.size)


def main():
    SCALE = 6  # character sprite pixel-cell size
    for pose in ("walk_a", "walk_b", "sit"):
        save(draw_ultron(SCALE, RED_BRIGHT, pose), f"ultron_{pose}.png")
    save(draw_ultron(int(SCALE * 0.6), CYAN, "sit"), "agent_cyan_sit.png")
    save(draw_ultron(int(SCALE * 0.6), GREEN, "sit"), "agent_green_sit.png")

    save(draw_desk_monitor(10, 11, 3.6, 4.6, 4.4, RED_BRIGHT, False, 60), "desk_ultron_idle.png")
    save(draw_desk_monitor(10, 11, 3.6, 4.6, 4.4, RED_BRIGHT, True, 90), "desk_ultron_active.png")
    save(draw_desk_monitor(6, 8, 2.4, 3.2, 3.0, CYAN, False, 50), "desk_cyan_idle.png")
    save(draw_desk_monitor(6, 8, 2.4, 3.2, 3.0, CYAN, True, 80), "desk_cyan_active.png")
    save(draw_desk_monitor(6, 8, 2.4, 3.2, 3.0, GREEN, False, 50), "desk_green_idle.png")
    save(draw_desk_monitor(6, 8, 2.4, 3.2, 3.0, GREEN, True, 80), "desk_green_active.png")

    save(draw_tube(10, 3, 14, RED_BRIGHT), "tube_red.png")
    save(draw_tube(6, 2, 9, CYAN), "tube_cyan.png")
    save(draw_tube(6, 2, 9, GREEN), "tube_green.png")

    save(draw_room_background(1280, 560, 440), "room_bg.png")


if __name__ == "__main__":
    main()
