"""Case-mix derivation, above all the age unit trap."""

from __future__ import annotations

import pytest

pl = pytest.importorskip("polars")

from termar.transform import casemix  # noqa: E402


@pytest.mark.invariant
@pytest.mark.parametrize(
    ("idade", "cod_idade", "years"),
    [
        (6, 2, 0.5),    # 6 months, not 6 years. The trap.
        (20, 1, 20 / 365.25),  # 20 days
        (61, 3, 61.0),  # 61 years
        (0, 2, 0.0),
    ],
)
def test_age_is_normalised_by_cod_idade(idade: int, cod_idade: int, years: float) -> None:
    frame = pl.DataFrame({"IDADE": [idade], "COD_IDADE": [cod_idade]})
    got = frame.select(
        casemix.normalise_age(pl.col("IDADE"), pl.col("COD_IDADE")).alias("years")
    )["years"][0]
    assert got == pytest.approx(years, rel=1e-3)


@pytest.mark.parametrize(
    ("age", "band"),
    [(0.5, "0"), (7, "1-14"), (30, "15-44"), (50, "45-59"), (68, "60-74"), (88, "75+")],
)
def test_age_bands(age: float, band: str) -> None:
    frame = pl.DataFrame({"age": [age]})
    assert frame.select(casemix.age_band(pl.col("age")).alias("b"))["b"][0] == band


@pytest.mark.parametrize(
    ("days", "band"), [(1, "1"), (3, "2-3"), (7, "4-7"), (14, "8-14"), (52, "15+")]
)
def test_icu_days_bands(days: int, band: str) -> None:
    frame = pl.DataFrame({"d": [days]})
    assert frame.select(casemix.icu_days_band(pl.col("d")).alias("b"))["b"][0] == band
