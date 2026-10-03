"""IBGE reference data: municipality codes, population, health regions, geometry."""

from __future__ import annotations

from pathlib import Path


def fetch_municipalities(vintage: str) -> Path:
    """Municipality table for a vintage: code7, name, UF, health region.

    Boundaries and codes change between vintages. The vintage is pinned in
    ``config.py`` and recorded in ``meta.json``.
    """
    raise NotImplementedError


def fetch_population(vintage: str) -> Path:
    """Population estimates per municipality, used as the per-100k denominator."""
    raise NotImplementedError


def fetch_malha(uf: str, *, quality: str = "minima") -> Path:
    """Municipality geometry for one UF from the IBGE malhas v3 API.

    Milestone M8. Simplify with ``mapshaper`` before it reaches ``site/data``;
    the raw national malha is tens of megabytes.
    """
    raise NotImplementedError
