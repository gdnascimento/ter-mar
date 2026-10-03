"""The four required sensitivity analyses.

Not optional extras: ``docs/02-methodology.md`` section 10 and the M6 acceptance
criteria. Results are published on the methodology page whatever they say.
"""

from __future__ import annotations

import polars as pl


def transfer_rule() -> pl.DataFrame:
    """Recompute every SMR three ways: transfers as survivors, excluded, as deaths.

    Reports how many municipalities change verdict across the three. If many do,
    the transfer rule is doing more work than the data and
    ``docs/decisions/0002-transfer-rule.md`` is reopened.
    """
    raise NotImplementedError


def private_coverage() -> pl.DataFrame:
    """Regress municipality SMR on ANS private-plan coverage.

    A strong association means the indicator substantially measures who uses
    SUS, not how well the ICU performs. Publish the coefficient whatever it is.
    """
    raise NotImplementedError


def window_stability() -> pl.DataFrame:
    """Fraction of above/below verdicts that persist into the next overlapping window.

    Flags that do not persist are noise, and the persistence rate is itself
    worth publishing.
    """
    raise NotImplementedError


def coding_discontinuity() -> pl.DataFrame:
    """Detect sudden shifts in case-mix composition per CNES.

    A hospital that starts recording secondary diagnoses more thoroughly shows
    an SMR improvement that is pure documentation. Affected municipalities are
    flagged, not scored.
    """
    raise NotImplementedError
