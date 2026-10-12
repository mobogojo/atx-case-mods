"""PSU sleeve: holds an ATX PSU on its side behind the case's rear 120 mm fan opening.

The flange sits against the inside of the rear wall over the fan opening and bolts
through the fan slots. The sleeve runs forward into the case. The PSU slides in from
the front, and its rear face (switch, socket, screw holes) ends flush with the flange,
so it can also be screwed to the rear wall once the metal is cut out.

Coordinate system (mm): origin at the centre of the flange on its rear face, which is
also the print bed (print standing on the flange). X = across the case (the PSU's
86 mm side), Y = up in the case (the PSU's 150 mm side), Z = forward into the case.
Full spec and notes: docs/psu-sleeve.md

Usage (inside Blender, with <repo>/blender on sys.path):
    from parts import psu_sleeve
    psu_sleeve.build()
    psu_sleeve.build(psu_sleeve.PSUSleeveParams(fan_side="-x"))
"""

from dataclasses import dataclass
from typing import Tuple

import casekit as ck

PART_NAME = "PSU_Sleeve"
VARIANTS = ("sleeve",)
FAN_SIDES = ("+x", "-x", "none")


@dataclass
class PSUSleeveParams:
    # PSU: Corsair RM850, standard ATX. Mounted sideways, so its 86 mm thickness runs
    # across the case (X) and its 150 mm width runs up (Y).
    psu_size: Tuple[float, float, float] = (86.0, 150.0, 160.0)  # X, Y, length; spec
    psu_clearance: float = 0.5    # per side, so it slides in after printing

    # Sleeve
    wall: float = 3.0             # sleeve wall thickness
    length: float = 300.0         # flange rear face -> open front end

    # Flange over the rear 120 mm fan opening (1 mm clearance each side of the area)
    flange_size: Tuple[float, float] = (125.0, 168.0)  # X, Y
    flange_thickness: float = 4.0

    # Mounting holes through the case's fan slots (standard 120 mm fan pattern)
    hole_spacing: float = 105.0
    hole_dia: float = 4.5         # M4 / fan-screw clearance
    hole_segments: int = 32
    nut_clearance: float = 3.5    # hole centre -> sleeve wall, room for a nut/screw head

    # Window for the PSU's own fan (on the 150 x 160 face, i.e. an X wall)
    fan_side: str = "+x"          # "+x", "-x" or "none"
    fan_window_dia: float = 140.0  # RM850 has a 135 mm fan
    fan_segments: int = 96

    # Printing (standing on the flange)
    bed_size: float = 305.0           # largest X or Y extent
    max_print_height: float = 254.0   # ASSUMED (Airwolf AXIOM); confirm for your printer

    def inner(self):
        """(x, y) inside size of the sleeve."""
        c = 2 * self.psu_clearance
        return self.psu_size[0] + c, self.psu_size[1] + c

    def outer(self):
        """(x, y) outside size of the sleeve."""
        ix, iy = self.inner()
        return ix + 2 * self.wall, iy + 2 * self.wall

    def hole_positions(self):
        h = self.hole_spacing / 2.0
        return [(dx, dy) for dx in (-h, h) for dy in (-h, h)]

    def fan_window_centre_z(self):
        """Fan sits mid-length on the PSU, whose rear face is at the flange (Z=0)."""
        return self.psu_size[2] / 2.0


def validate(p):
    """Return a list of human-readable problems with the parameters (empty == OK)."""
    problems = []
    ix, iy = p.inner()
    ox, oy = p.outer()
    fx, fy = p.flange_size
    r = p.hole_dia / 2.0

    if p.fan_side not in FAN_SIDES:
        problems.append("fan_side must be one of %s, got %r." % (FAN_SIDES, p.fan_side))
    if ox > fx or oy > fy:
        problems.append("Sleeve outside %.1f x %.1f is larger than the %.1f x %.1f flange."
                        % (ox, oy, fx, fy))
    if p.length < p.psu_size[2]:
        problems.append("Sleeve length %.1f is shorter than the %.1f mm PSU."
                        % (p.length, p.psu_size[2]))

    for x, y in p.hole_positions():
        if abs(x) + r > fx / 2.0 or abs(y) + r > fy / 2.0:
            problems.append("Mounting hole at (%.1f, %.1f) breaks out of the flange edge."
                            % (x, y))
        inside_x = abs(x) - p.nut_clearance < ox / 2.0
        inside_y = abs(y) - p.nut_clearance < oy / 2.0
        if inside_x and inside_y:
            problems.append(
                "Mounting hole at (%.1f, %.1f) is within %.1f mm of the sleeve (outside "
                "%.1f x %.1f), so there's no room for a nut or screw head."
                % (x, y, p.nut_clearance, ox, oy))

    if p.fan_side in ("+x", "-x"):
        rw = p.fan_window_dia / 2.0
        zc = p.fan_window_centre_z()
        if rw > iy / 2.0:
            problems.append("Fan window (%.0f mm) is taller than the %.1f mm inside wall."
                            % (p.fan_window_dia, iy))
        if zc - rw < p.flange_thickness or zc + rw > p.length:
            problems.append("Fan window Z=%.1f..%.1f runs into the flange or off the end."
                            % (zc - rw, zc + rw))

    if max(fx, fy) > p.bed_size:
        problems.append("Flange %.1f x %.1f does not fit the %.0f mm bed."
                        % (fx, fy, p.bed_size))
    if p.length > p.max_print_height:
        problems.append(
            "Sleeve is %.0f mm tall standing on its flange, more than the %.0f mm print "
            "height. Shorten it (it only needs >= %.0f for the PSU) or print it lying down "
            "with supports." % (p.length, p.max_print_height, p.psu_size[2]))
    return problems


def build_sleeve(p, name=None):
    """Build the sleeve (unlinked)."""
    e = ck.EPS
    ix, iy = p.inner()
    ox, oy = p.outer()
    fx, fy = p.flange_size
    t = p.flange_thickness

    obj = ck.box(name or PART_NAME, -fx / 2, fx / 2, -fy / 2, fy / 2, 0.0, t)
    ck.boolean(obj, ck.box("sleeve_body", -ox / 2, ox / 2, -oy / 2, oy / 2, 0.0, p.length),
               operation='UNION')
    ck.boolean(obj, ck.box("cutter_bore", -ix / 2, ix / 2, -iy / 2, iy / 2, -e, p.length + e))

    holes = [ck.cylinder("cutter_hole", x, y, -e, t + e, p.hole_dia, p.hole_segments)
             for x, y in p.hole_positions()]
    ck.boolean(obj, ck.join_meshes("cutter_holes", holes))

    if p.fan_side in ("+x", "-x"):
        sign = 1.0 if p.fan_side == "+x" else -1.0
        x0, x1 = sorted((0.0, sign * (ox / 2 + e)))
        window = ck.cylinder("cutter_fan_window", 0.0, p.fan_window_centre_z(), x0, x1,
                             p.fan_window_dia, p.fan_segments, axis='X')
        ck.boolean(obj, window)
    return obj


def build(params=None, variant="sleeve", segmented=False, export_dir=None,
          strict=False, scene=None):
    """Build the sleeve into the ``ATX_Case_Mods/PSU_Sleeve`` collection.

    ``segmented`` is accepted for a uniform API but the sleeve prints in one piece.
    """
    p = params or PSUSleeveParams()
    if variant not in VARIANTS:
        raise ValueError("variant must be one of %s, got %r" % (VARIANTS, variant))
    problems = validate(p)
    for msg in problems:
        print("[%s] WARNING: %s" % (PART_NAME, msg))
    if problems and strict:
        raise ValueError("Invalid %s parameters:\n  " % PART_NAME + "\n  ".join(problems))
    if segmented:
        print("[%s] note: the sleeve prints in one piece; 'segmented' ignored." % PART_NAME)

    ck.setup_scene_units(scene)
    coll = ck.part_collection(PART_NAME, scene)
    obj = build_sleeve(p)
    ck.link(obj, coll)
    if export_dir:
        ck.export_stl(obj, "%s/%s.stl" % (export_dir.rstrip("/"), obj.name))
    print("[%s] built 1 object." % PART_NAME)
    return [obj]
