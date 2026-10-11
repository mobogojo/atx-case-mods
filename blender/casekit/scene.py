"""Scene, unit and collection management."""

import bpy

ROOT_COLLECTION = "ATX_Case_Mods"


def setup_scene_units(scene=None):
    """Make 1 Blender unit display as 1 mm (metric, scale 0.001)."""
    scene = scene or bpy.context.scene
    units = scene.unit_settings
    units.system = 'METRIC'
    units.scale_length = 0.001
    units.length_unit = 'MILLIMETERS'
    return scene


def _root(scene):
    root = bpy.data.collections.get(ROOT_COLLECTION)
    if root is None:
        root = bpy.data.collections.new(ROOT_COLLECTION)
    if root.name not in scene.collection.children:
        scene.collection.children.link(root)
    return root


def part_collection(name, scene=None, clear=True):
    """Return the collection ``ATX_Case_Mods/<name>``, emptied if ``clear``."""
    scene = scene or bpy.context.scene
    root = _root(scene)
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
    if coll.name not in root.children:
        root.children.link(coll)
    if clear:
        clear_collection(coll)
    return coll


def clear_collection(coll):
    """Delete every object (and its now-orphaned mesh) in ``coll``."""
    for obj in list(coll.objects):
        mesh = obj.data if obj.type == 'MESH' else None
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh is not None and mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def link(obj, coll):
    """Link ``obj`` into ``coll`` (unlinking it from any other collection)."""
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)
    return obj
