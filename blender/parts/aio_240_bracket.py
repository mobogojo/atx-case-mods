"""240 mm AIO radiator bracket: 19 mm (0.75 in) structural base + 4 mm cosmetic bezel.

A 2-fan sibling of the 360 bracket (see aio_360_bracket.py). Same sandwich: a base
under the case top panel that the radiator/fans screw through, and a cosmetic bezel on
top. At 295 mm the plate fits a 305 mm print bed in one piece, so it does NOT have to be
segmented. A single shiplap joint is available for anyone who prefers two pieces: it runs
along a fan centreline (X=-60), not the middle, because the inner fan holes sit at X=+/-7.5
and a central lap would cut through them. That gives an unequal 217 + 97 mm pair with every
hole well clear of the seam.

Unlike the 360, this plate has NO lid-rail pocket. A 295 mm plate sitting 20 mm behind
the rear wall ends at ~315 mm from the rear, only clipping the front edge of the support
rail at 308-325 mm, so the pocket-over-the-rail trick doesn't apply. The intended build
removes that support bar; if you keep it, trim the plate to end before 308 mm from the
rear, or port the pocket over from the 360 part. See docs/aio-240-bracket.md.

Coordinate system (mm): origin at the plate centre on its bottom face, X along the
radiator length, Y across it, Z up.

Usage (inside Blender, with <repo>/blender on sys.path):
    from parts import aio_240_bracket as aio
    aio.build()                                   # base plate, one piece (fits the bed)
    aio.build(variant="bezel")                    # bezel, one piece
    aio.build(segmented=True)                     # split into two halves for printing
"""

from dataclasses import dataclass
from typing import Tuple

import casekit as ck

PART_NAME = "AIO_240_Bracket"
VARIANTS = ("base", "bezel")


@dataclass
class AIO240BracketParams:
    # Plate footprint
    length: float = 295.0         # X; fits a 275-280 mm 240 radiator incl. end tanks, and a 305 mm bed in one piece
    width: float = 145.0          # Y; 12.5 mm border outside a 120 mm fan
    base_thickness: float = 19.05  # 0.75 in structural standoff (matches the 360 base)
    bezel_thickness: float = 4.0  # upper cosmetic trim

    # Airflow opening (single rectangular slot, centred)
    cutout_l: float = 245.0    # length - 50: ~25 mm border each end
    cutout_w: float = 94.0     # < 100.5 so the fan holes keep a ~3 mm web (same as the 360)

    # Fan / radiator mounting grid
    fan_count: int = 2                # 240 = two 120 mm fans
    fan_pitch: float = 120.0          # centre-to-centre distance between fans
    fan_hole_spacing: float = 105.0   # square hole pattern of a 120 mm fan
    hole_dia: float = 4.5             # clearance for M4 / 6-32 radiator screws
    hole_segments: int = 48

    # Print segmentation (shiplap joint along X). The whole plate already fits the bed,
    # so this only matters when build(segmented=True) is used for two pieces. The joint
    # sits on a fan centreline, not the middle: the inner fan holes are at X=+/-7.5, so a
    # central lap would cut through them. X=-60 keeps all holes clear (217 + 97 mm pieces).
    split_x: Tuple[float, ...] = (-60.0,)
    lap_length: float = 20.0      # overlap length of the half-lap joint
    joint_clearance: float = 0.2  # gap left on the vertical faces of the joint
    bed_size: float = 305.0       # largest printable X or Y extent

    def thickness(self, variant):
        if variant not in VARIANTS:
            raise ValueError("variant must be one of %s, got %r" % (VARIANTS, variant))
        return self.base_thickness if variant == "base" else self.bezel_thickness

    def fan_centers(self):
        mid = (self.fan_count - 1) / 2.0
        return [(i - mid) * self.fan_pitch for i in range(self.fan_count)]

    def hole_positions(self):
        """(x, y) of every fan screw hole, fan by fan."""
        h = self.fan_hole_spacing / 2.0
        return [(cx + dx, dy)
                for cx in self.fan_centers()
                for dx in (-h, h)
                for dy in (-h, h)]

    def segment_bounds(self):
        """[(x_start, x_end), ...] of each printed segment, split at ``split_x``."""
        edges = [-self.length / 2.0] + sorted(self.split_x) + [self.length / 2.0]
        return list(zip(edges[:-1], edges[1:]))


def validate(p):
    """Return a list of human-readable problems with the parameters (empty == OK)."""
    problems = []
    r = p.hole_dia / 2.0
    half_cl, half_cw = p.cutout_l / 2.0, p.cutout_w / 2.0

    if p.cutout_l >= p.length or p.cutout_w >= p.width:
        problems.append("Cutout %.1f x %.1f does not fit inside plate %.1f x %.1f."
                        % (p.cutout_l, p.cutout_w, p.length, p.width))

    swallowed = [(x, y) for x, y in p.hole_positions()
                 if abs(x) + r <= half_cl and abs(y) + r <= half_cw]
    clipped = [(x, y) for x, y in p.hole_positions()
               if (x, y) not in swallowed
               and abs(x) - r < half_cl and abs(y) - r < half_cw]
    if swallowed:
        problems.append(
            "%d of %d fan holes fall entirely inside the %.1f x %.1f cutout, so they "
            "cut nothing and the radiator has no material to screw into. Holes sit at "
            "Y=+/-%.2f; the cutout must be narrower than %.2f mm to leave a web "
            "(e.g. cutout_w=94 leaves ~3 mm)."
            % (len(swallowed), len(p.hole_positions()), p.cutout_l, p.cutout_w,
               p.fan_hole_spacing / 2.0, p.fan_hole_spacing - p.hole_dia))
    if clipped:
        problems.append("%d fan holes break into the cutout edge: %s"
                        % (len(clipped), clipped))

    for x, y in p.hole_positions():
        if abs(x) + r > p.length / 2.0 or abs(y) + r > p.width / 2.0:
            problems.append("Fan hole at (%.2f, %.2f) breaks out of the plate edge." % (x, y))

    if p.width > p.bed_size:
        problems.append("Plate width %.1f does not fit the %.0f mm bed." % (p.width, p.bed_size))
    if not p.split_x and p.length > p.bed_size:
        problems.append("Whole plate length %.1f does not fit the %.0f mm bed; split it "
                        "(build with segmented=True)." % (p.length, p.bed_size))

    for x0, x1 in p.segment_bounds():
        seg_len = (x1 - x0) + p.lap_length / 2.0 * sum(
            1 for s in p.split_x if abs(s - x0) < 1e-9 or abs(s - x1) < 1e-9)
        if seg_len > p.bed_size or p.width > p.bed_size:
            problems.append("Segment %.2f..%.2f is %.2f x %.2f mm (incl. lap), larger "
                            "than the %.0f mm bed." % (x0, x1, seg_len, p.width, p.bed_size))

    for s in p.split_x:
        lo, hi = s - p.lap_length / 2.0, s + p.lap_length / 2.0
        if not (-p.length / 2.0 < lo and hi < p.length / 2.0):
            problems.append("Joint at X=%.2f (lap %.1f) runs off the plate." % (s, p.lap_length))
        for x, y in p.hole_positions():
            if lo - r < x < hi + r:
                problems.append("Joint at X=%.2f overlaps the fan hole at (%.2f, %.2f)."
                                % (s, x, y))
    return problems


def build_plate(p, variant="base", name=None):
    """Build one solid plate (unlinked) with the airflow cutout and fan holes."""
    t = p.thickness(variant)
    e = ck.EPS
    plate = ck.box(name or "%s_%s" % (PART_NAME, variant.capitalize()),
                   -p.length / 2, p.length / 2, -p.width / 2, p.width / 2, 0.0, t)

    cutout = ck.box("cutter_airflow", -p.cutout_l / 2, p.cutout_l / 2,
                    -p.cutout_w / 2, p.cutout_w / 2, -e, t + e)
    ck.boolean(plate, cutout)

    holes = [ck.cylinder("cutter_hole", x, y, -e, t + e, p.hole_dia, p.hole_segments)
             for x, y in p.hole_positions()]
    ck.boolean(plate, ck.join_meshes("cutter_holes", holes))
    return plate


def split_segments(plate, p, variant="base"):
    """Split ``plate`` into shiplap segments; returns new objects, consumes ``plate``.

    At every joint the left segment keeps the bottom half of the lap and the right
    segment keeps the top half, so the pieces stack and can be glued/screwed.
    """
    t = p.thickness(variant)
    e = ck.EPS
    half_y = p.width / 2 + e
    lap = p.lap_length / 2.0
    c = p.joint_clearance
    splits = sorted(p.split_x)
    bounds = p.segment_bounds()
    labels = _segment_labels(len(bounds))

    segments = []
    for i, (x0, x1) in enumerate(bounds):
        has_left_joint = i > 0
        has_right_joint = i < len(bounds) - 1
        seg = plate.copy()
        seg.data = plate.data.copy()
        seg.name = seg.data.name = "%s_Seg%d_%s" % (plate.name, i + 1, labels[i])

        # Keep everything between the outer ends of the laps on either side.
        keep_x0 = (x0 - lap + c) if has_left_joint else x0 - e
        keep_x1 = (x1 + lap - c) if has_right_joint else x1 + e
        ck.boolean(seg, ck.box("cutter_keep", keep_x0, keep_x1, -half_y, half_y, -e, t + e),
                   operation='INTERSECT')

        if has_right_joint:   # tongue on the right: drop the upper half of the lap
            s = splits[i]
            ck.boolean(seg, ck.box("cutter_lap", s - lap, s + lap + e,
                                   -half_y, half_y, t / 2.0, t + e))
        if has_left_joint:    # step on the left: drop the lower half of the lap
            s = splits[i - 1]
            ck.boolean(seg, ck.box("cutter_lap", s - lap - e, s + lap,
                                   -half_y, half_y, -e, t / 2.0))
        segments.append(seg)

    ck.geometry._discard(plate)
    return segments


def build(params=None, variant="base", segmented=False, export_dir=None,
          strict=False, scene=None):
    """Build the bracket into the ``ATX_Case_Mods/AIO_240_Bracket_<variant>`` collection.

    With ``segmented=False`` (default) the whole plate is built in one piece, which fits
    a 305 mm bed. ``segmented=True`` splits it at ``split_x`` into two half-lap halves.
    Returns the list of created objects; problems from ``validate`` are printed (or raised
    when ``strict``). If ``export_dir`` is given, each object is written there as STL.
    """
    p = params or AIO240BracketParams()
    problems = validate(p)
    for msg in problems:
        print("[%s] WARNING: %s" % (PART_NAME, msg))
    if problems and strict:
        raise ValueError("Invalid %s parameters:\n  " % PART_NAME + "\n  ".join(problems))

    ck.setup_scene_units(scene)
    coll = ck.part_collection("%s_%s" % (PART_NAME, variant.capitalize()), scene)

    plate = build_plate(p, variant)
    objects = split_segments(plate, p, variant) if segmented else [plate]
    for obj in objects:
        ck.link(obj, coll)
        if export_dir:
            ck.export_stl(obj, "%s/%s.stl" % (export_dir.rstrip("/"), obj.name))

    print("[%s] built %d object(s) for variant '%s'%s."
          % (PART_NAME, len(objects), variant, " (segmented)" if segmented else ""))
    return objects


def _segment_labels(n):
    if n == 1:
        return ["Full"]
    if n == 2:
        return ["Rear", "Front"]
    if n == 3:
        return ["Rear", "Center", "Front"]
    return ["Part%d" % (i + 1) for i in range(n)]
