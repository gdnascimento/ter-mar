"""Funnel limits, overdispersion and verdict classification."""

from __future__ import annotations

import numpy as np
import pytest

from termar.model import funnel


@pytest.fixture
def grid() -> np.ndarray:
    return funnel.geometric_grid(500.0)


def test_limits_bracket_one_and_converge(grid) -> None:  # noqa: ANN001
    lower, upper = funnel.limit_curves(grid, alpha=0.05)
    assert np.all(lower < 1.0) and np.all(upper > 1.0)
    assert np.all(np.diff(upper) <= 1e-9)
    assert np.all(np.diff(lower) >= -1e-9)
    assert upper[-1] == pytest.approx(1.0, abs=0.3)


def test_tighter_level_gives_wider_limits(grid) -> None:  # noqa: ANN001
    _, upper95 = funnel.limit_curves(grid, alpha=0.05)
    _, upper998 = funnel.limit_curves(grid, alpha=0.002)
    assert np.all(upper998 >= upper95)


@pytest.mark.invariant
def test_classification_uses_exact_poisson_not_the_curve() -> None:
    """The smooth curve is for drawing. Classifying from it misfires at small E.

    At E below about 5 the discrete Poisson admits no observation that is
    significant at 0.002, so nothing there can ever be flagged.
    """
    expected = np.full(6, 3.0)
    observed = np.arange(6, dtype=np.int64)
    p = funnel.poisson_p_value(observed, expected)
    assert np.all((p >= 0) & (p <= 1))
    assert np.all(p > 0.002)


def test_phi_is_about_one_for_pure_poisson_data() -> None:
    rng = np.random.default_rng(7)
    expected = np.geomspace(1.0, 200.0, 2000)
    observed = rng.poisson(expected).astype(np.int64)
    assert funnel.overdispersion_phi(observed, expected) == pytest.approx(1.0, abs=0.2)


@pytest.mark.invariant
def test_phi_detects_extra_poisson_variation() -> None:
    """With thousands of units this is the realistic case, and unadjusted limits
    would flag hundreds of municipalities for structural reasons."""
    rng = np.random.default_rng(7)
    expected = np.geomspace(1.0, 200.0, 2000)
    theta = rng.gamma(shape=4.0, scale=0.25, size=expected.size)
    observed = rng.poisson(expected * theta).astype(np.int64)
    assert funnel.overdispersion_phi(observed, expected) > 1.2


def test_inflation_widens_symmetrically() -> None:
    limits = np.array([0.6, 1.4])
    got = funnel.inflate(limits, phi=4.0)
    assert got[0] == pytest.approx(1 - 2 * 0.4)
    assert got[1] == pytest.approx(1 + 2 * 0.4)


@pytest.mark.invariant
def test_suppression_wins_over_significance() -> None:
    """Verdict precedence: suppressed first, whatever the p-value says."""
    verdicts = funnel.classify(
        smr=np.array([3.0, 1.5, 0.4, 1.01]),
        p_value=np.array([0.0001, 0.0001, 0.0001, 0.9]),
        suppressed=np.array([True, False, False, False]),
        alpha=0.002,
    )
    assert verdicts == ["insufficient", "above", "below", "within"]
