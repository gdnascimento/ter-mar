"""Cross-check aggregates against DATASUS TABNET.

M1 acceptance: raw row counts for at least three competencias must match. If
they do not, the ingest filter is wrong, and no amount of downstream care
recovers from that.
"""

from __future__ import annotations


def compare_counts(uf: str, year: int, month: int) -> dict[str, int]:
    """Return pipeline and TABNET counts for one competencia, plus the difference."""
    raise NotImplementedError
