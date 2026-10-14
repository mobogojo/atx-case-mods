# Generated STLs

Pre-built, ready-to-slice meshes, checked in for convenience. All are in millimetres,
watertight, and fit a 305 mm (Airwolf) bed. They are generated from the scripts in
[`../blender`](../blender) — regenerate them rather than editing by hand.

| File | Size (mm) | Notes |
|---|---|---|
| `AIO_360_Bracket_Base_Seg1_Rear.stl` | 217.3 × 145 × 19.05 | base (0.75 in), rear half; prints flat |
| `AIO_360_Bracket_Base_Seg2_Front.stl` | 217.3 × 145 × 19.05 | base (0.75 in), front half; **has the lid-rail pocket** |
| `AIO_360_Bracket_Bezel_Seg1_Rear.stl` | 217.3 × 145 × 4 | bezel, rear half; prints flat |
| `AIO_360_Bracket_Bezel_Seg2_Front.stl` | 217.3 × 145 × 4 | bezel, front half; prints flat |
| `PSU_Sleeve.stl` | 125 × 168 × 30 | prints standing on the flange, no supports |

The two AIO base segments are handed: `Seg1_Rear` goes toward the case rear wall,
`Seg2_Front` toward the front. Each plate is two pieces joined by a shiplap lap at the
middle.

## Regenerating

```sh
blender -b -P blender/build.py -- --part aio_360_bracket --variant all --segmented --export out/
blender -b -P blender/build.py -- --part psu_sleeve --export out/
```

`out/` is the local, gitignored export directory; copy finished STLs here into
`generated/` when you want to commit them. See [../docs](../docs) for the full specs and
the pre-print checks (notably: verify the PSU screw-hole positions against your own PSU).
