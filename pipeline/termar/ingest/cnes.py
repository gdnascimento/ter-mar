"""CNES establishment and bed downloads.

``LT`` carries beds by type, which is what separates "this municipality has no
ICU" from "this municipality has an ICU with poor outcomes".
"""

from __future__ import annotations

from pathlib import Path


def download_lt(uf: str, year: int, month: int, *, force: bool = False) -> Path:
    """Download one CNES LT competencia as parquet."""
    raise NotImplementedError


def icu_beds_by_municipality(uf: str, year: int, month: int) -> object:
    """ICU bed counts per municipality for one competencia.

    Returns a frame of ``(municipality_code_7, icu_beds)``. Establishment-level
    detail is used internally and never emitted (invariant 7).
    """
    raise NotImplementedError
