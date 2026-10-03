"""Collapse AIH records into hospital stays. Invariant 1.

ICU days are billed per month, so a stay spanning months is split across a
primary AIH and continuation records (``IDENT = 5``). Counting records instead
of stays double-counts exactly the longest and sickest cases, which biases the
outcome in the direction that looks like a quality signal.

This is the single most dangerous step in the pipeline. The unit tests in
``tests/test_stays.py`` are not negotiable.
"""

from __future__ import annotations

import duckdb


def collapse_aih_chains(
    con: duckdb.DuckDBPyConnection,
    source_table: str,
    target_table: str,
) -> None:
    """Collapse ``source_table`` into one row per stay in ``target_table``.

    Grouping key is ``N_AIH``. Aggregation rules, per
    ``docs/02-methodology.md`` section 1:

    * ``icu_days``        -- sum of ``UTI_MES_TO``
    * ``length_of_stay``  -- sum of ``DIAS_PERM``
    * ``admitted_at``     -- min ``DT_INTER``
    * ``discharged_at``   -- max ``DT_SAIDA``
    * ``died``            -- from the record with max ``DT_SAIDA``
    * ``discharge_reason``-- from the record with max ``DT_SAIDA`` (``COBRANCA``)
    * everything else     -- from the record with min ``DT_INTER``

    Records may arrive out of order; do not assume row order.
    """
    raise NotImplementedError


def filter_icu(con: duckdb.DuckDBPyConnection, table: str) -> None:
    """Keep only stays with ``icu_days > 0``.

    ``UTI_INT_TO`` is intermediate care and is **not** ICU exposure.
    """
    raise NotImplementedError


def transferred_out(discharge_reason: int) -> bool:
    """True for ``COBRANCA`` 31 and 32.

    Per ``docs/decisions/0002-transfer-rule.md`` these stays count as survivors
    in v1, and the transfer-out rate is published as a context variable.
    """
    raise NotImplementedError
