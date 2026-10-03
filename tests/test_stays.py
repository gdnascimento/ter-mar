"""The AIH collapse. Invariant 1, and the step where this project most often
goes silently wrong.

Oracle: tests/fixtures/expected_stays.csv, computed by hand.
"""

from __future__ import annotations

import pytest

from termar.transform import stays as mod


def _by_aih(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["N_AIH"]: row for row in rows}


@pytest.fixture
def collapsed(aih_chains: list[dict[str, str]]):  # noqa: ANN201
    """Run the collapse over the fixture chains in an in-memory DuckDB."""
    duckdb = pytest.importorskip("duckdb")
    con = duckdb.connect()
    con.execute("CREATE TABLE raw AS SELECT * FROM (VALUES) t")  # replaced at M2
    mod.collapse_aih_chains(con, "raw", "stays")
    return con.execute("SELECT * FROM stays").fetchdf()


@pytest.mark.invariant
def test_one_row_per_chain(collapsed, aih_chains) -> None:  # noqa: ANN001
    """Stays are chains, not records. Counting records double-counts long stays."""
    assert len(collapsed) == len({row["N_AIH"] for row in aih_chains})


@pytest.mark.invariant
def test_icu_days_are_summed(collapsed, expected_stays) -> None:  # noqa: ANN001
    want = _by_aih(expected_stays)
    for _, got in collapsed.iterrows():
        assert got["icu_days"] == int(want[str(got["N_AIH"])]["icu_days"])


@pytest.mark.invariant
def test_total_icu_days_are_conserved(collapsed, aih_chains) -> None:  # noqa: ANN001
    """Sum over stays equals sum over raw records. Nothing is lost or duplicated."""
    assert collapsed["icu_days"].sum() == sum(int(r["UTI_MES_TO"]) for r in aih_chains)


@pytest.mark.invariant
def test_outcome_comes_from_the_last_record(collapsed, expected_stays) -> None:  # noqa: ANN001
    """Chain 1000000000002 dies on its continuation record, not its index record."""
    want = _by_aih(expected_stays)
    for _, got in collapsed.iterrows():
        row = want[str(got["N_AIH"])]
        assert int(got["died"]) == int(row["died"])
        assert int(got["discharge_reason"]) == int(row["discharge_reason"])


def test_record_order_in_the_file_does_not_matter(collapsed, expected_stays) -> None:  # noqa: ANN001
    """Chain 1000000000003 appears out of order in the fixture on purpose."""
    want = _by_aih(expected_stays)["1000000000003"]
    got = collapsed[collapsed["N_AIH"].astype(str) == "1000000000003"].iloc[0]
    assert str(got["admitted_at"])[:10] == want["admitted_at"]
    assert str(got["discharged_at"])[:10] == want["discharged_at"]


@pytest.mark.invariant
def test_non_icu_stays_are_excluded(collapsed) -> None:  # noqa: ANN001
    """UTI_INT_TO is intermediate care and is not ICU exposure."""
    assert (collapsed["icu_days"] > 0).all()


def test_transferred_out_is_detected() -> None:
    assert mod.transferred_out(31) is True
    assert mod.transferred_out(32) is True
    assert mod.transferred_out(41) is False
    assert mod.transferred_out(12) is False
