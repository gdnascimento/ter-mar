"""Clayton-Kaldor empirical Bayes.

Property-based rather than oracle-based: the properties are what make the
published number defensible, and they do not go stale when the estimator is
refined.
"""

from __future__ import annotations

import numpy as np
import pytest

from termar.model import shrinkage


@pytest.fixture
def population():  # noqa: ANN201
    """A synthetic set spanning four orders of magnitude of expected counts."""
    rng = np.random.default_rng(20261002)
    expected = np.geomspace(0.5, 500.0, 400)
    theta = rng.gamma(shape=9.0, scale=1 / 9.0, size=expected.size)
    observed = rng.poisson(expected * theta).astype(np.int64)
    return observed, expected


def test_prior_recovers_a_known_gamma(population) -> None:  # noqa: ANN001
    observed, expected = population
    prior = shrinkage.estimate_prior(observed, expected)
    assert prior.alpha / prior.nu == pytest.approx(1.0, abs=0.15)
    assert not prior.s2_clamped


@pytest.mark.invariant
def test_shrinkage_pulls_toward_the_mean(population) -> None:  # noqa: ANN001
    """Every shrunk value sits between its raw SMR and the global mean."""
    observed, expected = population
    prior = shrinkage.estimate_prior(observed, expected)
    raw = observed / expected
    shrunk = shrinkage.shrink(observed, expected, prior)
    mean = observed.sum() / expected.sum()
    assert np.all((shrunk - mean) * (raw - mean) >= 0)
    assert np.all(np.abs(shrunk - mean) <= np.abs(raw - mean) + 1e-9)


@pytest.mark.invariant
def test_small_areas_shrink_more(population) -> None:  # noqa: ANN001
    """A municipality with 12 stays and 4 deaths must not render as a crisis."""
    observed, expected = population
    prior = shrinkage.estimate_prior(observed, expected)
    raw = observed / expected
    shrunk = shrinkage.shrink(observed, expected, prior)
    mean = observed.sum() / expected.sum()
    pull = np.abs(raw - mean) - np.abs(shrunk - mean)
    small, large = expected < 5, expected > 100
    assert pull[small].mean() > pull[large].mean()


def test_degenerate_variance_clamps_rather_than_crashing() -> None:
    """s2 <= 0 means no detectable extra-Poisson variation. Record it, continue."""
    expected = np.full(50, 20.0)
    observed = np.full(50, 20, dtype=np.int64)
    prior = shrinkage.estimate_prior(observed, expected)
    assert prior.s2_clamped
    assert prior.alpha > 0 and prior.nu > 0


@pytest.mark.invariant
def test_interval_always_accompanies_the_point(population) -> None:  # noqa: ANN001
    """Invariant 4: there is no code path producing a bare point estimate."""
    observed, expected = population
    prior = shrinkage.estimate_prior(observed, expected)
    lower, upper = shrinkage.credible_interval(observed, expected, prior)
    shrunk = shrinkage.shrink(observed, expected, prior)
    assert lower.shape == upper.shape == shrunk.shape
    assert np.all(lower <= shrunk) and np.all(shrunk <= upper)
    assert np.all((upper - lower)[expected < 5] > (upper - lower)[expected > 100].max())
