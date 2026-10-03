# AGENTS.md — operating contract

**ter-mar** compares ICU (UTI) outcomes across Brazilian municípios using open
SIH/SUS data, and publishes the result as a fully static web page. There is no
backend: a Python pipeline precomputes everything into JSON, and the site reads
those files.

This is a research artifact, not a dashboard. The statistical correctness of the
output matters more than the number of features in it.

---

## Read before writing code

| File | What it settles |
| --- | --- |
| `docs/00-overview.md` | What the project is and the two views it publishes |
| `docs/01-data-sources.md` | Every dataset, every field, every known gotcha |
| `docs/02-methodology.md` | The statistics. The hardest and most important document here |
| `docs/03-data-contracts.md` | The exact JSON the pipeline emits and the site consumes |
| `docs/04-frontend.md` | Page structure, copy rules, pt-BR label glossary |
| `docs/05-milestones.md` | Work order. Do not skip ahead |
| `docs/06-acceptance.md` | What "done" means for each milestone |
| `docs/decisions/` | Decisions already made, with the reasoning. Do not silently reverse one |

If a task seems to contradict one of these documents, the document wins. Raise
the contradiction rather than resolving it yourself.

---

## The seven invariants

These are not style preferences. Each one, violated, turns the output from
research into misinformation. They are enforced by tests marked `invariant` in
`tests/`. **Never skip, xfail or weaken an invariant test.**

1. **Collapse before counting.** One hospital stay is one collapsed `N_AIH`
   chain, never one AIH record. Continuation records (`IDENT = 5`) split a long
   stay across billing months; counting records double-counts exactly the
   sickest patients.

2. **Never publish an unstandardised rate as the headline.** The comparable
   number is the standardised mortality ratio against the national reference
   model. A crude percentage may appear as supporting detail, never as the
   verdict.

3. **Suppress below threshold.** No SMR is emitted when expected deaths
   `E < 5.0` or stays `n < 30`. When suppressed, the emitted `smr` and `smr_ci`
   fields are `null` — not a number, not omitted, not zero. The frontend must be
   structurally unable to render a suppressed estimate.

4. **The interval travels with the point.** Any function, JSON field or UI
   component that carries an SMR carries its interval in the same structure.
   There is no code path that produces a bare point estimate.

5. **The two views never merge.** Residence (`MUNIC_RES`) and provider
   (`MUNIC_MOV`) are computed end to end as separate pipelines over separate
   aggregations. No composite score, no averaging of the two, no single
   "rating" per município.

6. **Nothing is sorted by outcome.** No emitted artifact is ordered by SMR, and
   no UI element ranks municípios by it. Sort by name or by code. This is what
   keeps the output from being read as a league table.

7. **No stay-level data leaves the pipeline.** `site/data/` contains
   aggregates only. Anything with a patient, an admission or a single CNES
   establishment stays in `data/`, which is gitignored.

---

## Repo map

```
pipeline/termar/
  config.py        Window, thresholds, paths, model version — the single source of settings
  paths.py         Every filesystem location. Never hard-code a path anywhere else
  cli.py           Typer app. The only entry point; Make and CI both call it
  ingest/          DATASUS, CNES and IBGE downloads into data/raw/ as parquet
  transform/       Crosswalk, AIH collapse, case-mix derivation. DuckDB over parquet
  model/           Reference model, standardisation, shrinkage, funnel limits
  emit/            data/out/ -> site/data/*.json, validated against schemas/
  validate/        TABNET cross-checks, sensitivity analyses, schema validation
schemas/           JSON Schema files. The contract between pipeline and site
site/              Plain HTML + ES modules. No build step, no bundler, no framework
tests/             pytest. Invariant tests are the ones that matter
docs/              Specifications. Treated as normative
data/              Raw, interim and output data. Gitignored
```

---

## Commands

```
make setup       # uv sync --all-groups
make ingest UF=GO START=2021-01 END=2023-12
make transform UF=GO
make model
make site        # emit + validate
make serve       # http://localhost:8000
make test lint typecheck
```

Everything runs through `uv run termar <command>`. If you need a new operation,
add a CLI command — do not add a loose script.

---

## Conventions

- **Code, identifiers, comments, docstrings, commit messages, JSON field names:
  English.** No exceptions, including for domain terms that are Portuguese in
  the source data — keep `MUNIC_RES` as the SIH column name, but call the
  concept `residence_municipality`.
- **User-visible strings: Brazilian Portuguese.** They live in
  `site/js/labels.js` and nowhere else. Never inline a Portuguese string in a
  component.
- Python 3.12, fully type-annotated, `mypy --strict` clean.
- `ruff` for lint and format. Line length 100.
- Pure functions in `model/`: they take arrays and return arrays, read no files
  and know nothing about DuckDB. This is what makes them testable.
- SQL that is more than a few lines lives in `transform/sql/*.sql`, not in a
  Python string.
- No emoji, anywhere, including commit messages.

---

## Definition of done, for any module

1. `mypy --strict` and `ruff check` pass.
2. Tests exist and pass, including every invariant test that touches the module.
3. The module's behaviour matches `docs/` — and where it cannot, `docs/` has
   been updated in the same change with the reason.
4. If it emits JSON, the output validates against its schema in `schemas/`.
5. No new path string outside `paths.py`, no new threshold outside `config.py`.

---

## Traps that have already been identified

- **6 vs 7 digit município codes.** SIH uses 6 digits (IBGE minus the check
  digit). Join through `transform/crosswalk.py` only. Never join on name.
- **`.dbc` is not `.dbf`.** It is a DATASUS-specific compressed format. PySUS
  handles it; `pandas.read_*` does not.
- **DATASUS revises past competências.** Two runs a month apart give different
  numbers. `meta.json` carries the extraction date and the site displays it.
- **Transfers censor the outcome.** `COBRANCA` 31/32 mean transfer out. The rule
  chosen is in `docs/decisions/0002-transfer-rule.md`; the sensitivity analysis
  that justifies it is in `validate/sensitivity.py` and is not optional.
- **Regional hubs absorb the sickest patients of their whole region.** Their raw
  mortality is higher for reasons unrelated to quality. This is what case-mix
  adjustment is for, and it only partly succeeds — see `docs/02-methodology.md`.
- **Municipal grain may be too fine.** If very few municípios clear the
  suppression threshold, that is a finding, not a bug. See milestone M4 in
  `docs/05-milestones.md` for the pivot.

---

## When you are blocked

Stop and say so. Specifically do not:

- weaken a suppression threshold to make more municípios appear
- substitute a crude rate for an SMR because the model is not ready
- mark an invariant test `xfail` to get a green run
- invent a plausible number for a figure you could not compute

Any of those produces a page that looks finished and is wrong, which is worse
than an unfinished page.
