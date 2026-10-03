"""Validate emitted files. A required gate, not a report.

Two layers: JSON Schema, then the structural invariants JSON Schema cannot
express.
"""

from __future__ import annotations

from pathlib import Path


def validate_all(out_dir: Path) -> list[str]:
    """Validate every file in ``out_dir``. Returns violations; empty means pass.

    Beyond the schemas, checks:

    * funnel ``lower``/``upper`` lengths match ``expected_grid``
    * series arrays match the length of ``years``
    * ``municipalities`` is sorted by ``code`` ascending (invariant 6)
    * every municipality in ``busca.json`` exists in ``municipios.json``
    * no emitted file contains a CNES code or an ``N_AIH`` (invariant 7)
    * published counts in ``meta.json`` match what was actually emitted
    """
    raise NotImplementedError
