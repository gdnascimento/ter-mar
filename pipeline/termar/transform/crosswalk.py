"""The 6 <-> 7 digit municipality code crosswalk.

SIH uses the 6-digit IBGE code (the 7-digit code without its check digit).
Everything joins through here. Never join on municipality name -- dozens repeat
across states.
"""

from __future__ import annotations

import polars as pl


def build(vintage: str) -> pl.DataFrame:
    """Build the crosswalk for an IBGE vintage.

    Columns: ``code6``, ``code7``, ``name``, ``uf``, ``health_region``.
    """
    raise NotImplementedError


def to_code7(codes6: pl.Series, crosswalk: pl.DataFrame) -> pl.Series:
    """Map 6-digit SIH codes to 7-digit IBGE codes.

    Unmapped codes are **not** silently dropped: they are returned as null and
    reported by :func:`unmapped`, which fails the M1 acceptance criteria if
    non-empty and unexplained.
    """
    raise NotImplementedError


def unmapped(codes6: pl.Series, crosswalk: pl.DataFrame) -> pl.DataFrame:
    """Distinct 6-digit codes present in the data but absent from the crosswalk."""
    raise NotImplementedError
