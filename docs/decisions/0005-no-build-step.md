# 0005 — No frontend build step

**Status:** accepted
**Date:** 2026-10-02

## Context

The site is static files reading static JSON. A bundler and TypeScript would
give type checking across the JSON boundary, at the cost of a toolchain that
needs maintaining and that will rot.

This is a research artifact. It should still run in five years, from a clone,
with no `npm install`.

## Decision

Plain HTML and ES modules. Third-party code is vendored into `site/vendor/` and
committed — no CDN at runtime, no package manager.

Type safety across the JSON boundary comes from JSON Schema validation in the
pipeline (which fails the build) plus JSDoc typedefs in `site/js/types.js`.
Editors give useful checking from JSDoc without a compile step.

## Consequences

- No type errors caught at build time on the JS side. The schemas carry that
  weight, which is why `termar validate` is a required gate.
- `types.js` and `schemas/` must be changed together. This is stated in
  `docs/04-frontend.md` and checked at review.
- Vendored files are pinned with their version and source URL in
  `site/vendor/README.md`.
