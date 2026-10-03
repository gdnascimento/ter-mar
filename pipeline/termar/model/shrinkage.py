"""Poisson-gamma empirical Bayes, Clayton & Kaldor (1987) moment estimators.

Without shrinkage a municipality with 12 stays and 4 deaths renders as a
public-health crisis. Formulas: ``docs/02-methodology.md`` section 5.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class GammaPrior:
    """Prior on the relative risk, ``theta ~ Gamma(alpha, nu)``."""

    alpha: float
    nu: float
    s2_clamped: bool
    """True when the moment estimate of ``s2`` was non-positive and was clamped.

    That means no detectable extra-Poisson variation. Record it in ``meta.json``
    and continue -- do not crash, and do not silently skip shrinkage.
    """


def estimate_prior(
    observed: NDArray[np.int64], expected: NDArray[np.float64]
) -> GammaPrior:
    """Clayton-Kaldor moment estimators over all municipalities in a view.

    ``m = sum(O)/sum(E)``; ``s2 = sum(E*(SMR-m)**2)/sum(E) - m/mean(E)``;
    ``alpha = m**2/s2``; ``nu = m/s2``.
    """
    raise NotImplementedError


def shrink(
    observed: NDArray[np.int64], expected: NDArray[np.float64], prior: GammaPrior
) -> NDArray[np.float64]:
    """Posterior mean, ``(O + alpha) / (E + nu)``. This is the published value."""
    raise NotImplementedError


def credible_interval(
    observed: NDArray[np.int64],
    expected: NDArray[np.float64],
    prior: GammaPrior,
    *,
    level: float = 0.95,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Gamma posterior quantiles: ``Gamma(shape=O+alpha, rate=E+nu)``.

    Returns ``(lower, upper)``. The interval travels with the point estimate
    everywhere downstream (invariant 4); there is no code path that returns one
    without the other.
    """
    raise NotImplementedError
