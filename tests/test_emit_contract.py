"""Emitted files against the contract. Runs only once something was emitted."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / "site" / "data"


pytestmark = pytest.mark.skipif(
    not (SITE_DATA / "municipios.json").exists(),
    reason="nothing emitted yet; run `make emit` first",
)


def _load(name: str) -> dict:
    return json.loads((SITE_DATA / name).read_text(encoding="utf-8"))


@pytest.mark.invariant
def test_sorted_by_code_never_by_outcome() -> None:
    """Invariant 6. Sorting by SMR is how a research page becomes a league table."""
    codes = [m["code"] for m in _load("municipios.json")["municipalities"]]
    assert codes == sorted(codes)


@pytest.mark.invariant
def test_suppressed_entries_are_null_not_zero() -> None:
    for m in _load("municipios.json")["municipalities"]:
        for view in ("residence", "provider"):
            block = m[view]
            if block["suppressed"]:
                assert block["smr"] is None
                assert block["smr_ci"] is None
                assert block["p_value"] is None
                assert block["verdict"] == "insufficient"


@pytest.mark.invariant
def test_every_municipality_appears_exactly_once() -> None:
    """Absence is not how suppression is expressed."""
    codes = [m["code"] for m in _load("municipios.json")["municipalities"]]
    assert len(codes) == len(set(codes))


@pytest.mark.invariant
def test_no_record_level_identifiers_leak() -> None:
    """Invariant 7: site/data carries aggregates only."""
    forbidden = ("N_AIH", "CNES", "cnes", "n_aih")
    for path in SITE_DATA.rglob("*.json"):
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text, f"{path.name} contains {token}"


def test_funnel_arrays_line_up() -> None:
    """A length check JSON Schema cannot express."""
    for view in ("residence", "provider"):
        doc = _load(f"funnel/{view}.json")
        n = len(doc["expected_grid"])
        for band in doc["limits"].values():
            assert len(band["lower"]) == n
            assert len(band["upper"]) == n
