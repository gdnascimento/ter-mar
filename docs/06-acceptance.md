# 06 — Acceptance criteria

## Gates that apply to every change

1. `make lint` — `ruff check` and `ruff format --check` clean.
2. `make typecheck` — `mypy --strict` clean.
3. `make test` — all tests pass. **No invariant test is skipped, xfailed or
   weakened.**
4. Anything emitted to `site/data/` validates against `schemas/`.
5. Documentation changed in the same commit as the behaviour it describes.

---

## M1 — Ingest

- [ ] `termar ingest --uf GO --start 2021-01 --end 2023-12` completes from a
      clean `data/raw/`.
- [ ] Re-running it downloads nothing and changes no file.
- [ ] Partition layout matches `docs/01-data-sources.md`.
- [ ] Raw row counts for at least three competências match DATASUS TABNET.
      Record the comparison in the PR.
- [ ] The crosswalk maps every 6-digit SIH código appearing in the data to a
      7-digit IBGE código, or lists the unmapped ones explicitly. Silent drops
      fail this criterion.

## M2 — Transform

- [ ] `tests/test_stays.py` passes against the hand-built fixtures in
      `tests/fixtures/aih_chains.csv`, including: a single-record stay, a
      two-month continuation, a three-month continuation, a chain where the
      death is on the last record, and a chain where records are out of order.
- [ ] Collapsed stay count is strictly less than the raw record count, and the
      difference equals the number of `IDENT = 5` records.
- [ ] `sum(icu_days)` over stays equals `sum(UTI_MES_TO)` over raw records.
- [ ] No stay has `icu_days <= 0` in the analytic table.
- [ ] Age normalisation verified for `COD_IDADE` in days, months and years.
      A record with `IDADE=6, COD_IDADE=2` resolves to 0.5 years, not 6.

## M3 — Reference model

- [ ] c-statistic reported and between 0.70 and 0.85. Outside that range,
      investigate before proceeding — above 0.85 usually means outcome leakage.
- [ ] Calibration by decile of predicted risk plotted and reviewed; the top
      decile is not systematically off.
- [ ] `sum(expected_deaths)` over all stays equals `sum(observed_deaths)`
      nationally, to within floating-point tolerance. This is a property of
      indirect standardisation and is a hard check, not a soft one.
- [ ] Raw SMR vs E scatter inspected before any município is named.

## M4 — Shrinkage, funnel, suppression

- [ ] `tests/test_shrinkage.py` reproduces hand-computed Clayton–Kaldor
      estimates on a small synthetic set.
- [ ] Shrunk SMRs are closer to 1 than raw SMRs for every município, and the
      shrinkage is strictly larger for smaller `E`.
- [ ] `s2 <= 0` path is tested and clamps rather than crashing.
- [ ] `tests/test_funnel.py` checks the smooth curve and the exact Poisson
      classification agree in sign for `E > 20`, and documents where they
      diverge below it.
- [ ] `phi` computed, published, and greater than or equal to 1 in practice.
- [ ] **The gate:** number of municípios clearing `E >= 5` recorded in
      `docs/decisions/0001-municipio-grain.md`, with the continue-or-pivot
      decision written down.

## M5 — Emit and site

- [ ] Every emitted file validates against its schema.
- [ ] `validate/schema.py` additionally checks the array-length invariants that
      JSON Schema cannot express (funnel bands against `expected_grid`, series
      against `years`).
- [ ] A suppressed município in `municipios.json` has `smr`, `smr_ci` and
      `p_value` all `null` and `verdict: "insufficient"`. Verified by test, not
      by eye.
- [ ] `municipalities` is sorted by `code` ascending.
- [ ] No file under `site/data/` contains a CNES code, an `N_AIH`, or any
      row that corresponds to fewer than the minimum cell size.
- [ ] Page is usable with JavaScript errors visible in the console: zero errors
      on load and on selecting a município.
- [ ] Keyboard-only walkthrough completes: search, select, switch tabs, read the
      peer table.
- [ ] First view under 400 KB transferred, measured.
- [ ] One person from a small município used it unguided; what they misread is
      written down in the PR.

## M6 — Sensitivity and methodology page

- [ ] All four analyses in `docs/02-methodology.md` §10 implemented and run.
- [ ] Transfer-rule sensitivity reports how many municípios change verdict
      across the three treatments.
- [ ] The ANS coverage coefficient is published **whatever it says**.
- [ ] `metodologia.html` renders its figures from `meta.json` and the validation
      output, not from hard-coded numbers.
- [ ] The page states, in plain Portuguese, how many false flags are expected
      under the null.
- [ ] A health-services epidemiologist has read the methodology page.

**Nothing is published publicly before M6 passes.**

## M7 — National

- [ ] All 27 UFs ingest and transform.
- [ ] Reference model refitted on the national pool; c-statistic re-reported.
- [ ] Payload sizes re-measured against `docs/03-data-contracts.md`. If
      `municipios.json` exceeds 400 KB gzipped, the columnar fallback is adopted
      and `data.js` rehydrates.
