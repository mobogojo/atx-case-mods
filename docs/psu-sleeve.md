# PSU sleeve

A printed sleeve that holds the PSU on its side behind the case's rear 120 mm fan
opening. The radiator takes over the top of the case, where the PSU used to sit.
Built by [`blender/parts/psu_sleeve.py`](../blender/parts/psu_sleeve.py); every
number below is a field of `PSUSleeveParams`.

## How it fits

- The **flange** sits against the inside of the rear wall, over the fan-opening area,
  and bolts through the case's fan slots.
- The **sleeve** runs forward into the case. The PSU slides in from the front, and its
  rear face (switch, power socket, screw holes) ends flush with the flange.
- Cut the rear-wall metal for the switch and socket. The PSU can then also be screwed
  to the rear wall with its own four screws.
- The front end is open for the cables.

## Coordinate system

Millimetres. Origin at the centre of the flange on its rear face, which is also the
print bed. **X** = across the case (the PSU's 86 mm side), **Y** = up in the case
(the PSU's 150 mm side), **Z** = forward into the case.

## Dimensions

| Parameter | Field | Value | Why |
|---|---|---|---|
| PSU | `psu_size` | 86 × 150 × 160 mm | Corsair RM850 spec (measured 85 mm thick) |
| Clearance | `psu_clearance` | 0.5 mm per side | Slides in after printing |
| Sleeve inside | (derived) | 87 × 151 mm | PSU + clearance |
| Wall | `wall` | 3 mm | Sleeve outside 93 × 157 mm |
| Length | `length` | 300 mm | Flange rear face → open front end |
| Flange | `flange_size`, `flange_thickness` | 125 × 168 × 4 mm | Fan-opening area with 1 mm clearance each side |
| Mounting holes | `hole_spacing`, `hole_dia` | 105 mm square, 4.5 mm | Standard 120 mm fan pattern, through the case's fan slots |
| PSU fan window | `fan_side`, `fan_window_dia` | 140 mm round on the +X wall | The RM850's 135 mm fan faces a side wall when mounted sideways |

The mounting holes sit at (±52.5, ±52.5) mm, beside the sleeve, with 6 mm between each
hole and the sleeve wall for a nut or screw head. The fan window is centred 80 mm
forward of the flange, where the fan is on the PSU. Set `fan_side="-x"` if the PSU goes
in the other way up, or `"none"` for a closed sleeve.

## Still open

1. **Print height.** Standing on its flange, the 300 mm sleeve is taller than the
   254 mm Z height of an Airwolf AXIOM. That printer is an assumption from the 305 mm
   bed, so set `max_print_height` to your printer's real Z. If it doesn't fit, a
   250 mm sleeve (`length=250`) still covers the 160 mm PSU plus 90 mm for cables and
   passes every check. Printing it lying down needs supports under the top wall.
2. **Fan side.** Which side of the case the PSU fan should face: toward the side panel
   (needs vents there) or toward the motherboard.
3. **Clearance inside the case.** The sleeve runs 300 mm forward at the height of the
   rear fan opening. Check it clears the radiator and fans (which hang ≈ 62 mm below
   the lid), the CPU cooler and RAM, and the graphics card.

## Building

```python
import sys; sys.path.insert(0, "/path/to/atx-case-mods/blender")
import build
build.build_part("psu_sleeve")
build.build_part("psu_sleeve", length=250.0, fan_side="-x")
```

or headless: `blender -b -P blender/build.py -- --part psu_sleeve --export out/`.
