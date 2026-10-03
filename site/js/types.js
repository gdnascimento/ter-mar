/**
 * Type definitions mirroring `schemas/`. No runtime code.
 *
 * If you change a schema, change this file in the same commit
 * (docs/decisions/0005-no-build-step.md).
 *
 * @module types
 */

/** @typedef {'within'|'above'|'below'|'insufficient'} Verdict */

/**
 * @typedef {object} Outcome
 * @property {number} stays
 * @property {number} observed_deaths
 * @property {number} expected_deaths
 * @property {number|null} smr          Null when suppressed. Never 0, never absent.
 * @property {[number,number]|null} smr_ci
 * @property {number|null} p_value
 * @property {Verdict} verdict
 * @property {boolean} suppressed
 */

/**
 * @typedef {Outcome & {
 *   stays_per_100k: number,
 *   treated_outside_pct: number
 * }} ResidenceView
 */

/**
 * @typedef {Outcome & {
 *   has_icu: boolean,
 *   icu_beds: number,
 *   icu_beds_per_100k: number,
 *   from_other_municipalities_pct: number|null
 * }} ProviderView
 */

/**
 * @typedef {object} Municipality
 * @property {number} code             7-digit IBGE code.
 * @property {string} name
 * @property {string} uf
 * @property {string} health_region
 * @property {number} population
 * @property {ResidenceView} residence
 * @property {ProviderView} provider
 * @property {{private_coverage_pct: number|null}} context
 */

/**
 * @typedef {object} Meta
 * @property {string} model_version
 * @property {string} generated_at
 * @property {string} datasus_extracted_at
 * @property {string} ibge_vintage
 * @property {{start: string, end: string, label: string}} window
 * @property {{min_expected_deaths: number, min_stays: number}} suppression
 * @property {number} verdict_alpha
 * @property {{kind: string, c_statistic: number, strata_count: number}} reference_model
 * @property {Record<string, ViewMeta>} views
 */

/**
 * @typedef {object} ViewMeta
 * @property {number} phi
 * @property {{alpha: number, nu: number, s2_clamped: boolean}} prior
 * @property {number} municipalities_total
 * @property {number} municipalities_published
 * @property {number} expected_false_flags
 */

/**
 * @typedef {object} FunnelCurves
 * @property {'residence'|'provider'} view
 * @property {number} phi               Display only; limits are already adjusted.
 * @property {number[]} expected_grid
 * @property {{p95: Band, p998: Band}} limits
 */

/** @typedef {{lower: number[], upper: number[]}} Band */

export {};
