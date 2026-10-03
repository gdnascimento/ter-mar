"""Write ``site/data/municipios.json``. The main payload.

Contract: ``docs/03-data-contracts.md``. Schema: ``schemas/municipios.schema.json``.
"""

from __future__ import annotations

from pathlib import Path


def write(out_dir: Path) -> Path:
    """Emit one entry per municipality in scope.

    Hard rules, all schema-enforced:

    * sorted by ``code`` ascending, never by an outcome field (invariant 6)
    * every municipality appears exactly once, including suppressed ones --
      absence is not how suppression is expressed
    * ``suppressed`` implies ``smr``, ``smr_ci`` and ``p_value`` are ``null``
      and ``verdict`` is ``"insufficient"`` (invariant 3)
    * ``has_icu`` false implies the provider block is suppressed and
      ``icu_beds`` is 0
    * codes are 7-digit IBGE; the 6-digit SIH form never leaves the pipeline
    """
    raise NotImplementedError
