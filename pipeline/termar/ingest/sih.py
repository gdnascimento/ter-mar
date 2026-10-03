"""SIH/SUS RD (AIH reduzida) download.

``.dbc`` is a DATASUS-specific compressed ``.dbf``; pandas cannot read it.
PySUS bundles the blast-dbf decompression. See ``docs/01-data-sources.md``.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path


def download_rd(uf: str, year: int, month: int, *, force: bool = False) -> Path:
    """Download one RD competencia and write it as parquet.

    Returns the partition path. Skips the download when the partition exists and
    ``force`` is false -- raw files are written once and never silently
    overwritten.
    """
    raise NotImplementedError


def extraction_date() -> date:
    """The date this ingest run read DATASUS.

    DATASUS revises past competencias, so two runs months apart return different
    numbers. This date is stamped into ``meta.json`` and shown on the page.
    """
    raise NotImplementedError
