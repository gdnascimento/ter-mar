# Licence for the derived aggregates

The code in this repository is MIT licensed (`LICENSE`). The **derived
aggregates** — everything under `site/data/`, and any figure computed by this
pipeline — are licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Full legal text: https://creativecommons.org/licenses/by/4.0/legalcode

## Source data

The inputs are public Brazilian open data and are not covered by this licence:

- **SIH/SUS** (Sistema de Informações Hospitalares) — Ministério da Saúde / DATASUS
- **CNES** (Cadastro Nacional de Estabelecimentos de Saúde) — Ministério da Saúde / DATASUS
- **IBGE** — municipality codes, population estimates and territorial meshes
- **ANS** — private health plan coverage

## Attribution

Reuse of the aggregates must credit this project and name the DATASUS
extraction date, which is carried in `site/data/meta.json` as
`datasus_extracted_at`. DATASUS revises past competências, so a figure without
its extraction date is not reproducible and should not be cited.

Suggested form:

> ter-mar, derived from SIH/SUS (DATASUS), extracted YYYY-MM-DD. CC BY 4.0.

## What attribution does not license

CC BY permits redistribution and adaptation. It does not make a derived figure
correct in a context this project did not validate. In particular:

- These are **not** hospital quality rankings. The methodology
  (`docs/02-methodology.md`) is built to prevent that reading, and sorting the
  aggregates by standardised mortality ratio defeats it.
- A standardised mortality ratio published here is meaningless without its
  interval and its suppression status, both of which travel with it in the
  data. Republishing the point estimate alone misrepresents it.
- Municipalities below the suppression threshold carry `null`, not zero. Any
  reuse that treats `null` as a value is wrong.
