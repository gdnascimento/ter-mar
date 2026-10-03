# ter-mar

Comparação de desfechos em UTI entre municípios brasileiros, a partir de dados
abertos do SIH/SUS, publicada como página estática.

A page where a resident of any Brazilian município can see how ICU outcomes
compare against peer municípios, the health region, the state and a national
reference — with honest uncertainty, and without being turned into a hospital
league table.

## Status

Scaffold. No pipeline code written yet. See `docs/05-milestones.md`.

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

TODO: choose before first publication. Recommended: MIT for the code, CC BY 4.0
for the derived aggregates. The underlying DATASUS data is public.
