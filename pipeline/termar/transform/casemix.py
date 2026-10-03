"""Derive the case-mix variables the reference model conditions on.

The full set is in ``docs/02-methodology.md`` section 2: age band, sex,
diagnosis group, admission type, ICU-days band. Nothing else enters the model.
"""

from __future__ import annotations

import polars as pl


def normalise_age(idade: pl.Expr, cod_idade: pl.Expr) -> pl.Expr:
    """Convert SIH age to years.

    ``COD_IDADE`` gives the unit -- days, months or years. Ignoring it turns an
    infant recorded as ``IDADE=6, COD_IDADE=2`` into a six-year-old and silently
    corrupts paediatric ICU case-mix.
    """
    raise NotImplementedError


def age_band(age_years: pl.Expr) -> pl.Expr:
    """Bucket to ``0``, ``1-14``, ``15-44``, ``45-59``, ``60-74``, ``75+``."""
    raise NotImplementedError


def icu_days_band(icu_days: pl.Expr) -> pl.Expr:
    """Bucket to ``1``, ``2-3``, ``4-7``, ``8-14``, ``15+``."""
    raise NotImplementedError


def diagnosis_group(diag_princ: pl.Expr) -> pl.Expr:
    """Map a primary ICD-10 code to one of roughly twenty clinical groups.

    The mapping lives in ``transform/sql/diagnosis_groups.csv`` and is versioned
    with the model: changing it changes every expected count, so bump
    ``Settings.model_version`` in the same commit.
    """
    raise NotImplementedError


def derive(stays: pl.DataFrame) -> pl.DataFrame:
    """Add every case-mix column to a stays frame."""
    raise NotImplementedError
