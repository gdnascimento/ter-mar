"""The 6 <-> 7 digit municipality code crosswalk."""

from __future__ import annotations

import pytest

pl = pytest.importorskip("polars")

from termar.transform import crosswalk  # noqa: E402


@pytest.fixture
def table():  # noqa: ANN201
    return crosswalk.build("2022")


def test_round_trip(table) -> None:  # noqa: ANN001
    """Every 6-digit code maps to exactly one 7-digit code."""
    assert table.select("code6").n_unique() == len(table)
    assert table.select("code7").n_unique() == len(table)


@pytest.mark.invariant
def test_unmapped_codes_are_reported_not_dropped(table) -> None:  # noqa: ANN001
    """A code absent from the crosswalk must surface, never vanish silently."""
    codes = pl.Series("code6", [520870, 999999])
    mapped = crosswalk.to_code7(codes, table)
    assert mapped[1] is None
    assert len(crosswalk.unmapped(codes, table)) == 1
