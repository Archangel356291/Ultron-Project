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

Quality pass (2026-09-15): same shapes/proportions/canvas sizes as before
(so ultron-dashboard.html's positioning math -- WALK_MIN_X/MAX_X, desk/tube
X offsets, FLOOR_Y anchoring -- needs zero changes), but every sprite now
gets a crisp dark outline, multi-tone shading instead of flat single-color
fills, and small grounding/material details (contact shadows, rim-lit glass,
a keyboard, panel seams) that a flat-Pillow-rectangle pass skips. Closest
available in-repo style reference is body_design.png/relic_gauge.png
(gen_design_assets.py) -- both already use rim-glow + multi-tone shading;
this brings the room sprites up to that same bar. The owner's own two
source photos referenced above were only ever shared in chat, never saved
to this repo, so they aren't available to re-check against here.

Run to (re)generate everything directly into ../pixel-assets/, which
ultron-backend/app.py serves at /pixel-assets/<file> (same pattern as
/three-pipeline/<file>):
    python dev-tools/gen_pixel_assets.py
"""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os
import random

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
# The two subagents the owner named on 2026-09-16: Sentinel (security
# watchdog) in the dashboard's --amber, Scout (web research) in the violet
# the activity feed already uses for its backup icon -- both colours the
# UI already speaks, not new ones.
AMBER = (255, 194, 75, 255)
VIOLET = (176, 132, 240, 255)
OUTLINE_COLOR = (5, 6, 8, 255)


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


def outline(img, color=OUTLINE_COLOR, size=3):
    """Crisp dark rim around the opaque silhouette -- the single biggest
    lever for making flat Pillow-primitive shapes read as pixel art instead
    of plain rectangles. Dilates the alpha channel and fills the resulting
    ring, so it hugs whatever shape (rect/poly/ellipse) is already there."""
    alpha = img.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(size))
    ring = ImageChops.subtract(dilated, alpha)
    ring_layer = Image.new("RGBA", img.size, color)
    ring_layer.putalpha(ring)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(ring_layer)
    out.alpha_composite(img)
    return out


def shade(color, factor):
    """Lighten (factor>1) or darken (factor<1) an RGBA tuple, clamped."""
    r, g, b = (max(0, min(255, int(c * factor))) for c in color[:3])
    return (r, g, b, color[3] if len(color) > 3 else 255)


def draw_ultron(scale, accent, pose):
    """pose: 'walk_a' | 'walk_b' | 'sit'. Layered polygons for an angular
    armored silhouette, multi-tone shaded (light from upper-left) with a
    dark contact shadow at the feet so the sprite reads as grounded rather
    than pasted-on."""
    W, H = 20 * scale, 28 * scale
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def px(x, y):
        return (x * scale, y * scale)

    def rect(x0, y0, x1, y1, color):
        d.rectangle([px(x0, y0), px(x1 - 0.01, y1 - 0.01)], fill=color)

    def poly(points, color):
        d.polygon([px(x, y) for x, y in points], fill=color)

    def hline(x0, x1, y, color, w=0.5):
        rect(x0, y, x1, y + w, color)

    # Crested head, pushed much closer to the owner's pixel-Ultron
    # reference's proportions/palette placement (full glowing red faceplate
    # with dark eye cutouts and a mouth grille, a fuller jagged crown) while
    # still an independently-drawn silhouette, not a traced copy.
    poly([(5.5, 5.5), (5.8, 2.2), (7, -1), (10, -2.3), (13, -1), (14.2, 2.2), (14.5, 5.5)], BODY_MID)
    poly([(5.5, 5.5), (5.8, 2.2), (7, -1), (10, -2.3), (10, 5.5)], shade(BODY_MID, 1.25))  # left-face highlight
    rect(5.5, 5.5, 14.5, 8.4, BODY_LIGHT)
    # Full glowing faceplate (not just a brow band) -- covers eyes through
    # jaw, per the reference's mostly-red lit face.
    poly([(6.0, 5.9), (14.0, 5.9), (13.6, 8.2), (6.4, 8.2)], accent)
    poly([(6.0, 5.9), (14.0, 5.9), (13.7, 6.5), (6.3, 6.5)], shade(accent, 1.3))  # top-edge highlight
    poly([(6.4, 8.2), (13.6, 8.2), (13.3, 8.6), (6.7, 8.6)], shade(accent, 0.55))  # jaw undershade
    # Dark almond eye cutouts within the glow (negative space, not glowing
    # dots) -- the reference's eyes read as dark slits inside the red mask.
    for ex in (8.1, 11.9):
        d.ellipse([px(ex - 1.15, 6.25), px(ex + 1.15, 7.35)], fill=(8, 6, 6, 255))
        d.ellipse([px(ex - 0.7, 6.5), px(ex + 0.7, 7.1)], fill=shade(accent, 0.7))  # faint inner glow rim
    # Mouth grille -- vertical dark slats across the lower faceplate.
    for gx in (7.3, 8.5, 9.7, 10.9, 12.1):
        rect(gx, 7.6, gx + 0.5, 8.5, (8, 6, 6, 255))
    # Fuller jagged crown -- five uneven spikes instead of a smooth
    # three-point ridge, matching the reference's spikier crest silhouette.
    # y=0 is the actual canvas top at this scale (negative y clips flat,
    # confirmed by render) -- tips kept just above 0 so the points stay
    # sharp instead of getting cut into a flat bar.
    tips = ((6.3, 0.7), (7.9, 0.25), (10.0, 0.05), (12.1, 0.25), (13.7, 0.7))
    bases = (6.0, 7.1, 8.5, 11.5, 12.9, 14.0)
    for i in range(5):
        poly([(bases[i], 1.4), tips[i], (bases[i + 1], 1.4)], accent)
        poly([(bases[i], 1.4), tips[i], ((bases[i] + tips[i][0]) / 2, 0.2)], shade(accent, 1.3))

    # Neck + shoulders -- wide, armored.
    rect(8, 8, 12, 9.5, BODY_MID)
    poly([(3, 9.5), (17, 9.5), (16, 13), (4, 13)], BODY_LIGHT)
    poly([(3, 9.5), (10, 9.5), (9, 13), (4, 13)], shade(BODY_LIGHT, 1.2))
    rect(4, 13, 16, 14, BODY_MID)
    # shoulder rivets, echoing body_design.png's joint accents
    d.ellipse([px(4.3, 10.3), px(5.5, 11.5)], fill=shade(accent, 0.85))
    d.ellipse([px(14.5, 10.3), px(15.7, 11.5)], fill=shade(accent, 0.85))

    # Chest core -- the glowing centerpiece, echoing the reference's lit
    # chest panel.
    rect(7.5, 10.5, 12.5, 16, PANEL)
    rect(7.5, 10.5, 9, 16, shade(PANEL, 1.4))  # left panel bevel
    d.ellipse([px(8.3, 11.3), px(11.7, 14.7)], fill=accent)
    d.ellipse([px(8.6, 11.6), px(11.4, 14.4)], outline=shade(accent, 0.5), width=1)
    d.ellipse([px(9, 12), px(11, 14)], fill=(255, 255, 255, 230))

    # Torso.
    rect(4, 14, 16, 19, BODY_MID)
    rect(4, 14, 5.5, 19, BODY_DARK)
    rect(14.5, 14, 16, 19, BODY_DARK)
    rect(5.5, 14, 8, 14.6, shade(BODY_MID, 1.18))  # top-edge highlight catch-light
    for gy in (15, 17):
        rect(6, gy, 14, gy + 0.6, accent)  # armor seam glow lines
        rect(6, gy + 0.6, 14, gy + 0.8, shade(accent, 0.4))

    if pose == "sit":
        # Bent forward slightly, arms toward a keyboard, legs folded
        # under -- drawn as one wide seated base rather than distinct legs.
        poly([(3, 19), (17, 19), (18, 20), (2, 20)], BODY_LIGHT)
        rect(2, 20, 18, 25, BODY_DARK)
        rect(2, 20, 18, 21, STEEL)
        rect(2, 20, 10, 20.8, shade(STEEL, 1.15))
        # one arm forward
        rect(11, 15, 17, 17, BODY_MID)
        rect(15, 15.5, 18, 17.5, BODY_LIGHT)
        d.ellipse([px(16.5, 15.5), px(18.5, 17.5)], fill=accent)
        d.ellipse([px(16.9, 15.9), px(18.1, 17.1)], fill=shade(accent, 1.3))
        # contact shadow (feet bottom at y=25, canvas is 28 tall -- room below)
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.ellipse([px(3, 25.6), px(17, 27.3)], fill=(0, 0, 0, 130))
        shadow = shadow.filter(ImageFilter.GaussianBlur(scale * 0.4))
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        base.alpha_composite(shadow)
        base.alpha_composite(img)
        img = base
    else:
        # Arms at sides.
        rect(2, 14.5, 4, 19.5, BODY_MID)
        rect(16, 14.5, 18, 19.5, BODY_MID)
        rect(2, 14.5, 2.8, 19.5, shade(BODY_MID, 1.2))
        rect(16, 14.5, 16.8, 19.5, shade(BODY_MID, 1.2))
        d.ellipse([px(2, 19), px(4, 21)], fill=RED_DIM if accent == RED_BRIGHT else BODY_DARK)
        d.ellipse([px(16, 19), px(18, 21)], fill=RED_DIM if accent == RED_BRIGHT else BODY_DARK)
        # Legs -- walk_a/walk_b alternate stance, clearly separated.
        lead = pose == "walk_b"
        left_x = 5.5 if lead else 6.5
        right_x = 11.5 if lead else 10.5
        rect(left_x, 19, left_x + 2.4, 24, BODY_MID)
        rect(right_x, 19, right_x + 2.4, 24, BODY_LIGHT)
        rect(left_x, 19, left_x + 0.7, 24, shade(BODY_MID, 1.25))
        rect(right_x, 19, right_x + 0.7, 24, shade(BODY_LIGHT, 1.2))
        rect(left_x - 0.5, 24, left_x + 2.9, 25.5, BODY_DARK)
        rect(right_x - 0.5, 24, right_x + 2.9, 25.5, BODY_DARK)
        # contact shadow, both feet -- shifts slightly with stride for a
        # believable ground-plane read as the character walks.
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        cx = (left_x + right_x) / 2 + 1.2
        sd.ellipse([px(cx - 6, 25.7), px(cx + 6, 27.2)], fill=(0, 0, 0, 120))
        shadow = shadow.filter(ImageFilter.GaussianBlur(scale * 0.4))
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        base.alpha_composite(shadow)
        base.alpha_composite(img)
        img = base

    return glow(outline(img, size=max(3, scale // 2 * 2 + 1)), accent, blur=max(2, scale // 2))


def draw_desk_monitor(scale, w_units, h_units, mon_w, mon_h, accent, active, label_alpha):
    W, H = int(w_units * scale), int((h_units + mon_h + 10) * scale)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    top_desk = H - h_units * scale

    # Desk body with a lit top edge (catches the monitor glow) and a
    # darker recessed front kick-panel instead of one flat slab.
    d.rectangle([0, top_desk, W, H], fill=PANEL_RAISED)
    d.rectangle([0, top_desk, W, top_desk + 2 * scale], fill=BODY_LIGHT)
    d.rectangle([0, top_desk + 2 * scale, W, top_desk + 2.4 * scale], fill=shade(BODY_LIGHT, 0.6))
    kick_y0 = top_desk + (h_units * scale) * 0.55
    d.rectangle([scale * 0.6, kick_y0, W - scale * 0.6, H - scale * 0.4], fill=shade(PANEL_RAISED, 0.7))

    mx0 = (W - mon_w * scale) / 2
    my0 = top_desk - mon_h * scale - 6 * scale

    # Monitor stand + a cable running down into the desk (small material
    # detail that a bare stand-rectangle skips).
    d.rectangle([mx0 - scale, my0 + mon_h * scale, mx0 + scale, top_desk], fill=BODY_DARK)
    d.line([mx0 + scale * 1.5, top_desk, mx0 + scale * 1.5, top_desk + h_units * scale * 0.4],
           fill=shade(BODY_DARK, 1.6), width=max(1, scale // 5))

    # Screen: bezel, glow, scanlines, and (only above a small size, so the
    # tiny subagent screens don't get illegibly cramped detail) a couple of
    # corner accent rivets.
    screen_color = accent if active else tuple(int(c * 0.35) for c in accent[:3]) + (255,)
    screen = Image.new("RGBA", (int(mon_w * scale), int(mon_h * scale)), screen_color)
    sd = ImageDraw.Draw(screen)
    for ly in range(2, int(mon_h * scale) - 2, max(3, scale)):
        sd.rectangle([2, ly, int(mon_w * scale) - 2, ly + 1], fill=(255, 255, 255, label_alpha))
    sd.rectangle([0, 0, int(mon_w * scale) - 1, int(mon_h * scale) * 0.35], fill=(255, 255, 255, 22))
    img.alpha_composite(glow(screen, screen_color, blur=scale), (int(mx0), int(my0)))
    d.rectangle([mx0 - 1, my0 - 1, mx0 + mon_w * scale + 1, my0 + mon_h * scale + 1], outline=BODY_LIGHT, width=1)
    if mon_w >= 4:
        for cx, cy in ((mx0 + 2, my0 + 2), (mx0 + mon_w * scale - 2, my0 + 2)):
            d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=STEEL)

    # Keyboard tray + a small status LED, sitting on the desk in front of
    # the stand -- the detail that most reads as "a desk" vs. "a box."
    kb_w, kb_h = mon_w * scale * 0.8, max(2, scale * 0.5)
    kb_x, kb_y = mx0 + (mon_w * scale - kb_w) / 2, top_desk - kb_h - scale * 0.15
    d.rectangle([kb_x, kb_y, kb_x + kb_w, kb_y + kb_h], fill=shade(BODY_LIGHT, 0.85), outline=BODY_DARK)
    for kx in range(int(kb_x + 2), int(kb_x + kb_w - 2), max(2, int(scale * 0.28))):
        d.rectangle([kx, kb_y + 1, kx + 1, kb_y + kb_h - 1], fill=shade(BODY_LIGHT, 0.55))
    led_color = accent if active else shade(accent, 0.4)
    d.ellipse([W - scale * 1.1, top_desk + scale * 0.3, W - scale * 0.5, top_desk + scale * 0.9], fill=led_color)

    return glow(outline(img, size=3), accent, blur=1) if active else outline(img, size=3)


def draw_tube(scale, w_units, h_units, accent):
    W, H = int(w_units * scale), int(h_units * scale)
    cap = max(2, scale // 2)
    total_h = H + cap * 2
    img = Image.new("RGBA", (W + 4, total_h + int(scale * 0.8)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ox = 2  # small horizontal margin so the outline pass has room to breathe

    # Glass cylinder: rim highlight ellipses top/bottom instead of a flat
    # rectangle, so it reads as round glass rather than a painted strip.
    d.rectangle([ox, cap, ox + W, cap + H], fill=(255, 255, 255, 6))
    fill = Image.new("RGBA", (W - 2, H - 2), accent[:3] + (150,))
    img.alpha_composite(glow(fill, accent, blur=max(2, scale // 3)), (ox + 1, cap + 1))
    core = Image.new("RGBA", (max(1, int((W - 2) * 0.4)), H - 2), shade(accent, 1.15)[:3] + (120,))
    img.alpha_composite(core, (int(ox + 1 + (W - 2) * 0.3), cap + 1))

    random.seed(int(accent[0]) + int(w_units * 10))
    for _ in range(max(3, int(h_units / 3))):
        bx = ox + random.uniform(2, W - 4)
        by = cap + random.uniform(4, H - 4)
        br = random.uniform(1, 2.2)
        d.ellipse([bx, by, bx + br, by + br * 1.4], fill=(255, 255, 255, random.randint(40, 90)))
    for sy in range(cap + 6, H, max(6, H // 5)):
        d.line([(ox + 1, sy), (ox + W - 1, sy)], fill=(255, 255, 255, 40), width=1)

    d.ellipse([ox, cap - cap * 0.6, ox + W, cap + cap * 0.6], fill=(255, 255, 255, 60))
    d.ellipse([ox, cap + H - cap * 0.6, ox + W, cap + H + cap * 0.6], fill=(0, 0, 0, 70))
    d.rectangle([ox, cap, ox + W, cap + H], outline=BODY_LIGHT, width=1)

    # Cap (with vent lines) and plinth (with bolts), replacing the plain
    # end-cap rectangles.
    d.rectangle([ox - 2, 0, ox + W + 2, cap], fill=LINE)
    for vx in range(int(ox), int(ox + W), max(3, int(scale * 0.3))):
        d.line([(vx, 1), (vx, cap - 1)], fill=shade(LINE, 0.5), width=1)
    plinth_h = int(scale * 0.7)
    d.rectangle([ox - 4, cap + H, ox + W + 4, cap + H + plinth_h], fill=shade(LINE, 1.3))
    d.rectangle([ox - 4, cap + H + plinth_h, ox + W + 4, cap + H + plinth_h + int(scale * 0.35)], fill=LINE)
    for bx in (ox - 2, ox + W + 2):
        d.ellipse([bx - 1, cap + H + 2, bx + 1, cap + H + 4], fill=STEEL)

    return outline(img, size=3)


def draw_skyline(w, h):
    img = Image.new("RGBA", (w, h), VOID)
    d = ImageDraw.Draw(img)
    random.seed(7)
    x = 0
    while x < w:
        bw = random.randint(w // 14, w // 8)
        bh = random.randint(h // 3, h - 6)
        building = shade((18, 21, 26, 255), random.uniform(0.85, 1.25))
        d.rectangle([x, h - bh, x + bw, h], fill=building)
        d.line([(x, h - bh), (x + bw, h - bh)], fill=shade(building, 1.6), width=1)
        win_color = CYAN if random.random() < 0.25 else RED_BRIGHT
        for wy in range(h - bh + 4, h - 3, 7):
            for wx in range(x + 3, x + bw - 3, 6):
                if random.random() < 0.35:
                    d.rectangle([wx, wy, wx + 2, wy + 2], fill=win_color)
        x += bw + random.randint(2, 6)
    # a lone blinking antenna light on the tallest silhouette for a touch of life
    d.ellipse([w * 0.42, 0, w * 0.42 + 3, 3], fill=(255, 255, 255, 200))
    d.rectangle([0, 0, w - 1, h - 1], outline=LINE, width=2)
    return img


def draw_console_panel(d, img, x, y, w, h, seed):
    """A wall-mounted control console -- small screen, a button grid, and
    a couple of slider readouts -- per the owner's workstation-room
    reference (dense wall consoles are most of what makes that room read
    as lived-in rather than an empty box). Cheap: a handful of rects per
    panel, no per-frame cost since this bakes into the static backdrop."""
    random.seed(seed)
    d.rectangle([x, y, x + w, y + h], fill=PANEL_RAISED, outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 2], fill=shade(PANEL_RAISED, 1.5))

    screen_w, screen_h = w * 0.85, h * 0.4
    screen_x, screen_y = x + (w - screen_w) / 2, y + h * 0.08
    screen = Image.new("RGBA", (int(screen_w), int(screen_h)), (30, 60, 70, 255))
    sd = ImageDraw.Draw(screen)
    for ly in range(1, int(screen_h) - 1, 3):
        sd.line([(1, ly), (int(screen_w) - 1, ly)], fill=CYAN[:3] + (random.randint(60, 140),), width=1)
    img.alpha_composite(glow(screen, CYAN, blur=2), (int(screen_x), int(screen_y)))
    d.rectangle([screen_x, screen_y, screen_x + screen_w, screen_y + screen_h], outline=shade(LINE, 1.6), width=1)

    btn_y = screen_y + screen_h + h * 0.12
    btn_colors = [CYAN, GREEN, RED_BRIGHT, CYAN, GREEN, CYAN]
    bw = w * 0.1
    for i, c in enumerate(btn_colors):
        bx = x + w * 0.08 + i * (bw + w * 0.03)
        if bx + bw > x + w * 0.95:
            break
        lit = random.random() < 0.7
        d.rectangle([bx, btn_y, bx + bw, btn_y + bw], fill=c if lit else shade(c, 0.35))

    slider_y = btn_y + bw + h * 0.1
    for i in range(2):
        sy = slider_y + i * h * 0.1
        d.line([(x + w * 0.08, sy), (x + w * 0.92, sy)], fill=shade(LINE, 1.5), width=1)
        knob_x = x + w * (0.15 + random.uniform(0, 0.7))
        d.ellipse([knob_x - 2, sy - 2, knob_x + 2, sy + 2], fill=CYAN)


def draw_room_background(w, h, floor_y):
    """Static backdrop: wall, floor, server rack, skyline window, cable
    clutter. Per the owner's reference (teal-lit control-room mood; kept
    as a straight-on 2D scene rather than true isometric -- redoing the
    whole scene's perspective/movement math for an isometric camera was
    out of scope for this pass, flagged rather than silently attempted
    and half-done). This pass adds wall paneling, a ceiling light strip,
    a floor reflection gradient, a wall conduit, and a vignette on top of
    the previous flat grid, for a lit-room feel instead of a lit-grid feel."""
    img = Image.new("RGBA", (w, h), PANEL)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, floor_y], fill=PANEL)

    # Wall paneling: vertical seams with a highlight/shadow pair, reading
    # as material rather than a bare flat-colored plane.
    for px_ in range(0, w, 64):
        d.line([(px_, 0), (px_, floor_y)], fill=shade(PANEL, 1.4), width=1)
        d.line([(px_ + 1, 0), (px_ + 1, floor_y)], fill=shade(PANEL, 0.7), width=1)

    # Ceiling light strip: a bright core line with a soft glow gradient
    # falling down the wall beneath it.
    strip_y = int(floor_y * 0.03)
    ceiling_glow = Image.new("RGBA", (w, int(floor_y * 0.22)), (0, 0, 0, 0))
    cg = ImageDraw.Draw(ceiling_glow)
    cg.rectangle([0, 0, w, 2], fill=(210, 240, 255, 230))
    ceiling_glow = ceiling_glow.filter(ImageFilter.GaussianBlur(6))
    img.alpha_composite(ceiling_glow, (0, strip_y))
    d.rectangle([0, strip_y, w, strip_y + 2], fill=(230, 250, 255, 255))

    grid = Image.new("RGBA", (w, floor_y), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for gx in range(0, w, 28):
        gd.line([(gx, 0), (gx, floor_y)], fill=(61, 214, 255, 12))
    for gy in range(0, floor_y, 28):
        gd.line([(0, gy), (w, gy)], fill=(61, 214, 255, 12))
    img.alpha_composite(grid)

    # Wall conduit: a horizontal pipe run with hangers, midway up the wall,
    # for the kind of mechanical clutter a real server room actually has.
    pipe_y = int(floor_y * 0.62)
    d.rectangle([0, pipe_y, w, pipe_y + 6], fill=shade(LINE, 1.3))
    d.line([(0, pipe_y), (w, pipe_y)], fill=shade(LINE, 1.8), width=1)
    for hx in range(20, w, 90):
        d.rectangle([hx, pipe_y - 3, hx + 4, pipe_y + 9], fill=LINE)

    sky_w, sky_h = int(w * 0.24), int(floor_y * 0.55)
    sky = draw_skyline(sky_w, sky_h)
    img.alpha_composite(sky, (int(w * 0.06), int(floor_y * 0.08)))

    # Wall consoles across the whole back wall (not just one cluster) --
    # quality pass per the owner's second workstation-room reference,
    # whose room reads as densely instrumented floor-to-ceiling on every
    # wall segment, not just near the window. Live desks/tubes still get
    # drawn on top each frame further right (see SUBAGENTS/ULTRON_DESK_X
    # in the dashboard's own pixel-room script); these are just the static
    # backdrop filling what would otherwise be bare wall between/behind them.
    draw_console_panel(d, img, int(w * 0.34), int(floor_y * 0.18), int(w * 0.09), int(floor_y * 0.5), seed=11)
    draw_console_panel(d, img, int(w * 0.46), int(floor_y * 0.22), int(w * 0.07), int(floor_y * 0.42), seed=23)
    for i, wx in enumerate((0.58, 0.68, 0.78, 0.88)):
        draw_console_panel(d, img, int(w * wx), int(floor_y * (0.16 + 0.05 * (i % 2))),
                            int(w * 0.055), int(floor_y * (0.4 - 0.04 * (i % 2))), seed=31 + i * 7)

    # Floor: reflection gradient (brighter near the wall, fading to void)
    # under the existing tile grid, plus the tile seams themselves.
    floor_grad = Image.new("L", (1, h - floor_y), 0)
    for gy in range(h - floor_y):
        t = gy / max(1, h - floor_y - 1)
        floor_grad.putpixel((0, gy), int(38 * (1 - t)))
    floor_grad = floor_grad.resize((w, h - floor_y))
    floor_tint = Image.new("RGBA", (w, h - floor_y), (61, 214, 255, 255))
    floor_tint.putalpha(floor_grad)
    d.rectangle([0, floor_y, w, h], fill=VOID)
    img.alpha_composite(floor_tint, (0, floor_y))
    for gx in range(0, w, 18):
        d.line([(gx, floor_y), (gx, h)], fill=(20, 22, 25, 255))
    # Catwalk grating: short cross-hatch ticks between the tile seams, per
    # the reference's metal-grate floor -- cheap (one short line per
    # cell), baked into the static backdrop so it costs nothing per frame.
    for gy in range(floor_y + 6, h, 10):
        for gx in range(0, w, 18):
            d.line([(gx + 3, gy), (gx + 15, gy)], fill=(30, 33, 37, 200), width=1)
    d.line([(0, floor_y), (w, floor_y)], fill=LINE, width=2)

    rack_x, rack_y, rack_w, rack_h = int(w * 0.02), int(floor_y * 0.35), int(w * 0.045), int(floor_y * 0.6)
    d.rectangle([rack_x, rack_y, rack_x + rack_w, rack_y + rack_h], fill=PANEL_RAISED, outline=LINE, width=2)
    d.rectangle([rack_x, rack_y, rack_x + rack_w, rack_y + int(rack_h * 0.04)], fill=shade(PANEL_RAISED, 1.5))
    lights = [CYAN, GREEN, CYAN, RED_BRIGHT, GREEN]
    for i, c in enumerate(lights):
        ly = rack_y + 10 + i * (rack_h - 20) // len(lights)
        d.rectangle([rack_x + 6, ly, rack_x + 6 + 8, ly + 8], fill=c)
        d.rectangle([rack_x + 6, ly, rack_x + 6 + 8, ly + 2], fill=(255, 255, 255, 90))

    # Ambient teal wash across the whole wall -- the owner's reference room
    # reads as bathed in teal light throughout, not just near individual
    # screens; a flat low-alpha tint over the wall area is the cheap way to
    # push the room's overall cast without re-tinting every element above.
    ambient = Image.new("RGBA", (w, floor_y), (61, 214, 255, 20))
    img.alpha_composite(ambient)

    # Vignette: darken the corners a touch so the room reads as lit from
    # the ceiling strip/tubes rather than uniformly flat-lit -- lighter
    # than before so the newly-added consoles across the back wall stay
    # visible instead of falling into the darkened edges.
    vignette = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse([-w * 0.25, -h * 0.4, w * 1.25, h * 1.25], fill=60)
    vignette = vignette.filter(ImageFilter.GaussianBlur(70))
    dark = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    dark.putalpha(ImageChops.invert(vignette))
    img.alpha_composite(dark)

    return img


def draw_app_icon(size, maskable=False):
    """Installable-app icon: the dashboard header's own mark (a hexagon
    outline in the site's oxide orange with a gold core pulse), drawn large
    on the void background. Original geometry, no source image. `maskable`
    keeps everything inside Android's safe zone (the centre 80%) so nothing
    is clipped when the launcher masks it to a circle or squircle."""
    s = size
    img = Image.new("RGBA", (s, s), (10, 11, 13, 255))
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = cy = s / 2
    r = s * (0.30 if maskable else 0.40)
    oxide = (255, 138, 30, 255)
    gold = (255, 178, 56, 255)
    import math
    hexagon = [(cx + r * math.cos(math.radians(90 + 60 * i)), cy - r * math.sin(math.radians(90 + 60 * i))) for i in range(6)]
    d.polygon(hexagon, outline=oxide, width=max(2, s // 24))
    inner = r * 0.62
    d.ellipse([cx - inner, cy - inner, cx + inner, cy + inner], outline=(255, 178, 56, 110), width=max(1, s // 64))
    core = r * 0.30
    core_layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(core_layer).ellipse([cx - core, cy - core, cx + core, cy + core], fill=gold)
    img.alpha_composite(glow(core_layer, gold, blur=max(4, s // 16)))
    img.alpha_composite(layer)
    ImageDraw.Draw(img).ellipse([cx - core * 0.45, cy - core * 0.45, cx + core * 0.45, cy + core * 0.45], fill=(255, 233, 194, 255))
    return img


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print("wrote", path, img.size)


def main():
    SCALE = 6  # character sprite pixel-cell size
    for pose in ("walk_a", "walk_b", "sit"):
        save(draw_ultron(SCALE, RED_BRIGHT, pose), f"ultron_{pose}.png")
    save(draw_desk_monitor(10, 11, 3.6, 4.6, 4.4, RED_BRIGHT, False, 60), "desk_ultron_idle.png")
    save(draw_desk_monitor(10, 11, 3.6, 4.6, 4.4, RED_BRIGHT, True, 90), "desk_ultron_active.png")
    save(draw_tube(10, 3, 14, RED_BRIGHT), "tube_red.png")

    # One sprite/desk/tube set per subagent, all from the same drawing code
    # so the four read as one team in four colours.
    for name, color in (("cyan", CYAN), ("green", GREEN), ("amber", AMBER), ("violet", VIOLET)):
        save(draw_ultron(int(SCALE * 0.6), color, "sit"), f"agent_{name}_sit.png")
        save(draw_desk_monitor(6, 8, 2.4, 3.2, 3.0, color, False, 50), f"desk_{name}_idle.png")
        save(draw_desk_monitor(6, 8, 2.4, 3.2, 3.0, color, True, 80), f"desk_{name}_active.png")
        save(draw_tube(6, 2, 9, color), f"tube_{name}.png")

    save(draw_room_background(1280, 560, 440), "room_bg.png")

    # Installable-app icons, referenced by /manifest.webmanifest in app.py.
    save(draw_app_icon(192), "app-icon-192.png")
    save(draw_app_icon(512), "app-icon-512.png")
    save(draw_app_icon(512, maskable=True), "app-icon-maskable-512.png")


if __name__ == "__main__":
    main()
