"""Registry of buildable parts.

Each part module exposes ``PART_NAME``, ``VARIANTS``, a params dataclass,
``validate(params)`` and ``build(params=None, variant=..., segmented=..., export_dir=...)``.
Add new parts (e.g. the ATX case top template) here so ``build.py`` can find them.
"""

from . import aio_360_bracket

PARTS = {
    "aio_360_bracket": aio_360_bracket,
}
