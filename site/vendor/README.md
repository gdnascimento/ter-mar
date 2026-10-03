# Vendored third-party modules

No CDN at runtime, no package manager
(`docs/decisions/0005-no-build-step.md`). Files here are committed, and each one
is listed below with its version, source URL and licence.

Add a row when you add a file. A file with no row fails review.

| File | Version | Source | Licence |
| --- | --- | --- | --- |
| _(none yet)_ | | | |

Expected at M5: the d3 submodules the funnel plot needs — `d3-scale`,
`d3-shape`, `d3-selection`, `d3-axis`. Vendor the individual modules, not the
full `d3` bundle.
