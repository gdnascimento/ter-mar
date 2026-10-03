"""Indirect standardisation properties."""

from __future__ import annotations

import numpy as np
import pytest

from termar.model import standardise


@pytest.mark.invariant
def test_national_calibration_is_a_hard_check() -> None:
    """sum(E) == sum(O) nationally is a property of indirect standardisation.

    A mismatch means the reference model or the aggregation is wrong, and it
    must stop the run rather than warn.
    """
    observed = np.array([10, 20, 30], dtype=np.int64)
    standardise.check_national_calibration(observed, np.array([10.0, 20.0, 30.0]))
    with pytest.raises(Exception):  # noqa: B017 - the stub decides the type
        standardise.check_national_calibration(observed, np.array([5.0, 20.0, 30.0]))


def test_smr_is_the_ratio() -> None:
    got = standardise.smr(np.array([12, 0], dtype=np.int64), np.array([10.0, 4.0]))
    assert got[0] == pytest.approx(1.2)
    assert got[1] == pytest.approx(0.0)


@pytest.mark.invariant
def test_views_are_aggregated_separately() -> None:
    """Residence and provider are different keys over the same stays, never merged."""
    pl = pytest.importorskip("polars")
    stays = pl.DataFrame(
        {
            "MUNIC_RES": [5200050, 5200050, 5208707],
            "MUNIC_MOV": [5208707, 5208707, 5208707],
            "died": [1, 0, 0],
            "predicted": [0.4, 0.3, 0.2],
        }
    )
    residence = standardise.aggregate(stays, view="residence")
    provider = standardise.aggregate(stays, view="provider")
    assert len(residence) == 2
    assert len(provider) == 1
