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
| Airflow cutout | `cutout_l` × `cutout_w` | 365 × 94 mm | Leaves a ≈ 3 mm web around the fan holes (spec had 121) |
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
          X = 119.5 → 138.5 (19 mm)
```

| Parameter | Field | Value | Notes |
|---|---|---|---|
| Rail span from rear wall | `rail_from_rear` | 308 → 325 mm | Measured from the outside rear face, confirmed (17 mm) |
| Rail thickness | `rail_thickness` | 5 mm | Measured |
| Pocket depth | `pocket_depth` | 6 mm | 1 mm clearance over the rail; 6.5 mm also fine (3.5 mm floor) |
| Pocket clearance | `pocket_clearance` | 2 mm | Added to the span, 1 mm each side → 19 mm, room to adjust |
| Outside rear face → plate −X edge | `rear_wall_to_plate` | 20 mm | Rear 20 mm reserved for the PSU |
| Case length, outside | `case_length` | 440 mm | Plate must end inside it (20 + 415 = 435) |

The plate runs from 20 to 435 mm from the rear wall, so the 440 mm case leaves
5 mm at the front. With those values the pocket sits at **X = 119.5 → 138.5 mm**
(307–326 mm from the rear wall) and runs the full
width of the plate. It only removes material from the two side rails beside the
airflow cutout, which drop to 4 mm thick for those 19 mm. The pocket makes the base
**handed**: the −X end goes towards the rear wall. The bezel has no pocket.

## Print segmentation (Airwolf 305 mm bed)

415 mm does not fit a 305 mm bed (not even diagonally: the plate diagonal is
~440 mm), so each plate is split in two with a **shiplap (half-lap) joint** at
`split_x = (0,)`, i.e. in the middle of fan 2. The rear piece keeps the bottom half
of a `lap_length` = 20 mm overlap and the front piece keeps the top half;
`joint_clearance` = 0.2 mm is left on the vertical faces. The joint is clear of
every fan hole and of the rail pocket.

| Piece | X bounds | Printed size incl. lap | Rail pocket |
|---|---|---|---|
| `Base_Seg1_Rear` | −207.5 → 0 | 217.3 × 145 × 10 mm | No |
| `Base_Seg2_Front` | 0 → +207.5 | 217.3 × 145 × 10 mm | **Yes** |
| `Bezel_Seg1_Rear` | −207.5 → 0 | 217.3 × 145 × 4 mm | No |
| `Bezel_Seg2_Front` | 0 → +207.5 | 217.3 × 145 × 4 mm | No |

## Still open

1. **Front of the radiator runs into the 5.25" drive cage, so the bays must be
   empty.** The cage runs from about 285 mm from the rear to the front frame. A test
   fit shows a 120 mm radiator drops down between the cage side walls, under the
   cross support. So the cage frame isn't in the way, but any drive in the top bays
   is. If the cage stays: its walls stop at the cross support, ≈ 5 mm below the lid,
   so the lower 5 mm of the 10 mm base plate sits between them over the front
   ≈ 130 mm. The cage's inside width there has to be more than 145 mm (5.25" bays
   are usually ≈ 148 mm). Either confirm that width or step the plate narrower in
   that zone. If the cage is removed, this goes away. Width elsewhere is fine: the
   lid is ≈ 192 mm and the chassis ≈ 195 mm wide inside.
2. **Power supply placement.** The rear 20 mm is reserved for the PSU, and the
   plate starts behind it. How the PSU itself mounts is outside this part; see
   [case-measurements.md](case-measurements.md#power-supply).

## Resolved

These came up while turning the supplied specs into code. `validate()` still
checks for each of them, so changing a parameter back gets a warning.

1. **Cutout 121 → 94 mm.** At 121 mm the cutout reached Y = ±60.5 mm, past the
   fan holes at ±52.5, so all 12 holes landed in empty space and the radiator had
   nothing to screw into. Anything under 100.5 mm leaves a web; 94 mm leaves ≈ 3 mm.
2. **Hole positions follow the 120 mm fan pitch.** The original notes listed fan 1
   at X = −165 / −60 and fan 3 at +60 / +165, which would put neighbouring fans'
   holes 7.5 mm apart. The code uses −172.5 / −67.5 / −52.5 / +52.5 / +67.5 / +172.5.
3. **Split ±108.75 → one split at X = 0.** ±108.75 wasn't midway between fans (that's
   ±60, where a lap would hit the holes). With the plate 20 mm in from the rear,
   the +108.75 joint also ended 0.75 mm before the rail pocket, leaving the lap
   hanging off a thin wall (`validate()` wants `joint_pocket_margin` = 10 mm).
   One joint at X = 0 avoids both and gives two equal pieces.
4. **Pocket width.** The rail is 17 mm wide (308–325 mm from the rear wall). The
   "7 mm" in the notes was the pocket depth, now 6 mm, with the pocket 19 mm long.
5. **Plate position.** The plate starts 20 mm in from the outside of the rear wall
   (`rear_wall_to_plate = 20`), leaving room for the PSU, and ends at 435 mm, inside
   the 440 mm case. The pocket only has 1 mm of play on each side, so a test fit is
   still worthwhile.
6. **Bugs in the supplied pocket script**, fixed in the code:
   - all of the clearance went on one side of the rail instead of being split evenly;
   - it resized the base through `bpy.context.active_object`, which `select_set`
     doesn't change, so it could scale the wrong object. The code builds the base at
     10 mm directly;
   - its ASCII diagram labels the floor layer as the face against the lid. It's
     actually the floor *under* the pocket; the lid-facing face is the full-height
     surface around the pocket.

## Building

```python
import sys; sys.path.insert(0, "/path/to/atx-case-mods/blender")
import build
build.build_part("aio_360_bracket", variant="all", segmented=True)
```

or headless: `blender -b -P blender/build.py -- --variant all --segmented --export out/`.
