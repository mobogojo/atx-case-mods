# 360 mm AIO radiator bracket

A two-plate "sandwich" that mounts a 360 mm AIO radiator (3 × 120 mm fans) to the
top of an old ATX case: a **10 mm structural base** under the case top panel, and a
**4 mm cosmetic bezel** on top. The base has a pocket in its lid-facing face that
steps over the lid's support rail, so the rest of it sits flush on the steel. Built by
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
| Base thickness | `base_thickness` | 10 mm | 6 mm rail pocket + 4 mm floor under it |
| Bezel thickness | `bezel_thickness` | 4 mm | Cosmetic trim |
| Airflow cutout | `cutout_l` × `cutout_w` | 365 × 121 mm | Clears the airflow path |
| Fans | `fan_count`, `fan_pitch` | 3 @ 120 mm centre-to-centre | Three 120 mm fans inline |
| Fan hole pattern | `fan_hole_spacing` | 105 × 105 mm | Industry standard for 120 mm fans |
| Hole diameter | `hole_dia` | 4.5 mm | Clearance for M4 or 6-32 radiator screws |

Fan holes are at **Y = ±52.5 mm** and, with a 120 mm pitch,
**X = −172.5, −67.5, −52.5, +52.5, +67.5, +172.5 mm** (fan centres at −120, 0, +120;
15 mm between the nearest holes of neighbouring fans).

## Support rail pocket (base only)

A 5 mm thick, 17 mm wide reinforcement rail hangs under the middle of the case lid,
running across the plate (along Y). Measured at **308–325 mm from the outside face of
the case rear wall**.

```
 lid-facing face (Z = 10) ── sits flush on the steel lid
 ┌──────────┐            ┌──────────┐
 │          │  pocket    │          │   6 mm deep: clears the 5 mm rail by 1 mm
 │          └────────────┘          │
 │         4 mm floor               │
 └──────────────────────────────────┘   Z = 0, radiator side
           X = 99.5 → 118.5 (19 mm)
```

| Parameter | Field | Value | Notes |
|---|---|---|---|
| Rail span from rear wall | `rail_from_rear` | 308 → 325 mm | Measured from the outside rear face, confirmed (17 mm) |
| Rail thickness | `rail_thickness` | 5 mm | Measured |
| Pocket depth | `pocket_depth` | 6 mm | 1 mm clearance over the rail; 6.5 mm also fine (3.5 mm floor) |
| Pocket clearance | `pocket_clearance` | 2 mm | Added to the span, 1 mm each side → 19 mm, room to adjust |
| Outside rear face → plate −X edge | `rear_wall_to_plate` | 0 mm | **Assumed**, see open issues |

With those values the pocket sits at **X = 99.5 → 118.5 mm** and runs the full
width of the plate. It only removes material from the two side rails beside the
airflow cutout, which drop to 4 mm thick for those 19 mm. The pocket makes the base
**handed**: the −X end goes towards the rear wall. The bezel has no pocket.

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

These were found while turning the specs into code. The code keeps the spec
values as defaults and prints a warning, so nothing is silently changed.
`AIOBracketParams(cutout_w=94.0, split_x=(0,))` resolves all the warnings.

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
4. **The joint at X = +108.75 runs straight through the rail pocket.** The lap
   spans 98.75–118.75 and the pocket 99.5–118.5, so the right-hand joint loses almost
   all of its overlap in the base. `validate()` flags this. A single split at
   X = 0 (issue 3) is clear of both the pocket and the holes.
5. **Where the plate sits relative to the rear wall isn't measured.** The rail is
   measured from the *outside* of the rear wall, and the supplied script assumed the
   plate's −X edge is flush with that face (`rear_wall_to_plate = 0`). The plate sits
   inside the case, so it starts at least one wall thickness in, plus any lip or
   rolled edge, and the pocket shifts by the same amount. Measure from the outside
   rear face to where the plate's back edge will sit. Also measure the lid's inside
   length, to confirm the 415 mm plate fits front to back.
6. **The supplied pocket script had a few bugs.** These are fixed in the code:
   - all of the clearance went on one side of the rail instead of being split evenly;
   - it resized the base by picking `bpy.context.active_object`, which `select_set`
     doesn't change, so it would scale whatever object happened to be active. The
     code builds the base at 10 mm directly;
   - the ASCII diagram labels the floor layer as the face against the lid. It's
     actually the floor *under* the pocket; the lid-facing face is the full-height
     surface around the pocket.

## Building

```python
import sys; sys.path.insert(0, "/path/to/atx-case-mods/blender")
import build
build.build_part("aio_360_bracket", variant="all", segmented=True,
                 cutout_w=94.0, split_x=(0.0,))
```

or headless: `blender -b -P blender/build.py -- --variant all --segmented --export out/`.
