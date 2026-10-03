"""Write ``site/data/malha/{UF}.topojson``.

Milestone M8. Simplify with ``mapshaper`` before emission:

    mapshaper in.json -simplify 1% -o format=topojson quantization=1e5 out.json

Any map renders suppressed municipalities in a distinct, labelled neutral fill
-- never on the same colour scale as a measured value
(``docs/decisions/0003-no-national-map-in-v1.md``).
"""

from __future__ import annotations

from pathlib import Path


def write(out_dir: Path, *, uf: str) -> Path:
    """Emit simplified municipality geometry for one UF."""
    raise NotImplementedError
