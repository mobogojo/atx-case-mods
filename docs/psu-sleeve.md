# PSU sleeve

A short printed sleeve that holds the PSU on its side behind the case's rear 120 mm fan
opening. The radiator takes over the top of the case, where the PSU used to sit.
Built by [`blender/parts/psu_sleeve.py`](../blender/parts/psu_sleeve.py); every number
below is a field of `PSUSleeveParams`.

## How it fits

```
   outside the case │ rear wall │ inside the case
                    │           │
          screws ──►│ ┌─seat────┤◄── PSU slides in from inside, stops on the seat
                    │ │         │
                    │ │  sleeve │ 30 mm
```

1. Cut the rear-wall metal for the PSU's switch, socket and vents, and drill its four
   screw holes (the seat makes a handy drilling template).
2. Put the sleeve against the inside of the rear wall, flange flat on the metal.
3. Slide the PSU in from inside the case until its rear face stops on the seat.
4. Screw the PSU's four screws in from outside: through the case wall, through the seat,
   into the PSU. That clamps all three together, so the sleeve needs no other fixing.

## Coordinate system

Millimetres. Origin at the centre of the flange on its rear face, which is also the
print bed (prints standing on the flange, no supports). **X** = across the case (the
PSU's 86 mm side), **Y** = up in the case (the PSU's 150 mm side, switch and socket at
the bottom), **Z** = forward into the case. Seen from outside, +X is to the left.

## Dimensions

| Parameter | Field | Value | Why |
|---|---|---|---|
| PSU | `psu_size` | 86 × 150 × 160 mm | Corsair RM850 spec (measured 85 mm thick) |
| Clearance | `psu_clearance` | 0.5 mm per side | Slides in after printing |
| Sleeve inside | (derived) | 87 × 151 mm | PSU + clearance |
| Wall | `wall` | 3 mm | Sleeve outside 93 × 157 mm |
| Length | `length` | 30 mm | Just enough to snug the PSU; the screws do the holding |
| Flange | `flange_size`, `flange_thickness` | 125 × 168 × 3 mm | Fan-opening area with 1 mm clearance each side |
| Seat | `seat_top`, `seat_sides`, `seat_bottom` | 10 / 10 / 3 mm | Bottom stays narrow to clear the switch and socket |
| Seat opening | (derived) | 67 × 141 mm | Switch, socket and rear vents stay open |
| PSU screw holes | `psu_screw_holes`, `psu_screw_dia` | 4 holes, 4.0 mm | #6-32 clearance |

PSU screw holes, seen from outside the case with the switch at the bottom (from the
PSU's left edge, from its top edge):

| Hole | From left | From top | Lands on |
|---|---|---|---|
| Top left | 16 mm | 6 mm | Top seat |
| Top right | 80 mm | 6 mm | Right seat |
| Left, low | 6 mm | 134 mm | Left seat |
| Bottom right | 80 mm | 144 mm | Right seat |

Optional extras, both off by default: `fan_slot_holes=True` adds the 120 mm fan pattern
(105 mm square) to the flange, and `fan_side="+x"`/`"-x"` cuts a 140 mm window for the
PSU fan. The window only makes sense for a sleeve long enough to reach the fan, about
160 mm.

## Before printing

1. **Check the screw hole positions.** They were read off a photo using the ATX-style
   6 mm / 16 mm offsets. Measure your PSU's four holes from its edges and set
   `psu_screw_holes` if any differ. Printing just the seat (`length=4`) is a cheap test.
2. **Screw length.** The screws now pass through ≈ 0.8 mm of steel plus the 3 mm seat
   before reaching the PSU. The standard 6 mm PSU screws would only catch about 2 mm of
   thread, so use **#6-32 × 8–10 mm** screws.

## Building

```python
import sys; sys.path.insert(0, "/path/to/atx-case-mods/blender")
import build
build.build_part("psu_sleeve")
build.build_part("psu_sleeve", length=40.0)
```

or headless: `blender -b -P blender/build.py -- --part psu_sleeve --export out/`.
