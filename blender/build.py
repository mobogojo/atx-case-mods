"""Build parts headless or from Blender's Text Editor / Python console.

Command line:
    blender -b -P blender/build.py -- --part aio_360_bracket --variant all --segmented --export out/
    blender -b -P blender/build.py -- --list

Inside a running Blender (Text Editor, Python console or the Blender MCP bridge):
    import sys; sys.path.insert(0, "/path/to/atx-case-mods/blender")
    import build
    build.build_part("aio_360_bracket", variant="base", segmented=True)
"""

import argparse
import importlib
import os
import sys

BLENDER_DIR = os.path.dirname(os.path.abspath(__file__))
if BLENDER_DIR not in sys.path:
    sys.path.insert(0, BLENDER_DIR)


def reload_modules():
    """Pick up edits to casekit/parts without restarting Blender."""
    for name in sorted(sys.modules):
        if name == "casekit" or name.startswith("casekit.") \
                or name == "parts" or name.startswith("parts."):
            importlib.reload(sys.modules[name])


def build_part(part, variant=None, segmented=False, export_dir=None, strict=False, **overrides):
    """Build one part; ``variant`` may be a name, 'all' or None (first variant).

    Any keyword in ``overrides`` replaces the matching field of the part's params,
    e.g. ``build_part("aio_360_bracket", pocket_depth=6.5)``.
    """
    reload_modules()
    from parts import PARTS

    mod = PARTS[part]
    params = None
    if overrides:
        params_cls = next(v for k, v in vars(mod).items() if k.endswith("Params"))
        params = params_cls(**overrides)
    variants = mod.VARIANTS if variant == "all" else [variant or mod.VARIANTS[0]]
    objects = []
    for v in variants:
        objects += mod.build(params, variant=v, segmented=segmented,
                             export_dir=export_dir, strict=strict)
    return objects


def main(argv):
    ap = argparse.ArgumentParser(prog="build.py")
    ap.add_argument("--list", action="store_true", help="list parts and variants")
    ap.add_argument("--part", default="aio_360_bracket")
    ap.add_argument("--variant", default=None, help="variant name or 'all'")
    ap.add_argument("--segmented", action="store_true", help="split into printable segments")
    ap.add_argument("--export", default=None, metavar="DIR", help="write STL files here")
    ap.add_argument("--strict", action="store_true", help="fail on parameter warnings")
    ap.add_argument("--save", default=None, metavar="FILE.blend", help="save the .blend")
    args = ap.parse_args(argv)

    if args.list:
        from parts import PARTS
        for name, mod in PARTS.items():
            print("%s: variants %s" % (name, ", ".join(mod.VARIANTS)))
        return

    build_part(args.part, args.variant, args.segmented, args.export, args.strict)
    if args.save:
        import bpy
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.save))


def _launched_from_command_line():
    import bpy
    return bpy.app.background or "--" in sys.argv


# Only auto-run for `blender -b -P build.py -- ...`; `import build` just defines helpers.
if __name__ == "__main__" and _launched_from_command_line():
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
