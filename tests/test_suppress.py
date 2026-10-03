"""Invariant 3, made mechanical."""

from __future__ import annotations

import numpy as np
import pytest

from termar.config import Suppression
from termar.model import suppress


@pytest.mark.invariant
def test_threshold_rule() -> None:
    rule = Suppression()
    mask = suppress.suppressed(
        expected=np.array([4.9, 5.0, 20.0, 100.0]),
        stays=np.array([400, 400, 29, 400], dtype=np.int64),
        rule=rule,
    )
    assert list(mask) == [True, False, True, False]


@pytest.mark.invariant
def test_thresholds_are_not_weakened() -> None:
    """A guard against the most tempting shortcut: lowering the bar to fill the map."""
    rule = Suppression()
    assert rule.min_expected_deaths >= 5.0
    assert rule.min_stays >= 30
