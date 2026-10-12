# Donor case measurements

Measurements of the donor ATX case, used by the AIO bracket and the planned case top
template. "Measured" values came straight from the tape. "Photo" values were read
off tape-measure photos and are only good to about ±3–5 mm. Confirm a photo value
before a part depends on it.

Directions: **rear** = I/O and exhaust-fan wall, **front** = drive bays.
"From rear" means from the outside face of the rear wall.

## Lid (removable top panel)

| Dimension | Value | Source |
|---|---|---|
| Length (front–back) | ≈ 437 mm | Photo: 17¼ in, hook over the end flange |
| Width (side–side), outside | ≈ 200 mm | Photo |
| Width between the side flanges (inside) | ≈ 192 mm | Photo, tape across the flanges |
| Construction | Flat steel sheet with folded flanges on all four edges | Photo |

## Chassis

| Dimension | Value | Source |
|---|---|---|
| Length, outside rear → front frame | ≈ 440 mm | Photo |
| Width at the top, outside | ≈ 207 mm | Photo |
| Width at the top, inside (rear frame) | ≈ 195 mm | Photo, close-up of the tape at the edge |

## Cross support under the lid

A riveted steel channel runs side to side under the lid. It also forms the top of
the 5.25" drive cage's rear frame.

| Dimension | Value | Source |
|---|---|---|
| Position from rear | 308 → 325 mm | Measured |
| Width (front–back) | 17 mm | Measured, confirmed by photo |
| Thickness (how far it hangs below the lid) | 5 mm | Measured |

## 5.25" drive cage

It sits under the front of the lid, from roughly **285 mm from the rear to the
front frame (≈ 440 mm)**. Its side walls stop at the cross support, which sits on
top of them, so they end ≈ 5 mm below the lid. Inside width between the walls is
roughly 148–150 mm (rough photo estimate; 5.25" bays are normally ≈ 148 mm). A test fit
shows a 120 mm wide radiator drops down between its side walls, so only drives in
the top bays get in the way. See "Still open" in [aio-360-bracket.md](aio-360-bracket.md#still-open).

## Power supply

The stock PSU sits top-rear, where the radiator's rear end goes, so it has to be
relocated. The rear 20 mm of the case is reserved for it, and the bracket starts
behind that.

| Dimension | Value | Source |
|---|---|---|
| PSU envelope incl. connected cables | 150 × 86 × **200 mm** (W × H × L) | Measured in a reference build (≥ 195 mm, rounded up) |
| Space under the radiator stack | lid → 62 mm down (10 bracket + 27 radiator + 25 fans) | Bracket design |
| Old drive cage zone, front–back | ≈ 150 mm (≈ 285 mm from rear → front frame) | Photo |

Where it can go once the drive cage is removed:

- **Flat at the front, under the radiator:** doesn't fit. The PSU needs 200 mm of
  length but the zone is ≈ 150 mm deep, and the case is ≈ 195 mm wide inside, so
  it can't turn sideways either.
- **Standing on end at the front:** takes 150 mm across × 86 mm front–back, which
  fits. It needs ≈ 262 mm clear below the lid (62 + 200), away from the GPU.
- **Flat on the case floor:** 200 mm front–back, if there's room below the GPU.

Either way, the old PSU opening in the rear wall needs a cover plate, and a
front-mounted PSU needs its own air intake.

## Still to measure

- Lid flange height and the inside length between the end flanges.
- Inside width of the drive cage at the top, measured directly. The bottom 5 mm of
  the 10 mm base plate sits between the cage walls, so it must be > 145 mm.
- Height from the lid to the top of the motherboard tray / tallest board
  component, for radiator + fan clearance.
- Case inside height (lid to floor), what sits below the 5.25" cage at the front
  (3.5" cage?), and how far forward / how high the GPU reaches, to place the PSU.
