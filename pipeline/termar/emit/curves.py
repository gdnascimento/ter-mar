"""Write ``site/data/funnel/{view}.json``: the control-limit curves.

Curves only. The points are derived in the browser from ``municipios.json`` so
that each number lives in exactly one place, and so the browser does no
statistics.
"""

from __future__ import annotations

from pathlib import Path


def write(out_dir: Path, *, view: str) -> Path:
    """Emit the 95% and 99.8% bands over the expected-count grid.

    Limits are already overdispersion-adjusted; ``phi`` is carried for display.
    ``lower`` and ``upper`` must each have the same length as ``expected_grid``
    -- a check JSON Schema cannot express, enforced in ``validate/schema.py``.
    """
    raise NotImplementedError
