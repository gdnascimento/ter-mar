# 02 — Methodology

Normative. Implementations live in `pipeline/termar/model/`. Every function
named here exists as a pure function over arrays: it reads no files, touches no
database, and is unit-testable against hand-computed values.

---

## 1. Analytic unit

A **stay** is one collapsed `N_AIH` chain. Collapse rule
(`transform/stays.py::collapse_aih_chains`):

| Field | Rule across the chain |
| --- | --- |
| `N_AIH` | Group key |
| `icu_days` | Sum of `UTI_MES_TO` |
| `length_of_stay` | Sum of `DIAS_PERM` |
| `admitted_at` | Min `DT_INTER` |
| `discharged_at` | Max `DT_SAIDA` |
| `died` | From the record with the max `DT_SAIDA` |
| `discharge_reason` | From the record with the max `DT_SAIDA` (`COBRANCA`) |
| everything else | From the record with the min `DT_INTER` (the index admission) |

A stay enters the analysis when `icu_days > 0`. `UTI_INT_TO` (intermediate
care) is **not** ICU exposure.

---

## 2. Case-mix strata

The reference model conditions on these and nothing else. All are derived in
`transform/casemix.py`.

| Variable | Levels |
| --- | --- |
| `age_band` | `0`, `1-14`, `15-44`, `45-59`, `60-74`, `75+` (years, after `COD_IDADE` normalisation) |
| `sex` | `M`, `F` |
| `diagnosis_group` | ~20 clinically coherent groups mapped from `DIAG_PRINC`. The mapping table is `transform/sql/diagnosis_groups.csv` and is versioned |
| `admission_type` | elective / urgent, from `CAR_INT` |
| `icu_days_band` | `1`, `2-3`, `4-7`, `8-14`, `15+` |

Full cross product is 6 × 2 × 20 × 2 × 5 = 2,400 strata. Nationally this is
tractable; per state it is not, which is why **the reference model is always
fitted on the national pool**, never per state.

---

## 3. Reference model

Two implementations, same interface (`model/reference.py`).

**Stratified (default, milestone M3).** The expected death probability for a
stay is the national death rate in its stratum. Strata with fewer than 30
national stays collapse upward by dropping `icu_days_band`, then
`admission_type`. Transparent, no fitting, easy to audit.

**Logistic (milestone M5).** Logistic regression on the national pool: a
restricted cubic spline on age, plus sex, diagnosis group, admission type and
an ICU-days spline. More power, no empty strata, harder to explain.

Both must report:

- **c-statistic** — expect 0.75–0.80. Anything above 0.85 on this data is a
  sign of leakage, most likely a variable that encodes the outcome.
- **Calibration by decile of predicted risk** — the top decile matters most,
  because that is where regional hubs sit.

Both figures go into `meta.json` and onto the methodology page.

---

## 4. Standardisation

For município `i` in a given view and window (`model/standardise.py`):

```
O_i = number of deaths among that municipality's stays
E_i = sum of predicted death probabilities over the same stays
SMR_i = O_i / E_i
```

Indirect standardisation. `SMR = 1` means "as many deaths as the national
case-mix-matched reference would predict".

Residence and provider views are two separate aggregations of the same
stay-level table, keyed on `MUNIC_RES` and `MUNIC_MOV` respectively. Invariant 5.

---

## 5. Empirical-Bayes shrinkage

Poisson–gamma, Clayton & Kaldor (1987) moment estimators
(`model/shrinkage.py`).

Model: `O_i ~ Poisson(E_i * theta_i)`, `theta_i ~ Gamma(alpha, nu)` with mean
`alpha/nu` and variance `alpha/nu^2`.

Moment estimators, over all municípios in the view:

```
m   = sum(O) / sum(E)
Ebar = mean(E)
s2  = sum( E_i * (SMR_i - m)^2 ) / sum(E)  -  m / Ebar
alpha = m^2 / s2
nu    = m   / s2
```

If `s2 <= 0` there is no detectable extra-Poisson variation: clamp `s2` to a
small positive epsilon, record the fact in `meta.json`, and continue — do not
crash and do not silently skip shrinkage.

Posterior for `theta_i` is `Gamma(shape = O_i + alpha, rate = E_i + nu)`, so:

```
shrunk_smr_i = (O_i + alpha) / (E_i + nu)
ci_i = gamma.ppf([0.025, 0.975], a = O_i + alpha, scale = 1 / (E_i + nu))
```

**The shrunk value is what is published.** The raw SMR may be kept in
`data/out/` for diagnostics and never emitted to `site/data/`.

---

## 6. Funnel limits

Two different computations for two different jobs. Conflating them is a real
bug (`model/funnel.py`).

### Drawing the curves

Continuous, smooth, over a grid of expected deaths `E`. Gamma/chi-square form:

```
lower(E, alpha) = chi2.ppf(alpha/2,     2*E)     / (2*E)
upper(E, alpha) = chi2.ppf(1 - alpha/2, 2*E + 2) / (2*E)
```

Emitted as `site/data/funnel/{view}.json` so the browser does no statistics.
Grid: `E` from 0.5 to the view's maximum, geometrically spaced, ~120 points.

### Classifying one município

Exact two-sided Poisson tail probability on the integer count — never by
comparing a point to the smoothed curve, which produces discreteness artifacts
near small `E`:

```
p_i = min(1, 2 * min( poisson.cdf(O_i, E_i), poisson.sf(O_i - 1, E_i) ))
```

### Overdispersion

With thousands of units, extra-Poisson variation is close to certain, and
unadjusted limits will flag hundreds of municípios for structural reasons.

Variance-stabilised residuals, winsorised at the 10th and 90th percentiles
before the sum so that genuine outliers do not inflate the estimate:

```
y_i   = 2 * (sqrt(O_i) - sqrt(E_i))
y_w   = winsorise(y, 0.10, 0.90)
phi   = mean(y_w ** 2)
```

If `phi > 1`, inflate every limit's distance from 1 multiplicatively:

```
limit_adjusted = 1 + sqrt(phi) * (limit_raw - 1)
```

and divide the classification statistic by `sqrt(phi)` equivalently. `phi` is
published per view in `meta.json` and stated on the methodology page. The
additive random-effects alternative is deliberately not used in v1 — see
`docs/decisions/0004-overdispersion-adjustment.md`.

---

## 7. Suppression

```
suppressed = (E_i < 5.0) or (n_i < 30)
```

Thresholds live in `config.py` and are emitted in `meta.json`. When suppressed,
`smr` and `smr_ci` are `null` in the emitted JSON. Invariant 3.

This is simultaneously a statistical necessity and a small-cell disclosure
safeguard. Do not relax it to increase map coverage.

---

## 8. Verdict

Four values, in this order of precedence:

| Verdict | Condition | pt-BR label |
| --- | --- | --- |
| `insufficient` | suppressed | dados insuficientes para avaliar |
| `above` | `p_i < 0.002` and `SMR_i > 1` | acima do esperado |
| `below` | `p_i < 0.002` and `SMR_i < 1` | abaixo do esperado |
| `within` | otherwise | compatível com a média nacional |

The threshold is 0.002 (the 99.8% limit), not 0.05. With 5,570 municípios at
95% several hundred fall outside by chance; `meta.json` records the expected
false-flag count under the null so the page can state it.

---

## 9. Time windows

- Headline: three-year rolling windows, e.g. 2021–2023.
- Trend view: annual values, with visibly wider intervals, never used for the
  verdict.
- The window is a `config.py` setting and appears in `meta.json` and in the page
  header.

---

## 10. Required sensitivity analyses

Implemented in `validate/sensitivity.py`, run by `termar validate`, results
published on the methodology page. These are not optional extras — see
`docs/06-acceptance.md`.

1. **Transfer rule.** Recompute every SMR with transfers-out treated as
   survivors, excluded, and counted as deaths. Report how many municípios change
   verdict across the three.
2. **Private coverage confounding.** Regress município SMR on ANS coverage.
   Publish the coefficient whatever it is.
3. **Window stability.** Fraction of `above`/`below` verdicts that persist from
   one three-year window to the next overlapping one.
4. **Coding discontinuity.** Per CNES, detect sudden shifts in case-mix
   composition; flag affected municípios rather than scoring them.

---

## References

- Clayton, D. and Kaldor, J. (1987). Empirical Bayes estimates of
  age-standardized relative risks for use in disease mapping. *Biometrics*.
- Spiegelhalter, D. J. (2005). Funnel plots for comparing institutional
  performance. *Statistics in Medicine*.
