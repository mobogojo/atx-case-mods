"""casekit: small, context-free helpers for building printable case parts in Blender.

Conventions (see CLAUDE.md at the repo root):
  * 1 Blender unit == 1 mm. ``setup_scene_units()`` makes Blender display it that way.
  * Every helper works through ``bpy.data`` / ``bmesh`` rather than ``bpy.ops`` so it
    runs the same in the UI, over the Blender MCP bridge and in ``blender -b`` mode.
  * Each part lives in its own collection so rebuilding one part never deletes
    anything else in the scene.
"""

from .scene import setup_scene_units, part_collection, clear_collection, link
from .geometry import (
    EPS,
    box,
    cylinder,
    join_meshes,
    boolean,
    mesh_stats,
)
from .export import export_stl

__all__ = [
    "EPS",
    "setup_scene_units",
    "part_collection",
    "clear_collection",
    "link",
    "box",
    "cylinder",
    "join_meshes",
    "boolean",
    "mesh_stats",
    "export_stl",
]
