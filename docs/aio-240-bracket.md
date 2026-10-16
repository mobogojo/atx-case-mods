# 240 mm AIO radiator bracket

A two-fan version of the [360 bracket](aio-360-bracket.md) for mounting a 240 mm AIO
radiator (2 × 120 mm fans) to the top of an old ATX case: a **19 mm (0.75 in) structural
base** under the case top panel and a **4 mm cosmetic bezel** on top. Built by
[`blender/parts/aio_240_bracket.py`](../blender/parts/aio_240_bracket.py); every number
below is a field of `AIO240BracketParams`.

The big difference from the 360: at **295 mm the whole plate fits a 305 mm (Airwolf)
bed in one piece**, so it does not have to be segmented, and it has **no lid-rail
pocket** (see [Rail / placement](#rail--placement)).

## Coordinate system

Millimetres, 1 Blender unit = 1 mm. Origin at the centre of the plate on its bottom
face. **X** runs along the radiator (length), **Y** across it (width), **Z** up.

## Dimensions

| Parameter | Field | Value | Why |
|---|---|---|---|
| Plate length (X) | `length` | 295 mm | Fits a 275–280 mm 240 AIO body incl. end tanks, and a 305 mm bed in one piece |
| Plate width (Y) | `width` | 145 mm | 12.5 mm clamping border outside a 120 mm fan |
| Base thickness | `base_thickness` | 19.05 mm | 0.75 in standoff (matches the 360 base) |
| Bezel thickness | `bezel_thickness` | 4 mm | Cosmetic trim |
| Airflow cutout | `cutout_l` × `cutout_w` | 245 × 94 mm | Leaves a ≈ 3 mm web around the fan holes |
| Fans | `fan_count`, `fan_pitch` | 2 @ 120 mm centre-to-centre | Two 120 mm fans inline |
| Fan hole pattern | `fan_hole_spacing` | 105 × 105 mm | Industry standard for 120 mm fans |
| Hole diameter | `hole_dia` | 4.5 mm | Clearance for M4 or 6-32 radiator screws |

Fan holes are at **Y = ±52.5 mm** and, with a 120 mm pitch, at
**X = −112.5, −7.5, +7.5, +112.5 mm** (fan centres at ±60).

## Printing (Airwolf 305 mm bed)

The whole plate is 295 × 145 mm, so it **prints in one piece** — that is the default
(`build(... )` / the headless build without `--segmented`). The margin to the bed edge
is only ~10 mm, so if your first layer or adhesion is fussy near the edges, print it in
two pieces instead.

Two-piece (`build(segmented=True)` / `--segmented`): one shiplap half-lap joint on a
**fan centreline at X = −60**, not the middle. The inner fan holes sit at X = ±7.5, so a
central lap would cut through them; the fan-line joint keeps every hole ≈ 42 mm clear of
the seam. The pieces are unequal:

| Piece | X bounds | Printed size incl. lap |
|---|---|---|
| `…_Seg1_Rear` | −147.5 → −60 | 97.3 × 145 mm |
| `…_Seg2_Front` | −60 → +147.5 | 217.3 × 145 mm |

Glue/fasten the lap after printing; the radiator and its fan screws bridge and clamp the
seam. This applies to both the base (19.05 mm) and the bezel (4 mm).

## Rail / placement

The 360 base has a pocket that steps over the lid's 5 mm support rail (308–325 mm from
the rear wall). The 240 plate does **not**: a 295 mm plate sitting 20 mm behind the rear
wall ends at ~315 mm from the rear, only clipping the front edge of the rail, so the
pocket trick doesn't apply. The reference build removes that support bar (cut it or pull
the rivets), which is the assumption here.

If you keep the bar: either shorten the plate so it ends before 308 mm from the rear
(`length ≤ 288`, tight for a 277 mm radiator), reposition the plate forward of the rail,
or port the pocket code from [`aio_360_bracket.py`](../blender/parts/aio_360_bracket.py)
(`pocket_x_range`, the `build_plate` pocket cutter, and the related `validate` checks).

## Building

```python
import sys; sys.path.insert(0, "/path/to/atx-case-mods/blender")
import build
build.build_part("aio_240_bracket", variant="all")                 # one piece each
build.build_part("aio_240_bracket", variant="all", segmented=True) # two pieces each
```

or headless:

```sh
blender -b -P blender/build.py -- --part aio_240_bracket --variant all --export out/
blender -b -P blender/build.py -- --part aio_240_bracket --variant all --segmented --export out/
```
