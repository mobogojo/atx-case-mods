"""Primitive solids and boolean operations, all in millimetres.

Primitives return *unlinked* mesh objects. Cutters are never added to the scene, so
nothing is left behind if a script fails half way through.
"""

import math

import bmesh
import bpy
from mathutils import Matrix

# Overshoot used for cutters so booleans never leave zero-thickness skins.
EPS = 1.0


def _object_from_bmesh(name, bm):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return bpy.data.objects.new(name, mesh)


def box(name, x0, x1, y0, y1, z0, z1):
    """Axis-aligned box spanning [x0,x1] x [y0,y1] x [z0,z1]."""
    lo = (min(x0, x1), min(y0, y1), min(z0, z1))
    hi = (max(x0, x1), max(y0, y1), max(z0, z1))
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = lo[0] if v.co.x < 0 else hi[0]
        v.co.y = lo[1] if v.co.y < 0 else hi[1]
        v.co.z = lo[2] if v.co.z < 0 else hi[2]
    return _object_from_bmesh(name, bm)


def cylinder(name, x, y, z0, z1, diameter, segments=48, axis='Z'):
    """Cylinder of ``diameter`` along ``axis``.

    For axis 'Z' it is centred on (x, y) and spans z0..z1. For 'X' and 'Y' the
    arguments are taken in the rotated frame: (x, y) are the two cross-axis
    coordinates in X, Y, Z order with the long axis left out, and z0..z1 is the
    span along the long axis. E.g. axis='X': x -> Y, y -> Z, z0..z1 -> X.
    """
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        segments=segments,
        radius1=diameter / 2.0,
        radius2=diameter / 2.0,
        depth=abs(z1 - z0),
    )
    mid = (z0 + z1) / 2.0
    if axis == 'Z':
        offset = (x, y, mid)
    elif axis == 'X':
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0),
                         matrix=Matrix.Rotation(math.radians(90), 3, 'Y'))
        offset = (mid, x, y)
    elif axis == 'Y':
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0),
                         matrix=Matrix.Rotation(math.radians(90), 3, 'X'))
        offset = (x, mid, y)
    else:
        raise ValueError("axis must be 'X', 'Y' or 'Z', got %r" % (axis,))
    bmesh.ops.translate(bm, verts=bm.verts, vec=offset)
    return _object_from_bmesh(name, bm)


def join_meshes(name, objects):
    """Merge several unlinked primitives into one object (consumes the inputs).

    Inputs should not overlap each other; use separate booleans if they do.
    """
    bm = bmesh.new()
    for obj in objects:
        bm.from_mesh(obj.data)
        _discard(obj)
    return _object_from_bmesh(name, bm)


def boolean(target, cutter, operation='DIFFERENCE', keep_cutter=False):
    """Apply a boolean to ``target`` in place using the EXACT solver.

    Needs no active object or selection, so it is safe from scripts, the MCP
    bridge and background mode. ``cutter`` is deleted unless asked not to.
    """
    mod = target.modifiers.new(name="casekit_bool", type='BOOLEAN')
    mod.operation = operation
    mod.solver = 'EXACT'
    mod.object = cutter

    # Evaluation needs both objects in a view layer: link them into the active scene
    # just long enough to evaluate, then take them out again.
    scene_coll = bpy.context.scene.collection
    linked = []
    try:
        for obj in (target, cutter):
            if obj.name not in scene_coll.objects:
                scene_coll.objects.link(obj)
                linked.append(obj)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        depsgraph.update()
        evaluated = target.evaluated_get(depsgraph)
        new_mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph)
    finally:
        for obj in linked:
            scene_coll.objects.unlink(obj)

    target.modifiers.remove(mod)
    old_mesh, mesh_name = target.data, target.data.name
    target.data = new_mesh
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)
    new_mesh.name = mesh_name
    if not keep_cutter:
        _discard(cutter)
    return target


def mesh_stats(obj):
    """Volume (mm^3), bounding box and manifold check for print sanity tests."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    volume = bm.calc_volume(signed=False)
    xs = [v.co.x for v in bm.verts] or [0.0]
    ys = [v.co.y for v in bm.verts] or [0.0]
    zs = [v.co.z for v in bm.verts] or [0.0]
    bm.free()
    return {
        "volume_mm3": volume,
        "bounds": ((min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs))),
        "size": (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)),
        "non_manifold_edges": non_manifold,
    }


def _discard(obj):
    mesh = obj.data
    bpy.data.objects.remove(obj, do_unlink=True)
    if mesh is not None and mesh.users == 0:
        bpy.data.meshes.remove(mesh)
