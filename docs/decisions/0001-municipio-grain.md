# 0001 — Publish at município grain

**Status:** provisional — confirm or reverse at milestone M4
**Date:** 2026-10-02

## Context

The product promise is that a person can look up their own município. But most
Brazilian municípios are small, ICU deaths are rare, and the suppression rule
(`E >= 5`) may exclude the large majority of them. If it does, a município-grain
page is mostly empty and the promise cannot be kept.

The alternative grain is **região de saúde**, which has three advantages: it
matches how ICU referral actually works, it aggregates enough events to produce
usable estimates, and it is the unit at which the relevant funding decisions are
made. Its disadvantage is that nobody knows which região de saúde they live in.

## Decision

Build at município grain. At M4, count how many municípios in the pilot state
clear the threshold and record the number here.

If the count is too low to be useful, pivot: the outcome view moves to região de
saúde, and the município page keeps the access metrics — ICU stays per 100k and
share treated outside — which do not depend on rare events and remain
meaningful at município grain. The search stays município-first either way,
because that is how people find themselves.

## Consequences

- The pivot must read as a design decision, not a retreat. Write it up as a
  finding about the limits of municipal-level inference on administrative data.
- Either way the access metrics survive, so M1–M3 are not wasted work.

## M4 result

<!-- Fill in at M4. Do not proceed to M5 until this is written. -->

- Municípios in scope:
- Clearing `E >= 5` (residence):
- Clearing `E >= 5` (provider):
- Decision:
