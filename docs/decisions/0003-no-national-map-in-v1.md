# 0003 — No national map in version 1

**Status:** accepted
**Date:** 2026-10-02

## Context

The full-resolution IBGE malha for 5,570 municípios is tens of megabytes of
GeoJSON. Making a national map work on static hosting means either aggressive
simplification or vector tiles (PMTiles over HTTP range requests). Both are real
work.

A national choropleth is also the single most dangerous view in this project: it
renders noise as geography, and a reader takes a coloured map as a ranking far
more readily than they take a funnel plot as one.

## Decision

Version 1 ships with no national map. The funnel plot and the peer table carry
the argument. Per-state TopoJSON arrives at M8; national PMTiles only if the
national view turns out to be the product.

Any map that does ship renders suppressed municípios in a distinct, clearly
labelled neutral fill — never on the same colour scale as a measured value.

## Consequences

- Faster to a publishable v1, and the risky view is deferred until the
  methodology is validated.
- The site must be genuinely useful without a map. That is a design constraint
  on M5, not a limitation to apologise for.
