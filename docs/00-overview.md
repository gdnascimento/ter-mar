# 00 — Overview

## The question the page answers

A person opens the page, types their município, and learns two things that are
currently not available anywhere in one place:

1. **Do residents of this município reach intensive care, and how do they fare
   once they do?** — the *residence view*, keyed on `MUNIC_RES`.
2. **How do the ICUs physically located here perform?** — the *provider view*,
   keyed on `MUNIC_MOV`.

These are different questions with different answers. A município with no ICU
beds has a residence view and no provider view. A regional hub has a provider
view dominated by patients who live somewhere else.

## What the data can and cannot support

SIH/SUS is a **billing system**, not a clinical registry. It supports exactly
one defensible outcome: in-hospital death among stays billed for ICU days.
There are no severity scores, no physiologic variables, no comorbidity index.

Five limits follow, and they shape every design decision in this repository:

1. **No real risk adjustment is possible** — only crude case-mix adjustment on
   age, sex, diagnosis group, urgency and procedure. Expect a reference model
   c-statistic around 0.75–0.80, not the 0.85+ a severity-scored registry
   reaches. The figure is published on the methodology page.
2. **Transfers censor the outcome.** A patient transferred out and dying
   elsewhere is not counted at the first hospital. Hospitals that transfer
   heavily look better than they are.
3. **It is SUS-only.** Private-plan coverage varies from under 5% to over 40%
   across municípios, so the SUS ICU population is a different selection in
   each. This is a confounder, not noise, and it is carried as a context
   variable.
4. **ICU exposure is a billed quantity**, counted per billing month, so long
   stays are split across records. See invariant 1 in `AGENTS.md`.
5. **The worst failure is invisible.** Someone who dies before reaching an ICU
   never generates an ICU stay. A município whose system fails earliest can post
   an excellent conditional mortality. This is why the access measure is always
   shown beside the outcome, and why SIM is on the roadmap.

## Architecture in one paragraph

Everything heavy runs offline. `pipeline/` downloads, transforms, models and
emits a handful of small JSON files into `site/data/`. `site/` is static HTML
that reads them. A GitHub Actions workflow runs the pipeline on a schedule and
deploys the site. The browser never sees a record-level row.

## Non-goals for version 1

- A national zoomable map (see `docs/decisions/0003-no-national-map-in-v1.md`)
- Hospital-level (CNES) publication — a different project with different ethics
- Any form of ranking, score, grade or top-N list
- Linking SIH to any other dataset at individual level
