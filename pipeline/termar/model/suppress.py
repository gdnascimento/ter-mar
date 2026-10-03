"""The suppression rule. Invariant 3.

A statistical necessity and a small-cell disclosure safeguard at the same time.
Do not relax either threshold to increase map coverage.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from termar.config import Suppression


def suppressed(
    expected: NDArray[np.float64],
    stays: NDArray[np.int64],
    rule: Suppression,
) -> NDArray[np.bool_]:
    """True where ``E < min_expected_deaths`` or ``n < min_stays``."""
    raise NotImplementedError


def blank_suppressed(frame: object, mask: NDArray[np.bool_]) -> object:
    """Set ``smr``, ``smr_ci`` and ``p_value`` to null where suppressed.

    Applied once, immediately before emission, so that no downstream code can
    read a suppressed estimate. Emitting ``0`` or omitting the field instead of
    ``null`` violates the contract in ``docs/03-data-contracts.md``.
    """
    raise NotImplementedError
