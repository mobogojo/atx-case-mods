# atx-case-mods
open source brackets for repurposing old cases so they can be used with modern hardware and cooling systems.

## Project overview

The goal is a set of parametric, 3D-printable parts that let an old ATX case take
modern hardware. Parts are generated as Python scripts for Blender, so Claude can
build them directly in Blender through the
[Blender MCP](https://github.com/ahujasid/blender-mcp) connection, down to the
millimetre, and anyone can rebuild them with different dimensions.

The first part is a **360 mm AIO radiator bracket** for the case top: a two-plate
sandwich with a 19 mm (0.75 in) structural base under the top panel and a 4 mm cosmetic
bezel above it. The base has a pocket that steps over the support rail under the middle
of the lid, so it sits flush against the steel. Both plates are split into
interlocking segments so they print on a 305 mm (Airwolf) bed.
An ATX case top template that the bracket mounts into is next. The PSU and donor
case this was built around are in [docs/hardware.md](docs/hardware.md); raw donor case
measurements are in [docs/case-measurements.md](docs/case-measurements.md).

| Part | Module | Variants | Spec |
|---|---|---|---|
| 360 mm AIO bracket | `blender/parts/aio_360_bracket.py` | `base` (19.05 mm), `bezel` (4 mm) | [docs/aio-360-bracket.md](docs/aio-360-bracket.md) |
| 240 mm AIO bracket | `blender/parts/aio_240_bracket.py` | `base` (19.05 mm), `bezel` (4 mm) | [docs/aio-240-bracket.md](docs/aio-240-bracket.md) |
| PSU sleeve | `blender/parts/psu_sleeve.py` | `sleeve` | [docs/psu-sleeve.md](docs/psu-sleeve.md) |
| ATX case top template | *planned* | | |

### 360 mm AIO bracket at a glance

- Plate 415 × 145 mm (fits a 395–400 mm AIO body; 12.5 mm border outside a 120 mm fan).
- Airflow cutout 365 × 94 mm (leaves a ≈ 3 mm web around the fan holes).
- Three 120 mm fans on a 120 mm pitch, 105 × 105 mm hole pattern, 4.5 mm holes
  (M4 / 6-32), at Y = ±52.5 mm and X = ±52.5, ±67.5, ±172.5 mm.
- Plate sits 20–435 mm from the outside of the rear wall (rear 20 mm reserved for the PSU).
- Base: 19.05 mm (0.75 in) thick; 6 mm deep × 39 mm pocket dropping over the lid's 5 mm × 17 mm support rail (308–325 mm from the outside of the rear wall), with 11 mm slack each side.
- Each plate prints as two 217.3 mm pieces (Rear / Front) joined by a shiplap joint at
  the middle; only the front base piece has the rail pocket.

Still open: the drive cage (empty bays, or removed). See
[docs/aio-360-bracket.md](docs/aio-360-bracket.md#still-open).

### 240 mm AIO bracket at a glance

A two-fan sibling of the 360 bracket for a 240 mm radiator.

- Plate 295 × 145 mm, which **fits the 305 mm bed in one piece** — no split needed.
- Airflow cutout 245 × 94 mm; two 120 mm fans on a 120 mm pitch, 105 × 105 mm hole
  pattern, 4.5 mm holes at Y = ±52.5 mm and X = ±7.5, ±112.5 mm.
- Base 19.05 mm (0.75 in), bezel 4 mm. **No rail pocket** — the short plate doesn't
  span the lid support bar, which the reference build removes anyway.
- Optional two-piece print: one shiplap joint on a fan centreline (X = −60) → unequal
  97.3 + 217.3 mm halves, all holes clear of the seam.

See [docs/aio-240-bracket.md](docs/aio-240-bracket.md).

### PSU sleeve at a glance

With the radiator in the top of the case, the PSU moves to the rear 120 mm fan opening
and lies on its side in a short printed sleeve.

- Sleeve inside 87 × 151 mm (Corsair RM850, 86 × 150 mm, + 0.5 mm per side), 3 mm walls,
  30 mm long, on a 125 × 168 × 3 mm flange.
- A seat at the rear (10 mm top and sides, 3 mm bottom to clear the switch) stops the
  PSU. The PSU's own screws go through the case wall and the seat, clamping everything.

## Repository layout

```
blender/
  build.py              entry point: CLI and build_part() helper
  selftest.py           geometry checks (manifold, size, volume, bed fit)
  casekit/              shared helpers: mm units, collections, primitives, booleans, STL
  parts/                one module per part, registered in parts/__init__.py
docs/                   per-part specs, design notes and donor case measurements
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
build.build_part("aio_360_bracket", variant="base", pocket_depth=6.5)
build.build_part("psu_sleeve")
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
