"""Geometry sanity checks. Run with either:
    blender -b -P blender/selftest.py
    python blender/selftest.py          # needs the `bpy` wheel (pip install bpy)
Exits non-zero on failure.
"""

import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402

import casekit as ck  # noqa: E402
from parts import aio_360_bracket as aio  # noqa: E402
from parts import psu_sleeve as ps  # noqa: E402

failures = []


def check(cond, msg):
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond:
        failures.append(msg)


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# The originally supplied values (which validate() should flag) and the defaults.
# pocket_clearance is pinned to the original 2 mm (1 mm/side) so this case keeps
# documenting the original pocket at X=119.5..138.5; the defaults (WEBBED) use the
# current wider 22 mm clearance.
SPEC = aio.AIOBracketParams(cutout_w=121.0, split_x=(-108.75, 108.75), pocket_clearance=2.0)
WEBBED = aio.AIOBracketParams()

print("validate()")
check(any("fall entirely inside" in m for m in aio.validate(SPEC)),
      "spec cutout (121 mm) is flagged for swallowing the fan holes")
check(aio.validate(WEBBED) == [], "defaults pass validation: %s" % aio.validate(WEBBED))
check(sorted({round(x, 3) for x, _ in SPEC.hole_positions()})
      == [-172.5, -67.5, -52.5, 52.5, 67.5, 172.5], "hole X positions on a 120 mm fan pitch")
check(all(close(a, b) for a, b in zip(SPEC.pocket_x_range(), (119.5, 138.5))),
      "rail pocket at X=%s (rail 308..325 from rear wall, plate 20 mm in, +1 mm each side)"
      % (SPEC.pocket_x_range(),))
check(any("rail pocket at" in m for m in aio.validate(SPEC)),
      "spec joint at X=108.75 is flagged for ending 0.75 mm from the rail pocket")
check(any("past the" in m for m in aio.validate(aio.AIOBracketParams(rear_wall_to_plate=30.0))),
      "plate running past the front of the case is flagged")

for variant in aio.VARIANTS:
    t = SPEC.thickness(variant)
    for params, label in ((SPEC, "original spec"), (WEBBED, "defaults")):
        print("build %s / %s" % (variant, label))
        with tempfile.TemporaryDirectory() as tmp:
            whole = aio.build(params, variant=variant, export_dir=tmp)[0]
            st = ck.mesh_stats(whole)
            check(st["non_manifold_edges"] == 0, "whole plate is manifold")
            check(all(close(a, b) for a, b in zip(st["size"], (415.0, 145.0, t))),
                  "whole plate size %s" % (st["size"],))
            frame = (415.0 * 145.0 - params.cutout_l * params.cutout_w) * t
            if variant == "base":  # pocket only crosses the side rails beside the cutout
                px0, px1 = params.pocket_x_range()
                frame -= (px1 - px0) * (145.0 - params.cutout_w) * params.pocket_depth
            hole_area = 3.14159265 * (params.hole_dia / 2) ** 2
            n_holes = 0 if params is SPEC else len(params.hole_positions())
            check(abs(st["volume_mm3"] - (frame - n_holes * hole_area * t)) < 0.01 * frame,
                  "volume %.0f mm^3 matches frame minus %d holes" % (st["volume_mm3"], n_holes))
            check(os.path.getsize(os.path.join(tmp, whole.name + ".stl")) > 84, "STL written")

            segs = aio.build(params, variant=variant, segmented=True)
            n_segs = len(params.split_x) + 1
            check(len(segs) == n_segs, "%d segments" % n_segs)
            seg_stats = [ck.mesh_stats(s) for s in segs]
            check(all(s["non_manifold_edges"] == 0 for s in seg_stats), "segments are manifold")
            total = sum(s["volume_mm3"] for s in seg_stats)
            check(abs(total - st["volume_mm3"]) < 0.01 * st["volume_mm3"],
                  "segment volumes sum to the whole plate minus joint clearance")
            check(all(max(s["size"][:2]) <= params.bed_size for s in seg_stats),
                  "every segment fits the %.0f mm bed: %s"
                  % (params.bed_size, [tuple(round(v, 2) for v in s["size"]) for s in seg_stats]))

# Rebuilding must not pile up objects.
aio.build(WEBBED)
aio.build(WEBBED)
coll = bpy.data.collections["%s_Base" % aio.PART_NAME]
check(len(coll.objects) == 1, "rebuilding replaces the old objects")

# PSU sleeve
print("psu_sleeve")
PSU = ps.PSUSleeveParams()
check(ps.validate(PSU) == [], "defaults pass validation: %s" % ps.validate(PSU))
check(all(a > b for a, b in zip(PSU.inner(), PSU.psu_size[:2])),
      "PSU %s fits inside %s" % (PSU.psu_size[:2], PSU.inner()))
check(any("doesn't land" in m for m in ps.validate(ps.PSUSleeveParams(seat_sides=4.0))),
      "PSU screw holes off a too-narrow seat are flagged")
check(any("nut or screw head" in m
          for m in ps.validate(ps.PSUSleeveParams(wall=8.0, fan_slot_holes=True))),
      "fan-slot holes too close to a thick sleeve wall are flagged")
ix, iy = PSU.inner()
ox, oy = PSU.outer()
fx, fy = PSU.flange_size
t = PSU.flange_thickness
sx0, sx1, sy0, sy1 = PSU.seat_opening()
screws = len(PSU.psu_screw_holes) * math.pi * (PSU.psu_screw_dia / 2) ** 2 * t
seat_plate = (fx * fy - (sx1 - sx0) * (sy1 - sy0)) * t - screws
window = math.pi * (PSU.fan_window_dia / 2) ** 2 * PSU.wall
cases = (
    ("default 30 mm", PSU, seat_plate + (ox * oy - ix * iy) * (PSU.length - t)),
    ("300 mm, fan +x", ps.PSUSleeveParams(length=300.0, fan_side="+x"),
     seat_plate + (ox * oy - ix * iy) * (300.0 - t) - window),
)
for label, params, expected in cases:
    with tempfile.TemporaryDirectory() as tmp:
        obj = ps.build(params, export_dir=tmp)[0]
        st = ck.mesh_stats(obj)
        check(st["non_manifold_edges"] == 0, "sleeve (%s) is manifold" % label)
        check(all(close(a, b) for a, b in zip(st["size"], (fx, fy, params.length))),
              "sleeve (%s) size %s" % (label, st["size"]))
        check(abs(st["volume_mm3"] - expected) < 0.01 * expected,
              "sleeve (%s) volume %.0f ~ %.0f mm^3" % (label, st["volume_mm3"], expected))
        check(os.path.getsize(os.path.join(tmp, obj.name + ".stl")) > 84, "sleeve STL written")

print("\n%s" % ("ALL CHECKS PASSED" if not failures else "%d FAILURE(S)" % len(failures)))
sys.exit(1 if failures else 0)
