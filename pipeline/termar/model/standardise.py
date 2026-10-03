"""Indirect standardisation: observed, expected and the raw SMR.

The two views are two separate aggregations of the same stay-level table, keyed
on residence and on provider municipality. They are never merged (invariant 5).
"""

from __future__ import annotations

import numpy as np
import polars as pl
from numpy.typing import NDArray


def aggregate(stays: pl.DataFrame, *, view: str) -> pl.DataFrame:
    """Aggregate stays to municipality level for one view.

    ``view`` is ``"residence"`` (key ``MUNIC_RES``) or ``"provider"``
    (key ``MUNIC_MOV``). Returns ``code7``, ``stays``, ``observed_deaths``,
    ``expected_deaths``.
    """
    raise NotImplementedError


def smr(
    observed: NDArray[np.int64], expected: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Raw standardised mortality ratio, ``O / E``.

    Kept for diagnostics only. The published value is the shrunk estimate from
    :mod:`termar.model.shrinkage`.
    """
    raise NotImplementedError


def check_national_calibration(
    observed: NDArray[np.int64], expected: NDArray[np.float64], *, tolerance: float = 1e-6
) -> None:
    """Assert ``sum(expected) == sum(observed)`` nationally.

    This is a property of indirect standardisation, not a soft check. A failure
    means the reference model or the aggregation is wrong, and it must stop the
    run rather than warn.
    """
    raise NotImplementedError
