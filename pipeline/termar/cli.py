"""Typer entry point. The only way to run the pipeline.

Make targets and the CI workflow both call these commands, so there is exactly
one code path from a developer's shell to production.
"""

from __future__ import annotations

import typer

app = typer.Typer(help="ter-mar pipeline", no_args_is_help=True)


@app.command()
def ingest(
    uf: str = typer.Option(..., help="Two-letter UF code, uppercase."),
    start: str = typer.Option(..., help="First competencia, YYYY-MM."),
    end: str = typer.Option(..., help="Last competencia, YYYY-MM."),
    force: bool = typer.Option(False, help="Re-download partitions that already exist."),
) -> None:
    """Download SIH, CNES and IBGE sources into ``data/raw/`` as parquet.

    Idempotent: an existing partition is skipped unless ``--force``. Records the
    extraction date, which every emitted file carries.
    """
    raise NotImplementedError


@app.command()
def transform(uf: str = typer.Option(..., help="Two-letter UF code.")) -> None:
    """Crosswalk, collapse AIH chains into stays, filter to ICU, derive case-mix.

    The collapse is invariant 1 and the single most dangerous step in the
    pipeline. See ``docs/02-methodology.md`` section 1.
    """
    raise NotImplementedError


@app.command()
def model(
    start: str = typer.Option(None, help="Override the window start."),
    end: str = typer.Option(None, help="Override the window end."),
) -> None:
    """Fit the national reference model, standardise, shrink, compute limits.

    Produces ``data/out/municipality_metrics.parquet`` with both views.
    """
    raise NotImplementedError


@app.command()
def emit(out: str = typer.Option("site/data", help="Output directory.")) -> None:
    """Write the JSON contract files described in ``docs/03-data-contracts.md``."""
    raise NotImplementedError


@app.command()
def validate(out: str = typer.Option("site/data", help="Directory to validate.")) -> None:
    """Validate emitted files against ``schemas/`` and run the invariant checks.

    Fails the build on any violation. This is a required gate, not a report.
    """
    raise NotImplementedError


if __name__ == "__main__":
    app()
