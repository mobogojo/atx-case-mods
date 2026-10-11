"""360 mm AIO radiator bracket: 10 mm structural base + 4 mm cosmetic bezel.

The two plates sandwich the case top panel: the base sits under the panel and the
radiator/fans screw through it, the bezel sits on top for a clean look. Both can be
split into shiplap (half-lap) segments so they fit a 305 mm print bed.

The case lid has a 5 mm thick support rail running across its underside (along Y).
The base has a pocket in its top (lid-facing) face that steps over that rail, so the
rest of the base sits flush against the steel. The pocket makes the base handed: its
-X end goes towards the case rear wall.

Coordinate system (mm): origin at the plate centre on its bottom face, X along the
radiator length, Y across it, Z up. Full spec and design notes: docs/aio-360-bracket.md

Usage (inside Blender, with <repo>/blender on sys.path):
    from parts import aio_360_bracket as aio
    aio.build()                                   # base plate, one piece
    aio.build(variant="bezel", segmented=True)    # bezel split for printing
    aio.build(AIOBracketParams(cutout_w=94.0))    # override any dimension
"""

from dataclasses import dataclass
from typing import Tuple

import casekit as ck

PART_NAME = "AIO_360_Bracket"
VARIANTS = ("base", "bezel")


@dataclass
class AIOBracketParams:
    # Plate footprint
    length: float = 415.0         # X; fits a 395-400 mm radiator incl. end tanks
    width: float = 145.0          # Y; 12.5 mm border outside a 120 mm fan
    base_thickness: float = 10.0  # lower structural bracket: 6 pocket + 4 floor
    bezel_thickness: float = 4.0  # upper cosmetic trim

    # Airflow opening (single rectangular slot, centred)
    cutout_l: float = 365.0
    cutout_w: float = 121.0

    # Fan / radiator mounting grid
    fan_count: int = 3
    fan_pitch: float = 120.0          # centre-to-centre distance between fans
    fan_hole_spacing: float = 105.0   # square hole pattern of a 120 mm fan
    hole_dia: float = 4.5             # clearance for M4 / 6-32 radiator screws
    hole_segments: int = 48

    # Pocket over the lid's support rail (base only). The rail runs across the plate
    # (along Y) on the lid underside; the pocket opens on the base's top face (Z=t).
    rail_from_rear: Tuple[float, float] = (308.0, 325.0)  # measured 17 mm rail span
    rail_thickness: float = 5.0        # measured; how far the rail hangs below the lid
    rear_wall_to_plate: float = 0.0    # rear wall -> plate's -X edge (ASSUMED, not measured)
    pocket_depth: float = 6.0          # rail + 1 mm so it doesn't bind (6.5 also OK)
    pocket_clearance: float = 2.0      # 17 -> 19 mm pocket: room to adjust along X

    # Print segmentation (shiplap joints along X)
    split_x: Tuple[float, ...] = (-108.75, 108.75)
    lap_length: float = 20.0      # overlap length of each half-lap joint
    joint_clearance: float = 0.2  # gap left on the vertical faces of each joint
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

    def pocket_x_range(self):
        """(x0, x1) of the rail pocket in plate coordinates, centred on the rail."""
        x_edge = -self.length / 2.0 + self.rear_wall_to_plate
        r0, r1 = self.rail_from_rear
        half = (r1 - r0 + self.pocket_clearance) / 2.0
        centre = x_edge + (r0 + r1) / 2.0
        return centre - half, centre + half

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

    # Rail pocket (base only)
    px0, px1 = p.pocket_x_range()
    if p.pocket_depth <= p.rail_thickness:
        problems.append("Pocket depth %.2f does not clear the %.2f mm rail."
                        % (p.pocket_depth, p.rail_thickness))
    if p.pocket_depth >= p.base_thickness:
        problems.append("Pocket depth %.2f cuts through the %.2f mm base."
                        % (p.pocket_depth, p.base_thickness))
    if not (-p.length / 2.0 < px0 and px1 < p.length / 2.0):
        problems.append("Rail pocket X=%.2f..%.2f runs off the plate." % (px0, px1))
    for x, y in p.hole_positions():
        if px0 - r < x < px1 + r:
            problems.append("Rail pocket X=%.2f..%.2f overlaps the fan hole at (%.2f, %.2f)."
                            % (px0, px1, x, y))
    for s in p.split_x:
        lo, hi = s - p.lap_length / 2.0, s + p.lap_length / 2.0
        if px0 < hi and lo < px1:
            problems.append(
                "Joint at X=%.2f (lap %.2f..%.2f) runs through the base plate's rail pocket at "
                "X=%.2f..%.2f, which removes most of the lap. Move the joint, e.g. "
                "split_x=(0,)." % (s, lo, hi, px0, px1))
    return problems


def build_plate(p, variant="base", name=None):
    """Build one solid plate (unlinked) with cutout, fan holes and (base) rail pocket."""
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

    if variant == "base":
        px0, px1 = p.pocket_x_range()
        pocket = ck.box("cutter_rail_pocket", px0, px1, -p.width / 2 - e, p.width / 2 + e,
                        t - p.pocket_depth, t + e)
        ck.boolean(plate, pocket)
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
    """Build the bracket into the ``ATX_Case_Mods/AIO_360_Bracket_<variant>`` collection.

    Returns the list of created objects. Problems found by ``validate`` are printed
    (or raised when ``strict``). If ``export_dir`` is given, each object is also
    written there as ``<object name>.stl``.
    """
    p = params or AIOBracketParams()
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
        return ["Left", "Right"]
    if n == 3:
        return ["Left", "Center", "Right"]
    return ["Part%d" % (i + 1) for i in range(n)]
