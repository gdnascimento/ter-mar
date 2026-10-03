# 0004 — Multiplicative overdispersion adjustment

**Status:** accepted
**Date:** 2026-10-02

## Context

Across thousands of units, extra-Poisson variation is close to certain.
Unadjusted funnel limits would flag hundreds of municípios as outliers for
structural reasons — referral patterns, coding practice, case-mix the model
cannot see.

Spiegelhalter (2005) gives two adjustments: a multiplicative inflation by
`sqrt(phi)`, and an additive random-effects term `tau^2`.

## Decision

Use the **multiplicative** adjustment in v1:

```
limit_adjusted = 1 + sqrt(phi) * (limit_raw - 1)
```

with `phi` from winsorised variance-stabilised residuals
(`docs/02-methodology.md` §6).

It is simple, standard, implementable in a dozen lines, and auditable. The
additive random-effects form is better behaved at very large `E`, but the
estimation is more delicate and the benefit does not apply to most municípios in
this dataset, which sit at small `E`.

## Consequences

- At very large `E` — a handful of big-city hubs — the multiplicative form is
  slightly conservative. Note it on the methodology page.
- `phi` is published per view so the adjustment is visible rather than hidden.
- If a reviewer at M6 objects, the additive form is a contained change inside
  `model/funnel.py`.
