# Generated STLs

Pre-built, ready-to-slice meshes, checked in for convenience. All are in millimetres,
watertight, and fit a 305 mm (Airwolf) bed. They are generated from the scripts in
[`../blender`](../blender) — regenerate them rather than editing by hand.

### 360 mm bracket (415 mm plate — must print in two pieces)

| File | Size (mm) | Notes |
|---|---|---|
| `AIO_360_Bracket_Base_Seg1_Rear.stl` | 217.3 × 145 × 19.05 | base (0.75 in), rear half; prints flat |
| `AIO_360_Bracket_Base_Seg2_Front.stl` | 217.3 × 145 × 19.05 | base (0.75 in), front half; **has the lid-rail pocket** |
| `AIO_360_Bracket_Bezel_Seg1_Rear.stl` | 217.3 × 145 × 4 | bezel, rear half; prints flat |
| `AIO_360_Bracket_Bezel_Seg2_Front.stl` | 217.3 × 145 × 4 | bezel, front half; prints flat |

The two 360 base segments are handed: `Seg1_Rear` goes toward the case rear wall,
`Seg2_Front` toward the front. Each plate is two pieces joined by a shiplap lap at the
middle.

### 240 mm bracket (295 mm plate — one piece, or optional two)

| File | Size (mm) | Notes |
|---|---|---|
| `AIO_240_Bracket_Base.stl` | 295 × 145 × 19.05 | base (0.75 in), **one piece**; prints flat |
| `AIO_240_Bracket_Bezel.stl` | 295 × 145 × 4 | bezel, one piece; prints flat |
| `AIO_240_Bracket_Base_Seg1_Rear.stl` | 97.3 × 145 × 19.05 | base, two-piece option, rear half |
| `AIO_240_Bracket_Base_Seg2_Front.stl` | 217.3 × 145 × 19.05 | base, two-piece option, front half |
| `AIO_240_Bracket_Bezel_Seg1_Rear.stl` | 97.3 × 145 × 4 | bezel, two-piece option, rear half |
| `AIO_240_Bracket_Bezel_Seg2_Front.stl` | 217.3 × 145 × 4 | bezel, two-piece option, front half |

The 240 plate fits the bed whole, so the one-piece `Base`/`Bezel` files are the default;
the `Seg*` files are the optional two-piece split along a fan centreline. Print **either**
the one-piece or the two `Seg` pieces for a given plate, not both. No rail pocket on the
240 (see [../docs/aio-240-bracket.md](../docs/aio-240-bracket.md)).

### Other

| File | Size (mm) | Notes |
|---|---|---|
| `PSU_Sleeve.stl` | 125 × 168 × 30 | prints standing on the flange, no supports |

## Regenerating

```sh
blender -b -P blender/build.py -- --part aio_360_bracket --variant all --segmented --export out/
blender -b -P blender/build.py -- --part aio_240_bracket --variant all --export out/             # one piece
blender -b -P blender/build.py -- --part aio_240_bracket --variant all --segmented --export out/ # two pieces
blender -b -P blender/build.py -- --part psu_sleeve --export out/
```

`out/` is the local, gitignored export directory; copy finished STLs here into
`generated/` when you want to commit them. See [../docs](../docs) for the full specs and
the pre-print checks (notably: verify the PSU screw-hole positions against your own PSU).
