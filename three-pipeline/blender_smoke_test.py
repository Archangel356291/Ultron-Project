"""Smoke test for the headless Blender -> .glb pipeline Module 9 (the
hero robotic head) will actually use. Doesn't build anything real --
just proves the mechanism itself: a bpy script run headlessly via
Blender's command line, constructing geometry procedurally, exporting
a real, loadable .glb file. Module 9's own script will follow this
exact same shape with real head geometry instead of a cube.

Run headlessly (no GUI, no window):

    "<blender.exe>" --background --python three-pipeline/blender_smoke_test.py
"""
import bpy
import os

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_smoke_test_output.glb")

# Start from an empty scene -- Blender's default scene has a camera/light/
# cube already; a real build script wants full control, not leftover
# defaults from Blender's startup file.
bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "SmokeTestCube"

bpy.ops.export_scene.gltf(
    filepath=OUT_PATH,
    export_format="GLB",
    use_selection=False,
)

size = os.path.getsize(OUT_PATH)
print(f"[blender_smoke_test] wrote {OUT_PATH} ({size} bytes)")
assert size > 0, "exported .glb is empty"
