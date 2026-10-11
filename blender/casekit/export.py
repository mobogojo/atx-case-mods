"""Binary STL export that does not depend on Blender's exporter operators.

Blender renamed its STL operator in 4.1 (``export_mesh.stl`` -> ``wm.stl_export``) and
operators need a UI context; writing the file directly avoids both problems.
Coordinates are written as Blender units, i.e. millimetres.
"""

import os
import struct


def export_stl(obj, path):
    mesh = obj.data
    mesh.calc_loop_triangles()
    matrix = obj.matrix_world
    verts = [matrix @ v.co for v in mesh.vertices]
    tris = mesh.loop_triangles

    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "wb") as fh:
        header = ("atx-case-mods: %s (mm)" % obj.name).encode("ascii", "replace")
        fh.write(header[:80].ljust(80, b" "))
        fh.write(struct.pack("<I", len(tris)))
        for tri in tris:
            a, b, c = (verts[i] for i in tri.vertices)
            n = (b - a).cross(c - a)
            if n.length > 0:
                n.normalize()
            fh.write(struct.pack("<12fH", n.x, n.y, n.z,
                                 a.x, a.y, a.z, b.x, b.y, b.z, c.x, c.y, c.z, 0))
    return path
