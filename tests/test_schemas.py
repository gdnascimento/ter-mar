"""The data contract itself. These tests run today, before any pipeline exists.

If the schemas do not reject the invalid fixtures, the invariants in AGENTS.md
are documentation rather than enforcement.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = Path(__file__).parent / "fixtures"


def _validator(name: str):  # noqa: ANN202
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    return cls(schema)


@pytest.mark.parametrize(
    "name",
    [
        "municipios.schema.json",
        "meta.schema.json",
        "busca.schema.json",
        "funnel.schema.json",
        "serie.schema.json",
    ],
)
def test_schema_is_itself_valid(name: str) -> None:
    _validator(name)


def test_valid_document_passes() -> None:
    doc = json.loads((FIXTURES / "municipios.valid.json").read_text(encoding="utf-8"))
    _validator("municipios.schema.json").validate(doc)


@pytest.mark.invariant
@pytest.mark.parametrize(
    ("fixture", "where", "why"),
    [
        ("municipios.invalid-suppressed-with-smr.json",
         "municipalities/0/provider",
         "invariant 3: a suppressed estimate must be null, never renderable"),
        ("municipios.invalid-no-icu-with-beds.json",
         "municipalities/0/provider/icu_beds",
         "a municipality with has_icu false cannot report beds"),
        ("municipios.invalid-code6.json",
         "municipalities/1/code",
         "6-digit SIH codes must never leave the pipeline"),
        ("municipios.invalid-extra-field.json",
         "municipalities/1/residence",
         "an unknown field -- here a rank -- must not slip through"),
    ],
)
def test_invalid_document_is_rejected(fixture: str, where: str, why: str) -> None:
    """Rejected, and rejected at the right place.

    Asserting only that validation raises would pass even when the schema
    rejects for an unrelated reason, which has happened once already and hid a
    structural bug in the conditionals.
    """
    doc = json.loads((FIXTURES / fixture).read_text(encoding="utf-8"))
    errors = sorted(_validator("municipios.schema.json").iter_errors(doc),
                    key=lambda e: len(list(e.path)))
    assert errors, why
    path = "/".join(str(part) for part in errors[-1].path)
    assert path.startswith(where), f"rejected at {path}, expected {where}: {why}"
