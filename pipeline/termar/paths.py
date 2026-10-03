"""Every filesystem location used by the pipeline.

No path string is constructed anywhere else. This is what makes the layout in
``docs/01-data-sources.md`` enforceable rather than aspirational.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
OUT = DATA / "out"
SITE_DATA = ROOT / "site" / "data"
SCHEMAS = ROOT / "schemas"


def raw_sih(uf: str, year: int, month: int) -> Path:
    """Parquet for one SIH RD competencia, e.g. ``data/raw/sih/uf=GO/year=2021/month=01/``."""
    raise NotImplementedError


def raw_cnes(uf: str, year: int, month: int) -> Path:
    """Parquet for one CNES LT competencia."""
    raise NotImplementedError


def raw_ibge(vintage: str) -> Path:
    """Municipality reference table for a given IBGE vintage."""
    raise NotImplementedError


def interim_stays(uf: str) -> Path:
    """Collapsed stays for one UF -- one row per hospital stay."""
    raise NotImplementedError


def interim_casemix(uf: str) -> Path:
    """Stays with case-mix columns derived, ready for the reference model."""
    raise NotImplementedError


def out_metrics() -> Path:
    """Modelled municipality metrics, both views, all UFs."""
    raise NotImplementedError


def site_file(name: str) -> Path:
    """A file under ``site/data/``, e.g. ``municipios.json`` or ``funnel/residence.json``."""
    raise NotImplementedError


def schema(name: str) -> Path:
    """A JSON Schema under ``schemas/``, e.g. ``municipios.schema.json``."""
    raise NotImplementedError
