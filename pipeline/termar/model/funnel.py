"""Funnel limits and verdict classification.

Two different computations for two different jobs, and conflating them is a real
bug: smooth curves for drawing, exact Poisson tails for classifying. See
``docs/02-methodology.md`` section 6.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def geometric_grid(
    max_expected: float, *, start: float = 0.5, n: int = 120
) -> NDArray[np.float64]:
    """Geometrically spaced grid of expected counts for drawing the curves."""
    raise NotImplementedError


def limit_curves(
    expected_grid: NDArray[np.float64], *, alpha: float
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Smooth control limits on the SMR scale, for drawing only.

    ``lower = chi2.ppf(alpha/2, 2E) / (2E)``;
    ``upper = chi2.ppf(1 - alpha/2, 2E + 2) / (2E)``.

    Never classify a municipality by comparing its point to these curves --
    the continuity smoothing produces artifacts at small ``E``.
    """
    raise NotImplementedError


def poisson_p_value(
    observed: NDArray[np.int64], expected: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Exact two-sided Poisson tail probability, for classification.

    ``p = min(1, 2 * min(cdf(O, E), sf(O - 1, E)))``.
    """
    raise NotImplementedError


def overdispersion_phi(
    observed: NDArray[np.int64],
    expected: NDArray[np.float64],
    *,
    winsorise: tuple[float, float] = (0.10, 0.90),
) -> float:
    """Winsorised variance-stabilised overdispersion factor.

    ``y = 2*(sqrt(O) - sqrt(E))``, winsorised at the given quantiles so genuine
    outliers do not inflate the estimate, then ``phi = mean(y**2)``.

    With thousands of units ``phi > 1`` is close to certain. Unadjusted limits
    would flag hundreds of municipalities for structural reasons.
    """
    raise NotImplementedError


def inflate(limits: NDArray[np.float64], phi: float) -> NDArray[np.float64]:
    """Multiplicative adjustment, ``1 + sqrt(phi) * (limit - 1)``.

    See ``docs/decisions/0004-overdispersion-adjustment.md`` for why the
    multiplicative form rather than additive random effects.
    """
    raise NotImplementedError


def classify(
    smr: NDArray[np.float64],
    p_value: NDArray[np.float64],
    suppressed: NDArray[np.bool_],
    *,
    alpha: float,
) -> list[str]:
    """Verdict per municipality: ``insufficient``, ``above``, ``below`` or ``within``.

    Precedence: suppression first, then the two-sided test at ``alpha`` (0.002,
    the 99.8% limit, not 0.05), then ``within``.
    """
    raise NotImplementedError
