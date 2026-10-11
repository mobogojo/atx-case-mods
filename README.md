# atx-case-mods
open source brackets for repurposing old cases so they can be used with modern hardware and cooling systems.

## Project overview

The goal is a set of parametric, 3D-printable parts that let an old ATX case take
modern hardware. Parts are generated as Python scripts for Blender, so Claude can
build them directly in Blender through the
[Blender MCP](https://github.com/ahujasid/blender-mcp) connection, down to the
millimetre, and anyone can rebuild them with different dimensions.

The first part is a **360 mm AIO radiator bracket** for the case top: a two-plate
sandwich with a 10 mm structural base under the top panel and a 4 mm cosmetic bezel
above it. The base has a pocket that steps over the support rail under the middle
of the lid, so it sits flush against the steel. Both plates are split into
interlocking segments so they print on a 305 mm (Airwolf) bed.
An ATX case top template that the bracket mounts into is next.

| Part | Module | Variants | Spec |
|---|---|---|---|
| 360 mm AIO bracket | `blender/parts/aio_360_bracket.py` | `base` (10 mm), `bezel` (4 mm) | [docs/aio-360-bracket.md](docs/aio-360-bracket.md) |
| ATX case top template | *planned* | | |

### 360 mm AIO bracket at a glance

- Plate 415 × 145 mm (fits a 395–400 mm AIO body; 12.5 mm border outside a 120 mm fan).
- Airflow cutout 365 × 121 mm.
- Three 120 mm fans on a 120 mm pitch, 105 × 105 mm hole pattern, 4.5 mm holes
  (M4 / 6-32), at Y = ±52.5 mm and X = ±52.5, ±67.5, ±172.5 mm.
- Base: 6 mm deep × 19 mm pocket over the lid's 5 mm × 17 mm support rail (308–325 mm from the outside of the rear wall).
- Split with shiplap joints at X = ±108.75 mm into 98.75 / 217.5 / 98.75 mm segments.

> **Heads up:** as specified, the 121 mm cutout leaves no material around the fan
> holes, so the radiator has nothing to screw into. The script warns about this.
> The right-hand joint also runs through the rail pocket. See
> [open design issues](docs/aio-360-bracket.md#open-design-issues) for these and the
> other things to decide or measure.

## Repository layout

```
blender/
  build.py              entry point: CLI and build_part() helper
  selftest.py           geometry checks (manifold, size, volume, bed fit)
  casekit/              shared helpers: mm units, collections, primitives, booleans, STL
  parts/                one module per part, registered in parts/__init__.py
docs/                   per-part specs and design notes
CLAUDE.md               conventions for Claude when adding or changing parts
```

## Building the parts

**From Claude via Blender MCP** (or Blender's Python console / Text Editor) — the repo
must be on the same machine as Blender:

```python
import sys; sys.path.insert(0, "/path/to/atx-case-mods/blender")
import build
build.build_part("aio_360_bracket", variant="all", segmented=True)
# override any dimension:
build.build_part("aio_360_bracket", variant="base", cutout_w=94.0)
```

Calling `build_part` again rebuilds just that part's collection
(`ATX_Case_Mods/AIO_360_Bracket_Base`, ...). It reloads the modules every time, so
edits to the scripts show up without restarting Blender. Nothing else in the scene
is touched.

**Headless, with STL export:**

```sh
blender -b -P blender/build.py -- --list
blender -b -P blender/build.py -- --part aio_360_bracket --variant all --segmented --export out/
```

STLs are in millimetres, one file per object (e.g. `AIO_360_Bracket_Base_Seg2_Center.stl`).

**Tests:** `blender -b -P blender/selftest.py`, or `python blender/selftest.py` with
the [`bpy`](https://pypi.org/project/bpy/) wheel installed (`bpy==4.2.0` needs Python 3.11).
Tested with Blender 4.2.
