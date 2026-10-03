/**
 * The funnel plot. The centrepiece of each tab, not an appendix — it is what
 * stops the page being read as a ranking.
 *
 * Curves come from data/funnel/{view}.json already overdispersion-adjusted; the
 * points are derived from municipios.json. The browser does no statistics.
 *
 * Accessibility contract (docs/04-frontend.md): `role="img"` with an
 * `aria-label` that states this município's verdict in words, plus a table
 * alternative reachable without a mouse. Verdict is never carried by colour
 * alone.
 *
 * @module funnel
 */

/**
 * @param {HTMLElement} root
 * @param {import('./types.js').FunnelCurves} curves
 * @param {import('./types.js').Municipality[]} peers
 * @param {import('./types.js').Municipality} selected
 * @param {'residence'|'provider'} view
 */
export function render(root, curves, peers, selected, view) {
  throw new Error('not implemented');
}

/** Table alternative with the same numbers, for screen readers and keyboards. */
export function renderTableAlternative(root, peers, selected, view) {
  throw new Error('not implemented');
}
