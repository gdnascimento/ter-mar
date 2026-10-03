# 0002 — Transferred-out stays count as survivors

**Status:** accepted — revisit after the M6 sensitivity analysis
**Date:** 2026-10-02

## Context

`COBRANCA` 31 and 32 mark transfer to another establishment. A patient moved out
and dying elsewhere is not recorded as a death at the first hospital. SIH has no
reliable patient identifier across AIHs, so the transfer cannot be followed.

This is informative censoring: transfer rates vary with regional network
structure, so establishments and municípios that transfer heavily look better
than they are.

Three possible treatments: count as survivor, exclude from both numerator and
denominator, or count as a death.

## Decision

**Count transferred-out stays as survivors** in both views.

It is the conservative and transparent choice, it keeps the denominator
interpretable, and it is what a reader assumes by default. Excluding them
changes the denominator in a way that varies by município and is harder to
explain; counting them as deaths is unjustifiable without evidence.

Two obligations come with it:

1. Publish the transfer-out rate per município as a context variable, so a
   reader can see where the bias is largest.
2. Run the three-way sensitivity analysis (`validate/sensitivity.py`) and report
   how many municípios change verdict across the treatments.

## Consequences

- Municípios with high transfer-out rates have systematically optimistic SMRs.
  They carry a visible flag on the page.
- If the sensitivity analysis shows many verdicts flipping, this decision is
  reopened and the indicator may need to be restricted to municípios below a
  transfer-rate threshold.
