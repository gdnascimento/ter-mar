# 03 — Data contracts

The pipeline writes these files into `site/data/`. The site reads them and
nothing else. Every file is validated against `schemas/*.json` by
`termar validate`, which **fails the build** on any violation.

JSON field names are English (`AGENTS.md`, Conventions). Portuguese appears only
in `site/js/labels.js`.

## Files

| Path | Schema | Loaded | Budget (gzipped) |
| --- | --- | --- | --- |
| `site/data/meta.json` | `meta.schema.json` | eagerly | < 5 KB |
| `site/data/busca.json` | `busca.schema.json` | eagerly | ~80 KB |
| `site/data/municipios.json` | `municipios.schema.json` | eagerly | 150–300 KB |
| `site/data/funnel/{view}.json` | `funnel.schema.json` | on first funnel render | ~10 KB each |
| `site/data/serie/{UF}.json` | `serie.schema.json` | when a trend view opens | 20–60 KB each |
| `site/data/malha/{UF}.topojson` | — | when a map opens (M6) | 100–400 KB each |

`view` is `residence` or `provider`. `UF` is the two-letter uppercase code.

**Budget rule.** If gzipped `municipios.json` exceeds 400 KB, switch to the
columnar form at the end of this document rather than dropping fields.

---

## `meta.json`

Every other file is meaningless without this one. The site displays
`datasus_extracted_at` and `window.label` in the header.

```json
{
  "schema": "meta/1.0.0",
  "model_version": "2026-10-02-stratified-v1",
  "generated_at": "2026-10-02T17:04:11Z",
  "datasus_extracted_at": "2026-09-28",
  "ibge_vintage": "2022",
  "window": { "start": "2021-01", "end": "2023-12", "label": "2021–2023" },
  "suppression": { "min_expected_deaths": 5.0, "min_stays": 30 },
  "verdict_alpha": 0.002,
  "reference_model": {
    "kind": "stratified",
    "c_statistic": 0.781,
    "strata_count": 1446,
    "collapsed_strata": 212
  },
  "views": {
    "residence": {
      "phi": 1.84,
      "prior": { "alpha": 12.4, "nu": 12.1, "s2_clamped": false },
      "municipalities_total": 5570,
      "municipalities_published": 1183,
      "expected_false_flags": 11.1
    },
    "provider": { "...": "same shape" }
  }
}
```

`expected_false_flags` = `municipalities_published * verdict_alpha`. The
methodology page states it in words.

---

## `municipios.json`

```json
{
  "schema": "municipios/1.0.0",
  "municipalities": [
    {
      "code": 5208707,
      "name": "Goiânia",
      "uf": "GO",
      "health_region": "52001",
      "population": 1437237,
      "residence": {
        "stays": 12840,
        "stays_per_100k": 893.4,
        "observed_deaths": 2611,
        "expected_deaths": 2498.7,
        "smr": 1.044,
        "smr_ci": [1.004, 1.085],
        "p_value": 0.031,
        "verdict": "within",
        "treated_outside_pct": 3.1,
        "suppressed": false
      },
      "provider": {
        "has_icu": true,
        "icu_beds": 612,
        "icu_beds_per_100k": 42.6,
        "stays": 21904,
        "observed_deaths": 4890,
        "expected_deaths": 4511.2,
        "smr": 1.084,
        "smr_ci": [1.054, 1.114],
        "p_value": 0.0004,
        "verdict": "above",
        "from_other_municipalities_pct": 41.3,
        "suppressed": false
      },
      "context": { "private_coverage_pct": 24.8 }
    }
  ]
}
```

### Rules the schema enforces

1. `code` is the **7-digit IBGE** code. The 6-digit SIH form never leaves the
   pipeline.
2. `verdict` is one of `within`, `above`, `below`, `insufficient`.
3. **`suppressed: true` implies `smr`, `smr_ci` and `p_value` are `null` and
   `verdict` is `"insufficient"`.** Enforced with `if`/`then`. This is
   invariant 3 made mechanical: a bug cannot produce a renderable suppressed
   estimate.
4. `has_icu: false` implies the provider block is suppressed and `icu_beds` is
   `0`. A município with no ICU still appears, with its residence view intact.
5. `municipalities` is sorted by `code` ascending. Never by any outcome field —
   invariant 6.
6. Every município in scope appears exactly once, including suppressed ones.
   Absence is not how suppression is expressed.

---

## `busca.json`

Flat and compact; the autocomplete index.

```json
{
  "schema": "busca/1.0.0",
  "fields": ["code", "name", "uf", "normalized"],
  "rows": [[5208707, "Goiânia", "GO", "goiania"]]
}
```

`normalized` is lowercase, accent-stripped, for matching. Precomputed in the
pipeline so the browser never normalises 5,570 strings on load.

---

## `funnel/{view}.json`

Curves only. The points are derived in the browser from `municipios.json` —
one number lives in one place.

```json
{
  "schema": "funnel/1.0.0",
  "view": "residence",
  "phi": 1.84,
  "expected_grid": [0.5, 0.54, 0.58],
  "limits": {
    "p95":  { "lower": [0.0, 0.0, 0.0], "upper": [7.38, 7.02, 6.70] },
    "p998": { "lower": [0.0, 0.0, 0.0], "upper": [13.4, 12.6, 11.9] }
  }
}
```

All four arrays have the same length as `expected_grid`. Limits are already
overdispersion-adjusted; `phi` is carried for display only.

---

## `serie/{UF}.json`

```json
{
  "schema": "serie/1.0.0",
  "uf": "GO",
  "years": [2015, 2016, 2017],
  "municipalities": [
    {
      "code": 5208707,
      "residence": {
        "smr":         [1.02, null, 1.07],
        "smr_ci_low":  [0.96, null, 1.01],
        "smr_ci_high": [1.09, null, 1.13],
        "stays":       [3912, 3740, 4102]
      },
      "provider": { "...": "same shape" }
    }
  ]
}
```

`null` at a position means suppressed in that year. Arrays are positional
against `years` and must be the same length. Annual values are never used for a
verdict — `docs/02-methodology.md` §9.

---

## Columnar fallback

Only if the budget rule above is hit. Same information, no per-row keys:

```json
{
  "schema": "municipios/2.0.0-columnar",
  "fields": ["code", "name", "uf", "health_region", "population",
             "res_stays", "res_smr", "res_ci_low", "res_ci_high", "res_verdict"],
  "rows": [[5208707, "Goiânia", "GO", "52001", 1437237,
            12840, 1.044, 1.004, 1.085, "within"]]
}
```

If adopted, `site/js/data.js` rehydrates into the object form at load so that
no other module knows which encoding is on disk.
