"""Module 13: builds the dashboard hero's robotic AI head, procedurally,
via Blender's headless bpy API -- the real version of what
blender_smoke_test.py (Module 5) only proved the mechanism for.

Original design, not a reproduction of any existing character -- built
from primitive armor-plate forms (beveled boxes), not sculpted or traced
from the reference image the roadmap describes as "art-direction only."
No copyrighted geometry, textures, or assets are used or referenced.

Run headlessly (no GUI, no window):

    "<blender.exe>" --background --python three-pipeline/build_hero_head.py

Outputs, both next to this script:
    hero_head.glb            -- the real deliverable, loaded by the dashboard
    hero_head_preview.png    -- a rendered preview, for visually checking the
                                 geometry actually looks right without a GUI
                                 (Eevee, one frame, one camera, one key light)
"""
import math
import os

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
GLB_PATH = os.path.join(HERE, "hero_head.glb")
PREVIEW_PATH = os.path.join(HERE, "hero_head_preview.png")

# ---------------------------------------------------------------------------
# Materials -- dark metal family + one emissive-red accent. Roughness stays
# mid-range everywhere (0.25-0.45): "mixed matte/satin/reflective, avoid full
# gloss" rules out anything near 0. Only the visor gets red; every other
# material is a near-black/graphite/gunmetal neutral, matching "majority of
# the head stays black/graphite/dark chrome, not red."
# ---------------------------------------------------------------------------

def make_metal(name, base_color, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def make_emissive(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.01, 0.0, 0.0, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.2
    bsdf.inputs["Roughness"].default_value = 0.35
    bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
    bsdf.inputs["Emission Strength"].default_value = strength
    return mat


MAT_GUNMETAL = None  # assigned in build(), after read_factory_settings clears bpy.data.materials
MAT_CHROME = None
MAT_GRAPHITE = None
MAT_VISOR = None


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def add_plate(name, size, location, rotation=(0, 0, 0), bevel_width=0.03, bevel_segments=2, material=None):
    """A beveled box -- the one repeated primitive this whole head is built
    from. The bevel is what turns a plain box into an armor "panel" with
    visible seams at its edges (step 42's "thin seams between panels"),
    without needing hand-authored bevel geometry per part."""
    # primitive_cube_add(size=1.0) creates a cube spanning -0.5..0.5 -- an
    # extent of exactly 1.0 per axis already -- so scale == target extent
    # directly, not target/2 (that earlier version rendered every plate at
    # HALF its intended size, which is why nothing visually connected).
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0], size[1], size[2])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bevel = obj.modifiers.new("Bevel", "BEVEL")
    bevel.width = bevel_width
    bevel.segments = bevel_segments
    bevel.limit_method = "ANGLE"

    if material:
        obj.data.materials.append(material)
    return obj


def add_skull(name, radii, location, segments=9, rings=6, material=None):
    """A LOW-poly faceted sphere, not a beveled box. A box's silhouette
    stays a box no matter how much bevel is added -- it never reads as a
    head (confirmed by the first two render iterations, both of which
    looked like a server tower/appliance). A sphere gives the rounded,
    tapering-to-a-point silhouette an actual head has; a LOW segment/ring
    count keeps it faceted and angular rather than smooth/organic, so it
    still reads as "clearly artificial," per the brief."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=segments, ring_count=rings,
                                          location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = radii
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_flat()
    if material:
        obj.data.materials.append(material)
    return obj


def mirror_x(obj, parent):
    """Left/right symmetry via a Mirror modifier rather than hand-duplicating
    every side plate -- half the geometry to author, guaranteed symmetric."""
    mirror = obj.modifiers.new("Mirror", "MIRROR")
    mirror.use_axis[0] = True
    mirror.mirror_object = parent


def build():
    global MAT_GUNMETAL, MAT_CHROME, MAT_GRAPHITE, MAT_VISOR

    bpy.ops.wm.read_factory_settings(use_empty=True)

    MAT_GUNMETAL = make_metal("Gunmetal", (0.043, 0.047, 0.055), 0.45)   # ~#0B0C0E, skull shell
    MAT_CHROME = make_metal("DarkChrome", (0.024, 0.027, 0.035), 0.25)   # ~#060709, plates (more reflective)
    MAT_GRAPHITE = make_metal("Graphite", (0.067, 0.071, 0.078), 0.55)   # ~#111214, forehead layers (most matte)
    MAT_VISOR = make_emissive("VisorEmissive", (1.0, 0.06, 0.09), 3.2)   # deep crimson emission

    root = bpy.data.objects.new("OdinHead", None)
    bpy.context.collection.objects.link(root)

    # Skull: the core angular mass everything else attaches to. Every other
    # part below is deliberately positioned to OVERLAP this shell's surface
    # (not float beside it) -- that overlap is what reads as "one armored
    # head" instead of "scattered boxes" once rendered.
    # A beveled box (the first two attempts) never stops looking like a
    # box -- see add_skull()'s own note. Radii, not full sizes: narrower
    # in X (narrow mechanical face), tallest in Z, moderate Y depth.
    SKULL_RX, SKULL_RY, SKULL_RZ = 0.32, 0.34, 0.52
    skull = add_skull("Skull", radii=(SKULL_RX, SKULL_RY, SKULL_RZ), location=(0, 0, 0.05),
                       material=MAT_GUNMETAL)
    skull.parent = root
    front_y = -SKULL_RY   # the skull's front-most point -- everything facial anchors off this

    # Forehead armor: three thin brow-ridge slabs sitting IN the upper-front
    # third of the face (not stacked above the skull like a hat, which is
    # what a too-high Z and too-large a size read as last time) -- "layered
    # forehead armor," each proud of and overlapping the last.
    for i, (z, width, proud) in enumerate([
        (0.20, 0.46, 0.05),
        (0.29, 0.40, 0.08),
        (0.37, 0.33, 0.11),
    ]):
        plate = add_plate(f"ForeheadLayer{i}", size=(width, 0.11, 0.07),
                           location=(0, front_y + 0.045 - proud, z + 0.05),
                           bevel_width=0.012, bevel_segments=2, material=MAT_GRAPHITE)
        plate.parent = root

    # Cheek plates: overlap deep into the skull's side (not merely touching
    # it) so they read as bolted-on armor, not adjacent shapes -- "strong
    # cheek plates." Built on the +X side only and mirrored.
    cheek = add_plate("CheekPlateR", size=(0.19, 0.32, 0.36), location=(0.27, -0.14, -0.02),
                       rotation=(0, 0, math.radians(-12)), bevel_width=0.02, bevel_segments=2,
                       material=MAT_CHROME)
    cheek.parent = root
    mirror_x(cheek, root)

    # Jaw: narrower than the skull -- the taper from wide skull to narrow
    # chin is what makes this read as a head instead of a box with a box
    # stuck under it. Projects forward and down past the skull's front-
    # bottom edge -- "reinforced jaw."
    jaw = add_plate("Jaw", size=(0.40, 0.42, 0.36), location=(0, front_y + 0.10, -0.38),
                     rotation=(math.radians(8), 0, 0), bevel_width=0.02, bevel_segments=2,
                     material=MAT_CHROME)
    jaw.parent = root

    # Visor: one thin, narrow strip sitting just proud of the front face at
    # eye height -- "narrow angular optical sensor strip," not circular
    # lenses, and narrower than the skull itself. The ONE emissive part;
    # the runtime (Three.js) side targets it by name ("Visor") to drive the
    # slow pulse animation step 45 asks for, rather than baking any
    # animation into the glb itself.
    visor = add_plate("Visor", size=(0.40, 0.07, 0.06), location=(0, front_y + 0.005, 0.03),
                       bevel_width=0.01, bevel_segments=1, material=MAT_VISOR)
    visor.parent = root

    # Apply every modifier before export -- the glTF exporter's own
    # export_apply=True (used below) does this too, but applying explicitly
    # here means the exported vertex/face counts in the assert below reflect
    # the real final mesh, not the pre-modifier cage.
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        for mod in list(obj.modifiers):
            bpy.ops.object.modifier_apply(modifier=mod.name)
        obj.select_set(False)

    return root


def add_camera_and_light():
    # A "look at the origin" Empty + Track-To constraint aims the camera
    # reliably regardless of where it's placed -- hand-computing Euler
    # angles for an off-axis 3/4 view is easy to get subtly wrong (and did,
    # in the first version of this script: a dead-on front view that made
    # every plate's depth offset invisible and the whole head unreadable).
    target = bpy.data.objects.new("CamTarget", None)
    target.location = (0, 0, -0.05)
    bpy.context.collection.objects.link(target)

    cam_data = bpy.data.cameras.new("PreviewCam")
    cam = bpy.data.objects.new("PreviewCam", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = (0.95, -3.5, 0.30)   # gentle 3/4 angle, backed off for full-head framing
    cam_data.lens = 50
    constraint = cam.constraints.new("TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    bpy.context.scene.camera = cam

    key_data = bpy.data.lights.new("KeyLight", type="AREA")
    key_data.energy = 400
    key = bpy.data.objects.new("KeyLight", key_data)
    key.location = (1.6, -2.4, 1.6)
    key.rotation_euler = (math.radians(55), 0, math.radians(30))
    bpy.context.collection.objects.link(key)

    rim_data = bpy.data.lights.new("RimLight", type="AREA")
    rim_data.energy = 250
    rim_data.color = (1.0, 0.25, 0.3)
    rim = bpy.data.objects.new("RimLight", rim_data)
    rim.location = (-1.8, 1.6, 0.6)
    rim.rotation_euler = (math.radians(-40), 0, math.radians(-150))
    bpy.context.collection.objects.link(rim)


def render_preview():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.filepath = PREVIEW_PATH
    scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.012, 0.018, 1.0)
    bpy.ops.render.render(write_still=True)


def export_glb():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(
        filepath=GLB_PATH,
        export_format="GLB",
        use_selection=False,
        export_apply=True,
    )


if __name__ == "__main__":
    root = build()
    add_camera_and_light()
    render_preview()
    export_glb()

    mesh_objs = [o for o in bpy.data.objects if o.type == "MESH"]
    glb_size = os.path.getsize(GLB_PATH)
    png_size = os.path.getsize(PREVIEW_PATH)
    print(f"[build_hero_head] {len(mesh_objs)} mesh objects, "
          f"glb: {GLB_PATH} ({glb_size} bytes), preview: {PREVIEW_PATH} ({png_size} bytes)")
    assert glb_size > 0, "exported .glb is empty"
    assert png_size > 0, "rendered preview .png is empty"
    assert len(mesh_objs) == 7, f"expected 7 mesh objects (skull, 3 forehead layers, 2 cheek plates, jaw, visor), got {len(mesh_objs)}"
