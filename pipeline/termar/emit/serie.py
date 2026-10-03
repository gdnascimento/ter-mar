"""Write ``site/data/serie/{UF}.json``: annual series for the trend view.

Milestone M9. Annual values carry visibly wider intervals and never drive a
verdict -- ``docs/02-methodology.md`` section 9.
"""

from __future__ import annotations

from pathlib import Path


def write(out_dir: Path, *, uf: str) -> Path:
    """Emit positional arrays aligned to ``years``, ``null`` where suppressed."""
    raise NotImplementedError
