# 05 — Milestones

Work in order. Each milestone has acceptance criteria in `docs/06-acceptance.md`
and is a reviewable unit. Do not start a milestone before the previous one
passes its criteria.

`UF=GO` throughout the single-state phase. Goiás is mid-size with a clear
hub-and-periphery structure. Avoid São Paulo for a first pass (too big to
iterate on) and the smallest states (too few events to see the shape).

---

## M0 — Scaffold ✅

Repository structure, docs, schemas, stubs, CI skeleton. Done.

## M1 — Ingest one state

`termar ingest --uf GO --start 2021-01 --end 2023-12`

SIH `RD` and CNES `LT` to `data/raw/` as parquet, partitioned. IBGE município
table and the 6↔7 digit crosswalk. Idempotent: an existing partition is never
silently overwritten.

## M2 — Transform

`termar transform --uf GO`

Crosswalk, AIH chain collapse, ICU filter, case-mix derivation. Produces
`data/interim/casemix/uf=GO/*.parquet`, one row per stay.

**This is where the project most often goes silently wrong.** The collapse unit
tests are not negotiable.

## M3 — Reference model and standardisation

`termar model`

Stratified national reference model, per-stay expected probabilities, O / E /
raw SMR per município for both views. Produces
`data/out/municipality_metrics.parquet`.

Report the c-statistic and calibration by decile. Plot raw SMR against E and
look at the scatter **before** looking at any município names.

## M4 — Shrinkage, funnel, suppression — DECISION GATE

Clayton–Kaldor prior, shrunk SMR with credible intervals, overdispersion `phi`,
funnel limits, suppression, verdicts.

Then count: **how many municípios in GO clear `E >= 5`?**

- **Enough to make a map meaningful** → continue to M5 as planned.
- **Very few** → stop and reconsider. The project moves to região de saúde
  grain, with município-level access metrics layered on top. This is not a
  failure; it is a publishable finding about the limits of municipal-level
  inference on administrative health data. See
  `docs/decisions/0001-municipio-grain.md`.

Record the count and the decision in that decision document before proceeding.

## M5 — Emit and the site shell

`termar emit && termar validate`, then `site/` for one state: search, stat
tiles, funnel plot, peer table. No map, no trend view.

Deploy to GitHub Pages. Watch one person who lives in a small município use it
without guidance, and write down what they misread.

## M6 — Sensitivity analyses and the methodology page

All four analyses in `docs/02-methodology.md` §10, with results rendered into
`metodologia.html` from `meta.json` and the validation output.

Nothing is published publicly before this milestone passes.

## M7 — National scale-out

All 27 UFs. Re-fit the reference model on the national pool. Re-measure payload
sizes against the budgets in `docs/03-data-contracts.md`.

## M8 — Maps

Per-state TopoJSON via `mapshaper`. National PMTiles only if the national view
turns out to be the product — `docs/decisions/0003-no-national-map-in-v1.md`.

## M9 — Trend view

Annual series, wider intervals, never driving a verdict.

---

## Out of scope until explicitly reopened

CNES establishment-level publication, individual-level record linkage, SIM
integration, any ranking feature, any single composite score.
