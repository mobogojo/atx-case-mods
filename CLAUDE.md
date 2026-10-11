# CLAUDE.md

Parametric, printable ATX case mod parts generated with Blender Python. Claude usually
runs these in the user's Blender through the Blender MCP bridge.

## Running

- In Blender / over MCP: `import sys; sys.path.insert(0, "<repo>/blender"); import build;
  build.build_part("<part>", variant=..., segmented=..., **param_overrides)`.
  `build_part` reloads `casekit` and `parts`, so edits take effect without restarting.
- Tests: `blender -b -P blender/selftest.py` (or `python blender/selftest.py` with the
  `bpy` pip wheel; `bpy==4.2.0` needs Python 3.11). Run them after any geometry change.

## Conventions

- **Units:** 1 Blender unit = 1 mm. Never scale objects; bake dimensions into vertices.
- **Origin:** part centre on its bottom face; X = length, Y = width, Z = up (print bed is Z=0).
- **No `bpy.ops`** in part code. Use `casekit` (`box`, `cylinder`, `join_meshes`,
  `boolean`, `export_stl`), which works through `bpy.data`/`bmesh` so it runs the same
  over MCP, in the UI and headless. Booleans use the EXACT solver; cutters overshoot
  by `casekit.EPS` and are never linked to the scene.
- **Scene hygiene:** each part/variant builds into its own collection under
  `ATX_Case_Mods` and only clears that collection. Never delete the user's other objects.
- **Every dimension is a dataclass field** with a comment saying why it has that value.
  No magic numbers in build code.
- **Validate, don't silently fix.** Each part has `validate(params)` returning
  human-readable problems (holes with no material, segments too big for the bed, joints
  through holes...). `build()` prints them; `strict=True` raises. If a user-given
  dimension looks wrong, keep it as the default, warn, and document it under
  "Open design issues" in the part's doc.
- **Printability:** default bed is 305 mm (Airwolf). Parts bigger than that get a
  `segmented=True` path with shiplap joints; check every segment fits.

## Adding a part

1. `blender/parts/<name>.py` exposing `PART_NAME`, `VARIANTS`, a `<Name>Params`
   dataclass, `validate(p)` and `build(params=None, variant=..., segmented=False,
   export_dir=None, strict=False, scene=None)` returning the created objects.
   Use `aio_360_bracket.py` as the template.
2. Register it in `blender/parts/__init__.py`.
3. Add checks to `blender/selftest.py` (manifold, size, volume, bed fit).
4. Write `docs/<name>.md` (dimensions table, coordinate system, open issues) and add a
   row to the parts table in `README.md`.
