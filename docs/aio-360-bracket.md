# 360 mm AIO radiator bracket

A two-plate "sandwich" that mounts a 360 mm AIO radiator (3 × 120 mm fans) to the
top of an old ATX case: an **8 mm structural base** under the case top panel, and a
**4 mm cosmetic bezel** on top. Built by
[`blender/parts/aio_360_bracket.py`](../blender/parts/aio_360_bracket.py); every
number below is a field of `AIOBracketParams`.

## Coordinate system

Millimetres, 1 Blender unit = 1 mm. Origin at the centre of the plate on its bottom
face. **X** runs along the radiator (length), **Y** across it (width), **Z** up.

## Dimensions

| Parameter | Field | Value | Why |
|---|---|---|---|
| Plate length (X) | `length` | 415 mm | Fits a 395–400 mm AIO body incl. end-tank tolerance |
| Plate width (Y) | `width` | 145 mm | 12.5 mm clamping border outside a 120 mm fan |
| Base thickness | `base_thickness` | 8 mm | Rigidity for ABS |
| Bezel thickness | `bezel_thickness` | 4 mm | Cosmetic trim |
| Airflow cutout | `cutout_l` × `cutout_w` | 365 × 121 mm | Clears the airflow path |
| Fans | `fan_count`, `fan_pitch` | 3 @ 120 mm centre-to-centre | Three 120 mm fans inline |
| Fan hole pattern | `fan_hole_spacing` | 105 × 105 mm | Industry standard for 120 mm fans |
| Hole diameter | `hole_dia` | 4.5 mm | Clearance for M4 or 6-32 radiator screws |

Fan holes are at **Y = ±52.5 mm** and, with a 120 mm pitch,
**X = −172.5, −67.5, −52.5, +52.5, +67.5, +172.5 mm** (fan centres at −120, 0, +120;
15 mm between the nearest holes of neighbouring fans).

## Print segmentation (Airwolf 305 mm bed)

415 mm does not fit a 305 mm bed (not even diagonally: the plate diagonal is
~440 mm), so each plate is split along X with **shiplap (half-lap) joints** at
`split_x = (−108.75, +108.75)`. At each joint the left piece keeps the bottom half
of a `lap_length` = 20 mm overlap and the right piece keeps the top half;
`joint_clearance` = 0.2 mm is left on the vertical faces.

| Segment | Nominal X bounds | Nominal length | Printed size incl. laps |
|---|---|---|---|
| Left | −207.5 → −108.75 | 98.75 mm | 108.55 × 145 mm |
| Center | −108.75 → +108.75 | 217.50 mm | 237.10 × 145 mm |
| Right | +108.75 → +207.5 | 98.75 mm | 108.55 × 145 mm |

## Open design issues

These were found while turning the original spec into code. The code keeps the
spec values as defaults and prints a warning, so nothing is silently changed.

1. **The 121 mm cutout swallows every fan hole.** Holes sit at Y = ±52.5 mm but the
   cutout reaches Y = ±60.5 mm (and X = ±182.5 mm, past the outermost holes at
   ±172.5), so all 12 holes land in empty space and the radiator has nothing to
   screw into. Options:
   - narrow the slot: `cutout_w` < 100.5 mm leaves a web; **94 mm leaves ~3 mm**
     (`validate()` passes with this), or
   - keep a full-width opening in the bezel only and narrow it in the base, or
   - switch to per-fan round openings (not implemented yet).
2. **Hole list in the original notes didn't match the script.** It listed fan 1 at
   X = −165 / −60 and fan 3 at +60 / +165, which would put fan 1's and fan 2's
   holes 7.5 mm apart and doesn't match a 120 mm pitch. The code uses the
   script's 120 mm pitch (−172.5 / −67.5 etc.), which is the standard layout.
3. **The ±108.75 split is not "midway between the fan clusters".** The gap between
   fan 1 and fan 2 is at X = ±60. ±108.75 lands inside fan 1's / fan 3's opening,
   so with the slot cutout only the two side rails carry each joint. Splitting at
   ±60 is a bad idea: the 20 mm lap would run through the holes at ±52.5 / ±67.5
   (`validate()` flags this). A single split at X = 0 (`split_x=(0,)`) gives two
   217.5 mm halves (incl. lap) that fit the bed, with one joint instead of two and
   clear of all holes. The spec's ±108.75 is kept as the default.

## Building

```python
import sys; sys.path.insert(0, "/path/to/atx-case-mods/blender")
import build
build.build_part("aio_360_bracket", variant="all", segmented=True, cutout_w=94.0)
```

or headless: `blender -b -P blender/build.py -- --variant all --segmented --export out/`.
