# ter-mar

> ### Status: scaffold — no validated results
>
> This repository contains **no computed figures**. Nothing in it has been
> through the sensitivity analyses in `docs/06-acceptance.md`, and the site is
> not published.
>
> **Do not cite any number from this repository.** If it later produces output,
> that output is not a ranking of hospitals or of municípios, and reading it as
> one is a mistake the methodology is specifically designed to prevent — see
> `docs/02-methodology.md`.

Comparação de desfechos em UTI entre municípios brasileiros, a partir de dados
abertos do SIH/SUS, publicada como página estática.

A page where a resident of any Brazilian município can see how ICU outcomes
compare against peer municípios, the health region, the state and a national
reference — with honest uncertainty, and without being turned into a hospital
league table.

## Status

Milestone M0 complete: contracts, documentation and stubs. No pipeline code
written yet. Work order and the M4 decision gate: `docs/05-milestones.md`.

The pipeline workflow runs on manual dispatch only, and its deploy job is gated
behind the `PUBLISH_ENABLED` repository variable. Both stay closed until M6.

## Quick start

```
make setup
make ingest UF=GO START=2021-01 END=2023-12
make transform UF=GO
make model
make site
make serve
```

## How it works

A Python pipeline downloads SIH/SUS hospital admission records, collapses them
into hospital stays, fits a national case-mix reference model, and computes a
shrunk standardised mortality ratio per município for two separate views —
residents, and local hospitals. The results are written as small JSON files.
The site is plain HTML and ES modules reading those files. There is no server.

## Why it is built this way

Comparing raw ICU mortality between municípios produces nonsense: most
municípios are small, ICU deaths are rare, and regional hubs concentrate the
sickest patients of an entire region. Everything in `docs/02-methodology.md`
exists to stop that nonsense from being published with a map attached.

## Documentation

Start at `AGENTS.md` if you are an automated contributor, `docs/00-overview.md`
if you are a person.

## Licence

- **Code** — MIT, see `LICENSE`.
- **Derived aggregates** (anything under `site/data/`) — CC BY 4.0, see
  `LICENSE-DATA.md`.

The underlying SIH/SUS, CNES and IBGE data is public. Attribution requirements
for reuse of the aggregates are in `LICENSE-DATA.md`.
