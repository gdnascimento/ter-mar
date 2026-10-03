/**
 * pt-BR number formatting. Decimal comma, thousands point.
 * Suppressed values render as an em dash, never 0, null or NaN.
 */

const n0 = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 0 });
const n1 = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const n2 = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export const DASH = '—';

/** @param {number|null} v */
export function count(v) {
  return v === null || v === undefined ? DASH : n0.format(v);
}

/** @param {number|null} v */
export function rate(v) {
  return v === null || v === undefined ? DASH : n1.format(v);
}

/** @param {number|null} v */
export function percent(v) {
  return v === null || v === undefined ? DASH : `${n1.format(v)}%`;
}

/**
 * The SMR with its interval. Invariant 4: there is no formatter that renders a
 * point estimate without its interval.
 *
 * @param {number|null} smr
 * @param {[number,number]|null} ci
 */
export function smrWithInterval(smr, ci) {
  if (smr === null || ci === null) return DASH;
  return `${n2.format(smr)} (IC 95%: ${n2.format(ci[0])}–${n2.format(ci[1])})`;
}
