# Hardware used in this build

What actually went into the reference build these parts were designed around: the
donor case being modernised and the components fitted into it. If you're adapting
these brackets, this is the baseline to compare your own hardware against. Measure
yours — the printed parts are parametric for a reason.

## The build in one line

An old full-size ATX tower, gutted and re-fitted with a 360 mm AIO liquid cooler in
the roof (via [aio-360-bracket.md](aio-360-bracket.md)) and its power supply relocated
to the rear fan opening (via [psu-sleeve.md](psu-sleeve.md)), because the radiator now
occupies the top-rear corner where the PSU used to live.

## Power supply

**Corsair RM850** — 850 W, 80+ Gold, standard ATX form factor.

| Property | Value | Source |
|---|---|---|
| Model | Corsair RM850 | Component used |
| Form factor | Standard ATX (PS/2) | Spec |
| Dimensions (W × H × L) | 150 × 86 × 160 mm | Spec; thickness measured at **85 mm** |
| Envelope incl. connected cables | 150 × 86 × **≈ 200 mm** | Measured (≥ 195 mm, rounded up) |
| Mounting screws | 4 × #6-32 (ATX standard) | Spec |
| Screw hole offsets | ATX-style 6 mm / 16 mm from the edges | Read off a photo — **verify yours** |

Notes for anyone reusing this:

- The 160 mm spec length is the bare body. Once the 24-pin, EPS and PCIe cables are
  plugged in and bent, allow ≈ 200 mm of clearance — that's what dictated the
  relocation, since the radiator stack needs the top-rear space.
- The sleeve ([psu-sleeve.md](psu-sleeve.md)) is modelled for the 86 mm × 150 mm rear
  face. A different PSU means different `psu_size`, and almost certainly different
  screw-hole offsets — the `psu_screw_holes` were read off a photo, not a jig, so
  measure your unit's four holes from its edges before committing to a print. Printing
  just the seat (`length=4`) is a cheap way to check the holes against the real PSU.
- With the sleeve, the four PSU screws pass through ≈ 0.8 mm of case steel plus the
  3 mm seat before reaching the PSU, so the stock 6 mm screws are too short. Use
  **#6-32 × 8–10 mm**.

## Donor case

A vintage full-size steel **ATX tower** with a removable top lid and a 5.25" drive
cage up front. Brand/model not recorded — if you know yours, note it here. What matters
for the parts is the geometry, measured in [case-measurements.md](case-measurements.md);
the key figures are summarised below.

| Dimension | Value | Notes |
|---|---|---|
| Chassis length, outside (rear → front frame) | ≈ 440 mm | Limits the roof bracket to 435 mm |
| Chassis width at top, inside | ≈ 195 mm | At the rear frame |
| Lid length (front–back) | ≈ 437 mm | Flat steel sheet, flanged all four edges |
| Lid width between side flanges, inside | ≈ 192 mm | Bracket must clear this |
| Lid support rail (cross channel) | 5 mm thick × 17 mm wide, 308–325 mm from rear | Base plate pockets over it |
| Rear fan opening | 120 mm fan | Now the PSU location |
| 5.25" drive cage | ≈ 285 mm from rear → front frame, inside ≈ 148–150 mm | Must be empty for the radiator |

Construction notes:

- The lid is a flat steel panel with folded flanges on all four edges; the roof
  bracket sits on top of it, outside the case, with a pocket that steps over the
  internal support rail.
- A riveted steel cross-channel runs side-to-side under the lid (it also forms the top
  of the drive cage's rear frame). It hangs ≈ 5 mm below the lid — that's the rail the
  base plate's pocket clears.
- The 5.25" bays overlap the front of the radiator. A test fit showed a 120 mm
  radiator drops between the cage side walls under the cross support, so the cage frame
  itself isn't in the way, but any drive in the top bays is. Plan to empty the top bays.

## Cooling

**360 mm AIO** (3 × 120 mm fans), mounted in the roof. The bracket is sized for a
395–400 mm radiator body (`length = 415 mm` plate) with a 105 × 105 mm fan hole
pattern and 120 mm fan pitch. The radiator + fan stack hangs ≈ 62 mm below the lid
(10 mm bracket + 27 mm radiator + 25 mm fans). See
[aio-360-bracket.md](aio-360-bracket.md) for the full fit.

## Fasteners summary

| Where | Fastener | Count |
|---|---|---|
| PSU → sleeve → case wall | #6-32 × 8–10 mm | 4 |
| Radiator/fans → bracket | M4 or #6-32 (4.5 mm clearance holes) | up to 12 |

## Still to confirm for a clone

These depend on the specific case and aren't nailed down (see "Still to measure" in
[case-measurements.md](case-measurements.md)):

- Case inside height (lid → floor) and GPU reach, for final PSU placement.
- Drive-cage inside width at the top, measured directly, if the cage stays.
- Lid-to-tallest-component height, for radiator + fan clearance.
